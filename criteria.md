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
