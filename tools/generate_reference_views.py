#!/usr/bin/env python3
"""
SHIELD-AI Reference Views Generator
===================================
Generates the simplified, cross-cutting reference views for the SHIELD-AI
framework: (1) pillar -> control atlas, (2) control -> incident map,
(3) control -> Australian framework matrix, (4) pillar -> maturity heat grid.

Every number is DERIVED at generation time from the committed sources so the
views can never drift from the framework:

  * control IDs / titles / per-pillar counts  -> tools/control_metadata.py
  * incident -> control coverage counts        -> framework/shield-ai-gap-analysis.md
  * pillar -> AU framework mappings            -> framework/shield-ai-framework.md
  * pillar -> L1-L4 maturity progression       -> framework/shield-ai-framework.md

Output:
  assets/diagrams/pillar-control-atlas.svg
  assets/diagrams/controls-incident-map.svg
  assets/diagrams/control-au-framework-matrix.svg
  assets/diagrams/pillar-maturity-heat.svg
  reference-views/01-pillar-control-atlas.md
  reference-views/02-controls-incidents.md
  reference-views/03-control-au-framework-matrix.md
  reference-views/04-pillar-maturity.md
  reference-views/05-controls-outcomes.md
  reference-views/06-controls-technical.md
  reference-views/README.md

Usage:
  python3 tools/generate_reference_views.py
  python3 tools/generate_reference_views.py --check   # verify outputs exist
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from control_metadata import control_ids, count_controls, pillar_ranges

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DIAG_DIR = os.path.join(REPO_ROOT, "assets", "diagrams")
VIEW_DIR = os.path.join(REPO_ROOT, "reference-views")

FRAMEWORK = os.path.join(REPO_ROOT, "framework", "shield-ai-framework.md")
GAP = os.path.join(REPO_ROOT, "framework", "shield-ai-gap-analysis.md")

# ── Colours (match generate_diagrams.py so the family looks consistent) ──
NAVY = "#0a1e3d"; BLUE = "#1a3a6b"; GOLD = "#d4a017"
LTBL = "#dce6f0"; WHITE = "#ffffff"; TEXT = "#1a1a2e"; MUTED = "#5a6a8a"
GREEN = "#22c55e"; AMBER = "#f59e0b"; RED = "#ef4444"

PILLARS = ["EE", "MS", "IAM", "DS", "TP", "MIR", "GRM"]
PILLAR_FULL = {
    "EE": "Execution Environment", "MS": "Model Security", "IAM": "Identity & Access",
    "DS": "Data Security", "TP": "Tool & Pipeline Security",
    "MIR": "Monitoring, Logging & IR", "GRM": "Governance & Risk",
}

# ── Data loading ─────────────────────────────────────────────────────────


def load_control_titles():
    """{control_id: title} from the framework's '- ID: title' bullets."""
    txt = open(FRAMEWORK, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^- ([A-Z]{2,5}-\d{2}):\s*(.+)$", txt, re.M):
        title = re.split(r"\s*\(", m.group(2), maxsplit=1)[0].strip()
        # strip any leading structural label left by the layout pass. The source
        # bold can be "**Requirement:**<space>title" (colon INSIDE the bold) or
        # "**Requirement**:<space>title" (colon after), so accept both.
        title = re.sub(r"^\*\*(Requirement|Implementation|Rationale[^:]*|Mappings)\*?\*?\s*:\s*\**", "", title)
        title = title.strip(" *")
        out[m.group(1)] = title
    return out


def load_short_titles():
    """{control_id: clean short title} from the framework's AU-mapping table.

    Some 'ID: title' bullets carry the full requirement sentence (MIR-02,
    MIR-04); the mapping table in the same committed file always names the
    control tersely, so use that as the display title where a bullet title
    looks like a requirement sentence (contains ';' or ' -- ').
    """
    txt = open(FRAMEWORK, encoding="utf-8").read()
    short = {}
    for m in re.finditer(r"\|\s*\*\*([A-Z]{2,5}-\d{2}):\s*([^|*]+?)\*\*\s*\|", txt):
        short[m.group(1)] = m.group(2).strip()
    return short


def display_title(cid):
    """The short display title for a control page/heading.

    Uses the framework's own terser mapping-table name when the bullet title
    is a requirement sentence; otherwise the bullet title itself.
    """
    t = load_control_titles()
    base = t.get(cid, "")
    if ";" in base or " -- " in base:
        s = load_short_titles().get(cid, "")
        if s:
            return s
        # fall back to the first clause of the requirement sentence
        return re.split(r";|--", base)[0].strip().rstrip()
    return base


def load_incident_coverage():
    """{control_id: number of references across all incident coverage verdicts}."""
    txt = open(GAP, encoding="utf-8").read()
    counts = {}
    for m in re.finditer(r"\b((?:EE|MS|IAM|DS|TP|MIR|GRM)-\d{2})\b", txt):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    for cid in control_ids():
        counts.setdefault(cid, 0)
    return counts


def load_pillar_au_mappings():
    """{pillar: AU framework mapping text} from '**AU framework mappings:**'."""
    txt = open(FRAMEWORK, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^### Pillar \d: .*?\(([A-Z]{2,5})\)", txt, re.M):
        code = m.group(1)
        tail = txt[m.end():]
        mm = re.search(r"\*\*AU framework mappings:\*\*(.*?)(?=\n## |\n### Pillar |\n# )", tail, re.S)
        if mm:
            out[code] = " ".join(mm.group(1).split()).strip()
    return out


def load_maturity():
    """{pillar: {L1..L4 description}} from the maturity progression table."""
    txt = open(FRAMEWORK, encoding="utf-8").read()
    i = txt.find("### Maturity Progression by Pillar")
    seg = txt[i:i + 2600]
    rows = re.findall(
        r"\|\s*([MS]{2}|IAM|DS|TP|MIR|GRM|EE)\s*\([^)]+\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        seg)
    return {r[0]: {"L1": r[1].strip(), "L2": r[2].strip(), "L3": r[3].strip(), "L4": r[4].strip()} for r in rows}


# ── SVG helpers (mirror generate_diagrams.py) ───────────────────────────


def svg(w, h, body):
    body = body.replace("&", "&amp;").replace("&lt;", "&lt;").replace("&gt;", "&gt;")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <style>
    text {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
    .title {{ font-size: 15px; font-weight: bold; fill: {NAVY}; }}
    .label {{ font-size: 11px; fill: {TEXT}; }}
    .sm {{ font-size: 9px; fill: {MUTED}; }}
    .cap {{ font-size: 8px; font-weight: bold; text-transform: uppercase; fill: {MUTED}; }}
    .white {{ fill: #ffffff; }}
  </style>
  {body}
</svg>'''


def group_title(body, w, text):
    return f'''<text x="{w/2}" y="24" text-anchor="middle" class="title">{text}</text>
    {body}'''


# ── Diagram 1: Pillar -> Control Atlas (7 coloured rings + count) ────────


def diagram_pillar_atlas():
    """Seven-pillar atlas: each pillar's controls stacked numerically under its
    column, each control box sized to fit its full title (no truncation), with
    canvas height computed from the tallest column so nothing clips."""
    import textwrap
    titles = load_control_titles()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    w = 1180
    x0 = 30
    col_w = 150
    gap = 14
    top_h = 66
    row_gap = 6
    wrap_w = 26
    by = {}
    for p in PILLARS:
        ids = [c for c in control_ids() if c.startswith(p)]
        ids.sort(key=lambda s: int(s.split("-")[1]))
        by[p] = ids
    plan = {}
    for p in PILLARS:
        for cid in by[p]:
            title = titles.get(cid, "")
            wrapped = textwrap.wrap(title, width=wrap_w,
                                    break_on_hyphens=False, break_long_words=False) or [""]
            plan[cid] = (wrapped, len(wrapped))
    parts = []
    for idx, p in enumerate(PILLARS):
        px = x0 + idx * (col_w + gap)
        cx = px + col_w / 2.0
        n = len(by[p])
        parts.append(f'<rect x="{px}" y="38" width="{col_w}" height="{top_h}" rx="8" fill="{col[p]}" opacity="0.12"/>')
        parts.append(f'<rect x="{px}" y="38" width="{col_w}" height="26" rx="8" fill="{col[p]}"/>')
        parts.append(f'<text x="{cx}" y="55" text-anchor="middle" class="white" font-size="11" font-weight="bold">{p}</text>')
        parts.append(f'<text x="{cx}" y="72" text-anchor="middle" class="label" font-weight="bold" fill="{col[p]}">{n} controls</text>')
        parts.append(f'<text x="{cx}" y="88" text-anchor="middle" class="sm">{PILLAR_FULL[p]}</text>')
    for idx, p in enumerate(PILLARS):
        px = x0 + idx * (col_w + gap)
        y = 38 + top_h + 10
        for cid in by[p]:
            wrapped, nlines = plan[cid]
            bh = 26 + nlines * 11
            parts.append(f'<rect x="{px}" y="{y}" width="{col_w}" height="{bh}" rx="5" fill="{WHITE}" stroke="{col[p]}" stroke-width="1"/>')
            parts.append(f'<text x="{px+10}" y="{y+14}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>')
            ty = y + 25
            for line in wrapped:
                parts.append(f'<text x="{px+10}" y="{ty}" class="sm">{line}</text>')
                ty += 11
            y += bh + row_gap
    col_h = {p: top_h + sum(26 + plan[c][1] * 11 + row_gap for c in by[p]) for p in PILLARS}
    h = max(col_h.values()) + 44 + 30
    parts.append(f'<text x="{w/2.0}" y="{h-12}" text-anchor="middle" class="sm" font-style="italic">Seven pillars, {count_controls()} controls -- execution environment is the foundation</text>')
    body = "\n".join(parts)
    return svg(w, h, group_title(body, w, "SHIELD-AI: Pillar to Control Atlas"))



def diagram_incident_map():
    w, h = 820, 440
    cov = load_incident_coverage()
    titles = load_control_titles()
    mx = max(cov.values()) or 1
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    body = ""
    # two-column layout of horizontal bars, one per control, sorted by coverage
    ordered = sorted(control_ids(), key=lambda c: -cov[c])
    left = ordered[:36]
    right = ordered[36:]
    for col_idx, items in enumerate([left, right]):
        x0 = 30 + col_idx * 410
        body += f'''<text x="{x0}" y="44" class="cap">control</text>
        <text x="{x0+230}" y="44" class="cap"># incidents evidencing it</text>'''
        for i, cid in enumerate(items):
            yy = 56 + i * 10
            p = cid.split("-")[0]
            body += f'''<text x="{x0}" y="{yy+4}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>
            <rect x="{x0+40}" y="{yy}" width="{90 + int(150*cov[cid]/mx)}" height="6" rx="3" fill="{col[p]}"/>
            <text x="{x0+40 + 90 + int(150*cov[cid]/mx) + 6}" y="{yy+5}" class="sm">{cov[cid]}</text>'''
    body += f'''<text x="{w/2}" y="{h-10}" text-anchor="middle" class="sm" font-style="italic">Across {count_controls()} controls, the most-evidenced (MS-08, EE-01, TP-15, MIR-02) are the highest-priority hardening targets</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Which Controls Are Evidenced by Incidents?"))


# ── Diagram 3: Control -> AU framework matrix (heat grid) ────────────────


def diagram_au_matrix():
    w, h = 780, 520
    au = ["ISM", "E8", "SOCI", "CPS234", "Priv/APPs", "PSPF"]
    pillar_au = load_pillar_au_mappings()
    # map each pillar to the AU frameworks it touches (per committed mappings)
    pillar_touch = {}
    for p, text in pillar_au.items():
        t = text.lower()
        touch = set()
        if "ism" in t or "guidelines" in t: touch.add("ISM")
        if "essential eight" in t or "e8" in t or "privilege" in t or "patch" in t: touch.add("E8")
        if "soci" in t: touch.add("SOCI")
        if "cps 234" in t or "cps234" in t: touch.add("CPS234")
        if "privacy act" in t or "app " in t or "notifiable data" in t: touch.add("Priv/APPs")
        if "pspf" in t or "protective security" in t: touch.add("PSPF")
        pillar_touch[p] = touch
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    body = ""
    # header row of AU frameworks
    body += f'''<text x="180" y="48" class="cap">pillar · AU framework</text>'''
    for j, fw in enumerate(au):
        body += f'''<rect x="{180+j*86}" y="38" width="76" height="16" rx="3" fill="{BLUE}"/>
        <text x="{180+j*86+38}" y="{49}" text-anchor="middle" class="white" font-size="9" font-weight="bold">{fw}</text>'''
    # rows per pillar
    for i, p in enumerate(PILLARS):
        yy = 60 + i * 46
        body += f'''<rect x="30" y="{yy}" width="140" height="34" rx="4" fill="{col[p]}" opacity="0.15"/>
        <text x="40" y="{yy+13}" class="sm" font-weight="bold" fill="{col[p]}">{p}</text>
        <text x="40" y="{yy+26}" class="sm">{PILLAR_FULL[p]}</text>'''
        touch = pillar_touch.get(p, set())
        for j, fw in enumerate(au):
            cx = 180 + j * 86 + 38
            on = fw in touch
            fill = col[p] if on else "#f1f3f6"
            body += f'''<rect x="{180+j*86}" y="{yy}" width="76" height="34" rx="4" fill="{fill}" stroke="{col[p]}" stroke-width="{1 if on else 0.5}"/>
            <text x="{cx}" y="{yy+21}" text-anchor="middle" class="label" font-weight="bold" fill="{WHITE if on else MUTED}">{"✓" if on else "·"}</text>'''
    body += f'''<text x="{w/2}" y="{h-24}" text-anchor="middle" class="sm">Derived from each pillar's committed "AU framework mappings". Full control-by-control ISM/E8/SOCI/CPS234/APPs mapping is maintained separately (framework §2.4).</text>'''
    body += f'''<text x="{w/2}" y="{h-8}" text-anchor="middle" class="sm" font-style="italic">Shaded cells = the pillar signals that Australian framework in its control definitions ({count_controls()} controls)</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Pillars aligned to Australian frameworks"))


# ── Diagram 4: Pillar -> Maturity heat grid ──────────────────────────────


def diagram_maturity_heat():
    import textwrap
    w = 820
    maturity = load_maturity()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    lvl_col = {"L1": "#8a9ab0", "L2": "#4a7a9c", "L3": "#2563eb", "L4": "#d4a017"}
    cell_x0, cell_w, cell_gap = 140, 140, 10
    pillar_w = 100
    body = ""
    # header row: level labels
    body += f'''<text x="{cell_x0}" y="44" class="cap">pillar · maturity level</text>'''
    for j, lvl in enumerate(["L1 Initial", "L2 Managed", "L3 Defined", "L4 Optimised"]):
        body += f'''<rect x="{cell_x0+j*(cell_w+cell_gap)}" y="34" width="{cell_w}" height="16" rx="3" fill="{BLUE}"/>
        <text x="{cell_x0+j*(cell_w+cell_gap)+cell_w/2}" y="45" text-anchor="middle" class="white" font-size="9" font-weight="bold">{lvl}</text>'''
    # Each pillar is one row; text is WRAPPED inside each cell and left-aligned so
    # it never overflows the right edge into the adjacent box. Row height is sized
    # to the tallest of its four cells, and the canvas grows to fit all rows.
    lvls = ["L1", "L2", "L3", "L4"]
    lvl_labels = ["L1 Initial", "L2 Managed", "L3 Defined", "L4 Optimised"]
    line_gap = 11
    top_pad = 14
    wrap_w = 25  # chars per line at 9px in a 140px cell (pad inside both edges)
    y = 60
    rows = []  # (pillar, [(lvl, lines)])
    for p in PILLARS:
        prog = maturity.get(p, {})
        cells = []
        for lvl in lvls:
            desc = prog.get(lvl, "")
            if not desc:
                cells.append([])
                continue
            lines = textwrap.wrap(desc, width=wrap_w,
                                  break_on_hyphens=False, break_long_words=False)
            cells.append(lines)
        nlines = max((len(c) for c in cells), default=1)
        rows.append((p, cells, nlines))
    for p, cells, nlines in rows:
        rh = max(34, top_pad + nlines * line_gap + 8)
        body += f'''<rect x="30" y="{y}" width="{pillar_w}" height="{rh}" rx="4" fill="{col[p]}" opacity="0.15"/>
        <text x="40" y="{y+16}" class="sm" font-weight="bold" fill="{col[p]}">{p}</text>
        <text x="40" y="{y+27}" class="sm">{PILLAR_FULL[p]}</text>'''
        for j, (lvl, lines) in enumerate(zip(lvls, cells)):
            cx = cell_x0 + j * (cell_w + cell_gap)
            fill = lvl_col[lvl]
            body += f'''<rect x="{cx}" y="{y}" width="{cell_w}" height="{rh}" rx="4" fill="{fill}" opacity="0.18" stroke="{fill}" stroke-width="1"/>'''
            if not lines:
                body += f'''<text x="{cx+8}" y="{y+22}" class="sm" fill="{fill}" font-style="italic">—</text>'''
                continue
            ty = y + 14
            for ln in lines:
                body += f'''<text x="{cx+8}" y="{ty}" class="sm" fill="{fill}">{ln}</text>'''
                ty += line_gap
        y += rh + 10  # gap after each pillar row
    h = y + 26
    body += f'''<text x="{w/2}" y="{h-8}" text-anchor="middle" class="sm" font-style="italic">Across {count_controls()} controls, the weakest pillar determines overall maturity -- target the L2->L3 transition first (regulated entities)</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Pillar Maturity Heat Grid (L1->L4)"))


# ── Markdown view documents (derived, embedded numbers) ──────────────────


def md_pillar_atlas():
    titles = load_control_titles()
    by = {p: [] for p in PILLARS}
    for cid in control_ids():
        by[cid.split("-")[0]].append((cid, titles.get(cid, "")))
    lines = [
        "# 01 · Pillar → Control Atlas",
        "",
        "A simplified inventory of the **seven pillars** and their **69 controls**. Use this to see",
        "the full control surface at a glance: every control belongs to exactly one pillar, and the",
        "pillars are ordered by the logical dependencies they introduce (execution environment is",
        "the foundation).",
        "",
        "![Pillar to control atlas](../assets/diagrams/pillar-control-atlas.svg)",
        "",
        "## Controls by pillar",
        "",
    ]
    for p in PILLARS:
        lines.append(f"### {p} — {PILLAR_FULL[p]}")
        lines.append("")
        lines.append("| ID | Control |")
        lines.append("|---|---|")
        for cid, t in by[p]:
            lines.append(f"| {cid} | {t} |")
        lines.append("")
    lines += [
        "## Signal for architects",
        "",
        "- **EE → MS → IAM → DS → TP → MIR → GRM** is the dependency order: an escaped execution",
        "  environment invalidates every control layered above it.",
        "- **MS (15) and TP (16)** carry the most controls — model integrity and tool/pipeline",
        "  security are where the framework concentrates its coverage.",
        "",
    ]
    return "\n".join(lines)


def md_incident_map():
    cov = load_incident_coverage()
    titles = load_control_titles()
    links = load_incident_links()
    ordered = sorted(control_ids(), key=lambda c: -cov[c])
    lines = [
        "# 02 · Controls → Industry Incidents",
        "",
        "Which SHIELD-AI controls are actually **evidenced by real incidents**? This view",
        "links every control to the specific catalogue incidents (INC-01…INC-92) that",
        "reference it in their coverage verdicts. The most-evidenced controls are the",
        "highest-priority hardening targets — they are the controls the real world has",
        "repeatedly shown we need.",
        "",
        "![Controls incident map](../assets/diagrams/controls-incident-map.svg)",
        "",
        "## Coverage leaders (most evidenced)",
        "",
        "| Control | Title | Unique incidents |",
        "|---|---|---|",
    ]
    for cid in ordered[:10]:
        lines.append(f"| **{cid}** | {titles.get(cid,'')} | {len(links.get(cid,[]))} |")
    lines.append("")
    lines += [
        "## Incident evidence by control",
        "",
        "Each control lists the incidents that evidence it, as links into the",
        "gap-analysis document (unique incidents, verified coverage verdicts).",
        "",
    ]
    for cid in ordered:
        title = titles.get(cid, "")
        inc = links.get(cid, [])
        if inc:
            inc_links = ", ".join(
                f"[{i['id']}](../reference-views/07-incident-summaries.md#{i['anchor']})"
                for i in inc)
            lines.append(f"- **{cid}** — {title} ({len(inc)}): {inc_links} "
                         f"(human-readable summary in [doc 07](07-incident-summaries.md))")
        else:
            lines.append(f"- **{cid}** — {title} (0): no catalogue incident yet")
    lines.append("")
    zero = [c for c in ordered if not links.get(c)]
    lines += [
        f"## Not yet directly evidenced by an incident ({len(zero)} controls)",
        "",
        "These controls are part of the framework's baseline but have not yet been the direct",
        "subject of a catalogue incident. They are required coverage, not optional — the absence",
        "of a documented incident is a coverage gap to close, not a control to drop.",
        "",
        ", ".join(zero) if zero else "(none)",
        "",
    ]
    return "\n".join(lines)


def md_au_matrix():
    pillar_au = load_pillar_au_mappings()
    lines = [
        "# 03 · Controls → Australian Frameworks",
        "",
        "How SHIELD-AI pillars map to the Australian frameworks and regulatory instruments an",
        "organisation must comply with — ISM, Essential Eight, SOCI Act, APRA CPS 234, the Privacy",
        "Act (APPs), and the Protective Security Policy Framework (PSPF). Shaded cells mark the",
        "framework each pillar signals in its committed control definitions.",
        "",
        "![Control to AU framework matrix](../assets/diagrams/control-au-framework-matrix.svg)",
        "",
        "## Per-pillar AU framework mappings",
        "",
    ]
    for p in PILLARS:
        lines.append(f"### {p} — {PILLAR_FULL[p]}")
        lines.append("")
        lines.append(pillar_au.get(p, "*(no dedicated AU mapping line)*"))
        lines.append("")
    lines += [
        "## Notes",
        "",
        "- The framework (§2.4) maintains a **control-by-control** ISM / E8 / SOCI / CPS 234 /",
        "  Privacy Act map as a separate reference document; this view is the pillar-level",
        "  simplification for stakeholder presentation.",
        "- **MIR** is the most regulation-bound pillar: SOCI s.30B mandatory reporting (12h critical,",
        "  72h other), APRA CPS 234 s.3(c), and the Notifiable Data Breaches scheme all land there.",
        "",
    ]
    return "\n".join(lines)


def load_incident_links():
    """{control_id: [ {id, title, anchor}, ... ]} for every incident that
    references the control in its coverage verdicts. Anchors are generated
    exactly like GitHub's autogenerated ones from the `### INC-xx: Title`
    heading, so the links resolve in the rendered repo/GitHub.
    """
    txt = open(GAP, encoding="utf-8").read()
    incidents = []
    cur = None
    ctrl_re = re.compile(r"\b((?:EE|MS|IAM|DS|TP|MIR|GRM)-\d{2})\b")
    for ln in txt.split("\n"):
        m = re.match(r"^### (INC-\d+):\s*(.*)$", ln)
        if m:
            if cur:
                incidents.append(cur)
            title = m.group(2).strip()
            # GitHub renders the anchor from the FULL heading line, which
            # includes the "INC-xx: " prefix (e.g. "### INC-01: Title" ->
            # "#inc-01-title"), so the anchor must be derived from heading text.
            anchor = github_anchor(f"{m.group(1)}: {title}")
            cur = {"id": m.group(1), "title": title, "anchor": anchor, "refs": set()}
            continue
        if cur:
            for mm in ctrl_re.finditer(ln):
                cur["refs"].add(mm.group(1))
    if cur:
        incidents.append(cur)
    out = {}
    for inc in incidents:
        for cid in inc["refs"]:
            out.setdefault(cid, []).append(inc)
    for lst in out.values():
        lst.sort(key=lambda i: i["id"])
    return out


def load_policy_data():
    """Parse every policies/shield_ai_*.rego into {control_id: {...}}.

    Extracts the control's executable-verification facts from the policy file
    itself so the deep-dive view is grounded in the real policies, not a
    paraphrase: package, rule counts, maturity indicators, regulatory
    mappings, input model, purpose comment, named tool sets, and the
    IMPLEMENTED / stub status.
    """
    import glob
    out = {}
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "policies", "shield_ai_*.rego"))):
        t = open(path, encoding="utf-8").read()
        m = re.search(r"shield_ai_([a-z]+)_((?:ee|ms|iam|ds|tp|mir|grm)-\d{2})\.rego", os.path.basename(path))
        if not m:
            continue
        pillar, cid = m.group(1).upper(), m.group(2).upper()
        pkg = re.search(r"^package\s+([^\s]+)", t, re.M)
        # maturity indicators block
        mat = re.search(r"# Maturity indicators:\n((?:#\s*[^\n]*\n)*)", t)
        mat_lv = {}
        for lv in ["L1", "L2", "L3", "L4"]:
            lm = re.search(rf"#\s*{lv}:\s*(.+)", (mat.group(1) if mat else ""))
            mat_lv[lv] = lm.group(1).strip() if lm else ""
        # regulatory lines (stop at section markers so a trailing
        # "# IMPLEMENTED" / "# Input model" / "# Maturity" line is not swallowed)
        reg = re.search(r"# Regulatory mappings:\n((?:#\s*[^\n]*\n)*)", t)
        regs = []
        if reg:
            for ln in reg.group(1).splitlines():
                s = ln.lstrip("#").strip()
                if not s:
                    continue
                if any(mark in s for mark in
                       ("IMPLEMENTED", "Input model", "Maturity indicators",
                        "# Regulatory", "deny contains", "allow if")):
                    continue
                regs.append(s)
            regs = regs[:8]
        # deny rule definitions (modern rego.v1 syntax)
        deny = (len(re.findall(r"\bdeny\s+contains\b", t))
                + len(re.findall(r"\bdeny\s*\[[^\]]*\]\s*if\b", t))
                + len(re.findall(r"(?<!count\()\bdeny\b\s+if\b", t)))
        # Plain-language denial messages ("<cid> deny: <what fails>"), used to
        # render human-readable "What to verify" checklists derived verbatim
        # from the executable policy (never hand-paraphrased into new claims).
        deny_msgs = []
        # Plain messages: msg := "EE-01 deny: ..."
        for pm in re.finditer(r"msg\s*:=\s*\"([^\"]+)\"", t):
            deny_msgs.append(pm.group(1).strip())
        # sprintf form: msg := sprintf("...%q...", [...]) -- take the format
        # string, then soften the Rego %q/%v markers so the fragment reads
        # naturally in prose (agent X kept, not agent %q).
        for pm in re.finditer(r"msg\s*:=\s*sprintf\(\s*\"([^\"]+)\"", t):
            fmt = pm.group(1).strip()
            fmt = fmt.replace("%q", "'...'").replace("%v", "...").replace("%s", "...")
            # Rego sprintf uses %% for a literal percent sign; in prose it is a
            # single % (e.g. "CPU usage 95% exceeds limit 90%"). Collapse every
            # %% to % so the fragment reads naturally.
            fmt = fmt.replace("%%", "%")
            deny_msgs.append(fmt)
        # normalise: strip per-control prefix, collapse whitespace, drop empties
        _normed = []
        for pm in deny_msgs:
            pm = re.sub(rf"^{re.escape(cid)} deny:\s*", "", pm)
            pm = " ".join(pm.split()).strip()
            if pm:
                _normed.append(pm)
        # de-dupe preserving order
        seen = set(); deny_msgs = []
        for m in _normed:
            if m not in seen:
                deny_msgs.append(m); seen.add(m)
        implemented = "# IMPLEMENTED" in t
        # Purpose comment: the first descriptive '# ...' sentence after the
        # Pillar line (the control's plain objective, verbatim from the policy).
        purpose = ""
        pm = re.search(r"# SHIELD-AI\(TM\)[^\n]*\n# Pillar[^\n]*\n#[^\n]*\n#[ \t]*([^\n]+)\n", t)
        if pm:
            purpose = pm.group(1).strip()
        # Input model line: what signals the policy reads (verbatim).
        im = re.search(r"# Input model:[ \t]*(.+)", t)
        input_model = im.group(1).strip() if im else ""
        # Named tool/interface sets:  name := { "a", "b", ... } blocks.
        tool_sets = {}
        for sm in re.finditer(r"([a-z_][a-z0-9_]*)\s*:=\s*\{(?:[^{}]|\"[^\"]*\")*?\}", t):
            items = [x.strip().strip('"') for x in sm.group(0).split("{")[1].split("}")[0].split(",") if x.strip()]
            if len(items) >= 2:
                tool_sets[sm.group(1)] = items
        out[cid] = {
            "pillar": pillar,
            "package": pkg.group(1) if pkg else "",
            "file": os.path.basename(path),
            "maturity": mat_lv,
            "regulatory": regs,
            "deny": deny,
            "deny_msgs": deny_msgs,
            "implemented": implemented,
            "purpose": purpose,
            "input_model": input_model,
            "tool_sets": tool_sets,
        }
    return out


def _outcome(cid, title):
    """A one-line, business-readable statement of the outcome a control produces."""
    return f"Verify that {title.lower() if title else 'the control'} holds under agent action"


def github_anchor(title):
    """GitHub-compatible heading anchor (e.g. for '#INC-xx: Title' links).

    Matches GitHub's rendered-slug algorithm: lowercase, then drop every
    character that is not [0-9a-z], a space, or a hyphen (so '.', '/', '_',
    ''', '"' vanish entirely rather than becoming hyphens), then collapse
    whitespace runs to a single hyphen and strip leading/trailing hyphens.
    """
    t = title.lower()
    t = re.sub(r"[^0-9a-z\s-]", "", t)
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"-{2,}", "-", t)
    return t.strip("-")


def plain_verify(cid, title, pol_entry, cap=5):
    """Human-readable "What to verify" block for a control.

    Enriched for technical SMEs using ONLY information from the committed
    repo:
      - purpose: the control's plain objective, verbatim from the policy's
        own comment block
      - input_model: the signals the executable policy reads (verbatim)
      - checks: each fail-closed deny message, expanded with the named
        tool/interfacessets (if any) the policy references
      - maturity target: the policy's own L3 descriptor
    Returns (purpose, input_model, [(check, context or "")], rest, l3).
    """
    msgs = pol_entry.get("deny_msgs", [])
    purpose = pol_entry.get("purpose", "") or ""
    im = pol_entry.get("input_model", "") or ""
    sets = pol_entry.get("tool_sets", {}) or {}
    mat = pol_entry.get("maturity", {}) or {}
    l3 = (mat.get("L3") or "").strip()
    checks = [m for m in msgs if m.strip()]
    shown = checks[:cap]
    rest = max(0, len(checks) - cap)
    # Expand each check with the policy's named sets when the message refers
    # to one (keyword-matched on a normalised basis, so "high-risk tools"
    # matches high_risk_tools -- the context is always the policy's own list).
    expanded = []
    for chk in shown:
        ctx = ""
        chk_norm = re.sub(r"[-_ ]+", " ", chk.lower())
        for name, items in sets.items():
            keyword = re.sub(r"[-_ ]+", " ", name).strip()
            if keyword in chk_norm or keyword.rstrip("s") in chk_norm:
                ctx = ", ".join(items)
                break
        expanded.append((chk, ctx))
    return purpose, im, expanded, rest, l3


def load_incident_briefs():
    """{inc_id: {id, title, anchor, brief, controls}} for every incident in the
    gap-analysis.

    The 'brief' is the incident's OWN first sentence (from its `**What
    happened:**` narrative, or its intro paragraph for short-format incidents)
    -- reused verbatim so the human-readable summary view is derived from the
    committed source, never hand-paraphrased into a new claim. 'controls' is
    the set of SHIELD-AI control IDs the incident references.
    """
    txt = open(GAP, encoding="utf-8").read()
    out = {}
    ctrl_re = re.compile(r"\b((?:EE|MS|IAM|DS|TP|MIR|GRM)-\d{2})\b")
    for block in re.split(r"\n### INC-", txt):
        if not block.strip():
            continue
        head = block.split("\n", 1)[0]
        mm = re.match(r"(\d+):\s*(.*)$", head, re.DOTALL)
        if not mm:
            continue
        inc_id = "INC-" + mm.group(1)
        title = mm.group(2).strip()
        # The evidence body: everything from this block up to the next top-level
        # section or next incident (the block already stopped at the next \n### INC-).
        mtop = re.search(r"\n## ", block)
        body = block[:mtop.start()] if mtop else block
        wh = re.search(r"\*\*What happened:\*\*\s*(.*?)(?=\n\n|\n\*\*|\n\|)", body, re.S)
        brief = ""
        if wh:
            t = " ".join(wh.group(1).split())
            parts = re.split(r"(?<=[a-z0-9\)\]])\.\s+(?=[A-Z])", t, maxsplit=1)
            brief = parts[0].rstrip(" .") + "."
        else:
            # short-format incidents: first sentence of the intro paragraph
            para = re.search(r"\n\n\>.*?\n\n(.*?)(?=\n###|\n## |\nAffected controls|\Z)", body, re.S)
            if para:
                t = " ".join(para.group(1).split())
                t = re.split(r"\bAffected controls:\s*$", t)[0].strip()
                brief = re.split(r"(?<=[a-z0-9])\.\s+(?=[A-Z])", t, maxsplit=1)[0].rstrip(" .") + "."
        # Same rule as load_incident_links: the GitHub-rendered anchor covers the
        # whole heading line ("### INC-01: Title" -> "#inc-01-title"), so derive
        # the anchor from the full heading text, not the bare title.
        anchor = github_anchor(f"{inc_id}: {title}")
        out[inc_id] = {
            "id": inc_id,
            "title": title,
            "anchor": anchor,
            "brief": brief,
            "controls": sorted(set(ctrl_re.findall(body))),
        }
    return out


def md_incident_summaries():
    """Document 07: human-readable incident summaries.

    One card per incident: what happened (the incident's own first sentence),
    the SHIELD-AI controls it evidences, and a one-click link to the full
    technical detail in the gap-analysis -- so a reader who follows a link from
    a control's incident evidence lands on something scannable first and can
    drill down only if needed.
    """
    briefs = load_incident_briefs()
    links = load_incident_links()
    ids = sorted(briefs)
    lines = [
        "# 07 · Incident Summaries",
        "",
        "A human-friendly index of the **92 catalogue incidents**. Each card gives",
        "what happened in one sentence, the SHIELD-AI controls it evidences, and a",
        "link to the full technical detail in the gap-analysis document. Use this",
        "page when a control's 'incident evidence' link in doc 06 leads you here —",
        "it is the scannable summary; the catalogue entry is the deep dive.",
        "",
        "## Incidents A–Z",
        "",
    ]
    total_links = sum(len(links.get(i, [])) for i in ids)
    lines.append(
        f"> **Use with the field guide:** every incident-evidence link in "
        f"[06 · Control Technical Verification Field Guide](06-controls-technical.md) "
        f"now resolves to its card here. {len(ids)} incidents, "
        f"{sum(len(briefs[i]['controls']) for i in ids)} control references across the set.\n")
    lines.append("")
    for inc_id in ids:
        b = briefs[inc_id]
        ctrls = b["controls"]
        lines.append(f"### {inc_id}: {b['title']}")
        lines.append("")
        lines.append(f"**In brief:** {b['brief'] or '*No standalone summary; see full detail.*'}")
        lines.append("")
        if ctrls:
            ctrl_str = ", ".join(f"**{c}**" for c in ctrls)
            lines.append(f"- **Controls evidenced:** {ctrl_str}")
        else:
            lines.append("- **Controls evidenced:** none directly referenced")
        lines.append(f"- **Full detail:** [view the INC-{inc_id.split('-')[1]} catalogue entry]"
                     f"(../framework/shield-ai-gap-analysis.md#{b['anchor']})")
        lines.append("")
    lines += [
        "## How this page is generated",
        "",
        "- **Summary card:** one card per incident, ordered by INC number.",
        "- **'In brief'** reuses the incident's own opening sentence from the gap-analysis —",
        "  no paraphrase, no invented summary.",
        "- **'Controls evidenced'** is the set of SHIELD-AI control IDs referenced in the",
        "  incident's catalogue entry.",
        "- **'Full detail'** links to the complete technical record in the gap-analysis.",
        "",
    ]
    return "\n".join(lines)


# ── Diagram 5: Control -> Outcome & Executable verification ─────────────


def diagram_control_outcomes():
    w = 880
    pol = load_policy_data()
    titles = load_control_titles()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    total_deny = sum(p["deny"] for p in pol.values())
    body = ""
    # header: legend + headline counts
    body += f'''<text x="40" y="44" class="cap">Executable verification coverage</text>
    <text x="40" y="60" class="label" font-weight="bold">{len(pol)} policies · {total_deny} deny rules · {"69/69 implemented" if sum(1 for p in pol.values() if p['implemented'])==len(pol) else "some stubs"}</text>'''
    # per-pillar rows: control blocks with status + deny count
    body += f'''<text x="40" y="84" class="cap">Control</text>
    <text x="200" y="84" class="cap">Outcome (what the policy verifies)</text>
    <text x="600" y="84" class="cap">Policy</text>
    <text x="760" y="84" class="cap">Rules · status</text>'''
    row_h = 20
    block_head = 18
    groups = {p: [] for p in PILLARS}
    for cid, d in pol.items():
        groups[d["pillar"]].append((cid, d))
    groups = {p: v for p, v in groups.items() if v}
    # Cumulative stacking: each pillar block = header line + N control rows.
    y = 100
    for p in PILLARS:
        if p not in groups:
            continue
        block_h = block_head + len(groups[p]) * row_h
        y0 = y
        body += f'''<rect x="30" y="{y0}" width="820" height="{block_h+4}" rx="4" fill="{col[p]}" opacity="0.07"/>
        <text x="40" y="{y0+12}" class="cap" fill="{col[p]}">{p} · {PILLAR_FULL[p]}</text>'''
        iy = y0 + block_head
        for cid, d in groups[p]:
            title = titles.get(cid, "")
            body += f'''<text x="40" y="{iy+8}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>
            <text x="200" y="{iy+8}" class="sm">{title[:46]}</text>
            <text x="600" y="{iy+8}" class="sm">{d['file'].replace('shield_ai_','').replace('.rego','')}</text>
            <text x="760" y="{iy+8}" class="sm">{d['deny']} deny · {"✓" if d['implemented'] else "stub"}</text>'''
            iy += row_h
        y += block_h + 14  # gap after each pillar block
    h = y + 32
    body += f'''<text x="{w/2}" y="{y+18}" text-anchor="middle" class="sm" font-style="italic">All {count_controls()} controls map 1:1 to an executable Rego policy (verified by OPA tests); the deny-rule count shows verification depth</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Control → Outcome & Executable Verification"))


# ── Document 05 ──────────────────────────────────────────────────────────


def md_control_outcomes():
    pol = load_policy_data()
    titles = load_control_titles()
    total_deny = sum(p["deny"] for p in pol.values())
    implemented = sum(1 for p in pol.values() if p["implemented"])
    lines = [
        "# 05 · Controls → Outcomes & Executable Verification",
        "",
        "A deep dive on every SHIELD-AI control: what **outcome** it produces, and the",
        "**executable policy** that verifies the control is being met. Each control maps 1:1",
        "to a Rego policy in `policies/` (`shield_ai_{pillar}_{control}.rego`) that is",
        "evaluated by the OPA test suite — so a control is only considered verified when",
        "its policy holds.",
        "",
        f"This view is derived from the policy files themselves: **{len(pol)}** implemented",
        f"policies (**{implemented}/{len(pol)}** marked IMPLEMENTED), ",
        f"**{total_deny}** deny rules across the suite.",
        "",
        "![Control outcome diagram](../assets/diagrams/control-outcomes-diagram.svg)",
        "",
        "## How verification works",
        "",
        "- **Input model:** each policy declares the agent/tool/action shape it inspects",
        "  (declared in the policy header as `Input model:`).",
        "- **`deny` rules:** the assertions that must *not* hold — a control is met when",
        "  its deny set is empty (`allow if count(deny) == 0`).",
        "- **Fail closed:** the absence of a required flag is treated as a violation, so",
        "  verification never silently passes on missing data.",
        "",
    ]
    for p in PILLARS:
        subs = {cid: d for cid, d in pol.items() if d["pillar"] == p}
        lines.append(f"## {p} — {PILLAR_FULL[p]}")
        lines.append("")
        lines.append("| Control | Outcome | Executable policy | Deny rules | Maturity reach | Mappings |")
        lines.append("|---|---|---|---|---|---|")
        for cid, d in sorted(subs.items()):
            title = titles.get(cid, "")
            outcome = _outcome(cid, title)
            # maturity reach = highest L with non-empty indicator
            reach = max((lv for lv in ["L1","L2","L3","L4"] if d["maturity"].get(lv)),
                        default="(none)")
            regs = "; ".join(d["regulatory"][:3]) or "-"
            status = "✓" if d["implemented"] else "stub"
            lines.append(
                f"| **{cid}** | {outcome} | `{d['file']}` | {d['deny']} ({status}) | {reach} | {regs} |")
        lines.append("")
    lines += [
        "## Reading the table",
        "",
        "- **Outcome** states in plain terms what the control guarantees.",
        "- **Executable policy** is the exact `policies/` file that verifies the outcome.",
        "- **Deny rules** is the number of fail-closed assertions the policy evaluates; more",
        "  deny rules = deeper verification (e.g. MS-15 tenant isolation exercises 8).",
        "- **Maturity reach** is the highest L1–L4 indicator the policy documents.",
        "- **Mappings** lists the Australian framework references the policy header carries.",
        "",
        "A control with a `stub` status is defined in the framework but its policy test",
        "logic is not yet implemented — it should be treated as unverified until `make",
        "test` passes it.",
        "",
    ]
    return "\n".join(lines)


def md_technical_controls():
    """Document 06: controls-only technical verification field guide for
    highly-technical security specialists. Control ID, title, the normative
    text to verify, the executable policy + deny rules, and incident evidence
    with links to the actual incidents."""
    titles = load_control_titles()
    pol = load_policy_data()
    links = load_incident_links()
    lines = [
        "# 06 · Control Technical Verification Field Guide",
        "",
        "A controls-only deep dive for **highly-technical security specialists**. For each of",
        f"the **{count_controls()} SHIELD-AI controls** it gives the identifier, the exact",
        "normative text that must hold, the executable policy that verifies it, and the",
        "catalogue incidents that evidence the control in practice. This is a working",
        "assessment document, not a stakeholder briefing.",
        "",
        "![Control technical sheet](../assets/diagrams/control-technical-sheet.svg)",
        "",
        "## How this sheet is derived",
        "",
        "Every control is verified by an executable Rego policy. The sheet above shows, for",
        "all 69 controls, the plain objective, the verification depth (deny rules), the",
        "exact policy file, and the incidents evidencing the control class. The 'What to",
        "verify' checklist beneath each control is derived directly from those deny rules.",
        "",
        "",
        "## How to use this field guide",
        "",
        "- **Control** is the stable identifier from the framework.",
        "- **What to verify** is the enriched block for a technical specialist: it states the",
                "  objective, adds the control's plain purpose (from the policy's own comment), names",
                "  the **input model** the executable policy evaluates (so you know what to instrument",
                "  and feed it), lists each fail-closed condition the policy actually checks, expands",
                "  each with the concrete tool/interface set it references, and gives the **L3 maturity",
                "  target** from the policy.",
                "- **Executable policy** names the exact `policies/*.rego` file; open it for the full",
                "  `deny` rules and the exact input schema.",
                "- **Incident evidence** links each incident to its human-readable summary card in",
                "  [07 · Incident Summaries](07-incident-summaries.md), which gives what happened in",
                "  one sentence and then links the full catalogue detail in the gap-analysis — this",
                "  keeps the control page scannable and the deep dive one click further out.",
                "",
                "> **How to read the checks:** each bullet is a condition that, when true, makes the",
                "> control *fail closed* (the action is blocked). To satisfy the control, confirm",
                "> none of those conditions holds in your deployment, and that `make test` passes.",
                "> `<name>` marks the runtime subject (agent, tool, server, or record) named in the",
                "> actual deny message — substitute the real identifier when assessing a deployment.",
                "",
            ]

    for p in PILLARS:
        subs = sorted([c for c in control_ids() if c.startswith(p)])
        lines.append(f"## {p} — {PILLAR_FULL[p]}")
        lines.append("")
        for cid in subs:
            title = titles.get(cid, "")
            pd = pol.get(cid, {})
            inc = links.get(cid, [])
            purpose, im, checks, rest, l3 = plain_verify(cid, title, pd)
            lines.append(f"### {cid}: {display_title(cid)}")
            lines.append("")
            lines.append(f"- **Executable policy:** `{pd.get('file','—')}` "
                         f"(package `{pd.get('package','—')}`, {pd.get('deny',0)} deny rules)")
            lines.append("")
            intro = (f"**What to verify:** {display_title(cid)} must hold.")
            if purpose:
                intro += f" {purpose}"
            if im:
                intro += f" The policy evaluates `{im}` and fails closed -- blocks the action -- when any of the following is true:"
            elif checks:
                intro += " The executable policy fails closed -- blocks the action -- when any of the following is true:"
            else:
                intro += f" Confirm the condition holds and `make test` passes ({pd.get('file','policy')})."
            lines.append(intro)
            if checks:
                for chk, ctx in checks:
                    chk_w = chk.replace("'...'", "<name>")
                    if ctx:
                        lines.append(f"  - {chk_w}  *(relevant set: {ctx})*")
                    else:
                        lines.append(f"  - {chk_w}")
                if rest:
                    lines.append(f"  - *{rest} more fail-closed conditions in the policy.*")
            if l3:
                lines.append("")
                lines.append(f"- **Maturity target (L3):** {l3}")
            lines.append("")
            if inc:
                inc_links = ", ".join(
                    f"[{i['id']}](../reference-views/07-incident-summaries.md#{i['anchor']})"
                    for i in inc)
                lines.append(f"- **Incident evidence ({len(inc)}):** {inc_links} "
                             "-- opens each incident's human-readable summary (see doc 07)")
            else:
                lines.append("- **Incident evidence:** none yet — baseline coverage, "
                             "not yet demonstrated by a catalogue incident")
            lines.append("")
    lines += [
        "## Verification protocol",
        "",
        f"- Run `make test` — the OPA suite evaluates every `policies/*.rego` "
        f"({len(pol)} files, {sum(pd['deny'] for pd in pol.values())} deny rules).",
        "- A control is met when its policy's `deny` set is empty for the input under test.",
        "- Missing input fields are treated as violations (fail closed).",
        "",
    ]
    return "\n".join(lines)


def diagram_technical_sheet():
    """Per-pillar technical verification coverage: control, objective, deny
    rules, incident evidence, implemented status -- dense for specialists."""
    w = 880
    pol = load_policy_data()
    titles = load_control_titles()
    links = load_incident_links()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    total_deny = sum(p["deny"] for p in pol.values())
    total_links = sum(len(links.get(c, [])) for c in control_ids())
    body = ""
    body += f'''<text x="40" y="44" class="cap">Technical verification field guide</text>
    <text x="40" y="60" class="label" font-weight="bold">{count_controls()} controls · {total_deny} deny rules · {total_links} control-incident links</text>'''
    body += f'''<text x="40" y="84" class="cap">Control</text>
    <text x="170" y="84" class="cap">Objective (what must hold)</text>
    <text x="470" y="84" class="cap">Verify via policy</text>
    <text x="590" y="84" class="cap">Policy file</text>
    <text x="780" y="84" class="cap">Incidents</text>'''
    row_h = 20
    block_head = 18
    groups = {p: [] for p in PILLARS}
    for cid in control_ids():
        groups[cid.split("-")[0]].append(cid)
    groups = {p: v for p, v in groups.items() if v}
    # Cumulative stacking: each pillar block = header line + N control rows.
    y = 100
    for p in PILLARS:
        if p not in groups:
            continue
        block_h = block_head + len(groups[p]) * row_h
        y0 = y
        body += f'''<rect x="30" y="{y0}" width="820" height="{block_h+4}" rx="4" fill="{col[p]}" opacity="0.06"/>
        <text x="40" y="{y0+12}" class="cap" fill="{col[p]}">{p} · {PILLAR_FULL[p]}</text>'''
        iy = y0 + block_head
        for cid in groups[p]:
            title = display_title(cid)
            inc_count = len(links.get(cid, []))
            deny = pol.get(cid, {}).get('deny', 0)
            policy = pol.get(cid, {}).get('file', '').replace('shield_ai_', '').replace('.rego', '')
            body += f'''<text x="40" y="{iy+8}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>
            <text x="170" y="{iy+8}" class="sm">{title[:48]}</text>
            <text x="470" y="{iy+8}" class="sm">{deny} deny rules</text>
            <text x="590" y="{iy+8}" class="sm">{policy[:24]}</text>
            <text x="780" y="{iy+8}" class="sm">{inc_count} incidents</text>'''
            iy += row_h
        y += block_h + 14  # gap after each pillar block
    h = y + 32  # footer margin
    body += f'''<text x="{w/2}" y="{y+18}" text-anchor="middle" class="sm" font-style="italic">Specialist sheet: objective, executable policy + verification depth, and incident evidence per SHIELD-AI control</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Control Technical Verification Field Guide"))


def md_maturity():
    maturity = load_maturity()
    lines = [
        "# 04 · Pillars & Controls → Maturity Model",
        "",
        "Where each pillar sits on the SHIELD-AI maturity curve (**L1 Initial → L2 Managed → L3",
        "Defined → L4 Optimised**), consistent with ISM and the Essential Eight maturity model.",
        "The weakest pillar determines the organisation's overall maturity score.",
        "",
        "![Pillar maturity heat grid](../assets/diagrams/pillar-maturity-heat.svg)",
        "",
        "## Progression by pillar",
        "",
        "| Pillar | L1 | L2 | L3 | L4 |",
        "|---|---|---|---|---|",
    ]
    for p in PILLARS:
        prog = maturity.get(p, {})
        lines.append(f"| **{p}** | {prog.get('L1','')} | {prog.get('L2','')} | {prog.get('L3','')} | {prog.get('L4','')} |")
    lines += [
        "",
        "## Practical guidance",
        "",
        "- Move from **L1 → L2** first (documented controls, per-agent identities, basic monitoring).",
        "- Regulated entities and government target **L3** (automated controls, anomaly detection,",
        "  board reporting, full regulatory mapping).",
        "- **L4** (optimised) applies to critical infrastructure and national-security workloads.",
        "",
    ]
    return "\n".join(lines)


def md_readme():
    return """# SHIELD-AI Reference Views

Eleven cross-cutting views for presenting the framework to security architects
and business stakeholders. Each view derives its content from the committed
framework sources (see `tools/generate_reference_views.py`) so it can never
drift from the main document; most ship as both a Markdown page and an SVG
diagram, and the index is maintained for both formats.

| # | View | Question it answers | SVG |
|---|------|--------------------|-----|
| 01 | [Pillar → Control Atlas](01-pillar-control-atlas.md) | What is the full control surface, by pillar? | `pillar-control-atlas.svg` |
| 02 | [Controls → Incidents](02-controls-incidents.md) | Which controls are evidenced by real incidents? | `controls-incident-map.svg` |
| 03 | [Controls → AU Frameworks](03-control-au-framework-matrix.md) | What must we align to (ISM/E8/SOCI/CPS234/Privacy/PSPF)? | `control-au-framework-matrix.svg` |
| 04 | [Pillar → Maturity](04-pillar-maturity.md) | How mature are we per pillar, and what does L3 require? | `pillar-maturity-heat.svg` |
| 05 | [Controls → Outcomes & Executable Verification](05-controls-outcomes.md) | What does the control guarantee, and which executable policy verifies it? | `control-outcomes-diagram.svg` |
| 06 | [Control Technical Verification Field Guide](06-controls-technical.md) | What precisely must hold per control, and how is it verified? *(technical specialists)* | `control-technical-sheet.svg` |
| 07 | [Incident Summaries](07-incident-summaries.md) | What happened in each catalogue incident, in one line, with which controls it evidences? | — |
| 08 | [Policy Coverage Heatmap](08-policy-coverage-heat.md) | How deep is each control's executable verification? | `policy-coverage-heat.svg` |
| 09 | [Self-Assessment Scorecard](09-assessment-scorecard.md) | How do we record our own posture, control by control? | — |
| 10 | [Implementation Roadmap](10-implementation-roadmap.md) | Which controls should we harden first, and in what order? | `implementation-roadmap.svg` |
| 11 | [Executive One-Pager](11-executive-one-pager.md) | What is the 60-second board-level story? | `shield-ai-at-a-glance.svg` |

## For business stakeholders (the 60-second story)

- **What we protect:** the model, who can use it, what it can touch, the tools it
  invokes, how we monitor it, how we govern it, and the sandbox that contains it
  — seven pillars, each with defined controls.
- **Where the real risk shows up:** the controls repeatedly shown up by real
  incidents (MS-08 MCP security, EE-01 execution boundary, TP-15 code-execution
  sandbox, MIR-02 anomaly detection) are where hardening effort pays first.
- **What we must align to:** ISM, Essential Eight, SOCI Act, APRA CPS 234, the
  Privacy Act, and PSPF — mapped per pillar.
- **How far along we are:** a maturity heat grid shows the L2 → L3 point where
  regulated entities reach automated, board-reported security.
- **How we know we're compliant:** every control maps to an executable policy
  (`policies/*.rego`) that OPA runs — so claims are machine-verifiable, not
  declarative.

> Generated by `python3 tools/generate_reference_views.py`. Add it to
> `make check` / `update_all.sh` so the views always reflect the framework.
"""



def diagram_shield_ai_at_a_glance():
    """'What SHIELD-AI protects' schematic: the seven pillars arranged in a
    ring around a shielded agent + model core. A compact first-read visual that
    gives a board member the mental model in one glance. All text and counts are
    deterministic; the canvas is sized from content."""
    import math
    w, h = 880, 440
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    short = {"EE": "the sandbox", "MS": "the model", "IAM": "who + what may act",
             "DS": "the data", "TP": "the tools", "MIR": "the monitoring",
             "GRM": "the governance"}
    cx, cy = w / 2, h / 2 + 10
    body = ''
    # core badge: the shielded agent
    body += (f'<circle cx="{cx}" cy="{cy}" r="58" fill="{NAVY}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="4 3"/>'
             f'<text x="{cx}" y="{cy-6}" text-anchor="middle" class="white" font-size="11" font-weight="bold">SHIELD-AI</text>'
             f'<text x="{cx}" y="{cy+10}" text-anchor="middle" class="white" font-size="8">agentic AI,</text>'
             f'<text x="{cx}" y="{cy+22}" text-anchor="middle" class="white" font-size="8">model + tool calls,</text>'
             f'<text x="{cx}" y="{cy+32}" text-anchor="middle" class="white" font-size="8">contained and verified</text>')
    # ring of pillars
    n = len(PILLARS)
    R = 150
    for i, p in enumerate(PILLARS):
        ang = -math.pi / 2 + i * (2 * math.pi / n)  # start at top, clockwise
        x = cx + R * math.cos(ang)
        y = cy + R * math.sin(ang)
        bx, by, bw, bh = x - 58, y - 26, 116, 52
        body += (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw}" height="{bh}" rx="6" '
                 f'fill="{col[p]}" opacity="0.10"/>'
                 f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw}" height="3" rx="1.5" fill="{col[p]}"/>'
                 f'<text x="{x:.0f}" y="{y-8:.0f}" text-anchor="middle" fill="{col[p]}" font-size="10" font-weight="bold">{p}</text>'
                 f'<text x="{x:.0f}" y="{y+6:.0f}" text-anchor="middle" class="sm" fill="{col[p]}">{PILLAR_FULL[p]}</text>'
                 f'<text x="{x:.0f}" y="{y+18:.0f}" text-anchor="middle" class="sm" fill="{MUTED}">{short[p]}</text>')
    body += (f'<text x="{cx}" y="{h-14}" text-anchor="middle" class="sm" font-style="italic">'
             f'seven pillars, {count_controls()} controls - each verified by an executable policy</text>')
    return svg(w, h, group_title(body, w, "SHIELD-AI at a glance: the seven pillars that protect agentic AI"))


