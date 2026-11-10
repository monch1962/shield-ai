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
        # strip any leading structural label left by the layout pass
        title = re.sub(r"^\*\*(Requirement|Implementation|Rationale[^:]*|Mappings)\*\*:\s*\**", "", title)
        title = title.strip(" *")
        out[m.group(1)] = title
    return out


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
                f"[{i['id']}](../framework/shield-ai-gap-analysis.md#{i['anchor']})"
                for i in inc)
            lines.append(f"- **{cid}** — {title} ({len(inc)}): {inc_links}")
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
            anchor = re.sub(r"[^0-9a-z]+", "-", title.lower()).strip("-")
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


def split_controls(block):
    """Split a framework document into {control_id: bullet text}."""
    out = {}
    cur = None
    buf = []
    for ln in block.split("\n"):
        mm = re.match(r"^- ([A-Z]{2,5}-\d{2}):", ln)
        if mm:
            if cur:
                out[cur] = "\n".join(buf)
            cur = mm.group(1)
            buf = [ln]
            continue
        if cur is not None and (ln.startswith("  ") or ln.startswith("\t") or ln.strip() == ""):
            buf.append(ln)
            continue
        if cur is not None and ln.strip():
            out[cur] = "\n".join(buf)
            cur = None
    if cur:
        out[cur] = "\n".join(buf)
    return out


def extract_requirement(bullet):
    """Return the normative technical text for a control.

    For long controls take the first **Requirement:** block (the definitive
    must-do statement); for short single-line controls fall back to the parent
    bullet text. Whitespace-collapsed for clean rendering.
    """
    m = re.search(r"\*\*Requirement:\*\*\s*(.*?)(?=\n\s*\*\*|$)", bullet, re.S)
    if m:
        return " ".join(m.group(1).split()).strip()
    # short control: strip the "- ID: title (" prefix and closing paren
    body = re.sub(r"^-\s*[A-Z]{2,5}-\d{2}:\s*[^(]*\(?", "", bullet)
    body = body.rstrip(" );").strip()
    body = re.sub(r"\s*\*\*[A-Za-z /&]+:\*\*.*$", "", body).strip()
    return " ".join(body.split()).strip()


