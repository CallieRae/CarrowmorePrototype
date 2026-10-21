# Carrowmore: what a keeper is qualified for, nearly qualified for, and the shortest honest route

Senior PM, Zero to One exercise. Read in this order: `FRAMING.md` (the bet), the prototype, then `CALL.md` (kill, pivot or persevere, with the evidence and the three written answers).

## Open the prototype

Open `prototype/index.html` in any browser. It needs no install or server; without a network it falls back from Plus Jakarta Sans to Arial.

Sign in as a **keeper** (any keeper code, e.g. `K0566` or `K1483`, password `carrowmore`) to see one record only, with a drop-down of open roles: pick a role to see how the record compares, the training needed for it, and where the keeper is asked to clarify. Two roles are assessed; the other four postings are listed but marked as not yet assessed. Sign in as an **employer** (any email, password `array`) to browse all shared records by role, sorted alphabetically or by closeness to ready.

The sign-in is a prototype affordance, not security: every record is in the one file. It's there to show how the two views are scoped differently.

To rebuild it from the data (Python 3, standard library only):

```
python3 prototype/build.py
```

## What's here

| Path | What it is |
|---|---|
| `FRAMING.md` | The one-page framing |
| `CALL.md` | The call, the evidence behind it, and the Section 6 answers |
| `EVALUATION_PLAN.md` | The test and its kill rules, committed before any AI output existed |
| `ai-was-wrong.md` | Running log of where the AI was wrong and what I did about it |
| `prototype/` | The keeper and employer views (`index.html`), the template and build script, and the Pearson logo from the brand guidelines |
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

The commit history is the audit trail: rules (`ed3fd56`), hand grades (`1430b6d`), AI labels (`e53487b`), second grading pass (`b784d07`).
