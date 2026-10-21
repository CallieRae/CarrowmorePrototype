# Mapping prompt (AI under test)

Used to label every distinct logbook sentence in `clean/` against the five requirements in `eval/requirements.json`. The labels in `eval/ai_labels.json` were produced by Claude (Opus 5.5) in a Cowork session following this prompt, without sight of the hand grades. `prototype/ai_map.py` reproduces the run through the API when a key is available.

---

You are reading lighthouse keepers' logbook sentences. For each sentence, decide which of these employer requirements it is evidence for:

- **R1_MAINT** Hands-on mechanical or electrical maintenance of plant (engines, generators, pumps, motors, compressors, electrical gear).
- **R2_FAULT** Diagnosing an electrical fault, working out what was wrong. Replacing a part on its own is not enough.
- **R3_PERMIT** Working to, or issuing, a permit-to-work or formal safety document.
- **R4_HVSW** Personally carrying out high-voltage switching, isolation or earthing.
- **R5_HEIGHT** Working at height, or inside a confined or enclosed space.

For each requirement, answer:

- `Y` The sentence, read on its own, shows the writer personally doing this.
- `?` It might, but the sentence alone doesn't settle it (voltage not stated, unclear who did it, preparing for the work rather than doing it).
- omit: no.

Rules:

1. The writer must be the one doing it. "Stood by while…", "detailed 2nd to…", "witnessed" are not evidence of doing.
2. Judge the activity, not the readings. Ignore odd numbers or units.
3. Don't infer beyond the sentence. If a skill is plausible but not shown, it's `?` at most.
4. Never treat any sentence as proof of authorization or certification. You are labeling evidence of activity only.

Return one line per sentence: `<id>|<requirement>=<Y or ?>,...` or `<id>|` if none apply.
