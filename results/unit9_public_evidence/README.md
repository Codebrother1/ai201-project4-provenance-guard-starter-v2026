# Unit 9 publication evidence copies

These are publication copies of six completed official Provenance Guard Unit 9
acceptance-trial archives. The originals remain locally under
`results/unit9_acceptance/` and were not modified to prepare these copies.
Creating this directory does not itself stage, commit, push, or publish evidence.

## Redactions

Only temporary audit filesystem-path metadata was redacted in the copied
`report.json` files:

- `audit_temporary_directory` is `[REDACTED_TEMP_AUDIT_DIRECTORY]`.
- Absolute temporary audit paths within `provenance.isolated_audit_paths` are
  `[REDACTED_TEMP_PATH]`; dictionary keys, structure, and non-path values remain
  unchanged.

All other report fields and their original JSON formatting are preserved.
Every copied `summary.txt` and `audit.jsonl` is byte-for-byte identical to its
original. Fixtures, case IDs, request IDs, HTTP responses/statuses, timestamps,
durations, scoring/audit counts, verdicts, Git revisions, specification
fingerprints, and trial-level outcomes were not changed.

## Trial context and outcomes

The before baseline was **instrumented**, not untouched Unit 8. All six trials
used mocked detector and stylometry scoring, not real GPT-2 inference. They do
not measure GPT-2 inference accuracy, latency, cost, or cold-start performance.

Each trial tested all 27 fixed requests and all five acceptance criteria.
All six trials passed, with all five criteria MET and zero trial-level failures.
These statements describe the existing reports; no trials were rerun to prepare
these publication copies.

## Contents

Each folder contains `report.json`, `summary.txt`, and `audit.jsonl`:

- `before-trial-1/`
- `before-trial-2/`
- `before-trial-3/`
- `after-trial-1/`
- `after-trial-2/`
- `after-trial-3/`

Keep the local originals and these publication copies distinct. Do not overwrite
or delete official evidence to repeat an occupied phase/trial combination.
