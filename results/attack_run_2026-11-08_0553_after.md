# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 05:53
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `e3abd0c3-6447-45b0-8648-51935a899491` | human | 0.330 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d70be861-5798-4b07-a0d2-443d8c9247fd` | unsure | 0.490 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `92032147-a543-4a8f-b6dc-a16dd051c2cf` | unsure | 0.554 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d58fb423-9af5-4fed-965f-0048aa8526b7` | unsure | 0.552 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5018f43b-8974-4436-8eb2-ec00326a6aeb` | unsure | 0.376 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `ace0721b-bce7-4337-8626-7f716b3b575b` | unsure | 0.478 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e564b586-1832-46d5-823c-2479b5813485` | unsure | 0.488 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `49950f21-fe66-4f09-977a-e0c01e7c139f` | human | 0.329 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6e395239-dfd8-4f0f-b461-b3125b9709cb` | unsure | 0.569 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ea64bac4-b7ec-4f2d-bd08-e6d01050bf7e` | ai | 0.819 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `21ea91bd-6071-4fec-9ed6-dc8e661100f1` | unsure | 0.554 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `482b2e1a-fc7e-4517-8abb-d5796dc686f8` | unsure | 0.638 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `8a23f436-1072-4111-afe4-3e9283909268` | unsure | 0.658 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `40095126-ce2c-4bee-ae2a-cd2e8c6b529c` | unsure | 0.651 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `4add0dc2-7ba8-4798-94d6-4bec54f7b39e` | unsure | 0.690 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `0a67f5dd-54df-4672-9070-20a576a61822` | unsure | 0.500 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b9a782b8-b957-4949-8066-43131ba76467` | unsure | 0.715 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `23f6c7e7-c508-450f-a142-4515c710c946` | unsure | 0.351 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `5adf6ec7-0c48-4064-a531-5dd8f75080ef` | unsure | 0.415 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cc984745-b621-4973-843f-92c9cdafd059` | human | 0.282 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1ac2998e-1525-4642-8110-65e8df9e18af` | unsure | 0.514 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b79b0e79-94ce-408a-bed9-f3b6cb99d1c1` | unsure | 0.471 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `0d9e192f-c62f-4fdd-acc4-c5094aa7db56` | unsure | 0.513 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7f79ac0c-46f3-4a0c-91a6-0188d732985b` | unsure | 0.526 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `5d79d342-7051-4696-a605-9a51e896b0fa` | human | 0.150 |  |
| MF04 | malformed | text is only punctuation | 200 | `9c681be2-a524-491e-b40e-c2f211c37f91` | unsure | 0.500 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `a575ef0d-c945-4e47-b4ce-9f41e7acf378` | unsure | 0.500 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `02ee4c00-58bf-4916-850b-9956ed3c54dc` | human | 0.164 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `713af2f6-90a7-4dba-bd80-af828061324e` | human | 0.164 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9777292b-5ad8-4ea6-9873-cc8a997a6472` | human | 0.164 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c66471c3-aa74-463a-8a10-30132092f67c` | human | 0.164 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8976455e-7f8f-42d1-b0a8-032c16defffc` | human | 0.164 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `80060ed5-ecc7-44c7-91ab-a88d02a41bd5` | human | 0.164 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3464f109-e765-4d14-9051-2c6eac5f50a3` | human | 0.164 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7ecfc115-c710-43c8-a523-61aa251aa6e5` | human | 0.164 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47518d27-10ee-4e8c-ba96-c18eadf8f008` | human | 0.164 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a5072da-da6c-4f8a-81b7-c92f102d068b` | human | 0.164 |  |
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
  "content_id": "e3abd0c3-6447-45b0-8648-51935a899491",
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
  "content_id": "d70be861-5798-4b07-a0d2-443d8c9247fd",
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
  "content_id": "92032147-a543-4a8f-b6dc-a16dd051c2cf",
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
  "content_id": "d58fb423-9af5-4fed-965f-0048aa8526b7",
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
  "content_id": "5018f43b-8974-4436-8eb2-ec00326a6aeb",
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
  "content_id": "ace0721b-bce7-4337-8626-7f716b3b575b",
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
  "content_id": "e564b586-1832-46d5-823c-2479b5813485",
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
  "content_id": "49950f21-fe66-4f09-977a-e0c01e7c139f",
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
  "content_id": "6e395239-dfd8-4f0f-b461-b3125b9709cb",
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
  "content_id": "ea64bac4-b7ec-4f2d-bd08-e6d01050bf7e",
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
  "content_id": "21ea91bd-6071-4fec-9ed6-dc8e661100f1",
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
  "content_id": "482b2e1a-fc7e-4517-8abb-d5796dc686f8",
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
  "content_id": "8a23f436-1072-4111-afe4-3e9283909268",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6585,
  "model_score": 0.8051,
  "style_score": 0.512,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
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
  "content_id": "40095126-ce2c-4bee-ae2a-cd2e8c6b529c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6511,
  "model_score": 0.8329,
  "style_score": 0.4692,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
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
  "content_id": "4add0dc2-7ba8-4798-94d6-4bec54f7b39e",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6897,
  "model_score": 0.8005,
  "style_score": 0.579,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
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
  "content_id": "0a67f5dd-54df-4672-9070-20a576a61822",
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
  "content_id": "b9a782b8-b957-4949-8066-43131ba76467",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7148,
  "model_score": 0.8816,
  "style_score": 0.548,
  "label": "Our analysis could not confidently determine whether this writing was human-written or AI-generated. Detection tools can make mistakes, and this result is not an accusation. If you disagree, you may request a review.",
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
  "content_id": "23f6c7e7-c508-450f-a142-4515c710c946",
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
  "content_id": "5adf6ec7-0c48-4064-a531-5dd8f75080ef",
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
  "content_id": "cc984745-b621-4973-843f-92c9cdafd059",
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
  "content_id": "1ac2998e-1525-4642-8110-65e8df9e18af",
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
  "content_id": "b79b0e79-94ce-408a-bed9-f3b6cb99d1c1",
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
  "content_id": "0d9e192f-c62f-4fdd-acc4-c5094aa7db56",
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
  "content_id": "7f79ac0c-46f3-4a0c-91a6-0188d732985b",
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
  "content_id": "5d79d342-7051-4696-a605-9a51e896b0fa",
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
  "content_id": "9c681be2-a524-491e-b40e-c2f211c37f91",
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
  "content_id": "a575ef0d-c945-4e47-b4ce-9f41e7acf378",
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
  "content_id": "02ee4c00-58bf-4916-850b-9956ed3c54dc",
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
  "content_id": "713af2f6-90a7-4dba-bd80-af828061324e",
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
  "content_id": "9777292b-5ad8-4ea6-9873-cc8a997a6472",
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
  "content_id": "c66471c3-aa74-463a-8a10-30132092f67c",
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
  "content_id": "8976455e-7f8f-42d1-b0a8-032c16defffc",
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
  "content_id": "80060ed5-ecc7-44c7-91ab-a88d02a41bd5",
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
  "content_id": "3464f109-e765-4d14-9051-2c6eac5f50a3",
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
  "content_id": "7ecfc115-c710-43c8-a523-61aa251aa6e5",
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
  "content_id": "47518d27-10ee-4e8c-ba96-c18eadf8f008",
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
  "content_id": "2a5072da-da6c-4f8a-81b7-c92f102d068b",
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
