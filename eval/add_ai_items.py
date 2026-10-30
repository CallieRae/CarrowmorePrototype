"""Second grading pass: sentences the AI cited that the first sheet didn't cover.

To keep the pass blind, these are mixed with an equal number of random sentences
from the same keepers' logs that neither method cited, then sorted alphabetically.
Written to a separate file so the first, already-graded sheet is never touched.

Run: python3 eval/add_ai_items.py  ->  eval/grading_sheet_part2.csv
"""
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import norm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"
SEED = 2030


def main():
    reqs = [r["id"] for r in json.loads((EVAL / "requirements.json").read_text())["requirements"]]
    selected = {k["keeper_code"] for k in json.loads((EVAL / "selection.json").read_text())["keepers"]}
    entries = {e["entry_id"]: e for e in json.loads((CLEAN / "logbook_entries.json").read_text())}
    with open(EVAL / "grading_sheet.csv", encoding="utf-8-sig") as f:
        graded = {norm(r["entry_text"]) for r in csv.DictReader(f)}

    cited = set()
    for m in ("ai", "keyword"):
        p = json.loads((EVAL / "predictions" / f"{m}.json").read_text())["cells"]
        cited |= {i for k in p for c in p[k].values() for i in c["cited"]}

    ai = json.loads((EVAL / "predictions" / "ai.json").read_text())["cells"]
    new = {}
    for k in ai:
        for c in ai[k].values():
            for i in c["cited"]:
                n = norm(entries[i]["text"])
                if n not in graded:
                    new.setdefault(n, entries[i]["text"])

    others = {}
    for e in entries.values():
        n = norm(e["text"])
        if e["keeper_code"] in selected and n not in graded and n not in new and e["entry_id"] not in cited:
            others.setdefault(n, e["text"])
    rng = random.Random(SEED)
    decoys = dict(rng.sample(sorted(others.items()), min(len(new), len(others))))

    rows = {**new, **decoys}
    order = sorted(rows, key=lambda n: rows[n].lower())
    with open(EVAL / "grading_sheet_part2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "entry_text"] + reqs + ["note"])
        for i, n in enumerate(order, 1):
            w.writerow([f"P{i:03d}", rows[n]] + [""] * len(reqs) + [""])
    src = {f"P{i:03d}": ("ai" if n in new else "decoy") for i, n in enumerate(order, 1)}
    (EVAL / "pool_sources_part2.json").write_text(json.dumps(src, indent=1))
    print(len(new), "AI-only sentences +", len(decoys), "decoys =", len(order), "rows")


if __name__ == "__main__":
    main()
