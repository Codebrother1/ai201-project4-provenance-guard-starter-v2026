# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False-positive protection

Of 10 verified human-written samples, no more than 1 may receive the high-confidence AI label in any evaluation trial.

**Why this target:**

I chose this limit because I don't want the system to falsely accuse someone of using AI, upset them, or hurt their feelings. I want the system to protect real writers from unfair accusations.

---

## 2. Fair appeal process

All 5 out of 5 valid appeals must be successfully recorded in the audit log and have their submission status marked `under_review` in each evaluation trial.

**Revision after baseline testing:** In each evaluation trial, 5 out of 5 valid appeals must return HTTP 200, append exactly one matching appeal event with status `under_review` and recorded reasoning, and preserve the corresponding original decision and scores unchanged. This measures appeal intake and audit recording, not human adjudication. The revision matches the existing append-only audit design. It does not weaken that design or change the implemented behavior. The original sentence asks for the submission status itself to be marked `under_review`. That literal status change was not met. The new appeal event records the `under_review` status instead, and the original decision stays `decided`.

**Why this target:**

I chose this target because I want the appeal process to be fair. Everyone who submits a valid appeal should have the opportunity to challenge the system's decision and have their request recorded for review.

---

## 3. Label coverage and uncertainty

Across a test set of 10 writing samples selected to exercise the three outcomes, the system must produce all three labels (`human`, `unsure`, and `ai`) at least once in each evaluation trial.

**Why this target:**

I chose this target because I want the system to acknowledge that it can make mistakes. When the system is unsure, it should communicate that honestly rather than make an accusation that could upset someone or hurt their feelings. This gives writers a clearer understanding of the system's limitations.

---

## 4. Invalid input handling

All 5 out of 5 invalid submissions must receive an appropriate HTTP 400 error with a clear explanation, without crashing the service or producing an AI-detection result, in each evaluation trial.

**Why this target:**

I chose this target because I don't want the service to crash when someone submits invalid information. I want the system to provide clear error messages so users understand what's wrong and have an opportunity to correct their submissions.

---

## 5. Score separation

Using 5 verified human-written samples and 5 verified AI-generated samples, the average combined score for AI-generated writing must be at least 0.20 higher than the average combined score for human-written writing in each evaluation trial.

**Why this target:**

I want the system to recognize meaningful differences between human-written and AI-generated writing. I chose a difference of 0.20 because I want the scores to show some separation, while recognizing that the detector isn't perfect and could make mistakes.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 9 — Capstone acceptance criteria and frozen fixtures

## Scope and evidence status

**Project:** Project 4, Provenance Guard.

**Shape B — Harden Against Failure.** The planned extension will harden malformed-input handling on `POST /submit`, improve structured rejection logging, and add unique request IDs and server-side request timing while preserving existing legitimate-writing behavior.

**Path B — Reproducible local run with logs and evidence.** The criteria and fixtures below are student-approved targets for future testing, not claims of implemented behavior or passing results. No Unit 9 measurements, passing statuses, or measured costs are recorded here. The Unit 7/8 criteria and historical revision above remain unchanged.

## Shared fixture and assertion conventions

- Unless a complete body is specified, send `POST /submit` with `Content-Type: application/json` and JSON body `{"creator_id":"u9-CASE_ID","text":TEXT}`. Replace `CASE_ID` with the fixture ID and `TEXT` with its exact JSON string; for example, P01 uses `{"creator_id":"u9-P01","text":"!!! ??? ..."}`.
- Quoted text in the tables is a JSON string representation. Decode JSON escapes into actual characters: `\n` is a newline, `\t` is a tab, and `\u0000` is NUL. Do not submit literal backslashes instead.
- Keep literal text, request bodies, and detection thresholds fixed across trials and before/after phases. Only request correlation metadata may change.
- Every individual request must receive a unique server-generated request ID returned through the `X-Request-ID` response header, including malformed requests.
- Correlate business audit and timing records with the returned request ID, not merely timestamps, creator IDs, or content IDs. Keep a manifest mapping phase, trial, criterion, fixture ID, and returned request ID.
- A successful request must produce exactly one decision audit record. A validation rejection must produce exactly one rejection audit record and no decision record. Every tested request must produce exactly one timing record. Two different record types for one request are appropriate; duplicate business or timing records are not.
- **No detection result** means `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score` must each be absent or null. Rejected responses may contain error information and the request ID only.
- **Normal detection-response fields** are `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score`, populated through the controlled successful scoring path.
- All text fixtures that exercise the new content rules contain at least three whitespace-separated tokens. Missing-field, invalid-type, and malformed-JSON fixtures intentionally exercise earlier validation branches instead.
- Rejection audit entries must not unnecessarily contain raw submitted text. Record the request ID, reason, status, and necessary metadata rather than copying the submission into the rejection log.
- A fixture meets its target only when every required assertion holds. A correct HTTP status alone is insufficient.

