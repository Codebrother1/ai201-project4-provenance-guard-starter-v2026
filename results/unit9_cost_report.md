# Unit 9 — Provenance Guard local processing-time and cost report

## Scope and evidence source

This CodePath AI201 capstone extends Provenance Guard through **Shape B — Harden Against Failure** and **Path B — reproducible local execution with logs**. It is not a hosted deployment.

The measurements below are actual terminal measurements supplied by the project owner. They are informal local observations, not a controlled performance study or a public-hosting benchmark. No new experiments were run to prepare this report.

### Shared measurement methodology and environment

Both measurement series used `time.perf_counter()` for elapsed timing and the repository's `.venv/bin/python` interpreter, previously identified as Python **3.13.3**. Both used this exact English sample:

> I spent Saturday morning organizing my desk and sorting through old notebooks. Some pages reminded me of ideas I had forgotten, while others contained unfinished plans that I wanted to revisit.

Previously inspected environment versions were Flask **3.1.3**, Transformers **4.57.6**, PyTorch **2.14.1**, Flask-Limiter **3.12**, and Gunicorn **23.0.0**. These are previously inspected environment information, not package-version values newly measured during the timing runs.

## Measurement A — Real GPT-2 detector only

**Methodology:** The owner used locally cached GPT-2 with network downloads disabled. Initially, `detector._model` was `None`. Four real detector calls were measured; all four returned valid scores. These are detector-only timings, not full Flask application timings.

| Detector call | Elapsed time | Model state |
|---|---:|---|
| Run 1 | 4.365 seconds | Initially unloaded |
| Run 2 | 0.054 seconds | Warm |
| Run 3 | 0.049 seconds | Warm |
| Run 4 | 0.052 seconds | Warm |

**Warm median: 0.052 seconds**, using Runs 2–4.

The first call began with the model unloaded but its files already cached locally. This is not a first-download measurement or proof that operating-system disk caches were cold.

## Measurement B — Real GPT-2 full Flask `/submit` route

**Methodology:** The owner used Flask's in-process test client with real GPT-2, not mocked scoring. Network downloads were disabled. Rate limiting was temporarily disabled for controlled measurement, and audit output was redirected to an isolated temporary directory. The same legitimate sample text was submitted four times. The first request began with the model unloaded.

| Request | HTTP status | Elapsed time | Model state |
|---|---:|---:|---|
| Request 1 | 200 | 3.727 seconds | Initially unloaded |
| Request 2 | 200 | 0.051 seconds | Warm |
| Request 3 | 200 | 0.051 seconds | Warm |
| Request 4 | 200 | 0.048 seconds | Warm |

**Warm median: 0.051 seconds**, using Requests 2–4.

All four responses included `X-Request-ID`. The isolated audit output contained eight records: four decisions and four request-timing records. No historical logs or official acceptance-trial archives were changed by this measurement.

This measures the full route through an in-process test client, not detector inference alone. It is not end-to-end network HTTP latency or a measurement of a deployed web server. The supplied elapsed times are not asserted to be identical to the application's `duration_ms` audit values, whose timing-hook boundaries differ.

## Projection — 100 comparable submissions

Use Measurement B, not the detector-only timings, for this application-processing projection.

Assume one long-lived local process handles comparable submissions sequentially, with one cold request and 99 warm requests represented by the measured warm median:

- Estimated total application processing time: `3.727 + (99 * 0.051) = 8.776 seconds`.
- Estimated average: `8.776 / 100 = 0.08776 seconds per submission`.

**These are projections from four measured route requests, not 100 observed HTTP requests.** The calculation excludes initial model downloading and does not establish throughput, a latency guarantee, or a concurrent-service capacity.

Input lengths and content, system load, cache state, cold starts, process restarts, and concurrency can change the outcome. Multiple processes can incur separate model loads. Repeatedly submitting one sample does not represent a varied production workload.

## Monetary and resource costs

- Local GPT-2 uses no hosted inference API and requires no API key. There are no per-request hosted-model API fees in this configuration.
- Hardware, electricity, idle machine operation, and network costs were **not measured**. The absence of hosted API fees does not mean total monetary cost is exactly $0.
- The initial GPT-2 download is approximately **550 MB**. This is an approximate disk/cache transfer size, not measured RAM use. Downloads were disabled during these timing measurements, so their transfer cost is not included.
- No measured energy consumption, RAM usage, or dollar price is available. No wattage, electricity rate, or dollar-cost estimate is assumed here.
- Elapsed processing time alone is insufficient to calculate electricity consumption or total operating cost.

## Acceptance evidence is separate

The six official before/after acceptance trials are mocked-scoring regression tests. They exercise validation, scoring integration under mocks, audit correlation, and instrumentation requirements; they are **not real GPT-2 cost benchmarks**.

Neither Measurement A nor Measurement B replaces those trials or constitutes a new official acceptance run. Conversely, acceptance-trial timing records must not be presented as real GPT-2 inference cost, accuracy, or latency.

## Methodology limitations

- Each measurement series has only four observations, including three warm observations. A median of three warm calls does not characterize tail latency or long-run variability.
- Detector-only and route timings came from separate measurement series. Their differences do not establish an optimization, overhead estimate, or before/after speedup.
- The exact sample, elapsed timer, interpreter, and previously inspected package versions are documented above. Hardware specifications and measured electricity/RAM use are unknown. Raw profiler traces were not collected, and no tokenizer-specific token count is asserted.
- These observations do not measure authorship-detection accuracy, fairness, energy, RAM, monetary operating cost, or suitability for memory-constrained hosting.
- The 100-submission estimate applies only under its stated assumptions and must remain labeled as an estimate.
