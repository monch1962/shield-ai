# SHIELD-AI(TM)

**S**ecurity and **H**olistic **I**ntegrity for **E**nterprise-**L**evel **D**eployment of **A**rtificial **I**ntelligence

A sovereign Australian framework for securing agentic AI systems -- designed for Australian enterprises and government bodies, mapped to all relevant Australian regulatory frameworks, and independent of cloud providers, LLMs, and industry verticals.

## Repository Structure

```
shield-ai/
+-- README.md                           # This file
+-- framework/                          # The core SHIELD-AI framework documents
|   +-- shield-ai-framework.md          #   Full framework (v1.9)
|   +-- shield-ai-framework.pdf         #   PDF
|   +-- shield-ai-framework.epub        #   EPUB for ereaders
|   +-- shield-ai-implementation-architecture.md   #   Deployable components, reference
|   |                                          #   architecture, full diagram set (NEW)
|   +-- shield-ai-implementation-architecture.pdf
|   +-- shield-ai-implementation-architecture.epub
|   +-- shield-ai-gap-analysis.md       #   Sandbox escape gap analysis (v1.9)
|   +-- shield-ai-field-findings.md     #   Field validation findings, staged for the
|                                      #   next framework cycle (FF-01..FF-06)
|   +-- shield-ai-gap-analysis.pdf      #   Gap analysis PDF
|   +-- shield-ai-gap-analysis.epub     #   Gap analysis EPUB
|   +-- shield-ai-watchlist.md          #   Always-current watchlist (replaced monthly)
|   +-- shield-ai-watchlist.pdf         #   Watchlist PDF
|   +-- shield-ai-watchlist.epub        #   Watchlist EPUB
+-- assessment-guide/                   # Consultant's field manual
|   +-- shield-ai-assessment-guide.md   #   Full guide, all 7 pillars x 61 controls
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
|   +-- nbn/                            # NBN Co national-infrastructure briefing
|       +-- shield-ai-deck-nbn.pptx         #  PowerPoint, 25 slides (deck v1.0)
|       +-- deck-manifest.json              #  Version + build metadata
|       +-- nbn-alignment.svg               #  SOCI Act/TSSR/APP 11/ISM-E8 map
|       +-- build_deck.py                   #  Builder (regenerates the deck)
+-- exploits/                           # Novel AI exploit catalog (per-type entries)
|   +-- README.md                       #   Index + coverage table (25 classes, v1.9)
|   +-- g01-..g25-*.md                  #   One entry per exploit type (G1-G25)
|   +-- _TEMPLATE.md                    #   Entry format for the monitoring cycles
|   +-- exploit-catalog.pdf             #   Combined PDF (README + all entries)
|   +-- exploit-catalog.epub            #   Combined EPUB
+-- policies/                           # Policy-as-code controls (Rego/OPA, 61/61 shipped)
|   +-- shield_ai_*.rego               #   61 machine-readable controls (59 implemented + MS-12, TP-13 stubs)
|   +-- shield_ai_<pillar>_<id>.rego   #   (MS, IAM, DS, TP, MIR, GRM, EE)
+-- case-studies/                     # Sanitised field-validation records (M3)
|   +-- 2026-08-reference-implementation.md  # First assessment (overall L1)
+-- reference-impl/                    # Milestone 2: runnable sidecar + OPA + telemetry
|   +-- sidecar/                       #   Go gateway: enrich -> decide -> audit (stdlib only)
|   +-- scripts/e2e.sh                 #   End-to-end verdict matrix against the 59 policies
|   +-- docker-compose.yml             #   OPA bundle + sidecar + mock tool/SIEM
+-- assets/
|   +-- diagrams/                       # SVG diagram set (framework + implementation)
|   +-- shield-ai-control-schema.json   # Machine-readable control definitions (v1.9)
|   +-- logo*.svg                       # Brand assets
|   +-- style.css                       # Document styling (Markdown/HTML/PDF/EPUB)
+-- tools/
    +-- generate_control_schema.py      # Regenerates control schema JSON + Rego stubs
    +-- generate_diagrams.py            # Regenerates SVG diagrams
    +-- check_exploit_catalog.py        # Catalog integrity gate (links + coverage)
```

## Framework at a Glance

- **7 Pillars**: Model Security (MS), Identity & Access (IAM), Data Security (DS),
  Tool & Pipeline Security (TP), Monitoring & Incident Response (MIR),
  Governance & Risk Management (GRM), Execution Environment (EE)

- **60 Controls** across all pillars, each with implementation guidance,
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
  incident research driving framework evolution (v1.9, 47 incidents, 25 gaps)

- **[Novel AI Exploit Catalog (Markdown)](exploits/README.md)** -- one entry per
  identified exploit type (G1-G25), with the nature of each exploit and the
  framework controls that cover it; maintained by the weekly and monthly
  monitoring cycles (PDF/EPUB available)

- **[Tooling and Process Map (Markdown)](framework/shield-ai-tooling-map.md)** --
  tools and processes addressing all 61 controls, each assessed with the Six
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

- **[Policy-as-Code (Rego)](policies/)** -- the 61 controls as executable,
  deny-override policies with test vectors; the shared input model and
  conversion conventions are documented in `policies/README.md`
- **[Case Studies (Markdown)](case-studies/README.md)** -- sanitised field-validation
  records; the first assessment (2026-08-reference-implementation) runs the full
  methodology and scores the reference implementation at overall L1
- **[Field Findings (Markdown)](framework/shield-ai-field-findings.md)** -- lessons
  from field validation, staged for adoption by the next framework cycle

