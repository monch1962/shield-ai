# 10 · Implementation Roadmap

Which controls to harden first. Ranking is evidence-weighted from the committed sources - incident evidence and implementation gap - so the sequence is transparent and reproducible.

## Method

Priority score = incident evidence (x3) + implementation gap (x6 when the executable policy is missing). Controls are bucketed into three phases.

## Phase 1 · Foundations (fix incident-evidenced gaps first)

| Priority | Control | Title | Score | Focus |
|---|---|---|---|---|
| 1 | **MS-08** | MCP | 183 | MCP tool definitions from '...' are not cryptographically signed; MCP server '...' is not  |
| 2 | **EE-01** | Execution environment boundary enforcement | 153 | tool '...' is high-risk and agent '...' is not sandboxed (fail closed) |
| 3 | **TP-15** | In-process code-execution sandbox sufficienc | 147 | code execution by agent '...' runs LLM-generated/untrusted code outside an OS/VM-isolated  |

## Phase 2 · Consolidation (raise maturity to L3)

| Priority | Control | Title | Score | Focus |
|---|---|---|---|---|
| 1 | **MIR-02** | Behavioural anomaly detection baseline per-a | 129 | action by agent '...' deviates from its behaviour baseline; sensitive tool '...' from ephe |
| 2 | **EE-07** | Agent control-plane configuration integrity | 123 | agent configuration loaded from a world-writable location (config-trust class); agent cont |
| 3 | **MS-09** | Perception-fidelity enforcement for human-in | 120 | approval evidence comes from an agent-generated attestation (sockpuppet class); out-of-ban |
| 4 | **TP-06** | Dependency scanning | 117 | deployment with unscanned dependencies; critical-severity dependency finding not blocked |
| 5 | **TP-10** | Agent platform inbound control-plane protect | 108 | listener binding '...' is not on the approved binding list (default deny); web-origin bind |
| 6 | **MS-04** | Adversarial robustness | 105 | prompt-injection or imperceptible-content marker '...' found in agent-visible content |
| 7 | **EE-08** | Evaluation-harness isolation and integrity | 87 | evaluation run without a verified egress block (isolation asserted, not enforced); evaluat |

## Phase 3 · Optimisation (deepen verification)

