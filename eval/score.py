"""Score each method against the hand grades and apply the pre-registered decision rules.

The rules live here in code, committed before any AI output existed, so the call
can't be reshaped after the results are in. See EVALUATION_PLAN.md.

Run: python3 eval/score.py  ->  prints the report, writes eval/results.json
Needs: eval/grading_sheet.csv (graded), eval/predictions/*.json
"""
import csv
import json
import re

from collections import defaultdict
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "eval"
CLEAN = ROOT / "carrowmore-data-pack" / "clean"

# ---- Pre-registered decision rules -------------------------------------------
EVIDENCED_MIN = 2            # supporting entries needed for a cell to count as Evidenced
PERSEVERE_MAX = 0.10         # AI overclaim rate at or below this: persevere
PIVOT_MAX = 0.25             # above PERSEVERE_MAX and up to this: pivot (advisor-reviewed)
RECALL_FLOOR = 0.50          # AI recall below this: kill (the over-cautious failure)
BASELINE_RECALL_SLACK = 0.10 # AI may trail keyword recall by up to this and still "beat" it
NEAR_BOUNDARY = 0.05         # point estimate this close to a band edge, with a wide CI: inconclusive
REQ_DROP_OVERCLAIM = 0.50    # per requirement: drop from the tool if overclaim exceeds this
REQ_DROP_RECALL = 0.30       # ...or recall falls below this
ERA_GAP_FLAG = 0.20          # era-1 entry recall trailing era-3 by more than this: fairness flag
GATE_REQS = {"R4_HVSW"}      # log evidence may never mark these as met
# ------------------------------------------------------------------------------


import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import norm  # noqa: E402


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def rate(k, n):
    return {"k": k, "n": n, "rate": round(k / n, 3) if n else None, "ci95": wilson(k, n)}


def guide_example_prefixes():
    """Normalized prefixes of the example sentences in GRADING_GUIDE.md. The same model
    wrote those example calls and the AI labels, so they are excluded in a sensitivity run."""
    out = []
    for line in (EVAL / "GRADING_GUIDE.md").read_text().splitlines():
        m = re.match(r"- (?:`[Y?]`|blank:)\s+(.*)", line.strip())
        if m:
            text = re.split(r"\.\.\.|\*\(", m.group(1))[0]
            out.append(norm(text))
    return [p for p in out if p]


def load_grades(reqs):
    """Wide sheet: one row per sentence, one column per requirement.
    Y = supports. ? = can't tell (counted as not supporting). Blank = No."""
    grades, unsure, odd = {}, 0, 0
    sheets = [EVAL / "grading_sheet.csv", EVAL / "grading_sheet_part2.csv"]
    rows = []
    for path in sheets:
        if path.exists():
            with open(path, encoding="utf-8-sig") as f:
                rows += list(csv.DictReader(f))
    for row in rows:
        n = norm(row["entry_text"])
        for r in reqs:
            g = (row.get(r) or "").strip().upper()
            if g == "?":
                unsure += 1
            elif g not in ("", "Y", "N"):
                odd += 1
            grades[(r, n)] = (g == "Y")
    return grades, unsure, odd


