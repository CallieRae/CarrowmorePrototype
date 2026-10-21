"""Build the blind hand-grading sheet.

One row per distinct sentence, one column per requirement. The grader marks Y or ?
only where a sentence applies; a blank cell means No. Every sentence is judged
against all five requirements, so the ground truth isn't limited to whichever
requirement surfaced the sentence.

Why sentences: the clean logbooks are heavily templated (10,627 entries, about 620
distinct sentences once numbers are masked). A sentence is graded once and the
grade applies to every entry that uses it.

Pool (pooled evaluation, standard when no full ground truth exists): for each
selected keeper and requirement, every sentence the keyword baseline matches, plus
2 seeded random sentences it doesn't. Sentences the AI cites are appended later,
still blind. Rows are alphabetical, which groups near-duplicates and reveals
nothing about source. Sources are in eval/pool_sources.json; don't open it until
grading is done.

Run: python3 eval/build_grading_sheet.py  ->  eval/grading_sheet.csv
"""
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from common import norm

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"
SEED = 2029


def main():
    reqs = json.loads((EVAL / "requirements.json").read_text())["requirements"]
    keywords = json.loads((EVAL / "keywords.json").read_text())
    selected = {k["keeper_code"] for k in json.loads((EVAL / "selection.json").read_text())["keepers"]}
    entries = [e for e in json.loads((CLEAN / "logbook_entries.json").read_text())
               if e["keeper_code"] in selected]

    texts_by_keeper = defaultdict(dict)
    for e in entries:
        texts_by_keeper[e["keeper_code"]].setdefault(norm(e["text"]), e["text"])

    rng = random.Random(SEED)
    sources = defaultdict(set)
    example = {}
    for k in sorted(selected):
        for r in reqs:
            hits, misses = [], []
            for n, text in sorted(texts_by_keeper[k].items()):
                example[n] = text
                t = text.lower()
                (hits if any(term in t for term in keywords[r["id"]]) else misses).append(n)
            for n in hits:
                sources[n].add(f"keyword:{r['id']}")
            for n in rng.sample(misses, min(2, len(misses))):
                sources[n].add(f"random:{r['id']}")

    rows = sorted(sources, key=lambda n: example[n].lower())
    with open(EVAL / "grading_sheet.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "entry_text"] + [r["id"] for r in reqs] + ["note"])
        for i, n in enumerate(rows, 1):
            w.writerow([f"S{i:03d}", example[n]] + [""] * len(reqs) + [""])
    (EVAL / "pool_sources.json").write_text(json.dumps(
        {f"S{i:03d}": {"norm": n, "sources": sorted(sources[n])} for i, n in enumerate(rows, 1)},
        indent=1))
    print(len(rows), "sentences to grade")


if __name__ == "__main__":
    main()
