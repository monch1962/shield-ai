# SHIELD-AI(TM)

**S**ecurity and **H**olistic **I**ntegrity for **E**nterprise-**L**evel **D**eployment of **A**rtificial **I**ntelligence

A sovereign Australian framework for securing agentic AI systems -- designed for Australian enterprises and government bodies, mapped to all relevant Australian regulatory frameworks, and independent of cloud providers, LLMs, and industry verticals.

## Repository Structure

```
shield-ai/
+-- README.md                           # This file
+-- framework/                          # The core SHIELD-AI framework documents
|   +-- shield-ai-framework.md          #   Full framework (v1.4)
|   +-- shield-ai-framework.pdf         #   PDF
|   +-- shield-ai-framework.epub        #   EPUB for ereaders
|   +-- shield-ai-implementation-architecture.md   #   Deployable components, reference
|   |                                          #   architecture, full diagram set (NEW)
|   +-- shield-ai-implementation-architecture.pdf
|   +-- shield-ai-implementation-architecture.epub
|   +-- shield-ai-gap-analysis.md       #   Sandbox escape gap analysis (v1.4)
|   +-- shield-ai-gap-analysis.pdf      #   Gap analysis PDF
|   +-- shield-ai-gap-analysis.epub     #   Gap analysis EPUB
+-- assessment-guide/                   # Consultant's field manual
|   +-- shield-ai-assessment-guide.md   #   Full guide, all 7 pillars x 51 controls
|   +-- shield-ai-assessment-guide.pdf  #   PDF
|   +-- shield-ai-assessment-guide.epub #   EPUB for field use
+-- presentations/
|   +-- business-deck/                  # Business decision-maker slide deck
|   |   +-- shield-ai-deck-business.html  #   Reveal.js HTML slides (14 slides)
|   |   +-- shield-ai-deck-business.pdf   #   PDF version
|   +-- technical-deck/                 # Technical SME deep-dive slide deck
|   |   +-- shield-ai-deck-technical.html #   Reveal.js HTML slides (27 slides)
|   |   +-- shield-ai-deck-technical.pdf  #   PDF version
|   +-- buyers-journey-bridge/          # Bridge deck connecting the two
|       +-- shield-ai-deck-bridge.html    #   Reveal.js HTML slides (7 slides)
|       +-- shield-ai-deck-bridge.pdf     #   PDF version
+-- policies/                           # Policy-as-code control stubs (Rego/OPA)
|   +-- shield_ai_ms_*.rego             #   36 machine-readable control stubs
|   +-- shield_ai_iam_*.rego            #   (MS, IAM, DS, TP, MIR, GRM)
+-- assets/
|   +-- diagrams/                       # SVG diagram set (framework + implementation)
|   +-- shield-ai-control-schema.json   # Machine-readable control definitions (v1.4)
|   +-- logo*.svg                       # Brand assets
|   +-- style.css                       # Document styling (Markdown/HTML/PDF/EPUB)
+-- tools/
    +-- generate_control_schema.py      # Regenerates control schema JSON + Rego stubs
    +-- generate_diagrams.py            # Regenerates SVG diagrams
```

## Framework at a Glance

- **7 Pillars**: Model Security (MS), Identity & Access (IAM), Data Security (DS),
  Tool & Pipeline Security (TP), Monitoring & Incident Response (MIR),
  Governance & Risk Management (GRM), Execution Environment (EE)

- **51 Controls** across all pillars, each with implementation guidance,
  maturity indicators, and regulatory mappings

- **4 Maturity Levels**: L1 (Initial) -> L2 (Managed) -> L3 (Defined) -> L4 (Optimised)
- **Regulatory Alignment**: ISM, Essential Eight, SOCI Act, APRA CPS 234,
  PSPF, Privacy Act 1988, OWASP LLM Top 10 v2, NIST AI RMF, EU AI Act,
  ISO/IEC 42001, Google SAIF, MITRE ATLAS, AU Mandatory Guardrails (proposed)

## Key Documents

- **[Framework (Markdown)](framework/shield-ai-framework.md)** -- the complete framework
  definition, principles, pillars, control mappings, and emerging trends coverage
  (2026-2029)

- **[Implementation Architecture (Markdown)](framework/shield-ai-implementation-architecture.md)** --
  the deployable component model: what to build and deploy to implement SHIELD-AI,
  with a full set of SVG diagrams and explanatory text (reference architecture,
  policy decision points, request flows, telemetry pipeline, network boundaries,
  deployment topologies, maturity mapping)

- **[Gap Analysis (Markdown)](framework/shield-ai-gap-analysis.md)** -- sandbox escape
  incident research driving framework evolution (v1.4, 17 incidents, 13 gaps)

- **[Assessment Guide (Markdown)](assessment-guide/shield-ai-assessment-guide.md)** --
  consultant's field manual with per-control assessment questions, artifacts to
  examine, maturity indicators, progression paths, and regulatory cross-reference

- **[Business Deck (HTML)](presentations/business-deck/shield-ai-deck-business.html)** --
  14-slide Reveal.js presentation for CISO/CRO/Board stakeholders

- **[Technical Deck (HTML)](presentations/technical-deck/shield-ai-deck-technical.html)** --
  27-slide Reveal.js deep-dive for AI engineers, security architects, and
  platform teams

- **[Control Schema (JSON)](assets/shield-ai-control-schema.json)** -- machine-readable
  control definitions for tooling and automation

- **[Policy Stubs (Rego)](policies/)** -- per-control policy-as-code stubs for the
  Open Policy Agent evaluation layer

## How to View Slides

Open the `.html` files in any web browser. Navigate with arrow keys. Press `O` for overview, `ESC` for slide navigator.

## Framework Version

**v1.4** -- August 3, 2026 (added fail-closed sandbox operation EE-06, agent control-plane configuration integrity EE-07, multi-tenant agent platform isolation IAM-09, explicit tool registration TP-09; extended TP-04/TP-06/MIR-02 for interpreter-flag misuse, code-validation endpoints, and swarm-campaign detection; addressed CrewAI, Codex CLI, CVE-2026-35603, Langflow KEV, Semantic Kernel/.NET SDK, DeepSeek incidents)

**v1.3** -- July 27, 2026 (added host-trusted file injection prevention EE-05 and MCP security controls MS-08; 50 controls)

**v1.2** -- July 2026 (added P7 Execution Environment pillar, EE-01 to EE-04, IAM-07/08, TP-07/08, MS-07)

**v1.1** -- July 2026 (initial framework: 6 pillars, 36 controls)

Authored by the Security Architecture Practice.
