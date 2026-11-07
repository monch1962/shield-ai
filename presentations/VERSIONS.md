# Presentation Deck Versions

Versioning convention: every change to a deck bumps its version and adds an
entry here. The version is stamped in the deck footer, and the machine-readable
deck-manifest.json (next to each .pptx) records the exact repo commit the deck
was built from. Client-specific materials live under `client-specific/<client>/`,
one directory per client, each self-contained (deck, manifest, client alignment
diagram, builder script). Rebuild a client deck with its builder:

- Defence briefing: `python3 client-specific/defence/build_deck.py`
- Aware Super briefing: `python3 client-specific/aware-super/build_deck.py`
- NBN Co briefing: `python3 client-specific/nbn/build_deck.py`
- Major Australian Retailer briefing: `python3 client-specific/retailer/build_deck.py`

The deck version is independent of the framework version (v1.14); a framework
update that changes deck content bumps the deck version, not the framework
version.

## Shield-AI Deck: Defence

| Version | Date | Change |
|---------|------|--------|
| 1.18 | 2026-11-08 | Updated to framework v1.21 (69 controls): INC-85..INC-90 (AgentScope unpatched MCP command injection, Langflow auth-bypass/MCP-enumeration RCE, seventeen-CVE framework RCE mega-cluster, MCP protocol pivoting, MCP trust-boundary measurement, WorkOS ARTEX escape), TP-16/MS-08/TP-15 guidance extensions, footer version bumped |
| 1.17 | 2026-11-07 | Updated to framework v1.20 (69 controls): INC-79..INC-84 (MCP connection-path OAuth RCE, MCP tool-argument injection wave, cross-tenant memory leakage, multi-tenant hosting escapes, CI config-file trust-ordering, visual prompt injection), new controls TP-16/MS-15, EE-01/MS-09/MS-13 extensions, footer version bumped |
| 1.16 | 2026-10-12 | Updated to framework v1.19 (67 controls): INC-77..INC-78 (VTCode CVE-2026-104247 learned-approval/blocklist bypass, loopback DNS-rebinding cluster), EE-07/MS-08 guidance extensions, footer version bumped |
| 1.15 | 2026-10-05 | Updated to framework v1.18 (67 controls): INC-74..INC-76 (GitLab AI Gateway CVE-2026-90970, Comment and Control CI, MCP tooling argument-injection cluster), TP-15/MS-08/EE-07 guidance extensions, footer version bumped |
| 1.13 | 2026-09-28 | Updated to framework v1.15 (63 controls): INC-64 DNS-filtering training-escape and INC-65 Codex Heapjack/Overpatch, EE-08/EE-05/TP-15 guidance extensions, footer version bumped |
| 1.14 | 2026-10-05 | Updated to framework v1.16 (63 controls): INC-66 Plugin4Shell SHA-pinning bypass, INC-67 Sentry Seer PhantomFix, INC-68 PraisonAI CVE-2026-57138, INC-69 OpenCode localhost-RCE, TP-14/MS-11/EE-07 guidance extensions, footer version bumped |
| 1.12 | 2026-09-25 | Updated to framework v1.14 (63 controls): INC-63 Medicare portal breach, EE-08/GRM-04/MIR-02 egress + sovereign-assurance guidance extensions, footer version bumped |
| 1.11 | 2026-09-21 | Updated to framework v1.13 (63 controls): MS-08 protocol-layer-identifier/credentials + fail-closed-auth and EE-08/GRM-04 harness-assurance guidance extensions (INC-60..INC-62), footer version bumped |
| 1.10 | 2026-09-19 | Updated to framework v1.12 (63 controls): added TP-15 (in-process code-execution sandbox sufficiency) to the tool/pipeline slide and evidence slide, footer version bumped |
| 1.9 | 2026-09-07 | Updated to framework v1.11 (62 controls): MS-08 MCP-gateway authentication fail-closed and EE-07 repository-supplied tool-configuration guidance extensions, footer version bumped |
| 1.8 | 2026-09-01 | Updated to framework v1.10 (62 controls): added TP-14 (skill/plugin payload integrity and instruction-channel isolation) to the evolution slide, evidence slide refreshed (52 incidents, 26 gaps, G26 added), footer version bumped |
| 1.7 | 2026-08-31 | Updated to framework v1.9 (61 controls): added TP-13 (dependency-install provenance verification) to the evolution slide, evidence slide refreshed (47 incidents, 25 gaps, G25 added), footer version bumped |
| 1.5 | 2026-08-17 | Updated to framework v1.7 (59 controls): added MS-11 and TP-12 to pillar slides, evidence slide refreshed (36 incidents, 23 gaps, G22/G23 added), footer version bumped |
| 1.6 | 2026-08-24 | Updated to framework v1.8 (60 controls): added MS-12 to the model-security slide, evidence slide refreshed (41 incidents, 24 gaps, G24 added), footer version bumped |
| 1.4 | 2026-08-12 | Client communication refresh: ABC News Australian agent incident added to threat slide, new "What This Means in Practice" engagement-path slide (posture assessment → pilot → rollout, auditor-question framing), speaker notes updated |
| 1.3 | 2026-08-12 | Updated to framework v1.6 (57 controls): added MS-10 and TP-11 to pillar slides, evidence slide refreshed (32 incidents, 21 gaps), footer version bumped |
| 1.2 | 2026-08-06 | Added future-threats watchlist summary slide (single-page table of the six watchlist components with decision gates and September promotion candidates); 24 slides; builders moved into repo with manifest + version stamping |
| 1.1 | 2026-08-06 | Humanised copy across all slides and speaker notes (plain professional voice, AI tells stripped) |
| 1.0 | 2026-08-06 | Initial 23-slide briefing for the Australian Defence Department: threat framing, seven pillars (one slide each), reference implementation, policy as code, maturity, PSPF/ISM/E8/SOCI/Five Eyes alignment, deployment, evidence base |