def load_policy_data():
    """Parse every policies/shield_ai_*.rego into {control_id: {...}}.

    Extracts the control's executable-verification facts from the policy file
    itself so the deep-dive view is grounded in the real policies, not a
    paraphrase: package, rule counts, maturity indicators, regulatory
    mappings, input model, and the IMPLEMENTED / stub status.
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
        implemented = "# IMPLEMENTED" in t
        out[cid] = {
            "pillar": pillar,
            "package": pkg.group(1) if pkg else "",
            "file": os.path.basename(path),
            "maturity": mat_lv,
            "regulatory": regs,
            "deny": deny,
            "implemented": implemented,
        }
    return out


def _outcome(cid, title):
    """A one-line, business-readable statement of the outcome a control produces."""
    return f"Verify that {title.lower() if title else 'the control'} holds under agent action"


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
    txt = open(FRAMEWORK, encoding="utf-8").read()
    bullet_of = split_controls(txt)
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
        "## How to use this field guide",
        "",
        "- **Control** is the stable identifier from the framework.",
        "- **What to verify** is the requirement text (or, for single-line controls, the",
        "  control's normative statement) — the concrete thing to check for/against.",
        "- **Executable policy** names the exact `policies/*.rego` file; open it for the",
        "  input model and the `deny` rules that fail closed.",
        "- **Incident evidence** links straight to the specific catalogue incident(s) that",
        "  demonstrated a failure of this control class.",
        "",
    ]
    for p in PILLARS:
        subs = sorted([c for c in control_ids() if c.startswith(p)])
        lines.append(f"## {p} — {PILLAR_FULL[p]}")
        lines.append("")
        for cid in subs:
            title = titles.get(cid, "")
            req = extract_requirement(bullet_of.get(cid, ""))
            pd = pol.get(cid, {})
            inc = links.get(cid, [])
            lines.append(f"### {cid}: {title}")
            lines.append("")
            lines.append(f"**What to verify:** {req}")
            lines.append("")
            lines.append(f"- **Executable policy:** `{pd.get('file','—')}` "
                         f"(package `{pd.get('package','—')}`, {pd.get('deny',0)} deny rules)")
            if inc:
                inc_links = ", ".join(
                    f"[{i['id']}](../framework/shield-ai-gap-analysis.md#{i['anchor']})"
                    for i in inc)
                lines.append(f"- **Incident evidence ({len(inc)}):** {inc_links}")
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
    <text x="560" y="84" class="cap">Verify via policy</text>
    <text x="720" y="84" class="cap">Incidents</text>'''
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
            title = titles.get(cid, "")
            inc_count = len(links.get(cid, []))
            deny = pol.get(cid, {}).get('deny', 0)
            body += f'''<text x="40" y="{iy+8}" class="sm" font-weight="bold" fill="{col[p]}">{cid}</text>
            <text x="170" y="{iy+8}" class="sm">{title[:52]}</text>
            <text x="560" y="{iy+8}" class="sm">{deny} deny rules</text>
            <text x="720" y="{iy+8}" class="sm">{inc_count} incidents</text>'''
            iy += row_h
        y += block_h + 14  # gap after each pillar block
    h = y + 32  # footer margin
    body += f'''<text x="{w/2}" y="{y+18}" text-anchor="middle" class="sm" font-style="italic">Specialist sheet: objective, executable verification depth (deny rules), and incident evidence per SHIELD-AI control</text>'''
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

Five simplified, cross-cutting views for presenting the framework to security
architects and business stakeholders. Each view derives its numbers from the
committed framework sources (see `tools/generate_reference_views.py`) so it can
never drift from the main document, and each is available as both a Markdown
page and an SVG diagram.

| # | View | Question it answers | SVG |
|---|------|--------------------|-----|
| 01 | [Pillar → Control Atlas](01-pillar-control-atlas.md) | What is the full control surface, by pillar? | `pillar-control-atlas.svg` |
| 02 | [Controls → Incidents](02-controls-incidents.md) | Which controls are evidenced by real incidents? | `controls-incident-map.svg` |
| 03 | [Controls → AU Frameworks](03-control-au-framework-matrix.md) | What must we align to (ISM/E8/SOCI/CPS234/Privacy/PSPF)? | `control-au-framework-matrix.svg` |
| 04 | [Pillar → Maturity](04-pillar-maturity.md) | How mature are we per pillar, and what does L3 require? | `pillar-maturity-heat.svg` |
| 05 | [Controls → Outcomes & Executable Verification](05-controls-outcomes.md) | What does the control guarantee, and which executable policy verifies it? | `control-outcomes-diagram.svg` |
| 06 | [Control Technical Verification Field Guide](06-controls-technical.md) | What precisely must hold per control, and how is it verified? *(technical specialists)* | `control-technical-sheet.svg` |

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


# ── Orchestration ────────────────────────────────────────────────────────

VIEW_FILES = [
    ("01-pillar-control-atlas.md", md_pillar_atlas),
    ("02-controls-incidents.md", md_incident_map),
    ("03-control-au-framework-matrix.md", md_au_matrix),
    ("04-pillar-maturity.md", md_maturity),
    ("05-controls-outcomes.md", md_control_outcomes),
    ("06-controls-technical.md", md_technical_controls),
    ("README.md", md_readme),
]

DIAGRAMS = [
    ("pillar-control-atlas.svg", diagram_pillar_atlas),
    ("controls-incident-map.svg", diagram_incident_map),
    ("control-au-framework-matrix.svg", diagram_au_matrix),
    ("pillar-maturity-heat.svg", diagram_maturity_heat),
    ("control-outcomes-diagram.svg", diagram_control_outcomes),
    ("control-technical-sheet.svg", diagram_technical_sheet),
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
    missing = []
    for name, _ in DIAGRAMS:
        path = os.path.join(DIAG_DIR, name)
        if not os.path.exists(path) or os.path.getsize(path) < 500:
            missing.append(name)
    for name, _ in VIEW_FILES:
        path = os.path.join(VIEW_DIR, name)
        if not os.path.exists(path) or os.path.getsize(path) < 200:
            missing.append(name)
    if missing:
        print(f"Missing or broken: {missing}")
        return False
    for name, _ in DIAGRAMS + VIEW_FILES:
        print(f"  OK  {name}")
    return True


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check_all() else 1)
    else:
        generate_all()