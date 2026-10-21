# Carrowmore: what a keeper is qualified for, nearly qualified for, and the shortest honest route

Senior PM, Zero to One exercise. Start with `FRAMING.md` (the bet), then open the prototype.

## Open the prototype

Open `prototype/keeper_view.html` in any browser. It needs no install, server or network. Pick a keeper from the list; add `#K0566` to the URL to jump to one with HV evidence.

To rebuild it from the data (Python 3, standard library only):

```
python3 prototype/build.py
```

## What's here

| Path | What it is |
|---|---|
| `FRAMING.md` | The one-page framing |
| `EVALUATION_PLAN.md` | The test and its kill rules, committed before any AI output existed |
| `ai-was-wrong.md` | Running log of where the AI was wrong and what I did about it |
| `prototype/` | The keeper view and its build script |
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
