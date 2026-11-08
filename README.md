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

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