def diagram_policy_coverage():
    """Glanceable heat grid: per control, implementation status, deny-rule
    depth, incident evidence, and a coverage-intensity bar. All cells derive
    from the committed policies + incident catalogue (deterministic)."""
    w = 880
    pol = load_policy_data()
    cov = load_incident_coverage()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    body = ''
    body += ('<text x="40" y="44" class="cap">Policy coverage heatmap</text>\n'
             '    <text x="40" y="60" class="label" font-weight="bold">'
             f'{count_controls()} controls · implementation × deny depth × incident evidence</text>')
    body += ('<text x="40" y="84" class="cap">Control</text>'
             '<text x="180" y="84" class="cap">Policy</text>'
             '<text x="300" y="84" class="cap">Deny rules</text>'
             '<text x="420" y="84" class="cap">Incidents</text>'
             '<text x="520" y="84" class="cap">Coverage intensity</text>')
    scores = {c: cov.get(c, 0) * 3 + pol[c].get('deny', 0) * 2 + (4 if pol[c].get('implemented') else 0) for c in control_ids()}
    mx = max(scores.values()) or 1
    y = 100; row_h = 16; block_head = 18
    for p in PILLARS:
        ids = [c for c in control_ids() if c.startswith(p)]
        if not ids:
            continue
        bh = block_head + len(ids) * row_h; y0 = y
        body += (f'<rect x="30" y="{y0}" width="820" height="{bh+4}" rx="4" '
                 f'fill="{col[p]}" opacity="0.06"/>\n<text x="40" y="{y0+12}" '
                 f'class="cap" fill="{col[p]}">{p} · {PILLAR_FULL[p]}</text>')
        iy = y0 + block_head
        for cid in ids:
            d = pol[cid]
            st = "IMPL" if d.get('implemented') else "stub"
            dn = d.get('deny', 0); ic = cov.get(cid, 0)
            t = max(0.0, min(1.0, scores[cid] / mx))
            r = int(200 * t + 40); g = int(150 * (1 - t) + 40); b = int(60 + 120 * (1 - t))
            body += (f'<text x="40" y="{iy+8}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>'
                     f'<text x="180" y="{iy+8}" class="sm">{st}</text>'
                     f'<text x="300" y="{iy+8}" class="sm">{dn}</text>'
                     f'<text x="420" y="{iy+8}" class="sm">{ic}</text>'
                     f'<rect x="520" y="{iy-2}" width="{int(280*t)}" height="10" rx="3" fill="#{r:02x}{g:02x}{b:02x}"/>')
            iy += row_h
        y += bh + 12
    h = y + 40
    body += (f'<text x="{w/2}" y="{y+18}" text-anchor="middle" class="sm" font-style="italic">'
             'Intensity = incident evidence (x3) + deny-rule depth (x2) + implemented status (x4)</text>')
    return svg(w, h, group_title(body, w, "SHIELD-AI: Policy Coverage Heatmap"))


