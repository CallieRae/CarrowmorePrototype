# Carrowmore: what a keeper is qualified for, nearly qualified for, and the shortest route

> **Post-submission sandboxing.** The last commit of the exercise is `b6cc45b` ("Final write-up", 21 Oct 2026). Everything after it is interface work done afterwards: the First Light sign-in, the gradient backdrop, sign-in autofill, the keeper's Show menu and titled containers, the employer's count buttons and Logged experience sort, and fixes from a later QA pass. The evidence logic (how each requirement is labelled and ranked), the evaluation and its results are unchanged; `CALL.md` gains one item in its list of what to throw away. To see the prototype as it stood: `git checkout b6cc45b`.

Senior PM, Zero to One exercise. Read in this order: `FRAMING.md` (the bet), the prototype, then `CALL.md` (the call, QA, and the three written answers). The two are also combined as a one-page Word file, `Carrowmore_Framing_and_Call.docx`.

## Open the prototype

**Live:** https://callierae.github.io/CarrowmorePrototype/prototype/

Or open `prototype/index.html` in any browser. It needs no install or server; without a network it falls back from Plus Jakarta Sans to Arial.

- **Keeper/Applicant:** any keeper code (e.g. `K0566`, `K1483`, `K0303`), password `carrowmore`. One record only: choose an open role to see how the record compares, the training it needs, and where the keeper is asked to clarify. Two roles are assessed; the other four postings are listed but marked as not yet assessed. **Show** narrows the page to one part: Full Posting, Role Summary, All Qualifications, Required Certifications, Required Skills/Experience, Open Questions or Training Path. The role card is split into Role Description, Role Certification and Role Experience.
- **Employer/Advisor:** any email, password `array`. Choose a role and a candidate; sort by closest to ready (requirements left to clear), by logged experience, or alphabetically. Each candidate's summary has count buttons, never percentages: requirements on record, certifications held, medical on record (✓) or not (?), and experience shown in the logs. Each jumps to its section. Logged HV switching never counts toward requirements on record, because logs cannot clear an insurer requirement.
- **Autofill (prototype only):** clicking into a sign-in box fills a working value, left visible and editable; each further click in the keeper code box steps to the next keeper. Passwords show as plain text.

The sign-in is a prototype affordance, not security: every record is in the one file. It's there to show how the two views are scoped differently. It opens on a short intro, the lighthouse coming up from dark; any key or tap skips it, and it is off for anyone who has reduced motion turned on.

### What the labels mean

| Label | Meaning |
|---|---|
| ✓ Qualified and/or Certified | Certificate held and in date (flagged where the training records show no renewal) |
| ◐ Nearly Qualified (Partial Cert) | Some modules held, or the certificate has lapsed |
| ● Logged experience, needs validation or cert | Logs show the work on at least two dates in two different entries; to confirm with the keeper, or a certificate not on record. On HV switching: *needs authorization* |
| ○ Insufficient Documented Qualifications | Logs don't show the work clearly enough yet, or no certificate or medical in the training records |

Each requirement is tagged REQUIRED or PREFERRED, following the posting. Log evidence never marks an insurer gate as met.

To rebuild the page from the data (Python 3, standard library only):

```
python3 prototype/build.py
```

## What's here

| Path | What it is |
|---|---|
| `FRAMING.md` | The one-page framing, including what I chose not to build |
| `CALL.md` | The call, the evidence, QA (reviewer feedback, AI errors, build fixes) and what to keep |
| `Carrowmore_Framing_and_Call.docx` | `FRAMING.md` and `CALL.md` on one branded page |
| `EVALUATION_PLAN.md` | The test and its kill rules, committed before any AI output existed |
| `ai-was-wrong.md` | Running log of every error found, by the AI, the build or QA, and what changed |
| `prototype/` | The keeper and employer views (`index.html`), template, build script and the Pearson logo from the brand guidelines |
| `prototype/sign-in-options/` | Three sign-in intro studies (First Light, Beacon, Approach); First Light is the one in use |
| `prompts/map_prompt.md` | The prompt the AI followed to label log sentences |
| `eval/` | Keeper selection, keyword baseline, blind grading sheets, AI labels, scoring |
| `carrowmore-data-pack/` | `clean/`, `employers/` and `reference/` from the supplied pack; `raw/` is not committed |

## Re-run the evaluation

```
python3 eval/baseline_keyword.py
python3 eval/predict_ai.py
python3 eval/score.py                  # main result
python3 eval/score.py --exclude-guide  # sensitivity: drops the grading guide's example sentences
```

The commit history is the audit trail: rules (`ed3fd56`), hand grades (`1430b6d`), AI labels (`e53487b`), second grading pass (`b784d07`), scoring (`ce2392f`).

## What changed after the test

The scored results use the pre-registered rule (two supporting entries). After QA, the tool applies a stricter rule (two different dates and two different sentences), which re-scores at 6.5% overclaims and 76% recall on the same ten keepers; the call is unchanged. Tier names changed after outside review (`ai-was-wrong.md`, #13 to #16); `EVALUATION_PLAN.md` keeps the original names because it was committed before results.
