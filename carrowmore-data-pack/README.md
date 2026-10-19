# Carrowmore Lighthouse Authority — keeper records extract

Prepared by the Authority's data team, March 2026, for the redeployment working group.

---

## Why you have this

The Authority is automating its last 68 manned stations. 340 keepers are
affected. Between them they have something like 8,057 years of service, and we
cannot tell you what any of them can do.

That is not a figure of speech. There is no competence record anywhere in this
organisation. There never has been. What we have instead is forty-two years of station
logs written for a completely different purpose, a personnel system that records grades
and postings and nothing else, three training systems that were never reconciled, and a
cupboard of appraisal forms.

This extract is everything we hold. We have not tidied it up, because tidying it up is
most of the problem and we would rather you saw it as it is.

We should say plainly: we have tried this ourselves twice, in 2019 and in 2024, and both
attempts stalled. Neither of us thinks this is easy.

---

## What is in the pack

```
raw/
  logbooks/
    era1-ocr/            1292 files, ~53,971 dated entries   1985-2003
    era2-keeperlog/      12 files, ~31,676 rows               2003-2014
    era3-spreadsheets/   3 files, ~165,844 rows                2014-2026
  personnel/             2 files, 340 current + 260 former keepers
  training/              4 files
  appraisals/            1 file (~4,422 records) + 120 loose notes
reference/               the occupational standards framework, 2 files
employers/               6 job postings + 1 certification reference
clean/                   40 keepers, tidied. See clean/README.md.
```

Approximately 53 MB uncompressed.

Most of that volume is routine watchkeeping — weather, visibility, barometer, watch
handover. Roughly a quarter of the logbook rows describe an actual job of work. We have
not separated them for you because the boundary is a judgement and it is your judgement
we are interested in.

---

## The logbooks, and what is wrong with them

The station journals are the only record of what people actually did. They exist in three
incompatible generations because the Authority changed systems twice and migrated nothing.

### `raw/logbooks/era1-ocr/` — 1985 to 2003

One plain text file per station per year, named `<station>-<year>.txt`.

These are scans of handwritten journals, put through optical character recognition in 2016
by a contractor. **The recognition is poor.** Roughly a third of entries contain character
errors. Words run together, words split in the middle, letters swap for digits, and lines
occasionally break where the page edge was. You will see `[illegible]` where even the
contractor gave up.

Three or four station-years are effectively unreadable. The originals for those were water
damaged before scanning and we no longer hold them.

Date formats vary within a single file because they varied within a single volume: you
will find `12/3/87`, `12.03.87` and `12 Mar 87`, sometimes on the same page. About one date
in fifty is ambiguous or outright impossible — `31/02/91` is in there more than once. We
have not corrected any of them, because we do not know what the keeper meant and neither
do you.

Keepers are identified by name, and the names are written differently by different people
and then damaged by the OCR on top of that. There is no keeper code in era 1 at all.

### `raw/logbooks/era2-keeperlog/` — 2003 to 2014

KEEPERLOG was an in-house desktop application. It was retired in 2014 and the machine it
ran on was disposed of in 2017. What we have is the final export, one `.DAT` file per year.

- Pipe-delimited, with a nine-line proprietary header block before the data starts.
- **The files are CP1252 encoded, not UTF-8.** If you read them as UTF-8 they will throw on
  the first accented surname. We are sorry. We cannot re-export them.
- The `ACTIVITY` field is truncated at 120 characters with no ellipsis, so a lot of entries
  just stop mid-word. The rest of the text is gone; it was never in the export.
- The `KPR` column holds the five-character keeper code. **This is the only reliable
  identity key anywhere in this pack.**

### `raw/logbooks/era3-spreadsheets/` — 2014 to 2026

Three CSV files, because the columns changed twice and nobody backfilled.

| File | What changed |
|---|---|
| `station-logs-2014-2017.csv` | `Date, Station, Keeper Name, Activity, Notes` |
| `station-logs-2018-2021.csv` | dropped names for `keeper_id`, added `activity_type` and `hours` |
| `station-logs-2022-2026.csv` | added `verified_by` and `skill_tags`, dropped `hours` |

Two things you should know:

- **`keeper_id` in the 2018 files is not the keeper code.** It is the payroll reference. We
  do not hold a mapping between the two. It exists somewhere in the payroll bureau's
  systems and we have not been able to get it.
- **`skill_tags` is populated on about 18% of rows** and was filled in by three different
  people who each had a different idea of what a skill tag was. One used framework
  references, one used ordinary words, one used course codes. We have not harmonised them
  and we would not know how.

These files have been opened in Excel by many hands over ten years, and it shows. Dates
appear as serial numbers, as ISO strings and in two different slash formats. Some
identifiers have lost their leading zeros and a few have been converted to scientific
notation. A handful of text fields have acquired a leading apostrophe. At least one column
header has a trailing space in it.

---

## `raw/personnel/`

