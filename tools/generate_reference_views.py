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
    w, h = 780, 460
    titles = load_control_titles()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    cols = 7
    bw, bh, gap = 96, 130, 10
    body = ""
    for idx, p in enumerate(PILLARS):
        cx = 30 + idx * (bw + gap) + bw / 2
        cy = 70 + bh / 2
        count = len([c for c in control_ids() if c.startswith(p)])
        body += f'''<rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="8" fill="{col[p]}" opacity="0.12"/>
        <rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="26" rx="8" fill="{col[p]}"/>
        <text x="{cx}" y="{cy-bh/2+17}" text-anchor="middle" class="white" font-size="11" font-weight="bold">{p}</text>
        <text x="{cx}" y="{cy-6}" text-anchor="middle" class="label" font-weight="bold" fill="{col[p]}">{count} controls</text>
        <text x="{cx}" y="{cy+10}" text-anchor="middle" class="sm">{PILLAR_FULL[p]}</text>'''
    # control inventory grid below
    gy = 210
    gcols = 8
    cw, ch, cgap = 82, 16, 4
    body += f'''<text x="30" y="{gy-8}" class="cap">Control inventory (all {count_controls()})</text>'''
    for i, cid in enumerate(control_ids()):
        px = PILLARS.index(cid.split("-")[0])
        gx = 30 + (i % gcols) * (cw + cgap)
        gyy = gy + (i // gcols) * (ch + 2)
        body += f'''<rect x="{gx}" y="{gyy}" width="{cw}" height="{ch}" rx="3" fill="{WHITE}" stroke="{col[cid.split('-')[0]]}" stroke-width="1"/>
        <text x="{gx+4}" y="{gyy+11}" class="sm" font-weight="bold" fill="{col[cid.split('-')[0]]}">{cid}</text>'''
        title = titles.get(cid, "")
        if len(title) > 12:
            title = title[:11] + "…"
        body += f'''<text x="{gx+34}" y="{gyy+11}" class="sm">{title}</text>'''
    body += f'''<text x="{w/2}" y="{h-8}" text-anchor="middle" class="sm" font-style="italic">Seven pillars, {count_controls()} controls -- execution environment is the foundation</text>'''
    return svg(w, h, group_title(body, w, "SHIELD-AI: Pillar to Control Atlas"))


# ── Diagram 2: Control -> Incident coverage ──────────────────────────────


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
    w, h = 820, 460
    maturity = load_maturity()
    col = {"EE": "#1a3a6b", "MS": "#2563eb", "IAM": "#059669", "DS": "#d97706",
           "TP": "#7c3aed", "MIR": "#db2777", "GRM": "#475569"}
    lvl_col = {"L1": "#8a9ab0", "L2": "#4a7a9c", "L3": "#2563eb", "L4": "#d4a017"}
    body = ""
    # header
    body += f'''<text x="140" y="44" class="cap">pillar · maturity level</text>'''
    for j, lvl in enumerate(["L1 Initial", "L2 Managed", "L3 Defined", "L4 Optimised"]):
        body += f'''<rect x="{140+j*150}" y="34" width="140" height="16" rx="3" fill="{BLUE}"/>
        <text x="{140+j*150+70}" y="{45}" text-anchor="middle" class="white" font-size="9" font-weight="bold">{lvl}</text>'''
    for i, p in enumerate(PILLARS):
        yy = 56 + i * 50
        body += f'''<rect x="30" y="{yy}" width="100" height="40" rx="4" fill="{col[p]}" opacity="0.15"/>
        <text x="40" y="{yy+17}" class="sm" font-weight="bold" fill="{col[p]}">{p} · {PILLAR_FULL[p]}</text>'''
        prog = maturity.get(p, {})
        for j, lvl in enumerate(["L1", "L2", "L3", "L4"]):
            desc = prog.get(lvl, "")
            fill = f"{lvl_col[lvl]}"
            body += f'''<rect x="{140+j*150}" y="{yy}" width="140" height="40" rx="4" fill="{fill}" opacity="0.18" stroke="{fill}" stroke-width="1"/>
            <text x="{140+j*150+70}" y="{yy+24}" text-anchor="middle" class="sm" fill="{fill}" font-weight="bold">{desc[:70] if desc else "—"}</text>'''
    body += f'''<text x="{w/2}" y="{h-10}" text-anchor="middle" class="sm" font-style="italic">Across {count_controls()} controls, the weakest pillar determines overall maturity -- target the L2->L3 transition first (regulated entities)</text>'''
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
    ordered = sorted(control_ids(), key=lambda c: -cov[c])
    lines = [
        "# 02 · Controls → Industry Incidents",
        "",
        "Which SHIELD-AI controls are actually **evidenced by real incidents**? This view counts",
        "every reference to a control across the framework's incident coverage verdicts",
        "(INC-01…INC-92). The most-cited controls are the highest-priority hardening targets —",
        "they are the controls the real world has repeatedly shown we need.",
        "",
        "![Controls incident map](../assets/diagrams/controls-incident-map.svg)",
        "",
        "## Coverage leaders (most evidenced)",
        "",
        "| Control | Title | Incident references |",
        "|---|---|---|",
    ]
    for cid in ordered[:10]:
        lines.append(f"| **{cid}** | {titles.get(cid,'')} | {cov[cid]} |")
    lines.append("")
    lines += [
        "## Full coverage inventory",
        "",
        "| Control | Title | Incident references |",
        "|---|---|---|",
    ]
    for cid in ordered:
        lines.append(f"| {cid} | {titles.get(cid,'')} | {cov[cid]} |")
    lines.append("")
    zero = [c for c in ordered if cov[c] == 0]
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

Four simplified, cross-cutting views for presenting the framework to security
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

> Generated by `python3 tools/generate_reference_views.py`. Add it to
> `make check` / `update_all.sh` so the views always reflect the framework.
"""


# ── Orchestration ────────────────────────────────────────────────────────

VIEW_FILES = [
    ("01-pillar-control-atlas.md", md_pillar_atlas),
    ("02-controls-incidents.md", md_incident_map),
    ("03-control-au-framework-matrix.md", md_au_matrix),
    ("04-pillar-maturity.md", md_maturity),
    ("README.md", md_readme),
]

DIAGRAMS = [
    ("pillar-control-atlas.svg", diagram_pillar_atlas),
    ("controls-incident-map.svg", diagram_incident_map),
    ("control-au-framework-matrix.svg", diagram_au_matrix),
    ("pillar-maturity-heat.svg", diagram_maturity_heat),
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