def md_policy_coverage():
    pol = load_policy_data(); cov = load_incident_coverage()
    lines = ["# 08 · Policy Coverage Heatmap", "",
             "How deep is each control's executable verification? A glanceable grid of implementation status, deny-rule depth, and incident evidence per control, derived from the committed policies and incident catalogue so it stays current with the sources.", "",
             "![Policy coverage heatmap](../assets/diagrams/policy-coverage-heat.svg)", "",
             "## Verification depth by pillar", "", "| Pillar | Controls | Implemented | Deny rules | Incident refs |", "|---|---|---|---|---|"]
    for p in PILLARS:
        ids = [c for c in control_ids() if c.startswith(p)]
        if not ids:
            continue
        imp = sum(1 for c in ids if pol[c].get('implemented'))
        dn = sum(pol[c].get('deny', 0) for c in ids)
        ic = sum(cov.get(c, 0) for c in ids)
        lines.append(f"| **{p}** | {len(ids)} | {imp} | {dn} | {ic} |")
    lines += ["", "## Reading the heat", "",
              "- **Implementation status** - `IMPL` is an executable policy; `stub` is declared but not yet enforced.",
              "- **Deny rules** - how many fail-closed conditions the policy enforces.",
              "- **Incidents** - how many catalogue events evidence the control class; intensity shades cool (low) to hot (high).", ""]
    return "\n".join(lines)