## How to View Slides

Open the `.html` files in any web browser. Navigate with arrow keys. Press `O` for overview, `ESC` for slide navigator.

The `.pptx` briefing decks live under `client-specific/<client>/` (one
directory per client: deck, manifest, alignment diagram, builder script).
They are generated by their `build_deck.py` builders and carry a deck version
stamped in the footer. Version history: [presentations/VERSIONS.md](presentations/VERSIONS.md).
Each deck ships with a `deck-manifest.json` recording version, slide count,
diagrams, builder script, and the exact git commit it was built from.

## Local Gates

Before committing, run the local gate suite: `make check` (regenerates the
schema and Rego stubs non-destructively, then runs the list-spacing scan,
artifact verification, exploit catalog gate, and all OPA policy tests).

Git hooks are versioned in `.githooks/` and enforce the gates automatically:

- `pre-commit` runs the cheap checks (list-spacing, catalog gate, OPA tests)
- `pre-push` runs the full `make check` suite

Enable them once per clone:

```bash
git config core.hooksPath .githooks
```

Bypass with `git commit --no-verify` / `git push --no-verify` only when you
know the gates would pass (e.g. a mechanical manifest refresh).

## Framework Version

**v1.9** -- August 31, 2026 (weekly monitoring cycle: added agent dependency-install provenance verification TP-13 for gap G25 (the llms.txt dangling-install supply-chain class — unregistered-package installs executed by Claude, Codex, and Hermes in Fortune 500 environments, live malware at Clerk.com); extended MS-10 (model-definition/template-store integrity — NemoClaw CVE-2026-65105), TP-12 (provenance receipts at every trust boundary — Novee), and MS-12 (aggregate tool-surface screening — ShareLock); added INC-42..INC-47 (RovoBlast, ShareLock, llms.txt, NemoClaw, Novee trust-handoffs, Wiz Red Agent) plus the OpenAI full incident report and the HF technical timeline as INC-40 evidence; 61 controls)
**v1.8** -- August 24, 2026 (weekly monitoring cycle: added MCP discovery-metadata and shared-cache integrity MS-12 for gap G24; extended TP-06 (sandbox binding layers are part of the trust boundary; eval-with-empty-locals is not a sandbox), MS-09 (approval dialogs bind to the canonicalised, resolved action target), and MS-08 (discovery/cache surfaces); added INC-37..INC-41 (MCP-2026-008/015 and Context7 CVE-2026-75130, isolated-vm GHSA-864f-rcv7-6rh4 and Langroid CVE-2026-54769, browser-tools-mcp / atomic-agents-stack / mcp-searxng, OpenAI evaluation-escape follow-up disclosures, Wiz GhostApproval); 60 controls)
**v1.7** -- August 17, 2026 (weekly monitoring cycle: added operational data-stream integrity MS-11 and tool-call provenance and dispatch verification TP-12; extended MIR-02/IAM-03/TP-09/GRM-02; addressed GhostJacking observability-stream poisoning (Tenet, DEFCON 34), CoreBreak tool-dispatch provenance failures (AWS/Google/Vercel), the first autonomous multi-agent attack on critical infrastructure (Taiwan nuclear safety agency), and the AI-assisted exploit-development cluster (SharePoint chain, Zoomsday); G19 escalated to Critical; 59 controls)

**v1.6** -- August 10, 2026 (weekly monitoring cycle: added agent memory-store integrity MS-10 and agent browser and content-rendering isolation TP-11; extended EE-08/EE-01/MS-04/MS-09/IAM-03/MIR-02/GRM-04; addressed the Meta/Irregular third-party evaluation containment failure, UK AISI incident report, Kimi K3 benchmark-cheat escape, ChatMate Remote Prompt Execution against Microsoft 365 Copilot, Zenity Intent Collision agentic-browser takeover, Ruflo/RufRoot MCP-bridge RCE with persistent memory poisoning, and the first documented Australian autonomous agent attack; Langflow CVE-2026-9198 CISA KEV escalation; 57 controls)

**v1.5** -- August 3, 2026 (monthly deep review: added perception-fidelity enforcement MS-09, agent-originated artifact publication control DS-07, agent platform inbound control-plane protection TP-10, and evaluation-harness isolation and integrity EE-08; extended MS-04/MS-08/IAM-03/EE-07/MIR-02/GRM-02/GRM-04; addressed the Anthropic evaluation-breach cluster, AWS Kiro, OpenClaw, Azure DevOps MCP, Unit 42 autonomous-attacker campaign, Metasploit/Wiz MCP research, and Android on-device agent incidents; 55 controls)

**v1.4** -- August 3, 2026 (added fail-closed sandbox operation EE-06, agent control-plane configuration integrity EE-07, multi-tenant agent platform isolation IAM-09, explicit tool registration TP-09; extended TP-04/TP-06/MIR-02 for interpreter-flag misuse, code-validation endpoints, and swarm-campaign detection; addressed CrewAI, Codex CLI, CVE-2026-35603, Langflow KEV, Semantic Kernel/.NET SDK, DeepSeek incidents)

**v1.3** -- July 27, 2026 (added host-trusted file injection prevention EE-05 and MCP security controls MS-08; 50 controls)

**v1.2** -- July 2026 (added P7 Execution Environment pillar, EE-01 to EE-04, IAM-07/08, TP-07/08, MS-07)

**v1.1** -- July 2026 (initial framework: 6 pillars, 36 controls)

Authored by the Security Architecture Practice.
