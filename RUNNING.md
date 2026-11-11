# Running Provenance Guard

Local setup, everyday use, and evidence inspection for the completed Provenance
Guard capstone: **Shape B — Harden Against Failure**, **Path B — reproducible
local execution with logs**, not a hosted deployment.

This is a **web service**. It runs on your machine and you talk to it with
`curl` from another terminal. If you've not built a backend before, that's
assumed. The Unit 7/8 milestone explanations below are retained as historical
context; the submission, scoring, and appeal components are now implemented.

---

## Before your first class

### macOS/Linux setup

Use **Python 3.11, 3.12, or 3.13, not 3.14**. For a new checkout, the commands
below select an installed Python 3.13; substitute `python3.12` or `python3.11`
if that is your supported interpreter.

```bash
cd ~/ai201-project4-provenance-guard-starter-v2026
python3.13 --version
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python test.py
```

If `.venv` already exists, do not recreate it just to follow this guide. Check
its version with `.venv/bin/python --version`, then use its interpreter for
installation and checks. Activation with `source .venv/bin/activate` is optional
because these commands explicitly select `.venv/bin/python`. System `python3`
may lack the project's installed dependencies.

`requirements.txt` lists Flask, Flask-Limiter, requests, transformers, torch,
gunicorn, and certifi. The environment checker is `test.py`; it is not the
Unit 9 acceptance harness.

### First real-model use

If the checker warns that the detector model has not been downloaded, this
optional command downloads GPT-2 if needed, loads it, and scores a sample:

```bash
.venv/bin/python detector.py
```

The first download is approximately **550 MB** and requires network access.
Loading the model into memory adds startup work; actual time depends on your
machine and cache. Normal `/submit` requests use the real model. Within one
server process it remains loaded after first use; restarting or reloading the
process requires loading it again. Running `detector.py` prepares the disk
cache but does not warm the separate Flask process.

> **No API key for this pair.** Nothing here calls a hosted service. The model
> that reads your text runs on your own laptop.

---

## Your first five minutes

Two terminals, both in the repository directory. In the first, start the local
server with the debug reloader disabled:

```bash
AI201_DEBUG=0 .venv/bin/python app.py
```

In the second:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You should get JSON back. That's the whole idea of a web service — something
sent it data, it sent something back.

Check service health without requesting model scoring:

```bash
curl http://127.0.0.1:5000/health
```

`detector_loaded` can be `false` until this server process handles a valid real
submission. `/health` reports state; it does not download or load GPT-2.

**Stop the server with Ctrl+C in its terminal.** The default address is
`127.0.0.1:5000`, accessible from your own machine.

