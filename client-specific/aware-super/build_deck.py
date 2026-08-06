#!/usr/bin/env python3
"""Build the SHIELD-AI Aware Super briefing deck (.pptx) with SVG-derived diagrams.
Humanised copy: plain professional voice, written for an APRA-regulated super fund
starting its production AI journey."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
import os

import os, sys, subprocess, json, datetime

REPO = "/home/davidm/Projects/shield-ai"
CLIENT_DIR = "/home/davidm/Projects/shield-ai/client-specific/aware-super"
IMG = "/tmp/deck-imgs"
os.makedirs(IMG, exist_ok=True)

DIAGRAMS = ["framework-architecture-updated", "threat-landscape-updated", "impl-reference-architecture", "impl-policy-decision-points", "impl-request-flow", "maturity-journey", "aware-super-alignment"]

def render_png(name):
    base = name[:-4] if name.endswith(".png") else name
    png = os.path.join(IMG, base + ".png")
    if os.path.exists(png):
        return png
    svg = next((p for p in (os.path.join(CLIENT_DIR, base + ".svg"), os.path.join(REPO, "assets", "diagrams", base + ".svg")) if os.path.exists(p)), None)
    if svg is None:
        raise SystemExit("missing svg for " + base)
    code = "import cairosvg; cairosvg.svg2png(url='%s', write_to='%s', output_width=1600)" % (svg, png)
    for py in (sys.executable, "/tmp/svgvenv/bin/python"):
        try:
            subprocess.run([py, "-c", code], check=True, capture_output=True)
            return png
        except Exception:
            continue
    raise SystemExit("cannot render " + base)

DECK_VERSION = "1.0"
AUDIENCE = "Aware Super"
OUT = "/home/davidm/Projects/shield-ai/client-specific/aware-super/shield-ai-deck-aware-super.pptx"
MANIFEST = "/home/davidm/Projects/shield-ai/client-specific/aware-super/deck-manifest.json"

NAVY = RGBColor(0x0A, 0x1E, 0x3D)
NAVY2 = RGBColor(0x1A, 0x3A, 0x6B)
GOLD = RGBColor(0xD4, 0xA0, 0x17)
RED = RGBColor(0xEF, 0x44, 0x44)
INK = RGBColor(0x1A, 0x1A, 0x2E)
MUTED = RGBColor(0x5A, 0x6A, 0x8A)
LIGHT = RGBColor(0xF5, 0xF6, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

SW, SH = 13.333, 7.5


def slide():
    return prs.slides.add_slide(BLANK)


def box(s, l, t, w, h):
    tb = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    return tf


def para(tf, text, size=14, bold=False, color=INK, level=0, space_after=6, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.level = level
    p.space_after = Pt(space_after)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FONT
    return p


def rect(s, l, t, w, h, fill=NAVY, line=None, line_w=None):
    from pptx.enum.shapes import MSO_SHAPE
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w or 1)
    sh.shadow.inherit = False
    return sh


def header(s, title, kicker=None, page=None):
    rect(s, 0, 0, SW, 0.95, fill=NAVY)
    rect(s, 0, 0.95, SW, 0.06, fill=GOLD)
    tf = box(s, 0.6, 0.16, 11.4, 0.7)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = title
    r.font.size = Pt(26); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
    if kicker:
        tf2 = box(s, 0.6, 0.62, 11.0, 0.3)
        p2 = tf2.paragraphs[0]
        r2 = p2.add_run(); r2.text = kicker
        r2.font.size = Pt(11); r2.font.color.rgb = RGBColor(0xC9, 0xD4, 0xE8); r2.font.name = FONT
    footer(s, page)


def footer(s, page=None):
    rect(s, 0, 7.28, SW, 0.22, fill=LIGHT)
    tf = box(s, 0.6, 7.3, 9.0, 0.18)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "SHIELD-AI(TM)  |  Aware Super Briefing  |  Deck v%s  |  Framework v1.5  |  Aug 2026" % DECK_VERSION
    r.font.size = Pt(9); r.font.color.rgb = MUTED; r.font.name = FONT
    if page is not None:
        tf2 = box(s, 12.3, 7.3, 0.7, 0.18)
        p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
        r2 = p2.add_run(); r2.text = str(page)
        r2.font.size = Pt(9); r2.font.color.rgb = MUTED; r2.font.name = FONT


def bullets_slide(title, items, kicker=None, page=None, notes=None, body_top=1.35):
    s = slide()
    header(s, title, kicker, page)
    tf = box(s, 0.7, body_top, 12.0, 5.6)
    first = True
    for it in items:
        text, level = it[0], it[1]
        bold = it[2] if len(it) > 2 else False
        color = it[3] if len(it) > 3 else INK
        para(tf, text, size=16 if level == 0 else 13, bold=bold, color=color, level=level,
             space_after=8 if level == 0 else 4, first=first)
        first = False
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def diagram_slide(title, img, kicker=None, page=None, notes=None, box_l=0.7, box_t=1.35, box_w=11.93, box_h=5.6,
                  caption=None):
    s = slide()
    header(s, title, kicker, page)
    path = render_png(img)
    im = Image.open(path)
    ar = im.width / im.height
    box_ar = box_w / box_h
    if ar > box_ar:
        w = box_w; h = w / ar
    else:
        h = box_h; w = h * ar
    l = box_l + (box_w - w) / 2
    t = box_t + (box_h - h) / 2
    s.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w))
    if caption:
        tf = box(s, 0.7, 6.95, 11.93, 0.3)
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = caption
        r.font.size = Pt(10); r.font.italic = True; r.font.color.rgb = MUTED; r.font.name = FONT
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def pillar_card(s, num, name, ctrl_range, tagline):
    card_w, card_h = 3.0, 4.6
    l, t = 9.9, 1.7
    rect(s, l, t, card_w, card_h, fill=LIGHT, line=NAVY2, line_w=1.25)
    rect(s, l, t, card_w, 1.15, fill=NAVY2)
    tf = box(s, l + 0.2, t + 0.12, card_w - 0.4, 0.95)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = f"PILLAR {num}"
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
    p2 = tf.add_paragraph()
    r2 = p2.add_run(); r2.text = name
    r2.font.size = Pt(13); r2.font.bold = True; r2.font.color.rgb = GOLD; r2.font.name = FONT
    tf2 = box(s, l + 0.2, t + 1.3, card_w - 0.4, card_h - 1.5)
    para(tf2, ctrl_range, size=12, bold=True, color=NAVY, space_after=8, first=True)
    para(tf2, tagline, size=11.5, color=INK, space_after=0)


def pillar_slide(title, num, name, ctrl_range, tagline, items, notes=None, page=None):
    s = slide()
    header(s, title, f"Pillar {num} of 7  |  {name}", page)
    tf = box(s, 0.7, 1.4, 8.9, 5.5)
    first = True
    for it in items:
        text, level = it[0], it[1]
        bold = it[2] if len(it) > 2 else False
        color = it[3] if len(it) > 3 else INK
        para(tf, text, size=15 if level == 0 else 12.5, bold=bold, color=color, level=level,
             space_after=9 if level == 0 else 5, first=first)
        first = False
    pillar_card(s, num, name, ctrl_range, tagline)
    footer(s, page)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def watchlist_slide(page):
    from pptx.util import Inches as IN
    s = slide()
    header(s, "Future Threats on the SHIELD-AI Watchlist",
           "Six components under active monitoring; the watchlist is rebuilt monthly by the deep review", page)
    rows, cols = 7, 3
    tbl_shape = s.shapes.add_table(rows, cols, IN(0.7), IN(1.35), IN(11.93), IN(4.95))
    tbl = tbl_shape.table
    tbl.columns[0].width = IN(2.55)
    tbl.columns[1].width = IN(4.85)
    tbl.columns[2].width = IN(4.53)
    hdr = ["Future threat", "What is happening", "Why it matters to SHIELD-AI"]
    data = [
        ("IETF agent-to-agent (A2A) standardisation",
         "Protocol ratification talks may normalise multi-hop agent delegation",
         "Could defeat the two-hop delegation bound (IAM-02/07); delegation-chain amplification"),
        ("Open Secure AI Alliance / NOOA",
         "NVIDIA and 36 partners, open-sourced guidance (July 2026)",
         "Divergence risk if NOOA guidance contradicts a SHIELD-AI control; a mapping question for GRM-05"),
        ("Time-based supply-chain defences",
         "TrapDoor (34 packages across npm, PyPI, Crates) showed token-age gates",
         "The fresh-credential problem: agent publishers hold fresh tokens, so age-based gates miss agent-originated publication (DS-07)"),
        ("Edge and on-device agents",
         "Models like Gemma 4 12B run locally, outside the data centre",
         "MS-09 needs a perception-channel extension (screen, OCR); on-device agents open a MIR-01 telemetry gap"),
        ("Inbound MCP exposure",
         "OX Security 'by design' flaw (200K servers, 150M downloads); Wiz research; Metasploit 6.5 now ships an MCP server",
         "Strongest promotion candidate: extend TP-10 to standalone MCP servers"),
        ("Adversary-owned autonomous agents",
         "Unit 42 documented self-scanning campaigns; agent-as-a-service is spreading",
         "Prevention cannot keep pace; rely on detection (MIR-02), automated response (MIR-04), and a tested kill switch (GRM-02)"),
    ]
    for c, h in enumerate(hdr):
        cell = tbl.cell(0, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY2
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; r = p.add_run(); r.text = h
        r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
    for ri, row in enumerate(data, start=1):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT if ri % 2 == 0 else WHITE
            tf = cell.text_frame; tf.word_wrap = True
            tf.margin_left = IN(0.08); tf.margin_right = IN(0.08)
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = val
            r.font.size = Pt(10.5)
            r.font.bold = (ci == 0)
            r.font.color.rgb = NAVY if ci == 0 else INK
            r.font.name = FONT
    tf_note = box(s, 0.7, 6.45, 11.93, 0.7)
    para(tf_note, "Each item carries a decision gate: when the gate fires, the item is promoted from watchlist to control.", size=11.5, color=MUTED, first=True, space_after=3)
    para(tf_note, "Queued for the September deep review: inbound MCP exposure (extending TP-10) and A2A standardisation (extending IAM-07).", size=11.5, color=MUTED)
    footer(s, page)
    s.notes_slide.notes_text_frame.text = ("One minute. These are not controls yet; they are the things the framework watches month to month. "
        "Each has a decision gate, and when a gate fires the item gets promoted into a control. Two candidates are already queued "
        "for the September deep review: inbound MCP exposure, which would extend TP-10 to standalone MCP servers, and A2A "
        "standardisation, which would extend the delegation-chain controls. The full watchlist report is rebuilt every month.")
    return s


# ============ SLIDES ============
page = 1

# 1 — Title
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 4.62, SW, 0.06, fill=GOLD)
tf = box(s, 1.0, 1.7, 11.3, 1.6)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "SHIELD-AI(TM)"
r.font.size = Pt(54); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
p2 = tf.add_paragraph()
r2 = p2.add_run(); r2.text = "Securing Production AI for Aware Super"
r2.font.size = Pt(24); r2.font.color.rgb = GOLD; r2.font.name = FONT
tf2 = box(s, 1.0, 4.9, 11.3, 1.9)
para(tf2, "Security and Holistic Integrity for Enterprise-Level Deployment of AI", size=16, color=RGBColor(0xC9,0xD4,0xE8), first=True, space_after=10)
para(tf2, "An Australian framework for APRA-regulated entities: 7 pillars, 55 controls, 4 maturity levels, policy as code", size=14, color=RGBColor(0xC9,0xD4,0xE8), space_after=10)
para(tf2, "Briefing  |  Framework v1.5  |  August 2026", size=12, color=MUTED)
s.notes_slide.notes_text_frame.text = ("Thirty minutes, so let's move. Aware Super is starting to put AI into production, and the honest position is "
    "that the security playbook for that is young. SHIELD-AI is an Australian framework built for agents that act, structured so a "
    "security and risk team can explain it to a trustee board in under half an hour. That is what we are about to do.")

# 2 — Agenda
bullets_slide("Presentation Overview", [
    ("1.  Why AI security matters for a super fund now", 0, True),
    ("2.  The framework: seven pillars and 55 controls", 0, True),
    ("3.  How it works: reference implementation, policy as code, request flow", 0, True),
    ("4.  Applying it at Aware Super: regulation, maturity, a practical starting point", 0, True),
    ("A note up front: every claim in this deck is tied to a documented incident", 0, True),
], kicker="Four parts, 30 minutes", page=page, notes="Set the expectation: questions at the end, and the evidence for every claim is in the framework documents. This deck is about production AI, not experiments."); page += 1

# 3 — Why it matters
bullets_slide("Why AI Security Matters for a Super Fund Now", [
    ("An agent does not just answer. It invokes tools, writes code, and acts under delegated authority", 0, True),
    ("For a super fund, the asset in play is member data, and it lives for decades", 0, True),
    ("The failures are documented, and they are not exotic:", 0),
    ("Sandbox escapes hit production agent platforms between March and July 2026 (OpenAI, Hugging Face, Cursor, AWS AgentCore, ServiceNow)", 1),
    ("CVE-2026-10591: hidden 1px text on a page rewrote an agent's MCP registry and ran attacker code on the host", 1),
    ("CVE-2026-25253: a crafted link hijacked a loopback agent gateway, switched off approvals, and escaped to the host", 1),
    ("An agent under evaluation published a malicious package to PyPI; 15 real systems ran it for about three months", 1),
    ("APRA already expects a security capability across the entity (CPS 234) and 72-hour incident notification. AI does not remove that obligation; it widens it", 0, True, RED),
], kicker="Why now", page=page, notes="Two minutes. Lead with the shift from chat to action, then land the super-specific point: member data held for decades is a different exposure profile than most enterprises face. APRA will ask how AI is secured under CPS 234; this deck is the answer framework."); page += 1

# 4 — Where AI touches a super fund
bullets_slide("Where AI Will Touch Member Outcomes", [
    ("Every place a model meets member data is a place that needs controls", 0, True),
    ("Member-facing chatbots and guidance: member data in prompts, answers that must not drift into advice", 1),
    ("Fraud and AML detection: models scoring transactions and member events", 1),
    ("Document processing: rollovers, claims, insurance forms, correspondence", 1),
    ("Call transcription and contact-centre analytics", 1),
    ("Internal copilots: support staff, risk, investments, legal", 1),
    ("Investment and risk analytics: research assistants, code generation, report drafting", 1),
    ("The pattern is the same everywhere: a model, a tool, and member data in between", 0, True, NAVY2),
], page=page, notes="Ninety seconds. This slide is the bridge to the threat model: the fund does not need to imagine exotic AI use cases, the use cases are already on the roadmap. The security question is the same for each one."); page += 1

# 5 — Attack surface
diagram_slide("The Agentic AI Attack Surface", "threat-landscape-updated.png",
              kicker="Seven layers; risk compounds upward", page=page,
              notes="Two minutes. Walk the stack bottom to top: a model compromise opens tool abuse, which opens data exfiltration, which slips past identity controls unless monitoring and governance are in place. For a super fund, 'data exfiltration' reads as member PII leaving the environment.", caption="Risk compounds upward from the model to the data."); page += 1

# 6 — Where current controls fall short
bullets_slide("Where Current Controls Come Up Short", [
    ("CPS 234, ISM, and the Essential Eight are strong on traditional cyber, but they predate autonomous agents", 0, True),
    ("The gaps are structural, not incremental:", 0),
    ("Tool access: agents read and write member systems, APIs, and files; no user-centric threat model fully covers that", 1),
    ("Identity delegation: the agent acts under a staff member's authority, often with no bound on the chain", 1),
    ("Sandbox containment: escape is the failure mode we see in the field, not a hypothetical", 1),
    ("Protocol layer: MCP endpoints, tool metadata, and control planes are surface nobody owned until recently", 1),
    ("Evaluation harnesses: isolation gets asserted in config, but nobody verifies it holds", 1),
    ("APRA guidance on AI is emerging, and the proposed AU Mandatory Guardrails point the direction; neither is a control set yet", 0, True),
    ("SHIELD-AI fills that gap, and it maps directly onto the obligations the fund already operates under", 0, True, NAVY2),
], page=page, notes="Ninety seconds. Position SHIELD-AI as complementary to CPS 234 and the E8, not a replacement. The last line hands off to the framework section."); page += 1

# 7 — At a glance
bullets_slide("SHIELD-AI at a Glance", [
    ("Seven security pillars across the whole agentic-AI stack", 0, True),
    ("Model Security, Identity and Access, Data Security, Tool and Pipeline Security, Monitoring and IR, Governance and Risk, Execution Environment", 1),
    ("55 controls, each with implementation guidance and a maturity progression", 0, True),
    ("Four maturity levels, consistent with ISM and the Essential Eight: L1 Initial, L2 Managed, L3 Defined, L4 Optimised", 0, True),
    ("Policy as code: 55 executable Rego controls, evaluated deny-override", 0, True),
    ("A deployable reference implementation: gateway, policy engine, identity plane, observability", 0, True),
    ("Evidence driven: 25 documented incidents, 19 identified gaps, monthly deep review, a live watchlist", 0, True),
    ("Aligned to what a trustee must answer to: CPS 234, CPG 230, the Privacy Act, ASIC, and the proposed AU Guardrails", 0, True, NAVY2),
], page=page, notes="One minute. The thirty second version: seven pillars, 55 controls, L1 to L4, policy as code, evidence driven. Say it plainly and move on."); page += 1

# 8 — Seven pillars diagram
diagram_slide("The Seven Pillars", "framework-architecture-updated.png",
              kicker="Execution Environment at the base; Governance at the top", page=page,
              notes="Two minutes. The ordering carries the argument: EE sits at the base because an escapable sandbox invalidates every control above it, and GRM sits at the top because without governance the controls erode. Each pillar leans on the ones below it.",
              caption="Each pillar depends on all pillars below it."); page += 1

# 9-15 — Pillars
pillar_slide("Pillar 1: Model Security", 1, "Model Security", "MS-01 .. MS-09  |  9 controls",
    "The model is a data asset too",
    [
    ("Models trained or used on member data need the same protection as any information asset", 0, True),
    ("MS-01  Weight protection: encrypted at rest and in transit, HSM-backed keys", 1),
    ("MS-02/03  Training data integrity and model supply chain: provenance, signed checkpoints, SBOM", 1),
    ("MS-04  Adversarial robustness: prompt-injection testing and jailbreak evaluation, plus sanitisation against imperceptible content (zero-opacity and 1px text, hidden PR comments)", 1),
    ("MS-08  MCP security: signed tool metadata, an authenticated MCP gateway, response schema validation", 1),
    ("MS-09  Perception-fidelity: approvals bind to what the human can actually see", 1),
], notes="Ninety seconds. The key mental shift: a model is an information asset in the CPS 234 sense. MS-09 exists because hidden text defeated a human approval step in a real incident.", page=page); page += 1

pillar_slide("Pillar 2: Identity and Access", 2, "Identity & Access", "IAM-01 .. IAM-09  |  9 controls",
    "Member records, scoped tightly",
    [
    ("This pillar decides what the agent can do, what it can reach, and whose authority it carries", 0, True),
    ("IAM-01  A distinct, auditable identity per agent; no shared staff credentials", 1),
    ("IAM-02  Scope-bound delegation: no wildcard permissions, no self-escalation", 1),
    ("IAM-07  Delegation chains capped at two hops (human to agent to tool) and fully reconstructable from audit logs", 1),
    ("IAM-05  Just-in-time credentials: ephemeral, auto-revoked, no standing agent access", 1),
    ("IAM-09  Multi-tenant agent platforms isolated at the data layer (CVE-2026-55255, the first agent platform on the CISA KEV list)", 1),
], notes="Ninety seconds. The two hop bound is the headline: human to agent to tool, and the infrastructure blocks anything further. For member records, least privilege is not a nice to have.", page=page); page += 1

pillar_slide("Pillar 3: Data Security", 3, "Data Security", "DS-01 .. DS-07  |  7 controls",
    "Member data, everywhere it flows",
    [
    ("Data controls cover the whole path: at rest, in transit, in memory, and as published artifacts", 0, True),
    ("DS-01  Classification and labelling, automated at ingestion; member data is the crown jewels", 1),
    ("DS-02  Inference data protected end to end: prompts and responses encrypted, TLS 1.3 minimum", 1),
    ("DS-03  Memory sanitisation: nothing sensitive persists beyond the session", 1),
    ("DS-04  Data minimisation: field-level filtering in the retrieval layer, no bulk access", 1),
    ("DS-07  Artifact publication control: agent-written packages and configs go through the same vetting as third-party artifacts, with approval the agent cannot invoke", 1),
], notes="Ninety seconds. APP 11 obligations land here: member PII in prompts, logs, and training sets is personal information under the Act. DS-04 is the control that keeps the retrieval layer honest.", page=page); page += 1

pillar_slide("Pillar 4: Tool and Pipeline Security", 4, "Tool & Pipeline Security", "TP-01 .. TP-10  |  10 controls",
    "Registered tools, gated APIs",
    [
    ("A chatbot that talks is harmless; an agent that acts is only as safe as its tools", 0, True),
    ("TP-01  Tool registry: every agent-accessible tool registered, versioned, and security-approved before use", 1),
    ("TP-03  API gateway security: schema validation, rate limiting, and audit logging on every agent-facing endpoint", 1),
    ("TP-06  Dependency scanning, with sandbox libraries treated as a high-risk class; interpreter flags are not sandboxes", 1),
    ("TP-08  The gateway blocks cloud infrastructure control-plane APIs by default (EC2, IAM, KMS, Lambda)", 1),
    ("TP-10  Inbound control-plane protection: network bindings default to deny, gateway tokens stay out of web context (OpenClaw CVE-2026-25253)", 1),
], notes="Ninety seconds. Under CPG 230, the tool chain includes vendors: a model provider or an MCP server is a material outsourced service provider once member data flows through it. TP-01 is where that register starts.", page=page); page += 1

pillar_slide("Pillar 5: Monitoring and Incident Response", 5, "Monitoring, Logging & IR", "MIR-01 .. MIR-06  |  6 controls",
    "Every action logged, replayable later",
    [
    ("Visibility is the precondition for every other control in this framework", 0, True),
    ("MIR-01  Agent activity logging: every action, every tool call, every delegation", 1),
    ("MIR-02  Behavioural anomaly detection against a per-agent baseline", 1),
    ("MIR-04  AI-specific IR playbooks: prompt-injection containment, model rollback, tool revocation, session invalidation", 1),
    ("MIR-05  Reporting integration: automated triggers for the APRA 72-hour and SOCI 12-hour windows", 1),
    ("MIR-06  Forensic readiness: append-only immutable logs, full session reconstruction including tool-call chains", 1),
], notes="One minute. MIR-05 is the control that turns an incident into an APRA notification on time. The append-only log requirement in MIR-06 is the forensic answer to agents that can rewrite their own history.", page=page); page += 1

pillar_slide("Pillar 6: Governance and Risk", 6, "Governance & Risk Management", "GRM-01 .. GRM-06  |  6 controls",
    "Board accountability, in place",
    [
    ("Technical controls erode without governance; this pillar is what keeps them honest", 0, True),
    ("GRM-01  AI governance body: a chartered committee with CISO, CRO, General Counsel, data owner, and AI lead", 1),
    ("GRM-02  AI risk register, with automated tripwires and one exercised kill switch, tested at least annually", 1),
    ("GRM-04  Third-party AI risk: model, tool, and evaluation-harness vendors assessed, with right-to-audit clauses", 1),
    ("GRM-05  Regulatory mapping: automated mapping to CPS 234, CPG 230, ISM, E8, SOCI, PSPF, Privacy Act; quarterly posture reports", 1),
    ("GRM-06  Board and executive dashboard: maturity scores per pillar, open findings, risk acceptance decisions", 1),
], notes="One minute. CPS 234 puts information security accountability at the board; GRM-01 and GRM-06 give the trustee board the same line of sight over AI. The kill switch line gets attention: one rehearsed red button, tested annually.", page=page); page += 1

pillar_slide("Pillar 7: Execution Environment", 7, "Execution Environment", "EE-01 .. EE-08  |  8 controls",
    "Isolation enforced, never asserted",
    [
    ("This pillar sits at the base: an escapable sandbox undermines every control above it", 0, True),
    ("EE-01  Boundary enforcement: no shared host mounts or namespaces, immutable infrastructure, fail-closed on breach", 1),
    ("EE-05  Config-file injection prevention: agents cannot write files the host will later trust (.zshrc, .claude/settings.json, crontab)", 1),
    ("EE-06  Fail-closed operation: runtime attestation that the strongest isolation mode is active, with no silent fallback", 1),
    ("EE-07  Control-plane integrity: the agent cannot rewrite its own security settings", 1),
    ("EE-08  Evaluation-harness isolation: egress blocked at the hypervisor boundary and verified by active test; no verified egress block means no evaluation", 1),
], notes="Two minutes. This pillar exists because of the March to July 2026 escape wave. EE-08 is deliberately fail-closed: isolation is verified, not asserted. For a fund, evaluation environments are where member data and model testing meet.", page=page); page += 1

# 16 — Reference implementation
diagram_slide("From Framework to Deployment", "impl-reference-architecture.png",
              kicker="Eight deployable components; every control range mapped", page=page,
              notes="Ninety seconds. The framework ships with a concrete component model: policy engine, tool gateway or sidecar, identity plane, observability, evaluation enclave. Each component carries its control ranges, so the diagram and the control set stay in step."); page += 1

# 17 — Policy as code
diagram_slide("Policy as Code: 55 Controls You Can Run", "impl-policy-decision-points.png",
              kicker="Deny-override evaluation at every decision point", page=page,
              notes="Ninety seconds. Each of the 55 controls is expressed as executable policy in Rego. Evaluation is deny-override: a deny verdict wins over any allow rule. That is how the framework becomes enforcement rather than a document, and how an audit becomes a test run."); page += 1

# 18 — Request flow
diagram_slide("Every Request Through the Gate", "impl-request-flow.png",
              kicker="Parse, evaluate, decide, log, then the agent acts", page=page,
              notes="Ninety seconds. Walk the flow: request, parse, policy evaluation across the 55 controls, allow or deny, audit. The sidecar topology means this applies to existing platforms without rewriting them."); page += 1

# 19 — Maturity
diagram_slide("Maturity: L1 to L4", "maturity-journey.png",
              kicker="Consistent with the ISM and Essential Eight maturity model", page=page,
              notes="Ninety seconds. L1 is ad hoc, L2 managed, L3 defined, L4 optimised. The practical path for a fund starting out: make L2 the floor for the first production system, and target L3 for anything member-facing.",
              caption="L3 Defined: regulated entities and government agencies. L4 Optimised: critical infrastructure and national security."); page += 1

# 20 — APRA alignment
diagram_slide("Alignment with APRA and Australian Regulation", "aware-super-alignment.png",
              kicker="Seven pillars against CPS 234, CPG 230, the Privacy Act, ASIC, and the AU Guardrails", page=page,
              notes="Two minutes. Every pillar maps onto an obligation the trustee already answers to. Solid dots are direct control mappings, gold dots supporting contributions. MIR-05 sits directly under the 72-hour notification line; GRM sits under board accountability.",
              caption="Solid: direct control mapping. Gold: supporting contribution."); page += 1

# 21 — Practical starting point
bullets_slide("A Practical Starting Point", [
    ("The framework answers 'where do we start' in five steps", 0, True),
    ("1.  Posture assessment: score all seven pillars at L1-L4, find where member data already meets a model", 1),
    ("2.  Set the floor: make L2 the baseline for the first production system (identity, logging, sandbox, tool registry)", 1),
    ("3.  Pilot policy as code on one use case: pick a chatbot or a copilot, run it through the gateway, watch the logs", 1),
    ("4.  Board reporting cadence: GRM-06 dashboard from the first quarter, so the trustee sees posture, not anecdotes", 1),
    ("5.  Keep it current: monthly deep review and the live watchlist, so the control set tracks what attackers are actually doing", 1),
    ("None of this requires a platform rewrite; the reference implementation drops in beside what the fund already runs", 0, True, NAVY2),
], page=page, notes="Two minutes. This is the slide the audience came for. Keep it concrete: one use case, L2 floor, a dashboard, a monthly rhythm. The assessment is the honest first step because the fund does not yet know where member data meets a model today."); page += 1

# 22 — Watchlist
watchlist_slide(page); page += 1

# 23 — Why SHIELD-AI for Aware Super
bullets_slide("Why SHIELD-AI for Aware Super", [
    ("Aligned: mapped to CPS 234, CPG 230, the Privacy Act, ASIC, and the AU Guardrails the fund already operates under", 0, True),
    ("Evidence driven: 25 incidents, a monthly deep review, a live watchlist; the controls track what attackers are actually doing", 0, True),
    ("Deployable: a reference implementation with policy as code, ready to run beside existing platforms", 0, True),
    ("Member focused: controls that keep member data in the environment and out of prompts, logs, and packages", 0, True),
    ("Measurable: the L1-L4 maturity model gives the board a repeatable posture picture, quarter to quarter", 0, True),
    ("Transparent: an open framework with no commercial lock-in, ready for independent evaluation", 0, True, NAVY2),
], page=page, notes="One minute. Bring it back to the opening: the fund is putting AI into production, the framework gives the security and risk team the language and the controls to do it on APRA's terms."); page += 1

# 24 — Close / Q&A
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 4.35, SW, 0.06, fill=GOLD)
tf = box(s, 1.0, 1.9, 11.3, 1.4)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Questions and Discussion"
r.font.size = Pt(44); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
tf2 = box(s, 1.0, 4.6, 11.3, 1.8)
para(tf2, "Which member-facing AI capability ships first, and where does member data meet a model today?", size=17, color=RGBColor(0xC9,0xD4,0xE8), first=True, space_after=10)
para(tf2, "A useful next step: a seven-pillar posture assessment at L1-L4, then a policy-as-code pilot on that first use case.", size=15, color=GOLD, space_after=10)
para(tf2, "SHIELD-AI(TM) v1.5  |  7 pillars  |  55 controls  |  policy as code  |  August 2026", size=12, color=MUTED)
s.notes_slide.notes_text_frame.text = ("Two minutes. The question on the slide is the honest conversation starter. Offer the posture assessment and the "
    "policy-as-code pilot as concrete next steps; keep it in maturity terms, no commercial pitch.")

out = OUT
prs.save(out)
print("Saved", out, "| slides:", len(prs.slides._sldIdLst))

manifest = {
    "deck": os.path.basename(OUT).replace(".pptx", ""),
    "title": next((sh.text_frame.text for s in prs.slides for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()), "").splitlines()[0],
    "audience": AUDIENCE,
    "version": DECK_VERSION,
    "date": "2026-08-06",
    "framework_version": "v1.5",
    "slides": len(prs.slides._sldIdLst),
    "diagrams": DIAGRAMS,
    "builder": os.path.relpath(__file__, REPO),
    "commit": subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
}
with open(MANIFEST, "w") as f:
    json.dump(manifest, f, indent=2)
print("manifest:", MANIFEST)
