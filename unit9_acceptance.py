#!/usr/bin/env python3
"""Unit 9 mocked acceptance harness; authoring this file does not run trials.

Use Python 3.11–3.13 with the project's existing Flask dependency installed.
Run ONLY after explicit authorization, in a fresh process:
    python unit9_acceptance.py --phase before --trial 1
    python unit9_acceptance.py --phase after --trial 1
Run trials 2 and 3 separately. There is no automatic multi-trial mode.

Specification: criteria.md at commit eb0d981. Each invocation sends exactly
27 Flask test-client requests if setup succeeds; no live server is started.
The phase is a label, NOT a checkout operation or a claim about baseline code.
Use the intended code state yourself; disclose an instrumented baseline with
--baseline-kind instrumented (the default is unspecified).

Evidence goes to results/unit9_acceptance/PHASE-trial-N/. An existing trial
directory is refused, including one left by an interrupted run. Never delete
official evidence simply to rerun; review it and preserve it first.

Only the temporary audit destination is used for app writes. Its exact bytes
are archived before temporary cleanup, even after ordinary execution errors.
If archival fails, the original directory is retained and its absolute recovery
path is printed to stderr and included in the available evidence report.
Assertions continue across fixtures and failures produce nonzero exit status.
Reports use application timing events only: no synthetic duration, real-model
latency, cold-start result, cost estimate, or invented baseline is supplied.
Current app timing starts in before_request, not at WSGI entry, and excludes
earlier Flask setup, timing persistence, transmission, and teardown.
Before requests, read-only Git checks enforce pinned criteria bytes, fixtures
independently reconstructed from committed tables, and approved configuration.
Application revisions may differ between phases; actual provenance is recorded.
"""

import argparse
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import call, patch
import uuid


ROOT = Path(__file__).resolve().parent
SPEC_COMMIT = "eb0d981"
# Independently established from approved Git objects, not current fixtures().
APPROVED_SPEC_REVISION = "eb0d981ecb685695c0c795c12819f5f27dd907d8"
APPROVED_SPEC_SHA256 = "293a1fff9bc23f7bc61da1289844de1fa2a927f277d20d2f270206c6acbd33f3"
APPROVED_CONFIG_SHA256 = "611242708a5b92fc04f6eefa187bb74f10cef7648a9b5cb1d1d27d98541b9f6b"
# config.py at the approved commit, with criteria-mandated limiter isolation.
APPROVED_APPLICATION_CONFIG = {
    "HUMAN_THRESHOLD": 0.35,
    "AI_THRESHOLD": 0.72,
    "WEIGHT_MODEL_SIGNAL": 0.5,
    "WEIGHT_STYLE_SIGNAL": 0.5,
    "DETECTOR_MODEL": "gpt2",
    "DETECTOR_MAX_TOKENS": 400,
    "RATE_LIMITING_ENABLED": False,
}
DETECTION_FIELDS = (
    "content_id", "guess", "confidence", "label", "model_score", "style_score",
)
CRITERIA = {
    1: ("Punctuation-only validation", 5),
    2: ("Structured rejection logging", 5),
    3: ("Legitimate-writing preservation", 5),
    4: ("Numbers/control-character rejection", 6),
    5: ("Request-timing instrumentation", 6),
}
EXPECTED_IDS = (
    "P01", "P02", "P03", "P04", "P05",
    "R01", "R02", "R03", "R04", "R05",
    "W01", "W02", "W03", "W04", "W05",
    "N01", "N02", "N03", "C01", "C02", "C03",
    "T01", "T02", "T03", "T04", "T05", "T06",
)


