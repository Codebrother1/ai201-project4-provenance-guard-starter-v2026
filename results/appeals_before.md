# Criterion 2 — Appeal Baseline (Before)

Five appeals were submitted in each of the three evaluation trials. That is 15 distinct content IDs, all taken from the first five `own human writing` submissions in `results/run_2026-11-08_0515_before.md`. Each request returned HTTP 200. The audit check below is separate from that HTTP acceptance.

## Original criterion

From `criteria.md`, left unchanged:

> All 5 out of 5 valid appeals must be successfully recorded in the audit log and have their submission status marked `under_review` in each evaluation trial.

## What the log shows

Every appeal uses this reasoning, copied from `logs/audit.jsonl`:

> I wrote this passage myself without AI assistance. I would like the result reviewed.

Each content ID has exactly one decision line and exactly one later appeal line. The 15 content IDs are unique. No selected ID has a second appeal.

The decision line stays `status` `"decided"`. The appeal is a separate line with `event` `"appeal"` and `status` `"under_review"`. The appeal copies the decision's `creator_id`. Guess, label, model score, style score, and combined score on the decision match the baseline report and were not changed. The report stores the combined score as `confidence`.

`under_review` means the appeal request was recorded. It does not mean a person reviewed the writing. No appeal in this file has been adjudicated.

| Trial | Sample | Content ID | Guess | Decision status | Appeal status | Audit check |
|---|---|---|---|---|---|---|
| 1 | H01 | `d34f5958-b5c1-44fd-a788-a5bc8b479711` | unsure | decided | under_review | PASS |
| 1 | H02 | `9a60bf19-0707-4a6c-aab4-a1d9658540ea` | human | decided | under_review | PASS |
| 1 | H03 | `bf7a9d5d-20d3-4caa-b9d5-dec6b1c7226b` | human | decided | under_review | PASS |
| 1 | H04 | `3b6ece8b-339c-4685-ae4b-016af86e6f8c` | unsure | decided | under_review | PASS |
| 1 | H05 | `e56b1dfe-5d79-4a10-9aa6-07d715b4c130` | unsure | decided | under_review | PASS |
| 2 | H01 | `b65254f2-336c-46e3-9570-864925eafa7d` | unsure | decided | under_review | PASS |
| 2 | H02 | `617d8dcf-b21b-4a2b-b10b-db8afd19723a` | human | decided | under_review | PASS |
| 2 | H03 | `e47d0a51-6cf7-49ba-985d-cdffe524cc16` | human | decided | under_review | PASS |
| 2 | H04 | `152947f5-1762-4b3e-a122-bd4bc8d04037` | unsure | decided | under_review | PASS |
| 2 | H05 | `d18d7427-c7d9-4f84-8f01-7ba5281b6155` | unsure | decided | under_review | PASS |
| 3 | H01 | `034619fa-bf16-40c0-8d5b-53277143363f` | unsure | decided | under_review | PASS |
| 3 | H02 | `b7b957d1-7e44-4509-a7a6-cb1aa304d8eb` | human | decided | under_review | PASS |
| 3 | H03 | `7568174f-cbe2-4bd6-a700-edd2b46e8efc` | human | decided | under_review | PASS |
| 3 | H04 | `32c4d305-a8f8-4d3a-9ce1-2717807dcb01` | unsure | decided | under_review | PASS |
| 3 | H05 | `01430600-6d06-4d19-b580-73228e635d16` | unsure | decided | under_review | PASS |

## Timestamps, creators, and preserved scores

Scores below are the original decision values. They match the named trial in the baseline report.

| Trial | Sample | Creator ID | Decision time | Appeal time | Model | Style | Combined |
|---|---|---|---|---|---|---|---|
| 1 | H01 | `eval_own human wr_1` | 2026-11-08T11:15:38+00:00 | 2026-11-08T11:20:16+00:00 | 0.6764 | 0.4681 | 0.5723 |
| 1 | H02 | `eval_own human wr_2` | 2026-11-08T11:15:38+00:00 | 2026-11-08T11:21:32+00:00 | 0.0207 | 0.3849 | 0.2028 |
| 1 | H03 | `eval_own human wr_3` | 2026-11-08T11:15:38+00:00 | 2026-11-08T11:22:05+00:00 | 0.0036 | 0.35 | 0.1768 |
| 1 | H04 | `eval_own human wr_4` | 2026-11-08T11:15:38+00:00 | 2026-11-08T11:22:35+00:00 | 0.2703 | 0.4799 | 0.3751 |
| 1 | H05 | `eval_own human wr_5` | 2026-11-08T11:15:38+00:00 | 2026-11-08T11:23:09+00:00 | 0.5477 | 0.4323 | 0.49 |
| 2 | H01 | `eval_own human wr_1` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:24:50+00:00 | 0.6764 | 0.4681 | 0.5723 |
| 2 | H02 | `eval_own human wr_2` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:25:21+00:00 | 0.0207 | 0.3849 | 0.2028 |
| 2 | H03 | `eval_own human wr_3` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:25:51+00:00 | 0.0036 | 0.35 | 0.1768 |
| 2 | H04 | `eval_own human wr_4` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:26:26+00:00 | 0.2703 | 0.4799 | 0.3751 |
| 2 | H05 | `eval_own human wr_5` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:27:04+00:00 | 0.5477 | 0.4323 | 0.49 |
| 3 | H01 | `eval_own human wr_1` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:28:35+00:00 | 0.6764 | 0.4681 | 0.5723 |
| 3 | H02 | `eval_own human wr_2` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:29:11+00:00 | 0.0207 | 0.3849 | 0.2028 |
| 3 | H03 | `eval_own human wr_3` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:29:45+00:00 | 0.0036 | 0.35 | 0.1768 |
| 3 | H04 | `eval_own human wr_4` | 2026-11-08T11:15:39+00:00 | 2026-11-08T11:30:19+00:00 | 0.2703 | 0.4799 | 0.3751 |
| 3 | H05 | `eval_own human wr_5` | 2026-11-08T11:15:40+00:00 | 2026-11-08T11:30:51+00:00 | 0.5477 | 0.4323 | 0.49 |

## Proposed trial results

These marks use the append-only reading: five appeals were accepted, five appeal lines were stored, and five original decisions stayed `decided`.

| Trial | HTTP 200 | Audit pairs | Proposal |
|---|---|---|---|
| 1 | 5 of 5 | 5 of 5 PASS | PROPOSED MET |
| 2 | 5 of 5 | 5 of 5 PASS | PROPOSED MET |
| 3 | 5 of 5 | 5 of 5 PASS | PROPOSED MET |

The original criterion asks for the submission status itself to be marked `under_review`. This log does not do that. It appends an appeal event and leaves the decision as `decided`. A later clarification can be added underneath the original criterion line. The original sentence was not changed for this file.