> **On Windows, use `curl.exe` and keep it on one line.**
>
> In PowerShell, `curl` is an alias for a different tool and the command above
> fails with `Cannot bind parameter 'Headers'` before it ever reaches your
> service. The `\` line breaks don't work there either. This does:
>
> ```powershell
> curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
> ```
>
> Every `curl` command in this file and in the brief works the same way: swap
> `curl` for `curl.exe` and put it on one line. Git Bash needs no change.

**Leave `/ping` alone.** It's your control. When something breaks later, check
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself, and that's a help-channel question.

Then try a real submission. `-i` shows the HTTP status and `X-Request-ID` header:

```bash
curl -i -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"creator_id":"local-demo","text":"I spent the morning organizing my desk and reading old notes. The quiet room helped me plan the rest of my day."}'
```

On success, `/submit` returns HTTP 200 with `content_id`, `guess`, `confidence`,
`label`, `model_score`, and `style_score`. The label is a heuristic assessment,
not proof of authorship. A first real submission may wait for model download
or loading. This manual request appends normal audit records; it is not a
mocked acceptance trial and does not change the archived trial directories.

`creator_id` must be a nonempty string. `text` must be a nonempty string with
**3–300 whitespace-separated tokens**, at least one Unicode letter, and no
disallowed Unicode category `Cc` controls. Ordinary tab, newline, and carriage
return are allowed in otherwise valid writing. Punctuation-only and
numbers-only text, including Arabic-Indic digits, are rejected with HTTP 400
before model scoring. Length checks precede the control check, which precedes
the Unicode-letter check. Accented-letter acceptance does not establish
multilingual authorship accuracy.

---

## The routes

| Route | State | What it does |
|---|---|---|
| `POST /ping` | **works** | The example. Don't edit it |
| `GET /health` | **works** | Is the service up, is the model loaded |
| `GET /log` | **works** | The audit log, as JSON |
| `POST /submit` | **works** | Validates writing, runs real GPT-2 and stylometry, combines signals, returns a label, and writes audit records |
| `POST /appeal` | **works** | Accepts `content_id` and nonempty `reasoning`; appends an appeal-intake event with status `under_review` |

An appeal records a request for review, not completed human adjudication. It
preserves the original decision and scores. An unknown content ID returns
HTTP 404; a repeated appeal returns HTTP 409.

---

## Every command

| Command | What it does |
|---|---|
| `.venv/bin/python test.py` | Checks your environment, not the Unit 9 acceptance criteria |
| `AI201_DEBUG=0 .venv/bin/python app.py` | Runs the local service without the debug reloader |
| `.venv/bin/python detector.py` | Optional real-model download/loading and sample scoring |
| `.venv/bin/python detector.py "some text"` | Scores text with the real detector from the terminal |
| `.venv/bin/python stylometry.py "some text"` | Displays the implemented style measures |
| `.venv/bin/python run_attacks.py --set <folder>` | Historical Unit 8 attack workflow; sends requests and writes results |
| `.venv/bin/python run_attacks.py --flood 15` | Historical Unit 8 flood workflow; sends requests and writes results |
| `.venv/bin/python run_eval.py --label before` | Historical Unit 8 evaluation workflow, not the Unit 9 harness |
| `.venv/bin/python unit9_acceptance.py --help` | Shows harness usage without running a trial |

Historical evaluation commands are reference material, not instructions to
regenerate completed evidence. Inspect saved results first.

---

## Which piece goes with which milestone

### Unit 7 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Trace a submission on paper | Nothing to run |
| 2 | Write your criteria | `criteria.md` — all five are yours |
| 3 | The route, one signal, the log | `app.py::submit`, `detector.py`, `audit.py` |
| 4 | Second signal, combine, score | `stylometry.py`, `scoring.py::combine_signals` |
| 5 | Labels and the appeal path | `scoring.py::score_to_label`, `app.py::appeal` |
| 6 | Write it up | `README.md` |

### Unit 8 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Rate limiting and the full log | `config.py`, the decorator in `app.py` |
| 2 | Run the attack set | `run_attacks.py` |
| 3 | Run your own criteria | `scenarios.py`, `run_eval.py` |
| 4 | Verdicts and diagnoses | `README.md` |
| 5 | Fix one thing, re-run | `run_attacks.py --label after` |
| 6 | What's still broken | `README.md` |

---

## Building `/submit` in three passes

**Historical Unit 7 workflow:** these passes have been completed. This section
explains how the service was built, not missing work in the current checkout.

The ordering is deliberate. It's how you tell a broken route from a broken
signal.

**Milestone 3.** Return a hardcoded response. Confirm `curl` gets it back
**before** you add any logic. Then pull `text` and `creator_id` out. Then call
one signal. Then log it.

**Milestone 4.** Add the second signal. Combine them. Log both scores.

**Milestone 5.** Turn the score into a label.

> Test each signal from a terminal on its own before wiring it in. If you skip
> that you'll spend an hour not knowing whether the route or the signal is
> lying to you.

---

## Turning on rate limiting (unit 8)

**Historical Unit 8 setup:** rate limiting is already enabled by default, the
decorator is active, and limits are **10/minute and 200/day**. Counts use
`memory://` storage and reset when the server process restarts. A nonempty
creator ID is the caller key; otherwise the limiter falls back to the IP
address. Creator IDs are not authenticated.

The original setup steps were:

