"""Turn the AI's sentence labels into per-keeper verdicts, in the same shape as the keyword baseline.

A keeper is Evidenced for a requirement when 2 or more of their entries carry a Y label.
'?' entries are kept as "possible, worth checking" and never count as evidence.
The HV gate (R4_HVSW) can reach Evidenced at most; it is never marked met.

Run: python3 eval/predict_ai.py  ->  eval/predictions/ai.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import norm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"


def main():
    labels = json.loads((EVAL / "ai_labels.json").read_text())["labels"]
    reqs = [r["id"] for r in json.loads((EVAL / "requirements.json").read_text())["requirements"]]
    selected = [k["keeper_code"] for k in json.loads((EVAL / "selection.json").read_text())["keepers"]]
    entries = json.loads((CLEAN / "logbook_entries.json").read_text())

    cells = {k: {} for k in selected}
    for k in selected:
        mine = [e for e in entries if e["keeper_code"] == k]
        for r in reqs:
            cited = [e["entry_id"] for e in mine
                     if labels.get(norm(e["text"]), {}).get("labels", {}).get(r) == "Y"]
            possible = [e["entry_id"] for e in mine
                        if labels.get(norm(e["text"]), {}).get("labels", {}).get(r) == "?"]
            cells[k][r] = {"verdict": "Evidenced" if len(cited) >= 2 else "Not yet shown",
                           "cited": cited, "possible": possible}
    (EVAL / "predictions").mkdir(exist_ok=True)
    (EVAL / "predictions" / "ai.json").write_text(json.dumps({"method": "ai", "cells": cells}, indent=1))
    print("wrote eval/predictions/ai.json")


if __name__ == "__main__":
    main()
