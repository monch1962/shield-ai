#!/usr/bin/env python3
"""
SHIELD-AI Implementation Architecture Diagram Generator
======================================================
Generates the SVG diagram set for framework/shield-ai-implementation-architecture.md:
the deployable component model for implementing SHIELD-AI controls.

Produces:
  assets/diagrams/impl-reference-architecture.svg   -- deployable component view (centre)
  assets/diagrams/impl-policy-decision-points.svg   -- OPA/Rego decision points
  assets/diagrams/impl-request-flow.svg             -- end-to-end request flow
  assets/diagrams/impl-telemetry-pipeline.svg       -- telemetry -> SIEM -> reporting
  assets/diagrams/impl-network-boundaries.svg       -- trust zones + egress allowlist
  assets/diagrams/impl-sidecar-topology.svg         -- Kubernetes sidecar deployment
  assets/diagrams/impl-maturity-components.svg      -- L1-L4 component coverage

Style follows the existing framework diagrams (navy/blue/gold on white).
"""

import os

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "assets", "diagrams")

NAVY  = "#0a1e3d"
BLUE  = "#1a3a6b"
GOLD  = "#d4a017"
LTBL  = "#dce6f0"
WHITE = "#ffffff"
TEXT  = "#1a1a2e"
MUTED = "#5a6a8a"
GRAY  = "#e8ecf0"
GREEN = "#22c55e"
RED   = "#c0392b"
AMBER = "#f59e0b"
PURPLE= "#8e6bb8"


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
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/>
    </marker>
  </defs>
  {body}
</svg>'''


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, w, h, colour, label, sub="", cap="", fs=12, bold=True, white_text=False, stroke=BLUE):
    label, sub, cap = esc(label), esc(sub), esc(cap)
    cls = "white" if white_text else "label"
    text_colour = f' fill="{WHITE}"' if white_text else ""
    if cap:
        label_y = y + h/2 + 4
        sub_y = y + h/2 + 22
    else:
        label_y = y + h/2 - (6 if sub else 0)
        sub_y = y + h/2 + 12
    parts = f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{colour}" stroke="{stroke}" stroke-width="1.5"/>
    <text x="{x + w/2}" y="{label_y}" text-anchor="middle" class="{cls}" font-size="{fs}" font-weight="{'bold' if bold else 'normal'}"{text_colour}>{label}</text>'''
    if sub:
        parts += f'''\n    <text x="{x + w/2}" y="{sub_y}" text-anchor="middle" class="sm">{sub}</text>'''
    if cap:
        parts += f'''\n    <text x="{x + w/2}" y="{y + 17}" text-anchor="middle" class="cap">{cap}</text>'''
    return parts


def zone(x, y, w, h, title, fill="#f4f7fb", dash=False):
    d = ' stroke-dasharray="6 4"' if dash else ""
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{BLUE}" stroke-width="1.2"{d}/>
    <text x="{x + 10}" y="{y + 16}" class="cap">{esc(title)}</text>'''


def arrow(x1, y1, x2, y2, colour=BLUE, w=1.5, dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    return f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{w}" marker-end="url(#a)"{d}/>'''


def varrow(x, y1, y2, colour=BLUE, dash=False):
    return arrow(x, y1, x, y2, colour, 1.5, dash)


def label(x, y, text, cls="sm", colour=None, bold=False, size=None, anchor="middle"):
    text = esc(text)
    extra = ""
    if colour: extra += f' fill="{colour}"'
    if bold: extra += ' font-weight="bold"'
    if size: extra += f' font-size="{size}"'
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}"{extra}>{text}</text>'