def md_assessment_scorecard():
    pol = load_policy_data(); titles = load_control_titles()
    lines = ["# 09 · Self-Assessment Scorecard", "",
             "A printable, per-control checklist for an adopting organisation to record its own posture. Every row is derived from the committed policy data - objective, implementation status, deny-rule depth, and the fail-closed conditions the executable policy enforces.", "",
             "## How to use", "",
             "- Work through each pillar below and mark the box when your organisation can evidence the condition.",
             "- The fail-closed conditions come from the control's own deny rules - tick each you demonstrably meet.",
             "- Cross-reference the field guide for the exact checks: [06 · Technical Verification](06-controls-technical.md).", ""]
    for p in PILLARS:
        ids = [c for c in control_ids() if c.startswith(p)]
        if not ids:
            continue
        lines += [f"## {p} · {PILLAR_FULL[p]}", ""]
        for cid in ids:
            d = pol[cid]; t = titles.get(cid, "")
            st = "implemented" if d.get('implemented') else "stub"
            dn = d.get('deny', 0)
            line = f"- [ ] **{cid}: {t}** - {_outcome(cid, t)} (policy {st}, {dn} deny rules)."
            shown = d.get('deny_msgs', [])[:3]
            if shown:
                line += " *Fail-closed:* " + "; ".join(shown)
                extra = len(d.get('deny_msgs', [])) - len(shown)
                if extra > 0:
                    line += f" (+{extra} more)."
            lines.append(line)
        lines.append("")
    return "\n".join(lines)


