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
- Freshness: every tracked PDF/EPUB/HTML derived artifact is not older than its
  source(s), so an edited markdown/build script can never be committed with a
  stale artifact (drift becomes a hard gate failure, not a silent regression)
"""
import json
import os
import re
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from control_metadata import control_count_text, pillar_ranges

EXPECTED_VERSION = "v1.22"
EXPECTED_COUNT = 69
EXPECTED_EDITION = "November 9, 2026"
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


def frontmatter_date(path):
    """First `date:` field in the YAML frontmatter (no YAML dependency)."""
    with open(path, encoding="utf-8") as f:
        in_fm = False
        for ln in f:
            s = ln.strip()
            if s == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm:
                m = re.match(r'^date:\s*"?([^"]+)"?\s*$', s)
                if m:
                    return m.group(1).strip()
    return None


def count_opa_tests():
    """Number of top-level OPA test rules (matches `opa test` PASS total)."""
    import glob
    total = 0
    for base in ("policies", "demo"):
        for p in glob.glob(f"{base}/**/*.rego", recursive=True):
            try:
                body = open(p, encoding="utf-8").read()
            except OSError:
                continue
            total += len(re.findall(r"(?m)^test_[\w]+\s+if\b", body))
    return total


def check_stale_control_counts(path, label):
    """Reject any '<N> controls' in a current-state doc where N != EXPECTED_COUNT.

    Presence of the correct count (checked elsewhere) never catches that the
    SAME document also asserts a stale number (e.g. v1.18==67 + v1.20==69 both
    in README). This closes that: a current-state doc states one number.
    """
    txt = re.sub(r"<[^>]+>", " ", open(path, encoding="utf-8").read())
    # Exclude fraction denominators ("47/61 controls deny-observed at runtime")
    # and digit runs that are parts of IDs or ranges -- we only want a standalone
    # integer asserting a control TOTAL.
    pat = re.compile(rf"(?<![0-9/])(?<![\d])(?!{EXPECTED_COUNT}\b)\d+\s+controls", re.IGNORECASE)
    for stale in pat.findall(txt):
        check(f"{label} asserts a stale control count: '{stale.strip()}'", False)


def main():
    print(f"== Artifact verification vs framework {EXPECTED_VERSION}, {EXPECTED_COUNT} controls ==")

    # 1. Framework + core docs
    actual = count_controls()
    check(f"framework.md control count == {EXPECTED_COUNT} (found {actual})", actual == EXPECTED_COUNT)
    for doc, markers in [
        ("framework/shield-ai-framework.pdf", ["MS-12", "TP-12", "TP-13", f"{EXPECTED_COUNT} controls"]),
        ("framework/shield-ai-gap-analysis.pdf", ["INC-44", "MS-12", "TP-13"]),
        ("framework/shield-ai-implementation-architecture.pdf", ["MS-01..MS-12", "TP-01..TP-15"]),
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
    check("watchlist.pdf has 62 controls", f"{EXPECTED_COUNT} controls" in wl)
    check(f"watchlist.pdf has current edition date ({EXPECTED_EDITION})", EXPECTED_EDITION in wl)

    # 3. HTML deck PDFs carry the current framework version
    for deck in ["board-brief/shield-ai-deck-board", "business-deck/shield-ai-deck-business",
                 "buyers-journey-bridge/shield-ai-deck-bridge", "technical-deck/shield-ai-deck-technical"]:
        p = f"presentations/{deck}.pdf"
        if not os.path.exists(p):
            check(f"{p} exists", False)
            continue
        txt = pdf_text(p)
        check(f"{os.path.basename(p)} footer/version {EXPECTED_VERSION}", EXPECTED_VERSION in txt)

    # 4. SVG ranges (derived from the framework so a control-set change forces
    #    a diagram rebuild -- the count can never silently lag EXPECTED_COUNT)
    arch = open("assets/diagrams/framework-architecture.svg", encoding="utf-8").read()
    for rng in pillar_ranges().values():
        check(f"framework-architecture.svg has {rng}", rng in arch)
    tel = open("assets/diagrams/impl-telemetry-pipeline.svg", encoding="utf-8").read()
    check(f"impl-telemetry-pipeline.svg has {control_count_text()}", control_count_text() in tel)

    # 4b. Reference views (derived from the framework so a control/incident/maturity
    #     change forces a rebuild -- the simplified views can never drift)
    _rv_diags = {
        "pillar-control-atlas.svg": control_count_text(),
        "controls-incident-map.svg": control_count_text(),
        "control-au-framework-matrix.svg": control_count_text(),
        "pillar-maturity-heat.svg": control_count_text(),
        "control-outcomes-diagram.svg": control_count_text(),
        "control-technical-sheet.svg": control_count_text(),
        "policy-coverage-heat.svg": control_count_text(),
    }
    for name, needle in _rv_diags.items():
        p = os.path.join("assets/diagrams", name)
        if not os.path.exists(p):
            check(f"reference view diagram {name} exists", False)
            continue
        data = open(p, encoding="utf-8").read()
        check(f"reference view diagram {name} carries {needle}", needle in data)
        # Guard against the viewport-clipping class of bug: every <text y=...>
        # (and the deepest <rect>) must fall inside the viewBox height, or the
        # rendered SVG silently drops controls past the hardcoded canvas edge.
        _vb = re.search(r'viewBox="0 0 \d+ (\d+)"', data)
        if _vb:
            _h = int(_vb.group(1))
            _ys = [int(y) for y in re.findall(r'y="(\d+)"', data)]
            _max = max(_ys) if _ys else 0
            check(f"reference view diagram {name} content fits viewport (max y {_max} <= {_h})", _max <= _h)
        # Horizontal-overlap guard: text in a fixed-width cell must stay inside
        # its cell so it can't bleed into the adjacent box (e.g. the maturity-heat
        # diagram's 140px cells: a line longer than the wrap width overruns the
        # right edge into the next cell). The generator wraps maturity cell text
        # at 25 chars @ 9px = ~133px < 140px cell, + 8px left pad.
        if name == "pillar-maturity-heat.svg":
            _mline = max((len(t) for t in re.findall(r'class="sm" fill="[^"]+">([^<]+)</text>', data)
                          if not t.startswith("Across ")), default=0)
            check(f"{name} maturity cell text stays within wrap (max line {_mline} <= 25)", _mline <= 25)
    _rv_docs = [
        "reference-views/01-pillar-control-atlas.md",
        "reference-views/02-controls-incidents.md",
        "reference-views/03-control-au-framework-matrix.md",
        "reference-views/04-pillar-maturity.md",
        "reference-views/05-controls-outcomes.md",
        "reference-views/06-controls-technical.md",
            "reference-views/07-incident-summaries.md",
            "reference-views/08-policy-coverage-heat.md",
            "reference-views/09-assessment-scorecard.md",
            "reference-views/10-implementation-roadmap.md",
            "reference-views/11-executive-one-pager.md",
            "reference-views/README.md",
    ]
    for p in _rv_docs:
        check(f"reference view {os.path.basename(p)} exists", os.path.exists(p))

    # 4c. Incident-link integrity: every incident link in docs 06 and 02 must
    #     resolve to a summary card anchor in doc 07, and every 'full detail'
    #     link in doc 07 must resolve to a real incident heading in the
    #     gap-analysis. Anchors are computed with the GitHub-compatible
    #     algorithm (_github_anchor) -- never a bespoke slug -- so each link
    #     resolves in the rendered GitHub view, not just in a self-consistent
    #     local comparison.
    def _github_anchor(heading):
        # heading is the FULL rendered heading line ("INC-01: Title").
        t = heading.lower()
        t = re.sub(r"[^0-9a-z\s-]", "", t)
        t = re.sub(r"\s+", "-", t)
        t = re.sub(r"-{2,}", "-", t)
        return t.strip("-")

    _rv7_p = "reference-views/07-incident-summaries.md"
    _rv7 = open(_rv7_p, encoding="utf-8").read() if os.path.exists(_rv7_p) else ""
    if _rv7:
        # GitHub anchors cover the whole heading incl. the INC-x: prefix, e.g.
        # "### INC-01: Title" -> "#inc-01-title". Reconstruct the full heading
        # from the two capture groups so the validation matches rendered links.
        _anchors7 = set(
            _github_anchor(f"{inc}: {t}")
            for inc, t in re.findall(r"^### (INC-\d+):\s*(.+?)\s*$", _rv7, re.M))
        for _src in ("reference-views/06-controls-technical.md",
                     "reference-views/02-controls-incidents.md"):
            _txt = open(_src, encoding="utf-8").read()
            _linked = re.findall(r"\]\(\.\./reference-views/07-incident-summaries\.md#([a-z0-9-]+)\)", _txt)
            _bad = sorted({a for a in _linked if a not in _anchors7})
            check(f"{os.path.basename(_src)} incident links resolve in doc 07 (broken: {_bad})", not _bad)
        _ga = open("framework/shield-ai-gap-analysis.md", encoding="utf-8").read()
        _g_anchors = set(
            _github_anchor(f"{inc}: {t}")
            for inc, t in re.findall(r"^### (INC-\d+):\s*(.+?)\s*$", _ga, re.M))
        _deep = re.findall(r"\]\(\.\./framework/shield-ai-gap-analysis\.md#([a-z0-9-]+)\)", _rv7)
        _bad_deep = sorted({a for a in _deep if a not in _g_anchors})
        check(f"doc 07 'full detail' links resolve in gap-analysis (broken: {_bad_deep})", not _bad_deep)

    # 5. Rego + schema counts
    rego = len([f for f in os.listdir("policies") if f.endswith(".rego")])
    check(f"policies/*.rego count == {EXPECTED_COUNT} (found {rego})", rego == EXPECTED_COUNT)
    schema_doc = json.load(open("assets/shield-ai-control-schema.json", encoding="utf-8"))
    schema = schema_doc.get("controls", schema_doc)
    check(f"schema JSON count == {EXPECTED_COUNT} (found {len(schema)})", len(schema) == EXPECTED_COUNT)
    # Schema meta.version/date must track the framework release (single source
    # of truth: tools/generate_control_schema.py derives it from the framework
    # footer; the schema generator regen is part of `make check`). Prevents the
    # schema's stamped version silently drifting behind the framework.
    meta_ver = schema_doc.get("meta", {}).get("version")
    meta_date = schema_doc.get("meta", {}).get("date")
    check(f"schema meta.version == framework {EXPECTED_VERSION} (found {meta_ver})",
          meta_ver == EXPECTED_VERSION.lstrip("v"))
    # Schema meta.date is "YYYY-MM"; EXPECTED_EDITION is "Month D, YYYY".
    _months = ["January","February","March","April","May","June","July",
               "August","September","October","November","December"]
    _er_parts = EXPECTED_EDITION.replace(",", "").split(" ")   # ["October","12","2026"]
    _expected_date = ""
    if len(_er_parts) == 3 and _er_parts[0] in _months and _er_parts[2].isdigit():
        _expected_date = f"{_er_parts[2]}-{_months.index(_er_parts[0]) + 1:02d}"
    check(f"schema meta.date == edition month (found {meta_date})",
          meta_date == _expected_date)

    # 5b. Schema <-> framework control-set drift (1:1, not just counts)
    fw_text = open("framework/shield-ai-framework.md", encoding="utf-8").read()
    ctrl_bullet = re.compile(r"^\- ((?:MS|IAM|DS|TP|MIR|GRM|EE)-[0-9]+):")
    fw_ids = {m.group(1) for ln in fw_text.split("\n") if (m := ctrl_bullet.match(ln))}
    schema_ids = set(schema)
    check(f"framework.md control IDs == schema control_ids "
          f"(missing in schema: {sorted(fw_ids - schema_ids)}, "
          f"extra in schema: {sorted(schema_ids - fw_ids)})",
          fw_ids == schema_ids)

    # 5c. Rego implementation status (informational; non-stub controls)
    implemented = sorted(
        f for f in os.listdir("policies")
        if f.endswith(".rego")
        and "# TODO: Implement control test logic"
        not in open(os.path.join("policies", f), encoding="utf-8").read()
    )
    print(f"  [info] {len(implemented)}/{EXPECTED_COUNT} controls implemented (non-stub):")
    for f in implemented:
        print(f"         {f}")

    # 6. Client deck manifests record the current framework version
    for c in ["client-specific/defence", "client-specific/aware-super", "client-specific/nbn",
              "client-specific/retailer", "presentations/reference-architecture-walkthrough"]:
        mf = os.path.join(c, "deck-manifest.json")
        if not os.path.exists(mf):
            check(f"{mf} exists", False)
            continue
        m = json.load(open(mf, encoding="utf-8"))
        fv = m.get("framework_version")
        check(f"{os.path.basename(c)} manifest framework_version == {EXPECTED_VERSION} (found {fv})",
              fv == EXPECTED_VERSION)

    # 7. Client deck PPTX contain the v1.9 controls
    for c, ids in [("client-specific/defence", ["MS-12", "TP-12", "TP-13"]),
                   ("client-specific/aware-super", ["MS-12", "TP-12"]),
                   ("client-specific/nbn", ["MS-12", "TP-12"]),
                   ("client-specific/retailer", ["MS-12", "TP-12"])]:
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

    # 8. Markdown source footers carry the current version (drift guard:
    #    catches the class of staleness the count sweep misses, e.g. a footer
    #    left at "v1.6" while the document content is v1.7).
    for doc, markers in [
        ("framework/shield-ai-framework.md", [f"SHIELD-AI {EXPECTED_VERSION}"]),
        ("framework/shield-ai-gap-analysis.md", [f"Gap Analysis {EXPECTED_VERSION}", EXPECTED_EDITION]),
        ("assessment-guide/shield-ai-assessment-guide.md", [f"Assessment Guide {EXPECTED_VERSION}", EXPECTED_EDITION]),
        ("framework/shield-ai-implementation-architecture.md", [f"SHIELD-AI {EXPECTED_VERSION}"]),
        ("framework/shield-ai-tooling-map.md", [f"Tooling and Process Map {EXPECTED_VERSION}", EXPECTED_EDITION]),
        ("presentations/what-is-shield-ai.md", [f"SHIELD-AI {EXPECTED_VERSION}, {EXPECTED_EDITION}"]),
        ("presentations/glossary.md", [f"{EXPECTED_VERSION} edition, {EXPECTED_EDITION}"]),
    ]:
        if not os.path.exists(doc):
            check(f"{doc} exists", False)
            continue
        txt = open(doc, encoding="utf-8").read()
        check(f"{os.path.basename(doc)} source footer carries {markers}",
              all(m in txt for m in markers))
    wl_md = open("framework/shield-ai-watchlist.md", encoding="utf-8").read()
    check(f"watchlist.md edition line is current ({EXPECTED_EDITION})",
          EXPECTED_EDITION in wl_md)

    # 8b. Frontmatter edition dates match the current edition (regression guard,
    #     Aug 2026): the gap-analysis frontmatter drifted to the v1.7 date while
    #     its footer was correct, and the PDF title page rendered the stale date.
    #     Every doc carrying a current-state edition date must agree.
    for doc in [
        "framework/shield-ai-gap-analysis.md",
        "framework/shield-ai-tooling-map.md",
        "framework/shield-ai-framework.md",
        "framework/shield-ai-implementation-architecture.md",
        "presentations/what-is-shield-ai.md",
        "presentations/glossary.md",
        "assessment-guide/shield-ai-assessment-guide.md",
        "framework/shield-ai-reference-architecture-walkthrough.md",
        "framework/shield-ai-watchlist.md",
    ]:
        fd = frontmatter_date(doc)
        check(f"{os.path.basename(doc)} frontmatter date == {EXPECTED_EDITION} (found {fd})",
              fd == EXPECTED_EDITION)
    ga_src = open("framework/shield-ai-gap-analysis.md", encoding="utf-8").read()
    check(f"gap-analysis subtitle carries 'Updated {EXPECTED_EDITION}'",
          f"Updated {EXPECTED_EDITION}" in ga_src)
    ga_pdf = pdf_text("framework/shield-ai-gap-analysis.pdf")
    # Regression guard for a stale EDITION stamp (Aug 2026: the footer/title
    # drifted to the v1.7 edition date while the body was current). The raw date
    # now legitimately appears in the version-history table (v1.7 cycle), so
    # match the stale-edition FOOTER patterns, not the bare noun-phrase date.
    check("gap-analysis.pdf carries no stale v1.7 edition stamp",
          "Gap Analysis v1.7" not in ga_pdf and "v1.7 --" not in ga_pdf
          and "Updated August 17, 2026" not in ga_pdf)

    # 9. README freshness (keeps the repo index tidy): current version present
    #    and every relative markdown path in the README resolves to a file.
    readme = open("README.md", encoding="utf-8").read()
    check(f"README carries current version ({EXPECTED_VERSION})",
          EXPECTED_VERSION in readme)
    check(f"README carries current control count ({EXPECTED_COUNT} controls)",
          f"{EXPECTED_COUNT} controls" in readme)
    # Reject a stale control count asserted anywhere in a current-state doc
    # (README, ROADMAP, policies/README -- each states a single current number).
    # Catches the v1.18==67 / v1.20==69 drift that presence-of-correct-count
    # alone never failed on, and the ROADMAP/policies-README "59 of 69
    # implemented" lag that re-appeared after all controls were implemented.
    check_stale_control_counts("README.md", "README")
    check_stale_control_counts("ROADMAP.md", "ROADMAP")
    check_stale_control_counts("policies/README.md", "policies/README")

    # OPA test count in current-state docs must match the actual suite, so a
    # cycle that adds/removes controls can't leave a stale "N OPA tests" claim.
    actual_tests = count_opa_tests()
    check(f"computed OPA test count ({actual_tests}) is consistent with 'N OPA tests' claims",
          all(actual_tests == int(n) for n in
              re.findall(r"(\d+)\s+OPA tests?\b", open("ROADMAP.md", encoding="utf-8").read())
              + re.findall(r"(\d+)\s+OPA tests?\b", open("policies/README.md", encoding="utf-8").read())))

    # No current-state doc may claim any control is a stub/pending/non-implemented
    # while the policy set is fully implemented. A cycle that introduces a stub
    # must first face check_exploit_catalog's non-stub gate; this catches a doc
    # that re-opens the stub story in prose.
    stub_claims = re.findall(r"(?<!none\s)(?<!no\s)(?:ship|ships|remain|remains|are)\s+(?:as\s+)?(?:generated\s+)?stubs?\b",
                             open("policies/README.md", encoding="utf-8").read())
    stub_claims += re.findall(r"still\s+(?:pending|a stub|stubs)", open("policies/README.md", encoding="utf-8").read())
    check(f"policies/README asserts no stub/pending claims (found {len(stub_claims)})", not stub_claims)
    readme_links = re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", readme)
    broken = sorted(
        {p for p in readme_links
         if p.startswith(("./", "../")) and not os.path.exists(p)}
    )
    check(f"README relative links all resolve (broken: {broken})", not broken)

    print()
    # 10. Freshness: no derived artifact may be older than its source(s).
    #     Prevents committing an edited markdown/HTML/build script with a stale
    #     PDF/EPUB. Condition: artifact mtime >= MAX(source mtimes). Sources and
    #     artifacts mirror tools/build_docs.sh + the decktape deck chain, plus the
    #     published field-findings/case-study docs now also built there.

    def max_mtime(paths):
        return max(os.path.getmtime(p) for p in paths)

    # (artifact, [source...], build_script) — artifact must not predate any
    # source or its producing build script. Doc PDF/EPUB come from
    # tools/build_docs.sh; deck PDFs come from tools/update_all.sh (decktape).
    pairs = []
    DOC_BUILDER = "tools/build_docs.sh"
    DECK_BUILDER = "tools/update_all.sh"
    doc_srcs = [
        "framework/shield-ai-framework.md",
        "framework/shield-ai-gap-analysis.md",
        "assessment-guide/shield-ai-assessment-guide.md",
        "framework/shield-ai-implementation-architecture.md",
        "framework/shield-ai-watchlist.md",
        "framework/shield-ai-tooling-map.md",
        "framework/shield-ai-reference-architecture-walkthrough.md",
        "presentations/what-is-shield-ai.md",
        "presentations/glossary.md",
        "framework/shield-ai-field-findings.md",
        "case-studies/2026-08-reference-implementation.md",
    ]
    for md in doc_srcs:
        base = md[:-3]
        for ext in (".pdf", ".epub"):
            pairs.append((base + ext, [md], DOC_BUILDER))
    for review in sorted(__import__("glob").glob("framework/shield-ai-deep-review-*.md")):
        base = review[:-3]
        for ext in (".pdf", ".epub"):
            pairs.append((base + ext, [review], DOC_BUILDER))
    catalog_srcs = sorted(["exploits/README.md"] + __import__("glob").glob("exploits/g*.md"))
    pairs.append(("exploits/exploit-catalog.pdf", catalog_srcs, DOC_BUILDER))
    pairs.append(("exploits/exploit-catalog.epub", catalog_srcs, DOC_BUILDER))
    for deck in ["board-brief/shield-ai-deck-board", "business-deck/shield-ai-deck-business",
                 "buyers-journey-bridge/shield-ai-deck-bridge", "technical-deck/shield-ai-deck-technical"]:
        html = os.path.join("presentations", deck + ".html")
        pdf = os.path.join("presentations", deck + ".pdf")
        pairs.append((pdf, [html], DECK_BUILDER))

    for art, _srcs, builder in pairs:
        if not os.path.exists(art):
            check(f"{art} exists (missing artifact)", False)
            continue
        all_src = list(_srcs) + ([builder] if (os.path.exists(builder) and art.endswith((".pdf", ".epub"))) else [])
        srcs = [s for s in all_src if os.path.exists(s)]
        if not srcs:
            continue
        try:
            fresh = os.path.getmtime(art) >= max_mtime(srcs)
        except OSError:
            fresh = False
        if not fresh:
            newest = max(srcs, key=os.path.getmtime)
            check(f"{art} is not older than its sources (stale: {art} <- {newest})", fresh)
        else:
            check(f"{art} is not older than its sources", True)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("All artifact checks passed.")


if __name__ == "__main__":
    main()