1. In `config.py`, set `RATE_LIMITING_ENABLED = True` — or run with
   `AI201_RATE_LIMITS=1`.
2. Choose your numbers there.
3. The `@limiter.limit(...)` decorator above `submit` in `app.py` is already
   enabled in the source. `AI201_RATE_LIMITS` controls whether rate limiting
   is active: `1` enables it (the default), and `0` disables it at startup.

The historical flood command, which sends requests and writes new results, was:

```bash
.venv/bin/python run_attacks.py --flood 15
```

That sends 15 submissions from one `creator_id` and prints the run of status
codes — `200 200 200 ... 429 429` — which is exactly what your README's **Rate
Limiting** section asks you to paste. It also writes `results/flood_<date>.md`.

Most attack cases use distinct creator IDs, so they do not collectively test
one caller's quota. Flood-family cases deliberately reuse a creator ID; inspect
the saved Unit 8 report for the actual requests and outcomes.

No `429` at all? Either your limit is above 15 a minute, or rate limiting is
still off. `GET /health` reports which.

Rejections are logged for you. **An attack that shows up only as an absence is
one you'll never find** — a thousand requests that got a `429` and left no
trace look exactly like a quiet afternoon.

---

## Running it somewhere else (unit 9)

This capstone uses **Path B: reproducible local execution with logs and
evidence**. It is not a hosted deployment. The walkthrough above is the
supported local demonstration.

Flask's built-in server says "development server" on startup because that's
what it is. A real one comes from `gunicorn`, which is in
`requirements.txt`. If a separate local WSGI demonstration is needed, stop the
Flask server first and use the same virtual environment and loopback address:

```bash
.venv/bin/python -m gunicorn app:app --bind 127.0.0.1:5000 --workers 1
```

For `app.py`, these settings read the environment. The Gunicorn command above
uses its explicit `--bind` address instead:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback — your machine only. A host needs `0.0.0.0`, or nothing outside the box can reach the service and it looks like the app is down |
| `PORT` | `5000` | Most hosts hand you a port in `PORT` and expect you to bind exactly that one |
| `AI201_DEBUG` | `1` | Debug mode. Off automatically whenever `HOST` isn't loopback — an interactive debugger on a public address is a stranger's Python prompt inside your process |

Nothing about your local workflow changes. With no variables set you get
`http://127.0.0.1:5000` and every `curl` above still works.

### Why Path B instead of memory-constrained free hosting?

Real submissions require the PyTorch runtime, GPT-2 weights, inference working
memory, and the web application together. The approximately 550 MB model
download is a disk/cache size, not a measurement of total RAM. A small free-tier
memory allowance may be insufficient; multiple worker processes can also
multiply model memory. Ephemeral caches can require another download after a
restart. Actual limits and persistence policies depend on the hosting provider.

Local execution avoids claiming that a memory-constrained host can support
this model. No measured RAM, power consumption, dollar cost, or universal
free-host capacity is asserted here. Gunicorn does not reduce model size, and
the mocked acceptance suite does not demonstrate real-model hosting capacity.

---

## Unit 9 audit records

Normal application records append to `logs/audit.jsonl`: one JSON object per
line (JSONL). Existing historical entries retain their older shapes.

- **Decision:** UTC `timestamp`, creator/content IDs, scores, label, status
  `decided`, and the Unit 9 `request_id`. The existing decision format has no
  `event` or `http_status` field; use its matching timing record for HTTP status.
- **Rejection:** UTC `timestamp`, `event="rejected"`, `status="rejected"`,
  `reason`, creator ID or `"unknown"`, `request_id`, and `http_status`.
  Validation failures use HTTP 400; rate limiting uses 429. Detector
  unavailability is recorded with reason `detector_unavailable` and status 503.
- **Timing:** UTC `timestamp`, `event="request_timing"`, `request_id`,
  `http_status`, numeric `duration_ms`, and `outcome`: `success` for 2xx,
  `rejected` for 4xx, `error` for 5xx, or `other` for other status classes.

