# SHIELD-AI to NIST SP 800-53 Rev 5: crosswalk fit report

Generated 2026-11-19 by `tools/generate_oscal_crosswalk.py` from `crosswalk/shield-ai-to-800-53r5.json`. Target catalog: SP 800-53 Rev 5.2.0. **Status: DRAFT, not SME-reviewed.**

Scope: MS, IAM, DS, TP, MIR, GRM and EE pillars, 69 of 69 controls.

## Headline

| Fit | Controls | Meaning |
|---|---|---|
| direct | 23 | An org meeting the mapped 800-53 controls, with agents in scope as subjects and sensible ODPs, substantially meets the SHIELD control. No residual requirement. |
| partial | 39 | The core of the control maps to 800-53, but SHIELD adds requirements 800-53 does not state. Residual is recorded. |
| novel | 7 | Only tangential 800-53 analogues exist. The control's main idea is new relative to 800-53. |

Every one of the 69 controls has at least one 800-53 neighbour (69 of 69), so none is wholly orphaned. That is a weak result by itself: 800-53 is broad enough that something always loosely applies. The fit column is the meaningful one.

## Mapping-level statistics

- 329 map entries. Relationships: intersects-with 325, no-relationship 1, subset-of 3.
- Confidence: high 47, medium 153, low 129.
- 325 of 329 entries are `intersects-with` (each side has content the other lacks); 3 are `subset-of`; 0 are `equal-to`/`equivalent-to`.

- 37 of 69 controls have at least one high-confidence mapping. 32 rest on medium or low confidence alone.

## By pillar

| Pillar | Direct | Partial | Novel |
|---|---|---|---|
| MS | 3 | 9 | 3 |
| IAM | 2 | 6 | 2 |
| DS | 2 | 6 | 0 |
| TP | 5 | 10 | 1 |
| MIR | 5 | 1 | 0 |
| GRM | 3 | 2 | 1 |
| EE | 3 | 5 | 0 |

## Per-control result

