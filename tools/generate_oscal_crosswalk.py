#!/usr/bin/env python3
"""Build the SHIELD-AI -> NIST SP 800-53 Rev 5 OSCAL mapping collection.

Input : crosswalk/shield-ai-to-800-53r5.json   curated mappings (human-reviewed data)
        NIST SP 800-53 Rev 5.2 OSCAL catalog    fetched once to ~/.cache/shield-ai/
        assets/shield-ai-control-schema.json    SHIELD-AI controls
Output: oscal/shield-ai-to-800-53r5-mapping.json   OSCAL mapping-collection (v1.2.0)
        crosswalk/REPORT.md                         fit analysis

Hard checks (exit 1): every SHIELD id and 800-53 id resolves; relationship and
confidence values are legal; output validates against the NIST OSCAL mapping schema
(when jsonschema is installed). Mappings are never inferred here; this only
validates and serialises curated data.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.expanduser("~/.cache/shield-ai")
OSCAL_VERSION = "1.2.0"
NIST_CATALOG_URL = ("https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/"
                    "SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json")
NIST_HREF = NIST_CATALOG_URL
MAP_SCHEMA_URL = f"https://github.com/usnistgov/OSCAL/releases/download/v{OSCAL_VERSION}/oscal_mapping_schema.json"
NS_URI = "https://github.com/monch1962/shield-ai/ns/oscal"
_UUID_NS = uuid.UUID("6f0b1c52-5a1e-4c1a-9a55-5a1e1d0a0001")
RELS = {"equivalent-to", "equal-to", "subset-of", "superset-of", "intersects-with", "no-relationship"}
CONFS = {"high", "medium", "low", "unspecified"}
FITS = ("direct", "partial", "novel")


def uid(*p):
    return str(uuid.uuid5(_UUID_NS, "/".join(p)))


def fetch(url, dest):
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        print(f"fetching {url}", file=sys.stderr)
        urllib.request.urlretrieve(url, dest)
    return dest


def load_800_53():
    cat = json.load(open(fetch(NIST_CATALOG_URL, os.path.join(CACHE, "nist-800-53r5-catalog.json"))))["catalog"]
    idx, withdrawn = {}, {}

    def walk(cs):
        for c in cs:
            idx[c["id"]] = c["title"]
            if any(p["name"] == "status" and p["value"] == "withdrawn" for p in c.get("props", [])):
                withdrawn[c["id"]] = [l["href"].lstrip("#") for l in c.get("links", [])
                                      if l.get("rel") in ("moved-to", "incorporated-into")]
            walk(c.get("controls", []))
    for g in cat["groups"]:
        walk(g.get("controls", []))
    return idx, withdrawn, cat["metadata"].get("version", "?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stamp", default=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat())
    a = ap.parse_args()

    cw = json.load(open(os.path.join(ROOT, "crosswalk", "shield-ai-to-800-53r5.json")))
    src = json.load(open(os.path.join(ROOT, "assets", "shield-ai-control-schema.json")))
    nist, withdrawn, nist_ver = load_800_53()

    errors = []
    maps = []
    for cid, e in cw["controls"].items():
        if cid not in src["controls"]:
            errors.append(f"{cid}: not a SHIELD-AI control")
            continue
        if e["fit"] not in FITS:
            errors.append(f"{cid}: bad fit {e['fit']!r}")
        if e["fit"] != "direct" and not e.get("residual"):
            errors.append(f"{cid}: fit={e['fit']} requires a residual statement")
        quals = {}
        for q in e.get("qualifiers", []):
            quals.setdefault(q["on"], []).append(q)
        mapped_targets = {m["t"] for m in e["mappings"]}
        for q in quals:
            if q not in mapped_targets:
                errors.append(f"{cid}: qualifier on {q} which is not a mapping target")
        for m in e["mappings"]:
            t = m["t"]
            if t not in nist:
                errors.append(f"{cid}: 800-53 id {t!r} not in Rev {nist_ver} catalog")
            if t in withdrawn:
                errors.append(f"{cid}: 800-53 id {t!r} is WITHDRAWN (see {withdrawn[t] or 'no successor listed'})")
            if m["rel"] not in RELS:
                errors.append(f"{cid}->{t}: bad relationship {m['rel']!r}")
            if m["conf"] not in CONFS:
                errors.append(f"{cid}->{t}: bad confidence {m['conf']!r}")
            entry = {
                "uuid": uid("map", cid, t), "relationship": m["rel"],
                "sources": [{"type": "control", "id-ref": cid.lower()}],
                "targets": [{"type": "control", "id-ref": t}],
                # OSCAL JSON form of confidence-score requires STRVALUE alongside category
                "confidence-score": {"category": m["conf"], "STRVALUE": m["conf"]},
                "remarks": m["why"],
            }
            if t in quals:
                entry["qualifiers"] = [{"subject": q["subject"], "predicate": q["predicate"],
                                        "category": q["category"], "description": q["description"]}
                                       for q in quals[t]]
            maps.append(entry)
    for t in cw.get("findings", []):
        for ref in re.findall(r"\b(?:MS|IAM|DS|TP|MIR|GRM|EE)-\d{2}\b", t):
            if ref not in src["controls"]:
                errors.append(f"findings cite unknown SHIELD-AI control {ref}")
            elif ref not in cw["controls"]:
                errors.append(f"findings cite {ref} which is not mapped in this crosswalk")
    if errors:
        print("ERRORS:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1

    order = list(src["pillars"])
    scope = [p for p in order if any(c.startswith(p + "-") for c in cw["controls"])]
    scope_txt = ", ".join(scope[:-1]) + " and " + scope[-1] if len(scope) > 1 else scope[0]
    mapped_src = {m["sources"][0]["id-ref"] for m in maps}
    all_src = [c.lower() for p in src["pillars"].values() for c in p["control_ids"]]
    unmapped = [c for c in all_src if c not in mapped_src]
    # no-relationship entries are not coverage; drop them when counting mapped sources
    covering = {m["sources"][0]["id-ref"] for m in maps if m["relationship"] != "no-relationship"}

    doc = {"mapping-collection": {
        "uuid": uid("mapping-collection"),
        "metadata": {"title": f"SHIELD-AI to NIST SP 800-53 Rev 5 (DRAFT, {scope_txt} pillars)",
                     "last-modified": a.stamp, "version": f"{src['meta']['version']}-draft",
                     "oscal-version": OSCAL_VERSION,
                     "remarks": "AI-assisted draft. Not reviewed by a control SME. See crosswalk/REPORT.md for fit and residuals."},
        "provenance": {
            "method": "hybrid", "matching-rationale": "functional", "status": "draft",
            "mapping-description": (
                "Functional mapping (NIST IR 8477) from SHIELD-AI controls to SP 800-53 Rev "
                f"{nist_ver}. Scope: {scope_txt} pillars ({len(cw['controls'])} of {len(all_src)} controls). "
                "One map entry per control pair so each relationship and confidence is individually reviewable. "
                "Targets are base controls or enhancements, mapped at control level, not statement level."),
            "props": [{"name": "fit-summary", "ns": NS_URI,
                       "value": json.dumps(collections.Counter(e["fit"] for e in cw["controls"].values()), sort_keys=True)}]},
        "mappings": [{
            "uuid": uid("mapping"), "method": "hybrid", "matching-rationale": "functional", "status": "draft",
            "source-resource": {"type": "catalog", "href": "shield-ai-catalog.json"},
            "target-resource": {"type": "catalog", "href": NIST_HREF},
            "maps": maps,
            "source-gap-summary": {"uuid": uid("gap", "source"),
                                   "unmapped-controls": [{"with-child-controls": "no", "with-ids": unmapped}]}}]}}
    out = os.path.join(ROOT, "oscal", "shield-ai-to-800-53r5-mapping.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(doc, open(out, "w"), indent=2)
    open(out, "a").write("\n")

    # ---- schema validation ----
    try:
        import jsonschema
        sp = fetch(MAP_SCHEMA_URL, os.path.join(CACHE, f"oscal_mapping_schema_v{OSCAL_VERSION}.json"))
        txt = open(sp).read().replace("\\\\p{L}", "[A-Za-z\\u00C0-\\uFFFF]").replace("\\\\p{N}", "[0-9]")
        errs = list(jsonschema.Draft7Validator(json.loads(txt)).iter_errors(doc))
        if errs:
            print(f"SCHEMA INVALID ({len(errs)}):", file=sys.stderr)
            for e in errs[:8]:
                print("  ", list(e.absolute_path)[-6:], e.message[:200], file=sys.stderr)
            return 1
        print("schema: VALID against OSCAL mapping v" + OSCAL_VERSION)
    except ImportError:
        print("schema: SKIPPED (pip install jsonschema)", file=sys.stderr)

    write_report(cw, src, nist, nist_ver, maps, unmapped, covering, a.stamp, scope, scope_txt)
    print(f"wrote {os.path.relpath(out, ROOT)}: {len(maps)} map entries over {len(cw['controls'])} controls "
          f"(800-53 Rev {nist_ver})")
    return 0


def write_report(cw, src, nist, nist_ver, maps, unmapped, covering, stamp, scope, scope_txt):
    L = []
    ctrls = cw["controls"]
    fits = collections.Counter(e["fit"] for e in ctrls.values())
    n = len(ctrls)
    L += ["# SHIELD-AI to NIST SP 800-53 Rev 5: crosswalk fit report", "",
          f"Generated {stamp[:10]} by `tools/generate_oscal_crosswalk.py` from `crosswalk/shield-ai-to-800-53r5.json`. "
          f"Target catalog: SP 800-53 Rev {nist_ver}. **Status: DRAFT, not SME-reviewed.**", "",
          f"Scope: {scope_txt} pillars, {n} of {sum(len(p['control_ids']) for p in src['pillars'].values())} controls.", "",
          "## Headline", "",
          "| Fit | Controls | Meaning |", "|---|---|---|"]
    for f in FITS:
        L.append(f"| {f} | {fits.get(f, 0)} | {cw['_fit_values'][f]} |")
    L += ["", f"Every one of the {n} controls has at least one 800-53 neighbour "
          f"({len(covering & {c.lower() for c in ctrls})} of {n}), so none is wholly orphaned. "
          "That is a weak result by itself: 800-53 is broad enough that something always loosely applies. "
          "The fit column is the meaningful one.", ""]
    rels = collections.Counter(m["relationship"] for m in maps)
    confs = collections.Counter(m["confidence-score"]["category"] for m in maps)
    L += ["## Mapping-level statistics", "",
          f"- {len(maps)} map entries. Relationships: " + ", ".join(f"{k} {v}" for k, v in sorted(rels.items())) + ".",
          f"- Confidence: " + ", ".join(f"{k} {confs.get(k, 0)}" for k in ("high", "medium", "low")) + ".",
          f"- {rels.get('intersects-with', 0)} of {len(maps)} entries are `intersects-with` (each side has content the other lacks); "
          f"{rels.get('subset-of', 0)} are `subset-of`; "
          f"{rels.get('equal-to', 0) + rels.get('equivalent-to', 0)} are `equal-to`/`equivalent-to`.", ""]
    hi = sum(1 for e in ctrls.values() if any(m["conf"] == "high" for m in e["mappings"]))
    L += [f"- {hi} of {n} controls have at least one high-confidence mapping. "
          f"{n - hi} rest on medium or low confidence alone.", ""]

    L += ["## By pillar", "", "| Pillar | Direct | Partial | Novel |", "|---|---|---|---|"]
    for pid in scope:
        pc = collections.Counter(e["fit"] for c, e in ctrls.items() if c.startswith(pid + "-"))
        L.append(f"| {pid} | {pc.get('direct', 0)} | {pc.get('partial', 0)} | {pc.get('novel', 0)} |")

    L += ["", "## Per-control result", "", "| SHIELD-AI | Title | Fit | 800-53 targets (conf.) |", "|---|---|---|---|"]
    for cid, e in ctrls.items():
        tg = ", ".join(f"{m['t'].upper()} ({m['conf'][0].upper()})" for m in e["mappings"] if m["rel"] != "no-relationship")
        L.append(f"| {cid} | {src['controls'][cid]['title']} | **{e['fit']}** | {tg} |")
    L += ["", "Confidence: H high, M medium, L low.", ""]

    L += ["## Residuals: what 800-53 does not cover", "",
          "For every control not rated `direct`, this is the requirement an 800-53-only organisation would still be missing.", ""]
    for cid, e in ctrls.items():
        if e["fit"] != "direct":
            L += [f"- **{cid} ({e['fit']})**: {e['residual']}"]
    L += ["", "## Findings", ""]
    L += findings(ctrls, maps, rels, cw.get("findings", []))
    L += ["", "## Method and limits", "",
          "- Matching rationale `functional` (NIST IR 8477): compares what the controls do, not their wording.",
          "- Mapped at control level. NIST recommends statement level; control-level mappings are coarser and will over-state overlap.",
          "- Each 800-53 ID was checked to exist in the Rev " + nist_ver + " catalog; the generator fails on a miss. "
          "That proves the ID exists, not that the mapping is sound.",
          "- 800-53 statements were read from the catalog for the candidate targets. "
          "Many have unfilled organisation-defined parameters (ODPs), so 'direct' assumes sensible ODP values.",
          "- Ratings are one analyst's judgement, AI-assisted. They need review by someone who has assessed against 800-53.",
          "- Out of scope: the pillars not listed above; the NIST COSAIS/COSIS agent overlays; "
          "800-53 baselines (low/moderate/high), which would change what 'covered' means in practice.", ""]
    open(os.path.join(ROOT, "crosswalk", "REPORT.md"), "w").write("\n".join(L))


def findings(ctrls, maps, rels, curated):
    """Computed bullets first (numbers derived from data), then curated prose from the data file.
    Curated text must not quote counts; they would drift."""
    by = {f: [c for c, e in ctrls.items() if e["fit"] == f] for f in FITS}
    eq = rels.get("equal-to", 0) + rels.get("equivalent-to", 0)
    out = [f"1. **Fit (computed).** Direct {len(by['direct'])}: {', '.join(by['direct']) or 'none'}. "
           f"Partial {len(by['partial'])}. Novel {len(by['novel'])}: {', '.join(by['novel']) or 'none'}.",
           f"2. **Equality (computed).** {eq} of {len(maps)} map entries are `equal-to`/`equivalent-to`; "
           f"{rels.get('subset-of', 0)} are `subset-of`. A compliance team cannot treat 'satisfies 800-53 control X' "
           "as 'satisfies SHIELD-AI control Y' for the partial and novel controls."]
    out += [f"{n}. {t}" for n, t in enumerate(curated, start=3)]
    return out


if __name__ == "__main__":
    sys.exit(main())