def md_implementation_roadmap():
    pol = load_policy_data(); cov = load_incident_coverage(); titles = load_control_titles()
    lines = ["# 10 · Implementation Roadmap", "",
             "Which controls to harden first. Ranking is evidence-weighted from the committed sources - incident evidence and implementation gap - so the sequence is transparent and reproducible.", "",
             "## Method", "",
             "Priority score = incident evidence (x3) + implementation gap (x6 when the executable policy is missing). Controls are bucketed into three phases.", ""]
    scored = []
    for cid in control_ids():
        d = pol[cid]
        sc = cov.get(cid, 0) * 3 + (0 if d.get('implemented') else 6)
        scored.append((cid, sc))
    scored.sort(key=lambda x: (-x[1], x[0]))
    mx = max(s for _, s in scored) or 1
    phases = {"1": "Foundations (fix incident-evidenced gaps first)", "2": "Consolidation (raise maturity to L3)", "3": "Optimisation (deepen verification)"}
    order = {cid: ("1" if sc >= 0.8 * mx else ("2" if sc >= 0.45 * mx else "3")) for cid, sc in scored}
    lines += ["", "![Implementation roadmap](../assets/diagrams/implementation-roadmap.svg)", ""]
    for ph in ("1", "2", "3"):
        bucket = [(cid, sc) for cid, sc in scored if order[cid] == ph]
        if not bucket:
            continue
        lines += [f"## Phase {ph} · {phases[ph]}", "",
                  "| Priority | Control | Title | Score | Focus (fail-closed condition to address) |",
                  "|---|---|---|---|---|"]
        for rank, (cid, sc) in enumerate(bucket, 1):
            d = pol[cid]
            focus = "; ".join(d.get('deny_msgs', [])[:2]) or _outcome(cid, titles.get(cid, ""))
            # Full title and full focus -- no mid-word truncation. GitHub wraps
            # long table cells, so cutting to a fixed character count only ever
            # lost information.
            lines.append(f"| {rank} | **{cid}** | {titles.get(cid,'')} | {sc} | {focus} |")
        lines.append("")
    lines += [""]
    # Ranked top-ten summary for a quick scan
    lines += ["## Ten highest-priority controls", ""]
    for rank, (cid, sc) in enumerate(scored[:10], 1):
        d = pol[cid]
        focus = (d.get('deny_msgs', []) or [_outcome(cid, titles.get(cid, ""))])[0]
        lines.append(f"{rank}. **{cid}** ({sc}) - {focus}")
    lines += ["", "See [06 · Technical Verification](06-controls-technical.md) for full per-control checklists.", ""]
    return "\n".join(lines)


