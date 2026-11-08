# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer submits their text and creator ID to the Provenance Guard service through POST /submit.
2. The GPT-2 model signal analyzes how predictable the writing is. This produces a model_score, but predictable writing does not prove that AI created it.
3. The stylometry signal examines sentence-length variation and word variety. punctuation_density() is measured, but style_signal() does not let that measurement change the score. The style score is 40% sentence consistency, 40% vocabulary repetition, and 20% a fixed neutral punctuation component of 0.5. This produces a style_score, but human writing can also have consistent patterns.
4. The service combines the model_score and style_score using a defined scoring rule to produce an overall result. If the signals disagree, the system should handle that uncertainty carefully rather than automatically making a strong accusation.
5. The service selects an internal guess of "human", "unsure", or "ai", and a complete message for the reader. That message explains the result. It does not prove who wrote the text.
6. After validation, model scoring, stylometry, combining, and labeling have succeeded, the service assigns a unique content_id, records the decision in the audit log, and keeps the information necessary to explain what happened.
7. The service returns the result to the website. If the writer disagrees, they can request a review through POST /appeal without having to rewrite their original work.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

My model signal runs a local GPT-2 model on the submission and estimates how predictable the text is. `detector.model_signal()` turns the model's perplexity into a `model_score` from 0 to 1. A higher score means the writing looked more predictable, so this heuristic treats it as more AI-like. That number is not a verified probability that AI wrote the passage.

**Why that might differ between human and AI writing:**

Some AI-generated writing follows predictable language patterns, because a model keeps choosing likely next words. That can give me one clue when I look at it alongside my style signal.

**What it can't see:**

Predictability does not establish authorship. Straightforward, formulaic, or carefully edited human writing can look predictable too, so a high score can be a false positive. AI writing can be less predictable, so a low score can be a false negative. I have not measured how often either mistake happens. The scorer also stops at 400 tokens, so it may not read an entire submission.

### Signal two — the style signal

**What it measures:**

I measure the shape of the writing. `sentence_length_spread()` measures variation in sentence lengths. `type_token_ratio()` measures unique words relative to all words. `punctuation_density()` measures selected punctuation marks per word: commas, semicolons, colons, exclamation points, question marks, hyphens, and en or em dashes. It does not count periods. `style_signal()` turns this into a `style_score` from 0 to 1 using 40% sentence consistency, 40% vocabulary repetition, and 20% a fixed neutral punctuation contribution of 0.5. Vocabulary repetition is one minus the type-token ratio. With at least two usable sentences, sentence consistency is `1 / (1 + spread)`, so similar lengths raise the score. Measured punctuation density does not currently change the score. A higher score means this heuristic reads the writing as more regular. It does not prove that AI wrote it.

**Why that might differ between human and AI writing:**

Repeated word choices and sentences of similar length can sometimes show more regular writing patterns. I use the style score as a second perspective alongside GPT-2. This is a heuristic, not a reliable rule for identifying AI authorship.

**What it can't see:**

Human writers can be consistent or repetitive, and AI-generated writing can vary, so this signal can produce false positives and false negatives. I have not measured how often. Short passages provide little evidence. With no usable words, `style_signal()` returns 0.5. With fewer than two sentences that contain words, sentence consistency stays at a neutral 0.5, because there is not enough variation to judge. Punctuation choices are not treated as a sign of AI use. Stylometry cannot prove authorship.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Both GPT-2 and stylometry produce a score from 0 to 1. Normally the combined score is their weighted average. If the absolute difference between the two scores is 0.40 or greater, `combine_signals()` returns 0.5000 instead of that average. I chose the disagreement rule to avoid making a strong accusation when the two signals point in different directions. Returning 0.5000 puts the result in the unsure band, above 0.35 and below 0.65. This is a design safeguard. It is not proof that the detection system has been validated, and it is not proof that the rule improves measured accuracy.

**The numbers:**

The current weights are 0.50 for the model signal and 0.50 for the style signal. The disagreement gap is 0.40. The weighted average is clamped to 0–1 and rounded to four decimal places. The disagreement result is returned as 0.5000.

On a live `POST /submit` test, the model score was 0.6764 and the style score was 0.4681. The difference was 0.2083, below 0.40, so the function used the weighted average. The combined score was 0.5723, and the guess was "unsure".

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

This case is illustrative. It is not a live submission. If the model score were 0.90 and the style score were 0.10, the difference would be 0.80. That gap is at least 0.40, so the function would return 0.5000 and the guess would be "unsure".



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35, including 0.00 and 0.35 | Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship. |
| unsure | above 0.35 and below 0.65 | Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review. |
| high-confidence AI | 0.65–1.00, including 0.65 and 1.00 | Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review. |

