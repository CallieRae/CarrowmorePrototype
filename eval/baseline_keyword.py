"""Keyword baseline: the naive approach the AI has to beat.

For each selected keeper and requirement, cite every entry whose text contains a
pre-registered keyword (eval/keywords.json). Evidenced if 2 or more entries match.
Not tuned after the AI was run.

Run: python3 eval/baseline_keyword.py  ->  eval/predictions/keyword.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"


def main():
    keywords = json.loads((EVAL / "keywords.json").read_text())
    reqs = [r["id"] for r in json.loads((EVAL / "requirements.json").read_text())["requirements"]]
    selected = [k["keeper_code"] for k in json.loads((EVAL / "selection.json").read_text())["keepers"]]
    entries = json.loads((CLEAN / "logbook_entries.json").read_text())

    cells = {k: {} for k in selected}
    for k in selected:
        mine = [e for e in entries if e["keeper_code"] == k]
        for r in reqs:
            cited = [e["entry_id"] for e in mine
                     if any(t in e["text"].lower() for t in keywords[r])]
            cells[k][r] = {"verdict": "Evidenced" if len(cited) >= 2 else "Not yet shown",
                           "cited": cited}
    (EVAL / "predictions").mkdir(exist_ok=True)
    (EVAL / "predictions" / "keyword.json").write_text(
        json.dumps({"method": "keyword", "cells": cells}, indent=1))
    print("wrote eval/predictions/keyword.json")


if __name__ == "__main__":
    main()
