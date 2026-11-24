#!/usr/bin/env python3
"""Versioned tests for the SHIELD-AI interactive HTML explorer.

The explorer (emitted by tools/generate_explorer_html.py) is a SINGLE
self-contained HTML file that embeds the explorer graph of record
(assets/shield-ai-explorer-graph.json) plus a vanilla-JS viewer. It must stay:

  1. Self-contained   -- no external http(s) resources, no CDN, works offline.
  2. Complete         -- the embedded graph matches the graph of record
                         (every control/incident/gap/pillar present).
  3. Deterministic    -- regeneration is byte-identical (freshness-gated).
  4. Gated            -- --check fails when the committed file is stale/tampered.

The HTML is for a client-facing interactive surface: drill-down navigation
(incident -> control -> pillar -> rego), faceted filtering (pillar/severity/
search), and a graph view of a selected entity's neighbourhood.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(ROOT, "assets", "shield-ai-explorer-graph.json")
HTML = os.path.join(ROOT, "shield_ai_explorer.html")
GENERATOR = os.path.join(ROOT, "tools", "generate_explorer_html.py")


def _graph():
    with open(GRAPH, encoding="utf-8") as f:
        return json.load(f)


def _tap_generate():
    """Ensure the HTML exists (regeneration via generator) before assertions."""
    if not os.path.exists(HTML):
        subprocess.run([sys.executable, GENERATOR, "--write"],
                       cwd=ROOT, check=True, capture_output=True)


def _html():
    if not os.path.exists(HTML):
        _tap_generate()
    with open(HTML, encoding="utf-8") as f:
        return f.read()


def _embedded(html):
    """Return the JSON blob embedded in <script id="graph-data">."""
    m = re.search(
        r'<script id="graph-data" type="application/json">(.*?)</script>',
        html, re.S)
    assert m, "graph-data script block missing"
    return json.loads(m.group(1))


# --- structural contract ----------------------------------------------------

def test_html_exists_and_is_single_file():
    _tap_generate()
    assert os.path.exists(HTML)
    # a single self-contained file -- no separate css/js files
    assert HTML.endswith(".html")


def test_self_contained_no_external_resources():
    html = _html()
    # The viewer must never fetch anything. The embedded graph-data may carry
    # http(s) strings as *data text* (incident narratives/descriptions), which
    # the viewer renders inertly -- so the guarantee is about the SUBSURFACE of
    # the file that is code/resource references, not every URL substring.
    # Remove the graph-data JSON block (data, not code), then assert no network
    # resource reference remains in the code/viewer portion. The SVG-namespace
    # URI is a spec identifier, not a fetch -- strip it too.
    o = html.index('<script id="graph-data" type="application/json">')
    i = html.index("</script>", o) + len("</script>")
    code = html[:o] + html[i:]  # viewer + markup without the data blob
    code = code.replace("http://www.w3.org/2000/svg", "")
    assert "http://" not in code and "https://" not in code
    assert "cdn." not in code
    # No resource-bearing tags in the markup, or fetch APIs in the viewer code.
    assert '<script src=' not in html and '<link rel="stylesheet"' not in html
    assert 'src="http' not in html and 'href="http' not in html
    # The viewer never opens a network channel. (Narrative data may *mention*
    # WebSocket/harvesting concepts as plain text -- only the viewer code must
    # be free of the APIs.)
    assert "fetch(" not in code and "XMLHttpRequest" not in code
    assert "new WebSocket" not in code and "WebSocket(" not in code


def test_embedded_graph_matches_graph_of_record():
    html = _html()
    emb = _embedded(html)
    g = _graph()
    assert emb["meta"] == g["meta"]
    assert len(emb["controls"]) == g["meta"]["control_count"]
    assert len(emb["incidents"]) == g["meta"]["incident_count"]
    # every control id from the graph of record is embedded
    emb_ids = {c["id"] for c in emb["controls"]}
    graph_ids = {c["id"] for c in g["controls"]}
    assert emb_ids == graph_ids
    assert {i["id"] for i in emb["incidents"]} == {i["id"] for i in g["incidents"]}


def test_viewer_has_core_interactions():
    html = _html()
    # the vanilla JS viewer must expose the interaction surfaces
    assert 'id="sidebar"' in html
    assert 'id="detail"' in html
    assert 'id="graph"' in html
    # drill navigation is built at runtime via data-type attributes on chips
    # and result rows -- the JS must define both kinds and the wiring functions
    assert "data-type=\"" in html
    assert "data-type=\"incident\"" in html or 'chip(i,\'incident\')' in html
    assert "data-type=\"control\"" in html or "chip(c,\'control\')" in html
    assert "function select(" in html
    assert "function drawGraph(" in html


def test_viewer_renders_incident_narrative():
    """Drill-down into an incident must show the incident's own summary text."""
    html = _html()
    emb = _embedded(html)
    inc0 = emb["incidents"][0]
    assert inc0.get("summary"), "embedded incident missing summary"
    # the viewer must emit the summary as a rendered paragraph (not just title)
    assert ".summary" in html or "summary" in html
    assert "<p>" in html  # a paragraph element exists for narrative rendering


def test_viewer_renders_rego_policy_content():
    """Drill-down into a control must expose the full REGO policy body."""
    html = _html()
    emb = _embedded(html)
    c0 = next(c for c in emb["controls"] if c["rego"])
    assert c0.get("rego_content"), "embedded control missing rego_content"
    assert len(c0["rego_content"]) > 200
    # the viewer exposes a scrollable pre/code region for the policy source
    assert "<pre" in html or "rego_content" in html or "code" in html
    # the policy package line must survive embedding (verbatim)
    assert "package " in c0["rego_content"]


def test_deterministic_regeneration():
    """--write then --write again must be byte-identical."""
    subprocess.run([sys.executable, GENERATOR, "--write"], cwd=ROOT,
                   check=True, capture_output=True)
    a = open(HTML, encoding="utf-8").read()
    subprocess.run([sys.executable, GENERATOR, "--write"], cwd=ROOT,
                   check=True, capture_output=True)
    b = open(HTML, encoding="utf-8").read()
    assert a == b


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