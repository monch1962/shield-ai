# SHIELD-AI(TM)

**S**ecurity and **H**olistic **I**ntegrity for **E**nterprise-**L**evel **D**eployment of **A**rtificial **I**ntelligence

A sovereign Australian framework for securing agentic AI systems -- designed for Australian enterprises and government bodies, mapped to all relevant Australian regulatory frameworks, and independent of cloud providers, LLMs, and industry verticals.

## Repository Structure

```
shield-ai/
+-- README.md                           # This file
+-- framework/                          # The core SHIELD-AI framework documents
|   +-- shield-ai-framework.md          #   Full framework (v1.5)
|   +-- shield-ai-framework.pdf         #   PDF
|   +-- shield-ai-framework.epub        #   EPUB for ereaders
|   +-- shield-ai-implementation-architecture.md   #   Deployable components, reference
|   |                                          #   architecture, full diagram set (NEW)
|   +-- shield-ai-implementation-architecture.pdf
|   +-- shield-ai-implementation-architecture.epub
|   +-- shield-ai-gap-analysis.md       #   Sandbox escape gap analysis (v1.5)
|   +-- shield-ai-gap-analysis.pdf      #   Gap analysis PDF
|   +-- shield-ai-gap-analysis.epub     #   Gap analysis EPUB
|   +-- shield-ai-watchlist.md          #   Always-current watchlist (replaced monthly)
|   +-- shield-ai-watchlist.pdf         #   Watchlist PDF
|   +-- shield-ai-watchlist.epub        #   Watchlist EPUB
+-- assessment-guide/                   # Consultant's field manual
|   +-- shield-ai-assessment-guide.md   #   Full guide, all 7 pillars x 55 controls
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
|   |   +-- shield-ai-deck-bridge.html    #   Reveal.js HTML slides (7 slides)
|   |   +-- shield-ai-deck-bridge.pdf     #   PDF version
|   +-- VERSIONS.md                     # Deck version changelog (all decks)
+-- client-specific/                    # Client-specific materials (one dir per client)
|   +-- defence/                        # Australian Defence Department briefing
|   |   +-- shield-ai-deck-defence.pptx  #   PowerPoint, 24 slides (deck v1.2)
|   |   +-- deck-manifest.json            #   Version + build metadata
|   |   +-- defence-alignment.svg         #   PSPF/ISM/E8/SOCI/Five Eyes map
|   |   +-- build_deck.py                 #   Builder (regenerates the deck)
|   +-- aware-super/                    # Aware Super production-AI briefing
|       +-- shield-ai-deck-aware-super.pptx  #  PowerPoint, 24 slides (deck v1.0)
|       +-- deck-manifest.json              #  Version + build metadata
|       +-- aware-super-alignment.svg       #  CPS 234/CPG 230/APP 11/ASIC map
|       +-- build_deck.py                   #  Builder (regenerates the deck)
+-- policies/                           # Policy-as-code control stubs (Rego/OPA)
|   +-- shield_ai_*.rego               #   55 machine-readable control stubs
|   +-- shield_ai_<pillar>_<id>.rego   #   (MS, IAM, DS, TP, MIR, GRM, EE)
+-- assets/
|   +-- diagrams/                       # SVG diagram set (framework + implementation)
|   +-- shield-ai-control-schema.json   # Machine-readable control definitions (v1.5)
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

- **55 Controls** across all pillars, each with implementation guidance,
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

- **[Watchlist (Markdown)](framework/shield-ai-watchlist.md)** -- the always-current
  watchlist of components under active monitoring (IETF A2A, Open Secure AI
  Alliance/NOOA, time-based supply-chain defences, edge/on-device agents,
  inbound MCP exposure, adversary-owned agents); rebuilt and REPLACED by each
  monthly deep review cycle

- **[Gap Analysis (Markdown)](framework/shield-ai-gap-analysis.md)** -- sandbox escape
  incident research driving framework evolution (v1.5, 25 incidents, 19 gaps)

- **[Tooling and Process Map (Markdown)](framework/shield-ai-tooling-map.md)** --
  tools and processes addressing all 55 controls, each assessed with the Six
  Thinking Hats; coverage analysis and an L1-L4 adoption roadmap (PDF/EPUB available)

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

The `.pptx` briefing decks live under `client-specific/<client>/` (one
directory per client: deck, manifest, alignment diagram, builder script).
They are generated by their `build_deck.py` builders and carry a deck version
stamped in the footer. Version history: [presentations/VERSIONS.md](presentations/VERSIONS.md).
Each deck ships with a `deck-manifest.json` recording version, slide count,
diagrams, builder script, and the exact git commit it was built from.

## Framework Version

**v1.5** -- August 3, 2026 (monthly deep review: added perception-fidelity enforcement MS-09, agent-originated artifact publication control DS-07, agent platform inbound control-plane protection TP-10, and evaluation-harness isolation and integrity EE-08; extended MS-04/MS-08/IAM-03/EE-07/MIR-02/GRM-02/GRM-04; addressed the Anthropic evaluation-breach cluster, AWS Kiro, OpenClaw, Azure DevOps MCP, Unit 42 autonomous-attacker campaign, Metasploit/Wiz MCP research, and Android on-device agent incidents; 55 controls)

**v1.4** -- August 3, 2026 (added fail-closed sandbox operation EE-06, agent control-plane configuration integrity EE-07, multi-tenant agent platform isolation IAM-09, explicit tool registration TP-09; extended TP-04/TP-06/MIR-02 for interpreter-flag misuse, code-validation endpoints, and swarm-campaign detection; addressed CrewAI, Codex CLI, CVE-2026-35603, Langflow KEV, Semantic Kernel/.NET SDK, DeepSeek incidents)

**v1.3** -- July 27, 2026 (added host-trusted file injection prevention EE-05 and MCP security controls MS-08; 50 controls)

**v1.2** -- July 2026 (added P7 Execution Environment pillar, EE-01 to EE-04, IAM-07/08, TP-07/08, MS-07)

**v1.1** -- July 2026 (initial framework: 6 pillars, 36 controls)

Authored by the Security Architecture Practice.
