# The call: persevere, with advisor review

**My rules return inconclusive, leaning persevere; my call is to persevere.** The AI beat the comparative keyword search for keepers’ qualifications, was wrong no more than 1 time in 10, and found more than half of the real evidence. Ship with advisor review until retesting with larger samples affirms or refines the logic.

|                                                                           | **AI (Prototype)** | **Keyword search** |
| ------------------------------------------------------------------------- | ------------------ | ------------------ |
| Overclaims (False Positives) of all 10 test keepers                       | 6%, 2 of 32        | 32%, 12 of 38      |
| Recall (% of hand grading matched by tool)                                | 79%                | 68%                |
| Overclaims (False Positives) of 3 held-out keepers, never used for tuning | 10%, 1 of 10       | 50%, 6 of 12       |

## QA:

- **Reviewer 1**: Took *Evidenced* to mean *qualified*, the exact failure the framing named. It is now *Logged experience, needs validation or cert*, with a follow-up on each, pending its own test.

- **Reviewer 2**: Understood how documented experience lined up with each role, but was surprised that *Closest to ready* needed a click to show the ranked list, that “honest” verbiage implied a dishonest route, and that “Insufficient logged experience” read as no experience. The last two are fixed; the ranked list is next.

- **AI and QA**: I set the test rules before any results and graded by hand (ai-was-wrong.md). Claude invented a figure, proposed a baseless kill threshold, applied mixed labeling formats, shipped a scoring bug that would have flipped the call, and inferred authorization from logs. Final QA of 228 screens fixed an overclaiming route line, verdicts resting on one repeated log line (now two dates and two sentences: 7 lines demoted, re-scored at 6.5% overclaims and 76% recall), and 3 certificates with no renewal on file.

- **Accessibility**: plain language, symbols with color, WCAG AA contrast. Time: about 3 hours, 1 each on discovery, build, and testing and write-up.

**If this graduated:** throw away the testing shortcuts (one-time AI labels, one file holding every record, a sign-in for UX with no security). Keep: the logic (translating between natural language and prescribed qualifications), the qualification labels, the rule that logged evidence never clears a licensed requirement, and the test setup. Roadmap would consider addition of estimated certification cost and time for candidates to meet requirements.