| SHIELD-AI | Title | Fit | 800-53 targets (conf.) |
|---|---|---|---|
| EE-01 | Execution Environment Boundary Enforcement | **partial** | SC-39 (H), SC-7.21 (M), SC-24 (M), CM-2 (L) |
| EE-02 | Infrastructure API Access Control | **direct** | AC-3 (H), AC-6 (M), SC-7.5 (L) |
| EE-03 | Resource Usage Limiting | **direct** | SC-6 (H), SC-5 (M), SI-4 (L) |
| EE-04 | Evaluation Sandbox Integrity | **partial** | CM-4.1 (H), SA-3.1 (M) |
| EE-05 | Host-Trusted Configuration File Injection Prevention | **partial** | CM-5 (M), SI-7 (M), CM-7.5 (L) |
| EE-06 | Fail-Closed Sandbox Operation | **direct** | SC-24 (H), SI-6 (M), SI-17 (M) |
| EE-07 | Agent Control-Plane Configuration Integrity | **partial** | CM-5 (H), AC-6.1 (M), CM-3 (M), CM-6 (M) |
| EE-08 | Evaluation-Harness Isolation and Integrity | **partial** | CM-4.1 (M), SA-3.1 (L), SI-6 (L) |
| IAM-01 | Agent Identity Management | **direct** | IA-4 (M), IA-13 (M), IA-9 (M), AU-3 (M), IA-2 (L) |
| IAM-02 | Scope-Bound Delegation | **partial** | AC-6 (H), AC-3 (M), AC-3.13 (L) |
| IAM-03 | Human Oversight Controls | **partial** | AC-4.9 (M), AC-5 (M), IA-5.6 (M), AC-3.2 (L) |
| IAM-04 | Credential Isolation | **partial** | IA-5 (H), IA-5.6 (M) |
| IAM-05 | Just-in-Time (JIT) Access | **direct** | AC-2.2 (H), IA-5 (M), IA-5.13 (L) |
| IAM-06 | Cross-Session Boundary Enforcement | **partial** | SC-4 (M), AC-4.21 (M), AC-3 (L) |
| IAM-07 | Transitive Delegation Chain Enforcement | **novel** | SA-8.22 (M), AU-3 (M), AU-10 (L), AC-6 (L) |
| IAM-08 | Credential Scope Narrowing | **partial** | AC-6 (H), IA-5 (M), AC-3.8 (M) |
| IAM-09 | Multi-Tenant Agent Platform Isolation | **partial** | AC-3 (H), SC-39 (M), AC-4.21 (M), SC-4 (L) |
| IAM-10 | Taint-Tracked Least-Privilege Subagent Scoping | **novel** | AC-6 (M), AC-16 (M), AC-16.1 (M), AC-4 (L), AC-4.3 (L), AC-3.13 (L) |
| TP-01 | Tool Inventory and Registry | **direct** | CM-8 (H), CM-7.5 (M), CM-8.3 (M), CM-3 (L) |
| TP-02 | Tool Access Control | **direct** | AC-3 (H), AC-6 (M), IA-9 (M), AC-3.13 (L) |
| TP-03 | API Gateway Security | **direct** | SI-10 (H), SC-7 (M), SC-7.17 (M), SC-5 (M), AU-12 (M) |
| TP-04 | Tool Output Validation | **partial** | SI-15 (M), SI-10 (M), SI-10.6 (L), SI-10.5 (L) |
| TP-05 | Pipeline Integrity | **direct** | SA-10 (M), SI-7.15 (H), CM-14 (M), SA-10.1 (M), SR-4.3 (L), SA-11 (L) |
| TP-06 | Dependency Scanning | **partial** | RA-5 (H), SI-2 (M), SA-15.7 (L), SR-3 (L), SI-3 (L) |
| TP-07 | Cross-Tool Dependency Analysis | **partial** | RA-3 (L), SA-11.2 (L), CM-4 (L), AC-5 (L) |
| TP-08 | API Gateway Infrastructure-Isolation Mode | **direct** | SC-7.5 (M), SC-7 (M), SI-4.5 (M), AU-12 (L) |
| TP-09 | Explicit Tool Registration | **partial** | CM-7 (M), CM-7.5 (M), SA-8.23 (M), CM-8 (L) |
| TP-10 | Agent Platform Inbound Control-Plane Protection | **partial** | CM-7 (M), SC-7.11 (M), SC-7.5 (M), SC-23 (M), SI-4 (L), IA-5.6 (L) |
| TP-11 | Agent Browser and Content-Rendering Isolation | **novel** | SI-10.5 (L), SC-18 (L), SC-44 (L), SC-39 (L) |
| TP-12 | Tool-Call Provenance and Dispatch Verification | **partial** | SC-23 (M), AC-25 (M), AU-10 (L), AC-3 (L), SI-7 (L) |
| TP-13 | Agent Dependency-Install Provenance Verification | **partial** | CM-11 (M), SR-4 (M), CM-7.5 (M), SR-4.3 (L), CM-14 (L) |
| TP-14 | Skill/Plugin Payload Integrity and Instruction-Channel Isolation | **partial** | CM-14 (H), SI-7.15 (H), SR-4 (M), AC-6 (M), SC-18.3 (L), SR-11 (L) |
| TP-15 | In-Process Code-Execution Sandbox Sufficiency | **partial** | SC-39 (H), CM-7.6 (M), SC-44 (L), SC-7.21 (L) |
| TP-16 | Tool-Connection and Launch-Path Integrity | **partial** | SI-10.6 (H), SI-10 (M), SI-10.5 (M), CM-7.5 (M), CM-7.2 (L), CA-3 (L) |
| MS-01 | Model Weight Protection | **direct** | SC-28.1 (H), SC-12 (H), SC-8.1 (M), SC-13 (M), SI-7 (L) |
| MS-02 | Training Data Integrity | **partial** | SR-4 (M), SI-7 (M), AC-3 (M), SI-10 (L) |
| MS-03 | Supply Chain Security | **direct** | SR-3 (H), SR-4 (H), SR-4.3 (M), SR-6 (M), SI-7.15 (M), CM-14 (L), PM-30 (L) |
| MS-04 | Adversarial Robustness | **partial** | CA-8 (M), SI-10 (L), SI-10.6 (L), SI-10.5 (L), AC-4.8 (L), CA-8.2 (M), SA-11.5 (M), SI-15 (L) |
| MS-05 | Model Behaviour Validation | **partial** | SI-15 (M), AC-4.8 (M), AC-4 (L), SI-4 (L) |
| MS-06 | Model Inventory and Lineage Tracking | **direct** | CM-8 (H), CM-8.1 (M), SR-4 (M), CM-2 (M), PM-5 (L), SA-10 (L) |
| MS-07 | Deployment Context Obfuscation | **novel** | CM-4.1 (L), SA-3.1 (L) |
| MS-08 | MCP Security Controls | **partial** | IA-9 (M), SI-7.15 (M), SI-10 (M), IA-5 (M), SC-24 (M), CM-14 (L), SI-4.5 (L), SR-4 (L) |
| MS-09 | Perception-Fidelity Enforcement for Human-in-the-Loop Approvals | **novel** | AC-4.8 (L), AU-10 (L), AC-4.9 (L) |
| MS-10 | Agent Memory-Store Integrity | **partial** | AC-3 (M), SI-7.6 (M), AU-12 (L), AU-9.1 (L), SI-4 (L), IR-4 (L) |
| MS-11 | Operational Data-Stream Integrity | **partial** | SI-10.5 (M), AU-10.1 (M), IA-9 (M), AC-4.17 (L), SI-4 (L) |
| MS-12 | MCP Discovery-Metadata and Shared-Cache Integrity | **partial** | SI-7 (M), AC-3 (M), CM-2 (L), SC-4 (L), SI-7.6 (L), SI-10.5 (L) |
| MS-13 | Transcript and Conversation Authenticity | **partial** | AU-9.3 (M), AU-10 (M), SC-23 (M), AU-9.1 (L), SI-7.6 (L) |
| MS-14 | Self-Replication Barrier | **novel** | SI-3 (L), SC-7.9 (L), SI-15 (L), AC-4.8 (L) |
| MS-15 | Cross-Tenant Agent Memory and State Isolation | **partial** | AC-3 (H), AC-4.21 (M), SC-4 (M), SA-8.2 (L), SA-8.6 (L) |
| DS-01 | Data Classification and Labelling | **direct** | AC-16 (H), AC-16.1 (H), RA-2 (M), AC-4 (L) |
| DS-02 | Inference Data Protection | **direct** | SC-8 (H), SC-8.1 (H), SC-13 (M), SC-12 (L), SC-23 (L) |
| DS-03 | Memory Sanitisation | **partial** | SC-28.1 (H), SI-12 (M), SI-12.3 (M), SC-4 (M), MP-6 (L) |
| DS-04 | Data Minimisation | **partial** | SI-12.1 (M), PT-2 (L), AC-6 (L), SA-8.14 (L), PM-25 (L) |
| DS-05 | Training Data Governance | **partial** | PT-4 (M), PT-3 (M), SI-12 (M), SI-12.2 (M), SR-4 (L), PM-23 (L) |
| DS-06 | Output Validation | **partial** | SI-15 (M), AC-4.8 (M), AU-13 (L), SC-7.10 (L) |
| DS-07 | Agent-Originated Artifact Publication Control | **partial** | AC-5 (M), SA-10 (M), SI-7.15 (M), CM-5 (M), AC-3.2 (L), CM-14 (L), SI-3 (L) |
| DS-08 | Destination and Emergent-Channel Egress Inventory | **partial** | SC-7.5 (H), SC-7.10 (H), SC-31 (M), SI-4.18 (M), AC-4 (M), SC-7.9 (L), SC-7.8 (L) |
| MIR-01 | Agent Activity Logging | **direct** | AU-2 (H), AU-3 (H), AU-12 (H), AU-3.1 (M), AU-12.1 (M), AU-14 (L) |
| MIR-02 | Behavioural Anomaly Detection | **direct** | SI-4.13 (H), SI-4 (M), IR-4.13 (M), SI-4.11 (L), AU-6 (L) |
| MIR-03 | Prompt Audit Log | **direct** | AU-14 (M), AU-3.3 (H), AU-3 (M), AU-3.1 (M), AU-9 (L), AU-11 (L) |
| MIR-04 | Incident Response Playbooks | **partial** | IR-4 (H), IR-8 (H), IR-3 (M), IR-4.1 (M), IR-4.5 (L), IR-2 (L) |
| MIR-05 | Mandatory Reporting Integration | **direct** | IR-6 (H), IR-6.1 (H), IR-8.1 (M), IR-8 (L), SR-8 (L) |
| MIR-06 | Forensic Readiness | **direct** | AU-9 (H), AU-9.1 (M), AU-9.2 (M), AU-9.3 (M), AU-11 (M), AU-7 (M), AU-14 (L) |
| GRM-01 | AI Governance Body | **direct** | PM-29 (M), CA-6 (M), PM-10 (M), PM-9 (L), PM-23 (L) |
| GRM-02 | AI Risk Register | **partial** | RA-3 (H), RA-7 (M), CA-5 (M), PM-9 (M), IR-4.5 (M), CM-8.3 (M), PM-28 (L) |
| GRM-03 | Ethical Use Policy | **novel** | PL-4 (L), AC-6 (L), PT-5 (L) |
| GRM-04 | Third-Party AI Risk Management | **direct** | SA-9 (H), SR-6 (M), SR-3 (M), SR-5 (M), SA-4 (M), SR-8 (M), IR-6.3 (L), RA-3.1 (L) |
| GRM-05 | Regulatory Mapping and Compliance Reporting | **direct** | CA-7 (H), PM-31 (M), CA-2 (M), PM-6 (L), PL-10 (L), PL-11 (L) |
| GRM-06 | Board and Executive Reporting | **partial** | PM-6 (M), CA-5 (M), RA-7 (L), PM-29 (L), CA-7 (L) |

