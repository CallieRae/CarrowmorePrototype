# Where the AI was wrong (running log)

Working notes for Section 6, question 2. Logged as it happens, not reconstructed after.

| # | When | What the AI did | Why it was wrong | What I did |
|---|---|---|---|---|
| 1 | Planning | Proposed the O&M posting's gaps would be mostly hard certificate gates ("everyone needs wind safety training") | Assumed, not read. The posting's only essential certificate is offshore safety, plus a medical; it says "we would rather train good people" and "no prior wind experience" | Read the postings myself before scoping. The kill moved from "every gap is a gate" to "can capability be evidenced at all" |
| 2 | Framing draft | Wrote "eleven entries reading 'isolated no.2 and earthed off'" | Fabricated count. The data README quotes that sentence once, as an example; "eleven" was borrowed from the brief's hypothetical | Checked every figure in the draft against the data; changed to "a log entry" |
| 3 | Framing draft | Called offshore safety "the Array's one hard gate" | Dropped the medical, also essential | Reworded to "the only certificate the posting makes essential" |
| 4 | Kill threshold | Gave "more than ~20% disagreement" as the kill | A placeholder presented as a criterion. Blended two errors with very different costs (overclaims vs misses), had no baseline, ignored sample size | Asked how it was derived. Rebuilt the rules: overclaims only, keyword baseline as the primary test, holdout keepers, per-requirement and per-era reporting, an "inconclusive" outcome. Committed before results (`EVALUATION_PLAN.md`) |
| 5 | Scoring code | First comparison rule judged "beats the baseline" on cell-level overclaim and recall only | A cite-everything keyword search keeps overclaim low by burying two good entries in a pile of fifteen (median 15 citations per cell). The rule rewarded the behavior we're trying to prevent | Caught on a dry run with dummy grades. Added citation precision as a required condition, since the citation list is what a keeper reads |
| 6 | Data read | Took `clean/README.md` at its word ("did not resolve certification status") | `keepers.json` carries `certifications[]` with modules held and missing, `complete`, `valid_2026`. Source contradicts itself | Treated as data to check, not truth; to note in the write-up |