# ------------------------------------------------------------------
# Diagram 1: Reference architecture -- deployable component view
# ------------------------------------------------------------------
def d1_reference():
    w, h = 1150, 720
    b = []
    # ---- Zones ----
    b.append(zone(20, 20, 1110, 130, "1. CLIENT & CONTROL PLANE", "#f0f4f8"))
    b.append(zone(20, 160, 540, 290, "2. AGENT EXECUTION ZONE (PER-AGENT SANDBOX)", "#f7fafd"))
    b.append(zone(580, 160, 550, 290, "3. POLICY, TOOL & MODEL PLANE", "#f7fafd"))
    b.append(zone(20, 460, 1110, 130, "4. DATA PLANE", "#f0f4f8"))
    b.append(zone(20, 600, 1110, 105, "5. OBSERVABILITY & GOVERNANCE", "#f0f4f8"))

    # ---- Row 1: client / control plane (left-to-right flow) ----
    b.append(box(60, 55, 170, 60, WHITE, "Users & Business Apps", "web / API / IDE"))
    b.append(box(270, 55, 190, 60, WHITE, "Agent Orchestrator", "LangGraph, CrewAI, Semantic Kernel"))
    b.append(box(500, 55, 170, 60, LTBL, "AI Gateway", "authN, WAF, intent filter", cap="INGRESS"))
    b.append(box(710, 55, 190, 60, WHITE, "Model Gateway & Guardrails", "output guardrails, redaction", cap="MS-01..11"))
    b.append(box(940, 55, 160, 60, WHITE, "LLM Provider(s)", "cloud / self-hosted"))
    b.append(arrow(230, 85, 270, 85))
    b.append(arrow(460, 85, 500, 85))
    b.append(arrow(670, 85, 710, 85))
    b.append(arrow(900, 85, 940, 85))
    b.append(arrow(365, 130, 420, 185, dash=True))
    b.append(label(385, 140, "dispatch to sandboxed agent runtime", "sm", anchor="start"))

    # ---- Row 2: agent execution zone ----
    b.append(box(60, 195, 220, 100, WHITE, "Agent Runtime (sandboxed)", "read-only rootfs, seccomp, quotas", cap="EE-01..08"))
    b.append(box(320, 195, 220, 100, WHITE, "Agent Sidecar", "OPA + tool gateway + telemetry", cap="POLICY POINT"))
    b.append(label(30, 315, "NetworkPolicy egress allow-list + fail-closed attestation (EE-06)", "sm", anchor="start"))
    b.append(arrow(280, 245, 320, 245))

    # ---- Row 3: policy, tool & model plane ----
    b.append(box(620, 195, 230, 100, LTBL, "Policy Decision Points (OPA)", "Rego: IAM, DS, TP, GRM", cap="POLICY-AS-CODE"))
    b.append(box(880, 195, 220, 100, WHITE, "Tool Registry + MCP Gateway", "signed tool defs, schema validation", cap="TP-01..13"))
    b.append(arrow(540, 245, 620, 245))
    b.append(arrow(850, 245, 880, 245))
    b.append(box(620, 330, 230, 90, WHITE, "Identity Plane", "SPIFFE/SPIRE, JIT creds, delegation", cap="IAM-01..09"))
    b.append(box(880, 330, 220, 90, WHITE, "External Tools / APIs", "databases, SaaS, code exec (sandboxed)"))
    b.append(varrow(620, 295, 330))
    b.append(varrow(880, 295, 330))

    # ---- Row 4: data plane ----
    b.append(box(60, 495, 250, 70, WHITE, "Data & RAG Security Layer", "classification, ABAC, redaction", cap="DS-01..07"))
    b.append(box(350, 495, 240, 70, WHITE, "Memory Store", "per-agent scoped, retention, sanitisation", cap="DS-03/04"))
    b.append(box(630, 495, 240, 70, WHITE, "Training Data Governance", "lineage, consent, poison detection", cap="DS-05"))
    b.append(box(910, 495, 190, 70, WHITE, "Data Sources", "warehouse, lake, APIs"))
    b.append(arrow(310, 530, 350, 530))
    b.append(arrow(590, 530, 630, 530))
    b.append(arrow(870, 530, 910, 530))

    # ---- Row 5: observability & governance ----
    b.append(box(60, 635, 230, 50, WHITE, "Agent Telemetry (OTLP)", "tool calls, decisions, verdicts", cap="MIR-01"))
    b.append(box(330, 635, 220, 50, WHITE, "SIEM + Anomaly Detection", "baselines, swarm detection", cap="MIR-02"))
    b.append(box(590, 635, 230, 50, WHITE, "Incident Response + Reporting", "SOCI 12h / APRA 72h / NDB", cap="MIR-04/05"))
    b.append(box(860, 635, 240, 50, WHITE, "Compliance & Governance Console", "control testing, board dashboard", cap="GRM-01..06"))
    b.append(arrow(290, 660, 330, 660))
    b.append(arrow(550, 660, 590, 660))
    b.append(arrow(820, 660, 860, 660))
    b.append(label(430, 330, "every action emits audit events (MIR-01) -> telemetry, zone 5", "sm", anchor="end"))
    b.append(label(575, 716, "Every component maps to SHIELD-AI controls -- see the component-to-control matrix in this document.", "sm"))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 2: Policy decision points