| Priority | Control | Title | Score | Focus |
|---|---|---|---|---|
| 1 | **EE-05** | Host-trusted configuration file injection pr | 81 | agent can write host-trusted path '...' (indirect escape class); agent '...' file write wi |
| 2 | **TP-16** | Tool-connection and launch-path integrity | 78 | agent '...' connection hands server-supplied protocol metadata to a process-launch/shell p |
| 3 | **MS-10** | Agent memory-store integrity | 75 | memory-store write by agent '...' is unauthenticated; memory-store write by agent '...' ca |
| 4 | **TP-01** | Tool inventory and registry | 63 | tool '...' is not in the approved tool registry |
| 5 | **TP-12** | Tool-call provenance and dispatch verificati | 63 | dispatch without session provenance (fail closed); dispatch without turn provenance (fail  |
| 6 | **MIR-01** | Agent activity logging | 57 | audit record not written to append-only storage (integrity requirement); agent '...' actio |
| 7 | **MS-12** | MCP discovery-metadata and shared-cache inte | 51 | MCP discovery response for agent '...' carries unbounded server-supplied instructions; mus |
| 8 | **TP-03** | API gateway security | 48 | tool '...' call not rate-limited by the gateway; tool '...' call payload not schema-valida |
| 9 | **TP-13** | Agent dependency-install provenance verifica | 48 | install by agent '...' references a package not confirmed to exist in the intended registr |
| 10 | **GRM-02** | Requirement:** AI risk register | 45 | kill-switch capability not exercised (AI-speed response requires one rehearsed red button) |
| 11 | **IAM-03** | Human oversight controls | 45 | approval evidence from session history is not human approval (forged-approval class); fina |
| 12 | **TP-04** | Tool output validation | 45 | tool '...' output not validated against a known-good schema; tool '...' output not sanitis |
| 13 | **MS-11** | Operational data-stream integrity | 42 | agent action triggered by log/alert content from an unverified producer; instruction-beari |
| 14 | **TP-09** | Explicit tool registration — no implicit too | 42 | tool '...' was not explicitly registered (implicit exposure class); tool '...' auto-regist |
| 15 | **GRM-04** | Requirement:** Third-party AI risk managemen | 39 | action using third-party vendor '...' without security assessment; vendor '...' without co |
| 16 | **IAM-02** | Scope-bound delegation | 39 | agent '...' has no scope-bound delegation claim (fail closed); agent '...' has wildcard pe |
| 17 | **MS-13** | Transcript and conversation authenticity | 36 | agent '...' reads a transcript whose model outputs are not signed at the model boundary; s |
| 18 | **TP-14** | Skill/plugin payload integrity and instructi | 36 | execute skill '...' for agent '...' with an unsigned payload; never execute unsigned; exec |
| 19 | **IAM-01** | Agent identity management | 33 | agent '...' has no unique identity (sharing human credentials); agent '...' identity is no |
| 20 | **DS-06** | Requirement:** Output validation | 30 | output not verified clean by the leakage scanner (fail closed); output flagged for data le |
| 21 | **EE-04** | Evaluation sandbox integrity | 30 | evaluation run with unverified evaluation-to-production isolation (fail closed); evaluatio |
| 22 | **IAM-09** | Multi-tenant agent platform isolation | 30 | request not scoped to tenant ID at the data layer (presentation-layer checks only); user-c |
| 23 | **MS-15** | Cross-tenant agent memory and state isolatio | 27 | pooled memory_read by agent '...' returned a cross-tenant hit (owner != querying principal |
| 24 | **TP-05** | Pipeline integrity | 27 | deployment from an unsigned CI/CD run; deployment without pipeline attestation |
| 25 | **DS-07** | Requirement:** Agent-originated artifact pub | 24 | execution-bearing configuration write requires human-console approval (Kiro class); agent  |
| 26 | **MIR-06** | Forensic readiness | 21 | high-impact action '...' by agent '...' is not reconstructible from immutable logs |
| 27 | **TP-11** | Agent browser and content-rendering isolatio | 21 | document upload rendered without sanitisation before assistant processing; token access fr |
| 28 | **EE-02** | Infrastructure API access control | 18 | agent call to infrastructure API '...' without explicit tool registration |
| 29 | **MS-05** | Model behaviour validation | 18 | output by agent '...' not evaluated by proxy-layer guardrails (fail closed); output by age |
| 30 | **EE-03** | Resource usage limiting | 15 | agent '...' CPU usage ...%% exceeds limit ...%%; agent '...' network usage ... Mbps exceed |
| 31 | **GRM-06** | Requirement:** Board and executive reporting | 15 | no executive dashboard for AI security posture (maturity, findings, compliance, risk accep |
| 32 | **IAM-10** | Taint-tracked least-privilege subagent scopi | 15 | agent '...' processed an externally-submitted record that was not taint-marked at ingestio |
| 33 | **MIR-04** | Incident response playbooks AI-specific IR p | 15 | ... incident acknowledged without a named AI-specific IR playbook; ... incident without an |
| 34 | **MS-07** | Deployment context obfuscation | 15 | evaluation environment distinguishable from production (endpoints, data shapes, latency);  |
| 35 | **MS-14** | Self-replication barrier | 15 | outbound publish by agent '...' matches an instruction-bearing n-gram fingerprint (replica |
| 36 | **DS-03** | Memory sanitisation | 12 | agent '...' persists classified or sensitive data beyond session lifetime; agent '...' ses |
| 37 | **DS-08** | Requirement:** Destination and emergent-chan | 12 | agent '...' egress to destination not on the payload-blind allow-list; agent '...' egress  |
| 38 | **EE-06** | Fail-closed sandbox operation | 12 | interpreter isolation flags are a convenience feature, not a security boundary; no sandbox |
| 39 | **GRM-03** | Ethical use policy | 12 | high-risk tier agent deployed without human-in-the-loop requirement per risk tier; action  |
| 40 | **IAM-04** | Credential isolation | 12 | agent '...' credentials not isolated from human credentials; agent '...' compromise signal |
| 41 | **IAM-06** | Cross-session boundary enforcement | 12 | agent '...' session shares credentials across sessions; agent '...' session is not an inde |
| 42 | **MS-03** | Supply chain security | 12 | model '...' deployed without an ML component SBOM; model '...' provenance signature not ve |
| 43 | **TP-07** | Cross-tool dependency analysis | 12 | deployment without cross-tool dependency (transitive risk) analysis; tool combination enab |
| 44 | **TP-08** | API gateway infrastructure-isolation mode | 12 | tool '...' call without an active gateway API allow-list; infrastructure control-plane API |
| 45 | **DS-01** | Data classification and labelling | 9 | data ingestion without automated classification (fail closed); data ingestion with no clas |
| 46 | **IAM-07** | Transitive delegation chain enforcement | 9 | delegation chain for agent '...' is ... hops, exceeding the bound of ...; delegation chain |
| 47 | **IAM-08** | Credential scope narrowing | 9 | agent '...' holds a broad service role instead of per-tool scoped credentials; agent '...' |
| 48 | **DS-04** | Data minimisation | 6 | bulk data access by agent (field-level filtering required); retrieval without field-level  |
| 49 | **DS-02** | Inference data protection | 3 | inference data not encrypted end-to-end; inference transport below TLS 1.3 minimum |
| 50 | **GRM-01** | AI governance body | 3 | deployment without a chartered AI governance body; AI governance body lacks cross-function |
| 51 | **GRM-05** | Regulatory mapping and compliance reporting | 3 | deployment without an automated regulatory mapping (ISM, E8, SOCI, CPS 234, PSPF, Privacy  |
| 52 | **MIR-03** | Prompt audit log | 3 | sensitive prompt/response pair not captured for the audit log; captured prompt/response pa |
| 53 | **MS-01** | Model weight protection | 3 | model '...' weights not encrypted at rest and in transit; model '...' weights lack key man |
| 54 | **MS-02** | Training data integrity | 3 | training run with untracked dataset provenance; training run with unsanitised dataset (PII |
| 55 | **MS-06** | Model inventory and lineage tracking | 3 | model '...' not registered in the model inventory; model '...' has no traceable lineage |
| 56 | **DS-05** | Training data governance | 0 | training run without dataset lineage tracking; training run on personal data without verif |
| 57 | **IAM-05** | Just-in-time access | 0 | agent '...' has standing (non-ephemeral) credentials; agent '...' session expired without  |
| 58 | **MIR-05** | Mandatory reporting integration | 0 | incident reported by agent '...' has no regulatory reporting trigger (SOCI 12h / APRA 72h  |
| 59 | **TP-02** | Tool access control | 0 | tool '...' call not authenticated to the agent identity; tool '...' authenticated against  |


See [06 · Technical Verification](06-controls-technical.md) for full per-control checklists.
