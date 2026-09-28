# SHIELD-AI

**S**ecurity and **H**olistic **I**ntegrity for **E**nterprise-**L**evel **D**eployment of **A**rtificial **I**ntelligence

A sovereign Australian framework for securing agentic AI systems, designed for Australian enterprises and government bodies. Mapped to all relevant Australian regulatory frameworks and independent of cloud providers, LLMs, and industry verticals.

**Current version:** [v1.16](CHANGELOG.md) (October 5, 2026) — 63 controls, 69 incidents, 27 gaps

---

## Repository Structure

```
shield-ai/
├── framework/            Core framework documents (Markdown + PDF + EPUB)
│   ├── shield-ai-framework.md                 Full framework definition
│   ├── shield-ai-implementation-architecture.md  Deployable components + diagrams
│   ├── shield-ai-gap-analysis.md              Sandbox escape gap analysis
│   ├── shield-ai-field-findings.md            Field validation lessons (FF-01..)
│   ├── shield-ai-watchlist.md                 Current watchlist (rebuilt monthly)
│   ├── shield-ai-tooling-map.md               Tools/processes covering all controls
│   ├── shield-ai-deep-review-*.md             Monthly deep-review records (2026-08, 2026-09)
│   └── shield-ai-reference-architecture-walkthrough.md
├── assessment-guide/     Consultant's field manual (7 pillars × 63 controls)
├── presentations/        Slide decks + static deliverables
│   ├── business-deck/         14-slide business decision-maker deck
│   ├── technical-deck/        27-slide technical SME deck
│   ├── board-brief/           Board-level brief
│   ├── buyers-journey-bridge/ Connects business ↔ technical
│   ├── reference-architecture-walkthrough/  PPTX walkthrough
│   ├── what-is-shield-ai.md/glossary.md      Static explainers (MD/PDF/EPUB)
│   └── VERSIONS.md           Deck version changelog
├── client-specific/      Client materials (one directory per client)
│   ├── defence/           Australian Defence briefing
│   ├── aware-super/       Aware Super production-AI briefing
│   ├── nbn/               NBN Co national-infrastructure briefing
│   └── retailer/          Retail-sector briefing
├── exploits/             Novel AI exploit catalog (G1–G27, one entry per type)
├── policies/             Policy-as-code controls (63 Rego/OPA, deny-override)
├── case-studies/         Sanitised field-validation records
├── reference-impl/       Milestone 2: runnable Go sidecar + OPA + telemetry
├── demo/                 Demo policies + OPA inputs/tests + docker-compose
├── infra/                Infrastructure notes (domain plan)
├── assets/               Diagrams, control schema JSON, brand, CSS
└── tools/                Generators + verification gates + build pipeline
```

## Framework at a Glance

- **7 Pillars:** Model Security (MS) · Identity & Access (IAM) · Data Security (DS) · Tool & Pipeline Security (TP) · Monitoring & Incident Response (MIR) · Governance & Risk Management (GRM) · Execution Environment (EE)
- **63 Controls** across all pillars, each with implementation guidance, maturity indicators and regulatory mappings (of which 60 are implemented as executable Rego; 3 are scaffolded stubs — MS-12, TP-13, TP-15).
- **4 Maturity Levels:** L1 (Initial) → L2 (Managed) → L3 (Defined) → L4 (Optimised)
- **Regulatory Alignment:** ISM, Essential Eight, SOCI Act, APRA CPS 234, PSPF, Privacy Act 1988, OWASP LLM Top 10 v2, NIST AI RMF, EU AI Act, ISO/IEC 42001, Google SAIF, MITRE ATLAS, AU Mandatory Guardrails (proposed)

## Key Documents

- **[Framework](framework/shield-ai-framework.md)** — principles, pillars, control mappings, emerging-trends coverage (2026–2029)
- **[Implementation Architecture](framework/shield-ai-implementation-architecture.md)** — deployable component model with full SVG diagram set
- **[Gap Analysis](framework/shield-ai-gap-analysis.md)** — sandbox-escape incident research driving framework evolution (v1.16, 69 incidents, 27 gaps)
- **[Watchlist](framework/shield-ai-watchlist.md)** — components under active monitoring; rebuilt and replaced each monthly deep-review cycle
- **[Novel AI Exploit Catalog](exploits/README.md)** — one entry per exploit type (G1–G27) mapped to covering controls
- **[Tooling and Process Map](framework/shield-ai-tooling-map.md)** — tools and processes covering all 63 controls, with L1–L4 adoption roadmap
- **[Assessment Guide](assessment-guide/shield-ai-assessment-guide.md)** — consultant's field manual with per-control assessment questions, artifacts, maturity indicators
- **[Control Schema](assets/shield-ai-control-schema.json)** — machine-readable control definitions for tooling and automation
- **[Policy-as-Code](policies/)** — the 63 controls as executable deny-override Rego policies with test vectors (see `policies/README.md`)
- **[Case Studies](case-studies/README.md)** — sanitised field-validation records
- **[Field Findings](framework/shield-ai-field-findings.md)** — lessons staged for the next framework cycle
- **[Changelog](CHANGELOG.md)** — full release history (v1.1 → v1.16)

## How to View Slides

Open the `.html` files in any web browser. Navigate with arrow keys; `O` for overview, `ESC` for the slide navigator.

The `.pptx` briefing decks live under `client-specific/<client>/` — each directory holds the deck, its `deck-manifest.json` (version, slide count, diagram set, builder script, build commit), an alignment diagram, and the `build_deck.py` builder. Rebuild a deck by running its builder from the repo root:

```bash
/usr/bin/python3 client-specific/<client>/build_deck.py
```

Deck version history: [presentations/VERSIONS.md](presentations/VERSIONS.md).

## Local Gates

Before committing, run the local gate suite:

```bash
make check
```

This regenerates the control schema and Rego stubs non-destructively, then runs the list-spacing scan, artifact verification (including README freshness), the exploit-catalog gate, and all OPA policy tests.

Git hooks are versioned in `.githooks/` and enforce the gates automatically (`pre-commit` runs the cheap checks; `pre-push` runs the full `make check`). Enable them once per clone:

```bash
git config core.hooksPath .githooks
```

Bypass with `git commit --no-verify` / `git push --no-verify` only when you know the gates would pass (e.g. a mechanical manifest refresh).

## Keep the README Tidy

This README stays stable by construction, not by discipline:

- **Version history lives in [CHANGELOG.md](CHANGELOG.md).** Every release appends one entry there. The README carries only the current-version line near the top — so it cannot grow unboundedly.
- **The structure tree and all document links are gate-checked.** `make check` (via `tools/verify_artifacts.py`) verifies every relative path in the README resolves to an existing file and that the current version/control counts are present. A stale tree or broken link fails the gate before anything ships.
- When you add a file or directory to the repo, update this tree in the same change — the gate will remind you, but it cannot auto-generate the tree for you, so keep the listing accurate.

---

Authored by the Security Architecture Practice.