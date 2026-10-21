# The call: persevere on the evidence, pivot on the language

**The mapping held; the wording didn't.** Ship it advisor-reviewed until a second grader, a larger sample and a wording retest confirm it. On accuracy, my rules return *inconclusive, leaning persevere*.

| | AI | Keyword search |
|---|---|---|
| Overclaims (95% CI) | 6%, 2 of 32 (2 to 20%) | 32%, 12 of 38 |
| Recall | 79% | 68% |
| Held-out keepers: overclaims | 10% | 50% |

The AI beat keyword search on the held-out keepers, but 6% sits near the persevere edge. Logs show maintenance, fault-finding and permit work well, and HV switching poorly (voltage is rarely stated; 2 of 6 found), the right failure for an insurer gate. The clean logs are templated; raw text is the real test.

## QA: where the AI and the build were wrong

- Reviewer: the one outside reader took *Evidenced* to mean *qualified*, the exact failure the framing named. It is now *Logged experience, needs validation or cert*, with a follow-up on each, pending its own test.
- AI: it invented a figure, proposed a baseless kill threshold, shipped a scoring bug that would have flipped the call, and wrote "your logs suggest you may once have held an HV authorization" into the interface. I checked every number, set the rules before results, and graded by hand (`ai-was-wrong.md`).
- Full build: 228 screens render cleanly, with no record leaking between keepers. Fixed a route line claiming the Array trains everything, verdicts resting on one repeated line (now two dates and two sentences: 7 lines demoted, re-scored at 6.5% overclaims and 76% recall), and 3 certificates marked current with no renewal on file.

## If this graduated

Throw away the one-pass labels, the single-file build and the mock sign-in; keep the tiers and gate rule, line-level citations, the clarify loop and the pre-registered harness. *Accessible by design: plain language, symbols with color, works offline. Time spent: [to add].*
