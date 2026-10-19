# clean/

This is a cleaned-up slice of the same data, produced by the Authority's own data team
over about three weeks. You may use it instead of `raw/` with no penalty. If you do, say
so in your write-up and say what you would have done differently with the raw pack.

## What is in it

- `keepers.json` — 40 keepers, one record each
- `logbook_entries.json` — 10,627 logbook entries belonging to those keepers

## What we did to it

- **Identities resolved.** Every logbook entry has been attributed to a keeper code by
  hand. Where we could not be certain, we dropped the entry rather than guess. About 4% of
  entries for these keepers were dropped this way.
- **Dates normalised** to ISO 8601. Entries whose date was ambiguous or impossible have
  been dropped, not repaired.
- **Text repaired.** Where the era-1 scans were legible enough for a human to transcribe,
  we transcribed them. The text in this file is what we believe was originally written.
- **Entries structured.** Each entry now has a station code, a station class, a keeper
  code, a source era and a date.
- **Encoding.** Everything is UTF-8.

## What we took out, and you should know we took it out

- **Routine watch and weather lines.** The raw logs are mostly "wind SW 5, nothing to
  report". We removed those. They are about 70% of the raw volume and they carry nothing.
  If your approach depends on knowing how much of a log is noise, this file will mislead
  you.
- **Entries we could not attribute.** See above.
- **Everything except these 40 keepers.** These were chosen to be a reasonable
  spread of stations, grades and lengths of service. They are not a random sample and we
  do not claim they are representative of anything.

## What we did NOT do

- We did not add any judgement about what anybody is good at. There is no competence,
  skill or rating field anywhere in this directory, and we would not know how to produce
  one. That is the whole problem.
- We did not touch the training records, the appraisals or the personnel files. If you
  want those, they are in `raw/`, in the state they are in.
- We did not resolve anybody's certification status.

## Caveat

Three weeks of work on 40 people out of 340. That rate does not scale and is the reason
this project exists.
