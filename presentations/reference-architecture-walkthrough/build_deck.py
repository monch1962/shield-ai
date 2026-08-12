#!/usr/bin/env python3
"""Build the SHIELD-AI Reference Architecture Walkthrough deck (.pptx).

A standalone technical-SME deck following the seven-act narrative from
framework/shield-ai-reference-architecture-walkthrough.md. Two diagrams on
slides (request flow + network boundaries), the rest as handouts. Every
decision point is anchored to a real 2026 incident. Speaker notes carry
timing and delivery guidance. Humanised copy: plain professional voice,
no AI tells, no trademark marks.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os, sys, subprocess, json, datetime

REPO = "/home/davidm/Projects/shield-ai"
OUT_DIR = "/home/davidm/Projects/shield-ai/presentations/reference-architecture-walkthrough"
os.makedirs(OUT_DIR, exist_ok=True)
IMG = "/tmp/deck-imgs"
os.makedirs(IMG, exist_ok=True)

DIAGRAMS = ["impl-request-flow", "impl-network-boundaries"]

def render_png(name):
    base = name[:-4] if name.endswith(".png") else name
    png = os.path.join(IMG, base + ".png")
    if os.path.exists(png):
        return png
    svg = os.path.join(REPO, "assets", "diagrams", base + ".svg")
    if not os.path.exists(svg):
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
AUDIENCE = "Technical SMEs (security architects, platform engineers, AI engineers)"
OUT = os.path.join(OUT_DIR, "reference-architecture-walkthrough.pptx")
MANIFEST = os.path.join(OUT_DIR, "deck-manifest.json")

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
    r = p.add_run(); r.text = "SHIELD-AI  |  Reference Architecture Walkthrough  |  Deck v%s  |  Framework v1.6  |  Aug 2026" % DECK_VERSION
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


def incident_box(s, text, top=5.9, left=0.7, width=12.0):
    rect(s, left, top, width, 1.15, fill=LIGHT, line=RED, line_w=1.5)
    tf = box(s, left + 0.25, top + 0.12, width - 0.5, 0.95)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text
    r.font.size = Pt(11.5); r.font.italic = True; r.font.color.rgb = NAVY2; r.font.name = FONT
    return tf


def diagram_slide(title, img, kicker=None, page=None, notes=None, caption=None):
    s = slide()
    header(s, title, kicker, page)
    png = render_png(img)
    from PIL import Image
    im = Image.open(png)
    w, h = im.size
    max_w, max_h = 11.93, 5.3
    scale = min(max_w / w, max_h / h)
    dw, dh = w * scale, h * scale
    left = (SW - dw) / 2
    top = 1.5 + (5.4 - dh) / 2
    s.shapes.add_picture(png, Inches(left), Inches(top), Inches(dw), Inches(dh))
    if caption:
        tf = box(s, 0.7, 6.85, 12.0, 0.4)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = caption
        r.font.size = Pt(11); r.font.italic = True; r.font.color.rgb = MUTED; r.font.name = FONT
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


# ============================================================
# SLIDE 1: TITLE
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 4.35, SW, 0.06, fill=GOLD)
tf = box(s, 1.0, 2.0, 11.3, 1.6)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "SHIELD-AI Reference Architecture"
r.font.size = Pt(44); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
p2 = tf.add_paragraph()
r2 = p2.add_run(); r2.text = "A walkthrough for technical audiences: one request, four gates, five zones, one audit trail"
r2.font.size = Pt(20); r2.font.color.rgb = GOLD; r2.font.name = FONT
tf2 = box(s, 1.0, 4.7, 11.3, 1.6)
para(tf2, "Every agent action passes four gates. Every verdict is audited. If any gate or audit path fails, the action is blocked.", size=18, color=RGBColor(0xC9, 0xD4, 0xE8), first=True, space_after=10)
para(tf2, "The next thirty minutes are that sentence, unpacked. One request, followed end to end, anchored to real incidents.", size=15, color=MUTED)
s.notes_slide.notes_text_frame.text = ("Ninety seconds. Deliver the one-sentence version without slides: every agent action passes four gates, every verdict is audited, and if any gate or audit path fails the action is blocked. Then the promise: one request, end to end, every component appearing at the moment it matters."); page = 1

# ============================================================
# SLIDE 2: ACT 1 — THE PROTAGONIST
# ============================================================
s = bullets_slide("The Protagonist: One Request", [
    ("A user in a business application asks agent-7 to summarise a thread and draft a reply", 0, True),
    ("The request enters through the AI gateway (Zone 1): authentication, web-application filtering, intent filtering, rate limiting", 1),
    ("The orchestrator (LangGraph, CrewAI, Semantic Kernel, or equivalent) dispatches the task to agent-7's sandbox (Zone 2)", 1),
    ("Everything the user touches is Zone 1. Everything the agent does happens inside a sandbox in Zone 2", 0, True),
    ("One agent, one request, one journey. Every component you meet from here on exists to gate or observe this journey", 0, True, NAVY2),
], kicker="Act 1 — Setting the scene", page=2,
   notes="Three minutes. Introduce agent-7 and its user; keep it concrete. Set the boundary: the gateway is the front door and it filters before the agent ever sees the request. Do NOT enumerate the eight component groups here. The audience meets each one at the moment it matters.")
incident_box(s, "Why this framing: the prior presentation failed because the components were presented as a catalogue. The request journey gives every component a reason to appear in order.")
page = 3

# ============================================================
# SLIDE 3: ACT 2 — P1 TOOL AUTHORISATION
# ============================================================
s = bullets_slide("Gate P1: Tool Authorisation", [
    ("Question: is this agent authorised to call this tool, within its registered scope?", 0, True),
    ("What it checks: agent identity (IAM-01), scope-bound delegation (IAM-02), per-tool scoped credentials (IAM-08), tool access control (TP-02)", 1),
    ("agent-7 may call summarise_thread: it is registered, versioned, and scoped to that agent", 1),
    ("agent-7 may not call drop_database: the tool is not in the registry, and P1 denies", 1),
    ("The OPA policy engine evaluates every proposed action against these assertions (Zone 3)", 1),
], kicker="Act 2 — The four gates (1 of 4)", page=3,
   notes="Two and a half minutes. Anchor to the incident, then land the gloss: registered, versioned, scoped. The registration and scoping P1 enforces is exactly the control the OpenClaw attack bypassed.")
incident_box(s, "Incident anchor: OpenClaw CVE-2026-25253 (CVSS 8.8). A crafted link hijacked a loopback agent gateway, switched off approvals, and escaped to the host.")
page = 4

# ============================================================
# SLIDE 4: ACT 2 — P2 DATA ACCESS
# ============================================================
s = bullets_slide("Gate P2: Data Access", [
    ("Question: what data may the agent retrieve, at what classification, under what conditions?", 0, True),
    ("What it checks: data classification (DS-01), attribute-based access control at retrieval (DS-04), data minimisation (DS-04)", 1),
    ("agent-7 may retrieve the thread: the documents are classified and the agent's attributes permit access", 1),
    ("A document outside the agent's classification boundary is denied at retrieval, before it ever enters context", 1),
    ("Field-level redaction happens before context injection, in the data plane (Zone 4)", 1),
], kicker="Act 2 — The four gates (2 of 4)", page=4,
   notes="Two minutes. The classification and ABAC gates are the answer to the Kiro attack: the agent reached for data and configuration it should never have been able to touch.")
incident_box(s, "Incident anchor: AWS Kiro CVE-2026-10591. Hidden 1px white text on an API docs page rewrote the agent's MCP server registry and ran attacker code on the host.")
page = 5

# ============================================================
# SLIDE 5: ACT 2 — P3 HUMAN APPROVAL
# ============================================================
s = bullets_slide("Gate P3: Human Approval", [
    ("Question: does this action require a human approval gate?", 0, True),
    ("What it checks: human oversight (IAM-03), enforced at the infrastructure layer, not as a polite request", 1),
    ("High-risk actions require approval: code execution, financial writes, security-relevant changes", 1),
    ("The approval gate is infrastructure-enforced: no gate, no action", 1),
], kicker="Act 2 — The four gates (3 of 4)", page=5,
   notes="Two minutes. The ABC story is the missing-gate story: no gate existed between the agent and the action. P3 is that gate.")
incident_box(s, "Incident anchor: the ABC News Australian case (INC-32). A personal assistant booked gym classes months ahead and cancelled another member's waitlist position because no gate existed between the agent and the action.")
page = 6

# ============================================================
# SLIDE 6: ACT 2 — P4 OUTPUT VALIDATION
# ============================================================
s = bullets_slide("Gate P4: Output Validation", [
    ("Question: is the tool response schema-valid and sanitised before it enters agent context?", 0, True),
    ("What it checks: tool output validation (TP-04), output scanning for PII and prompt leakage (DS-06), behaviour validation at the proxy (MS-05)", 1),
    ("The reply draft comes back from the tool; the gateway validates it against a known-good schema and sanitises it", 1),
    ("A malicious or malformed response cannot steer the agent, because it never reaches agent context intact", 1),
], kicker="Act 2 — The four gates (4 of 4)", page=6,
   notes="Two minutes. The rhythm to land: four gates, four incidents, one message. The architecture is the answer sheet to the incident ledger. Let the audience feel the pattern.")
incident_box(s, "Incident anchor: implicit tool exposure (CVE-2026-26030, CVE-2026-25592). A single prompt achieved code execution because an internal helper was auto-registered as a callable tool.")
page = 7

# ============================================================
# SLIDE 7: REQUEST FLOW DIAGRAM
# ============================================================
s = diagram_slide("The Journey, End to End", "impl-request-flow.png",
                  kicker="Act 2 — One request through the whole chain", page=7,
                  caption="Seven steps from user request to response; every hop emits a structured audit event.",
                  notes="Five minutes. Walk the diagram as the story: user request, gateway, agent planning, policy evaluation (P1-P3), tool execution, output validation (P4), response. Pause on the fail-closed note: if any dependency in the chain is unreachable, the action is blocked. This is the interaction story, made visible.")
page = 8

# ============================================================
# SLIDE 8: ACT 3 — SANDBOX AND SIDECAR
# ============================================================
s = bullets_slide("Where Enforcement Lives: Sandbox and Sidecar", [
    ("Zone 2: every agent runs in its own sandbox with a sidecar carrying the policy engine, tool gateway, and telemetry exporter", 0, True),
    ("The sandbox: read-only root filesystem, seccomp/AppArmor profiles, NetworkPolicy egress allow-list, resource quotas", 1),
    ("Runtime attestation: sandbox mode is attested before each code-execution step (EE-06). No attestation, no execution", 1),
    ("The sidecar fails closed: no policy, no audit, no action", 1),
    ("Enforcement is local, per agent, and it does not degrade", 0, True, NAVY2),
], kicker="Act 3 — The execution zone", page=8,
   notes="Five minutes. The CrewAI chain is the reason attestation and fail-closed exist: the framework fell back to a weaker sandbox when the configured one was unavailable, and prompt injection became host RCE.")
incident_box(s, "Incident anchor: CrewAI fail-open chain (CVE-2026-2275/2286/2287). Prompt injection turned into host RCE because the framework fell back to a weaker sandbox when the configured one was unavailable.")
page = 9

# ============================================================
# SLIDE 9: ACT 4 — DATA AND MEMORY PLANE
# ============================================================
s = bullets_slide("The Data and Memory Plane", [
    ("Zone 4: the RAG security layer and agent memory stores", 0, True),
    ("Documents classified at ingestion (DS-01); retrieval enforces ABAC with field-level redaction before context injection (DS-04)", 1),
    ("Agent memory: per-agent scoped, encrypted, sanitised between sessions (DS-03); memory-store integrity (MS-10)", 1),
    ("Outputs scanned for PII, training data, and system-prompt leakage (DS-06)", 1),
    ("Data is not a passive resource in an agent system. It is an attack surface", 0, True, NAVY2),
], kicker="Act 4 — Zone 4", page=9,
   notes="Four minutes. The RufRoot case is the memory-poisoning story: the attacker's patterns were written into the learning store and steered every future user's outputs. Patching does not undo poisoning.")
incident_box(s, "Incident anchor: Ruflo/RufRoot CVE-2026-59726 (CVSS 10.0). MCP-bridge RCE with persistent memory poisoning; remediation required credential rotation, not just a patch.")
page = 10

# ============================================================
# SLIDE 10: ACT 5 — THE AUDIT TRAIL
# ============================================================
s = bullets_slide("The Audit Trail: Every Verdict Is Evidence", [
    ("Zone 5: telemetry and incident response. Every event from the journey was emitted over OTLP", 0, True),
    ("Immutable, append-only log store (MIR-06); anomaly detection with per-agent baselines (MIR-02)", 1),
    ("Every audit event carries: agent ID, session ID, correlation ID, timestamp, action, target, verdict, originating user", 1),
    ("The correlation ID ties every event to the originating user session. The full chain is reconstructable", 0, True),
    ("Reporting triggers pre-populate SOCI 12-hour, APRA 72-hour, and NDB notifications (MIR-05)", 1),
    ("Incident response is not a hunt. It is a query", 0, True, NAVY2),
], kicker="Act 5 — Zone 5", page=10,
   notes="Four minutes. The same events that gate production are the evidence an auditor asks for. Audit becomes a test run is literal: the compliance console continuously tests the controls against the live deployment (GRM-05).")
page = 11

# ============================================================
# SLIDE 11: ACT 6 — THE FAIL-CLOSED BEAT
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 4.35, SW, 0.06, fill=GOLD)
tf = box(s, 1.0, 1.6, 11.3, 1.2)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "The Question"
r.font.size = Pt(40); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
tf2 = box(s, 1.0, 3.0, 11.3, 1.0)
para(tf2, "The OPA container just went down. Agent-7 proposes its next action. What happens?", size=24, color=GOLD, first=True)
tf3 = box(s, 1.0, 4.8, 11.3, 2.0)
para(tf3, "The action is blocked. Not degraded, not deferred: blocked. If any dependency in the chain is unreachable, the action is denied (EE-06, TP-03). The failed evaluation is itself an audit event.", size=18, color=RGBColor(0xC9, 0xD4, 0xE8), first=True, space_after=10)
para(tf3, "The framework never degrades to a weaker enforcement mode.", size=16, color=WHITE, bold=True)
s.notes_slide.notes_text_frame.text = ("Three minutes. The most memorable minute of the talk. Ask the question, pause, let the room answer, then deliver the answer slowly: blocked. Not degraded, not deferred. This converts the architecture from description into engineering decisions. Deliver it without slides, standing still.")
page = 12

# ============================================================
# SLIDE 12: NETWORK BOUNDARY DIAGRAM
# ============================================================
s = diagram_slide("The Network Boundary", "impl-network-boundaries.png",
                  kicker="Act 7 — The architecture for you", page=12,
                  caption="Agents have no direct path to infrastructure control planes; egress is allow-listed to registered tools and model providers.",
                  notes="Three minutes. The second of two on-slide diagrams. The memorable detail: EC2, IAM, KMS, CloudFormation, S3 control-plane, Azure Resource Manager, GCP Cloud Resource Manager are excluded from every allow-list. Any attempt by an agent to reach a control plane is logged, blocked, and treated as a potential indicator of compromise.")
page = 13

# ============================================================
# SLIDE 13: ACT 7 — TOPOLOGY DECISION TREE
# ============================================================
s = bullets_slide("The Architecture for You: Choose Your Topology", [
    ("Under ~10 agents: embedded library", 0, True),
    ("Controls run inside the agent framework; simplest path for pilots and single-agent PoCs", 1),
    ("10-100 agents: sidecar proxy", 0, True),
    ("Per-agent sidecar (OPA + tool gateway + telemetry) in a container-orchestrated deployment", 1),
    ("100+ or multi-agent: central gateway + sidecars", 0, True),
    ("Central policy/gateway for external tools; sidecars retained for per-agent policy and audit", 1),
], kicker="Act 7 — Close", page=13,
   notes="Three minutes. Turn the architecture into a decision each person can make. Hand out the full diagram set: reference architecture, policy decision points, sidecar topology, telemetry pipeline, network boundaries, maturity components. Then the closing question: what would you build first?")
page = 14

# ============================================================
# SLIDE 14: CLOSE
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 4.35, SW, 0.06, fill=GOLD)
tf = box(s, 1.0, 1.8, 11.3, 1.4)
p = tf.paragraphs[0]
r = p.add_run(); r.text = "One Request, Four Gates, One Audit Trail"
r.font.size = Pt(38); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
tf2 = box(s, 1.0, 3.6, 11.3, 2.6)
para(tf2, "Every agent action passes four gates. Every verdict is audited. If any gate or audit path fails, the action is blocked.", size=18, color=GOLD, first=True, space_after=12)
para(tf2, "The incidents are the reason the gates exist. The audit trail is the evidence. The topology is the choice.", size=15, color=RGBColor(0xC9, 0xD4, 0xE8), space_after=12)
para(tf2, "SHIELD-AI v1.6  |  57 controls  |  7 pillars  |  Reference architecture: framework/shield-ai-implementation-architecture.md", size=13, color=MUTED)
s.notes_slide.notes_text_frame.text = ("One minute. Close on the sentence you opened with. Remind the room: incidents are the reason the gates exist, the audit trail is the evidence, the topology is the choice. Point to the full architecture document and the walkthrough guide for anything they want to go deeper on.")
page = 15

# ---- manifest ----
manifest = {
    "deck": "reference-architecture-walkthrough",
    "title": "SHIELD-AI Reference Architecture Walkthrough",
    "audience": AUDIENCE,
    "version": DECK_VERSION,
    "date": "2026-08-12",
    "framework_version": "v1.6",
    "slides": len(prs.slides._sldIdLst),
    "diagrams": DIAGRAMS,
    "builder": "presentations/reference-architecture-walkthrough/build_deck.py",
    "commit": subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "built_at": datetime.datetime.utcnow().isoformat() + "Z",
}

prs.save(OUT)
with open(MANIFEST, "w") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")

print("built", OUT, "| slides:", manifest["slides"])