These ranges describe the original Unit 7 configuration. After the Unit 8 fairness improvement, the current AI cutoff is 0.72, so scores above 0.35 and below 0.72 are classified as `unsure`, while scores at or above 0.72 are classified as `ai`.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The detector cannot prove who wrote a passage. An unsure result means the analysis was inconclusive, not that the writer is being accused. A wrong accusation could unfairly affect a genuine writer, so the message says the tools can be mistaken and offers a way to request a review. If the writer does, the service records the appeal with status `under_review`. That status means the request was saved. It does not mean a person has finished reviewing the writing. The service also has no account login, so recording an appeal does not confirm the requester's identity.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"creator_id":"test-writer-002","text":"I spent Saturday morning organizing my desk and sorting through old notebooks. Some pages reminded me of ideas I had forgotten about, while others were filled with unfinished plans. By lunchtime, the room felt much more comfortable, and I was glad I had finally made time for it."}'
```

```json
{
  "content_id": "b76f60b0-5bd8-40ff-a1a3-5fe97d10c35a",
  "guess": "unsure",
  "confidence": 0.5723,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "model_score": 0.6764,
  "style_score": 0.4681
}
```

**An appeal**

```bash
curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"b76f60b0-5bd8-40ff-a1a3-5fe97d10c35a","reasoning":"I wrote this passage myself without AI assistance. I would like the result reviewed."}'
```

```json
{
  "content_id": "b76f60b0-5bd8-40ff-a1a3-5fe97d10c35a",
  "message": "Your appeal request was recorded. It has not yet been reviewed.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "timestamp": "2026-10-31T10:17:42+00:00",
      "content_id": "b76f60b0-5bd8-40ff-a1a3-5fe97d10c35a",
      "creator_id": "test-writer-002",
      "guess": "unsure",
      "model_score": 0.6764,
      "style_score": 0.4681,
      "combined_score": 0.5723,
      "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
      "status": "decided"
    },
    {
      "timestamp": "2026-10-31T10:21:43+00:00",
      "content_id": "b76f60b0-5bd8-40ff-a1a3-5fe97d10c35a",
      "creator_id": "test-writer-002",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this passage myself without AI assistance. I would like the result reviewed."
    }
  ]
}
```

These blocks are historical test outputs from an earlier run: rerunning `/submit` creates a new content_id, and replaying this appeal for the existing content_id would now return HTTP 409 because it is already recorded.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked ChatGPT and Cursor to help me build a combining rule for the GPT-2 and stylometry signals, especially when the two measurements disagreed. I wanted to avoid a strong accusation based on conflicting evidence.
- *What came back:* AI helped implement and explain a 50/50 weighted average with a disagreement safeguard. If the scores differ by 0.40 or more, the function returns 0.5000, which maps to "unsure". We checked that rule with several numerical examples.
- *What I changed:* I kept the disagreement safeguard because communicating uncertainty mattered to me. I also made sure the README describes it as a cautious design decision, not a validated improvement in detection accuracy. I verified the behavior through tests rather than assuming the AI-generated code was correct.

**Moment 2**

- *What I asked for:* I asked AI to inspect the Sample Run requirements and help document a real submission, its appeal, and the corresponding audit records.
- *What came back:* Cursor identified the stored scores and the appeal status, and reported that the original submitted passage could not be recovered from the repository's audit log.
- *What I changed:* I used the exact passage from my earlier Warp test command instead of inventing a replacement. I kept the real scores, content ID, and audit records together, and I added a note that these are historical outputs. I also documented that repeating the existing appeal would return HTTP 409, not another successful appeal.

**Moment 3 — Unit 8: Attack testing and fairness trade-offs**

- *What I asked for:* I asked AI to organize the rate-limiting test, the attack-family analysis, the three-trial evaluation, and the appeal audit check into a repeatable workflow.
- *What came back:* AI helped diagnose the failures by comparing model scores, style scores, the combining rule, and the label thresholds. It also compared possible improvements and pointed out that lowering the AI cutoff could create another false accusation.
- *What I changed:* AI helped draft and review the README and find rubric gaps. I checked the HTTP responses, scores, audit records, Git commits, and before/after reports myself. Those measured results came from the running service and the saved reports. I decided to raise `AI_THRESHOLD` from 0.65 to 0.72, accepting more `unsure` labels rather than making more unsupported AI accusations. No person adjudicated an appeal. I documented the remaining failures instead of hiding them.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A writer can submit several drafts or revisions without being blocked right away. A script that keeps sending variations as the same caller is slowed after 10 submissions in a minute. The 200-per-day limit leaves room for ongoing revisions and limits sustained automated probing. These are my initial design choices, not proven optimal limits.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

The limiter uses a non-empty `creator_id` string when the request supplies one. Otherwise it uses the requester's IP address. The flood test counted as `flood_tester`. That ID is not authenticated, so changing IDs can avoid the per-caller limit. Counts are stored with `memory://`, so they reset when the server restarts.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

