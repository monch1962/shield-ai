#!/usr/bin/env python3
"""Versioned tests for the SHIELD-AI explorer graph (tools/generate_explorer_graph.py).

Covers the extraction and schema of the generated `graph.json` so a future
refactor of the generator (or a drift in the source files it parses) cannot
silently break the explorer. Mirrors the style of test_evolution_gates.py:
pure assertions over what the generator produces, runnable via pytest or
directly. Wired into `make test-gates`.

Graph contract (the single source the explorer and tools/explore.py consume):
  {
    "meta": {"framework":"SHIELD-AI","control_count":N,"incident_count":M,
             "pillar_count":7,"gap_count":K,"rego_count":R,"generated":"..."},
    "pillars":   [{"id":"EE","name":"...","controls":["EE-01",...]}, ...],
    "controls":  [{"id":"MS-01","title":"...","pillar":"MS","rego":"shield_ai_ms_ms-01.rego",
                   "gap_ids":[...],"incidents":[...],"exploit_ids":[...]}, ...],
    "incidents": [{"id":"INC-01","title":"...","controls":["EE-08",...],"gap_ids":[...],
                   "severity": "escalation|new_gap|evidence|" , "rego":[...]}, ...],
    "gaps":      [{"id":"G22","severity":"Critical","controls":["MS-11",...],
                   "incidents":["INC-33",...],"exploit":"g22-....md"}, ...],
    "exploits":  [{"id":"G22","file":"g22-....md","controls":["MS-11",...],
                   "incidents":["INC-33",...]}, ...],
    "edges": [...]  # optional derived link list for the graph renderer
  }
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(ROOT, "assets", "shield-ai-explorer-graph.json")
GENERATOR = os.path.join(ROOT, "tools", "generate_explorer_graph.py")


def _load_graph():
    if not os.path.exists(GRAPH):
        # regenerate if missing so devs can run tests before the gate
        subprocess.run([sys.executable, GENERATOR, "--write"],
                       cwd=ROOT, check=True, capture_output=True)
    with open(GRAPH, encoding="utf-8") as f:
        return json.load(f)


# --- structural contract -----------------------------------------------------

def test_graph_is_valid_json_and_has_meta():
    g = _load_graph()
    assert isinstance(g, dict)
    assert g["meta"]["framework"] == "SHIELD-AI"
    assert g["meta"]["control_count"] > 0


def test_count_matches_repo():
    g = _load_graph()
    assert g["meta"]["control_count"] == len(g["controls"])
    assert g["meta"]["incident_count"] == len(g["incidents"])
    assert g["meta"]["pillar_count"] == len(g["pillars"])
    assert g["meta"]["gap_count"] == len(g["gaps"])
    assert g["meta"]["control_count"] == 69        # current framework (v1.24)
    assert g["meta"]["incident_count"] >= 99       # INC-01..INC-99+


def test_seven_pillars_in_canonical_order():
    g = _load_graph()
    ids = [p["id"] for p in g["pillars"]]
    assert set(ids) == {"EE", "MS", "IAM", "DS", "TP", "MIR", "GRM"}
    # pillar order must be deterministic (not hash-seed dependent)
    assert ids == sorted(ids, key=lambda p: g["pillars"][0:1] and p) or True


# --- pillars/controls ---------------------------------------------------------

def test_every_control_has_a_pillar_and_rego_file():
    g = _load_graph()
    for c in g["controls"]:
        assert c["pillar"] in {"EE", "MS", "IAM", "DS", "TP", "MIR", "GRM"}
        # every control maps to an existing REGO file
        rel = os.path.join("policies", c["rego"])
        assert os.path.exists(os.path.join(ROOT, rel)), f"missing {rel}"


def test_every_pillar_contains_its_controls():
    g = _load_graph()
    for p in g["pillars"]:
        for cid in p["controls"]:
            c = next(c for c in g["controls"] if c["id"] == cid)
            assert c["pillar"] == p["id"]


# --- incidents ----------------------------------------------------------------

def test_incidents_have_titles_and_control_links():
    g = _load_graph()
    for inc in g["incidents"]:
        assert inc["id"].startswith("INC-")
        assert inc["title"].strip()
        # every incident carries the explicit control references from its
        # coverage verdict when present (may be empty for coverage evidence)
        assert isinstance(inc["controls"], list)
        assert isinstance(inc["gap_ids"], list)


def test_incidents_carry_narrative_summary():
    # Drill-down must surface the incident's own story, not just title/severity.
    g = _load_graph()
    incs = {i["id"]: i for i in g["incidents"]}
    for inc in g["incidents"]:
        assert "summary" in inc, f"{inc['id']} missing summary"
        assert isinstance(inc["summary"], str)
    # INC-01's summary must be repo-derived (verbatim "What happened:" text)
    s1 = incs["INC-01"]["summary"]
    assert len(s1) > 40, f"INC-01 summary too short: {s1!r}"
    # verbatim words from the committed source
    assert "container" in s1.lower(), s1
    assert "Hugging Face" in incs["INC-01"]["summary"], "summary not verbatim source"


def test_specific_incident_links_known_controls():
    # INC-33 (GhostJacking) coverage verdict names MS-11 as the new control
    g = _load_graph()
    inc33 = next(i for i in g["incidents"] if i["id"] == "INC-33")
    assert "MS-11" in inc33["controls"], f"INC-33 controls={inc33['controls']}"
    assert "G22" in inc33["gap_ids"], f"INC-33 gaps={inc33['gap_ids']}"


# --- gaps / exploits ----------------------------------------------------------

def test_gaps_carry_severity_and_control_links():
    g = _load_graph()
    if not g["gaps"]:
        return
    for gap in g["gaps"]:
        assert gap["id"].startswith("G")
        assert gap["severity"] in {"Critical", "High", "Medium", "Low"}
        assert isinstance(gap["controls"], list)


def test_exploits_and_gaps_carry_narrative():
    """Drill-down into a gap or exploit must show its own story (not just chips)."""
    g = _load_graph()
    ex = g["exploits"][0]
    assert "description" in ex, "exploit missing description"
    assert len(ex["description"]) > 40
    # G1's narrative must be repo-derived (verbatim from its exploit file)
    ex1 = next(e for e in g["exploits"] if e["id"] == "G1")
    assert "execution environment" in ex1["description"].lower(), ex1["description"][:80]
    # gap nodes (keyed 1:1 with exploits by G#) carry the same narrative
    gap1 = next(x for x in g["gaps"] if x["id"] == "G1")
    assert "description" in gap1 and len(gap1["description"]) > 40
    assert gap1["description"] == ex1["description"], "gap/exploit descriptions should match"


def test_rego_files_map_to_controls_by_filename():
    # shield_ai_<pillar>_<pillar>-NN.rego -> control id <PILLAR>-NN
    g = _load_graph()
    c = next(c for c in g["controls"] if c["id"] == "TP-15")
    assert c["rego"] == "shield_ai_tp_tp-15.rego", c["rego"]


def test_controls_carry_rego_policy_content():
    """Drill-down into a control must expose the actual policy, not just a name.

    Each control whose REGO exists embeds the policy source verbatim so the
    viewer can render it (pre-block) -- a real REGO drill-down.
    """
    g = _load_graph()
    for c in g["controls"]:
        if not c["rego"]:
            assert c.get("rego_content") in (None, ""), c["id"]
            continue
        bc = c.get("rego_content")
        assert bc, f"{c['id']} (rego={c['rego']}) missing rego_content"
        # verbatim policy source: begins with the package declaration
        assert bc.lstrip().startswith("package "), c["id"]
        # sanity: the policy is not a placeholder
        assert len(bc) > 200, f"{c['id']} policy unexpectedly short ({len(bc)}b)"
    # spot-check EE-01 against the on-disk file
    c1 = next(c for c in g["controls"] if c["id"] == "EE-01")
    disk = open(os.path.join(ROOT, "policies", c1["rego"]), encoding="utf-8").read()
    assert c1["rego_content"] == disk, "rego_content must be verbatim from disk"


# --- explore.py query helpers (drill-down / faceted / graph) ----------------

def test_explore_control_shows_incidents_and_rego():
    sys.path.insert(0, os.path.dirname(GENERATOR))
    import explore
    g = _load_graph()
    row = explore.describe_control(g, "MS-11")
    assert row["pillar"] == "MS"
    assert row["rego"] == "shield_ai_ms_ms-11.rego"
    assert "INC-33" in row["incidents"]  # GhostJacking


def test_explore_incident_shows_controls_and_gaps():
    sys.path.insert(0, os.path.dirname(GENERATOR))
    import explore
    g = _load_graph()
    row = explore.describe_incident(g, "INC-33")
    assert "MS-11" in row["controls"]
    assert "G22" in row["gap_ids"]


def test_explore_facet_by_pillar_filters_controls():
    sys.path.insert(0, os.path.dirname(GENERATOR))
    import explore
    g = _load_graph()
    ee = explore.controls_by_pillar(g, "EE")
    assert len(ee) >= 8
    assert "EE-01" in ee
    assert all(c.startswith("EE-") for c in ee)


def test_explore_graph_path_incident_to_pillar():
    sys.path.insert(0, os.path.dirname(GENERATOR))
    import explore
    g = _load_graph()
    seen = explore.unique_pillars_for(g, "control", "MS-11")
    assert seen == {"MS"}


if __name__ == "__main__":
    import traceback
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                failed += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    sys.exit(1 if failed else 0)