Confidence: H high, M medium, L low.

## Residuals: what 800-53 does not cover

For every control not rated `direct`, this is the requirement an 800-53-only organisation would still be missing.

- **EE-01 (partial)**: No shared host mounts/IPC/network namespaces and immutable infrastructure are prescriptive technical requirements. 800-53 leaves them to ODPs; no 800-53 control names immutable infrastructure (closest: CM-2, CM-6, SI-7).
- **EE-04 (partial)**: Requirement that models must not be able to distinguish evaluation from production (links to MS-07) has no 800-53 analogue.
- **EE-05 (partial)**: Agent-writable paths the host later loads as trusted configuration (shell profiles, IDE config, cron, systemd units). 800-53 has no control for this write-then-execute-as-trusted path.
- **EE-07 (partial)**: Self-configuration poisoning by the agent, MCP registry entries as auto-run launch commands, and repository-supplied VCS config executing before the workspace-trust boundary are agent-era attack classes 800-53 does not name.
- **EE-08 (partial)**: Active egress test before and during runs, collision-checking evaluation targets against real domains, and cryptographic separation of runs to prevent cross-run contamination are not in 800-53.
- **IAM-02 (partial)**: Constraint that an agent cannot grant other agents permissions beyond its own scope. 800-53 has no delegation-of-privilege concept.
- **IAM-03 (partial)**: Human approval before high-risk autonomous agent actions is the central concept and has no direct 800-53 control. AC-4.9 is scoped to information flows; AC-3.2 is dual authorization between people.
- **IAM-04 (partial)**: Separate storage, management and rotation of agent versus human credentials, so that compromise of one does not compromise the other.
- **IAM-06 (partial)**: Per-session independent security context for agent memory and context, including between sessions of the same user. Agent context is not named as a shared resource.
- **IAM-07 (novel)**: Maximum delegation depth (two hops) and blocking downstream proxying of the agent's identity at the infrastructure layer. Reconstructing the chain with originating identity is now mapped to SA-8.22 and AU-3. 800-53 has no concept of transitive delegation (cf. OAuth token exchange / on-behalf-of).
- **IAM-08 (partial)**: Short-lived per-tool tokens and revocation that cascades through the delegation chain.
- **IAM-09 (partial)**: Server-side tenant-ID scoping on every execution, tool call and query, with no user-controlled object IDs able to bypass it (CWE-639). 800-53 has no explicit multi-tenancy control.
- **IAM-10 (novel)**: Taint-marking untrusted records at ingestion and dynamically narrowing the subagent's grants while it processes tainted data. AC-16, AC-4 and AC-6 supply labelling, flow and least-privilege vocabulary only.
- **TP-04 (partial)**: Sanitising tool output against instruction content that the model will follow (tool-output prompt injection). 800-53's injection controls rely on parameterized interfaces or escaping; natural-language instructions inside a context window cannot be escaped that way.
- **TP-06 (partial)**: Treating models and model registries as dependencies to be scanned (e.g. serialized model files that execute code on load), and an automated block on critical findings. RA-5 requires scanning and timely remediation, not a blocking gate.
- **TP-07 (partial)**: Combinatorial analysis of registered tools for escape, privilege-escalation and exfiltration chains, and explicit risk acceptance of escape-class chains. 800-53 has no concept of analysing capability composition across components.
- **TP-09 (partial)**: Prohibiting attribute-based, reflection-based or discovery-based registration of internal functions and SDK helpers as agent-callable tools; every callable must be explicitly declared.
- **TP-10 (partial)**: Origin-bound gateway tokens that cannot be read from browser context (cross-site WebSocket hijack resistance), and detecting and blocking service binding initiated by the agent itself. 800-53 assumes administrators, not the agent, open listeners.
- **TP-11 (novel)**: Classifying rendered content as untrusted, stripping imperceptible instruction vectors before agent action, preserving origin and content isolation for an agent acting across sites, and keeping credential material out of the browser/session layer. No 800-53 control is built on content-as-command.
- **TP-12 (partial)**: Verifying that a tool call originated from an authorised model turn (session, turn, model signature) before dispatch; binding approval records to the exact tool name and arguments; verifying approvals against the human channel, never against agent-writable session history. 800-53 does not treat a model as an authorised source of instructions.
- **TP-13 (partial)**: Refusing to treat ingested documentation (README, llms.txt) as an authoritative install script; registry-existence, namespace-ownership and domain-expiry checks before install; treating dangling references as findings.
- **TP-14 (partial)**: Fixing instruction content at install time and prohibiting runtime-fetchable instruction channels; capability-scoped skill privileges below the agent's own identity; behavioural baseline with quarantine on drift. 800-53's code-signing vocabulary assumes the signed artifact is code, not instructions.
- **TP-15 (partial)**: The explicit determination that denylist or blocklist in-process sandboxes are code-execution surfaces, not security boundaries; classifying any unavoidable in-process sandbox as high-risk with automated blocking; a mandatory alternative-evaluation gate at higher maturity.
- **TP-16 (partial)**: Origin-binding of OAuth authorization endpoints to the configured server; validating and allowlisting launch commands registered through tool or server definitions, including those a prompt-injected model can influence; assuming later compromise of a previously benign server.
- **MS-02 (partial)**: Statistical and semantic detection of poisoned samples (anomaly detection, drift monitoring) and retraining triggered by integrity findings. 800-53 integrity controls detect unauthorised modification, not authorised-but-malicious data.
- **MS-04 (partial)**: Model-level resistance to prompt injection cannot be specified or verified by any 800-53 control (SP 2400-102 itself says current mitigations do not offer full protection), and sanitising imperceptible content (zero-opacity, sub-pixel, DOM-hidden text) before reasoning has no 800-53 home. 800-53 can require that adversarial testing is done, not that it succeeds.
- **MS-05 (partial)**: Semantic output bounds (safety, scope, domain-appropriate advice) and bounds adjusted dynamically from production telemetry. SI-15 presumes the expected content can be specified.
- **MS-07 (novel)**: Indistinguishability of API endpoints, data formats, latency, error handling and credential lifetimes between evaluation and production, with divergence checks treated as an incident signal. 800-53 has no concept of a system under test that detects the test.
- **MS-08 (partial)**: Treating MCP tool definitions and discovery metadata as security-relevant content to be signed and validated against a known-good schema; monitoring model-originated writes to execution-bearing locations and publication channels; a protocol-level rule against downgrading to anonymous sessions and against default gateway credentials.
- **MS-09 (novel)**: Stripping or flagging imperceptible content (zero-opacity, sub-pixel, off-screen, DOM-hidden) before reasoning, and binding each approval to a rendering-fidelity snapshot of the exact content acted on.
- **MS-10 (partial)**: Treating persistent agent memory (vector stores, learned patterns, histories) as a behaviour-steering store; retrieval-layer filtering of flagged entries; a post-incident audit-and-clean procedure for the store itself; red-team testing of poisoning persistence.
- **MS-11 (partial)**: Treating log, alert and observability content as untrusted instruction-bearing input; independent non-log verification before a log-triggered action; flagging agent actions whose proximate cause was a log entry.
- **MS-12 (partial)**: Length-limiting and screening MCP instructions and tool descriptions for instruction content; isolating them from the trusted system prompt; verifying, not trusting, server-declared cache scope claims.
- **MS-13 (partial)**: Signing model outputs with a per-session key held outside the harness; verifying every stored response on read before the agent reasons over it; refusing confidence-gated action from an unverified transcript.
- **MS-14 (novel)**: Fingerprinting instruction-bearing input and matching it against outbound content before publish; quarantine and human sign-off on suspected echoes; blast-radius caps per propagation hop; worm-emulation drills.
- **MS-15 (partial)**: Hard post-retrieval ownership gating (similarity is not admissibility); treating any cross-tenant hit as an alarm; a tenant or namespace key that is never a model-controllable tool argument; fail-closed refusal when ownership cannot be verified.
- **DS-03 (partial)**: Detecting cross-session aggregation of sensitive data in agent memory, and per-agent memory scoping as a design requirement. MP-6 media sanitisation concerns media at disposal, not purging stored context.
- **DS-04 (partial)**: Minimising non-PII sensitive data exposed to the model's context, and per-task retrieval scoping. AC-6 least privilege applies to accounts and processes, not to the volume of data placed in a context window.
- **DS-05 (partial)**: Lineage from source through preprocessing to training for all training data, not only PII; verifying consent for personal data used to train a model; machine unlearning (removing a record's influence from a trained model); continuous training-data audit. 800-53 disposal controls act on stored information, not on a model derived from it.
- **DS-06 (partial)**: Detecting memorised training data and system-prompt fragments in model output, and memorisation testing in CI/CD. SI-15 validates output against 'expected content', which presumes the expected content can be specified.
- **DS-07 (partial)**: Publication as an egress event requiring approval the agent can neither trigger nor satisfy, and publication credentials unreachable through the ordinary tool path. 800-53 separation of duties is written for people.
- **DS-08 (partial)**: Enumerating client-side and third-party fetch channels (image rendering, link unfurl, webhook preview) as egress sinks; payload-blind hard allow-lists rather than content classifiers; DNS egress restricted to allow-listed resolvers with queried names inspected. SC-31 covers the analysis in principle, as a design-time covert channel analysis.
- **MIR-04 (partial)**: AI-specific scenarios (prompt-injection containment, model rollback, tool revocation, code-generation attack containment) as required playbook content. 800-53 requires the capability, not scenario coverage.
- **GRM-02 (partial)**: A dedicated AI threat taxonomy (model, tool, data, identity, pipeline), automated tripwires, and a single exercised kill-switch capability tested at least annually. IR-4.5 is a configurable automatic disable on detection, not an organisation-wide kill switch that is exercised.
- **GRM-03 (novel)**: A policy of acceptable agent conduct, risk-tiered autonomy levels, and agent transparency obligations, with technical enforcement at the tool gateway (L4).
- **GRM-06 (partial)**: Per-pillar maturity scoring for non-technical audiences. 800-53 baselines are met or not met per control and define no maturity ladder.

## Findings

1. **Fit (computed).** Direct 23: EE-02, EE-03, EE-06, IAM-01, IAM-05, TP-01, TP-02, TP-03, TP-05, TP-08, MS-01, MS-03, MS-06, DS-01, DS-02, MIR-01, MIR-02, MIR-03, MIR-05, MIR-06, GRM-01, GRM-04, GRM-05. Partial 39. Novel 7: IAM-07, IAM-10, TP-11, MS-07, MS-09, MS-14, GRM-03.
2. **Equality (computed).** 0 of 329 map entries are `equal-to`/`equivalent-to`; 3 are `subset-of`. A compliance team cannot treat 'satisfies 800-53 control X' as 'satisfies SHIELD-AI control Y' for the partial and novel controls.
3. **Direct without a high-confidence target (computed): IAM-01, TP-08, GRM-01.** These rest on medium or low confidence mappings only; review them first, as 'direct' may be generous.
4. **Human approval of autonomous action (IAM-03) is the notable IAM gap.** It is central to agent safety yet the nearest 800-53 controls are AC-4.9 (information flows) and AC-3.2 (dual authorization), neither scoped to actions. The NIST cross-check below found no NIST control for it either, and NIST publicly cautions about relying on it.
5. **Keyword matching would mislead.** IAM-10 'taint-tracking' collides with SI-20 'Tainting', a different concept (exfiltration detection). It is recorded as `no-relationship` with a blocking qualifier. Tooling that auto-maps on titles or text similarity would get this wrong.
6. **One identity tension (IAM-01 vs IA-2).** IA-2 ties a process to the user it acts for; IAM-01 requires a distinct agent identity. Compatible, but an implementation that reads IA-2 literally could satisfy it while failing IAM-01. Recorded as a qualifier. TP-02 inherits the same dependency (the tool must authenticate the agent, not the human).
7. **TP: mechanism maps, trigger does not.** The later TP controls (TP-10 to TP-16) come from incidents where an agent or its tooling is induced to execute attacker-controlled instructions or code. The mechanism half (signing, input validation, allow-listing, process isolation, provenance) has 800-53 homes. The trigger half (content the agent reads becomes a command; the model is an instruction source whose output must be authenticated) does not.
8. **TP-11 is the clearest novel control in the pillar.** Treating rendered content as a command channel and preserving origin isolation for an acting agent has no 800-53 vocabulary. A keyword search of Rev 5.2 statements and guidance for 'same-origin' returned no hits and for 'browser' one incidental hit. The targets listed are tangential.
9. **One 800-53 control, two different fits (SI-10.6).** Its mechanism (parameterized interfaces, output escaping) presumes a data/code boundary. TP-16 has one (an OS launch path), so SI-10.6 fits well. TP-04 does not: an LLM context has no such boundary, so the same control gives weak cover. Recorded as a qualifier on TP-04.
10. **TP-15: 800-53 permits the weak reading.** SC-39 (separate execution domain per process) arguably excludes an in-process denylist sandbox, but never says so; an assessor could accept a hardened interpreter as an 'execution domain'. SHIELD-AI's value here is the explicit negative.
11. **Supply-chain controls transfer best.** TP-05, TP-13 and TP-14 map onto the SR family, CM-14 and SI-7.15, where 800-53's provenance and authenticity vocabulary predates agent skill marketplaces but still applies. The residual is that the payload is natural-language instructions and runtime-fetchable instruction channels, not just code.
12. **TP-07 is a borderline partial/novel.** RA-3 and SA-11.2 would cover analysis of tool composition only if the organisation chose to scope threat modelling that way; nothing in 800-53 asks for it.
13. **Coverage tracks how generic the control is.** The governance, monitoring and incident-response controls map best because 800-53's PM, CA, AU and IR families are technology-neutral and apply to AI systems unchanged. The novel controls cluster where the model itself is the attack surface (MS-07, MS-09, MS-14), with IAM-07, IAM-10, TP-11 and GRM-03 as the others. MS-04 was first rated novel and was reclassified to partial by the NIST cross-check.
14. **800-53 Rev 5.2 has no vocabulary for AI as a thing to be secured.** A keyword search of non-withdrawn statements and guidance finds no hits for 'training data', 'poison', 'tenant', 'ethic', 'autonom', 'human oversight' or 'playbook'. 'Artificial intelligence' appears only in RA-3.4 and SI-3, as a detection technique. A missing word is evidence of a vocabulary gap, not proof of no coverage.
15. **Integrity controls do not detect authorised poison.** MS-02 (training data), MS-10 (agent memory) and MS-13 (transcripts) all involve data that is written through a legitimate path. SI-7 and SR-4 detect unauthorised change and provenance breaks; a malicious but authorised write is neither. An organisation could report SI-7 as met while the threat is untouched. Recorded as a qualifier on MS-02.
16. **Human approval of agent action is a recurring gap, not a single one.** IAM-03 (approval before high-risk action), TP-12 (approval bound to the exact call), MS-09 (fidelity of what the approver sees) and DS-07 (approval the agent cannot trigger) all rest on a human-in-the-loop concept that 800-53 lacks. The nearest controls (AC-4.9, AC-3.2, AC-5) are written for information flows and for people.
17. **MS-07 pushes the opposite way from 800-53's test-environment controls.** CM-4.1 and SA-3.1 require test environments to be separate and protected; nothing asks that they be undetectable. An organisation can satisfy CM-4.1 with an obviously labelled test environment that a model can recognise. Recorded as a qualifier.
18. **DS-08: the egress that matters may leave from the client.** SC-7.5 and SC-7.10 govern the network boundary, but a rendered image tag or link unfurl is fetched by the user's client or a third-party service. SC-31 covert channel analysis is the best fit, but it is a design-time analysis, so it does not by itself keep an emergent-channel inventory current.
19. **MIR-03 creates a privacy obligation.** AU-14 requires consultation with legal counsel and AU-3.3 ties retained PII to a privacy risk assessment. A full prompt/response log is a new sensitive data store, so the control cannot be considered met without that assessment. Recorded as a qualifier.
20. **Governance controls rate direct only if AI is in scope.** GRM-01, GRM-04 and GRM-05 map to organisation-level controls (PM-29, SA-9, CA-7). An existing programme meets them only if it already covers AI systems and AI vendors; 800-53 does not require that.
21. **The privacy mappings are PII-scoped.** DS-04 and DS-05 rely on 800-53's privacy controls (PT, SI-12, PM-25), which concern personal data. DS-04 extends to all sensitive data in a context window, and DS-05 to training data in general. Alignment with the Privacy Act 1988 and the Australian Privacy Principles is not assessed here.
22. **'Novel' means novel to 800-53 as written, not to NIST's thinking.** In the NIST material searched, most novel controls' threats or principles appear as attack descriptions, research defences or stakeholder positions, but none appears as a control requirement. NIST's stated method for closing such gaps is the overlay: tailoring existing controls with organisation-defined parameters and discussion text (for example its SI-03(08) tailoring for predictive AI). Some partial and novel ratings may therefore become direct once an agent overlay (NISTIR 8605D) exists. None was published when this cross-check was done.
23. **NIST is publicly cautious about human-in-the-loop, which sharpens the IAM-03 gap rather than closing it.** SP 2400-102 says human-in-the-loop oversight is 'difficult to apply at the speed and scale at which agentic systems operate' and calls balancing escalation 'an open research problem'. A NIST blog likens approval overload to MFA fatigue, and NCCoE commenters recommend reserving human approval for high-impact actions. IAM-03 requires approval for high-risk actions and uses risk-based tiers at L3, which is that posture. The SHIELD-AI control schema does not discuss approval fatigue (searched all 69 controls for fatigue, habituation, rubber-stamping and approval volume, rate or quality). Approval quality, not only approval presence, is worth adding to IAM-03 and MS-09.
24. **Absence-of-term evidence is weak.** The 'not found' results are term searches over four NIST documents, run on text extracted from PDFs and web pages. A concept can be present under different wording, and a draft taxonomy is not NIST's complete position. Treat 'not found' as a prompt to look, not as proof.

## NIST cross-check

Each control rated novel (plus any later reclassified) was checked against NIST material published or reachable at the time of writing. This is a check on the 'novel' ratings, not an endorsement of them. NIST has not published an agent overlay (NISTIR 8605D), so none of this is a NIST control mapping.

| Control | Fit now | Verdict | Summary |
|---|---|---|---|
| IAM-07 | novel | converging | NIST sources want attenuation and cryptographic traceability along delegation chains; none states a depth limit. |
| IAM-10 | novel | converging | NIST describes taint tracking as a research defence and NCCoE commenters want authorization to tighten on untrusted data; no control. |
| TP-11 | novel | threat-recognised | SP 2400-102 documents instructions injected visually into browser and computer-use agents; no NIST control addresses origin or content isolation. |
| MS-04 | partial | reclassified | Rated novel before the cross-check; on re-reading, most of the control is testing activity that 800-53 already covers, so downgraded to partial. NIST's predictive-AI overlay outline corroborates weakly. |
| MS-07 | novel | confirmed-novel | Not addressed. SP 2400-102 records models escaping test environments but excludes it from scope; NIST's overlay outline selects separation, not indistinguishability. |
| MS-09 | novel | threat-recognised | NIST documents visual injection and warns about approval fatigue; nothing addresses whether the approver sees what the agent acted on. |
| MS-14 | novel | threat-recognised | SP 2400-102 documents self-propagating injections and lists inter-agent firewalls; its mitigations do not include outbound-content screening. |
| GRM-03 | novel | converging | NIST drafts ask who is accountable for autonomous systems and when to disable autonomy; none describes risk-tiered autonomy. |

Verdicts: `reclassified` = rating changed; `confirmed-novel` = NIST material contradicts nothing and addresses nothing; `converging` = NIST material states the principle or a related goal but no control; `threat-recognised` = NIST documents the attack but no control or mitigation maps to the SHIELD-AI requirement.

### Sources and their weight

| Key | Source | Status | Weight |
|---|---|---|---|
| `sp800-53r5` | [NIST SP 800-53 Rev 5.2.0 (OSCAL catalog)](https://github.com/usnistgov/oscal-content/tree/main/nist.gov/SP800-53/rev5) | final | the catalog being mapped to |
| `sp2400` | [NIST SP 2400-102e2026 ipd, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://csrc.nist.gov/pubs/sp/2400-102/e2026/ipd) | initial public draft, 2026-11-09, comments to 2026-12-18 | NIST draft taxonomy of attacks and mitigations; not a control catalog |
| `nccoe` | [NCCoE, Summary of Comments on the Concept Paper (Software and Agentic SI Identity and Authorization)](https://pages.nist.gov/nccoe-ai-identity/summary-of-comments.html) | published 2026-09-29; the document states it was edited with Gemini | summarises commenters' positions; not NIST requirements |
| `ir8596` | [NIST IR 8596 iprd, Cybersecurity Framework Profile for AI (Cyber AI Profile)](https://csrc.nist.gov/pubs/ir/8596/iprd) | initial preliminary draft, 2025-12-16; no later draft found | CSF-level preliminary draft |
| `ir8621` | [NIST IR 8621, NIST Workshop on SI Incident Management](https://csrc.nist.gov/pubs/ir/8621/final) | final, 2026-11-02 | workshop report; stakeholder views, not NIST requirements |
| `cosais_outline` | [COSAiS annotated outline: Using and Fine-Tuning Predictive AI (NISTIR 8605A)](https://csrc.nist.gov/csrc/media/Projects/cosais/documents/COSAiS-Predictive-AI-annotated-outline-Jan2026.pdf) | discussion draft, 2026-01-08; its control list is stated to be incomplete | closest published overlay material; predictive AI only, no agent overlay (NISTIR 8605D) published |
| `nist_blog` | [NIST blog: Back to the Future: Why Agentic AI Needs a Strong Identity Foundation](https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation) | 2026-08-27 | blog post by NIST authors; not guidance |

### Per-control evidence

**IAM-07** (converging): Rating unchanged: novel relative to 800-53 as written. NIST's attenuation and traceability goals are already in IAM-02, IAM-07 (traceability) and IAM-08.

- `nccoe`, Task Scoped & Contextual Authorization (commenter position): "each agent in a delegation chain has fewer permissions than its predecessor"
- `nccoe`, Delegation and Accountability (commenter position): "remain cryptographically traceable to the entity originating the agentic instruction"
- `sp800-53r5`, SA-8.22 guidance: "trace security-relevant actions (i.e., subject-object interactions) to the entity on whose behalf the action is being taken"
- Not found: No maximum delegation depth or hop limit in SP 2400-102, IR 8596, the NCCoE summary or IR 8621 (terms searched: maximum depth, hop limit, max hops, delegation depth, depth limit: 0 hits). 'Hops' appears once, describing the problem.

**IAM-10** (converging): Rating unchanged. The cost caveat (utility loss) is worth carrying into IAM-10's L3/L4 guidance.

- `sp2400`, §4.4: "FIDES [121] applies dynamic taint tracking with confidentiality and integrity labels to regulate data flows"
- `sp2400`, §4.4: "restrict the generality of the agent, and in most cases induce utility loss"
- `nccoe`, Direct and Indirect Prompt Injection (commenter position): "might even need to change whenever an agent operates on untrusted data"
- Not found: No NIST control or guideline requires privilege to narrow with taint. SP 2400-102 presents information-flow control as an approach that 'future work should investigate'.

**TP-11** (threat-recognised): Rating unchanged.

- `sp2400`, §4.4: "adversaries can inject instructions visually"
- `sp2400`, §4.4: "agents clicked on adversarial pop-ups in 86% of cases on average"
- Not found: 'same-origin', 'origin isolation', 'cross-origin' and 'content isolation' return 0 hits across SP 2400-102, IR 8596, the NCCoE summary and IR 8621.

**MS-04** (reclassified): This downgrade rests mainly on the control's own maturity indicators, not on NIST. The earlier novel rating weighted the 'model resists injection' narrative over those testing requirements. NIST's overlay outline is for predictive AI; its SI-03(08) tailoring uses an SQL-injection analogy, but SI-3.8's statement concerns operating-system commands through a kernel interface, so I did not map to it.

- `cosais_outline`, Overlay control list and SI-03(08) discussion: "much in the way that SQL injection attacks are identified"
- `cosais_outline`, Additional proposed controls: "CA-08, Penetration Testing"
- `sp2400`, §3.5.4: "application designers may design systems with the assumption that prompt injection attacks are possible"
- `sp2400`, §4.2: "adaptive attacks have bypassed many published jailbreak and prompt injection defenses that initially reported strong robustness"

**MS-07** (confirmed-novel): Rating unchanged. The CM-4.1 tension recorded as a qualifier stands: NIST's own outline selects the separation direction.

- `sp2400`, §4 (introduction): "models have reached the internet from test environments and gained unauthorized access to third-party systems"
- `sp2400`, §4 (introduction): "are thus outside the scope of the taxonomy"
- `cosais_outline`, Additional proposed controls: "Separate Test Environments"
- Not found: 'evaluation awareness', 'situational awareness', 'sandbagging' and 'indistinguishable from production' return 0 hits in SP 2400-102, IR 8596, the NCCoE summary and IR 8621.

**MS-09** (threat-recognised): Rating unchanged. NCCoE's signed 'flight plan' binds an approval to a decomposed task list, which is related to MS-09's approval snapshot but binds to intent, not to what was rendered.

- `sp2400`, §4.4: "adversaries can inject instructions visually"
- `nccoe`, Delegation and Accountability: "cryptographically signed intent or flight plans"
- `nist_blog`, Relying on Human-in-the-Loop: "relying too heavily on HITL mechanisms introduces a severe risk of consent fatigue"
- Not found: 'rendering fidelity', 'perceptually equivalent', 'what the human sees' and 'approval snapshot' return 0 hits in the four documents searched.

**MS-14** (threat-recognised): Rating unchanged. Absence from a draft attack taxonomy is not absence from NIST's thinking; SP 2400-102 says mitigations for multi-agent threats are 'an understudied area'.

- `sp2400`, §3.5.2: "certain malicious prompts could serve as worms"
- `sp2400`, §4.6: "self-replicating prompt injection attacks that spread malicious instructions across interconnected agents"
- `sp2400`, §4.6: "Firewalls placed on inter-agent channels enforce constraints at each communication channel"
- Not found: 'fingerprint' and 'quarantin*' return 0 hits in SP 2400-102, IR 8596, the NCCoE summary and IR 8621. §3.5.4's indirect-injection mitigations (training, detection, input filtering, spotlighting, privilege separation) do not include screening of outbound content.

**GRM-03** (converging): Rating unchanged but the weakest remaining novel call after MS-04: the concept is present in NIST drafts and the policy container exists in 800-53 (PL-4, AC-1). May soften to partial once an agent overlay is published.

- `ir8596`, GV.RR-02 (Secure focus area): "Organizations decide who is accountable for actions taken by autonomous systems"
- `ir8596`, ID.RA-06 (Defend focus area: AI used for cyber defence): "Define conditions for disabling AI autonomy during risk response"
- `ir8621`, §8.3: "what actions can be automated, what actions require human authorization"
- Not found: 'risk tier', 'tiered autonomy', 'autonomy level' and 'autonomy tier' return 0 hits across the four documents searched.


## Method and limits

- Matching rationale `functional` (NIST IR 8477): compares what the controls do, not their wording.
- Mapped at control level. NIST recommends statement level; control-level mappings are coarser and will over-state overlap.
- Each 800-53 ID was checked to exist in the Rev 5.2.0 catalog; the generator fails on a miss. That proves the ID exists, not that the mapping is sound.
- 800-53 statements were read from the catalog for the candidate targets. Many have unfilled organisation-defined parameters (ODPs), so 'direct' assumes sensible ODP values.
- Ratings are one analyst's judgement, AI-assisted. They need review by someone who has assessed against 800-53.
- Out of scope: the pillars not listed above; a mapping to NIST agent overlays (none published; see the NIST cross-check, which covers only the novel ratings); 800-53 baselines (low/moderate/high), which would change what 'covered' means in practice.