I ran `python run_attacks.py --flood 15`. The saved result is `results/flood_2026-11-08_0357.md`. It sent 15 submissions as `flood_tester`. The first 10 returned HTTP 200, and the last 5 returned HTTP 429. Those five 429 responses show that the 10-per-minute limit was reached. This run did not test the 200-per-day limit. The audit log kept its earlier records, added 10 `decided` submissions, and added 5 rejections with `event` `"rejected"`, `status` `"rejected"`, `reason` `"rate_limited"`, and `limit` `"10 per 1 minute"`.

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

The saved baseline report is `results/attack_run_2026-11-08_0414_before.md`. It records 56 attacks from 2026-11-08 04:14. The runner automatically marked 0 BROKE. That automatic mark only covers a server error, a crash, or no response. I then marked each row by hand: 41 HELD and 15 BROKE. The 15 BROKE marks are my judgment that the attack got the outcome it was aiming for. HTTP status and guess below are copied from that report. A dash means the report had no guess.

| ID | Family | HTTP status | Guess | Verdict |
|---|---|---|---|---|
| EV01 | evasion | 200 | human | BROKE |
| EV02 | evasion | 200 | unsure | BROKE |
| EV03 | evasion | 200 | unsure | BROKE |
| EV04 | evasion | 200 | unsure | BROKE |
| EV05 | evasion | 200 | unsure | BROKE |
| EV06 | evasion | 200 | unsure | BROKE |
| EV07 | evasion | 200 | unsure | BROKE |
| EV08 | evasion | 200 | human | BROKE |
| EV09 | evasion | 200 | unsure | BROKE |
| EV10 | evasion | 200 | ai | HELD |
| FP01 | false_positive | 200 | unsure | HELD |
| FP02 | false_positive | 200 | unsure | HELD |
| FP03 | false_positive | 200 | ai | BROKE |
| FP04 | false_positive | 200 | ai | BROKE |
| FP05 | false_positive | 200 | ai | BROKE |
| FP06 | false_positive | 200 | unsure | HELD |
| FP07 | false_positive | 200 | ai | BROKE |
| FP08 | false_positive | 200 | unsure | HELD |
| PI01 | prompt_injection | 200 | unsure | HELD |
| PI02 | prompt_injection | 200 | human | HELD |
| PI03 | prompt_injection | 200 | unsure | HELD |
| PI04 | prompt_injection | 200 | unsure | HELD |
| PI05 | prompt_injection | 200 | unsure | HELD |
| PI06 | prompt_injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 400 | — | HELD |
| MF03 | malformed | 200 | human | BROKE |
| MF04 | malformed | 200 | unsure | BROKE |
| MF05 | malformed | 400 | — | HELD |
| MF06 | malformed | 400 | — | HELD |
| MF07 | malformed | 200 | unsure | HELD |
| MF08 | malformed | 400 | — | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 400 | — | HELD |
| RQ11 | malformed | 400 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | HELD |
| FL01_02 | flood_same_creator | 200 | human | HELD |
| FL01_03 | flood_same_creator | 200 | human | HELD |
| FL01_04 | flood_same_creator | 200 | human | HELD |
| FL01_05 | flood_same_creator | 200 | human | HELD |
| FL01_06 | flood_same_creator | 200 | human | HELD |
| FL01_07 | flood_same_creator | 200 | human | HELD |
| FL01_08 | flood_same_creator | 200 | human | HELD |
| FL01_09 | flood_same_creator | 200 | human | HELD |
| FL01_10 | flood_same_creator | 200 | human | HELD |
| FL01_11 | flood_same_creator | 429 | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | HELD |

**Family results**

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 4 | 4 |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 18 | 2 |
| flood_same_creator | 12 | 12 | 0 |