## Shield-AI Deck: Aware Super

| Version | Date | Change |
|---------|------|--------|
| 1.15 | 2026-11-08 | Updated to framework v1.21 (69 controls): INC-85..INC-90 (AgentScope unpatched MCP command injection, Langflow auth-bypass/MCP-enumeration RCE, seventeen-CVE framework RCE mega-cluster, MCP protocol pivoting, MCP trust-boundary measurement, WorkOS ARTEX escape), TP-16/MS-08/TP-15 guidance extensions, footer version bumped |
| 1.14 | 2026-11-07 | Updated to framework v1.20 (69 controls): INC-79..INC-84, new controls TP-16/MS-15, EE-01/MS-09/MS-13 extensions, footer version bumped |
| 1.13 | 2026-10-12 | Updated to framework v1.19 (67 controls): INC-77..INC-78 (VTCode CVE-2026-104247 learned-approval/blocklist bypass, loopback DNS-rebinding cluster), EE-07/MS-08 guidance extensions, footer version bumped |
| 1.12 | 2026-10-05 | Updated to framework v1.18 (67 controls): INC-74..INC-76 (GitLab AI Gateway CVE-2026-90970, Comment and Control CI, MCP tooling argument-injection cluster), TP-15/MS-08/EE-07 guidance extensions, footer version bumped |
| 1.11 | 2026-10-05 | Updated to framework v1.16 (63 controls): INC-66..INC-69 (Plugin4Shell, Sentry Seer PhantomFix, PraisonAI CVE-2026-57138, OpenCode localhost-RCE), TP-14/MS-11/EE-07 guidance extensions, footer version bumped |
| 1.10 | 2026-09-28 | Updated to framework v1.15 (63 controls): INC-64 DNS-filtering training-escape and INC-65 Codex Heapjack/Overpatch, EE-08/EE-05/TP-15 guidance extensions, footer version bumped |
| 1.9 | 2026-09-21 | Updated to framework v1.13 (63 controls): MS-08/EE-08/GRM-04 guidance extensions (INC-60..INC-62), footer version bumped |
| 1.8 | 2026-09-19 | Updated to framework v1.12 (63 controls): added TP-15 to the tool/pipeline slide, footer version bumped |
| 1.7 | 2026-09-07 | Updated to framework v1.11 (62 controls): MS-08 MCP-gateway authentication fail-closed and EE-07 repository-supplied tool-configuration guidance extensions, footer version bumped |
| 1.6 | 2026-09-01 | Updated to framework v1.10 (62 controls): added TP-14 to the tool/pipeline slide, evidence slide refreshed (52 incidents, 26 gaps), footer version bumped |
| 1.5 | 2026-08-31 | Updated to framework v1.9 (61 controls): added TP-13 to the tool/pipeline slide, evidence slide refreshed (47 incidents, 25 gaps), footer version bumped |
| 1.3 | 2026-08-17 | Updated to framework v1.7 (59 controls): added MS-11 and TP-12 to pillar slides, evidence slide refreshed (36 incidents, 23 gaps), footer version bumped |
| 1.4 | 2026-08-24 | Updated to framework v1.8 (60 controls): added MS-12 to the model-security slide, evidence slide refreshed (41 incidents, 24 gaps), footer version bumped |
| 1.2 | 2026-08-12 | Client communication refresh: ABC News Australian agent incident added to threat slide, new "What This Means in Practice" engagement-path slide (posture assessment → pilot → rollout, APRA-question framing), speaker notes updated |
| 1.1 | 2026-08-12 | Updated to framework v1.6 (57 controls): added MS-10 and TP-11 to pillar slides, evidence slide refreshed (32 incidents, 21 gaps), footer version bumped |
| 1.0 | 2026-08-06 | Initial 24-slide briefing for Aware Super: member-data threat framing, where AI touches a super fund, seven pillars, reference implementation, policy as code, maturity (L2 floor / L3 target), APRA alignment (CPS 234 / CPG 230 / Privacy Act / ASIC / AU Guardrails), five-step practical starting point, watchlist summary |

