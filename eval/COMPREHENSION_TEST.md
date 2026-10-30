# Label comprehension test (draft, for approval)

**Status: draft.** Thresholds and sample below are proposals. They take effect only once Callie approves them, dated here, before the first session. After results arrive they do not change; any later change is logged as an addendum.

Approved: `[date, by Callie]`

## What this tests

**The claim:** people read each status label and count as what the data supports: evidence of work, a certificate on file, or a gap in the records. They do not read it as a verdict on the person, or as clearance for a job.

This is the riskiest assumption from `FRAMING.md`, narrowed to the wording added after `b6cc45b`. It has failed once already: Reviewer 1 read *Evidenced* as *qualified*. The renamed label has not been tested since.

## Labels under test

| # | Label | Where | Correct reading | Misread (decided now, not after) |
|---|---|---|---|---|
| L1 | Logged experience, needs validation or cert | Keeper and employer, experience lines | The logs show this work; nobody has confirmed it yet | Qualified, certified, approved, "can do the job" |
| L2 | Logged experience, needs authorization | HV switching line | The logs show switching; an authorization is still required | Authorized, cleared, can be appointed |
| L3 | Nearly Qualified (Partial Cert) | Certificate lines | Some modules held, or a certificate that lapsed | Qualified; "almost certainly gets the job" |
| L4 | Insufficient Documented Qualifications | Experience, certificate and medical lines | The records don't show it | The person can't do it, has no experience, or failed |
| L5 | "3 of 6 Requirements on record" | Employer count button | 3 of the 6 requirements have a certificate or logged work behind them | A score, a percentage match, a ranking or "50% qualified" |
| L6 | "2 of 2 Experience shown in logs" (HV role) | Employer count button | The logs show both kinds of work, including switching that still needs authorization | Experience requirements met; switching cleared |
| L7 | "? Medical not on record" | Employer count button | No medical in the records; it needs checking | Failed the medical; unfit |
| L8 | Shortest route | Keeper, Role Description | The training or paperwork still to do | A guarantee of a job when done |

## Measures

1. **Comprehension:** each label's reading is coded as *correct*, *partial* (right idea, wrong detail) or *misread*, using the misread column above.
2. **Critical misreads:** any reading of L2, L5 or L6 as clearance of the HV requirement. These are the misreads that send an unqualified candidate to interview.
3. **Hesitation:** where people pause, scroll to the footer, or ask what something means. These are logged, not scored.

**Comparison point:** the one earlier reading, Reviewer 1's misread of *Evidenced*. If L1 still draws that misread, the rename didn't work.

## Decision rules (proposed)

| Result | Call for that label |
|---|---|
| 4 or 5 of 5 testers correct, no critical misread | Keep the label |
| 2 or more of 5 misread it | Relabel, then retest that label with new testers |
| Any critical misread, by any tester | Fix before the next deploy, whatever the other results |
| Fewer than 5 testers in a group | Inconclusive: report the readings, make no call |

In plain terms: one confused tester is a note; two is a pattern; one tester who thinks HV switching is cleared is a stop.

## Sample (proposed)

- **Keeper group:** 5 adults with hands-on trade or maintenance work, none in recruiting. They stand in for keepers.
- **Employer group:** 5 people who shortlist or hire.
- **Excluded:** Reviewers 1 and 2, and anyone who has seen the label definitions.
- Testers: `[unknown: who Callie can reach, and by when]`

## Scenarios

| # | Group | Sign in as | Role | Why this case |
|---|---|---|---|---|
| S1 | Keeper | `K0566` | Wind Turbine Technician (O&M) | Shows L1, L3, L4 and L8 together |
| S2 | Keeper | `K1374` | High Voltage Authorized Person | Shows L2 next to two held certificates: the most tempting misread |
| S3 | Employer | any email | High Voltage Authorized Person, candidate `K1374` | Shows L5 and L6 with HV switching logged (3 of 6, 2 of 2) |
| S4 | Employer | any email | Wind Turbine Technician (O&M), sort by Logged experience | Shows L5 to L7 in a ranked context |

## Script

**Before the session.** Open the live prototype in a fresh browser window. Sign in for the tester, so they never see the sign-in note. Keep the footer out of view: the label definitions are there, and they must not be read until the questions are done.

**Opening (read aloud):**
> "This is a prototype for people whose jobs are changing. I'm testing the page, not you, and there are no wrong answers. Please think aloud as you look. I'll ask what a few things mean to you. Say what you'd guess, even if you're not sure."

**Keeper tasks (S1, then S2):**
1. "This is your record for this job. Take a minute to look over it." *Watch where their eyes go first, and whether they scroll to the bottom.*
2. Point to each label in turn (L1, L3, L4, L8): "What does this tell you?"
3. Then: "Based on this page, could you apply for this job tomorrow?" *A yes on S2 is a critical misread of L2.*
4. "What would you do next?"

**Employer tasks (S3, then S4):**
1. "You're shortlisting for this role. Here is one candidate." *Watch whether they read the buttons before the details.*
2. Point to each count button (L5, L6, L7): "What does this tell you about the candidate?"
3. "Would you put this candidate forward for the HV Authorized Person interview today?" *A yes without mentioning authorization is a critical misread.*
4. On S4: "Why is this person at the top of the list?"

**Closing:** "Was anything on the page unclear, or did anything surprise you?" Only now, show the footer definitions, and ask whether any of them changes their earlier answers.

**Do not:** explain any label before the questions, say "evidence", "validation" or "authorization" before the tester does, or confirm whether an answer is right.

## Observation sheet (one per tester)

| Label | What they said (their words) | Code (correct / partial / misread) | Hesitated? |
|---|---|---|---|
| L1 | | | |
| L2 | | | |
| L3 | | | |
| L4 | | | |
| L5 | | | |
| L6 | | | |
| L7 | | | |
| L8 | | | |
| Q3 (apply or put forward?) | | | |

Code every reading against the misread column, which was written before any session.

## Known weaknesses

- Five per group finds big misreadings, not small ones. A clean result is not proof that the wording is safe.
- Testers aren't keepers or the Array's recruiters. Keepers may read "Insufficient" more personally after a career at the Authority.
- Pointing at a label draws attention a real reader might not give it. Task 1's unprompted look is the closer test of real use.
- The moderator codes the readings. Where possible, a second person codes them from notes without seeing the first coding.
- The footer definitions are on the same page. A tester who scrolls early is primed; note it and keep their answers separate.
