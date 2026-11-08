# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 04:14
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `0ae0ad37-cbcd-4bdf-8610-6f4295001839` | human | 0.330 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `736aa2f1-a4a7-48fd-9bd5-09bd2a2d9f31` | unsure | 0.490 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d622a0d6-32d9-4432-ba01-b6bb11e2b2b3` | unsure | 0.554 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `bcae3315-f243-406b-ba9a-8130f4e12852` | unsure | 0.552 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `0aa2c656-165d-46cf-9cdf-d97726e34a7b` | unsure | 0.376 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `03a70212-4fa5-489a-ae57-87b44751dbf6` | unsure | 0.478 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `0c8cbe44-8b42-4127-b18d-22b45d3ed985` | unsure | 0.488 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `7d155b1b-59b4-4e24-a634-a2319d175dfc` | human | 0.329 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `a3c1a88c-a76c-4a5d-8c97-8f07dc3d41b7` | unsure | 0.569 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f7f7fd75-1958-49d2-a14c-00e27cd879d9` | ai | 0.819 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `33613beb-54f8-4fcb-a42f-6e99e9782ba3` | unsure | 0.554 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `ca8fcc5f-c3e5-4d92-86f8-d376739f1ce8` | unsure | 0.638 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `745855e3-52ee-4372-be13-c7d7b77658a7` | ai | 0.658 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `b6491ac3-4c6e-43f1-b243-30a408bf6aab` | ai | 0.651 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `a8b29ed7-9685-44e4-a116-5f448a975358` | ai | 0.690 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `440f87f1-f033-4257-af88-f4692bde0020` | unsure | 0.500 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `172711d3-1975-4e3c-952e-a65705fe1b71` | ai | 0.715 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `b726b39f-a2a8-4910-9c15-1270c3f2a3e7` | unsure | 0.351 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6e165882-fe1f-4eba-a0b4-60d194dafb3a` | unsure | 0.415 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `6f189270-d872-46bd-805d-e396be31ce50` | human | 0.282 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `bfed6d68-7fd8-4e8d-af9d-9784f912f58c` | unsure | 0.514 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f61bd163-8b7f-49b8-96cd-666034496f1f` | unsure | 0.471 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `77bbc24b-e0d1-4db7-9bdc-f3efd5403d04` | unsure | 0.513 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f48a028c-7b01-4880-8f23-d638895ff81e` | unsure | 0.526 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `a1a9c668-ecba-4b9c-8c2b-f2c219022da5` | human | 0.150 |  |
| MF04 | malformed | text is only punctuation | 200 | `d81ed079-a4f2-4af3-bf60-600fb9b3de3a` | unsure | 0.500 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `7cae69e8-c428-47ae-9851-7878bdc2e7b2` | unsure | 0.500 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `39a2318a-f053-4944-b3b9-b06221678523` | human | 0.164 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `20d90821-aa25-4b8b-b05b-d1351f3cbeca` | human | 0.164 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ff92b050-21ee-4057-a2c2-219426787d6f` | human | 0.164 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `908c22d5-1343-4d9f-b274-f381ce38fcfb` | human | 0.164 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1181b3b6-571c-437e-acfc-0c1ae481e644` | human | 0.164 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bbd00472-7eac-40f2-a05c-f5aa0a9e70cc` | human | 0.164 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `58225516-6630-4790-b4c1-b1c3cfb8ef83` | human | 0.164 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `75622a1c-1fbb-463e-a8a5-6a0bb9e9783d` | human | 0.164 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a0081e07-771e-421e-ad15-a4d0d5f816a5` | human | 0.164 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4727e5f1-e84e-42a2-87d1-01897692e581` | human | 0.164 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "0ae0ad37-cbcd-4bdf-8610-6f4295001839",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.33,
  "model_score": 0.1635,
  "style_score": 0.4964,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "736aa2f1-a4a7-48fd-9bd5-09bd2a2d9f31",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4905,
  "model_score": 0.5943,
  "style_score": 0.3866,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d622a0d6-32d9-4432-ba01-b6bb11e2b2b3",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5537,
  "model_score": 0.6662,
  "style_score": 0.4413,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "bcae3315-f243-406b-ba9a-8130f4e12852",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5516,
  "model_score": 0.6114,
  "style_score": 0.4919,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "0aa2c656-165d-46cf-9cdf-d97726e34a7b",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3763,
  "model_score": 0.3212,
  "style_score": 0.4315,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "03a70212-4fa5-489a-ae57-87b44751dbf6",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4778,
  "model_score": 0.5727,
  "style_score": 0.383,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "0c8cbe44-8b42-4127-b18d-22b45d3ed985",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4885,
  "model_score": 0.5862,
  "style_score": 0.3907,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "7d155b1b-59b4-4e24-a634-a2319d175dfc",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3285,
  "model_score": 0.2452,
  "style_score": 0.4118,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "a3c1a88c-a76c-4a5d-8c97-8f07dc3d41b7",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.569,
  "model_score": 0.7042,
  "style_score": 0.4338,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "f7f7fd75-1958-49d2-a14c-00e27cd879d9",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.819,
  "model_score": 0.9792,
  "style_score": 0.6588,
  "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "33613beb-54f8-4fcb-a42f-6e99e9782ba3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5542,
  "model_score": 0.6175,
  "style_score": 0.4909,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "ca8fcc5f-c3e5-4d92-86f8-d376739f1ce8",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6385,
  "model_score": 0.7387,
  "style_score": 0.5383,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "745855e3-52ee-4372-be13-c7d7b77658a7",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6585,
  "model_score": 0.8051,
  "style_score": 0.512,
  "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "b6491ac3-4c6e-43f1-b243-30a408bf6aab",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6511,
  "model_score": 0.8329,
  "style_score": 0.4692,
  "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "a8b29ed7-9685-44e4-a116-5f448a975358",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6897,
  "model_score": 0.8005,
  "style_score": 0.579,
  "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "440f87f1-f033-4257-af88-f4692bde0020",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.4696,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "172711d3-1975-4e3c-952e-a65705fe1b71",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7148,
  "model_score": 0.8816,
  "style_score": 0.548,
  "label": "Our analysis found writing patterns that may be associated with AI-generated content. However, this result does not prove AI was used, and our detection system can make mistakes. If you believe this assessment is incorrect, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "b726b39f-a2a8-4910-9c15-1270c3f2a3e7",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3507,
  "model_score": 0.3223,
  "style_score": 0.3791,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6e165882-fe1f-4eba-a0b4-60d194dafb3a",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4149,
  "model_score": 0.4625,
  "style_score": 0.3672,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "6f189270-d872-46bd-805d-e396be31ce50",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2822,
  "model_score": 0.2044,
  "style_score": 0.3599,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "bfed6d68-7fd8-4e8d-af9d-9784f912f58c",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5142,
  "model_score": 0.5943,
  "style_score": 0.4342,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "f61bd163-8b7f-49b8-96cd-666034496f1f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4706,
  "model_score": 0.4998,
  "style_score": 0.4413,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "77bbc24b-e0d1-4db7-9bdc-f3efd5403d04",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5127,
  "model_score": 0.6401,
  "style_score": 0.3852,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "f48a028c-7b01-4880-8f23-d638895ff81e",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5259,
  "model_score": 0.5583,
  "style_score": 0.4935,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "a1a9c668-ecba-4b9c-8c2b-f2c219022da5",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.15,
  "model_score": 0.0,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "d81ed079-a4f2-4af3-bf60-600fb9b3de3a",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "7cae69e8-c428-47ae-9851-7878bdc2e7b2",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "39a2318a-f053-4944-b3b9-b06221678523",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "20d90821-aa25-4b8b-b05b-d1351f3cbeca",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "ff92b050-21ee-4057-a2c2-219426787d6f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "908c22d5-1343-4d9f-b274-f381ce38fcfb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "1181b3b6-571c-437e-acfc-0c1ae481e644",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "bbd00472-7eac-40f2-a05c-f5aa0a9e70cc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "58225516-6630-4790-b4c1-b1c3cfb8ef83",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "75622a1c-1fbb-463e-a8a5-6a0bb9e9783d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "a0081e07-771e-421e-ad15-a4d0d5f816a5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "4727e5f1-e84e-42a2-87d1-01897692e581",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1643,
  "model_score": 0.0287,
  "style_score": 0.3,
  "label": "Our analysis found writing patterns that are more consistent with human-written content. However, AI detection is not perfect, so this result should not be treated as proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