def score_method(pred, grades, entries_by_id, keepers, reqs, gt_supporting):
    res = {"cells": {}, "gate_violations": []}
    tot = defaultdict(lambda: defaultdict(int))
    era_hit, era_all = defaultdict(int), defaultdict(int)
    for k, split in keepers.items():
        for r in reqs:
            cell = pred["cells"][k][r]
            cited = [i for i in cell["cited"] if i in entries_by_id]
            ok = [i for i in cited if grades.get((r, norm(entries_by_id[i]["text"])), False)]
            ungraded = [i for i in cited if (r, norm(entries_by_id[i]["text"])) not in grades]
            # A claim is Evidenced with at least EVIDENCED_MIN citations. Recomputed here so a
            # sensitivity run that removes sentences also removes the claims they supported.
            claims = cell["verdict"] in ("Evidenced", "Authorized", "Met") and len(cited) >= EVIDENCED_MIN
            if r in GATE_REQS and cell["verdict"] in ("Authorized", "Met"):
                res["gate_violations"].append(f"{k}/{r}")
            gt = len(gt_supporting[k][r]) >= EVIDENCED_MIN
            found = claims and len(ok) >= EVIDENCED_MIN
            over = claims and len(ok) < EVIDENCED_MIN
            for s in (split, "all"):
                t = tot[s]
                t["claims"] += claims
                t["over"] += over
                t["gt_pos"] += gt
                t["found"] += found and gt
                t["cited"] += len(cited)
                t["cited_ok"] += len(ok)
                t["ungraded"] += len(ungraded)
                tr = tot[f"{s}:{r}"]
                tr["claims"] += claims
                tr["over"] += over
                tr["gt_pos"] += gt
                tr["found"] += found and gt
            for i in gt_supporting[k][r]:
                era = entries_by_id[i]["source_era"]
                era_all[era] += 1
                era_hit[era] += i in cited
            res["cells"][f"{k}/{r}"] = {"verdict": cell["verdict"], "gt_evidenced": gt,
                                         "supporting_cited": len(ok), "cited": len(cited),
                                         "overclaim": over}
    summ = {}
    for s, t in tot.items():
        summ[s] = {"overclaim": rate(t["over"], t["claims"]),
                   "recall": rate(t["found"], t["gt_pos"])}
        if ":" not in s:
            summ[s]["citation_precision"] = rate(t["cited_ok"], t["cited"])
            summ[s]["ungraded_citations"] = t["ungraded"]
    res["summary"] = summ
    res["era_recall"] = {e: rate(era_hit[e], era_all[e]) for e in sorted(era_all)}
    return res


def band(r):
    if r is None:
        return "no claims"
    if r <= PERSEVERE_MAX:
        return "persevere"
    if r <= PIVOT_MAX:
        return "pivot"
    return "kill"


def decide(ai, kw):
    notes = []
    if ai["gate_violations"]:
        notes.append(f"DEFECT: gate requirement marked met from logs: {ai['gate_violations']}. Fix in code; kill only if a rule cannot prevent it.")

    def beats(split):
        a, b = ai["summary"][split], kw["summary"][split]
        if a["overclaim"]["rate"] is None or b["overclaim"]["rate"] is None:
            return None
        # A cite-everything baseline can keep cell-level overclaim low simply by citing
        # so much that two supporting entries are always in the pile. What a keeper
        # sees is the citations, so the AI must show a cleaner evidence list
        # (higher citation precision), without overclaiming more and without
        # missing much more.
        cleaner = (a["citation_precision"]["rate"] or 0) > (b["citation_precision"]["rate"] or 0)
        no_worse_over = a["overclaim"]["rate"] <= b["overclaim"]["rate"]
        recall_ok = (a["recall"]["rate"] or 0) >= (b["recall"]["rate"] or 0) - BASELINE_RECALL_SLACK
        return cleaner and no_worse_over and recall_ok

    dev, hold = beats("dev"), beats("holdout")
    if hold is False:
        return "KILL", notes + ["AI does not beat the keyword baseline on the holdout keepers."]
    if hold is None or dev != hold:
        primary = "INCONCLUSIVE"
        notes.append("Dev and holdout disagree on whether the AI beats the keyword baseline (or holdout has no claims).")
    else:
        primary = None

    o = ai["summary"]["all"]["overclaim"]
    if o["rate"] is None:
        return "KILL", notes + ["AI made no Evidenced claims at all."]
    rc = ai["summary"]["all"]["recall"]["rate"] or 0
    if rc < RECALL_FLOOR:
        return "KILL", notes + [f"AI recall {rc:.0%} is below the {RECALL_FLOOR:.0%} floor: the over-cautious failure."]
    b = band(o["rate"])
    lo, hi = o["ci95"]
    edges = (PERSEVERE_MAX, PIVOT_MAX)
    near = any(abs(o["rate"] - e) <= NEAR_BOUNDARY for e in edges)
    spans = band(lo) != band(hi)
    if near and spans:
        return "INCONCLUSIVE", notes + [f"Overclaim {o['rate']:.0%} (95% CI {lo:.0%} to {hi:.0%}) sits within {NEAR_BOUNDARY:.0%} of a band edge."]
    call = primary or b.upper()
    if spans:
        notes.append(f"Provisional: the 95% interval ({lo:.0%} to {hi:.0%}) reaches into another band.")
    return call, notes


