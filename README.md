# SHIELD-AI(TM)

**S**ecurity and **H**olistic **I**ntegrity for **E**nterprise-**L**evel **D**eployment of **A**rtificial **I**ntelligence

A sovereign Australian framework for securing agentic AI systems -- designed for Australian enterprises and government bodies, mapped to all relevant Australian regulatory frameworks, and independent of cloud providers, LLMs, and industry verticals.

## Repository Structure

```
shield-ai/
+-- README.md                           # This file
+-- framework/                          # The core SHIELD-AI framework document
|   +-- shield-ai-framework.md          #   Full framework (v1.4, updated with EE-06/07, IAM-09, TP-09)
|   +-- shield-ai-framework.pdf         #   PDF (updated)
|   +-- shield-ai-framework.epub        #   EPUB for ereaders
|   +-- shield-ai-gap-analysis.md       #   Sandbox escape gap analysis (v1.4)
|   +-- shield-ai-gap-analysis.pdf      #   Gap analysis PDF
|   +-- shield-ai-gap-analysis.epub     #   Gap analysis EPUB
+-- presentations/
|   +-- business-deck/                  # Business decision-maker slide deck
|   |   +-- shield-ai-deck-business.html  #   Reveal.js HTML slides (15 slides)
|   |   +-- shield-ai-deck-business.pdf   #   PDF version
|   +-- technical-deck/                 # Technical SME deep-dive slide deck
|   |   +-- shield-ai-deck-technical.html #   Reveal.js HTML slides (26 slides)
|   |   +-- shield-ai-deck-technical.pdf  #   PDF version
|   +-- buyers-journey-bridge/          # Bridge deck connecting the two
|       +-- shield-ai-deck-bridge.html    #   Reveal.js HTML slides (8 slides)
|       +-- shield-ai-deck-bridge.pdf     #   PDF version
+-- assessment-guide/                   # Consultant's field manual
    +-- shield-ai-assessment-guide.md   #   Full guide (14,401 words)
    +-- shield-ai-assessment-guide.pdf  #   PDF (47 pages)
    +-- shield-ai-assessment-guide.epub #   EPUB for field use
```

## Framework at a Glance

- **7 Pillars**: Model Security (MS), Identity & Access (IAM), Data Security (DS),
  Tool & Pipeline Security (TP), Monitoring & Incident Response (MIR),
  Governance & Risk Management (GRM), **Execution Environment (EE) -- NEW**
- **46 Controls** across all pillars, each with implementation guidance,
  maturity indicators, and regulatory mappings
- **4 Maturity Levels**: L1 (Initial) -> L2 (Managed) -> L3 (Defined) -> L4 (Optimised)
- **Regulatory Alignment**: ISM, Essential Eight, SOCI Act, APRA CPS 234,
  PSPF, Privacy Act 1988, OWASP LLM Top 10 v2, NIST AI RMF, EU AI Act,
  ISO/IEC 42001, Google SAIF, MITRE ATLAS, AU Mandatory Guardrails (proposed)

## Service Tiers

| Tier | Investment | Duration | Target Maturity |
|------|-----------|----------|-----------------|
| Lite | $25-45K | 2-3 weeks | L1->L2 awareness |
| Standard | $120-250K | 12-16 weeks + 6mo assurance | L3 defined |
| Enterprise | $400-800K+/yr | Ongoing | L4 optimised |

## Key Documents

- **[Framework (Markdown)](framework/shield-ai-framework.md)** -- the complete framework
  definition, principles, pillars, control mappings, business offering, and emerging
  trends coverage (2026-2029)
- **[Assessment Guide (Markdown)](assessment-guide/shield-ai-assessment-guide.md)** --
  consultant's field manual with per-control assessment questions, artifacts to
  examine, maturity indicators, progression paths, and regulatory cross-reference
- **[Business Deck (HTML)](presentations/business-deck/shield-ai-deck-business.html)** --
  15-slide Reveal.js presentation for CISO/CRO/Board stakeholders
- **[Technical Deck (HTML)](presentations/technical-deck/shield-ai-deck-technical.html)** --
  26-slide Reveal.js deep-dive for AI engineers, security architects, and
  platform teams

## How to View Slides

Open the `.html` files in any web browser. Navigate with arrow keys. Press `O` for overview, `ESC` for slide navigator.

## Framework Version

**v1.4** -- August 3, 2026 (added fail-closed sandbox operation EE-06, agent control-plane configuration integrity EE-07, multi-tenant agent platform isolation IAM-09, explicit tool registration TP-09; extended TP-04/TP-06/MIR-02 for interpreter-flag misuse, code-validation endpoints, and swarm-campaign detection; addressed CrewAI, Codex CLI, CVE-2026-35603, Langflow KEV, Semantic Kernel/.NET SDK, DeepSeek incidents)

**v1.3** -- July 27, 2026 (added host-trusted file injection prevention EE-05 and MCP security controls MS-08; 50 controls)

**v1.2** -- July 2026 (added P7 Execution Environment pillar, EE-01 to EE-04, IAM-07/08, TP-07/08, MS-07)

Authored by the Security Architecture Practice.
