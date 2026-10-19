# Framing: Carrowmore keeper redeployment

**The bet:** a keeper's own station logs, read honestly, can tell them what they are qualified for, what they are nearly qualified for, and the shortest honest route to a job. The belief that would sink it is that the reading can be made accurate *and* worded so a keeper acts on it correctly. That is what the prototype tests, against the Carrowmore Array O&M Technician posting (about 40 hires).

## The problem, and whose it is

340 keepers lose their stations to automation, and the Authority says plainly that it "cannot tell you what any of them can do." There is no competence record anywhere. What exists is forty-two years of logs written for another purpose, three training systems that never reconciled, and a 1997 migration that lost training records for roughly a quarter of the workforce.

The problem belongs to the keeper first. The Authority, the employers and the redeployment group all need an answer too, but the keeper is the one who has to act on it, and the one most exposed if it is wrong. An employer shortlist is a secondary view at most.

The gap is one of translation more than evidence. The logs say "isolated no.2 and earthed off"; the framework says "apply established procedures for the isolation and earthing of electrical apparatus"; the posting says neither. Skills are what you know, not how you learned them, but translating them into applicable language is still important.

The data says "nearly qualified" is the common case. Of 38 current keepers in `clean/keepers.json`, 23 hold some HVAP record and 2 are complete and valid for 2026. For OSSC, the certificate the O&M posting cannot mobilize anyone without, 18 hold a record and 3 are valid. Such a pool is not a shortlist problem. It is a route problem.

## Beliefs we cannot yet prove

1. Log entries can be mapped to employer requirements accurately enough to act on. *Tested here.*
2. The wording can carry the uncertainty: a keeper reads "Evidenced" as "your logs show this," never as "qualified." *Tested here, with one outside reader if possible.*
3. Employers will accept inferred evidence at offer stage. The O&M posting pays Band 4 to 6 "depending on assessed capability," which is where this would earn its keep. *Not testable in four hours.*
4. Keepers can close the gaps quickly enough for the hiring waves. *Not testable in four hours.*
5. Attribution holds at scale. `clean/` resolved identity for 40 keepers by three weeks of hand work; the other 300 are unsolved. *Stated, not tested.*

## The one that would sink it

**Belief 1, with belief 2 inseparable from it.** If the mapping is wrong, everything downstream is confidently wrong. If the mapping is right but a keeper reads "Evidenced" as "qualified," the product does harm with true information. Either one alone kills it.

## How we keep it honest

No composite match score. "78% match" is the false precision this brief is fishing for. Each requirement instead gets one of four evidence tiers:

| Tier | Source | What the keeper sees |
|---|---|---|
| Authorised | `certifications[]`, complete and `valid_2026` | The certificate, with its expiry year |
| Partially certified | `certifications[]`, some modules held | Modules held, modules missing |
| Evidenced | Logbook entries | Count, date range and cited entries, e.g. "HV switching recorded 11× across 2019 to 2023" |
| Not yet shown | Nothing found | The route to close it. Never "unqualified." |

Log evidence never upgrades a license or insurer gate to "met." Recency counts, so a 1998 entry weighs less than a 2024 one. Every Evidenced claim cites its `source_record`, so a keeper can check us and correct us.

The HV Authorised Person posting is the sharpest case. The Competence Board accepts a lapsed internal HV authorization in place of the two-year switching requirement, but only with documentary evidence. The product may say "your logs suggest you may have held one; here is what the Board needs." It may never say "authorized."

## What we chose not to build, and why

Data comes from `clean/` only. The question lives in the inference and the interface, not in ingestion, and raw identity resolution would consume the whole four hours (which is precisely why it is the kill at scale). Also deferred on purpose: requirement weighting, learning-rate prediction, a polished employer view, and logins. `raw/appraisals/` and the station manager notes are excluded by design, since they hold illness, bereavement and disciplinary matters. We seek what we need rather than removing what we don't.

## Kill thresholds, set before building

- Kill if the AI's "Evidenced" disagrees with the hand grade in more than 20% of requirement calls. *Threshold to confirm.*
- Kill if a tester reads "Evidenced" as "qualified."
- Pivot to training cohorts if most gaps prove to be hard gates. The O&M posting already weakens this: its hard gates are OSSC and offshore medical, and both are trainable.
- Pivot to a keeper-only tool if employers will not accept inferred evidence.
- n = 40, not randomly sampled, is a limitation to state rather than a kill.

One fairness risk shapes all of this. The longest-serving keepers have their evidence in the noisiest era-1 OCR, and tenure is a proxy for age, so a naive reading would disadvantage exactly the people with the most to offer. A human decides; the keeper can always add what the logs missed.