def diagram_implementation_roadmap():
    """Three-phase roadmap as a horizontal pipeline: each phase bucket with its
    control count, the phase's goal, and the top controls in that bucket. All
    values derived from the same scoring used by the markdown view."""
    import textwrap
    w, h = 880, 300
    pol = load_policy_data(); cov = load_incident_coverage()
    scored = []
    for cid in control_ids():
        d = pol[cid]
        sc = cov.get(cid, 0) * 3 + (0 if d.get('implemented') else 6)
        scored.append((cid, sc))
    scored.sort(key=lambda x: (-x[1], x[0]))
    mx = max(s for _, s in scored) or 1
    order = {cid: ("1" if sc >= 0.8 * mx else ("2" if sc >= 0.45 * mx else "3")) for cid, sc in scored}
    buckets = {ph: [(c, s) for c, s in scored if order[c] == ph] for ph in ("1", "2", "3")}
    titles = load_control_titles()
    goals = {"1": "Foundations\nfix incident-evidenced gaps", "2": "Consolidation\nraise maturity toward L3", "3": "Optimisation\ndeepen verification"}
    body = ""
    body += f'<text x="40" y="44" class="cap">Implementation roadmap</text>'
    body += ('<text x="40" y="60" class="label" font-weight="bold">'
             'Priority = incident evidence (x3) + implementation gap (x6)</text>')
    x = 40; box_w = 260; gap = 20; box_h = 190; top = 80
    phase_col = {"1": "#c0392b", "2": "#b9770e", "3": "#1a3a6b"}
    for ph in ("1", "2", "3"):
        b = buckets[ph]
        y = top
        body += (f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" '
                 f'fill="{phase_col[ph]}" opacity="0.07"/>'
                 f'<rect x="{x}" y="{y}" width="{box_w}" height="4" rx="2" fill="{phase_col[ph]}"/>'
                 f'<text x="{x+12}" y="{y+26}" class="cap" fill="{phase_col[ph]}" font-size="10" font-weight="bold">Phase {ph} · {len(b)} controls</text>')
        for j, gtext in enumerate(goals[ph].split("\n")):
            body += f'<text x="{x+12}" y="{y+42+j*13}" class="sm" fill="{phase_col[ph]}">{gtext}</text>'
        body += f'<line x1="{x+8}" x2="{x+box_w-8}" y1="{y+76}" y2="{y+76}" stroke="{phase_col[ph]}" stroke-width="1" opacity="0.3"/>'
        iy = y + 92
        for cid, sc in b[:6]:
            body += (f'<text x="{x+12}" y="{iy}" class="sm" font-weight="bold">{cid}</text>'
                     f'<text x="{x+box_w-90}" y="{iy}" class="sm">score {sc}</text>')
            iy += 16
        if len(b) > 6:
            body += f'<text x="{x+12}" y="{iy}" class="sm" font-style="italic">+{len(b)-6} more in [doc 10](10-implementation-roadmap.md)</text>'
        x += box_w + gap
    w = x - gap + 20
    return svg(w, h, group_title(body, w, "SHIELD-AI: Implementation Roadmap, Three Phases"))