## 1. Punctuation-only validation

**Target:** 5 of 5 fixtures must satisfy every assertion in each trial.

**Motivation:** Rejecting punctuation-only submissions before scoring avoids misleading decisions and wasted model processing.

| Fixture | Exact text as a JSON string |
|---|---|
| P01 | `"!!! ??? ..."` |
| P02 | `",,, ;;; :::"` |
| P03 | `"--- ___ ..."` |
| P04 | `"((( ))) [[[]]]"` |
| P05 | `"… … …"` |

P05 uses Unicode U+2026 ellipsis characters. Each fixture has three whitespace-separated tokens, so the old three-token minimum cannot be the sole reason for rejection.

**Assertions for every fixture:**

- HTTP status is 400.
- The response contains no detection result as defined above.
- `detector.model_signal()` is called zero times.
- The matching rejection reason is `text_has_no_letters`.

## 2. Structured rejection logging

**Target:** 5 of 5 fixtures must each produce exactly one matching structured rejection record in each trial.

**Motivation:** Structured records support reproducible troubleshooting and accountable failures while avoiding unnecessary storage of submitted writing.

All five requests use `POST /submit` and `Content-Type: application/json`. R01 must be sent as raw malformed JSON, not through a helper that converts it into a valid JSON string.

| Fixture | Exact request body | Expected reason | Expected creator ID | HTTP status |
|---|---|---|---|---|
| R01 | `{"creator_id":"u9-R01","text":` | `invalid_json_object` | `"unknown"` | 400 |
| R02 | `[]` | `invalid_json_object` | `"unknown"` | 400 |
| R03 | `{"text":"I enjoyed walking beside the river this morning."}` | `invalid_creator_id` | `"unknown"` | 400 |
| R04 | `{"creator_id":"u9-R04"}` | `invalid_text` | `"u9-R04"` | 400 |
| R05 | `{"creator_id":"u9-R05","text":"!!! ??? ..."}` | `text_has_no_letters` | `"u9-R05"` | 400 |

**Assertions for every fixture:**

- HTTP status is 400.
- Exactly one rejection record matches the returned request ID.
- The record contains a parseable `timestamp`, `event="rejected"`, `status="rejected"`, the expected `reason`, the expected `creator_id`, `http_status=400`, and the matching `request_id`.
- The `"unknown"` fallback is used when the body cannot be parsed as an object or does not provide a valid creator ID. Do not extract a creator ID from malformed raw JSON.
- The rejection does not also produce a decision record. Its separate timing record is expected and is not a duplicate rejection.
- Raw submitted text is not unnecessarily included in the rejection record.

## 3. Legitimate-writing preservation

**Target:** 5 of 5 fixtures must satisfy every assertion in each trial.

**Motivation:** New validation must not falsely reject legitimate writing or introduce regressions, including for accented Latin-script writing and ordinary writing whitespace.

| Fixture | Exact text as a JSON string |
|---|---|
| W01 | `"I enjoyed walking beside the river this morning."` |
| W02 | `"My notes describe the garden.\n\tThe flowers opened after the rain."` |
| W03 | `"Après le déjeuner, Élodie a visité le musée du quartier."` |
| W04 | `"María escribió una reflexión sobre la educación y la comunicación."` |
| W05 | `"João escreveu sobre a experiência de conhecer uma cidade histórica."` |

W02 contains an actual newline followed by an actual tab after JSON decoding. All five samples satisfy the existing length requirements.

**Assertions for every fixture:**

- HTTP status is 200 under controlled scoring mocks, with no validation-related HTTP 400.
- `detector.model_signal()` is called exactly once with the original decoded text.
- `stylometry.style_signal()` is called exactly once with the original decoded text.
- The response contains the normal detection-response fields.
- The request produces one decision audit record and one matching timing record.