def main():
    reqs = [r["id"] for r in json.loads((EVAL / "requirements.json").read_text())["requirements"]]
    keepers = {k["keeper_code"]: k["split"] for k in json.loads((EVAL / "selection.json").read_text())["keepers"]}
    entries = json.loads((CLEAN / "logbook_entries.json").read_text())
    by_id = {e["entry_id"]: e for e in entries}
    grades, unsure, blank = load_grades(reqs)
    excluded = 0
    if "--exclude-guide" in sys.argv:
        prefixes = guide_example_prefixes()
        drop = {n for (_, n) in grades if any(n.startswith(p) for p in prefixes)}
        excluded = len(drop)
        entries = [e for e in entries if norm(e["text"]) not in drop]
        by_id = {e["entry_id"]: e for e in entries}
        print(f"Sensitivity run: excluding {excluded} guide-example sentences")
    if blank:
        print(f"WARNING: {blank} cells hold something other than Y, N, ? or blank")

    gt = {k: {r: [] for r in reqs} for k in keepers}
    for e in entries:
        if e["keeper_code"] in keepers:
            for r in reqs:
                if grades.get((r, norm(e["text"])), False):
                    gt[e["keeper_code"]][r].append(e["entry_id"])

    results = {"unsure_grades": unsure, "ungraded_items": blank, "methods": {}}
    for p in sorted((EVAL / "predictions").glob("*.json")):
        pred = json.loads(p.read_text())
        results["methods"][pred["method"]] = score_method(pred, grades, by_id, keepers, reqs, gt)

    m = results["methods"]
    if "ai" in m and "keyword" in m:
        call, notes = decide(m["ai"], m["keyword"])
        results["call"] = call
        results["notes"] = notes
        ai = m["ai"]["summary"]
        results["dropped_requirements"] = [
            r for r in reqs if (ai.get(f"all:{r}", {}).get("overclaim", {}).get("rate") or 0) > REQ_DROP_OVERCLAIM
            or ((ai.get(f"all:{r}", {}).get("recall", {}).get("rate") is not None)
                and ai[f"all:{r}"]["recall"]["rate"] < REQ_DROP_RECALL)]
        er = m["ai"]["era_recall"]
        if 1 in er and 3 in er and er[1]["rate"] is not None and er[3]["rate"] is not None:
            results["fairness_flag"] = (er[3]["rate"] - er[1]["rate"]) > ERA_GAP_FLAG

    (EVAL / ("results_exclude_guide.json" if "--exclude-guide" in sys.argv else "results.json")).write_text(json.dumps(results, indent=1, default=str))
    for name, r in m.items():
        s = r["summary"]["all"]
        print(f"{name:8s} overclaim {s['overclaim']['rate']} {s['overclaim']['ci95']}  "
              f"recall {s['recall']['rate']} {s['recall']['ci95']}  "
              f"citation precision {s['citation_precision']['rate']}  ungraded cites {s['ungraded_citations']}")
    if "call" in results:
        print("CALL:", results["call"])
        for n in results["notes"]:
            print(" -", n)
        print("dropped requirements:", results["dropped_requirements"])
        print("fairness flag:", results.get("fairness_flag"))


if __name__ == "__main__":
    main()