# ------------------------------------------------------------------
def d2_policy():
    w, h = 950, 450
    b = []
    b.append(box(40, 170, 170, 80, WHITE, "Agent Action", "tool call, data access, model"))
    b.append(box(255, 40, 160, 80, LTBL, "P1 Tool Authorisation", "IAM-01/02/08, TP-02", cap="ALLOW/DENY"))
    b.append(box(425, 40, 160, 80, LTBL, "P2 Data Access", "DS-01/04, ABAC at retrieval", cap="SCOPE"))
    b.append(box(595, 40, 160, 80, LTBL, "P3 Human Approval", "IAM-03, high-risk actions", cap="GATE"))
    b.append(box(765, 40, 160, 80, LTBL, "P4 Output Validation", "TP-04, DS-06, MS-05", cap="SANITISE"))
    b.append(box(765, 170, 160, 80, WHITE, "Tool / Data / Model", "execution proceeds"))
    for x1, x2 in [(415, 425), (585, 595), (755, 765)]:
        b.append(arrow(x1, 80, x2, 80))
    b.append(arrow(845, 120, 845, 170))
    b.append(arrow(210, 210, 255, 120))
    b.append(label(232, 168, "enforce", "sm"))
    b.append(arrow(335, 120, 335, 335, colour=RED))
    b.append(label(150, 320, "DENY -> log via MIR-01, alert MIR-02", "sm", RED))
    b.append(box(145, 335, 380, 55, WHITE, "Policy Engine (OPA)", "Rego assertions from policies/ -- audit every decision"))
    b.append(label(335, 415, "policy verdict + evidence -> telemetry (MIR-01)", "sm"))
    b.append(label(475, 440, "Every decision point is a Rego evaluation; every verdict is an audit event.", "sm"))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 3: Request flow
# ------------------------------------------------------------------
def d3_flow():
    w, h = 1080, 520
    b = []
    actors = [
        ("User", 40, 300),
        ("AI Gateway", 220, 300),
        ("Agent (sandbox)", 400, 300),
        ("OPA Policy", 580, 300),
        ("Tool Gateway", 760, 300),
        ("Tool / Model", 940, 300),
    ]
    for name, x, y in actors:
        b.append(box(x, y, 120, 50, WHITE, name))
    steps = [
        "1. User request (authenticated, session-scoped)",
        "2. Gateway: authN, WAF, intent filter, rate limit",
        "3. Agent plans; tool invocation proposed",
        "4. OPA: is agent authorised? scope? approval needed?",
        "5. Tool gateway: schema validation, allow-list, audit",
        "6. Output validated & sanitised before agent context",
        "7. Response returned; full chain logged (MIR-01)",
    ]
    y = 40
    for s in steps:
        b.append(label(540, y, s, "label", bold=False))
        y += 24
    xs = [100, 280, 460, 640, 820, 1000]
    for i in range(len(xs)-1):
        b.append(arrow(xs[i]+60, 340, xs[i+1]-60, 340))
    b.append(arrow(100, 390, 1000, 390, colour=GOLD, dash=True))
    b.append(label(550, 410, "every hop emits a structured audit event (agent ID, session ID, correlation ID, verdict) -> telemetry", "sm"))
    b.append(label(550, 490, "Fail-closed: any unreachable policy/tool/audit dependency blocks the action (EE-06, TP-03).", "sm", MUTED))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 4: Telemetry pipeline
# ------------------------------------------------------------------
def d4_telemetry():
    w, h = 1080, 480
    b = []
    b.append(zone(20, 30, 300, 400, "AGENT FLEET", "#f7fafd"))
    b.append(zone(340, 30, 320, 400, "INGESTION & ANALYTICS", "#f7fafd"))
    b.append(zone(680, 30, 380, 400, "RESPONSE & REPORTING", "#f7fafd"))
    b.append(box(50, 70, 240, 55, WHITE, "Agent A (sidecar)", "OTLP exporter"))
    b.append(box(50, 140, 240, 55, WHITE, "Agent B (sidecar)", "OTLP exporter"))
    b.append(box(50, 210, 240, 55, WHITE, "Agent C (sidecar)", "OTLP exporter"))
    b.append(label(170, 290, "tool calls, data access,", "sm"))
    b.append(label(170, 305, "policy verdicts, model calls", "sm"))
    b.append(box(370, 70, 260, 55, LTBL, "OTLP Collector", "batch, sample, enrich"))
    b.append(box(370, 140, 260, 55, WHITE, "SIEM / Log Store", "immutable, append-only", cap="MIR-06"))
    b.append(box(370, 210, 260, 55, WHITE, "Anomaly Detection", "per-agent + per-class baselines, swarm", cap="MIR-02"))
    b.append(box(710, 70, 320, 55, WHITE, "SOC Dashboards", "live posture, agent activity"))
    b.append(box(710, 140, 320, 55, WHITE, "IR Playbooks", "containment, tool revocation", cap="MIR-04"))
    b.append(box(710, 210, 320, 55, LTBL, "Mandatory Reporting Triggers", "SOCI 12h | APRA 72h | NDB", cap="MIR-05"))
    b.append(box(710, 280, 320, 55, WHITE, "Compliance Dashboard", "61 controls, per-pillar maturity", cap="GRM-06"))
    for y in (97, 167, 237):
        b.append(arrow(290, y, 370, y))
    b.append(varrow(500, 125, 140))
    b.append(varrow(500, 195, 210, dash=True))
    b.append(arrow(630, 97, 710, 97))
    b.append(arrow(630, 167, 710, 167))
    b.append(arrow(630, 237, 710, 237))
    b.append(varrow(870, 265, 280))
    b.append(label(550, 370, "correlation ID ties every event to the originating user session", "sm"))
    b.append(label(550, 430, "Forensic readiness: full session reconstruction from immutable logs (MIR-06).", "sm"))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 5: Network boundaries