def md_executive_one_pager():
    pol = load_policy_data(); cov = load_incident_coverage(); links = load_incident_links()
    titles = load_control_titles(); mat = load_maturity()
    impl = sum(1 for c in control_ids() if pol[c].get('implemented'))
    tot = len(control_ids())
    dn = sum(pol[c].get('deny', 0) for c in control_ids())
    trefs = sum(cov.values())
    lines = ["# 11 · Executive One-Pager", "",
             "A one-page view for a board member or senior executive, derived from the committed framework and incident evidence.", "",
             "## The picture in numbers", "",
             f"- **{tot} controls** across the seven pillars that protect the model, identity, data, tools, monitoring, and governance of agentic AI.",
             f"- **{impl} controls ({int(100*impl/tot)}%)** already have an executable verification policy enforcing **{dn}** fail-closed conditions.",
             f"- **{trefs} control-incident references** in the catalogue (92 events) show where real-world risk actually surfaces.", ""]
    # Where the same facts are stated in plain business language drawn from the
    # control's own title (no invented claims): what the control does, how many
    # catalogue incidents evidence it, and a link to a one-line human summary.
    plain = {"MS-08": "limits what tools an AI agent may call (Model Context Protocol servers)",
             "EE-01": "keeps every AI agent execution inside a defended sandbox",
             "TP-15": "forces untrusted code the agent runs into an OS- or VM-isolated sandbox"}
    lines += ["## Top controls to harden", ""]
    top = sorted(control_ids(), key=lambda c: (-cov.get(c, 0), c))[:3]
    for cid in top:
        inc = ""
        if links.get(cid):
            inc = " Evidence: [incident summary](07-incident-summaries.md#" + links[cid][0]["anchor"] + ")."
        why = plain.get(cid, _outcome(cid, titles.get(cid, "")))
        lines.append(f"- **{cid}: {titles.get(cid,'')}** - {why}. Shown up by {cov.get(cid,0)} of the catalogue incidents.{inc}")
    lines += ["", "## Recommended next steps", "",
              "- Close the highest-evidenced gaps first - the controls most often shown up by real incidents are where hardening pays fastest.",
              "- Raise each pillar toward **L3** (automated, board-reported security), the level regulated Australian entities target.",
              "- Keep every control verified by an executable policy so posture is measured, not asserted.", "",
              "## What SHIELD-AI protects",
              "",
              "![What SHIELD-AI protects](../assets/diagrams/shield-ai-at-a-glance.svg)",
              "",
              "The seven pillars wrap the agent and the model. Each pillar is a set of controls -",
              "about the model, who and what it may touch, the data it handles, the tools it",
              "invokes, the monitoring around it, the governance over it, and the sandbox that",
              "contains it. Every control is verified by an executable policy you can run.",
              "",
              "## Where we stand",
              "",
              "![Where SHIELD-AI sits on the maturity curve](../assets/diagrams/pillar-maturity-heat.svg)",
              "",
              "The heat grid shows each pillar's position on the L1 (initial) to L4 (optimised)",
              "maturity curve - the target for Australian regulated entities is **L3**, the level",
              "at which security becomes automated and board-reported. The weakest pillar sets",
              "the organisation's overall maturity.", ""]
    for p in PILLARS:
        lv = mat.get(p, {})
        desc = lv.get("L3", "").strip()
        if not desc:
            continue
        lines.append(f"- **{p} ({PILLAR_FULL[p]}):** L3 target - {desc}.")
    lines += ["", "Every control in every pillar is verified by an executable policy, so posture is", "measured, not asserted. The field guide shows the exact checks: [06 · Technical", "Verification](06-controls-technical.md).", ""]
    return "\n".join(lines)