## Shield-AI Deck: Major Australian Retailer

| Version | Date | Change |
|---------|------|--------|
| 1.12 | 2026-11-08 | Updated to framework v1.21 (69 controls): INC-85..INC-90 (AgentScope unpatched MCP command injection, Langflow auth-bypass/MCP-enumeration RCE, seventeen-CVE framework RCE mega-cluster, MCP protocol pivoting, MCP trust-boundary measurement, WorkOS ARTEX escape), TP-16/MS-08/TP-15 guidance extensions, footer version bumped |
| 1.11 | 2026-11-07 | Updated to framework v1.20 (69 controls): INC-79..INC-84, new controls TP-16/MS-15, EE-01/MS-09/MS-13 extensions, footer version bumped |
| 1.10 | 2026-10-12 | Updated to framework v1.19 (67 controls): INC-77..INC-78 (VTCode CVE-2026-104247 learned-approval/blocklist bypass, loopback DNS-rebinding cluster), EE-07/MS-08 guidance extensions, footer version bumped |
| 1.9 | 2026-10-05 | Updated to framework v1.18 (67 controls): INC-74..INC-76 (GitLab AI Gateway CVE-2026-90970, Comment and Control CI, MCP tooling argument-injection cluster), TP-15/MS-08/EE-07 guidance extensions, footer version bumped |
| 1.7 | 2026-09-28 | Updated to framework v1.15 (63 controls): INC-64 DNS-filtering training-escape and INC-65 Codex Heapjack/Overpatch, EE-08/EE-05/TP-15 guidance extensions, footer version bumped |
| 1.8 | 2026-10-05 | Updated to framework v1.16 (63 controls): INC-66..INC-69 (Plugin4Shell, Sentry Seer PhantomFix, PraisonAI CVE-2026-57138, OpenCode localhost-RCE), TP-14/MS-11/EE-07 guidance extensions, footer version bumped |
| 1.6 | 2026-09-21 | Updated to framework v1.13 (63 controls): MS-08/EE-08/GRM-04 guidance extensions (INC-60..INC-62), footer version bumped |
| 1.5 | 2026-09-19 | Updated to framework v1.12 (63 controls): added TP-15 to the tool/pipeline slide, footer version bumped |
| 1.4 | 2026-09-07 | Updated to framework v1.11 (62 controls): MS-08 MCP-gateway authentication fail-closed and EE-07 repository-supplied tool-configuration guidance extensions, footer version bumped |
| 1.3 | 2026-09-01 | Updated to framework v1.10 (62 controls): added TP-14 to the tool/pipeline slide, evidence slide refreshed (52 incidents, 26 gaps), footer version bumped |
| 1.2 | 2026-08-31 | Updated to framework v1.9 (61 controls): added TP-13 to the tool/pipeline slide, evidence slide refreshed (47 incidents, 25 gaps), footer version bumped |
| 1.0 | 2026-08-20 | Initial 25-slide briefing for a major Australian retailer (client unnamed in deck): retail threat framing (customer PII, loyalty data, cardholder data, supply chain), seven pillars (one slide each, retail-focused), reference implementation, policy as code, maturity, alignment to Privacy Act/APPs + NDB, PCI DSS, Cyber Security Act 2024, SOCI Act, ISM/E8, AU Guardrails, five-step practical starting point, watchlist summary |
| 1.1 | 2026-08-24 | Updated to framework v1.8 (60 controls): added MS-12 to the model-security slide, evidence slide refreshed (41 incidents, 24 gaps), footer version bumped |

