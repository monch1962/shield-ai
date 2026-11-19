#!/usr/bin/env python3
"""Generate OSCAL documents from the SHIELD-AI control schema.

Reads  assets/shield-ai-control-schema.json  (canonical control metadata)
Writes oscal/shield-ai-catalog.json               OSCAL catalog (7 groups, 69 controls)
       oscal/shield-ai-component-definition.json  OPA bundle as an OSCAL component

Deterministic: UUIDs are uuid5 of stable names, so re-running without a source change
produces identical output except metadata.last-modified (--stamp pins it).

Usage:  python3 tools/generate_oscal_catalog.py [--stamp 2026-11-19T00:00:00+00:00]
"""
import argparse
import datetime
import json
import os
import re
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OSCAL_VERSION = "1.2.0"
NS_URI = "https://github.com/monch1962/shield-ai/ns/oscal"
_UUID_NS = uuid.UUID("6f0b1c52-5a1e-4c1a-9a55-5a1e1d0a0001")


def uid(*parts):
    return str(uuid.uuid5(_UUID_NS, "/".join(parts)))


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def build(src, stamp):
    def meta(title):
        return {"title": title, "last-modified": stamp, "version": src["meta"]["version"],
                "oscal-version": OSCAL_VERSION}

    groups = []
    for pid, p in src["pillars"].items():
        ctrls = []
        for cid in p["control_ids"]:
            c = src["controls"][cid]
            lid = cid.lower()
            props = [{"name": "label", "value": cid}]
            props += [{"name": "tag", "ns": NS_URI, "value": t} for t in c.get("tags", [])]
            for fw, ref in c.get("regulatory_mappings", {}).items():
                # OSCAL 'class' is a token: no spaces
                props.append({"name": "regulatory-mapping", "ns": NS_URI, "class": slug(fw), "value": str(ref)})
            parts = [
                {"id": f"{lid}_smt", "name": "statement", "prose": c["description"]},
                {"id": f"{lid}_obj", "name": "objective", "prose": c["objective"]},
                {"id": f"{lid}_mat", "name": "maturity", "ns": NS_URI,
                 "parts": [{"id": f"{lid}_mat_{lv.lower()}", "name": "level", "ns": NS_URI,
                            "props": [{"name": "level", "ns": NS_URI, "value": lv}], "prose": t}
                           for lv, t in c["maturity"].items()]},
                {"id": f"{lid}_asm", "name": "assessment-objective",
                 "parts": [{"id": f"{lid}_asm_{i}", "name": "assessment-objective", "prose": q}
                           for i, q in enumerate(c.get("assessment_questions", []), 1)]},
                {"id": f"{lid}_art", "name": "assessment-method", "props": [{"name": "method", "value": "EXAMINE"}],
                 "parts": [{"name": "objects", "prose": a} for a in c.get("artifacts", [])]},
            ]
            ctrls.append({"id": lid, "class": "shield-ai-control", "title": c["title"],
                          "props": props, "parts": parts})
        groups.append({"id": pid.lower(), "class": "pillar", "title": p["name"], "controls": ctrls})

    catalog = {"catalog": {"uuid": uid("catalog"), "metadata": meta("SHIELD-AI Control Catalog"),
                           "groups": groups}}

    impl = []
    for p in src["pillars"].values():
        for cid in p["control_ids"]:
            impl.append({
                "uuid": uid("ir", cid), "control-id": cid.lower(),
                "description": f"Deny-override Rego policy policies/shield_ai_*_{cid.lower()}.rego, verified by OPA test vectors.",
                "props": [{"name": "implementation-status", "value": "implemented"},
                          {"name": "enforcement-point", "ns": NS_URI, "value": "opa-pdp"}]})
    compdef = {"component-definition": {
        "uuid": uid("compdef"), "metadata": meta("SHIELD-AI OPA Policy Bundle"),
        "components": [{
            "uuid": uid("comp", "opa"), "type": "software",
            "title": "SHIELD-AI OPA policy bundle + Go sidecar",
            "description": "Deny-override Rego policies evaluated by OPA behind a tool-gateway sidecar.",
            "control-implementations": [{
                "uuid": uid("ci"), "source": "shield-ai-catalog.json",
                "description": "All SHIELD-AI controls implemented as policy-as-code.",
                "implemented-requirements": impl}]}]}}
    return catalog, compdef


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default=os.path.join(ROOT, "assets", "shield-ai-control-schema.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "oscal"))
    ap.add_argument("--stamp", default=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat())
    a = ap.parse_args()
    src = json.load(open(a.schema))
    catalog, compdef = build(src, a.stamp)
    os.makedirs(a.out, exist_ok=True)
    for name, doc in (("shield-ai-catalog.json", catalog), ("shield-ai-component-definition.json", compdef)):
        with open(os.path.join(a.out, name), "w") as f:
            json.dump(doc, f, indent=2)
            f.write("\n")
    n = sum(len(g["controls"]) for g in catalog["catalog"]["groups"])
    print(f"wrote {a.out}: {n} controls in {len(catalog['catalog']['groups'])} groups (OSCAL {OSCAL_VERSION})")


if __name__ == "__main__":
    main()
