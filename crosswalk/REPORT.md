# SHIELD-AI to NIST SP 800-53 Rev 5: crosswalk fit report

Generated 2026-11-19 by `tools/generate_oscal_crosswalk.py` from `crosswalk/shield-ai-to-800-53r5.json`. Target catalog: SP 800-53 Rev 5.2.0. **Status: DRAFT, not SME-reviewed.**

Scope: IAM, TP and EE pillars, 34 of 69 controls.

## Headline

| Fit | Controls | Meaning |
|---|---|---|
| direct | 10 | An org meeting the mapped 800-53 controls, with agents in scope as subjects and sensible ODPs, substantially meets the SHIELD control. No residual requirement. |
| partial | 21 | The core of the control maps to 800-53, but SHIELD adds requirements 800-53 does not state. Residual is recorded. |
| novel | 3 | Only tangential 800-53 analogues exist. The control's main idea is new relative to 800-53. |

Every one of the 34 controls has at least one 800-53 neighbour (34 of 34), so none is wholly orphaned. That is a weak result by itself: 800-53 is broad enough that something always loosely applies. The fit column is the meaningful one.

## Mapping-level statistics

- 136 map entries. Relationships: intersects-with 132, no-relationship 1, subset-of 3.
- Confidence: high 21, medium 67, low 48.
- 132 of 136 entries are `intersects-with` (each side has content the other lacks); 3 are `subset-of`; 0 are `equal-to`/`equivalent-to`.

- 20 of 34 controls have at least one high-confidence mapping. 14 rest on medium or low confidence alone.

## By pillar

| Pillar | Direct | Partial | Novel |
|---|---|---|---|
| IAM | 2 | 6 | 2 |
| TP | 5 | 10 | 1 |
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
| IAM-07 | Transitive Delegation Chain Enforcement | **novel** | AU-3 (M), AU-10 (L), AC-6 (L) |
| IAM-08 | Credential Scope Narrowing | **partial** | AC-6 (H), IA-5 (M), AC-3.8 (M) |
| IAM-09 | Multi-Tenant Agent Platform Isolation | **partial** | AC-3 (H), SC-39 (M), AC-4.21 (M), SC-4 (L) |
| IAM-10 | Taint-Tracked Least-Privilege Subagent Scoping | **novel** | AC-6 (M), AC-16 (M), AC-4 (L), AC-3.13 (L) |
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
- **IAM-07 (novel)**: Maximum delegation depth (two hops), blocking downstream proxying of the agent's identity, and reconstructing the chain with originating identity. 800-53 has no concept of transitive delegation (cf. OAuth token exchange / on-behalf-of).
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

## Findings

1. **Fit (computed).** Direct 10: EE-02, EE-03, EE-06, IAM-01, IAM-05, TP-01, TP-02, TP-03, TP-05, TP-08. Partial 21. Novel 3: IAM-07, IAM-10, TP-11.
2. **Equality (computed).** 0 of 136 map entries are `equal-to`/`equivalent-to`; 3 are `subset-of`. A compliance team cannot treat 'satisfies 800-53 control X' as 'satisfies SHIELD-AI control Y' for the partial and novel controls.
3. **Human approval of autonomous action (IAM-03) is the notable IAM gap.** It is central to agent safety yet the nearest 800-53 controls are AC-4.9 (information flows) and AC-3.2 (dual authorization), neither scoped to actions. See the NIST COSIS agent overlays for whether NIST addresses it.
4. **Keyword matching would mislead.** IAM-10 'taint-tracking' collides with SI-20 'Tainting', a different concept (exfiltration detection). It is recorded as `no-relationship` with a blocking qualifier. Tooling that auto-maps on titles or text similarity would get this wrong.
5. **One identity tension (IAM-01 vs IA-2).** IA-2 ties a process to the user it acts for; IAM-01 requires a distinct agent identity. Compatible, but an implementation that reads IA-2 literally could satisfy it while failing IAM-01. Recorded as a qualifier. TP-02 inherits the same dependency (the tool must authenticate the agent, not the human).
6. **TP: mechanism maps, trigger does not.** The later TP controls (TP-10 to TP-16) come from incidents where an agent or its tooling is induced to execute attacker-controlled instructions or code. The mechanism half (signing, input validation, allow-listing, process isolation, provenance) has 800-53 homes. The trigger half (content the agent reads becomes a command; the model is an instruction source whose output must be authenticated) does not.
7. **TP-11 is the clearest novel control in the pillar.** Treating rendered content as a command channel and preserving origin isolation for an acting agent has no 800-53 vocabulary. A keyword search of Rev 5.2 statements and guidance for 'same-origin' returned no hits and for 'browser' one incidental hit. The targets listed are tangential.
8. **One 800-53 control, two different fits (SI-10.6).** Its mechanism (parameterized interfaces, output escaping) presumes a data/code boundary. TP-16 has one (an OS launch path), so SI-10.6 fits well. TP-04 does not: an LLM context has no such boundary, so the same control gives weak cover. Recorded as a qualifier on TP-04.
9. **TP-15: 800-53 permits the weak reading.** SC-39 (separate execution domain per process) arguably excludes an in-process denylist sandbox, but never says so; an assessor could accept a hardened interpreter as an 'execution domain'. SHIELD-AI's value here is the explicit negative.
10. **Supply-chain controls transfer best.** TP-05, TP-13 and TP-14 map onto the SR family, CM-14 and SI-7.15, where 800-53's provenance and authenticity vocabulary predates agent skill marketplaces but still applies. The residual is that the payload is natural-language instructions and runtime-fetchable instruction channels, not just code.
11. **TP-07 is a borderline partial/novel.** RA-3 and SA-11.2 would cover analysis of tool composition only if the organisation chose to scope threat modelling that way; nothing in 800-53 asks for it.

## Method and limits

- Matching rationale `functional` (NIST IR 8477): compares what the controls do, not their wording.
- Mapped at control level. NIST recommends statement level; control-level mappings are coarser and will over-state overlap.
- Each 800-53 ID was checked to exist in the Rev 5.2.0 catalog; the generator fails on a miss. That proves the ID exists, not that the mapping is sound.
- 800-53 statements were read from the catalog for the candidate targets. Many have unfilled organisation-defined parameters (ODPs), so 'direct' assumes sensible ODP values.
- Ratings are one analyst's judgement, AI-assisted. They need review by someone who has assessed against 800-53.
- Out of scope: the pillars not listed above; the NIST COSAIS/COSIS agent overlays; 800-53 baselines (low/moderate/high), which would change what 'covered' means in practice.
