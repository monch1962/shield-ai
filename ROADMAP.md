# SHIELD-AI(TM) Roadmap

> Framework evolution roadmap -- updated August 2026
> Supersedes the July 2026 commercialisation plan (pricing and go-to-market
> strategy are maintained outside this repository).

## Current State

| Artifact | Status | Notes |
|----------|--------|-------|
| Framework document v1.6 | [OK] Complete | 7 pillars, 57 controls, 4 maturity levels |
| Sandbox escape gap analysis v1.6 | [OK] Complete | 32 incidents, 21 gaps |
| Watchlist | [OK] Monthly | Canonical framework/shield-ai-watchlist.md, replaced each deep review |
| Tooling and process map | [OK] Complete | All 57 controls mapped, six-hat assessment, L1-L4 roadmap |
| Implementation architecture | [OK] Complete | Deployable components + full SVG diagram set |
| Assessment guide | [OK] Complete | All 7 pillars x 57 controls |
| Business slide deck (14 slides) | [OK] Complete | For CISO/CRO/Board |
| Technical slide deck (27 slides) | [OK] Complete | For AI engineers, security architects |
| Buyer's journey bridge (7 slides) | [OK] Complete | Connects both decks |
| Defence briefing deck (24 slides) | [OK] Versioned | v1.2, client-specific/defence/ |
| Aware Super briefing deck (24 slides) | [OK] Versioned | v1.0, client-specific/aware-super/ |
| JSON control schema | [OK] v1.6 | 57 controls, machine-readable |
| Rego policy stubs (57) | [OK] Complete | All 7 pillars; TODOs to assertions next |
| GitHub repo | [OK] Complete | Private, all artifacts |

## Priority Ranking (technical)

| Pri | Item | Verdict | Effort | Impact |
|-----|------|---------|--------|--------|
| [X] | Rego policy stubs for all 57 controls | Complete (v1.6) | Per-control | Automated control testing per GRM-05/06 |
| [X] | EE pillar policy stubs (EE-01..08) | Complete (v1.6) | 1-2 days | Closed the largest stub gap |
| P1 | Reference implementation (deployable tooling from the implementation architecture doc) | Next milestone | Multi-week | Validates the component model against real environments |
| P2 | Public release | After field validation | 1 day | Community adoption |
| P3 | Partner enablement programme | After P2 | Ongoing | Scale via partners |
| -- | Guardrails positioning paper | Deferred -- legislation not yet passed | 4 hours | Regulatory positioning |
| [X] | Compliance dashboard (SaaS) | **Killed** -- premature detour | -- | -- |
| [X] | NZ market expansion | **Killed** -- premature | -- | -- |

## Next Milestones

### Milestone 1: Convert the Rego policy set to evaluable assertions
- Convert the 57 shipped stubs from TODO bodies to evaluable assertions with test vectors
- Wire the policy set into the reference architecture's policy decision points

### Milestone 2: Reference implementation of the deployable components
- Build the tool gateway / sidecar proxy from the implementation architecture document
- Deploy the OPA policy layer with the full Rego set
- Instrument the telemetry pipeline (OTLP -> SIEM) per MIR-01..06
- Validate against real agent frameworks (LangGraph, CrewAI, Semantic Kernel, etc.)

### Milestone 3: Field validation
- Exercise the assessment guide against real agent deployments
- Feed findings back into the framework (v1.6 cycle)
- Generate case study material (sanitised)

## Key Decisions

### What stays unchanged
- Framework v1.6 -- frozen pending field feedback
- Assessment guide -- will be tested and refined in first field use
- Three slide decks -- use them in outreach and enablement
- JSON schema + Rego stubs -- good enough for tooling baseline

### What changes
- Rego implementation advances from "per-client later" to "next milestone" (the
  implementation architecture document defines the policy decision points that
  the stubs must satisfy)

- Implementation architecture document is the canonical reference for all
  deployable components

### What was killed
- **SaaS compliance dashboard** (6-12 month detour)
- **NZ market expansion** (premature without AU validation)

### What was deferred
- Public release (do after field validation makes content stronger)
- Partner programme (after public release)
- Guardrails mapping (positioning paper only until legislation passes)
