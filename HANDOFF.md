# HANDOFF — read this first

Working context for any Claude session picking up this repo. This is a working file, not a deliverable. Delete it or move it to `/notes` before submitting.

**Owner:** Callie Rae McSpadden · **Brief:** Carrowmore, Senior PM Zero to One (Pearson EL&S, New Product Innovation)
**Submit to:** greg.davis@pearson.com, as a repo link with its real commit history. **Time budget:** 4 hours total; record the actual time spent.
**Status at handoff (19 Oct 2026):** about 0:20 used. The data read is done. Next up: the one-page framing.

---

## 1. What the brief asks for

The brief is to frame the bet and then build the thing that could kill it. Hand in:

1. **One-page framing.** Problem and whose it is; beliefs we can't yet prove; the one belief that would sink it.
2. **A working artefact** that can be run from this repo. Rough is fine. A deck with no artefact fails outright.
3. **A kill, pivot or persevere call** with the evidence behind it, in a few paragraphs.
4. **Section 6 answers**, folded into the framing and the call: (a) what we chose not to build and why; (b) where the AI was wrong and what we did about it, naming specific moments; (c) if this graduated, what we'd throw away first and what we'd keep.

The scoring criteria are problem selection (loudest), craft, honesty about uncertainty (handled in the data and the language, not with a label), tool leverage, and scoping judgement. Accessibility is optional, and worth mentioning if it shaped what we built.

## 2. Decisions made

- **Primary user: the keeper.** The question we answer for them: *"What am I qualified for, what am I nearly qualified for, and what is the shortest honest route to a job?"* An employer or redeployment shortlist is a secondary view at most.
- **No composite match score.** "78% match" is the false precision the panel is testing for. Each requirement gets an evidence tier instead.
- **Data: `clean/` only.** We say so in the write-up, with the reasons: the question lives in the interface and the inference, not in ingestion, and `raw/` identity resolution would use the whole four hours. Raw identity resolution is the real kill at a scale of 340 keepers, and we should say that too.
- **Target postings:** the **Carrowmore Array O&M Technician** posting (about 40 hires) is the main test. The **HV Authorized Person** posting is a single sharp example of the "possible lapsed authorization" problem.
- **The riskiest belief, which is the one to test:** *inferred work evidence can be mapped to employer requirements accurately enough, and worded honestly enough, that a person acts on it correctly.*
- **Beliefs we can't test in 4 hours:** learning rate and upskilling speed, and whether employers will accept inferred evidence.

## 3. Evidence tiers (the honesty lives here)

| Tier | Source | Wording rule |
|---|---|---|
| **Authorized** | `certifications[]` shows complete and valid in 2026 | Show the expiry year |
| **Nearly Qualified (Partial Cert)** | `certifications[]` shows some modules held | Name the modules held and the modules missing |
| **Evidenced** | Logbook entries | Show the count, the date range and the cited source entries, e.g. "HV switching recorded 11× across 2019–2023" |
| **Not yet shown** | Nothing found | Give the route to close the gap. Never use the word "unqualified" |

**Hard rule:** log evidence never upgrades a license or insurer gate to "met." Apply recency: a 1998 entry counts for less than a 2024 one. Use the keeper's own vocabulary alongside the employer's.

## 4. Kill thresholds (set before building)

1. **Attribution.** This is resolved in `clean/` by three weeks of hand work. At a scale of 340 it is unsolved, so it gets stated as the kill at scale.
2. **Mapping accuracy.** SUPERSEDED: the 20% placeholder is gone. The rules are now in `EVALUATION_PLAN.md` and encoded in `eval/score.py`. Primary: beat the keyword baseline on 3 holdout keepers. Then a 50% recall floor and overclaim bands (≤10% persevere, ≤25% pivot, >25% kill), plus an inconclusive outcome. Ten keepers are selected by rule (`eval/selection.json`); 283 blind items are in `eval/grading_sheet.csv`.
3. **Every gap is a hard gate.** This is weakened by the data: O&M's only hard gates are the offshore safety certificate (OSSC) and the medical, and both can be fixed with training. Pivot if it holds: group keepers into training cohorts.
4. **Employers won't accept inferred evidence.** Pivot to a keeper-only tool.
5. **The wording backfires.** Kill if a tester reads "Evidenced" as "qualified."
6. **Sample size.** n=40 is a limitation to state, not a kill.

## 5. Data findings (from the 0:00–0:20 read)

