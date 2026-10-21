# Grading guide

**Job:** read each sentence on its own and mark the columns it supports. About 20 to 25 minutes for 188 rows.

| Mark | Meaning |
|---|---|
| `Y` | The sentence shows the keeper **personally doing** this |
| `?` | It might, but you'd need more context to say (counts as No in scoring) |
| blank | No. Most cells stay blank |

**Ground rules**

- Judge the activity, not the readings. The data has deliberate noise (a pump "delivery back up to 418 V"); ignore odd numbers and units.
- One sentence can be `Y` in several columns, and the same sentence can be `Y` in one and blank in another.
- Someone else did it? Blank. "Stood by while...", "Detailed 2nd to...", "SAK witnessing" (when the keeper is the witness).
- Planning, checking or admin only? Blank, unless the column is about exactly that (permits).
- Unsure after five seconds? `?` and move on. Speed beats agonizing; `?` is an honest answer.

## Columns, with examples from the data

**R1_MAINT** Hands-on maintenance of plant: engines, generators, pumps, motors, compressors, electrical gear.

- `Y` Rebuilt the No.1 pump end to end, new wear rings...
- `Y` Compressor not making pressure, rings worn. Rebuilt the no.1 cylinder.
- `?` Primed the no.3 pump, running sweet. *(operating or maintaining?)*
- blank: Repaired the storm damage to the landing wall... *(structure, not plant)*
- blank: Ran the sump pump out, 4 hrs. *(operating it)*

**R2_FAULT** Diagnosing an electrical fault, working out what was wrong. Replacing a part on its own is not enough.

- `Y` Traced and lifted an earth fault on the tower lighting ring, split the ring to find it.
- `Y` Megger test on the No.1 feeder... condemned the cable and ran a temporary.
- `?` Intermittent fault on the gallery lights, watching it.
- blank: Reset the overspeed after a false trip. *(a reset, no diagnosis)*
- blank: Stripped and cleaned the mercury bath... *(mechanical, not electrical)*

**R3_PERMIT** Working to, or issuing, a permit-to-work or formal safety document.

- `Y` Racked out No.2 breaker, locked off, caps on, danger notices up. PTW 114 refers.
- `Y` Signed on to PTW 331 for the day's work.
- `Y` Held the keys for the HV work, permit 1102 refers. *(a permit-system role, even though someone else switched)*
- blank: Set up the haul for a heavy lift in a poor sea...

**R4_HVSW** Personally carrying out high-voltage switching, isolation or earthing.

- `Y` Took the 11kV board off, worked the sequence myself, relief witnessing.
- `Y` Isolated no.1 transformer, earths applied both ends, PTW 114 issued to the contractor.
- `?` Racked out No.2 breaker, locked off... *(voltage not stated)*
- blank: Stood by while relief switched the NO.2 transformer out.
- blank: Held the keys for the HV work, permit 1102 refers. *(Y for R3, blank here)*

**R5_HEIGHT** Working at height, or inside a confined or enclosed space.

- `Y` Abseil inspection of the north face.
- `Y` Tank entry, 2 hrs inside.
- `Y` Cleaned the lantern glass from the staging.
- `?` Gas tested the fuel tank before entry. *(prepared the entry; did they go in?)*
- blank: Acted as top man for the tank entry... *(the top man stays outside)*
- blank: Detailed 2nd to the gallery work.

The examples above are my suggested calls. If you disagree with one, your call wins; just apply it consistently.

When you're done, save as CSV with the same name, and tell me the last row you reached if you stop part way.