def fixtures():
    """Return fresh frozen bodies; timing cases reuse entire original bodies."""
    cases = []

    def add(case_id, criterion, text, reason=None, success=False):
        cases.append({
            "case_id": case_id,
            "criterion": criterion,
            "body": {"creator_id": f"u9-{case_id}", "text": text},
            "expected_creator": f"u9-{case_id}",
            "expected_status": 200 if success else 400,
            "expected_reason": reason,
        })

    for case_id, text in (
        ("P01", "!!! ??? ..."),
        ("P02", ",,, ;;; :::"),
        ("P03", "--- ___ ..."),
        ("P04", "((( ))) [[[]]]"),
        ("P05", "… … …"),
    ):
        add(case_id, 1, text, "text_has_no_letters")

    for case_id, body, reason, creator, raw in (
        ("R01", '{"creator_id":"u9-R01","text":',
         "invalid_json_object", "unknown", True),
        ("R02", [], "invalid_json_object", "unknown", False),
        ("R03", {"text": "I enjoyed walking beside the river this morning."},
         "invalid_creator_id", "unknown", False),
        ("R04", {"creator_id": "u9-R04"}, "invalid_text", "u9-R04", False),
        ("R05", {"creator_id": "u9-R05", "text": "!!! ??? ..."},
         "text_has_no_letters", "u9-R05", False),
    ):
        cases.append({
            "case_id": case_id, "criterion": 2, "body": body, "raw": raw,
            "expected_creator": creator, "expected_status": 400,
            "expected_reason": reason,
        })

    for case_id, text in (
        ("W01", "I enjoyed walking beside the river this morning."),
        ("W02", "My notes describe the garden.\n\tThe flowers opened after the rain."),
        ("W03", "Après le déjeuner, Élodie a visité le musée du quartier."),
        ("W04", "María escribió una reflexión sobre la educación y la comunicación."),
        ("W05", "João escreveu sobre a experiência de conhecer uma cidade histórica."),
    ):
        add(case_id, 3, text, success=True)

    for case_id, text, reason in (
        ("N01", "123 456 789", "text_has_no_letters"),
        ("N02", "000 42 9000", "text_has_no_letters"),
        ("N03", "١٢٣ ٤٥٦ ٧٨٩", "text_has_no_letters"),
        ("C01", "\u0000 \u0000 \u0000", "disallowed_control_character"),
        ("C02", "\u0001 \u0002 \u0003", "disallowed_control_character"),
        ("C03", "\u007f \u007f \u007f", "disallowed_control_character"),
    ):
        add(case_id, 4, text, reason)

    originals = {case["case_id"]: case for case in cases}
    for timing_id, original_id in (
        ("T01", "W01"), ("T02", "W03"), ("T03", "W04"),
        ("T04", "P01"), ("T05", "N01"), ("T06", "C01"),
    ):
        cases.append({
            **originals[original_id], "case_id": timing_id,
            "criterion": 5, "reuses": original_id,
            "body": dict(originals[original_id]["body"]),
        })
    if tuple(case["case_id"] for case in cases) != EXPECTED_IDS or len(cases) != 27:
        raise ValueError("Frozen fixture count/order must be exactly 27.")
    for number, (_, target) in CRITERIA.items():
        if sum(case["criterion"] == number for case in cases) != target:
            raise ValueError(f"Incorrect frozen count for criterion {number}.")
    return cases