# ------------------------------------------------------------------
def d5_network():
    w, h = 1080, 560
    b = []
    b.append(zone(20, 30, 330, 480, "PUBLIC / CLIENT ZONE", "#fdf6ec"))
    b.append(zone(370, 30, 300, 480, "AGENT ZONE (SANDBOXES)", "#f0f4f8"))
    b.append(zone(690, 30, 370, 480, "TRUSTED SERVICE ZONE", "#eef7ee"))
    b.append(box(60, 70, 250, 60, WHITE, "Users / Browsers / Apps", "TLS 1.3 ingress"))
    b.append(box(60, 160, 250, 60, WHITE, "Agent Orchestrator APIs", "authenticated"))
    b.append(box(410, 70, 230, 90, WHITE, "Agent Sandbox Pods", "NetworkPolicy: egress allow-list only", cap="EE-01"))
    b.append(box(410, 200, 230, 90, WHITE, "Policy Engine (OPA)", "deny by default", cap="ALLOW-LIST"))
    b.append(box(410, 330, 230, 90, WHITE, "Tool Gateway / MCP", "allow-listed endpoints only", cap="TP-03/08"))
    b.append(box(725, 70, 300, 70, WHITE, "Registered Tools & APIs", "explicitly registered", cap="TP-01"))
    b.append(box(725, 170, 300, 70, WHITE, "Model Providers (egress)", "signed certs, IP allow-list"))
    b.append(box(725, 270, 300, 70, WHITE, "Data Stores (RAG, memory)", "ABAC + encryption", cap="DS-01..07"))
    b.append(box(725, 380, 300, 80, "#fdf0f0", "CLOUD CONTROL PLANES - BLOCKED", "EC2, IAM, Lambda, KMS, Azure RM, GCP CRM", cap="EE-02 / TP-08", stroke=RED))
    b.append(arrow(310, 100, 410, 115))
    b.append(arrow(310, 190, 410, 245))
    b.append(varrow(525, 160, 200))
    b.append(varrow(525, 290, 330))
    b.append(arrow(640, 115, 725, 105))
    b.append(arrow(640, 205, 725, 205))
    b.append(arrow(640, 375, 725, 305))
    b.append(arrow(640, 420, 725, 420, colour=RED, dash=True))
    b.append(label(520, 455, "agent -> control-plane attempts blocked + alerted (IoC)", "sm", RED))
    b.append(label(215, 260, "no direct path to", "sm"))
    b.append(label(215, 275, "infrastructure APIs", "sm"))
    b.append(label(870, 475, "Infrastructure APIs are only reachable as explicitly", "sm"))
    b.append(label(870, 490, "registered tools via TP-01 with risk acceptance (GRM-02).", "sm"))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 6: Sidecar topology