## Shield-AI Deck: NBN Co

| Version | Date | Change |
|---------|------|--------|
| 1.13 | 2026-11-08 | Updated to framework v1.21 (69 controls): INC-85..INC-90 (AgentScope unpatched MCP command injection, Langflow auth-bypass/MCP-enumeration RCE, seventeen-CVE framework RCE mega-cluster, MCP protocol pivoting, MCP trust-boundary measurement, WorkOS ARTEX escape), TP-16/MS-08/TP-15 guidance extensions, footer version bumped |
| 1.12 | 2026-11-07 | Updated to framework v1.20 (69 controls): INC-79..INC-84, new controls TP-16/MS-15, EE-01/MS-09/MS-13 extensions, footer version bumped |
| 1.11 | 2026-10-12 | Updated to framework v1.19 (67 controls): INC-77..INC-78 (VTCode CVE-2026-104247 learned-approval/blocklist bypass, loopback DNS-rebinding cluster), EE-07/MS-08 guidance extensions, footer version bumped |
| 1.10 | 2026-10-05 | Updated to framework v1.18 (67 controls): INC-74..INC-76 (GitLab AI Gateway CVE-2026-90970, Comment and Control CI, MCP tooling argument-injection cluster), TP-15/MS-08/EE-07 guidance extensions, footer version bumped |
| 1.8 | 2026-09-28 | Updated to framework v1.15 (63 controls): INC-64 DNS-filtering training-escape and INC-65 Codex Heapjack/Overpatch, EE-08/EE-05/TP-15 guidance extensions, footer version bumped |
| 1.9 | 2026-10-05 | Updated to framework v1.16 (63 controls): INC-66..INC-69 (Plugin4Shell, Sentry Seer PhantomFix, PraisonAI CVE-2026-57138, OpenCode localhost-RCE), TP-14/MS-11/EE-07 guidance extensions, footer version bumped |

## Shield-AI Deck: Reference Architecture Walkthrough