def strict_json(text):
    """Reject nonstandard numbers and duplicate keys as well as invalid JSON."""
    def reject_constant(value):
        raise ValueError(f"Nonstandard JSON constant: {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"Nonfinite JSON number: {value}")
        return number

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(
        text, parse_constant=reject_constant, object_pairs_hook=unique_object,
        parse_float=finite_float,
    )


def git_bytes(*arguments):
    """Read Git metadata/objects without optional index locks or replacement refs."""
    result = subprocess.run(
        ["git", "--no-pager", "-C", str(ROOT), *arguments],
        capture_output=True, check=False, timeout=30,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_NO_REPLACE_OBJECTS": "1"},
    )
    if result.returncode:
        raise RuntimeError(
            f"Provenance Git command failed ({' '.join(arguments)}): "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return result.stdout


def require_provenance(report, name, condition, detail):
    report.setdefault("provenance_checks", {})[name] = {
        "verified": bool(condition), "detail": detail,
    }
    if not condition:
        raise RuntimeError(f"Provenance check failed [{name}]: {detail}")


def approved_manifest(committed_text):
    """Reconstruct expectations from pinned criteria, never from fixtures()."""
    unit9 = committed_text.split(
        "# Unit 9 — Capstone acceptance criteria and frozen fixtures\n", 1,
    )[1]
    sections = {}
    targets = {}
    for match in re.finditer(r"^## ([1-5])\. (.+)$", unit9, re.MULTILINE):
        number = int(match.group(1))
        section = unit9[match.end():].split("\n## ", 1)[0]
        sections[number] = section
        target = re.search(r"\*\*Target:\*\* (\d+) of (\d+) fixtures", section)
        if target is None or target.group(1) != target.group(2):
            raise ValueError(f"Cannot establish approved target {number}.")
        targets[number] = (match.group(2), int(target.group(2)))

    def table(number):
        rows = []
        for line in sections[number].splitlines():
            if not re.match(r"^\| (?:P|R|W|N|C|T)\d{2} \|", line):
                continue
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            rows.append([
                cell[1:-1] if cell.startswith("`") and cell.endswith("`") else cell
                for cell in cells
            ])
        return rows

    reference = []
    for number in (1, 2, 3, 4):
        if number != 2:
            status = int(re.search(r"HTTP status is (\d+)", sections[number]).group(1))
        for cells in table(number):
            case_id = cells[0]
            if number == 2:
                raw = case_id == "R01"
                reference.append({
                    "case_id": case_id, "criterion": number,
                    "body": cells[1] if raw else strict_json(cells[1]),
                    "raw": raw, "expected_creator": strict_json(cells[3]),
                    "expected_status": int(cells[4]), "expected_reason": cells[2],
                })
                continue
            reason = None
            if number == 1:
                reason = re.search(
                    r"matching rejection reason is `([^`]+)`", sections[1],
                ).group(1)
            elif number == 4:
                reason = cells[3]
            reference.append({
                "case_id": case_id, "criterion": number,
                "body": {"creator_id": f"u9-{case_id}", "text": strict_json(cells[1])},
                "expected_creator": f"u9-{case_id}",
                "expected_status": status, "expected_reason": reason,
            })
    originals = {case["case_id"]: case for case in reference}
    for case_id, original_id, outcome, status in table(5):
        original = originals[original_id]
        if int(status) != original["expected_status"] or outcome != (
            "success" if int(status) == 200 else "rejected"
        ):
            raise ValueError(f"Inconsistent approved timing case {case_id}.")
        reference.append({
            **original, "case_id": case_id, "criterion": 5, "reuses": original_id,
            "body": dict(original["body"]),
        })
    if len(reference) != 27 or sum(target[1] for target in targets.values()) != 27:
        raise ValueError("Approved reference must define exactly 27 requests.")
    return reference, targets


def verify_specification(report, cases):
    metadata = report.setdefault("provenance", {})
    metadata["approved_criteria_commit"] = APPROVED_SPEC_REVISION
    metadata["tested_git_revision"] = git_bytes("rev-parse", "HEAD").decode().strip()
    metadata["working_tree_status"] = git_bytes(
        "status", "--porcelain=v1", "--untracked-files=normal",
    ).decode("utf-8", errors="replace")
    metadata["working_tree_capture"] = "Before requests; output directory reserved."
    for name, arguments in (
        ("unstaged_diff_sha256", ("diff", "--no-ext-diff", "--binary")),
        ("staged_diff_sha256", ("diff", "--cached", "--no-ext-diff", "--binary")),
    ):
        metadata[name] = hashlib.sha256(git_bytes(
            *arguments, "--", "app.py", "audit.py", "config.py", "detector.py",
            "stylometry.py", "scoring.py", "criteria.md", "unit9_acceptance.py",
        )).hexdigest()
    resolved = git_bytes("rev-parse", f"{SPEC_COMMIT}^{{commit}}").decode().strip()
    require_provenance(report, "approved_commit", resolved == APPROVED_SPEC_REVISION,
                       f"Expected {APPROVED_SPEC_REVISION}; resolved {resolved}.")
    committed = git_bytes("show", f"{APPROVED_SPEC_REVISION}:criteria.md")
    reference_sha = hashlib.sha256(committed).hexdigest()
    metadata["approved_specification_sha256"] = reference_sha
    require_provenance(report, "approved_criteria_object",
                       reference_sha == APPROVED_SPEC_SHA256,
                       f"Expected SHA-256 {APPROVED_SPEC_SHA256}; got {reference_sha}.")
    current = (ROOT / "criteria.md").read_bytes()
    metadata["current_specification_sha256"] = hashlib.sha256(current).hexdigest()
    require_provenance(report, "current_criteria_bytes", current == committed,
                       "Current criteria.md must byte-match the approved Git object.")
    committed_config = git_bytes("show", f"{APPROVED_SPEC_REVISION}:config.py")
    metadata["approved_config_source_sha256"] = hashlib.sha256(committed_config).hexdigest()
    require_provenance(
        report, "approved_config_object",
        metadata["approved_config_source_sha256"] == APPROVED_CONFIG_SHA256,
        "The committed configuration reference must match its pinned SHA-256.",
    )
    try:
        reference, targets = approved_manifest(committed.decode("utf-8"))
    except (ValueError, KeyError, IndexError, AttributeError) as exc:
        require_provenance(report, "approved_manifest_parsing", False, str(exc))
    metadata["approved_fixture_sha256"] = hashlib.sha256(json.dumps(
        reference, ensure_ascii=True, sort_keys=True,
    ).encode("utf-8")).hexdigest()
    metadata["current_fixture_sha256"] = report["fixture_sha256"]
    metadata["approved_targets"] = targets
    require_provenance(report, "frozen_fixtures",
                       cases == reference and report["fixture_sha256"] == metadata["approved_fixture_sha256"],
                       "All 27 bodies, IDs, creators, outcomes and reasons must match committed tables.")
    require_provenance(report, "criterion_targets",
                       json.dumps(CRITERIA, sort_keys=True) == json.dumps(targets, sort_keys=True),
                       "Criterion names and targets must match the committed criteria.")


def provenance_value(value):
    """Keep invalid runtime settings reportable without emitting nonfinite JSON."""
    if type(value) in (type(None), bool, int, str):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    return {"type": type(value).__name__, "representation": repr(value)}


def verify_configuration(report, config, app, model, style, temporary_dir, audit_path):
    observed = {
        key: getattr(config, key, None) for key in APPROVED_APPLICATION_CONFIG
    }
    report["provenance"]["approved_application_configuration"] = APPROVED_APPLICATION_CONFIG
    report["provenance"]["observed_application_configuration"] = {
        key: provenance_value(value) for key, value in observed.items()
    }
    report["scoring_configuration"] = {
        key: provenance_value(observed[key]) for key in (
            "HUMAN_THRESHOLD", "AI_THRESHOLD", "WEIGHT_MODEL_SIGNAL", "WEIGHT_STYLE_SIGNAL",
        )
    }
    for key, expected in APPROVED_APPLICATION_CONFIG.items():
        actual = observed[key]
        require_provenance(
            report, f"configuration.{key}",
            type(actual) is type(expected) and actual == expected,
            f"Expected {expected!r}; observed {actual!r}.",
        )
    expected_test = {
        "AI201_RATE_LIMITS": "0", "TESTING": True, "DEBUG": False,
        "PROPAGATE_EXCEPTIONS": False, "model_mock_return": 0.5,
        "style_mock_return": 0.5,
    }
    actual_test = {
        "AI201_RATE_LIMITS": os.environ.get("AI201_RATE_LIMITS"),
        **{key: app.config.get(key) for key in (
            "TESTING", "DEBUG", "PROPAGATE_EXCEPTIONS",
        )},
        "model_mock_return": model.return_value, "style_mock_return": style.return_value,
    }
    report["provenance"]["approved_test_configuration"] = expected_test
    report["provenance"]["observed_test_configuration"] = {
        key: provenance_value(value) for key, value in actual_test.items()
    }
    for key, expected in expected_test.items():
        actual = actual_test[key]
        require_provenance(
            report, f"test_configuration.{key}",
            type(actual) is type(expected) and actual == expected,
            f"Expected {expected!r}; observed {actual!r}.",
        )
    report["provenance"]["isolated_audit_paths"] = {
        "LOG_DIR": str(config.LOG_DIR), "AUDIT_LOG": str(config.AUDIT_LOG),
    }
    require_provenance(
        report, "isolated_audit_paths",
        config.LOG_DIR == temporary_dir and config.AUDIT_LOG == audit_path,
        "Both audit paths must point to this trial's dedicated temporary destination.",
    )


def read_audit(path):
    entries, failures = [], []
    if not path.exists():
        return [], ["Dedicated audit file was not created."]
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        return [], [f"Audit read failed: {type(exc).__name__}: {exc}"]
    for line_number, line in enumerate(text.splitlines(), 1):
        try:
            entry = strict_json(line)
            if not isinstance(entry, dict):
                raise ValueError("Audit line is not a JSON object.")
            entries.append(entry)
        except (ValueError, TypeError) as exc:
            failures.append(f"Audit line {line_number}: {exc}")
    if text and not text.endswith("\n"):
        failures.append("Audit file lacks its final newline; possible partial write.")
    return entries, failures


def valid_uuid(value):
    try:
        parsed = uuid.UUID(value)
        return parsed.version == 4 and str(parsed) == value
    except (ValueError, TypeError, AttributeError):
        return False


def valid_timestamp(value):
    try:
        parsed = datetime.fromisoformat(value)
        return parsed.tzinfo is not None and parsed.utcoffset() == timedelta(0)
    except (ValueError, TypeError):
        return False


def finite_number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def check(row, label, assertion, *args):
    """Collect unittest assertions without stopping at the first failure."""
    try:
        assertion(*args)
    except AssertionError as exc:
        row["failures"].append(f"{label}: {exc}")


def observe_requests(client, cases, model, style, load_guard):
    rows = []
    for case in cases:
        model.reset_mock()
        style.reset_mock()
        load_guard.reset_mock()
        row = {
            "case_id": case["case_id"], "criterion": case["criterion"],
            "expected_http_status": case["expected_status"],
            "actual_http_status": None, "request_id": None,
            "response_body": None, "failures": [],
        }
        try:
            kwargs = (
                {"data": case["body"], "content_type": "application/json"}
                if case.get("raw")
                else {"json": case["body"], "content_type": "application/json"}
            )
            response = client.post("/submit", **kwargs)
            row["actual_http_status"] = response.status_code
            row["request_id"] = response.headers.get("X-Request-ID")
            row["request_id_header_count"] = len(
                response.headers.getlist("X-Request-ID")
            )
            row["response_body"] = response.get_data(as_text=True)
        except Exception as exc:
            row["failures"].append(f"Request raised {type(exc).__name__}: {exc}")
        body = case["body"]
        text = body.get("text") if isinstance(body, dict) else None
        expected_calls = [call(text)] if case["expected_status"] == 200 else []
        row["scoring"] = {
            "expected_model_calls": len(expected_calls),
            "model_calls": model.call_count,
            "model_call_args": [repr(item) for item in model.call_args_list],
            "model_arguments_match": model.call_args_list == expected_calls,
            "expected_style_calls": len(expected_calls),
            "style_calls": style.call_count,
            "style_call_args": [repr(item) for item in style.call_args_list],
            "style_arguments_match": style.call_args_list == expected_calls,
            "model_load_attempts": load_guard.call_count,
        }
        rows.append(row)
    return rows


def validate_rows(cases, rows, entries, scoring):
    assertions = unittest.TestCase()
    seen = set()
    combined = scoring.combine_signals(0.5, 0.5)
    guess, label = scoring.score_to_label(combined)
    for case, row in zip(cases, rows):
        def equal(name, actual, expected):
            check(row, name, assertions.assertEqual, actual, expected)

        def truth(name, value):
            check(row, name, assertions.assertTrue, value)

        request_id = row["request_id"]
        equal("HTTP status", row["actual_http_status"], case["expected_status"])
        truth("UUID4 request ID", valid_uuid(request_id))
        equal("single X-Request-ID header", row.get("request_id_header_count"), 1)
        truth("unique request ID", bool(request_id) and request_id not in seen)
        if request_id:
            seen.add(request_id)
        observations = row["scoring"]
        equal("model call count", observations["model_calls"],
              observations["expected_model_calls"])
        equal("style call count", observations["style_calls"],
              observations["expected_style_calls"])
        truth("original model argument", observations["model_arguments_match"])
        truth("original style argument", observations["style_arguments_match"])
        equal("no model loading", observations["model_load_attempts"], 0)
        try:
            body = strict_json(row["response_body"])
            if not isinstance(body, dict):
                raise ValueError("Response is not a JSON object.")
        except (ValueError, TypeError) as exc:
            row["failures"].append(f"Response JSON: {exc}")
            body = {}
        success = case["expected_status"] == 200
        if success:
            for field in DETECTION_FIELDS:
                truth(f"populated response {field}", body.get(field) is not None)
            truth("content ID", valid_uuid(body.get("content_id")))
            for field, value in (
                ("model_score", 0.5), ("style_score", 0.5),
                ("confidence", combined), ("guess", guess), ("label", label),
            ):
                equal(f"response {field}", body.get(field), value)
        else:
            for field in DETECTION_FIELDS:
                equal(f"no detection {field}", body.get(field), None)
            truth("error-only response fields",
                  set(body) <= {"error", "message", "request_id", *DETECTION_FIELDS})
            equal("bad-request error", body.get("error"), "bad_request")
            truth("clear error message",
                  isinstance(body.get("message"), str) and bool(body["message"]))

        # Never match missing IDs to null-ID rows or infer correlation by order.
        matching = [
            entry for entry in entries if request_id
            and entry.get("request_id") == request_id
        ]
        rejected = [e for e in matching if e.get("event") == "rejected"]
        timing = [e for e in matching if e.get("event") == "request_timing"]
        # Existing log_decision has no event key; preserve that legacy contract.
        decisions = [
            e for e in matching if "event" not in e and e.get("status") == "decided"
        ]
        row["audit_counts"] = {
            "total": len(matching), "rejection": len(rejected),
            "decision": len(decisions), "timing": len(timing),
        }
        row["matching_audit_records"] = matching
        equal("total correlated records", len(matching), 2)
        equal("rejection count", len(rejected), 0 if success else 1)
        equal("decision count", len(decisions), 1 if success else 0)
        equal("timing count", len(timing), 1)
        for entry in matching:
            truth("UTC audit timestamp", valid_timestamp(entry.get("timestamp")))
            equal("audit request ID", entry.get("request_id"), request_id)
        for entry in rejected:
            equal("rejection status", entry.get("status"), "rejected")
            equal("rejection reason", entry.get("reason"), case["expected_reason"])
            equal("rejection creator", entry.get("creator_id"),
                  case["expected_creator"])
            truth("integer rejection HTTP status",
                  type(entry.get("http_status")) is int)
            equal("rejection HTTP status", entry.get("http_status"), 400)
            truth("privacy-safe rejection fields", set(entry) <= {
                "timestamp", "event", "status", "reason", "creator_id",
                "request_id", "http_status",
            })
        for entry in decisions:
            equal("decision creator", entry.get("creator_id"),
                  case["expected_creator"])
            equal("decision content ID", entry.get("content_id"),
                  body.get("content_id"))
            for field, value in (
                ("model_score", 0.5), ("style_score", 0.5),
                ("combined_score", combined), ("guess", guess), ("label", label),
            ):
                equal(f"decision {field}", entry.get(field), value)
        for entry in timing:
            equal("timing outcome", entry.get("outcome"),
                  "success" if success else "rejected")
            truth("integer timing HTTP status", type(entry.get("http_status")) is int)
            equal("timing expected HTTP status", entry.get("http_status"),
                  case["expected_status"])
            equal("timing actual HTTP status", entry.get("http_status"),
                  row["actual_http_status"])
            duration = entry.get("duration_ms")
            truth("finite nonnegative duration",
                  finite_number(duration) and duration >= 0)
            equal("timing record fields", set(entry), {
                "timestamp", "event", "request_id", "duration_ms", "outcome",
                "http_status",
            })


def run_trial(report, destination):
    cases = fixtures()
    report["fixtures"] = cases
    encoded = json.dumps(cases, ensure_ascii=True, sort_keys=True).encode("utf-8")
    report["fixture_sha256"] = hashlib.sha256(encoded).hexdigest()
    verify_specification(report, cases)
    if any(name in sys.modules for name in (
        "app", "config", "audit", "detector", "stylometry", "scoring",
    )):
        raise RuntimeError("Use a fresh process; project modules are already imported.")
    with ExitStack() as temporary_cleanup:
        temporary_dir = Path(tempfile.mkdtemp(prefix="unit9-acceptance-")).resolve()
        audit_path = temporary_dir / "audit.jsonl"
        report["audit_temporary_directory"] = str(temporary_dir)
        try:
            with ExitStack() as stack:
                stack.enter_context(patch.dict(os.environ, {"AI201_RATE_LIMITS": "0"}))
                stack.enter_context(patch.object(sys, "dont_write_bytecode", True))
                config = importlib.import_module("config")
                stack.enter_context(patch.object(config, "LOG_DIR", temporary_dir))
                stack.enter_context(patch.object(config, "AUDIT_LOG", audit_path))
                model = stack.enter_context(patch(
                    "detector.model_signal", return_value=0.5,
                ))
                style = stack.enter_context(patch(
                    "stylometry.style_signal", return_value=0.5,
                ))
                load_guard = stack.enter_context(patch(
                    "detector._load",
                    side_effect=AssertionError("Real model loading is forbidden."),
                ))
                appmod = importlib.import_module("app")
                scoring = importlib.import_module("scoring")
                if config.RATE_LIMITING_ENABLED:
                    raise RuntimeError("Rate-limit isolation did not take effect.")
                report["scoring_configuration"] = {
                    key: getattr(config, key) for key in (
                        "HUMAN_THRESHOLD", "AI_THRESHOLD",
                        "WEIGHT_MODEL_SIGNAL", "WEIGHT_STYLE_SIGNAL",
                    )
                }
                stack.enter_context(patch.dict(appmod.app.config, {
                    "TESTING": True, "DEBUG": False, "PROPAGATE_EXCEPTIONS": False,
                }))
                verify_configuration(
                    report, config, appmod.app, model, style, temporary_dir, audit_path,
                )
                report["rows"] = observe_requests(
                    appmod.app.test_client(), cases, model, style, load_guard,
                )
                report["requests_attempted"] = len(report["rows"])
                entries, failures = read_audit(audit_path)
                report["trial_failures"].extend(failures)
                validate_rows(cases, report["rows"], entries, scoring)
                returned_ids = {
                    row["request_id"] for row in report["rows"] if row["request_id"]
                }
                orphan_count = sum(
                    not isinstance(entry.get("request_id"), str)
                    or entry["request_id"] not in returned_ids
                    for entry in entries
                )
                if orphan_count:
                    report["trial_failures"].append(
                        f"{orphan_count} audit records lack a matching response ID."
                    )
                report["audit_record_count"] = len(entries)
                if len(entries) != 54:
                    report["trial_failures"].append(
                        f"Expected 54 total audit records; observed {len(entries)}."
                    )
        finally:
            report["audit_file_created"] = audit_path.exists()
            report["audit_archived"] = False
            if audit_path.exists():
                try:
                    original_bytes = audit_path.read_bytes()
                    archive_path = destination / "audit.jsonl"
                    with archive_path.open("xb") as saved:
                        saved.write(original_bytes)
                        saved.flush()
                        os.fsync(saved.fileno())
                    if archive_path.read_bytes() != original_bytes:
                        raise OSError("Archived audit bytes do not match the source.")
                except BaseException:
                    report["audit_recovery_path"] = str(audit_path)
                    message = (
                        "Audit archival failed; temporary evidence was retained. "
                        f"Recovery directory: {temporary_dir}; audit file: {audit_path}"
                    )
                    report["trial_failures"].append(message)
                    print(message, file=sys.stderr)
                    raise
                report["audit_archived"] = True
                temporary_cleanup.callback(shutil.rmtree, temporary_dir)
            else:
                # No audit exists to preserve; remove only an empty directory.
                temporary_cleanup.callback(temporary_dir.rmdir)


def save_reports(report, destination):
    rows = report["rows"]
    if len(rows) != 27:
        report["trial_failures"].append(
            f"Trial incomplete: expected 27 attempted requests, observed {len(rows)}."
        )
    report["criteria"] = {}
    for number, (name, target) in CRITERIA.items():
        group = [row for row in rows if row["criterion"] == number]
        met = (
            len(group) == target and not report["trial_failures"]
            and all(not row["failures"] for row in group)
        )
        report["criteria"][str(number)] = {
            "name": name, "target": target,
            "fixtures_without_failures": sum(not row["failures"] for row in group),
            "verdict": "MET" if met else "MISSED",
        }
    report["passed"] = all(
        item["verdict"] == "MET" for item in report["criteria"].values()
    )
    with (destination / "report.json").open("x", encoding="utf-8") as output:
        json.dump(report, output, ensure_ascii=True, indent=2, allow_nan=False)
        output.write("\n")
    lines = [
        f"Unit 9 {report['phase']} trial {report['trial']}",
        f"Baseline designation: {report['baseline_kind']}",
        "Mocked acceptance evidence only; not real GPT-2 performance or cost.",
        f"Requests attempted: {len(rows)}/27",
    ]
    for number, item in report["criteria"].items():
        lines.append(
            f"Criterion {number}: {item['verdict']} "
            f"({item['fixtures_without_failures']}/{item['target']} fixtures "
            "without fixture-level failures; trial-level failures also apply)"
        )
    for row in rows:
        observations = row["scoring"]
        lines.append(
            f"{row['case_id']}: HTTP expected={row['expected_http_status']} "
            f"actual={row['actual_http_status']}; request_id={row['request_id']}; "
            f"model={observations['model_calls']}/"
            f"{observations['expected_model_calls']}, "
            f"style={observations['style_calls']}/"
            f"{observations['expected_style_calls']}; "
            f"audit={row.get('audit_counts', 'unavailable')}"
        )
        lines.append(
            "  Original-text arguments: "
            f"model={observations['model_arguments_match']}, "
            f"style={observations['style_arguments_match']}"
        )
        lines.extend(f"  FAILURE: {failure}" for failure in row["failures"])
    lines.extend(f"TRIAL FAILURE: {failure}" for failure in report["trial_failures"])
    summary = "\n".join(lines) + "\n"
    with (destination / "summary.txt").open("x", encoding="utf-8") as output:
        output.write(summary)
    print(summary, end="")
    print(f"Evidence: {destination}")
    return 0 if report["passed"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=("before", "after"))
    parser.add_argument("--trial", required=True, type=int, choices=(1, 2, 3))
    parser.add_argument(
        "--baseline-kind", choices=("untouched", "instrumented", "unspecified"),
        default="unspecified",
        help="Explicit provenance label, not inferred from the phase.",
    )
    args = parser.parse_args()
    if not (3, 11) <= sys.version_info[:2] < (3, 14):
        parser.error("Project supports Python 3.11–3.13.")
    destination = ROOT / "results" / "unit9_acceptance" / (
        f"{args.phase}-trial-{args.trial}"
    )
    try:
        destination.mkdir(parents=True, exist_ok=False)
    except OSError as exc:
        parser.error(f"Cannot reserve new evidence directory (no overwrite): {exc}")
    report = {
        "phase": args.phase, "trial": args.trial,
        "baseline_kind": args.baseline_kind, "specification_commit": SPEC_COMMIT,
        "report_timestamp": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "rows": [], "trial_failures": [],
        "requests_attempted": 0,
        "measurement_mode": "mocked scoring; application timing events only",
        "source_sha256": {},
    }
    try:
        for name in (
            "criteria.md", "app.py", "audit.py", "config.py", "detector.py",
            "stylometry.py", "scoring.py", "unit9_acceptance.py",
        ):
            report["source_sha256"][name] = hashlib.sha256(
                (ROOT / name).read_bytes()
            ).hexdigest()
        report["flask_version"] = importlib.metadata.version("flask")
        run_trial(report, destination)
    except Exception as exc:
        report["trial_failures"].append(
            f"Trial execution/setup error: {type(exc).__name__}: {exc}"
        )
    try:
        return save_reports(report, destination)
    except (OSError, TypeError, ValueError) as exc:
        print(f"Evidence persistence FAILED in {destination}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