These tests establish validation acceptance and routing only. Mock-generated labels are not evidence that authorship predictions are accurate.

## 4. Numbers/control-character rejection

**Target:** 6 of 6 fixtures must satisfy every assertion in each trial.

**Motivation:** Reject nonsensical scoring inputs before model processing to avoid misleading labels and unnecessary computation.

| Fixture | Exact text as a JSON string | Character description | Expected reason |
|---|---|---|---|
| N01 | `"123 456 789"` | ASCII digits | `text_has_no_letters` |
| N02 | `"000 42 9000"` | ASCII digits, including leading zeroes | `text_has_no_letters` |
| N03 | `"١٢٣ ٤٥٦ ٧٨٩"` | Arabic-Indic digits | `text_has_no_letters` |
| C01 | `"\u0000 \u0000 \u0000"` | Decoded NUL characters separated by spaces | `disallowed_control_character` |
| C02 | `"\u0001 \u0002 \u0003"` | Decoded SOH, STX, ETX separated by spaces | `disallowed_control_character` |
| C03 | `"\u007f \u007f \u007f"` | Decoded DEL characters separated by spaces | `disallowed_control_character` |

**Assertions for every fixture:**

- HTTP status is 400.
- The response contains no detection result as defined above.
- `detector.model_signal()` is called zero times.
- The matching rejection record contains the fixture's expected reason.

**Frozen control-character policy:** Allow ordinary tab (U+0009), newline (U+000A), and carriage return (U+000D) whitespace in otherwise legitimate writing. Reject other Unicode category `Cc` control characters. The control check must take precedence over the general no-letters check, so C01–C03 receive `disallowed_control_character`.

## 5. Request-timing instrumentation

**Target:** 6 of 6 fixtures must each produce exactly one matching timing record in each trial.

**Motivation:** Make successful and failed request execution observable and support reproducible performance/cost analysis without treating mocked durations as real model latency or measured cost.

| Timing fixture | Reused fixture body | Expected outcome | HTTP status |
|---|---|---|---|
| T01 | W01 | `success` | 200 |
| T02 | W03 | `success` | 200 |
| T03 | W04 | `success` | 200 |
| T04 | P01 | `rejected` | 400 |
| T05 | N01 | `rejected` | 400 |
| T06 | C01 | `rejected` | 400 |

Reuse the entire referenced body, including its original creator ID: T01 uses `u9-W01`, not `u9-T01`. Each timing request is a separate request with a fresh server-generated request ID.

**Assertions for every fixture:**

- The HTTP response has the expected status.
- Exactly one record has `event="request_timing"` and the returned `request_id`.
- The record has the expected `outcome` and `http_status`.
- `duration_ms` is numeric, finite, and nonnegative. Boolean values do not qualify.
- The same request ID connects the response, its single business audit record, and its single timing record.

## Frozen test protocol

### Trials and improvement sequence

1. Preserve an identifiable before-improvement code state and the frozen fixture definitions.
2. Perform three separate before-improvement trials for every criterion.
3. Each trial executes all five criterion groups separately: 5 + 5 + 5 + 6 + 6 = 27 requests. Some bodies are intentionally reused under different criteria.
4. Each phase therefore contains 81 requests across its three trials.
5. Diagnose the observed failures, then implement one evidence-based improvement.
6. Perform three after-improvement trials with the same fixture bodies, thresholds, assertions, and isolation settings.
7. Compare before/after results without weakening targets or replacing disappointing fixtures.

This is a future execution protocol, not authorization to run trials while documenting it.

### Scoring mocks and rate-limit isolation

- Use `unittest.mock.patch("detector.model_signal", return_value=0.5)` at the actual call target. The current route locally imports `detector` and calls `detector.model_signal(text)`; do not assume `app.detector` exists.
- Use `unittest.mock.patch("stylometry.style_signal", return_value=0.5)` for controlled successful cases. Both fixed scores are synthetic test inputs, not measured scores.
- Keep `scoring.combine_signals()` and `scoring.score_to_label()` real so response construction follows the existing scoring and label rules.
- For rejected cases, assert that the model mock was not called. Its harmless return value prevents accidental real scoring if an unchanged baseline lets malformed text through.
- Set the existing `AI201_RATE_LIMITS=0` setting before importing `app` in the isolated test process. Changing it after import does not undo limiter initialization. This avoids unrelated HTTP 429 interference.
- Do not change production rate limits or detection thresholds to make the acceptance tests pass.

