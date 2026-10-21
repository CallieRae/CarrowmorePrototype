# Framing the bet

A keeper's working life is already written down, just not in any language an employer reads. The bet: forty years of logbooks can be translated into an employer's terms, graded honestly, so a keeper sees what he is qualified for, what he is nearly qualified for, and the shortest route between the two.

## Whose problem

At least four users want different things here: the keepers, the Authority's redeployment team, and employers who are themselves several. I'm building for the keeper and his question: *"What am I qualified for, what am I nearly qualified for, and what is the shortest honest route from here to a job?"* The redeployment team's shortlist runs on the same evidence, sorted differently, and can wait until the keeper's answer deserves trust. A shortlist built on a wrong answer is only wrong faster.

## What I believe but cannot yet prove

1. Skills are what you know, not how you learned them. "Isolated no.2 and earthed off" is the same competence a certification module assesses, in different words.
2. Translation is the value, even where the keeper already knows the skill. He knows he can keep a diesel plant running with no one to call; he may not know the Array's O&M posting would be "delighted by" exactly that.
3. Most keepers are nearly qualified, not unqualified. Of 38 current keepers in the clean subset, 23 hold some record against the HV Authorized Person scheme and 2 hold the full certificate.
4. Employers will weigh inferred evidence alongside certificates, and a keeper's history says something about how fast he can close a gap. Neither is testable this week.

## The one that sinks it

**AI can map logbook entries to employer requirements accurately enough, and word the result plainly enough, that a keeper acts on it correctly.** If the mapping is wrong, or right but read as a promise, the tool sends a fifty-four-year-old to an interview he was never going to pass.

## How I'll test it

Two postings: the Array's O&M Technician (about forty hires) and its HV Authorized Person (insurer-mandated, no discretion) as the sharp case. I hand-grade ten keepers first, chosen by rule and three of them held out from any tuning, then build a tool that grades the same keepers with every claim cited to its log entry.

No match score; a single percentage is precisely the false certainty at issue. Each requirement carries a tier instead: *Authorized*, *Nearly Qualified (Partial Cert)*, *Evidenced*, or *Not yet shown*, each with its route forward. Log evidence never upgrades a license or insurer gate to met.

The kill rules were committed before the AI ran (`EVALUATION_PLAN.md`). The primary one: if the AI can't give a cleaner evidence list than plain keyword search on keepers held out from tuning, the AI isn't earning its place. Behind that sits a recall floor of 50% and overclaim bands (10% or below persevere, up to 25% pivot to advisor review, above that kill), plus an honest "inconclusive" for when fifty cells can't decide.

## What I used, and left out

`clean/` rather than `raw/`: the question lives in the inference and the wording, not in OCR repair. That choice hides the real kill at scale, which is attribution. It took the Authority three weeks to tie entries to forty keepers; there are 340. Appraisals and manager notes are out by design. Rather than removing what we don't need, the tool seeks only what we do.