- `clean/keepers.json` has 40 keepers, 38 current and 2 left. Ages run from 37 to 73. The age-73 record (K1203) left in 2006, so the oldest current keeper is 65. Logs are templated: 1,270 distinct sentences, about 620 once numbers are masked.
- `clean/logbook_entries.json` has 10,627 entries: era 1 = 3,068, era 2 = 3,787, era 3 = 3,772. Each keeper has between 165 and 408 entries. Every entry has `keeper_code` and a `source_record` pointer into `raw/` (e.g. `raw/logbooks/era1-ocr/naomhog-1985.txt#L37`), which is what makes cited evidence buildable.
- **Contradiction worth naming in the write-up:** `clean/README.md` says the team "did not touch the training records" and "did not resolve anybody's certification status," yet `keepers.json` contains `training_records[]` (outcome: attended/completed) and `certifications[]` (modules held/missing, complete, `valid_2026`). Treat these as data to check, not as truth.
- **"Nearly qualified" shows up in the data. Of 38 current keepers:**
  - HVAP: 23 have a record; 2 are complete or valid in 2026
  - OSSC: 18 have a record; 3 are complete or valid
  - MECS: 20 have a record; 3 are complete or valid
  - WAHS: 16 have a record; 3 are complete; 2 are valid
- Keyword hits in the logs: switch 194 · earth 386 · isolat 110 · 11kV 41 · HV 113 · rope 175 · boat 352 · casualty 129 · first aid 43. These are crude substring counts, so they are an upper bound, not evidence.
- `keepers.json` includes `payroll_ref`, the mapping the top-level README says the Authority doesn't hold. It might link the era-3 2018–21 rows for these 40. It's a note for the write-up, not something to build.
- **O&M posting:** "We would rather train good people"; "no prior wind experience"; essentials are OSSC, comfort with heights, confined spaces and small boats, hands-on maintenance on plant they were responsible for, and offshore medical. Pay is Band 4–6 "depending on assessed capability" — so the inference adds value at offer stage, not just at shortlist.
- **HV AP posting:** insurer-mandated with no discretion; requires HVAP (all 4 modules), OSSC, a medical, and 2 years' switching on 11kV or above. **A lapsed internal Carrowmore HV authorization is accepted in lieu, but only with documentary evidence.** The product can say "your logs suggest you may have held one; here is what the Board needs." It can never say "authorised."
- **Sensitive data:** `raw/appraisals/` and the station manager notes contain illness, bereavement and disciplinary matters. They are excluded by design. Summaries are built from cited facts only.

## 6. Remaining plan (≈3:40 left)

| Block | Time | Output |
|---|---|---|
| Frame the bet | 0:20–0:45 | `FRAMING.md`, in Callie's voice; pause for her edits |
| Ground truth by hand | 0:45–1:15 | Split the O&M requirements into skill / cert / license; Callie hand-grades 8–10 keepers → `ground_truth.json` |
| Build | 1:15–2:30 | AI maps log entries to requirements with citations and tiers; keeper view: Qualified / Nearly / Route |
| Test | 2:30–3:00 | AI grades vs hand grades, an error log, one round of fixes, and one outside reaction if possible |
| Write up | 3:00–3:45 | Kill/pivot/persevere call with numbers, plus the Section 6 answers |
| Buffer | 3:45–4:00 | README run steps, push, record time spent |

**Throughout:** keep appending to `ai-was-wrong.md` with specific moments where the AI was wrong. It's scored. Commit at every milestone. Build no slides.

## 7. Considered, with a line or two each in the write-up

Privacy-by-design ("seek what we need rather than removing what we don't" — Callie's framing). Fairness: the longest-serving keepers have evidence in the noisiest era-1 OCR data, so the tool risks disadvantaging older workers; tenure is a proxy for age. A human decides, and keepers can correct or add evidence. The EU AI Act classes AI used in hiring as high-risk (Annex III); use this as an analogy only. Accessibility: plain language, low bandwidth.

**Deferred on purpose:** requirement weighting, learning-rate prediction, cost of candidacy, raw ingestion, identity matching, a polished employer view, logins.

## 8. Voice and working preferences

- Callie's framing lines to keep: *"Skills are what you know, not how you learned them."* *"Translating them into applicable language is still important."* *"Seek what we need rather than removing what we don't."*
- Copy fixes: "SEO" becomes "requirement-driven search" or "semantic matching"; "open rolls" becomes "open roles."
- Write concise, precise, unpadded prose. Fact-check every claim against the data and cite file and field. Name uncertainty in the wording, not with a disclaimer.