Correlate Unit 9 `/submit` records using the response's `X-Request-ID`.
Business records and timing records are separate, not duplicate decisions.
Neither these rejection nor timing records intentionally store raw submitted
text or complete request bodies. Appeal events record the supplied reasoning,
so audit files can still contain private information.

Timing starts near the beginning of the `/submit` `before_request` hook and
ends during `after_request` response preparation. It includes validation,
scoring when reached, and business audit writes, but excludes earlier Flask
setup, timing-record persistence, subsequent finalization, transmission, and
teardown. It is not WSGI-entry-to-client timing.

If a `/submit` decision, validation-rejection, or detector-failure rejection
write raises `OSError`, the route returns a generic HTTP 500
`audit_write_failed` response. This does not describe the separate rate-limit
handler's write-failure behavior. A timing-write failure is reported to the
application error logger without replacing the original response or claiming
that timing evidence was saved.

To inspect recent application records while the server is running:

```bash
curl "http://127.0.0.1:5000/log?limit=10"
```

## Inspecting completed Unit 9 acceptance evidence

The frozen five criteria are in `criteria.md`, approved at commit `eb0d981`.
The reproducible harness is `unit9_acceptance.py`. It uses Flask's in-process
test client, mocked detector and stylometry signals, and real validation,
signal combination, and labeling. It temporarily disables rate limiting and
redirects audit writes away from historical logs, then archives trial evidence.

**These acceptance checks do not load GPT-2 and do not measure GPT-2 inference
cost, accuracy, or latency.** Their application timing records describe mocked
request handling. Normal manual `/submit` requests are real-model runs instead.

Three official before-improvement trials and three official after-improvement
trials have already been executed and verified. Each attempted 27 requests;
all five criteria were MET in every trial, with zero trial-level failures.
The before trials were an **instrumented baseline**, not untouched Unit 8.

The six official archives currently exist only in this local working directory
under `results/unit9_acceptance/`. They have not been committed or pushed to
GitHub, so a fresh GitHub checkout does not contain them. The local archives are:

- `results/unit9_acceptance/before-trial-1/`
- `results/unit9_acceptance/before-trial-2/`
- `results/unit9_acceptance/before-trial-3/`
- `results/unit9_acceptance/after-trial-1/`
- `results/unit9_acceptance/after-trial-2/`
- `results/unit9_acceptance/after-trial-3/`

Each contains `report.json`, `summary.txt`, and `audit.jsonl`. Inspect the
existing evidence without executing a new trial:

```bash
cat results/unit9_acceptance/after-trial-1/summary.txt
.venv/bin/python -m json.tool results/unit9_acceptance/after-trial-1/report.json
cat results/unit9_acceptance/after-trial-1/audit.jsonl
.venv/bin/python unit9_acceptance.py --help
```

The JSON report contains per-fixture observations, assertions, request IDs,
configuration, provenance, and criterion results; the JSONL archive contains
the actual application audit records. Use the other listed directory names to
inspect their existing files. `--help` shows CLI options without importing the
application, sending requests, or creating a trial archive.

**Never overwrite, delete, or casually rerun an official trial archive.**
All six phase/trial combinations are occupied, and the harness refuses existing
directories. Do not remove or rename archives to bypass that protection.
Any new reproduction run requires an explicitly reviewed evidence-isolation
plan; this guide deliberately supplies no command that reuses an occupied slot.