# ── Orchestration ────────────────────────────────────────────────────────

VIEW_FILES = [
    ("01-pillar-control-atlas.md", md_pillar_atlas),
    ("02-controls-incidents.md", md_incident_map),
    ("03-control-au-framework-matrix.md", md_au_matrix),
    ("04-pillar-maturity.md", md_maturity),
    ("05-controls-outcomes.md", md_control_outcomes),
    ("06-controls-technical.md", md_technical_controls),
    ("07-incident-summaries.md", md_incident_summaries),
    ("08-policy-coverage-heat.md", md_policy_coverage),
    ("09-assessment-scorecard.md", md_assessment_scorecard),
    ("10-implementation-roadmap.md", md_implementation_roadmap),
    ("11-executive-one-pager.md", md_executive_one_pager),
    ("README.md", md_readme),
]

DIAGRAMS = [
    ("pillar-control-atlas.svg", diagram_pillar_atlas),
    ("controls-incident-map.svg", diagram_incident_map),
    ("control-au-framework-matrix.svg", diagram_au_matrix),
    ("pillar-maturity-heat.svg", diagram_maturity_heat),
    ("control-outcomes-diagram.svg", diagram_control_outcomes),
    ("control-technical-sheet.svg", diagram_technical_sheet),
    ("policy-coverage-heat.svg", diagram_policy_coverage),
    ("shield-ai-at-a-glance.svg", diagram_shield_ai_at_a_glance),
    ("implementation-roadmap.svg", diagram_implementation_roadmap),
]


def generate_all():
    os.makedirs(DIAG_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)
    for name, fn in DIAGRAMS:
        path = os.path.join(DIAG_DIR, name)
        with open(path, "w") as f:
            f.write(fn())
        print(f"  {name}: {os.path.getsize(path):>6,} bytes")
    for name, fn in VIEW_FILES:
        path = os.path.join(VIEW_DIR, name)
        with open(path, "w") as f:
            f.write(fn().rstrip() + "\n")
        print(f"  reference-views/{name}: {os.path.getsize(path):>6,} bytes")


def check_all():
    """Verify outputs exist AND are byte-identical to a fresh in-memory
    regeneration from the committed sources.

    This is the source->view freshness guarantee: editing
    framework/shield-ai-framework.md or framework/shield-ai-gap-analysis.md
    without regenerating the reference views now fails `make check` with a
    precise list of stale files, instead of silently shipping a view that lags
    the framework. It also catches any hand-edit of a generated file (which
    would otherwise drift from what the generator produces next time).
    """
    ok = True
    fresh = []   # (is_diagram, name) currently matching a fresh regen
    missing = []
    stale = []
    for name, fn in DIAGRAMS:
        path = os.path.join(DIAG_DIR, name)
        want = fn()
        if not os.path.exists(path) or os.path.getsize(path) < 40:
            missing.append(name)
        elif open(path, encoding="utf-8").read() != want:
            stale.append(name)
        else:
            fresh.append((True, name))
    for name, fn in VIEW_FILES:
        path = os.path.join(VIEW_DIR, name)
        want = fn().rstrip() + "\n"
        if not os.path.exists(path) or os.path.getsize(path) < 20:
            missing.append(name)
        elif open(path, encoding="utf-8").read() != want:
            stale.append(name)
        else:
            fresh.append((False, name))
    if missing or stale:
        ok = False
        if missing:
            print(f"MISSING reference-view outputs: {missing}")
        if stale:
            print("STALE reference-view outputs (source changed or file hand-edited):")
            for name in sorted(stale):
                print(f"  - {name}")
            print("Regenerate with:  python3 tools/generate_reference_views.py")
            print("then commit the rebuilt views (this gate will pass only when")
            print("the committed files match a fresh regeneration).")
    else:
        for is_diagram, name in fresh:
            where = "assets/diagrams" if is_diagram else "reference-views"
            print(f"  OK  {where}/{name} (fresh)")
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check_all() else 1)
    else:
        generate_all()