Evasion was BROKE when the guess was human or unsure, because the attack avoided an AI label. EV10 stayed `ai`, so it is HELD. False positives were BROKE only when the guess was `ai`. A human or unsure guess is HELD, because the service did not accuse that writer. Prompt injection was HELD when the response stayed on the normal scoring path and used one of the approved labels. All six did. Malformed requests were HELD when validation returned HTTP 400 and no score. MF07 was also HELD: right-to-left writing is valid text, and the service scored it instead of rejecting it for its script. MF03 and MF04 are BROKE because each still received HTTP 200 and a reader label. Flood rows were HELD because the first 10 submissions for `attacker_flood` were inside the 10-per-minute allowance, and the next 2 returned HTTP 429.

**Ten audit log entries from the run**

These ten lines are copied from `results/audit_extract.json`. The order is FP03, FP04, FP05, FP07, EV09, EV10, MF03, MF04, PI05, and one `attacker_flood` rate-limit rejection. Seventeen malformed requests returned HTTP 400: MF01, MF02, MF05, MF06, MF08, and RQ01 through RQ12. They do not appear in the decision audit because validation returned an error before a decision was logged.

```jsonl
{"combined_score": 0.6585, "content_id": "745855e3-52ee-4372-be13-c7d7b77658a7", "creator_id": "attacker_FP03", "guess": "ai", "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.", "model_score": 0.8051, "status": "decided", "style_score": 0.512, "timestamp": "2026-11-08T10:14:35+00:00"}
{"combined_score": 0.6511, "content_id": "b6491ac3-4c6e-43f1-b243-30a408bf6aab", "creator_id": "attacker_FP04", "guess": "ai", "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.", "model_score": 0.8329, "status": "decided", "style_score": 0.4692, "timestamp": "2026-11-08T10:14:36+00:00"}
{"combined_score": 0.6897, "content_id": "a8b29ed7-9685-44e4-a116-5f448a975358", "creator_id": "attacker_FP05", "guess": "ai", "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.", "model_score": 0.8005, "status": "decided", "style_score": 0.579, "timestamp": "2026-11-08T10:14:36+00:00"}
{"combined_score": 0.7148, "content_id": "172711d3-1975-4e3c-952e-a65705fe1b71", "creator_id": "attacker_FP07", "guess": "ai", "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.", "model_score": 0.8816, "status": "decided", "style_score": 0.548, "timestamp": "2026-11-08T10:14:36+00:00"}
{"combined_score": 0.569, "content_id": "a3c1a88c-a76c-4a5d-8c97-8f07dc3d41b7", "creator_id": "attacker_EV09", "guess": "unsure", "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.", "model_score": 0.7042, "status": "decided", "style_score": 0.4338, "timestamp": "2026-11-08T10:14:35+00:00"}
{"combined_score": 0.819, "content_id": "f7f7fd75-1958-49d2-a14c-00e27cd879d9", "creator_id": "attacker_EV10", "guess": "ai", "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.", "model_score": 0.9792, "status": "decided", "style_score": 0.6588, "timestamp": "2026-11-08T10:14:35+00:00"}
{"combined_score": 0.15, "content_id": "a1a9c668-ecba-4b9c-8c2b-f2c219022da5", "creator_id": "attacker_MF03", "guess": "human", "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.", "model_score": 0.0, "status": "decided", "style_score": 0.3, "timestamp": "2026-11-08T10:14:36+00:00"}
{"combined_score": 0.5, "content_id": "d81ed079-a4f2-4af3-bf60-600fb9b3de3a", "creator_id": "attacker_MF04", "guess": "unsure", "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.", "model_score": 0.0112, "status": "decided", "style_score": 0.5, "timestamp": "2026-11-08T10:14:36+00:00"}
{"combined_score": 0.5127, "content_id": "77bbc24b-e0d1-4db7-9bdc-f3efd5403d04", "creator_id": "attacker_PI05", "guess": "unsure", "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.", "model_score": 0.6401, "status": "decided", "style_score": 0.3852, "timestamp": "2026-11-08T10:14:36+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-08T10:14:37+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03. The staff target describes it as careful writing by a non-native English speaker. The service returned guess `ai` at combined score 0.6585, with model score 0.8051 and style score 0.5120. That is an AI label on writing the target presents as human. The stored label says the result does not prove AI was used, and it tells the writer they may request a review. The unsure result exists so the service can admit uncertainty instead of making that accusation. I have not independently verified who wrote the passage. The original text is not stored in the report.

The runner's automatic verdicts do not judge whether an attack succeeded. They only record crashes and server failures, and this run had none. The generated report does not include the original submitted passages. The flood rows tested the 10-per-minute limit. They did not independently test the 200-per-day limit.

---

## Run Log and Verdicts

The three trials are in `results/run_2026-11-08_0515_before.md`, produced by `run_eval.py::main`. The appeal check is in `results/appeals_before.md`. H01–H10 are self-reported human writing, not independently verified authorship. A01–A05 were generated by GPT-6 on November 8, 2026. The same scores came back in every trial.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False-positive protection | At most 1 of 10 human samples labeled `ai` | 0 of 10 | 0 of 10 | 0 of 10 | MET |
| 2. Fair appeal process | 5 of 5 appeals recorded, submission status `under_review` | 5 of 5 recorded | 5 of 5 recorded | 5 of 5 recorded | MISSED |
| 3. Label coverage | `human`, `unsure`, and `ai` each appear at least once | no `ai` | no `ai` | no `ai` | MISSED |
| 4. Invalid input | 5 of 5 return HTTP 400, with no detection result | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Score separation | AI mean at least 0.20 above the human mean | gap 0.2254 | gap 0.2254 | gap 0.2254 | MET |

Criterion 1 is MET because none of the ten self-reported human samples received guess `ai`. Five were `human` and five were `unsure`. That result is about these self-reported samples. It does not prove who wrote them.

Criterion 2, as written in `criteria.md`, requires that all 5 of 5 valid appeals be recorded in the audit log and that their submission status be marked `under_review`. Each trial sent five appeals. All 15 returned HTTP 200 and created a separate append-only appeal event with status `under_review`. Every original submission decision remained `decided`, with the same scores. The failure stage is appeal handling and audit-state representation in `app.py::appeal`. The endpoint appends an appeal event rather than updating the submission's status. That original requirement was measurable, and it was not met, so the later append-only revision cannot retroactively count as a passing verdict on the original wording. The revision remains in `criteria.md` as a record of the appeal-intake behavior that was tested. No person adjudicated these appeals. A future remedy would add an explicit current submission and appeal status representation, while preserving the immutable original audit records, and would verify that behavior with tests. I have not implemented that change.

Criterion 5 is MET. The human mean for H01–H05 is 0.3634. The AI mean for A01–A05 is 0.5888. The gap is 0.2254, which is above 0.20.

Criterion 4 is MET. In every trial, the five invalid bodies returned HTTP 400 with a specific `bad_request` message and null guess, confidence, and signal scores.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

This excerpt is Trial 1 of the `ai scores` group from `results/run_2026-11-08_0515_before.md`, produced by `run_eval.py::main`. The same five combined scores appear in Trials 2 and 3. The full 35-result trials are in that file.

```json
[
  {
    "content_id": "2938767c-41c6-41d9-be85-827303e0f489",
    "guess": "unsure",
    "confidence": 0.5841,
    "model_score": 0.6928,
    "style_score": 0.4755
  },
  {
    "content_id": "35bfd4bd-fb19-48d6-af1e-2f2fcbc5af74",
    "guess": "unsure",
    "confidence": 0.6179,
    "model_score": 0.7715,
    "style_score": 0.4643
  },
  {
    "content_id": "41df42ad-ace8-4a12-a7c6-e8060fd09db2",
    "guess": "unsure",
    "confidence": 0.6347,
    "model_score": 0.7836,
    "style_score": 0.4859
  },
  {
    "content_id": "48ec5bcb-92e5-47b9-a304-aa275dc825a8",
    "guess": "unsure",
    "confidence": 0.4798,
    "model_score": 0.5177,
    "style_score": 0.4418
  },
  {
    "content_id": "816fb321-c244-4a85-bd80-a97d052704f8",
    "guess": "unsure",
    "confidence": 0.6273,
    "model_score": 0.7424,
    "style_score": 0.5123
  }
]
```

**Diagnoses**

Criterion 3 missed in all three trials. The label-range set produced `human` and `unsure` only. The five GPT-6 passages were all `unsure`. Their combined scores were 0.5841, 0.6179, 0.6347, 0.4798, and 0.6273, all below 0.65. Four of those passages already had model scores at or above 0.65: 0.6928, 0.7715, 0.7836, and 0.7424. Their style scores were about 0.46 to 0.51. The equal-weight average stayed under the AI line. The remaining passage, A04, had a model score of 0.5177, already below that line. The route returned the normal unsure label. This is an evidence-based account of the averaging step. It is not a claim about the internal cause inside the model.

The attack-family marks in Attack Run — Before are a different test from these five criteria. In that baseline, four false-positive rows received an AI label, nine evasion rows avoided an AI label, and two malformed inputs still received a reader label. Six prompt-injection rows stayed on the normal scoring path. Twelve flood rows from one creator stayed within the 10-per-minute quota: ten accepted, then two HTTP 429 responses.

Making the service more willing to say `ai` could catch more of the GPT-6 passages. The same change could also label more legitimate writers as AI. I have not chosen or made that change.

---

## The Improvement

**What I changed:**

I raised `AI_THRESHOLD` in `config.py` from 0.65 to 0.72. A combined score of 0.72 or above is now the AI label. The human cutoff stays 0.35. The model and style weights stay 0.5 and 0.5. The disagreement rule in `scoring.py::combine_signals` stays 0.40. The comment next to the cutoff now says `score >= AI_THRESHOLD`, which matches `scoring.py::score_to_label`. That is the only behavior change.

**Which diagnosis pointed at it:**

The baseline evaluation missed Criterion 3. In `results/run_2026-11-08_0515_before.md`, the five GPT-6 combined scores were 0.5841, 0.6179, 0.6347, 0.4798, and 0.6273, so the label-range set never produced `ai`. The closest case was A03 at 0.6347. Lowering the AI cutoff far enough to label A03 as `ai` would also have labeled FP02 as `ai`. FP02's recorded combined score is 0.6385, which is higher than every GPT-6 combined score in that file. On the baseline attack report, four passages described as human writing were already labeled `ai`: FP04 at 0.6511, FP03 at 0.6585, FP05 at 0.6897, and FP07 at 0.7148. I widened the unsure band so those four accusations would fall below the line. I did not lower the cutoff to make Criterion 3 pass.

### Attack Run — After

The after report is `results/attack_run_2026-11-08_0553_after.md`. I compared every ID with `results/attack_run_2026-11-08_0414_before.md`. Both files contain 56 attacks. The runner again marked automatic BROKE as 0. That automatic mark only covers HTTP 500, a crash, or no response. It does not decide fairness or evasion. The HELD and BROKE marks below use the same hand rules as Attack Run — Before.

HTTP totals are the same in both reports: 37 HTTP 200, 17 HTTP 400, and 2 HTTP 429. There was no HTTP 500 and no missing attack. Model score, style score, and combined score match on every ID. The only guess changes are FP03, FP04, FP05, and FP07, from `ai` to `unsure`. Their reader-facing labels changed to the approved unsure sentence. Every other guess and every HTTP status stayed the same.

Manual totals are 41 HELD and 15 BROKE before, and 45 HELD and 11 BROKE after. The four-row drop in BROKE is those four false-positive rows.

| Family | Attacks | Before HELD | Before BROKE | After HELD | After BROKE |
|---|---:|---:|---:|---:|---:|
| evasion | 10 | 1 | 9 | 1 | 9 |
| false_positive | 8 | 4 | 4 | 8 | 0 |
| prompt_injection | 6 | 6 | 0 | 6 | 0 |
| malformed | 20 | 18 | 2 | 18 | 2 |
| flood_same_creator | 12 | 12 | 0 | 12 | 0 |

| ID | Family | HTTP status | Guess | Verdict |
|---|---|---|---|---|
| EV01 | evasion | 200 | human | BROKE |
| EV02 | evasion | 200 | unsure | BROKE |
| EV03 | evasion | 200 | unsure | BROKE |
| EV04 | evasion | 200 | unsure | BROKE |
| EV05 | evasion | 200 | unsure | BROKE |
| EV06 | evasion | 200 | unsure | BROKE |
| EV07 | evasion | 200 | unsure | BROKE |
| EV08 | evasion | 200 | human | BROKE |
| EV09 | evasion | 200 | unsure | BROKE |
| EV10 | evasion | 200 | ai | HELD |
| FP01 | false_positive | 200 | unsure | HELD |
| FP02 | false_positive | 200 | unsure | HELD |
| FP03 | false_positive | 200 | unsure | HELD |
| FP04 | false_positive | 200 | unsure | HELD |
| FP05 | false_positive | 200 | unsure | HELD |
| FP06 | false_positive | 200 | unsure | HELD |
| FP07 | false_positive | 200 | unsure | HELD |
| FP08 | false_positive | 200 | unsure | HELD |
| PI01 | prompt_injection | 200 | unsure | HELD |
| PI02 | prompt_injection | 200 | human | HELD |
| PI03 | prompt_injection | 200 | unsure | HELD |
| PI04 | prompt_injection | 200 | unsure | HELD |
| PI05 | prompt_injection | 200 | unsure | HELD |
| PI06 | prompt_injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 400 | — | HELD |
| MF03 | malformed | 200 | human | BROKE |
| MF04 | malformed | 200 | unsure | BROKE |
| MF05 | malformed | 400 | — | HELD |
| MF06 | malformed | 400 | — | HELD |
| MF07 | malformed | 200 | unsure | HELD |
| MF08 | malformed | 400 | — | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 400 | — | HELD |
| RQ11 | malformed | 400 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | HELD |
| FL01_02 | flood_same_creator | 200 | human | HELD |
| FL01_03 | flood_same_creator | 200 | human | HELD |
| FL01_04 | flood_same_creator | 200 | human | HELD |
| FL01_05 | flood_same_creator | 200 | human | HELD |
| FL01_06 | flood_same_creator | 200 | human | HELD |
| FL01_07 | flood_same_creator | 200 | human | HELD |
| FL01_08 | flood_same_creator | 200 | human | HELD |
| FL01_09 | flood_same_creator | 200 | human | HELD |
| FL01_10 | flood_same_creator | 200 | human | HELD |
| FL01_11 | flood_same_creator | 429 | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | HELD |

False-positive `ai` labels went from 4 of 8 to 0 of 8. FP03, FP04, FP05, and FP07 are HELD after because the guess is `unsure`. Their combined scores, 0.6585, 0.6511, 0.6897, and 0.7148, are all below 0.72. EV10 is still the only `ai` guess in the after report, at combined 0.819.

**Did it help, and how do I know:**

It reduced unsupported AI accusations on this attack set. Four staff-described human passages that had been labeled `ai` are now `unsure`, and the manual BROKE count fell from 15 to 11. It did not create an `ai` label for the GPT-6 evaluation samples. The after evaluation is `results/run_2026-11-08_0549_after.md`, three trials and 105 requests. Its combined scores match the baseline file, so no evaluation guess changed. The highest combined score in that run is 0.6347, which is below both 0.65 and 0.72.

| Criterion | After result |
|---|---|
| 1. False-positive protection | MET in all three trials. 0 of 10 self-reported human samples were labeled `ai`. |
| 2. Fair appeal process | Not rerun after the threshold change. The appeal code was not changed. |
| 3. Label coverage | MISSED in all three trials. The labels observed were `human` and `unsure`. |
| 4. Invalid input | MET in all three trials. 5 of 5 invalid requests returned HTTP 400 with a `bad_request` explanation and null detection fields. |
| 5. Score separation | MET in all three trials. Human mean 0.3634, AI mean 0.58876, gap 0.22536. |

Criterion 2 still rests on `results/appeals_before.md`. That file records 15 baseline appeals, five in each of three trials. Each returned HTTP 200, each added one appeal line with status `under_review`, and each original decision stayed `decided`. I did not submit new appeals after raising the cutoff.

---

## What's Still Broken

The before totals are 41 HELD and 15 BROKE. The after totals are 45 HELD and 11 BROKE. The eleven that remain are EV01 through EV09, MF03, and MF04. Their combined scores were already below 0.65, so raising the cutoff to 0.72 did not create them. EV10 still returns `ai` at combined 0.819. The remedies below are future work. I have not implemented them. Unit 8 asked for one isolated improvement. A broader redesign needs its own tests for false accusations and for evasion.

**EV01 and EV08 — the model-signal stage.** Both were scored by `detector.model_signal`, then by the equal-weight path in `scoring.py::combine_signals`, then by `score_to_label`. The signal gap is under 0.40 in both rows, so the 0.40 disagreement rule did not apply. EV01 has model score 0.1635, style score 0.4964, and combined score 0.33. EV08 has model score 0.2452, style score 0.4118, and combined score 0.3285. Both combined scores are at or below 0.35, so the guess is `human`. The low model scores are what pull the averages down. A weighted average stays between its two inputs, and neither input reaches 0.72, so changing the weights cannot make either row `ai`. Moving them only from `human` to `unsure` would still be BROKE, because an evasion that avoids the `ai` label counts as broken. Future work would retune the perplexity midpoint or steepness in `detector.model_signal`, then rerun the attack set and the human samples. The risk is that human writing with typos, short lines, or unusual words could be pushed toward an AI accusation.

**EV03 and EV09 — `scoring.py::combine_signals`.** The gap is under 0.40 on both rows, so the function uses the 0.5 / 0.5 average, and `score_to_label` reads that average. EV03 has model score 0.6662, style score 0.4413, and combined score 0.5537. EV09 has model score 0.7042, style score 0.4338, and combined score 0.569. Those model scores are already at or above the old 0.65 line. The lower style scores pull the average below both 0.65 and 0.72, so the guess stays `unsure`. Future work could raise `WEIGHT_MODEL_SIGNAL`. The false-positive trade-off is direct. FP02 has model score 0.7387 and combined score 0.6385. FP03, FP04, FP05, and FP07 have model scores from 0.8005 to 0.8816. A heavier model weight would move those staff-described human passages back toward `ai`. I have not made that change.

**EV02, EV04, EV05, EV06, and EV07 — scoring path, not one shared cause.** On each of these five rows the absolute gap between the model score and the style score is under 0.40, so `scoring.py::combine_signals` takes the equal-weight average and `score_to_label` maps it. Every combined score is below 0.65, which is why the new 0.72 cutoff leaves the labels unchanged. The saved scores do not support one common cause inside the text. EV02 is model 0.5943, style 0.3866, combined 0.4905. EV04 is model 0.6114, style 0.4919, combined 0.5516. EV06 is model 0.5727, style 0.383, combined 0.4778. EV07 is model 0.5862, style 0.3907, combined 0.4885. On those four, both inputs are below 0.65, so this average cannot reach the AI line. EV05 is different: model 0.3212 is below the 0.35 human line, style 0.4315 is in the unsure band, and combined 0.3763 is `unsure`. Both of EV05's inputs are also below 0.72, so reweighting cannot produce an `ai` label. The attack reports do not include the passages, so I cannot say which writing feature produced each score. Further investigation would mean inspecting those passages and rerunning the two signals. I am not claiming a single model failure for these five rows.

**MF03 and MF04 — input validation in `app.py` `submit`.** After the non-empty-string check, the route sets `word_count = len(text.split())` and accepts 3 to 300 tokens. `split()` counts whitespace-separated tokens, not letter-words, so control characters or spaced punctuation can pass that check and continue into scoring. MF03 returned HTTP 200 with model score 0.0, style score 0.3, and combined score 0.15, guess `human`. The gap is under 0.40, so the average was used. Style score 0.3 is not the 0.5 that `stylometry.style_signal` returns when it finds no words, so the scorer found some word characters. The report does not store the body. MF04 returned HTTP 200 with model score 0.0112, style score 0.5, and combined score 0.5, guess `unsure`. The gap is at least 0.40, so the disagreement rule forces 0.5000. Style score 0.5 matches the no-words fallback. Future work would count words with the same letter-and-number rule as `stylometry.words()`, and reject control characters before scoring. I have not made that change. The other malformed rows, including RQ01 through RQ12, still return HTTP 400 with no score. MF07 is still HELD: right-to-left text was scored, and the guess is `unsure`.

**Criterion 3 — `scoring.py::combine_signals` and `score_to_label`.** In all three after-evaluation trials, the five GPT-6 combined scores stayed `unsure` at 0.5841, 0.6179, 0.6347, 0.4798, and 0.6273. All five are below 0.72. A04's model score is 0.5177 and its style score is 0.4418, so both inputs are below 0.72 and reweighting that pair cannot reach the AI line. The other four model scores are 0.6928, 0.7715, 0.7836, and 0.7424. Their style scores are about 0.46 to 0.51, and the equal-weight average stays under 0.72. The closest combined score is A03 at 0.6347. Future work that lowered the cutoff far enough to label A03 as `ai` would also label FP02, whose combined score is 0.6385. That is a risk to writing the attack set describes as human. I have not made that change.

Four of the eight staff-described human passages changed from `ai` to `unsure`; these were the four cases with combined scores between the original 0.65 cutoff and the new 0.72 cutoff. That shows what this cutoff did on those rows. It does not show how the detector treats human writing outside this set. FP07 at 0.7148 is 0.0052 under the new line.

`unsure` means the two signals did not produce enough evidence for either confident label. It does not confirm that a person wrote the passage. The appeal records are intake records. No person adjudicated them.

Both attack reports describe the flood rows as "20 rapid submissions from one creator," and both reports contain 12 rows for that family. The saved result is 10 HTTP 200 responses for `attacker_flood`, then 2 HTTP 429 responses. The files do not say why the targeting text says 20 while the row count is 12. I am not filling that gap with a guess.

**The trade I'd make if this ran for real:**

I would keep the wider unsure band. A writer who receives a false `ai` label pays more than a reader who sees `unsure` on text that may have been generated. On this evidence, the writers in the 0.65 to 0.72 band are the ones I protected, and the readers who wanted a firm AI label on the nine evasions and the five GPT-6 samples are the ones who still do not get one.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