### Dedicated audit evidence and record ownership

- Redirect writes by patching both `config.LOG_DIR` and `config.AUDIT_LOG` in the isolated test process before requests are sent.
- Use dedicated Unit 9 paths, such as `logs/unit9/<run-id>/before-trial-1.jsonl`, with distinct destinations for phases and trials.
- Preserve historical `logs/audit.jsonl`. Never call `audit.clear()`, truncate historical files, or overwrite earlier evidence.
- Keep the real audit writer for record-persistence assertions; restore patched settings afterward.
- Parse new JSONL evidence strictly. Malformed lines, missing records, unexpected records, or duplicate records must not be silently ignored.
- Define one owner for rejection appends and one owner for timing appends. Do not log the same rejection independently in a route, an error handler, and a shared finalizer.
- If a shared finalizer takes ownership of rate-limit rejection records, replace rather than supplement the existing handler's rejection write. Rate-limit behavior itself is not one of these fixed validation fixtures.

### Timing boundaries and interpretation

- Measure full server-side request handling from Flask application request-handling start through response preparation using `time.perf_counter()`.
- A proposed broad boundary is a start timestamp at WSGI entry into Flask, before request parsing and limiter handling, with the end sampled in the final response-processing hook after other response preparation and business audit writes.
- Record the exact implemented start/end locations and hook ordering with future evidence. A first `before_request` hook excludes earlier Flask context/setup work and must be identified as a narrower measurement if used.
- Document exclusions honestly: client processing, network transport, response transmission, teardown after response preparation, and the timing record's own serialization/write after its duration is sampled are not covered by that proposed boundary.
- Mocked timing trials establish record completeness, correlation, and duration-field validity. They do not measure true GPT-2 inference latency, throughput, or actual model-related cost.
- Real warm-model request durations and cold-start overhead must be measured separately later, only with explicit authorization. Do not load GPT-2 or run those measurements as part of this documentation step.
- For a later authorized real-model study, measure cold-start overhead separately; keep one persistent process, load the model and perform an unmeasured inference warm-up, then repeat the same fixed timing cases under warm-model conditions. Use the same warm-up procedure before and after.

## Reporting requirements

- Report each criterion as `MET` or `MISSED` for each of the three trials in each phase, supported by per-fixture assertions and exact evidence locations.
- A criterion is `MET` in a trial only when all of its fixtures satisfy all required assertions: 5/5, 5/5, 5/5, 6/6, and 6/6 respectively. Do not average away a failed trial.
- Record phase, trial, fixture ID, request ID when available, expected versus actual HTTP status, scoring-call observations, record counts, and assertion failures.
- Diagnose failures before selecting the one evidence-based improvement; explain the change and compare all three before/after trials.
- If the untouched baseline lacks request IDs or timing, report them as unavailable or `MISSED`. Never invent baseline records, correlations, durations, or costs.
- Clearly identify any instrumented baseline as instrumented, not untouched. HTTP responses and mocked scoring-call observations can still supply baseline evidence where other instrumentation is absent.
- Preserve Unit 7/8 results, historical logs, and Git history. Keep criteria fixed even if baseline outcomes are disappointing.

## Scope limitations and review notes

- No GPT-2 retraining, detection-threshold changes, UI rebuild, scoring-pipeline rewrite, or appeals redesign is included.
- Multilingual input acceptance does not imply reliable authorship detection across all languages.
- The legitimate-writing fixtures cover selected English and accented Latin-script samples, not every Unicode script, decomposed accent sequence, or length boundary.
- The frozen control policy covers category `Cc`; treatment of other categories such as zero-width format characters is not established by these fixtures.
- These record-persistence assertions assume a writable dedicated audit destination. Failure behavior when rejection or timing logging itself cannot write requires separate review if added to scope.
- The fixed acceptance trials use mocks. Any real-model timing study is separate evidence and needs explicit authorization.
- No criterion is claimed to pass in this document. Implementation, official trials, and measurements remain future work.
