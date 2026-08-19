#!/usr/bin/env python3
"""
SHIELD-AI Diagram Generator
===========================
Generates SVG diagrams for the SHIELD-AI framework documents.
Produces clean, professional SVGs that render in Markdown (GitHub),
PDF (weasyprint), and EPUB (pandoc).

Usage:
  python3 tools/generate_diagrams.py             # generate all SVGs
  python3 tools/generate_diagrams.py --check     # verify SVGs exist
"""

import os, sys, textwrap

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "assets", "diagrams")

# ── Colours ────────────────────────────────────────────
NAVY  = "#0a1e3d"
BLUE  = "#1a3a6b"
GOLD  = "#d4a017"
LTBL  = "#dce6f0"
WHITE = "#ffffff"
TEXT  = "#1a1a2e"
MUTED = "#5a6a8a"
GRAY  = "#e8ecf0"
GREEN = "#22c55e"


def svg(w, h, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <style>
    text {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
    .title {{ font-size: 16px; font-weight: bold; fill: {NAVY}; }}
    .label {{ font-size: 12px; fill: {TEXT}; }}
    .sm {{ font-size: 10px; fill: {MUTED}; }}
    .gold {{ fill: {GOLD}; }}
    .white {{ fill: {WHITE}; }}
    .cap {{ font-size: 9px; font-weight: bold; text-transform: uppercase; fill: {MUTED}; }}
  </style>
  {body}
</svg>'''


def box(x, y, w, h, colour, label, sub, cap=""):
    """Render a rounded box with label and optional subtitle."""
    parts = f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{colour}" stroke="{BLUE}" stroke-width="1.5"/>
    <text x="{x + w/2}" y="{y + h/2 - 5}" text-anchor="middle" class="label" font-weight="bold">{label}</text>
    <text x="{x + w/2}" y="{y + h/2 + 10}" text-anchor="middle" class="sm">{sub}</text>'''
    if cap:
        parts += f'\n    <text x="{x + w/2}" y="{y + 14}" text-anchor="middle" class="cap">{cap}</text>'
    return parts


def arrow(x1, y1, x2, y2):
    """Vertical arrow from (x1,y1) to (x2,y2). Arrowhead at the end."""
    return f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#a)"/>'''


def arrow_head():
    return '''<defs>
      <marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="''' + BLUE + '''"/>
      </marker>
    </defs>'''


# ── Diagram 1: Framework Architecture ──────────────────

def diagram_architecture():
    """Seven pillars arranged bottom-to-top (P7 EE foundation -> P6 GRM top)."""
    w, h = 660, 520
    cx = 330       # centre X
    bw = 260       # box width
    bh = 45        # box height
    gap = 10       # gap between boxes
    arrow_gap = 8  # gap above arrowhead

    pillars = [
        ("P7  EXECUTION ENVIRONMENT",          "ISM | E8 | ASD Container Security Guidance", "EE-01 -> EE-08"),
        ("P1  MODEL SECURITY",                 "ISM | OWASP | NIST",                               "MS-01 -> MS-11"),
        ("P2  IDENTITY &amp; ACCESS",              "ISM | E8 | PSPF",                                  "IAM-01 -> IAM-09"),
        ("P3  DATA SECURITY",                  "Privacy Act | PSPF",                               "DS-01 -> DS-07"),
        ("P4  TOOL &amp; PIPELINE SECURITY",       "ISM | E8 | SOCI Act",                              "TP-01 -> TP-12"),
        ("P5  MONITORING &amp; INCIDENT RESPONSE",  "SOCI Act | APRA CPS 234 | Privacy NDB",           "MIR-01 -> MIR-06"),
        ("P6  GOVERNANCE &amp; RISK (GRM)",           "APRA CPS 234 | PSPF | Privacy Act | NIST AI RMF", "GRM-01 -> GRM-06"),
    ]

    # Bottom-to-top placement
    start_y = h - 65
    arr_l = []
    body = ""

    body += arrow(cx, 60, cx, 80)

    for i, (label, sub, cap) in enumerate(pillars):
        y = start_y - i * (bh + gap + arrow_gap)
        body += box(cx - bw/2, y, bw, bh, WHITE, label, sub, cap)
        # Arrow to next (above)
        if i < len(pillars) - 1:
            body += f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y - gap}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#a)"/>'

    body += arrow(cx, start_y + bh + 10, cx, h - 20)

    body = arrow_head() + body

    # Key at bottom
    body += f'''<text x="{cx}" y="{h - 8}" text-anchor="middle" class="sm" font-style="italic">Foundation (P7 EE) {'>>'} Oversight (P6 GRM) -- each pillar depends on those below it</text>'''

    return svg(w, h, textwrap.dedent(body))


# ── Diagram 2: Threat Landscape ────────────────────────

def diagram_threat():
    """Seven stacked layers: Model + Execution at bottom, Governance at top."""
    w, h = 580, 520
    cx = w / 2
    bw = 400
    bh = 46
    gap = 8

    layers = [
        ("GOVERNANCE", "[GOV]  Shadow AI | Missing audit trails | Incident reconstruction"),
        ("PIPELINE",   "[PPL]  CI/CD compromise | Model substitution | Chain poisoning"),
        ("IDENTITY",   "[ID]   Credential abuse | Session hijack | Escalation"),
        ("DATA",       "[DAT]  Cross-session aggregation | RAG poisoning | PII leak"),
        ("TOOLS",      "[TUL]  Tool output injection | Malicious registration | API abuse"),
        ("EXECUTION",  "[EXE]  Sandbox escape | Host-file injection | Fail-open fallback"),
        ("MODEL",      "[MDL]  Prompt injection | Jailbreaking | Model inversion"),
    ]

    body = ""
    for i, (layer, content) in enumerate(layers):
        y = h - 70 - i * (bh + gap)
        colour = WHITE
        body += box(cx - bw/2, y, bw, bh, colour, layer, content)
        if i < len(layers) - 1:
            body += f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y - gap}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#a)"/>'

    body += f'''<text x="{cx}" y="{h - 8}" text-anchor="middle" class="sm" font-style="italic">Risk compounds upward: an escaped sandbox invalidates every layer above it</text>'''

    return svg(w, h, arrow_head() + body)