# ------------------------------------------------------------------
def d6_sidecar():
    w, h = 1080, 480
    b = []
    b.append(zone(20, 30, 640, 420, "KUBERNETES CLUSTER - AGENT NAMESPACE", "#f0f4f8"))
    b.append(zone(690, 30, 370, 420, "CENTRAL SERVICES", "#f7fafd"))
    for px, name in ((60, "Agent Pod A"), (360, "Agent Pod B")):
        b.append(box(px, 70, 280, 55, WHITE, name, "agent container (sandbox)"))
        b.append(box(px, 140, 280, 55, LTBL, "Sidecar: OPA Policy", "Rego eval per action"))
        b.append(box(px, 210, 280, 55, LTBL, "Sidecar: Tool Gateway", "allow-list, schema, audit"))
        b.append(box(px, 280, 280, 55, LTBL, "Sidecar: Telemetry", "OTLP exporter, audit buffer"))
        b.append(varrow(px + 140, 125, 140))
        b.append(varrow(px + 140, 195, 210))
        b.append(varrow(px + 140, 265, 280))
    b.append(label(340, 370, "sidecars fail closed: no policy / no audit = no action (EE-06)", "sm"))
    b.append(box(720, 70, 310, 55, WHITE, "Central Model Gateway", "guardrails, redaction"))
    b.append(box(720, 140, 310, 55, WHITE, "Tool Registry + MCP Gateway", "signed tool definitions"))
    b.append(box(720, 210, 310, 55, WHITE, "Identity Plane", "SPIFFE/SPIRE, JIT creds"))
    b.append(box(720, 280, 310, 55, WHITE, "SIEM / Compliance", "dashboards, reporting"))
    for y, lbl in ((105, "policy + tool decisions"), (175, "audit events"), (245, "identity checks")):
        b.append(arrow(340, y, 720, y, dash=True))
        b.append(label(530, y - 8, lbl, "sm"))
    b.append(label(540, 440, "Scale: 10-100 agents. Beyond 100: central gateway for external tools, sidecars retained for per-agent policy and audit.", "sm"))
    return svg(w, h, "\n  ".join(b))


# ------------------------------------------------------------------
# Diagram 7: Maturity component coverage
# ------------------------------------------------------------------
def d7_maturity():
    w, h = 1080, 560
    b = []
    for x, t in ((30, "L1  INITIAL"), (290, "L2  MANAGED"), (550, "L3  DEFINED"), (810, "L4  OPTIMISED")):
        b.append(box(x, 30, 250, 40, NAVY, t, fs=13, white_text=True))
    l1 = [
        "Model inventory (MS-06)",
        "Container per agent (EE-01 basic)",
        "Basic logging (MIR-01)",
        "Per-agent accounts (IAM-01)",
        "Prompt injection testing (MS-04)",
    ]
    l2 = [
        "+ Model registry + signing (MS-03)",
        "+ Read-only rootfs, NetworkPolicy (EE-01)",
        "+ Resource limits (EE-03)",
        "+ Tool registry (TP-01)",
        "+ Structured audit logs (MIR-01)",
        "+ RAG security layer (DS-01/04)",
    ]
    l3 = [
        "+ OPA policy engine (IAM-02/07/08)",
        "+ Tool gateway / MCP gateway (TP-03/08)",
        "+ seccomp/AppArmor (EE-01)",
        "+ Host-file injection prevention (EE-05)",
        "+ Fail-closed sandbox (EE-06)",
        "+ SIEM + anomaly detection (MIR-02)",
        "+ Reporting triggers (MIR-05)",
    ]
    l4 = [
        "+ Remote attestation (EE-01)",
        "+ Continuous red-teaming (MS-04)",
        "+ AI-specific threat intel",
        "+ Multi-entity governance (GRM-01)",
        "+ Continuous compliance (GRM-05/06)",
    ]
    for x, items in ((30, l1), (290, l2), (550, l3), (810, l4)):
        b.append(zone(x, 80, 250, 380, "", "#fbfcfd"))
        yy = 110
        for it in items:
            b.append(label(x + 125, yy, it, "label", bold=False, size=11))
            yy += 26
    b.append(arrow(280, 100, 290, 100))
    b.append(arrow(540, 100, 550, 100))
    b.append(arrow(800, 100, 810, 100))
    b.append(label(540, 500, "Each level adds deployable components -- sequencing follows the Assessment Guide's maturity progression (weakest pillar first).", "sm"))
    b.append(label(540, 535, "Indicative progression: L1->L2 3-4 months | L1->L3 8-12 months | L3->L4 12+ months", "sm"))
    return svg(w, h, "\n  ".join(b))


DIAGRAMS = [
    ("impl-reference-architecture.svg", d1_reference),
    ("impl-policy-decision-points.svg", d2_policy),
    ("impl-request-flow.svg", d3_flow),
    ("impl-telemetry-pipeline.svg", d4_telemetry),
    ("impl-network-boundaries.svg", d5_network),
    ("impl-sidecar-topology.svg", d6_sidecar),
    ("impl-maturity-components.svg", d7_maturity),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name, fn in DIAGRAMS:
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, "w") as f:
            f.write(fn())
        print(f"  {name} ({os.path.getsize(path):,} bytes)")


if __name__ == "__main__":
    main()
