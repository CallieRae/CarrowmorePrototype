# Evaluation plan

These rules were set and committed before any AI mapping ran. The commit timestamp is the evidence, and the same rules are encoded in `eval/score.py` so the call can't be reshaped after the results are in.

## What gets graded

**Keepers.** Ten, chosen by rule rather than by eye (`eval/select_keepers.py`, seed 2029). From the 38 current keepers, split into tenure terciles, the draw takes 3 long-serving, 4 mid and 3 short, with at least 3 carrying heavy era-1 evidence (100 or more entries from 1985 to 2003), at least 3 rock and 3 shore keepers, and at least 1 island keeper. Three of the ten, one per tercile, are held out: graded, but never used to fix a prompt or a rule.

**Requirements.** Five, drawn from the two Array postings (`eval/requirements.json`): hands-on plant maintenance, electrical fault-finding, working to a permit system, HV switching (an insurer gate), and working at height or in confined spaces. The last is included on purpose as the one we expect logs to evidence poorly, since "comfortable at height" is a disposition and logs can only show exposure.

**The judgment.** One question per item: *does this entry show the keeper personally doing this?* Y, N, or ? (counted as N). I'm not a turbine or HV assessor, so I grade only whether an entry supports the claim, never whether a keeper is competent. Standing by, holding keys or watching someone else does not count.

**The unit.** The clean logbooks are heavily templated: 10,627 entries, 1,270 distinct sentences, about 620 once numbers are masked. A sentence is graded once and the grade applies to every entry that uses it.

**The pool.** For each keeper and requirement: every sentence the keyword baseline matches, plus 2 seeded random sentences it doesn't, plus (later) every sentence the AI cites. That came to 188 distinct sentences before the AI ran. The sheet has one row per sentence and one column per requirement, so every sentence is judged against all five; the grader marks only `Y` or `?`, and blank means No (`eval/GRADING_GUIDE.md`). Rows are alphabetical, which groups near-duplicates and reveals nothing about which method surfaced them. Any supporting sentence that no method surfaced and the random draw missed stays invisible, a known limit of pooled evaluation.

*Revised before grading began:* the first sheet had 283 rows, one per sentence and requirement pair. It was collapsed to the layout above to cut grading time and widen coverage. No grades or AI outputs existed at the time.

A keeper counts as **Evidenced** for a requirement when at least 2 of their entries are graded as supporting it.

## What gets measured

- **Overclaim rate:** of the cells a method marks Evidenced, the share where fewer than 2 of its own cited entries hold up.
- **Recall:** of the cells the hand grades show as Evidenced, the share the method found with at least 2 supporting citations.
- **Citation precision:** the share of cited entries that hold up. This is what a keeper actually reads.

Each is reported overall, per requirement, per split (dev and holdout) and per era of evidence, with 95% Wilson intervals.

## Decision rules, applied in order

1. **Gate.** If HV switching is ever marked as met from log evidence, that's a defect. Fix it in code; kill only if no rule can prevent it.
2. **Beat the baseline (primary).** On the holdout keepers, the AI must give a cleaner evidence list than keyword search (higher citation precision), overclaim no more, and trail its recall by no more than 10 points. If it fails on holdout, kill. If dev and holdout disagree, the result is inconclusive.
3. **Recall floor.** AI recall below 50% is a kill: the over-cautious search engine the brief warns about.
4. **Overclaim bands.** 10% or below: persevere. Above 10% up to 25%: pivot to a drafting aid an advisor reviews before any keeper sees it. Above 25%: kill. A point estimate within 5 points of a band edge, with an interval spanning two bands, is inconclusive; an interval that merely reaches into another band makes the call provisional.
5. **Per requirement.** Any requirement with AI overclaim above 50%, or recall below 30%, is dropped from the tool and reported, not averaged away.
6. **Fairness.** If era-1 recall trails era-3 by more than 20 points, flag it as a finding. I expect a null result here, because the Authority hand-transcribed the era-1 scans for `clean/`. That null would itself be the point: the clean subset hides the OCR penalty the raw data would impose on the longest-serving keepers.
7. **Wording.** Whether a reader takes *Evidenced* to mean *qualified* rests on one tester at most. It's reported as a quote, not a score.

## Why these numbers

A keeper sees roughly six graded requirements. If errors were independent, a 10% overclaim rate would put at least one false claim on 47% of profiles, and 20% would put one on 74%. Anything above 10% therefore needs an advisor in the loop. With about 50 cells the intervals are wide (10 errors in 50 could plausibly mean anything from 11% to 33%), so this experiment can show whether the approach is plausible, not that it is safe.

## Known weaknesses

- One grader, a layperson, is the ground truth.
- Fifty cells, ten keepers, a non-random clean subset.
- Because the logs are templated, a hand-built lookup of 620 sentences might beat both methods on this data. Real logs, and the raw pack, are not templated, which is where the AI would have to earn its keep.

## Running it

```
python3 eval/select_keepers.py        # who gets graded
python3 eval/build_grading_sheet.py   # blind sheet -> eval/grading_sheet.csv
python3 eval/baseline_keyword.py      # keyword predictions
# grade eval/grading_sheet.csv; run the AI mapper; add its citations
python3 eval/score.py                 # results and the call
```
