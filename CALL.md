# The call: persevere, with an advisor in the loop

**Persevere on the keeper-facing translation, and ship it advisor-reviewed until a second grader and a larger sample prove the overclaim rate.** The rules I committed before the AI ran returned *inconclusive, leaning persevere*. I would rather report that than round it up.

## The evidence

Ten keepers, chosen by rule, were graded blind by hand before the AI ran; three were held out from any tuning (`EVALUATION_PLAN.md`).

| | AI | Keyword search |
|---|---|---|
| Overclaims (says Evidenced, citations don't hold up) | 6% (2 of 32; 95% CI 2 to 20%) | 32% (12 of 38) |
| Recall | 79% (30 of 38) | 68% (26 of 38) |
| Citations that hold up | 65% | 43% |
| Held-out keepers: overclaims, recall | 10%, 75% | 50%, 50% |

The AI beat keyword search on both the tuning and held-out keepers, which was the primary test. Overclaims sit inside the persevere band but within five points of its edge, with an interval running to 20%, so fifty cells can't separate persevere from pivot. The same model wrote the grading guide's examples and the AI labels, so I reran without those 30 sentences: overclaims rise to 10%, still inconclusive.

## Actual vs expected

- I expected the Array's O&M role to be blocked by certificates. It asks for one (offshore safety) plus a medical, and says it would rather train good people. The value is evidence of capability at shortlist and pay-band stage, not routing to courses.
- I expected "nearly qualified" to be rare. Of 38 current keepers, 23 hold some HV Authorized Person modules and 2 hold the full certificate. The gap is modules, not careers.
- I expected messy narrative logs. The clean logs are templated: 10,627 entries, 1,270 distinct sentences, about 620 once numbers are masked. That made hand-grading feasible, and it means a lookup table might match the AI here. The AI earns its keep on raw text, which I didn't test.
- The clean README says certification status wasn't resolved; `keepers.json` carries it. I treated it as data to check, not truth.

## Where the time went

Most of it went to the line between what a log can show and what must be proven elsewhere. Logs carried maintenance (no overclaims; all 10 keepers my grades counted), fault-finding (8 of 9) and permit work (4 of 4) well. They carry HV switching badly: entries rarely state the voltage, so the AI marked them "possible" and found only 2 of 6. That is the right failure for an insurer gate, and the weakest number in the set. "Comfortable at height" is a disposition, and logs show exposure at best. Authorization, certificates and the medical never come from logs, and the tool never lets them. Most disagreements between my grades and the AI were domain knowledge ("worked the mast head", "racked out breaker"), which makes a second grader with an electrical background the next test.

## Who it serves, and the overlap

Keepers need their own work in an employer's words, and a route. The redeployment team needs to know whom the Array should interview, and on what evidence. The Array needs capability it can trust at offer stage; its insurer needs paper. The overlap is one body of cited evidence read through different lenses, so the prototype has one record and two views. The keeper sees their record against each open role, the training it needs and the questions only they can answer. The employer browses shared records sorted by closest to ready, with the reasons shown and no percentage.

## What I chose not to build

- The raw pack. Attribution took the Authority three weeks for forty keepers; at 340 it is the kill at scale, and an ingestion problem rather than the one I was testing. With raw, I would attribute first, then rerun the era test on the 1985 to 2003 scans, where the fairness risk to long-serving keepers actually lives. On clean data, recall by era was flat (66, 67, 70%), which is the clean subset hiding the problem.
- A match percentage. "Closest to ready" ranks by requirements left to clear, and shows why.
- Four of the six postings (listed, marked not yet assessed), learning-rate prediction, cost of candidacy and requirement weighting. Appraisals and manager notes are out by design.
- Real authentication. I built a mock sign-in anyway, because who sees what is a product decision here: a keeper sees only their own record, and nothing reaches an employer unseen. It is not security; every record is in one file.

## Where the AI was wrong, and where I stopped delegating

The running log is `ai-was-wrong.md`. The moments that mattered:

- It invented a figure ("eleven entries") in the first framing draft. Every number was checked against the data after that.
- It offered a 20% kill threshold that, asked how it was derived, had no basis: it blended overclaims with misses, ignored sample size and had no baseline. The rules were rebuilt and committed before any AI output existed.
- Its first scoring rule let a cite-everything keyword search win by burying two good entries among fifteen. Caught on a dummy run.
- Its sensitivity check first reported 19%, which would have flipped the call to pivot; a bug left verdicts standing after their citations were removed. The jump looked too large to be real.
- It wrote "your logs suggest you may once have held [an HV authorization]" into the keeper view, the exact overclaim the brief warns about.
- I graded by hand rather than let the AI pre-grade, because it would have been marking its own work.

## If this graduated

Throw away first: the one-pass label file (an artifact of templated data), the single HTML file with every record inside it, and the mock sign-in. Keep: the four tiers and the rule that log evidence never upgrades a license or insurer gate; every claim cited to its source line; the "where we need you to clarify" loop, which turns the keeper into a source of evidence rather than its subject; and the pre-registered harness (blind pooled grading, holdout, baseline), which is what makes the next number trustworthy.

## Accessibility, outside reaction, time

Plain language throughout. Tiers carry a symbol as well as a color. White text on the turquoise input box measures 4.45:1, so it is set large and bold to pass. The whole tool is one 830 KB file that works offline.

Outside reaction: [to add after the review].

Time actually spent: [to add].
