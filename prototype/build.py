"""Build the keeper view: one self-contained HTML file, no server, no dependencies.

Inputs:
  carrowmore-data-pack/clean/keepers.json          grades, postings, training, certificates
  carrowmore-data-pack/clean/logbook_entries.json  what each keeper actually did
  carrowmore-data-pack/employers/certification_schemes.json
  eval/ai_labels.json                              the AI's sentence labels (see prompts/map_prompt.md)

Deliberately NOT read: raw/appraisals and station manager notes. The tool looks only
for evidence of work and training, rather than trying to filter out what it shouldn't show.

Run: python3 prototype/build.py  ->  prototype/index.html  (open it in any browser)
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval"))
from common import norm  # noqa: E402

PACK = ROOT / "carrowmore-data-pack"
YEAR = 2026
EVIDENCED_MIN = 2

# Requirements as the keeper sees them. "employer" is the posting's own wording;
# "plain" is ours. Log requirements use the AI labels; certificate requirements
# use training records.
LOG_REQS = {
    "R1_MAINT": {
        "plain": "Keeping engines, pumps, generators and electrical gear running",
        "route": "The Array trains this on the job. If you want something on paper first, the Marine Plant Maintenance Certificate (MPMC) covers it.",
    },
    "R2_FAULT": {
        "plain": "Finding electrical faults yourself",
        "route": "Module 3 of the Marine Electrical Competence Standard (MECS-3, Diagnostic practice) is the formal version.",
    },
    "R3_PERMIT": {
        "plain": "Working under permits to work",
        "route": "Usually learned on site. HVAP module 3 (Safety documentation and permit issue) covers issuing permits.",
    },
    "R4_HVSW": {
        "plain": "High-voltage switching, isolation and earthing",
        "route": "Two years' documented switching at 11kV or above, or a lapsed Authority HV authorization backed by paperwork.",
    },
    "R5_HEIGHT": {
        "plain": "Working at height or in confined spaces",
        "route": "The Working at Height and Rope Access Scheme (WAHS) is the usual certificate.",
    },
}

POSTINGS = [
    {
        "id": "om",
        "title": "Wind Turbine Technician (Operations & Maintenance)",
        "employer": "Carrowmore Array",
        "posts": "About 40 jobs",
        "note": "The Array says it would rather train good people than hire certificates, and that it does not need prior wind experience.",
        "items": [
            {"kind": "cert", "scheme": "OSSC", "level": "essential",
             "employer": "A valid offshore safety and survival certificate covering sea survival, fire, first aid and working at height."},
            {"kind": "medical", "level": "essential", "employer": "Offshore medical fitness."},
            {"kind": "log", "req": "R1_MAINT", "level": "essential",
             "employer": "Hands-on mechanical or electrical maintenance experience on plant you were responsible for."},
            {"kind": "log", "req": "R5_HEIGHT", "level": "essential",
             "employer": "Comfortable working at height, in enclosed spaces, and on a small boat in a swell."},
            {"kind": "log", "req": "R2_FAULT", "level": "desirable",
             "employer": "Fault-finding on electrical systems without a laptop telling you the answer."},
            {"kind": "log", "req": "R3_PERMIT", "level": "desirable",
             "employer": "Experience of working to a permit system."},
        ],
        "flags": [
            "The posting says the safety certificate covers working at height. In the scheme list we were given, height is a separate certificate (WAHS). Worth asking the Array which they mean before booking anything.",
        ],
    },
    {
        "id": "hv",
        "title": "High Voltage Authorized Person",
        "employer": "Carrowmore Array",
        "posts": "6 jobs",
        "note": "Set by the Array's insurers. The Array says it has no discretion over these requirements.",
        "items": [
            {"kind": "cert", "scheme": "HVAP", "level": "mandatory",
             "employer": "A current High Voltage Authorized Person certificate, all four modules including the practical assessment."},
            {"kind": "cert", "scheme": "MECS", "level": "prerequisite", "stage": 3,
             "employer": "MECS at Stage 3 or above (a prerequisite for HVAP)."},
            {"kind": "cert", "scheme": "OSSC", "level": "mandatory",
             "employer": "A current Offshore Safety and Survival Certificate, all modules."},
            {"kind": "medical", "level": "mandatory", "employer": "Offshore medical fitness certification."},
            {"kind": "log", "req": "R4_HVSW", "level": "mandatory", "gate": True,
             "employer": "Two years of documented switching experience on a system at 11kV or above."},
            {"kind": "log", "req": "R3_PERMIT", "level": "desirable",
             "employer": "Experience of issuing safety documents under a formal permit regime."},
        ],
        "flags": [],
    },
]


def main():
    keepers = json.loads((PACK / "clean" / "keepers.json").read_text())
    entries = json.loads((PACK / "clean" / "logbook_entries.json").read_text())
    schemes = {s["code"]: s for s in json.loads((PACK / "employers" / "certification_schemes.json").read_text())["schemes"]}
    labels = json.loads((ROOT / "eval" / "ai_labels.json").read_text())["labels"]

    by_keeper = defaultdict(list)
    for e in entries:
        by_keeper[e["keeper_code"]].append(e)

    out = []
    for k in sorted(keepers, key=lambda k: k["name_ascii"]):
        if k["status"] != "current":
            continue
        mine = sorted(by_keeper[k["keeper_code"]], key=lambda e: e["date"])
        evidence = {}
        for r in LOG_REQS:
            yes, maybe = [], []
            for e in mine:
                lab = labels.get(norm(e["text"]), {}).get("labels", {}).get(r)
                row = [e["date"], e["station"], e["text"], e["source_record"]]
                if lab == "Y":
                    yes.append(row)
                elif lab == "?":
                    maybe.append(row)
            evidence[r] = {"yes": yes, "maybe": maybe[-12:], "maybe_count": len(maybe)}

        training = defaultdict(list)
        for t in k["training_records"]:
            training[t["scheme"]].append([t["module"], t["module_name"].replace("Authorised", "Authorized"), t["year"], t["outcome"]])
        certs = {c["scheme"]: c for c in k["certifications"]}
        stations = sorted({p["station"] for p in k["postings"]})
        out.append({
            "code": k["keeper_code"],
            "name": k["name"],
            "grade": k["current_grade"],
            "joined": int(k["date_joined"][:4]),
            "stations": stations,
            "entries": len(mine),
            "evidence": evidence,
            "training": training,
            "certs": certs,
        })

    payload = {
        "year": YEAR,
        "evidenced_min": EVIDENCED_MIN,
        "log_reqs": LOG_REQS,
        "postings": POSTINGS,
        "not_assessed": [
            "Marine Electrician, Port of Cnoc Harbour Trust",
            "Watch Officer, Northern Isles Coastguard Service",
            "Offshore Survey Technician, Deepline Offshore",
            "Hydrographic Technician, Meridian Survey",
        ],
        "schemes": {c: {"name": s["name"].replace("Authorised", "Authorized"), "renewal": s.get("renewal_years"),
                        "modules": [[m["code"], m["name"].replace("Authorised", "Authorized")] for m in s["modules"]]}
                    for c, s in schemes.items()},
        "keepers": out,
    }
    import base64
    logo = lambda name: "data:image/png;base64," + base64.b64encode(
        (ROOT / "prototype" / "assets" / name).read_bytes()).decode()
    template = (ROOT / "prototype" / "template.html").read_text()
    html = (template
            .replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
            .replace("__LOGO_WHITE__", logo("pearson-logo-white.png")))
    (ROOT / "prototype" / "index.html").write_text(html, encoding="utf-8")
    print(f"wrote prototype/index.html ({len(html) // 1024} KB, {len(out)} keepers)")


if __name__ == "__main__":
    main()
