#!/usr/bin/env python3
"""Generate the SHIELD-AI explorer graph of record (`assets/shield-ai-explorer-graph.json`).

Parses the repo's committed sources and derives, into ONE committable,
schema-checked JSON document, the links the interactive explorer and
`tools/explore.py` consume:

  incidents  -> controls  (from each coverage verdict's explicit control refs)
  controls   -> pillar    (from control-schema.json)
  controls   -> REGO file (from policies/<pillar>_<pillar>-NN.rego existence)
  gaps       -> controls  (from exploits/*.md "Covering controls" rows)
  gaps       -> incidents (from exploits/*.md "Canonical incidents") and from
                           coverage verdicts' explicit G-refs
  exploits   -> their gap, controls, incidents

Because the graph is DERIVED at build time from committed sources and gated
byte-exact (like the reference views), it can never drift from the source of
truth. Any change to a control, incident, gap or policy auto-refreshes the
graph on the next `make check` -- and a stale committed graph fails the gate.

Usage:
    python3 tools/generate_explorer_graph.py --write   # write graph.json
    python3 tools/generate_explorer_graph.py           # print to stdout
    python3 tools/generate_explorer_graph.py --check   # fail if committed file
                                                       # differs from fresh output
    python3 tools/generate_explorer_graph.py --stats   # link summary
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CONTROL_SCHEMA = os.path.join(ROOT, "assets", "shield-ai-control-schema.json")
GAP_ANALYSIS = os.path.join(ROOT, "framework", "shield-ai-gap-analysis.md")
POLICIES_DIR = os.path.join(ROOT, "policies")
EXPLOITS_DIR = os.path.join(ROOT, "exploits")
OUT = os.path.join(ROOT, "assets", "shield-ai-explorer-graph.json")

CONTROL_ID = re.compile(r"\b((?:MS|IAM|DS|TP|MIR|GRM|EE)-[0-9]+)\b")
GAP_ID = re.compile(r"\b(G[0-9]+)\b")
PILLAR_ORDER = ["EE", "MS", "IAM", "DS", "TP", "MIR", "GRM"]
GAP_SEVERITY = {"Critical", "High", "Medium", "Low"}
REPO_SEVERITY = {
    "critical": "Critical", "high": "High",
    "medium": "Medium", "low": "Low",
}


# --- source loading ----------------------------------------------------------

def load_controls():
    """controls from control-schema.json + REGO filename existence."""
    with open(CONTROL_SCHEMA, encoding="utf-8") as f:
        schema = json.load(f)
    out = []
    for cid, c in schema["controls"].items():
        pillar, _, _ = cid.partition("-")
        rego = f"shield_ai_{pillar.lower()}_{pillar.lower()}-{cid.split('-')[1]}.rego"
        rego_content = None
        if os.path.exists(os.path.join(POLICIES_DIR, rego)):
            with open(os.path.join(POLICIES_DIR, rego), encoding="utf-8") as rf:
                rego_content = rf.read()
        out.append({
            "id": cid,
            "title": c.get("title", "").strip(),
            "pillar": pillar,
            "pillar_name": c.get("pillar_name", "").strip(),
            "rego": rego if os.path.exists(os.path.join(POLICIES_DIR, rego)) else None,
            "rego_content": rego_content,  # verbatim policy source for drill-down
            "description": (c.get("description") or "").strip(),
            "gap_ids": [],
            "incidents": [],
            "exploit_ids": [],
        })
    # stable order: pillar then numeric
    out.sort(key=lambda c: (PILLAR_ORDER.index(c["pillar"]) if c["pillar"] in PILLAR_ORDER else 99,
                            int(c["id"].split("-")[1])))
    return out


def load_incidents():
    """incidents from gap-analysis.md headings + coverage verdict body."""
    with open(GAP_ANALYSIS, encoding="utf-8") as f:
        text = f.read()
    out = []
    # Reference views already parse this file; we re-derive here for self-containment.
    # Matches "### INC-01: OpenAI Model Sandbox Escape".
    pat = re.compile(r"^###\s+(INC-\d+):\s*(.+)$", re.M)
    for m in pat.finditer(text):
        iid, title = m.group(1).strip(), m.group(2).strip()
        nxt = pat.search(text, m.end())
        body = text[m.end(): nxt.start() if nxt else len(text)]
        # verbatim narrative for drill-down: the "What happened:" paragraph.
        summary = ""
        wh = re.search(r"\*\*What happened:\*\*\s*(.+?)(?=\n\n|\n\|)", body, re.S)
        if wh:
            summary = re.sub(r"\s+", " ", wh.group(1)).strip()
        verdict_seg = ""
        v = re.search(r"\*\*Coverage verdict:\*\*(.*?)(?=\n### |\n## |\Z)", body, re.S)
        if v:
            verdict_seg = v.group(1)
        controls = sorted(set(CONTROL_ID.findall(verdict_seg)))
        gaps = sorted(set(GAP_ID.findall(verdict_seg)))
        sev = "evidence"  # no explicit severity = coverage evidence
        low = verdict_seg.lower()
        if "new gap" in low or "gap (" in low or ("gap" in low and "**" in verdict_seg):
            sev = "new_gap"
        elif "escalation" in low:
            sev = "escalation"
        out.append({
            "id": iid,
            "num": int(iid.split("-")[1]),
            "title": title,
            "summary": summary,  # verbatim "What happened:" narrative for drill-down
            "controls": controls,
            "gap_ids": gaps,
            "severity": sev,
        })
    out.sort(key=lambda i: i["num"])
    return out


def load_exploits():
    """exploits from exploits/*.md (gap-keyed), extracting covering controls +
    canonical incidents from the front-matter table."""
    out = []
    for fn in sorted(os.listdir(EXPLOITS_DIR)):
        if not re.match(r"^g\d+.*\.md$", fn):
            continue
        path = os.path.join(EXPLOITS_DIR, fn)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        m = re.match(r"^#\s+(G\d+):", text)
        gid = m.group(1) if m else fn.split("-")[0].strip("g0").join(["G", ""])
        if not m:
            gid = "G" + re.match(r"^g(\d+)", fn).group(1)
        # verbatim narrative for drill-down: the "Nature of the exploit" section
        description = ""
        dm = re.search(r"## Nature of the exploit\s*(.+?)(?=\n## |\Z)", text, re.S)
        if dm:
            description = re.sub(r"\s+", " ", dm.group(1)).strip()
        # covering controls row: "MS-11 (P1, new v1.7), MIR-02 (P5, extended)"
        cm = re.search(r"\*\*Covering controls\*\*[^\n]*\|?\s*([^\n]*)", text)
        controls = [x.strip() for x in CONTROL_ID.findall(cm.group(1))] if cm and cm.group(1) else []
        # severity row
        sm = re.search(r"\*\*Severity\*\*\s*\|\s*([^\n]+)", text)
        sev = "Medium"
        if sm:
            sev = REPO_SEVERITY.get(sm.group(1).strip().lower(), sm.group(1).strip())
        # canonical incidents row: "INC-33, INC-67"
        im = re.search(r"\*\*Canonical incidents\*\*[^\n]*\|?\s*([^\n]*)", text)
        incs = sorted(set(re.findall(r"INC-\d+", im.group(1)))) if im else []
        out.append({
            "id": gid,
            "file": fn,
            "description": description,  # verbatim narrative for drill-down
            "controls": controls,
            "incidents": incs,
            "severity": sev if sev in GAP_SEVERITY else "Medium",
        })
    out.sort(key=lambda e: int(e["id"].lstrip("G0") or 0))
    return out


def build_graph():
    controls = load_controls()
    incidents = load_incidents()
    exploits = load_exploits()
    cby_id = {c["id"]: c for c in controls}

    for c in controls:
        c["incidents"] = sorted(inc["id"] for inc in incidents if c["id"] in inc["controls"])

    # exploits: gap -> controls/incidents; also register exploits on the controls
    for ex in exploits:
        for cid in ex["controls"]:
            c = cby_id.get(cid)
            if c and ex["id"] not in c["exploit_ids"]:
                c["exploit_ids"].append(ex["id"])

    # gaps node list (derived from exploits + G refs in incidents)
    gap_ids = sorted(set(GAP_ID.findall(open(GAP_ANALYSIS, encoding="utf-8").read())))
    gaps = []
    for gid in gap_ids:
        ex = next((e for e in exploits if e["id"] == gid), None)
        controls_g = []
        incidents_g = []
        if ex:
            controls_g = ex["controls"]
            incidents_g = ex["incidents"]
        else:
            # gaps with no exploit entry still carry incident references
            incidents_g = sorted(inc["id"] for inc in incidents if gid in inc["gap_ids"])
        gaps.append({
            "id": gid,
            "severity": ex["severity"] if ex else "Medium",
            "description": ex["description"] if ex else "",
            "controls": sorted(set(controls_g)),
            "incidents": sorted(set(incidents_g)),
            "exploit": ex["file"] if ex else None,
        })
    gaps.sort(key=lambda g: int(g["id"].lstrip("G0") or 0))

    # derived edges for the graph renderer
    edges = []
    for inc in incidents:
        for cid in inc["controls"]:
            edges.append({"from": inc["id"], "to": cid, "type": "incident->control"})
        for gid in inc["gap_ids"]:
            edges.append({"from": inc["id"], "to": gid, "type": "incident->gap"})
    for ex in exploits:
        for cid in ex["controls"]:
            edges.append({"from": ex["id"], "to": cid, "type": "exploit->control"})

    return {
        "meta": {
            "framework": "SHIELD-AI",
            "control_count": len(controls),
            "incident_count": len(incidents),
            "pillar_count": 7,
            "gap_count": len(gaps),
            "rego_count": sum(1 for c in controls if c["rego"]),
            "generated": "tools/generate_explorer_graph.py",
        },
        "pillars": [
            {"id": p, "name": _pillar_name(p, controls), "controls": [c["id"] for c in controls if c["pillar"] == p]}
            for p in PILLAR_ORDER if any(c["pillar"] == p for c in controls)
        ],
        "controls": controls,
        "incidents": incidents,
        "gaps": gaps,
        "exploits": exploits,
        "edges": edges,
    }


def _pillar_name(pid, controls):
    for c in controls:
        if c["pillar"] == pid and c.get("pillar_name"):
            return c["pillar_name"]
    return pid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    g = build_graph()
    blob = json.dumps(g, indent=2, ensure_ascii=False) + "\n"

    if args.stats:
        print(f"controls={g['meta']['control_count']} incidents={g['meta']['incident_count']} "
              f"gaps={g['meta']['gap_count']} exploits={len(g['exploits'])} "
              f"pillars={g['meta']['pillar_count']} rego={g['meta']['rego_count']} edges={len(g['edges'])}")
        return 0

    if args.check:
        if os.path.exists(OUT):
            with open(OUT, encoding="utf-8") as f:
                cur = f.read()
            if cur == blob:
                print("explorer graph fresh.")
                return 0
            print("STALE explorer graph -- source changed; run "
                  "python3 tools/generate_explorer_graph.py --write", file=sys.stderr)
            return 1
        print("MISSING explorer graph -- run --write", file=sys.stderr)
        return 1

    if args.write:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"wrote {OUT}")
        return 0

    print(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())