# SHIELD-AI to NIST SP 800-53 Rev 5: crosswalk fit report

Generated 2026-11-19 by `tools/generate_oscal_crosswalk.py` from `crosswalk/shield-ai-to-800-53r5.json`. Target catalog: SP 800-53 Rev 5.2.0. **Status: DRAFT, not SME-reviewed.**

Scope: EE and IAM pillars, 18 of 69 controls.

## Headline

| Fit | Controls | Meaning |
|---|---|---|
| direct | 5 | An org meeting the mapped 800-53 controls, with agents in scope as subjects and sensible ODPs, substantially meets the SHIELD control. No residual requirement. |
| partial | 11 | The core of the control maps to 800-53, but SHIELD adds requirements 800-53 does not state. Residual is recorded. |
| novel | 2 | Only tangential 800-53 analogues exist. The control's main idea is new relative to 800-53. |

Every one of the 18 controls has at least one 800-53 neighbour (18 of 18), so none is wholly orphaned. That is a weak result by itself: 800-53 is broad enough that something always loosely applies. The fit column is the meaningful one.

## Mapping-level statistics

- 60 map entries. Relationships: intersects-with 56, no-relationship 1, subset-of 3.
- Confidence: high 12, medium 32, low 16.
- Only 3 entries are `subset-of`, and no entry is `equal-to` or `equivalent-to`. Mappings overwhelmingly `intersects-with`: each side has content the other lacks.

- 12 of 18 controls have at least one high-confidence mapping. 6 rest on medium or low confidence alone.

## By pillar

| Pillar | Direct | Partial | Novel |
|---|---|---|---|
| EE | 3 | 5 | 0 |
| IAM | 2 | 6 | 2 |

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

## Findings

1. **Mechanism maps cleanly; agent semantics do not.** The 5 `direct` controls (EE-02, EE-03, EE-06, IAM-01, IAM-05) are classic security engineering (access enforcement, resource limits, fail-safe, ephemeral credentials) where the agent is just a new subject. The weak spots are where the agent changes the threat model.
2. **Genuinely new relative to 800-53:** IAM-07, IAM-10. Delegation-chain depth and taint-driven privilege narrowing are not stateable with 800-53 vocabulary without stretching it.
3. **Human approval of autonomous action (IAM-03) is the notable gap.** It is central to agent safety yet the nearest 800-53 controls are AC-4.9 (information flows) and AC-3.2 (dual authorization), neither scoped to actions. See the NIST COSIS agent overlays for whether NIST addresses it.
4. **Keyword matching would mislead.** IAM-10 'taint-tracking' collides with SI-20 'Tainting', a different concept (exfiltration detection). It is recorded as `no-relationship` with a blocking qualifier. Any tooling that auto-maps on titles or text similarity would get this wrong.
5. **Mappings are almost never equal.** No `equal-to`; `subset-of` is rare. A compliance team cannot treat 'satisfies 800-53 control X' as 'satisfies SHIELD-AI control Y' for the partial and novel controls: SHIELD-AI is not redundant with 800-53 for the agent-specific content.
6. **One identity tension (IAM-01 vs IA-2).** IA-2 ties a process to the user it acts for; IAM-01 requires a distinct agent identity. Compatible, but an implementation that reads IA-2 literally could satisfy it while failing IAM-01. Recorded as a qualifier.

## Method and limits

- Matching rationale `functional` (NIST IR 8477): compares what the controls do, not their wording.
- Mapped at control level. NIST recommends statement level; control-level mappings are coarser and will over-state overlap.
- Each 800-53 ID was checked to exist in the Rev 5.2.0 catalog; the generator fails on a miss. That proves the ID exists, not that the mapping is sound.
- 800-53 statements were read from the catalog for the candidate targets. Many have unfilled organisation-defined parameters (ODPs), so 'direct' assumes sensible ODP values.
- Ratings are one analyst's judgement, AI-assisted. They need review by someone who has assessed against 800-53.
- Out of scope: the other five pillars (MS, DS, TP, MIR, GRM); the NIST COSAIS/COSIS agent overlays; 800-53 baselines (low/moderate/high), which would change what 'covered' means in practice.