# ── Diagram 3: Maturity Journey ─────────────────────────

def diagram_maturity():
    """L1-L4 staircase with characteristics per level."""
    w, h = 700, 400
    lx = 180    # level label X
    cx = 420    # content X
    bw = 400    # box width
    bh = 60
    gap = 12

    levels = [
        ("L4  OPTIMISED", "Continuous improvement | Automated red-teaming | AI-specific SIEM | Real-time dashboard", GOLD),
        ("L3  DEFINED",   "Automated controls | Regulatory mapping complete | Anomaly detection | Board reporting", BLUE),
        ("L2  MANAGED",   "Documented controls | Per-agent service accounts | Basic monitoring | Vendor assessments", "#4a7a9c"),
        ("L1  INITIAL",   "Ad-hoc controls | No formal governance | Shared credentials | Basic logging", "#8a9ab0"),
    ]

    body = ""

    # Side staircase indicator
    stair_y = h - 80
    step_w = 40
    step_h = (stair_y - 30) / 4
    for i in range(4):
        sy = stair_y - i * step_h
        body += f'''<rect x="30" y="{sy - step_h}" width="{step_w + i * 10}" height="{step_h}" rx="3" fill="{levels[i][2]}" opacity="0.15"/>
        <text x="{30 + (step_w + i * 10)/2}" y="{sy - step_h/2 + 4}" text-anchor="middle" class="sm" fill="{levels[i][2]}" font-weight="bold">L{4-i}</text>'''

    # Labels beside the staircase
    labels = ["Foundational", "Managed", "Proactive", "Adaptive"]
    for i, lbl in enumerate(labels):
        y = stair_y - i * step_h - step_h/2 + 4
        body += f'''<text x="{30 + step_w + i * 10 + 50}" y="{y}" text-anchor="middle" class="cap">{lbl.upper()}</text>
        <line x1="{30 + step_w + i * 10 + 8}" y1="{y + 6}" x2="{30 + step_w + i * 10 + 28}" y2="{y + 6}" stroke="{MUTED}" stroke-width="1"/>'''

    # Level description boxes
    for i, (level, content, colour) in enumerate(levels):
        y = stair_y - (3 - i) * step_h
        body += box(lx, y - bh/2, bw, bh, WHITE, level, content)
        body += f'''<rect x="{lx}" y="{y - bh/2}" width="6" height="{bh}" rx="3" fill="{colour}"/>'''

    # Time estimate bar at bottom
    bar_y = h - 20
    body += f'''<text x="50" y="{bar_y}" class="sm" font-weight="bold">Typical progression:</text>'''
    segments = [("3-4 months", 0.2), ("8-12 months", 0.3), ("12+ months", 0.3)]
    sx = 220
    for seg_name, seg_w in segments:
        sw = int(seg_w * 300)
        body += f'''<rect x="{sx}" y="{bar_y - 5}" width="{sw}" height="12" rx="2" fill="{LTBL}" stroke="{BLUE}" stroke-width="1"/>
        <text x="{sx + sw/2}" y="{bar_y + 4}" text-anchor="middle" class="sm">{seg_name}</text>'''
        sx += sw + 4

    body += f'''<text x="{sx + 20}" y="{bar_y + 4}" class="sm" font-style="italic">Weakest pillar determines overall maturity</text>'''

    return svg(w, h, body)


