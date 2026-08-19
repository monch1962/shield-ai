#!/usr/bin/env python3
"""SHIELD-AI artifact verification gate.

Checks that every generated artifact carries the CURRENT framework version and
control set after a rebuild. Called by tools/update_all.sh and by cron cycles
after any doc edit. Exits 1 if any check fails, printing the failing checks.

Checks:
- Core PDFs contain the new-control markers and the current control count
- Watchlist PDF/EPUB carry the current edition
- HTML deck PDFs carry the current framework version footer
- Architecture/impl SVGs carry the current control ranges
- Rego stub count and schema JSON count match the framework
- Client deck manifests record the current framework version
"""
import json
import os
import re
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EXPECTED_VERSION = "v1.7"
EXPECTED_COUNT = 59
CONTROL_ID = re.compile(r"^\- (MS|IAM|DS|TP|MIR|GRM|EE)-[0-9]+")

failures = []


def pdf_text(path):
    try:
        from pypdf import PdfReader
        r = PdfReader(path)
        full = " ".join((p.extract_text() or "") for p in r.pages)
    except Exception:
        full = subprocess.run(["mutool", "draw", "-F", "text", path],
                              capture_output=True, text=True, timeout=300).stdout
    return re.sub(r"\s+", " ", full)


def check(label, cond):
    print(f"  [{'OK' if cond else 'FAIL'}] {label}")
    if not cond:
        failures.append(label)


def count_controls():
    t = open("framework/shield-ai-framework.md", encoding="utf-8").read()
    return len(set(CONTROL_ID.match(ln) and ln[2:] for ln in t.split("\n") if CONTROL_ID.match(ln)))


def main():
    print(f"== Artifact verification vs framework {EXPECTED_VERSION}, {EXPECTED_COUNT} controls ==")

    # 1. Framework + core docs
    actual = count_controls()
    check(f"framework.md control count == {EXPECTED_COUNT} (found {actual})", actual == EXPECTED_COUNT)
    for doc, markers in [
        ("framework/shield-ai-framework.pdf", ["MS-11", "TP-12", f"{EXPECTED_COUNT} controls"]),
        ("framework/shield-ai-gap-analysis.pdf", ["INC-36", "MS-11", "TP-12"]),
        ("framework/shield-ai-implementation-architecture.pdf", ["MS-01..MS-11", "TP-01..TP-12"]),
        ("framework/shield-ai-tooling-map.pdf", [f"{EXPECTED_COUNT} controls"]),
        ("assessment-guide/shield-ai-assessment-guide.pdf", [f"{EXPECTED_COUNT} controls"]),
        ("presentations/what-is-shield-ai.pdf", [f"{EXPECTED_COUNT} controls"]),
        ("presentations/glossary.pdf", [f"{EXPECTED_COUNT} controls"]),
    ]:
        if not os.path.exists(doc):
            check(f"{doc} exists", False)
            continue
        txt = pdf_text(doc)
        check(f"{os.path.basename(doc)} has {markers}", all(m in txt for m in markers))

    # 2. Watchlist current edition
    wl = pdf_text("framework/shield-ai-watchlist.pdf")
    check("watchlist.pdf has 59 controls", f"{EXPECTED_COUNT} controls" in wl)
    check("watchlist.pdf has current edition date", "August 17, 2026" in wl)

    # 3. HTML deck PDFs carry the current framework version
    for deck in ["board-brief/shield-ai-deck-board", "business-deck/shield-ai-deck-business",
                 "buyers-journey-bridge/shield-ai-deck-bridge", "technical-deck/shield-ai-deck-technical"]:
        p = f"presentations/{deck}.pdf"
        if not os.path.exists(p):
            check(f"{p} exists", False)
            continue
        txt = pdf_text(p)
        check(f"{os.path.basename(p)} footer/version {EXPECTED_VERSION}", EXPECTED_VERSION in txt)

    # 4. SVG ranges
    arch = open("assets/diagrams/framework-architecture.svg", encoding="utf-8").read()
    for rng in ["MS-01 -> MS-11", "TP-01 -> TP-12", "DS-01 -> DS-07", "EE-01 -> EE-08", "IAM-01 -> IAM-09"]:
        check(f"framework-architecture.svg has {rng}", rng in arch)
    tel = open("assets/diagrams/impl-telemetry-pipeline.svg", encoding="utf-8").read()
    check("impl-telemetry-pipeline.svg has 59 controls", "59 controls" in tel)

    # 5. Rego + schema counts
    rego = len([f for f in os.listdir("policies") if f.endswith(".rego")])
    check(f"policies/*.rego count == {EXPECTED_COUNT} (found {rego})", rego == EXPECTED_COUNT)
    schema_doc = json.load(open("assets/shield-ai-control-schema.json", encoding="utf-8"))
    schema = schema_doc.get("controls", schema_doc)
    check(f"schema JSON count == {EXPECTED_COUNT} (found {len(schema)})", len(schema) == EXPECTED_COUNT)

    # 6. Client deck manifests record the current framework version
    for c in ["client-specific/defence", "client-specific/aware-super", "client-specific/nbn",
              "presentations/reference-architecture-walkthrough"]:
        mf = os.path.join(c, "deck-manifest.json")
        if not os.path.exists(mf):
            check(f"{mf} exists", False)
            continue
        m = json.load(open(mf, encoding="utf-8"))
        fv = m.get("framework_version")
        check(f"{os.path.basename(c)} manifest framework_version == {EXPECTED_VERSION} (found {fv})",
              fv == EXPECTED_VERSION)

    # 7. Client deck PPTX contain the v1.7 controls
    for c, ids in [("client-specific/defence", ["MS-11", "TP-12"]),
                   ("client-specific/aware-super", ["MS-11", "TP-12"]),
                   ("client-specific/nbn", ["MS-11", "TP-12"])]:
        pptx = None
        for f in os.listdir(c):
            if f.endswith(".pptx"):
                pptx = os.path.join(c, f)
        if not pptx:
            check(f"{c} pptx exists", False)
            continue
        z = zipfile.ZipFile(pptx)
        slides = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist()
                          if n.startswith("ppt/slides/") and n.endswith(".xml"))
        check(f"{os.path.basename(pptx)} has {ids}", all(i in slides for i in ids))

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("All artifact checks passed.")


if __name__ == "__main__":
    main()
