# The call: persevere on the evidence, pivot on the language

**The mapping held; the wording didn’t.** Ship it advisor-reviewed until a second grader, a larger sample and a wording retest confirm it. On accuracy, my rules return *leaning persevere*, *inconclusive sample size.*

|                                                        | **AI (Prototype)** | **Keyword search** |
| ------------------------------------------------------ | ------------------ | ------------------ |
| Overclaims of 10 test keepers (False Positives)        | 6%, 2 of 32        | 32%, 12 of 38      |
| Recall (% hand graded correctly found by tool)         | 79%                | 68%                |
| Held-out keepers, never used to tune (False Positives) | 10%, 1 of 10       | 50%, 6 of 12       |

The AI beat keyword search on the held-out keepers, but 6% sits near the persevere edge. Logs show maintenance, fault-finding and permits well and HV switching poorly (voltage is rarely stated), the right failure for an insurer gate. On templated clean logs; raw text is the real test.

## QA:

- Reviewer 1: Took *Evidenced* to mean *qualified*, the exact failure the framing named. It is now *Logged experience, needs validation or cert*, with a follow-up on each, pending its own test.

- Reviewer 2: Understood how documented experience lined up with each role, but was surprised that *Closest to ready* needed a click to show the ranked list, that “honest” implied a dishonest route, and that “Insufficient logged experience” read as no experience. The last two are fixed; the ranked list is next.

- AI and QA: I set the test rules before any results and graded by hand (ai-was-wrong.md). Claude invented a figure, proposed a baseless kill threshold, applied mixed labeling formats, shipped a scoring bug that would have flipped the call, and inferred authorization from logs. Final QA of 228 screens fixed an overclaiming route line, verdicts resting on one repeated log line (now two dates and two sentences: 7 lines demoted, re-scored at 6.5% overclaims and 76% recall), and 3 certificates with no renewal on file.

- Accessibility: plain language, symbols with color, WCAG AA contrast. Time: about 3 hours, 1 each on discovery, build, and testing and write-up.

**If this graduated:** throw away the testing shortcuts (one-time AI labels, one file holding every record, a sign-in with no security). Keep what builds trust: the four labels, the rule that logs never clear a licensed requirement, line-level citations, the keeper clarify questions, and the test setup, re-run whenever labels change.