# ── Diagram 4: Delivery Flow ────────────────────────────

def diagram_delivery():
    """Five-phase horizontal flow: Discover -> Assess -> Design -> Implement -> Assure."""
    w, h = 750, 280
    bw = 120
    bh = 55
    gap = 20
    phases = [
        ("1", "DISCOVER", "Weeks 1-2", "Inventory + Regs Map"),
        ("2", "ASSESS", "Weeks 3-4", "Gap Analysis + Scores"),
        ("3", "DESIGN", "Weeks 5-8", "Architecture + Roadmap"),
        ("4", "IMPLEMENT", "Weeks 9-16", "Controls + Training"),
        ("5", "ASSURE", "Ongoing", "Reviews + Updates"),
    ]

    total_w = len(phases) * bw + (len(phases)-1) * gap
    start_x = (w - total_w) / 2

    body = ""

    for i, (num, name, time, out) in enumerate(phases):
        x = start_x + i * (bw + gap)
        y = 80

        # Phase box
        body += box(x, y, bw, bh, WHITE, f"{name}", time)
        # Number circle
        body += f'''<circle cx="{x + bw/2}" cy="{y - 18}" r="14" fill="{NAVY}"/>
        <text x="{x + bw/2}" y="{y - 13}" text-anchor="middle" class="white" font-size="11" font-weight="bold">{num}</text>'''

        # Output label below
        body += f'''<text x="{x + bw/2}" y="{y + bh + 18}" text-anchor="middle" class="sm" font-style="italic">{out}</text>'''

        # Arrow to next
        if i < len(phases) - 1:
            ax = x + bw
            ay = y + bh / 2
            body += f'''<line x1="{ax}" y1="{ay}" x2="{ax + gap}" y2="{ay}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a)"/>'''

    # Maturity scope below
    tier_y = y + bh + 55
    body += f'''<text x="{start_x}" y="{tier_y}" class="sm" font-weight="bold">Scope by maturity:</text>'''
    scopes = [
        ("L1-L2: Phases 1-2", start_x + 110, NAVY),
        ("L2-L3: Phases 1-4", start_x + 260, BLUE),
        ("L3-L4: Phases 1-5", start_x + 410, GOLD),
    ]
    for sname, sx, scol in scopes:
        body += f'''<rect x="{sx}" y="{tier_y - 12}" width="120" height="20" rx="10" fill="{scol}" opacity="0.15"/>
        <text x="{sx + 60}" y="{tier_y + 3}" text-anchor="middle" class="sm" fill="{scol}" font-weight="bold">{sname}</text>'''

    # Arrow marker definition
    body = arrow_head() + body

    # Title
    body += f'''<text x="{w/2}" y="35" text-anchor="middle" class="title">SHIELD-AI(TM) Delivery Methodology</text>'''

    return svg(w, h, body)


# ── Main ────────────────────────────────────────────────

def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    diagrams = [
        ("framework-architecture.svg", diagram_architecture()),
        ("threat-landscape.svg",       diagram_threat()),
        ("maturity-journey.svg",       diagram_maturity()),
        ("delivery-flow.svg",          diagram_delivery()),
    ]
    for name, content in diagrams:
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, 'w') as f:
            f.write(content)
        size = os.path.getsize(path)
        print(f"  {name}: {size:>6,} bytes")

    # Also generate a combined SVG index for quick reference
    print(f"\nGenerated {len(diagrams)} SVGs in {OUTPUT_DIR}/")


def check_all():
    """Verify all expected SVGs exist and have content."""
    expected = ["framework-architecture.svg", "threat-landscape.svg",
                "maturity-journey.svg", "delivery-flow.svg"]
    missing = []
    for name in expected:
        path = os.path.join(OUTPUT_DIR, name)
        if not os.path.exists(path):
            missing.append(name)
        elif os.path.getsize(path) < 500:
            missing.append(f"{name} (too small: {os.path.getsize(path)} bytes)")

    if missing:
        print(f"Missing or broken: {missing}")
        return False
    else:
        for name in expected:
            path = os.path.join(OUTPUT_DIR, name)
            print(f"  OK  {name} ({os.path.getsize(path):,} bytes)")
        return True


if __name__ == "__main__":
    if "--check" in sys.argv:
        check_all()
    else:
        generate_all()