The evidence-based additional improvement was detector-unavailability audit
logging, commit `862897a`. Separate mocked `DetectorUnavailable` checks found
zero structured detector-failure records before and one afterward, preserving
HTTP 503 and request correlation. A separate audit-write `OSError` check
returned HTTP 500 `audit_write_failed`. Those fault-injection checks are distinct
from the frozen 27-request trials; do not attribute their coverage to the five
criteria. Unit 9 history comprises eight pushed commits. No new tests or
measurements are implied by these documentation instructions.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting: thresholds, weights, rate limits, the model |
| `app.py` | Working routes, Unicode validation, request IDs, structured rejections, and request timing |
| `detector.py` | Signal one — the local model. Given to you |
| `stylometry.py` | Implemented style signal and text-shape measures |
| `scoring.py` | Implemented signal combination and uncertainty-aware labels |
| `audit.py` | The audit log writer. Given to you |
| `run_attacks.py` | Runs the attack set — **unit 8** |
| `run_eval.py` | Runs your criteria three times — **unit 8** |
| `scenarios.py` | Unit 7/8 evaluation scenarios |
| `criteria.md` | Preserved Unit 7/8 criteria and frozen Unit 9 criteria/fixtures |
| `unit9_acceptance.py` | Mocked, isolated Unit 9 acceptance harness with provenance checks |
| `logs/audit.jsonl` | Normal append-only audit history; review privacy before sharing |
| `results/` | Historical evidence and preserved Unit 9 trial archives; selectively review before staging |

---

## The two blind spots, up front

Both signals have one, and unit 8's attack set is built out of them. You have
to name them yourself in Milestone 1 — but knowing they exist now saves you
from being surprised.

**Signal one** measures how *predictable* your text is. Predictability isn't
authorship. What it really rewards is common words in short, ordinary
sentences — someone writing in a second language and staying with vocabulary
they're sure of, a younger writer, anyone writing plainly on purpose. Writing
like that scores about as machine-like as machine writing does. (Dense, ornate
prose often goes the other way and reads as human, because rare words are what
a language model fails to predict.) So the writers this signal is most likely
to accuse are the ones with the least room to argue back. That is the false
positive the whole project is about, and it's structural rather than a bug.

**Signal two** cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — typos, broken-up
sentences, a pasted quotation. That is very cheap to do on purpose.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `501 not_implemented` | Historical starter behavior, not expected from the completed `/submit` or `/appeal`; check that you are using the intended checkout/process |
| `404` from curl | The server answered but the resource was not found; check the exact path or, for appeals, the content ID |
| `Cannot bind parameter 'Headers'` | You're in PowerShell, where `curl` is a different tool. Use `curl.exe`, on one line |
| Request body arrives empty | curl needs `-H "Content-Type: application/json"` |
| `Address already in use` | Check the terminal running your earlier server and stop it with Ctrl+C before starting another |
| The first submission is slow | GPT-2 may be downloading or loading. Duration is machine-dependent; no latency guarantee is made |
| Repeated model loading | Check for server restarts or the debug reloader; `/health` reports whether the current process has loaded the model |
| HTTP 503 `detector_unavailable` | Check dependencies, network/cache access, and local resources. Optional diagnosis: `.venv/bin/python detector.py` runs the real model |
| HTTP 500 `audit_write_failed` | A business audit record could not be written; check local log-directory permissions and storage |
| `/appeal` returns 404 or 409 | 404 means no matching content ID; 409 means an appeal already exists. HTTP 200 records intake, not adjudication |
| No `429` | Check `/health`, the caller key, request count, and whether AI201_RATE_LIMITS was explicitly disabled; defaults are enabled |
| Flask-Limiter warns about storage | Shouldn't happen — `storage_uri` is preconfigured. If you changed it, put it back |
| Not all three labels appear in a sample set | Scores may all fall in only some bands; this alone does not prove a threshold gap. Preserve frozen thresholds and inspect the historical diagnoses |

If the route won't respond, go back to `/ping`. If that answers, the problem is
in your handler.

---

## A note on committing

At least four new commits in unit 7, four more in unit 8.

`logs/` and `results/` are deliberately **not** in `.gitignore`. They can contain
useful evidence, but that does not make every file appropriate to publish.
Review privacy, provenance, and relevance before selectively staging explicit
evidence paths. Do not use blanket `git add .`, `git add logs/`, or
`git add results/` to collect unrelated or private records.

Preserve official archives and historical evidence. Protect untracked
`attack_set/` and `legal-agent-workshop/`; do not stage them merely because
they appear in Git status. Inspect changes before any separately authorized
commit or push.

**Do not delete and recreate this repository.** You submit the same URL both
units.