| Version | Date | Change |
|---------|------|--------|
| 1.12 | 2026-11-08 | Updated to framework v1.21 (69 controls): INC-85..INC-90 (AgentScope unpatched MCP command injection, Langflow auth-bypass/MCP-enumeration RCE, seventeen-CVE framework RCE mega-cluster, MCP protocol pivoting, MCP trust-boundary measurement, WorkOS ARTEX escape), TP-16/MS-08/TP-15 guidance extensions, footer version bumped |
| 1.11 | 2026-11-07 | Updated to framework v1.20 (69 controls): INC-79..INC-84, new controls TP-16/MS-15, EE-01/MS-09/MS-13 extensions, footer version bumped |
| 1.10 | 2026-10-12 | Updated to framework v1.19 (67 controls): INC-77..INC-78 (VTCode CVE-2026-104247 learned-approval/blocklist bypass, loopback DNS-rebinding cluster), EE-07/MS-08 guidance extensions, footer version bumped |
| 1.9 | 2026-10-05 | Updated to framework v1.18 (67 controls): INC-74..INC-76 (GitLab AI Gateway CVE-2026-90970, Comment and Control CI, MCP tooling argument-injection cluster), TP-15/MS-08/EE-07 guidance extensions, footer version bumped |
| 1.8 | 2026-10-05 | Updated to framework v1.16 (63 controls): control/incident-count and footer version refreshed; INC-66..INC-69 anchors and guidance extensions reflected; footer version bumped |
| 1.7 | 2026-09-28 | Updated to framework v1.15 (63 controls): INC-64 DNS-filtering training-escape and INC-65 Codex Heapjack/Overpatch, EE-08/EE-05/TP-15 guidance extensions, footer version bumped |
| 1.7 | 2026-09-21 | Updated to framework v1.13 (63 controls): MS-08/EE-08/GRM-04 guidance extensions (INC-60..INC-62), footer version bumped |
| 1.6 | 2026-09-19 | Updated to framework v1.12 (63 controls): added TP-15 to the tool/pipeline slide, footer version bumped |
| 1.5 | 2026-09-07 | Updated to framework v1.11 (62 controls): MS-08 MCP-gateway authentication fail-closed and EE-07 repository-supplied tool-configuration guidance extensions, footer version bumped |
| 1.4 | 2026-09-01 | Updated to framework v1.10 (62 controls): added TP-14 to the tool/pipeline slide, evidence slide refreshed (52 incidents, 26 gaps), footer version bumped |
| 1.3 | 2026-08-31 | Updated to framework v1.9 (61 controls): added TP-13 to the tool/pipeline slide, evidence slide refreshed (47 incidents, 25 gaps), footer version bumped |
| 1.1 | 2026-08-17 | Updated to framework v1.7 (59 controls): added MS-11 and TP-12 to pillar slides, evidence slide refreshed (36 incidents, 23 gaps), footer version bumped |
| 1.2 | 2026-08-24 | Updated to framework v1.8 (60 controls): added MS-12 to the model-security slide, evidence slide refreshed (41 incidents, 24 gaps), footer version bumped |
| 1.0 | 2026-08-13 | Initial 25-slide briefing for NBN Co: national-infrastructure threat framing (SOCI 12-hour reporting, agentic AI strategy May 2026, AI incident-report drafting Jul 2026, ASTRID lab with RMIT), seven pillars (one slide each, network-focused), reference implementation, policy as code, maturity, SOCI Act / TSSR / Privacy Act / ISM-E8 / AU Guardrails alignment, five-step practical starting point, watchlist summary |

## Diagram Set

The SVG diagrams used by both decks live in assets/diagrams/ and are shared
with the framework documents. Deck-specific alignment diagrams:

- client-specific/defence/defence-alignment.svg (Defence deck slide 19)
- client-specific/aware-super/aware-super-alignment.svg (Aware Super deck slide 20)
- client-specific/nbn/nbn-alignment.svg (NBN Co deck slide 20)
