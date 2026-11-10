# 02 · Controls → Industry Incidents

Which SHIELD-AI controls are actually **evidenced by real incidents**? This view counts
every reference to a control across the framework's incident coverage verdicts
(INC-01…INC-92). The most-cited controls are the highest-priority hardening targets —
they are the controls the real world has repeatedly shown we need.

![Controls incident map](../assets/diagrams/controls-incident-map.svg)

## Coverage leaders (most evidenced)

| Control | Title | Incident references |
|---|---|---|
| **MS-08** | MCP | 61 |
| **EE-01** | Execution environment boundary enforcement | 51 |
| **TP-15** | In-process code-execution sandbox sufficiency | 49 |
| **MIR-02** | Behavioural anomaly detection baseline per-agent behaviour established over training period; alerts on deviation  --  unusual tool, unusual data access pattern, unusual frequency; | 43 |
| **EE-07** | Agent control-plane configuration integrity | 41 |
| **MS-09** | Perception-fidelity enforcement for human-in-the-loop approvals | 40 |
| **TP-06** | Dependency scanning | 39 |
| **TP-10** | Agent platform inbound control-plane protection | 36 |
| **MS-04** | Adversarial robustness | 35 |
| **EE-08** | Evaluation-harness isolation and integrity | 29 |

## Full coverage inventory

| Control | Title | Incident references |
|---|---|---|
| MS-08 | MCP | 61 |
| EE-01 | Execution environment boundary enforcement | 51 |
| TP-15 | In-process code-execution sandbox sufficiency | 49 |
| MIR-02 | Behavioural anomaly detection baseline per-agent behaviour established over training period; alerts on deviation  --  unusual tool, unusual data access pattern, unusual frequency; | 43 |
| EE-07 | Agent control-plane configuration integrity | 41 |
| MS-09 | Perception-fidelity enforcement for human-in-the-loop approvals | 40 |
| TP-06 | Dependency scanning | 39 |
| TP-10 | Agent platform inbound control-plane protection | 36 |
| MS-04 | Adversarial robustness | 35 |
| EE-08 | Evaluation-harness isolation and integrity | 29 |
| EE-05 | Host-trusted configuration file injection prevention | 27 |
| TP-16 | Tool-connection and launch-path integrity | 26 |
| MS-10 | Agent memory-store integrity | 25 |
| TP-12 | Tool-call provenance and dispatch verification | 21 |
| TP-01 | Tool inventory and registry | 21 |
| MIR-01 | Agent activity logging | 19 |
| MS-12 | MCP discovery-metadata and shared-cache integrity | 17 |
| TP-13 | Agent dependency-install provenance verification | 16 |
| TP-03 | API gateway security | 16 |
| GRM-02 | Requirement:** AI risk register | 15 |
| IAM-03 | Human oversight controls | 15 |
| TP-04 | Tool output validation | 15 |
| MS-11 | Operational data-stream integrity | 14 |
| TP-09 | Explicit tool registration — no implicit tool exposure | 14 |
| IAM-02 | Scope-bound delegation | 13 |
| GRM-04 | Requirement:** Third-party AI risk management | 13 |
| MS-13 | Transcript and conversation authenticity | 12 |
| TP-14 | Skill/plugin payload integrity and instruction-channel isolation | 12 |
| IAM-01 | Agent identity management | 11 |
| EE-04 | Evaluation sandbox integrity | 10 |
| IAM-09 | Multi-tenant agent platform isolation | 10 |
| DS-06 | Requirement:** Output validation | 10 |
| MS-15 | Cross-tenant agent memory and state isolation | 9 |
| TP-05 | Pipeline integrity | 9 |
| DS-07 | Requirement:** Agent-originated artifact publication control | 8 |
| TP-11 | Agent browser and content-rendering isolation | 7 |
| MIR-06 | Forensic readiness | 7 |
| MS-05 | Model behaviour validation | 6 |
| EE-02 | Infrastructure API access control | 6 |
| MIR-04 | Incident response playbooks AI-specific IR procedures distinct from general IR: prompt injection containment, model rollback, tool access revocation, session invalidation; | 5 |
| MS-14 | Self-replication barrier | 5 |
| IAM-10 | Taint-tracked least-privilege subagent scoping | 5 |
| EE-03 | Resource usage limiting | 5 |
| GRM-06 | Requirement:** Board and executive reporting | 5 |
| MS-07 | Deployment context obfuscation | 5 |
| DS-08 | Requirement:** Destination and emergent-channel egress inventory | 4 |
| TP-07 | Cross-tool dependency analysis | 4 |
| TP-08 | API gateway infrastructure-isolation mode | 4 |
| DS-03 | Memory sanitisation | 4 |
| MS-03 | Supply chain security | 4 |
| IAM-06 | Cross-session boundary enforcement | 4 |
| IAM-04 | Credential isolation | 4 |
| EE-06 | Fail-closed sandbox operation | 4 |
| GRM-03 | Ethical use policy | 4 |
| IAM-08 | Credential scope narrowing | 3 |
| IAM-07 | Transitive delegation chain enforcement | 3 |
| DS-01 | Data classification and labelling | 3 |
| DS-04 | Data minimisation | 2 |
| MS-01 | Model weight protection | 1 |
| GRM-05 | Regulatory mapping and compliance reporting | 1 |
| MS-06 | Model inventory and lineage tracking | 1 |
| MIR-03 | Prompt audit log | 1 |
| DS-02 | Inference data protection | 1 |
| MS-02 | Training data integrity | 1 |
| GRM-01 | AI governance body | 1 |
| IAM-05 | Just-in-time access | 0 |
| MIR-05 | Mandatory reporting integration | 0 |
| DS-05 | Training data governance | 0 |
| TP-02 | Tool access control | 0 |

## Not yet directly evidenced by an incident (4 controls)

These controls are part of the framework's baseline but have not yet been the direct
subject of a catalogue incident. They are required coverage, not optional — the absence
of a documented incident is a coverage gap to close, not a control to drop.

IAM-05, MIR-05, DS-05, TP-02
