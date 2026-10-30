"""Select the keepers to hand-grade, by a rule fixed before any AI output exists.

Rule (pre-registered in EVALUATION_PLAN.md):
  - Current keepers only.
  - Split into tenure terciles by date joined; draw 3 / 4 / 3 (long / mid / short).
  - Constraints on the 10: at least 3 with heavy era-1 evidence (>= 100 era-1 entries),
    at least 3 rock-primary and 3 shore-primary, at least 1 island-primary.
  - Seeded random draw (seed 2029), redrawn until the constraints hold.
  - Holdout: one keeper per tercile, seeded. Holdout keepers are graded but never used
    to fix prompts or rules.

Run: python3 eval/select_keepers.py  ->  writes eval/selection.json
"""
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "carrowmore-data-pack" / "clean"
SEED = 2029

keepers = json.loads((CLEAN / "keepers.json").read_text())
entries = json.loads((CLEAN / "logbook_entries.json").read_text())

by_keeper = defaultdict(list)
for e in entries:
    by_keeper[e["keeper_code"]].append(e)


def primary_class(k):
    years = Counter()
    for p in k["postings"]:
        span = (p["to_year"] or 2026) - p["from_year"] + 1
        years[p["station_class"]] += max(span, 1)
    return years.most_common(1)[0][0]


pool = []
for k in keepers:
    if k["status"] != "current":
        continue
    eras = Counter(e["source_era"] for e in by_keeper[k["keeper_code"]])
    pool.append({
        "keeper_code": k["keeper_code"],
        "joined": int(k["date_joined"][:4]),
        "class": primary_class(k),
        "era1_entries": eras.get(1, 0),
        "entries": len(by_keeper[k["keeper_code"]]),
    })

pool.sort(key=lambda r: r["joined"])
n = len(pool)
terciles = {
    "long": pool[: n // 3],
    "mid": pool[n // 3 : 2 * n // 3],
    "short": pool[2 * n // 3 :],
}
take = {"long": 3, "mid": 4, "short": 3}


def ok(sample):
    c = Counter(r["class"] for r in sample)
    heavy = sum(r["era1_entries"] >= 100 for r in sample)
    return heavy >= 3 and c["rock"] >= 3 and c["shore"] >= 3 and c["island"] >= 1


rng = random.Random(SEED)
for attempt in range(1, 10001):
    picked = {t: rng.sample(terciles[t], take[t]) for t in terciles}
    sample = [r | {"tercile": t} for t, rs in picked.items() for r in rs]
    if ok(sample):
        break
else:
    raise SystemExit("No sample met the constraints")

holdout = [rng.choice(picked[t])["keeper_code"] for t in ("long", "mid", "short")]
for r in sample:
    r["split"] = "holdout" if r["keeper_code"] in holdout else "dev"

out = {
    "seed": SEED,
    "attempts": attempt,
    "tercile_join_years": {t: [rs[0]["joined"], rs[-1]["joined"]] for t, rs in terciles.items()},
    "keepers": sorted(sample, key=lambda r: (r["split"], r["joined"])),
}
(ROOT / "eval" / "selection.json").write_text(json.dumps(out, indent=1))
for r in out["keepers"]:
    print(r)
print("attempts:", attempt)