`cla_personnel_export.csv` — the 340 keepers currently employed.
`cla_personnel_leavers.csv` — 260 former keepers, 1985 to 2026, who appear in the
logbooks but are not employed by us.

Name, keeper code, grade, grade history, postings with dates, contract type, date of birth,
date joined, date left.

**There is no competence information of any kind in these files.** This is the source that
looks most authoritative and tells you least. Grade in particular tells you nothing: it
follows length of service and the availability of a vacancy, and it has never been tied to
an assessment of anything.

The postings table has known problems. A few keepers have postings that overlap. Three have
a two-year gap with no station recorded — they were somewhere, we do not know where. Two
have grade histories that are out of chronological order.

---

## `raw/training/`

Three systems that never spoke to each other.

**`vendor-a-mareng-1994-2005.csv`** — course codes only. The course catalogue that
explained what the codes meant was the vendor's property and went with them when the
contract ended. There is one `status` column containing `A`, `C`, `X` and blanks.
**Attendance and completion were not distinguished in this system before 2011**, and we
have not found anything that documents what the letters mean.

**`vendor-b-skillsflow-2005-2017.json`** — has course descriptions. They are marketing
copy. We considered removing them and decided you should see what we are dealing with.
SkillsFlow held learners by name only; there is no keeper code in this file.

**`vendor-c-learnhub-2017-2026.json`** — the current system, and the only one that is any
good. Proper completion records, expiry dates, a sensible schema. It holds five years of
history and nothing before that was migrated. Its course codes are a different namespace
with no mapping to vendor A.

**`course_code_partial_glossary.csv`** — somebody in the District Office started mapping
the vendor A codes in 2013 and then left. It covers about 40% of them.

### The 1997 migration

When the Authority moved from paper training registers to the vendor A system in 1997, the
transfer was done by a contractor over one summer. **Records for roughly a quarter of the
workforce were lost.** This was known at the time, an internal report was written, and
nothing was done about it because the affected keepers were mostly mid-career and it was
assumed they would re-certify eventually. Many did not.

Anything before 1994 was never digitised at all.

---

## `raw/appraisals/`

`appraisals.jsonl` — one JSON object per line, roughly 4,422 of them, annual
free text from 1994 onward. Coverage is uneven and the quality varies enormously. Some are
two words. Some are three pages. One district superintendent wrote the same paragraph for
every keeper for six years.

Records before 2004 have no keeper code, because the field did not exist and was never
backfilled. They have a name.

`station_manager_notes/` — 120 loose text files, uneven coverage, no naming
convention worth the name. Some are scans and have been through the same OCR as the era-1
logs.

**A warning about these files.** They are personnel records and they contain things about
people's lives — illness, bereavement, a domestic situation, an old disciplinary matter
that was resolved thirty years ago. We debated redacting them and decided not to, because
in a real deployment you would have to handle them and we would rather see how you do. They
are yours to handle carefully.

---

## `reference/`

`nosf_taxonomy.json` — the Northern Occupational Standards Framework, eleventh edition.
About 2,514 skill statements in 170 occupations across
14 sectors, levelled 1 to 8.

It is written in policy language, because it is a policy document. It says things like
"apply established procedures for the isolation and earthing of electrical apparatus in
accordance with relevant safety requirements". The corresponding logbook entry says
"isolated no.2 and earthed off". Those are the same event.

Coverage is uneven between sectors. Maritime and energy were revised recently and are
detailed. Several others are thin.

`nosf_occupations.csv` — the flat occupation list, for convenience.

---

## `employers/`

Six live job postings from four employers, as published. They are written in four different
house styles and none of them uses the framework's vocabulary. The Carrowmore Array O&M
posting is the big one, around forty hires.

`certification_schemes.json` — the certification schemes those postings refer to, their
modules, their prerequisites and their renewal periods. Compiled by us from the issuing
bodies' published material, so treat it as good but not authoritative.

Note that the Authority's own internal authorisations are not certification schemes and do
not appear in this file, although at least one scheme will recognise one.

---

## `clean/`

Forty keepers, tidied up properly by hand. **You may use this instead of the raw pack with
no penalty at all**, provided you say so in your write-up. It exists because three weeks of
work on 40 people out of 340 is not a solution, and we would rather you spent your
two days on the interesting part than on character encodings.

See `clean/README.md` for exactly what was done to it and what was removed.

---

## Things we know and have not fixed

- About 3% of logbook entries name somebody we cannot resolve to any personnel record.
  Contractors, relief hands from other districts, and mis-transcriptions. We have left them.
- The changeover years, 2003 and 2014, are split across two systems. Half a station's year
  may be in the old system and half in the new one, and the split is not the same for every
  station.
- Nothing in this pack has been de-duplicated, reconciled or validated against anything
  else in this pack.
- We have not checked whether the data supports the conclusions anybody wants to draw from
  it. That is rather the point.

---

*Questions to the redeployment working group. Please do not contact station staff directly.*
