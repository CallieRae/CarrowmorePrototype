"""Build the blind hand-grading sheet.

Unit of judgment: one (requirement, entry text) pair. The clean logbooks are heavily
templated (10,627 entries, ~620 distinct sentences once numbers are masked), so a
sentence is graded once and the grade applies to every entry with that sentence.

Pool per selected keeper and requirement (pooled evaluation; a standard approach
when no full ground truth exists):
  - every distinct sentence the keyword baseline matches, plus
  - 2 seeded random sentences it does NOT match, to catch what keywords miss.
Sentences the AI cites later are appended by add_ai_items.py, still blind.

The sheet never says which method surfaced a sentence. Sources are kept in
eval/pool_sources.json. Please don't open that file until grading is done.

Run: python3 eval/build_grading_sheet.py  ->  eval/grading_sheet.csv
"""
import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"
SEED = 2029


def norm(text):
    return re.sub(r"\d+(\.\d+)?", "#", text.lower()).strip()


def keyword_hit(text, terms):
    t = text.lower()
    return any(term in t for term in terms)


def main():
    reqs = json.loads((EVAL / "requirements.json").read_text())["requirements"]
    keywords = json.loads((EVAL / "keywords.json").read_text())
    selection = json.loads((EVAL / "selection.json").read_text())["keepers"]
    selected = {k["keeper_code"] for k in selection}
    entries = [e for e in json.loads((CLEAN / "logbook_entries.json").read_text())
               if e["keeper_code"] in selected]

    texts_by_keeper = defaultdict(dict)  # keeper -> norm -> example text
    for e in entries:
        texts_by_keeper[e["keeper_code"]].setdefault(norm(e["text"]), e["text"])

    rng = random.Random(SEED)
    sources = defaultdict(set)  # (req, norm) -> {"keyword", "random"}
    example = {}
    for k in sorted(selected):
        for r in reqs:
            hits, misses = [], []
            for n, text in sorted(texts_by_keeper[k].items()):
                (hits if keyword_hit(text, keywords[r["id"]]) else misses).append(n)
                example[n] = text
            for n in hits:
                sources[(r["id"], n)].add("keyword")
            for n in rng.sample(misses, min(2, len(misses))):
                sources[(r["id"], n)].add("random")

    items = sorted(sources)
    rng.shuffle(items)  # so the grader can't infer a source from order
    order = {r["id"]: i for i, r in enumerate(reqs)}
    items.sort(key=lambda it: order[it[0]])  # stable: grouped by requirement, shuffled within
    q = {r["id"]: r["question"] for r in reqs}
    with open(EVAL / "grading_sheet.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "requirement", "question", "entry_text", "grade (Y/N/?)", "note"])
        for i, (rid, n) in enumerate(items, 1):
            w.writerow([f"G{i:04d}", rid, q[rid], example[n], "", ""])
    (EVAL / "pool_sources.json").write_text(json.dumps(
        {f"G{i:04d}": {"requirement": rid, "norm": n, "sources": sorted(sources[(rid, n)])}
         for i, (rid, n) in enumerate(items, 1)}, indent=1))
    by_req = defaultdict(int)
    for rid, _ in items:
        by_req[rid] += 1
    print(len(items), "items to grade", dict(by_req))


if __name__ == "__main__":
    main()
