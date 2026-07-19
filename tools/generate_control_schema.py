#!/usr/bin/env python3
"""
SHIELD-AI Control Schema Generator
===================================
Generates machine-readable control definitions from canonical Python data structures.

Outputs:
  assets/shield-ai-control-schema.json   — Full control definitions, maturity
                                            indicators, assessment questions,
                                            artifacts, regulatory mappings
  policies/shield_ai_*.rego              — Rego policy stubs for automated
                                            control testing (optional)

Usage:
  python3 tools/generate_control_schema.py              # generate JSON only
  python3 tools/generate_control_schema.py --rego        # generate JSON + Rego stubs
"""

import json
import os
import sys
from datetime import date

# ──────────────────────────────────────────────
# Canonical control definitions
# ──────────────────────────────────────────────

FRAMEWORK_VERSION = "1.1"
FRAMEWORK_DATE = "2026-07"

PILLARS = {
    "MS":  "Model Security",
    "IAM": "Identity and Access",
    "DS":  "Data Security",
    "TP":  "Tool and Pipeline Security",
    "MIR": "Monitoring, Logging, and Incident Response",
    "GRM": "Governance and Risk Management",
}

PILLAR_ORDER = ["MS", "IAM", "DS", "TP", "MIR", "GRM"]

CONTROLS = {}

def reg(cid, title, pillar, description, objective,
        maturity, questions, artifacts, mappings=None, tags=None):
    """Register a control definition."""
    cid = cid.upper()
    CONTROLS[cid] = {
        "id": cid,
        "title": title,
        "pillar": pillar,
        "description": description,
        "objective": objective,
        "maturity": {
            "L1": maturity[0],
            "L2": maturity[1],
            "L3": maturity[2],
            "L4": maturity[3],
        },
        "assessment_questions": questions,
        "artifacts": artifacts,
        "regulatory_mappings": mappings or {},
        "tags": tags or [],
    }

# ════════════════════════════════════════════
# PILLAR 1: MODEL SECURITY
# ════════════════════════════════════════════

reg("MS-01", "Model Weight Protection", "MS",
    "Model weights represent the trained intelligence of an AI system — often the single most valuable "
    "intellectual property an organisation has deployed. Weight protection covers encryption at rest and "
    "in transit, HSM-backed key management, and remote attestation for edge deployments.",
    "Ensure model weights are protected against exfiltration, cloning, and inversion attacks through "
    "encryption, access control, and integrity verification.",
    [
        "Weights stored on shared storage with default encryption. No key rotation.",
        "Weights encrypted at rest with cloud-managed KMS. Separate key per model. Basic access controls.",
        "HSM-backed key management. Automated key rotation. Access approval workflow. Full audit trail.",
        "Continuous attestation of weight integrity. Automated incident response on unauthorised access. Edge attestation.",
    ],
    [
        "Are model weights encrypted at rest? Which encryption standard and key management system?",
        "Are model weights encrypted during transit between training infrastructure, storage, and inference endpoints?",
        "Is a hardware security module (HSM) or cloud KMS used for weight encryption keys?",
        "Can model weights be downloaded by any engineer with cloud console access, or is there an approval workflow?",
        "For edge deployments: is there a remote attestation mechanism that verifies weight integrity at boot?",
        "Are weight encryption keys rotated on a schedule? What triggers a rotation?",
        "Is there an inventory of all locations where model weights are stored?",
    ],
    [
        "Key management policy (who has access to weight encryption keys)",
        "Cloud KMS configuration (key hierarchy, rotation schedule, access logs)",
        "Model weight storage configuration (bucket policies, encryption settings, ACLs)",
        "HSM configuration and audit logs (if hardware-backed)",
        "Remote attestation logs (for edge deployments)",
        "Data classification policy (are weights classified as sensitive/critical?)",
        "Incident response playbook for weight exfiltration",
    ],
    mappings={"ISM": "Guidelines for Cryptography, System Management — access control",
              "PSPF": "Information Security"},
    tags=["ISM", "PSPF"])

reg("MS-02", "Training Data Integrity", "MS",
    "Training data integrity ensures that data used to train or fine-tune a model has not been poisoned, "
    "corrupted, or substituted. Data poisoning — an attacker inserting crafted samples into the training "
    "dataset — can cause a model to behave normally until a specific trigger condition is met.",
    "Ensure training and fine-tuning datasets are verified for integrity, provenance, and freedom from "
    "poisoning or corruption before use.",
    [
        "Training data collected ad-hoc. No provenance tracking. No validation.",
        "Dataset versioning implemented. Basic format validation at ingestion. Access controls on training data.",
        "Automated data validation pipeline (format, anomaly detection, PII scanning). Full lineage tracking. Third-party data assessments.",
        "Continuous monitoring for data drift and statistical anomalies. Automated retraining triggered by integrity findings.",
    ],
    [
        "Is there a documented data provenance pipeline for all training datasets?",
        "How is training data validated before ingestion (format checks, anomaly detection, statistical profiling)?",
        "Is there a data sanitisation step that removes PII, sensitive content, and potential poison samples?",
        "Are dataset versions tracked with hashes or signatures to detect tampering?",
        "Who has write access to training data repositories? Is there an approval workflow?",
        "Are third-party datasets subject to the same integrity checks as internally generated data?",
    ],
    [
        "Data pipeline architecture documentation",
        "Dataset versioning records (DVC, HuggingFace datasets, MLflow)",
        "Data validation test results (Great Expectations, TFX, custom)",
        "Training data access control lists",
        "Data provenance / lineage tracking system configuration",
        "Data ingestion audit logs",
    ],
    mappings={"ISM": "Guidelines for Software Development — data validation",
              "OWASP LLM Top 10 v2": "LLM04 (Data Poisoning)",
              "NIST AI RMF": "IDENTIFY (ID.DA)"},
    tags=["ISM", "OWASP", "NIST"])

reg("MS-03", "Supply Chain Security", "MS",
    "AI supply chain security covers the provenance and integrity of model weights, ML libraries, "
    "training infrastructure, and deployment tooling at every stage. Pre-trained models from public "
    "repositories (HuggingFace, PyTorch Hub) and ML libraries are frequent targets for supply chain attacks.",
    "Verify the provenance and integrity of model weights, ML libraries, training infrastructure, and "
    "deployment tooling throughout the AI supply chain.",
    [
        "Models downloaded from public repos with no integrity verification. No ML SBOM.",
        "ML SBOM exists for critical models. Model publisher verified. Basic dependency scanning.",
        "Signed checkpoints at every stage. Vendor assessments for all model publishers. Automated dependency scanning.",
        "Continuous supply chain monitoring. Automated rollback on integrity violation. Published ML SBOM for regulator review.",
    ],
    [
        "Is there an ML software bill of materials (ML SBOM) for each model? What does it include?",
        "Are model weights verified against publisher signatures or hashes before deployment?",
        "Are all ML libraries and dependencies sourced from trusted registries with integrity verification?",
        "Is there a vulnerability scanning process for ML-specific dependencies?",
        "Are model publishers subject to a vendor security assessment?",
        "Are model checkpoints cryptographically signed at each stage?",
    ],
    [
        "ML SBOM(s) for each production model",
        "Model provenance documentation",
        "Third-party model/vendor security assessments",
        "PyTorch / TensorFlow / dependency registry configuration",
        "Vulnerability scanning reports for ML dependencies",
        "Model checkpoint signing configuration",
    ],
    mappings={"ISM": "Guidelines for Procurement and Outsourcing, System Management — supply chain",
              "SOCI Act": "CIRMP — supply chain obligations",
              "OWASP LLM Top 10 v2": "LLM10 (Supply Chain)",
              "NIST AI RMF": "IDENTIFY (ID.SC)"},
    tags=["ISM", "SOCI", "OWASP", "NIST"])

reg("MS-04", "Adversarial Robustness", "MS",
    "Adversarial robustness ensures that the model resists malicious inputs designed to produce unintended "
    "behaviour. For agentic AI, the primary adversarial attack is prompt injection — crafting input that "
    "causes the model to ignore its system prompt and follow attacker instructions.",
    "Test and verify that models resist prompt injection, jailbreaking, and other adversarial inputs "
    "through automated testing, red-teaming, and proxy-layer guardrails.",
    [
        "No adversarial testing. Models deployed based on functional tests only.",
        "Basic prompt injection test suite run manually before major deployments.",
        "Automated adversarial test suite in CI/CD. Quarterly red-teaming. Output guardrails at proxy layer.",
        "Continuous automated red-teaming. Real-time adversarial input detection and blocking. Coverage against MITRE ATLAS.",
    ],
    [
        "Is there a standardised prompt injection test suite? How often is it run?",
        "Are jailbreak evaluation techniques applied (DAN, token smuggling, role-playing, hypothetical framing)?",
        "Are new model versions required to pass adversarial tests before deployment (CI/CD gate)?",
        "Is red-teaming conducted with AI-specific focus?",
        "Are output guardrails deployed at the inference proxy layer (not in-model)?",
        "Is there a process for capturing and learning from adversarial inputs encountered in production?",
    ],
    [
        "Prompt injection test suite and results",
        "Jailbreak evaluation reports",
        "CI/CD pipeline configuration showing adversarial test gates",
        "Red-teaming engagement scope reports",
        "Output guardrail configuration (inference proxy layer)",
        "Production adversarial input monitoring logs",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM01 (Prompt Injection), LLM05 (Jailbreak)",
              "NIST AI RMF": "MEASURE (ME.AD)",
              "EU AI Act": "Art. 15 — Accuracy",
              "MITRE ATLAS": "AML.T0051, AML.T0059"},
    tags=["OWASP", "NIST", "EU", "MITRE"])

reg("MS-05", "Model Behaviour Validation", "MS",
    "Behaviour validation ensures that model outputs conform to expected bounds — the model produces "
    "content that is safe, contextually appropriate, and within its defined scope of operation. This "
    "is distinct from adversarial robustness (MS-04), which focuses on malicious inputs; behaviour "
    "validation focuses on model outputs regardless of input quality.",
    "Validate that model outputs conform to expected safety, content, and scope boundaries through "
    "proxy-layer guardrails and per-agent behaviour configuration.",
    [
        "No output validation. Model responses served as-is.",
        "Basic output guardrails (PII filtering, toxicity detection). Manual review of flagged outputs.",
        "Proxy-layer guardrails for all output categories. Automated blocking. Per-agent guardrail configuration.",
        "Continuous guardrail improvement based on production telemetry. Behavioural bounds dynamically adjusted.",
    ],
    [
        "Are output guardrails implemented at the inference proxy layer or within the model?",
        "What content categories are filtered (PII, toxic content, code, financial advice, medical guidance)?",
        "Are there topic scoping mechanisms that prevent the agent from operating outside its designated domain?",
        "Is output validation performed on every model response before it reaches the user or triggers a tool call?",
        "Are guardrails configurable per-agent?",
        "Are guardrail bypass attempts logged and reviewed?",
    ],
    [
        "Output guardrail configuration files",
        "Content filtering policy document",
        "Agent scope definition documents (per-agent operational domain)",
        "Guardrail test results (benign and adversarial)",
        "Guardrail bypass / violation incident logs",
        "Production guardrail monitoring dashboard",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM02 (Insecure Output Handling)",
              "NIST AI RMF": "MANAGE (MG.DE)",
              "EU AI Act": "Art. 14 — Human Oversight",
              "ISO 42001": "Clause 8.6"},
    tags=["OWASP", "NIST", "EU"])

reg("MS-06", "Model Inventory and Lineage Tracking", "MS",
    "Model inventory and lineage tracking ensures that every model in the organisation is known, "
    "versioned, and traceable from training through deployment to retirement. Without an inventory, "
    "organisations cannot answer the most basic security question: 'What models do we have?'",
    "Maintain a complete, versioned inventory of all models with traceable lineage from training "
    "through deployment to retirement.",
    [
        "No central model inventory. Models tracked in spreadsheets or not at all.",
        "Central model registry with manual entries for critical models. Basic metadata captured.",
        "Automated model discovery. Full metadata captured for all models. Promotion workflow enforced.",
        "Continuous inventory scanning. Automated decommissioning of dormant models. Real-time lineage tracking.",
    ],
    [
        "Is there a central model registry or inventory? Does it cover all models?",
        "What metadata is captured per model (version, training data, deployment location, owner, status)?",
        "Are models automatically discovered, or is the inventory manually maintained?",
        "Is there an approval workflow for model promotion?",
        "Are retired models properly decommissioned?",
        "Can the organisation produce a model inventory report for regulator review within 24 hours?",
    ],
    [
        "Model registry configuration (MLflow, SageMaker, custom)",
        "Model metadata completeness (coverage, fields populated)",
        "Model promotion workflow documentation",
        "Model retirement / decommissioning records",
        "Model access control lists",
        "Shadow AI detection mechanisms",
    ],
    mappings={"NIST AI RMF": "GOVERN (GV.OD)",
              "EU AI Act": "Art. 11 — Registration",
              "ISO 42001": "Clause 7.4"},
    tags=["NIST", "EU"])

# ════════════════════════════════════════════
# PILLAR 2: IDENTITY AND ACCESS
# ════════════════════════════════════════════

reg("IAM-01", "Agent Identity Management", "IAM",
    "Every agent must have a unique, auditable digital identity that is distinct from any human user's "
    "identity. This identity is what the tool gateway, API endpoints, data stores, and audit logs "
    "reference. When agents share human credentials, there is no way to attribute actions to a specific agent.",
    "Ensure every agent has a unique, lifecycle-managed digital identity distinct from human user "
    "identities, integrated with the organisation's identity provider.",
    [
        "Agents use shared human credentials or no credentials. No agent identity exists.",
        "Per-agent service accounts created. Manual lifecycle management.",
        "Automated agent identity lifecycle. Integrated with IDP. Agent identities flagged in monitoring.",
        "SPIFFE/SPIRE workload identity for every agent. Automated credential rotation. Cross-platform identity federation.",
    ],
    [
        "Do agents use service accounts / workload identities, or do they inherit human credentials?",
        "Is each agent's identity unique, or do multiple agents share the same identity?",
        "Is the agent identity lifecycle managed (creation, rotation, revocation)?",
        "Are agent identities integrated with the organisation's existing identity provider (Azure AD, Okta, etc.)?",
        "Can agent-to-agent calls be attributed to a specific source agent identity?",
        "Is there an audit trail showing which human initiated each agent session?",
    ],
    [
        "Agent identity provisioning process documentation",
        "Identity provider configuration (service accounts, workload identities)",
        "Agent identity lifecycle policy",
        "Identity governance tool configuration",
        "Audit logs showing agent identity attribution",
        "Session initiation audit records (human → agent correlation)",
    ],
    mappings={"ISM": "Guidelines for System Management — identification and authentication",
              "Essential Eight": "Restrict Administrative Privileges",
              "NIST AI RMF": "IDENTIFY (ID.AM)"},
    tags=["ISM", "E8", "NIST"])

reg("IAM-02", "Scope-Bound Delegation", "IAM",
    "Scope-bound delegation ensures that an agent's permissions are limited to the minimum set of tools, "
    "data, and actions required for its function — and that the agent cannot exceed these bounds, cannot "
    "grant permissions to other agents beyond its own scope, and cannot self-escalate privileges.",
    "Limit each agent's permissions to the minimum set of tools, data, and actions required for its "
    "function, enforced by a policy-as-code engine at invocation time.",
    [
        "Agents have the same permissions as the initiating human. No scope boundaries.",
        "Agent permissions manually scoped to a subset of human permissions. Static tool allow-lists.",
        "Policy-as-code engine enforces per-agent scope at invocation time. Bounded delegation in multi-agent architectures.",
        "Dynamic scope adjustment based on context and risk. Continuous verification of scope compliance.",
    ],
    [
        "Are agent permissions explicitly scoped per-agent, or do agents inherit the human's full permission set?",
        "Is there a policy enforcement point (OPA, custom authz) that evaluates every agent action against its permitted scope?",
        "Can an agent access tools or data that its initiating human cannot?",
        "Can an agent escalate its own privileges or modify its permission scope?",
        "In multi-agent architectures, does agent-to-agent delegation respect the original scope?",
        "Are tool permissions evaluated at invocation time, not just at session start?",
    ],
    [
        "Agent permission scope definitions (per-agent tool and data access)",
        "Policy-as-code files (OPA/Rego) defining agent authorisation rules",
        "Tool gateway configuration (allow-lists, schema validation)",
        "Agent authorisation audit logs (allowed vs denied actions)",
        "Multi-agent delegation chain documentation",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM08 (Excessive Agency)",
              "NIST AI RMF": "GOVERN (GV.AC)",
              "Essential Eight": "Restrict Administrative Privileges, User Application Hardening",
              "SOCI Act": "CIRMP s.4(b)"},
    tags=["OWASP", "NIST", "E8", "SOCI"])

reg("IAM-03", "Human Oversight Controls", "IAM",
    "Human oversight ensures that high-risk agent actions require explicit human approval before "
    "execution. Not every agent action needs human review — a customer support agent reading account "
    "details is low-risk; the same agent writing to the account requires approval.",
    "Implement risk-tiered human approval gates for agent actions, with documented break-glass "
    "procedures for urgent situations.",
    [
        "No human oversight. Agent acts autonomously on all actions.",
        "High-risk actions flagged for human review. Manual approval process.",
        "Risk-based approval tiers. Automated approval gates. Time-limited approvals. Break-glass procedures documented.",
        "Context-aware approval requirements. Multi-party approval for critical actions. Oversight mechanism independently audited.",
    ],
    [
        "Are agent actions classified into risk tiers? Which actions require human approval?",
        "Is there a human-in-the-loop mechanism for high-risk actions?",
        "What is the approval process (time limit, escalation, delegation)?",
        "Is there a break-glass procedure for urgent actions when the approver is unavailable?",
        "Are approvals logged with context (what action, why approved, by whom)?",
    ],
    [
        "Agent risk classification policy",
        "Human-in-the-loop workflow configuration",
        "Approval gate logs (approved, denied, expired)",
        "Break-glass procedure documentation",
        "Approval audit trail",
    ],
    mappings={"EU AI Act": "Art. 14 — Human Oversight",
              "NIST AI RMF": "MANAGE (MG.DE)",
              "APRA CPS 234": "s.2 — Board accountability for controls"},
    tags=["EU", "NIST", "CPS234"])

reg("IAM-04", "Credential Isolation", "IAM",
    "Credential isolation ensures that agent credentials are stored, managed, and rotated separately "
    "from human credentials, and that a compromise of one does not compromise the other.",
    "Store, manage, and rotate agent credentials separately from human credentials with hardware-backed "
    "protection for critical agents and automated rotation on compromise signals.",
    [
        "Agent and human credentials stored together. No rotation. No isolation.",
        "Agent credentials in separate secret store. Manual rotation on schedule.",
        "Automated credential rotation. Automatic rotation on compromise. Hardware-backed for critical agents.",
        "Just-in-time credential issuance. Continuous credential verification. Credential-less authentication (SPIFFE).",
    ],
    [
        "Are agent credentials stored in a separate secret store from human credentials?",
        "Is access to agent credentials subject to a separate approval process?",
        "Are agent credentials automatically rotated? On what schedule?",
        "Is credential rotation automatically triggered on a compromise signal?",
        "Are credentials hardware-backed (HSM, TPM) for critical agents?",
    ],
    [
        "Secret management configuration (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)",
        "Credential access policies (who can read agent credentials)",
        "Credential rotation policy and automation configuration",
        "Credential access audit logs",
        "HSM/TPM configuration (if applicable)",
    ],
    mappings={"ISM": "Guidelines for System Management — credential management",
              "NIST AI RMF": "PROTECT (PR.AC)",
              "Essential Eight": "Multi-factor Authentication — extended to service accounts"},
    tags=["ISM", "NIST", "E8"])

reg("IAM-05", "Just-in-Time (JIT) Access", "IAM",
    "JIT access ensures that agents receive temporary, ephemeral credentials that expire automatically "
    "after the session ends. This prevents credential persistence — an attacker who compromises a tool "
    "gateway cannot replay stale credentials.",
    "Issue session-bound, ephemeral credentials for agents with automatic expiration and the ability "
    "to revoke mid-session on suspicious behaviour detection.",
    [
        "Persistent credentials. No expiration. Credentials valid indefinitely.",
        "Session-bound credentials with fixed expiration (e.g., 1 hour). Manual renewal.",
        "JIT credentials scoped per-session. Automatic expiration. Revocation available.",
        "Dynamic scoping — credentials scoped to specific tools/data per agent task. Continuous authorisation checking.",
    ],
    [
        "Are agent credentials session-bound and automatically expired?",
        "What is the default credential lifetime? Can it be extended, and by whom?",
        "Is there a mechanism for emergency credential extension (e.g., long-running tasks)?",
        "Are JIT credentials scoped to the specific tools and data the agent needs for this session?",
        "Can credentials be revoked mid-session if suspicious behaviour is detected?",
    ],
    [
        "JIT credential configuration (lifespan, scope, renewal policy)",
        "Session management documentation",
        "Credential issuance audit logs",
        "Emergency / break-glass credential procedure",
        "Revocation mechanism configuration and test results",
    ],
    mappings={"NIST AI RMF": "PROTECT (PR.AC)",
              "Essential Eight": "Restrict Administrative Privileges",
              "ISM": "Guidelines for System Management — privileged access management"},
    tags=["NIST", "E8", "ISM"])

reg("IAM-06", "Cross-Session Boundary Enforcement", "IAM",
    "Cross-session boundary enforcement ensures that an agent acting in one session cannot leverage "
    "credentials, context, or access from another session — even if both sessions are for the same "
    "human user. Each session is an independent security context.",
    "Ensure each agent session is an independent security context with no credential or data sharing "
    "across sessions.",
    [
        "Agents share credentials across sessions. No session isolation.",
        "Session-specific credentials. No shared authentication between sessions.",
        "Independent session contexts enforced. Memory scoped per-session. Cross-session access blocked.",
        "Continuous session boundary verification. Automated incident response on boundary violation.",
    ],
    [
        "Are agent credentials scoped to a single session, or can they be reused across sessions?",
        "Can an agent in Session A access data retrieved in Session B (through shared memory or tools)?",
        "Is there a mechanism for agent-to-agent authentication that prevents credential sharing across sessions?",
        "Are session IDs independent and non-predictable?",
        "If the agent maintains persistent memory, is it scoped per-session?",
    ],
    [
        "Session management architecture",
        "Session credential isolation policy",
        "Cross-session access audit logs (should be empty if properly enforced)",
        "Agent memory scoping configuration",
        "Session ID generation and validation configuration",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM06 (Sensitive Information Disclosure — memory scoping)",
              "NIST AI RMF": "PROTECT (PR.AC)"},
    tags=["OWASP", "NIST"])

# ════════════════════════════════════════════
# PILLAR 3: DATA SECURITY
# ════════════════════════════════════════════

reg("DS-01", "Data Classification and Labelling", "DS",
    "Data classification ensures that every piece of data that enters an agentic AI system is "
    "classified according to its sensitivity and handling requirements. Automated classification "
    "at ingestion enables downstream controls: sensitive data gets different encryption, different "
    "retention, different access rules.",
    "Classify all data entering the AI system at ingestion using an automated pipeline that feeds "
    "into downstream encryption, retention, and access controls.",
    [
        "No data classification. All data treated equally.",
        "Manual classification of data inputs. Labels applied at ingestion.",
        "Automated classification pipeline. Labels feed downstream security controls.",
        "Real-time re-classification based on detected content. Continuous accuracy monitoring.",
    ],
    [
        "Is there an automated data classification pipeline for data entering the AI system?",
        "What classification scheme is used (PSPF, ISM, GovERP, proprietary)?",
        "Is data classified before it reaches the model context, or after?",
        "Is classification applied to data in prompts, tool responses, training data, and memory?",
        "Can classification labels be overridden? Who can override them?",
    ],
    [
        "Data classification policy document",
        "Automated classification pipeline configuration and test results",
        "Classification scheme mapping",
        "Data classification audit logs",
        "Integration between classification and downstream controls",
    ],
    mappings={"PSPF": "Information Security — classified information",
              "ISM": "Guidelines for Data Transfers — classification",
              "Privacy Act 1988": "APP 5 — Collection, APP 6 — Use and Disclosure"},
    tags=["PSPF", "ISM", "PRIVACY"])

reg("DS-02", "Inference Data Protection", "DS",
    "Inference data protection ensures that data transmitted between the user, the agent, the model, "
    "and the tool endpoints is encrypted end-to-end and that inference endpoints are secured against "
    "eavesdropping or data extraction.",
    "Encrypt all data in transit between user, agent, model, and tools with TLS 1.3 minimum, and "
    "secure inference endpoints within the organisation's trust boundary for sensitive workloads.",
    [
        "Basic TLS (1.2+). No private endpoints for inference.",
        "TLS 1.3 for all endpoints. Basic logging with manual redaction.",
        "End-to-end encryption. Private inference endpoints for sensitive data. Automated prompt/response redaction.",
        "Client-side encryption keys for cloud inference. Full audit trail of all inference data exposure.",
    ],
    [
        "Are all inference endpoints TLS 1.3 (or equivalent) encrypted?",
        "Is data encrypted in transit between every hop: user → agent → model → tool → response?",
        "Are inference logs encrypted? Who can access them?",
        "Are prompts and responses logged with sensitive data redacted before storage?",
        "Is inference performed within the organisation's trust boundary for sensitive workloads?",
    ],
    [
        "Network architecture diagram showing inference data flows",
        "TLS configuration for all inference endpoints",
        "Inference logging configuration (redaction, encryption, retention)",
        "Cloud provider contract / data processing agreement",
        "VPC / private endpoint configuration",
    ],
    mappings={"Privacy Act 1988": "APP 11 — Security of Personal Information",
              "ISM": "Guidelines for Cryptography",
              "PSPF": "Information Security"},
    tags=["PRIVACY", "ISM", "PSPF"])

reg("DS-03", "Memory Sanitisation", "DS",
    "Memory sanitisation ensures that agents do not persist sensitive, classified, or personal "
    "information beyond the current session, and that any persistent memory store is properly scoped, "
    "encrypted, and subject to retention policies. Persistent agent memory is one of the highest-risk "
    "capabilities because it creates a cross-session data aggregation point.",
    "Prevent persistence of sensitive data across sessions through automated purging, encryption, "
    "per-agent scoping, and cross-session aggregation detection.",
    [
        "Session-bound only. No persistent memory.",
        "Persistent memory with basic retention policy. Manual purging.",
        "Automated memory purging. Per-agent memory scoping. Encryption at rest. Access logging.",
        "Real-time memory access monitoring. Cross-session aggregation detection. Automated DSAR response.",
    ],
    [
        "Does the agent have persistent memory? What data is stored in it?",
        "Is there a data retention policy for agent memory? Is automated purging implemented?",
        "Is sensitive data stored in memory? If so, is it encrypted?",
        "Is memory scoped per-agent, or shared across agents?",
        "Are memory access events logged (read, write, delete)?",
        "Is memory wiped between non-correlated sessions?",
    ],
    [
        "Agent memory architecture",
        "Memory retention policy",
        "Automated purging configuration and logs",
        "Memory encryption configuration",
        "Memory access audit logs",
        "Data subject access request (DSAR) process for agent memory",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM06 (Sensitive Information Disclosure)",
              "Privacy Act 1988": "APP 11 — data security, Notifiable Data Breaches",
              "ISM": "Guidelines for Media — data sanitisation"},
    tags=["OWASP", "PRIVACY", "ISM"])

reg("DS-04", "Data Minimisation", "DS",
    "Data minimisation ensures that only the minimum data required for the agent to perform its task "
    "is exposed to the model, retrieved from data stores, or stored in memory. This is the AI "
    "equivalent of least privilege for data.",
    "Filter data at the retrieval layer (field-level, not document-level) and enforce attribute-based "
    "access control at query time to ensure agents receive only the minimum data required.",
    [
        "Full documents passed to model context. No data filtering at retrieval.",
        "Basic excerpt extraction. Tool response limits configured.",
        "Field-level filtering. ABAC at retrieval. Tool response minimisation enforced.",
        "Dynamic minimisation based on task context and sensitivity. Continuous monitoring of effectiveness.",
    ],
    [
        "Does the RAG pipeline filter data at the field level before passing to the model context?",
        "Are full documents ever passed to the model, or only relevant excerpts?",
        "Is there an attribute-based access control (ABAC) layer at retrieval time?",
        "Are tool responses filtered to return only the data fields the agent needs?",
        "Can an agent request bulk data export, or is minimisation enforced on every request?",
    ],
    [
        "RAG pipeline architecture (focusing on data filtering)",
        "Retrieval access control configuration (ABAC)",
        "Tool response filtering configuration",
        "Data volume monitoring (bytes per query before/after minimisation)",
        "Bulk data access request policy",
    ],
    mappings={"Privacy Act 1988": "APP 3 — Collection of solicited personal information, APP 11",
              "NIST AI RMF": "IDENTIFY (ID.DA)",
              "EU AI Act": "Art. 10(2) — Data Governance"},
    tags=["PRIVACY", "NIST", "EU"])

reg("DS-05", "Training Data Governance", "DS",
    "Training data governance ensures that data used to train or fine-tune AI models is properly "
    "sourced, consented, and retained in compliance with legal and regulatory requirements.",
    "Track training data lineage from source to model, verify consent for personal data, enforce "
    "retention limits, and provide machine unlearning capability.",
    [
        "No training data governance. Data collected without tracking or consent verification.",
        "Basic data lineage for critical models. Manual consent verification.",
        "Automated lineage tracking. Consent verification pipeline. Retention enforcement.",
        "Machine unlearning capability. Continuous training data audit. Third-party governance automatically assessed.",
    ],
    [
        "Is training data lineage tracked from source through preprocessing to training?",
        "Is consent verified for personal data used in training?",
        "Are there retention limits on training datasets? Are they enforced?",
        "Is there a process for removing specific data points from trained models (machine unlearning)?",
        "Are training datasets scanned for sensitive data before use?",
    ],
    [
        "Data lineage tracking system configuration",
        "Consent management records for training data",
        "Training data retention policy and enforcement configuration",
        "Machine unlearning capability (or documented alternative)",
        "Training data scanning results (for sensitive data)",
    ],
    mappings={"Privacy Act 1988": "APP 3 — Collection, APP 5 — Notification, APP 6 — Use/Disclosure",
              "EU AI Act": "Art. 10 — Data Governance",
              "NIST AI RMF": "IDENTIFY (ID.DA)"},
    tags=["PRIVACY", "EU", "NIST"])

reg("DS-06", "Output Validation", "DS",
    "Output validation ensures that model outputs do not leak training data, PII, sensitive business "
    "context, or system prompts. This includes scanning for memorised training examples, PII pattern "
    "matching, and detection of system prompt fragments in outputs.",
    "Scan all model outputs for data leakage (PII, training data, system prompts, credentials) at "
    "the inference proxy layer before delivery to users or systems.",
    [
        "No output validation for data leakage.",
        "Basic PII scanning on model outputs. Manual review of flagged outputs.",
        "Automated output scanning for PII, sensitive data, system prompts, memorised training data. Scanning at application layer.",
        "Real-time output scanning with automated blocking. Training data memorisation testing in CI/CD.",
    ],
    [
        "Are model outputs automatically scanned for data leakage?",
        "What patterns are checked (PII, credit card numbers, API keys, system prompt fragments)?",
        "Is there a mechanism for scanning outputs from tool calls, not just model responses?",
        "Are outputs validated before being displayed to users or written to data stores?",
        "Are model outputs tested for memorisation of training data?",
    ],
    [
        "Output scanning configuration and rules",
        "Data leakage detection alerts and incident records",
        "Tool output scanning configuration",
        "Output validation architecture (inference proxy layer placement)",
        "Memorisation test results for production models",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM02 (Insecure Output Handling)",
              "Privacy Act 1988": "APP 11 — data security",
              "NIST AI RMF": "MEASURE (ME.AD)"},
    tags=["OWASP", "PRIVACY", "NIST"])

# ════════════════════════════════════════════
# PILLAR 4: TOOL AND PIPELINE SECURITY
# ════════════════════════════════════════════

reg("TP-01", "Tool Inventory and Registry", "TP",
    "Every tool that an agent can invoke — APIs, databases, file systems, code executors — must be "
    "registered, versioned, and security-approved before any agent can call it. An unregistered tool "
    "is a blind spot: it cannot be monitored, access-controlled, or included in incident response.",
    "Maintain a central registry of all tools accessible to agents, with security review, versioning, "
    "and integration with the authorisation system.",
    [
        "No tool registry. Tools documented informally or not at all.",
        "Basic tool registry for critical tools. Manual registration.",
        "Central tool registry with full metadata. Automated security review. Integration with authorisation.",
        "Continuous registry scanning for unregistered tools. Automated deregistration of deprecated tools.",
    ],
    [
        "Is there a central tool registry listing all tools available to agents?",
        "Does the registry include metadata (tool owner, version, security review date, data sensitivity)?",
        "Are tools security-reviewed before being added to the registry?",
        "Is there a process for deregistering deprecated or vulnerable tools?",
        "Are agent-to-agent APIs registered as tools in the registry?",
    ],
    [
        "Tool registry system (custom, Backstage, service catalog)",
        "Tool metadata completeness",
        "Tool security review records",
        "Tool registration/deregistration workflow",
        "Agent-to-agent API tool registrations",
    ],
    mappings={"ISM": "Guidelines for Gateways",
              "NIST AI RMF": "IDENTIFY (ID.AM)",
              "SOCI Act": "CIRMP s.4(c)"},
    tags=["ISM", "NIST", "SOCI"])

reg("TP-02", "Tool Access Control", "TP",
    "Tool access control ensures that each agent can only invoke the specific tools it is authorised "
    "to use, and that each tool authenticates the agent — not the human — before accepting commands.",
    "Enforce per-agent tool allow-lists at invocation time with authenticated agent identity and "
    "version-controlled, auditable access policies.",
    [
        "Agents can invoke any registered tool. No per-agent access control.",
        "Per-agent tool allow-lists. Manual assignment.",
        "Tool-level least privilege enforced at invocation time. Agent identity authenticated by tool.",
        "Dynamic tool access assignment based on task and risk. Automated revocation on suspicious activity.",
    ],
    [
        "Is there a per-agent tool allow-list, or do agents have access to all registered tools?",
        "Do tools authenticate the agent identity, or do they trust the identity passed by the agent?",
        "Can an agent invoke a tool that its initiating human cannot access?",
        "Is tool access evaluated at invocation time (not just at configuration time)?",
        "Are tool access policies versioned and auditable?",
    ],
    [
        "Per-agent tool allow-list configuration",
        "Tool authentication configuration",
        "Tool authorisation policy files",
        "Tool access audit logs (allowed and denied invocations)",
        "Tool access revocation process and test results",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM08 (Excessive Agency)",
              "NIST AI RMF": "PROTECT (PR.AC)",
              "Essential Eight": "Application Control — extended to tools"},
    tags=["OWASP", "NIST", "E8"])

reg("TP-03", "API Gateway Security", "TP",
    "API gateway security protects every agent-facing API endpoint with rate limiting, payload "
    "validation, schema enforcement, and audit logging. The agent-to-tool API surface is often "
    "larger and more dynamic than traditional human-facing APIs.",
    "Deploy a gateway between agents and tools that enforces rate limiting, schema validation, "
    "audit logging, and MCP protocol awareness where applicable.",
    [
        "No gateway. Agents call tools directly.",
        "Basic reverse proxy between agents and tools. Rate limiting configured.",
        "Gateway with schema validation, rate limiting, and audit logging. MCP-aware. Fail-closed tested.",
        "Intelligent gateway with dynamic rate limiting, anomaly-based blocking, and auto-discovery.",
    ],
    [
        "Is there a gateway / proxy between agents and external tools?",
        "Does the gateway enforce rate limiting per agent? Per tool?",
        "Is payload validation performed against a known-good schema?",
        "Are all tool invocations logged with agent identity, tool, input summary, and timestamp?",
        "Does the gateway support MCP protocol if MCP-compliant tools are used?",
        "Does the gateway fail closed if the audit destination is unreachable?",
    ],
    [
        "API gateway configuration (rate limits, schemas, logging)",
        "Gateway audit logs",
        "Gateway fail-closed test results",
        "MCP gateway configuration (if applicable)",
        "Tool endpoint registration / discovery configuration",
    ],
    mappings={"ISM": "Guidelines for Gateways, Guidelines for Networking",
              "Essential Eight": "Application Control"},
    tags=["ISM", "E8"])

reg("TP-04", "Tool Output Validation", "TP",
    "Tool output validation ensures that data returned by tools is structurally validated and "
    "sanitised before being fed back into the agent's context. This prevents tool output injection "
    "attacks — a compromised tool returning crafted data that causes the agent to behave outside "
    "intended parameters.",
    "Validate all tool outputs against known-good schemas before passing to agent context, with "
    "content-type verification, size limits, and sandboxed execution for code-generation tools.",
    [
        "No tool output validation. Raw tool responses passed to agent context.",
        "Basic schema validation on tool outputs. Manual review of violations.",
        "Automated schema validation, content-type checking, and sanitisation. Size limits enforced.",
        "Sandbox execution for code-generation tools. Automated blocking of invalid outputs.",
    ],
    [
        "Are tool outputs validated against a known-good schema before entering agent context?",
        "Is content-type validation performed (expecting JSON, receiving script)?",
        "Are tool outputs sanitised before feeding to the model?",
        "Is there a maximum size limit on tool outputs?",
        "Are code-generation tool outputs sandbox-executed before affecting production?",
    ],
    [
        "Tool output validation schemas and rules",
        "Tool output sanitisation configuration",
        "Content-type validation configuration",
        "Tool output size limits",
        "Code sandbox configuration and test results",
        "Tool output validation failure logs",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM02 (Insecure Output Handling)",
              "NIST AI RMF": "MEASURE (ME.AD)"},
    tags=["OWASP", "NIST"])

reg("TP-05", "Pipeline Integrity", "TP",
    "Pipeline integrity ensures that the CI/CD pipelines that build, test, and deploy agent updates "
    "are cryptographically signed, attested, and gated by security validation. An attacker who "
    "compromises the pipeline can deploy a backdoored agent to every production environment.",
    "Sign and attest all CI/CD pipeline runs, enforce security gates before deployment, and store "
    "deployment artifacts in an immutable, integrity-verified registry.",
    [
        "Pipeline exists but no signing, attestation, or security gates.",
        "Pipeline signed. Basic security tests in pipeline. Access controlled.",
        "SLSA Level 2+ attestation. Automated SHIELD-AI control tests as gates. Immutable artifact registry.",
        "SLSA Level 3+ attestation. Continuous pipeline security scanning. Automated rollback on integrity failures.",
    ],
    [
        "Are CI/CD pipeline runs signed and attested (SLSA / in-toto)?",
        "Is there a security gate in the pipeline that requires passing SHIELD-AI control tests before deployment?",
        "Are pipeline configurations version-controlled and reviewed?",
        "Is access to the pipeline restricted and logged?",
        "Are third-party pipeline plugins and extensions security-reviewed?",
    ],
    [
        "CI/CD pipeline configuration files",
        "Pipeline signing / attestation configuration",
        "Security gate configuration (which tests must pass)",
        "Pipeline access control lists and audit logs",
        "Third-party plugin security reviews",
    ],
    mappings={"ISM": "Guidelines for Software Development — CI/CD",
              "NIST AI RMF": "PROTECT (PR.CI)",
              "Essential Eight": "Application Control — restricted execution"},
    tags=["ISM", "NIST", "E8"])

reg("TP-06", "Dependency Scanning", "TP",
    "Dependency scanning ensures that all libraries, models, and tools used by the agent are "
    "continuously scanned for known vulnerabilities, with automated blocking for critical-severity "
    "findings. ML libraries and model registries are frequent attack targets.",
    "Continuously scan all ML libraries, model dependencies, tool SDKs, and container images for "
    "vulnerabilities with automated blocking of critical-severity findings.",
    [
        "No dependency scanning. Dependencies updated ad-hoc.",
        "Basic scanning at build time. Manual review of critical findings.",
        "Continuous scanning. Automated blocking for critical findings. Automated patch deployment.",
        "AI-specific dependency scanning (ML libraries, model registries). Predictive vulnerability assessment.",
    ],
    [
        "Are ML libraries (PyTorch, TensorFlow, transformers) scanned for vulnerabilities?",
        "Are model weights and configurations scanned?",
        "Are tool SDKs and plugins scanned?",
        "Is there automated blocking for critical-severity findings, or just alerts?",
        "Are base container images scanned for the agent runtime?",
    ],
    [
        "Dependency scanning tool configuration",
        "Vulnerability scan reports (ML and non-ML dependencies)",
        "Automated blocking configuration",
        "Dependency update policy and automation",
        "Container image scanning configuration",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM10 (Supply Chain)",
              "ISM": "Guidelines for System Management — vulnerability management",
              "Essential Eight": "Patch Applications, Patch Operating Systems"},
    tags=["OWASP", "ISM", "E8"])

# ════════════════════════════════════════════
# PILLAR 5: MONITORING, LOGGING, AND IR
# ════════════════════════════════════════════

reg("MIR-01", "Agent Activity Logging", "MIR",
    "Agent activity logging captures every action an agent takes in a structured, auditable format "
    "with agent identity, session ID, timestamp, action type, target, result, and a correlation ID "
    "tying events to the initiating human session.",
    "Log all agent actions in structured format with immutable storage, SIEM integration, and "
    "distributed tracing support for multi-agent architectures.",
    [
        "Basic agent logs (start, stop). Limited structure. Stored locally.",
        "Structured audit logs for all agent actions. Centralised storage. 30-day retention.",
        "Immutable logs. Correlation IDs across multi-agent chains. SIEM integration. Log integrity verification.",
        "Real-time log streaming. Automated log anomaly detection. Extended retention for forensic readiness.",
    ],
    [
        "Are all agent actions logged (every tool call, data access, decision, error)?",
        "Is each log entry structured with agent ID, session ID, timestamp, action type, target, result?",
        "Is there a correlation ID that ties agent actions to the initiating human session?",
        "Are logs stored in an immutable append-only store?",
        "Are agent logs integrated with existing SIEM / logging infrastructure?",
    ],
    [
        "Log schema definition (agent event structure)",
        "Agent telemetry pipeline configuration",
        "Log storage configuration (immutability, retention)",
        "Log integrity verification mechanism",
        "SIEM integration configuration",
        "Log coverage report (are all agents logging?)",
    ],
    mappings={"SOCI Act": "s.30B(5)(a) — record-keeping",
              "APRA CPS 234": "s.3(c) — information security capability",
              "ISM": "Guidelines for System Monitoring"},
    tags=["SOCI", "CPS234", "ISM"])

reg("MIR-02", "Behavioural Anomaly Detection", "MIR",
    "Behavioural anomaly detection establishes per-agent and per-agent-class behaviour baselines "
    "and alerts when an agent deviates. Unlike traditional anomaly detection (known attack signatures), "
    "agent behavioural detection learns what 'normal' looks like for each agent.",
    "Establish per-agent and per-agent-class behaviour baselines for tool usage, data access, memory "
    "access, and decision patterns, with automated alerting on deviation.",
    [
        "No anomaly detection. Signature-based monitoring only (if any).",
        "Basic per-agent baselines. Manual alert review.",
        "Per-agent and per-class baselines. Automated alerting. Integration with SOC. Regular tuning.",
        "Continuous baseline learning. Cross-agent anomaly correlation. Predictive anomaly detection.",
    ],
    [
        "Are per-agent behaviour baselines established for each agent?",
        "Are per-agent-class baselines established (what is normal for this type of agent)?",
        "What deviation thresholds trigger alerts? Are they tuned per agent?",
        "Are memory access patterns monitored (agent reading records it should not access)?",
        "Are tool invocation patterns monitored (unusual tool, frequency, chain)?",
    ],
    [
        "Behavioural baseline definitions",
        "Anomaly detection rule configuration",
        "Recent anomaly alerts and their disposition",
        "Baseline tuning / calibration records",
        "Memory access monitoring configuration",
    ],
    mappings={"NIST AI RMF": "DETECT (DE.CM)",
              "ISM": "Guidelines for System Monitoring"},
    tags=["NIST", "ISM"])

reg("MIR-03", "Prompt Audit Log", "MIR",
    "The prompt audit log captures sanitised prompt/response pairs for forensic analysis while "
    "protecting sensitive data. This is the AI-equivalent of database query logging — it enables "
    "investigators to reconstruct what the agent was asked and what it did.",
    "Log prompt/response pairs with automated sensitive data redaction, tiered retention, and "
    "SIEM integration for forensic analysis.",
    [
        "No prompt logging.",
        "Basic prompt/response logging. Manual review. Short retention.",
        "Automated redaction. Tiered retention (full → redacted). SIEM integration.",
        "Real-time prompt scanning for security events. Automated incident triggering from prompt analysis.",
    ],
    [
        "Are prompt/response pairs logged with agent identity and session ID?",
        "Is sensitive data automatically redacted before long-term storage?",
        "Is there a mechanism to recover redacted data for incident investigation?",
        "How long are full (unredacted) prompts retained? Redacted prompts?",
        "Are prompt logs included in the data retention and disposal schedule?",
    ],
    [
        "Prompt logging configuration (redaction rules, retention periods)",
        "Prompt log storage architecture",
        "Redaction recovery mechanism (for legitimate IR use)",
        "Prompt log retention policy",
        "Prompt log review process documentation",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM01 (Prompt Injection — detection)",
              "NIST AI RMF": "DETECT (DE.AE)",
              "EU AI Act": "Art. 12 — Transparency"},
    tags=["OWASP", "NIST", "EU"])

reg("MIR-04", "Incident Response Playbooks", "MIR",
    "Incident response playbooks define AI-specific procedures for detecting, containing, and "
    "recovering from security incidents involving agentic AI. These address scenarios general IR "
    "does not cover: prompt injection containment, model rollback, tool revocation, and "
    "code-generation attack containment.",
    "Develop and maintain AI-specific IR playbooks covering prompt injection, model compromise, "
    "tool abuse, and code-generation attacks, tested through regular tabletop exercises.",
    [
        "No AI-specific IR playbooks. General IR procedures applied ad-hoc.",
        "Basic AI-specific playbooks documented. Manual response.",
        "Comprehensive playbooks for all AI incident types. SOAR integration. Regular tabletop exercises.",
        "Automated playbook execution for known incident types. Continuous playbook improvement from threat intelligence.",
    ],
    [
        "Are there AI-specific IR playbooks, or does the organisation rely on general IR procedures?",
        "What incident scenarios are covered (prompt injection, data exfiltration, model compromise, tool abuse, code-generation attack)?",
        "Are playbooks tested (tabletop exercises, simulations)?",
        "Are playbooks integrated with SOAR for automated response?",
        "Is there a process for post-incident review and playbook improvement?",
    ],
    [
        "AI-specific IR playbook documents",
        "Tabletop exercise records and findings",
        "SOAR playbook configuration",
        "Post-incident review records",
        "Playbook update history",
    ],
    mappings={"NIST AI RMF": "RESPOND (RS.RP)",
              "SOCI Act": "CIRMP — incident response",
              "APRA CPS 234": "s.3(c) — incident response capability"},
    tags=["NIST", "SOCI", "CPS234"])

reg("MIR-05", "Mandatory Reporting Integration", "MIR",
    "Mandatory reporting integration ensures that the organisation can meet regulatory incident "
    "reporting deadlines — SOCI Act 12/72-hour windows, APRA CPS 234 72-hour notification, "
    "and Privacy Act Notifiable Data Breaches reporting.",
    "Integrate incident detection with automated regulatory reporting triggers for SOCI Act, APRA "
    "CPS 234, and Notifiable Data Breaches, with pre-populated report templates.",
    [
        "No automated reporting. Incidents reported manually (if at all).",
        "Manual incident reports using templates. Deadlines tracked in spreadsheets.",
        "Automated incident detection triggers pre-populated reports. Escalation workflows active.",
        "Fully automated reporting lifecycle. Continuous compliance monitoring with regulator dashboards.",
    ],
    [
        "Are SOCI Act/APRA/NDB reporting triggers integrated with agent monitoring?",
        "Are incident report templates pre-populated with agent data?",
        "Is there an escalation workflow that notifies the designated reporting officer?",
        "Is the reporting integration tested (not just documented)?",
        "Are reporting deadlines tracked and alerted to compliance teams?",
    ],
    [
        "Reporting trigger configuration (which events trigger which reports)",
        "Incident report templates",
        "Escalation workflow documentation and test results",
        "Reporting deadline tracking configuration",
        "Historical incident report repository",
    ],
    mappings={"SOCI Act": "s.30B — mandatory incident reporting (12h critical, 72h other)",
              "APRA CPS 234": "s.3(c) — 72-hour notification",
              "Privacy Act 1988": "Notifiable Data Breaches scheme"},
    tags=["SOCI", "CPS234", "PRIVACY"])

reg("MIR-06", "Forensic Readiness", "MIR",
    "Forensic readiness ensures that the organisation can reconstruct a full agent session — every "
    "prompt, tool call, data access, decision, and response — for post-incident investigation. Logs "
    "are written to immutable, append-only storage with integrity guarantees.",
    "Maintain immutable, verifiable logs with full session reconstruction capability for all agents, "
    "including support for multi-agent chain reconstruction.",
    [
        "Logs stored in standard database. Can be modified. Retention ad-hoc.",
        "Logs in append-only storage. Basic retention policy.",
        "Immutable logs with integrity verification. Full session reconstruction capability. Multi-agent chain reconstruction.",
        "Real-time forensic readiness verification. Automated forensic data extraction. Continuous integrity monitoring.",
    ],
    [
        "Are logs written to immutable, append-only storage?",
        "Is log integrity verifiable (cannot be modified or deleted without detection)?",
        "Can a full agent session be reconstructed (every action in sequence)?",
        "For multi-agent chains, can the full chain be reconstructed?",
        "Are logs retained for the regulatory-required period (at minimum)?",
    ],
    [
        "Log storage architecture (immutability, append-only)",
        "Log integrity verification mechanism",
        "Session reconstruction capability demonstration",
        "Log retention policy (meeting regulatory minimums)",
        "Forensic data extraction procedure",
    ],
    mappings={"NIST AI RMF": "RECOVER (RC.RP)",
              "ISM": "Guidelines for Cyber Security Incidents — forensic readiness",
              "SOCI Act": "CIRMP — record-keeping"},
    tags=["NIST", "ISM", "SOCI"])

# ════════════════════════════════════════════
# PILLAR 6: GOVERNANCE AND RISK MANAGEMENT
# ════════════════════════════════════════════

reg("GRM-01", "AI Governance Body", "GRM",
    "The AI governance body is a chartered committee with the authority to approve agentic AI "
    "deployments, define acceptable use boundaries, and oversee the organisation's AI security "
    "posture. Membership must include CISO, CRO, General Counsel, data owner, and AI lead.",
    "Establish and charter an AI governance body with cross-functional membership (CISO, CRO, "
    "GC, data owner, AI lead) and defined decision authority over agentic AI deployments.",
    [
        "No AI governance body. AI decisions made by individual teams.",
        "Informal AI governance group meets ad-hoc. No formal charter.",
        "Chartered AI governance body with defined terms of reference. Regular meetings. Documented decisions.",
        "AI governance body with delegated authority. Independent audit of decisions. Cross-entity governance.",
    ],
    [
        "Is there a chartered AI governance body with defined terms of reference?",
        "Who sits on the committee (CISO, CRO, GC, data owner, AI lead)?",
        "What decisions require committee approval?",
        "How often does the committee meet?",
        "Are committee decisions documented and tracked?",
    ],
    [
        "AI governance body charter and terms of reference",
        "Committee meeting minutes and decision records",
        "Committee membership list and review schedule",
        "Escalation procedure documentation",
        "Decision implementation tracking",
    ],
    mappings={"APRA CPS 234": "s.2 — Board accountability",
              "PSPF": "Security Governance — Policy 1",
              "Privacy Act 1988": "APP 1 — accountability"},
    tags=["CPS234", "PSPF", "PRIVACY"])

reg("GRM-02", "AI Risk Register", "GRM",
    "The AI risk register is a distinct register that captures AI-specific risks using a dedicated "
    "threat taxonomy covering model-level, tool-level, data-level, identity-level, and pipeline-level "
    "risks. Each risk is assessed, owned, and tracked to resolution.",
    "Maintain a dedicated AI risk register using a threat taxonomy that covers model, tool, data, "
    "identity, and pipeline risks, with defined owners, assessment methodology, and review cadence.",
    [
        "No AI risk register. AI risks captured informally or not at all.",
        "Basic AI risk register with manual entries. Siloed from enterprise risk register.",
        "AI-specific risk taxonomy in enterprise risk register. Regular review cycle. Formal risk acceptance.",
        "Continuous AI risk assessment. Automated risk scoring from control monitoring. Integrated with ERM.",
    ],
    [
        "Is there a dedicated AI risk register or AI-specific section in the enterprise risk register?",
        "Does the AI risk taxonomy cover model, tool, data, identity, and pipeline risks?",
        "Are risks assessed using a defined methodology (likelihood × impact)?",
        "Are risk owners assigned to each AI risk?",
        "Is there a process for accepting AI risks with documented rationale and expiry?",
    ],
    [
        "AI risk register entries",
        "AI risk taxonomy documentation",
        "Risk assessment methodology",
        "Risk owner assignments",
        "Risk review schedule and records",
        "Risk acceptance records with rationale and expiry",
    ],
    mappings={"NIST AI RMF": "GOVERN (GV.RM)",
              "SOCI Act": "CIRMP — risk management",
              "APRA CPS 234": "s.3(a) — risk assessment"},
    tags=["NIST", "SOCI", "CPS234"])

reg("GRM-03", "Ethical Use Policy", "GRM",
    "The ethical use policy defines what agents are allowed and not allowed to do, what level of "
    "autonomy they may have based on risk tier, and what transparency obligations apply. It sets "
    "boundaries that technical controls then enforce.",
    "Document and enforce an ethical use policy that classifies agents by risk tier, defines "
    "autonomy boundaries per tier, and specifies transparency obligations.",
    [
        "No ethical use policy. Agents deployed without defined boundaries.",
        "Draft policy document. Basic risk classification. Manual compliance monitoring.",
        "Approved policy with risk-tiered autonomy. Automated compliance monitoring. Regular policy review.",
        "Continuous compliance verification. Automated enforcement at tool gateway. Policy improvement from experience.",
    ],
    [
        "Is there an approved ethical use policy for agentic AI?",
        "Does the policy define acceptable use boundaries (what agents can and cannot do)?",
        "Are agents classified into risk tiers with corresponding autonomy levels?",
        "Does the policy specify transparency obligations (disclosure that an interaction involves an AI)?",
        "Are policy violations investigated and remediated?",
    ],
    [
        "AI ethical use policy document",
        "Agent risk classification methodology and classifications",
        "Policy compliance monitoring configuration",
        "Policy violation records and remediation",
        "Policy review schedule and update history",
    ],
    mappings={"EU AI Act": "Art. 14 — Human Oversight",
              "NIST AI RMF": "GOVERN (GV.OC)",
              "Privacy Act 1988": "APP 1 — accountability"},
    tags=["EU", "NIST", "PRIVACY"])

reg("GRM-04", "Third-Party AI Risk Management", "GRM",
    "Third-party AI risk management ensures that external model providers, tool providers, and AI "
    "infrastructure vendors are assessed against security requirements, contractually bound to "
    "maintain controls, and subject to right-to-audit provisions.",
    "Assess and monitor third-party AI providers for security controls, with contractual security "
    "requirements and right-to-audit provisions in all AI-related procurement.",
    [
        "No third-party AI risk assessment. Providers used without evaluation.",
        "Basic vendor assessments for model providers. Contractual requirements in some contracts.",
        "Comprehensive vendor assessment programme for all AI providers. Right-to-audit. Ongoing monitoring.",
        "Continuous vendor security monitoring. Automated vendor risk scoring. Vendor decommissioning playbooks exercised.",
    ],
    [
        "Are model providers subject to a vendor security assessment?",
        "Are tool providers subject to a vendor security assessment?",
        "Does the assessment cover data protection, incident response, and shared responsibility?",
        "Are contractual controls in place (security requirements in contracts)?",
        "Is there a right-to-audit clause in contracts with AI providers?",
    ],
    [
        "Third-party AI vendor risk assessments",
        "Contractual security requirements (SOWs, MSAs)",
        "Right-to-audit clauses",
        "Vendor monitoring records (incidents, changes)",
        "Shared responsibility model documentation",
    ],
    mappings={"OWASP LLM Top 10 v2": "LLM10 (Supply Chain)",
              "NIST AI RMF": "IDENTIFY (ID.SC)",
              "ISM": "Guidelines for Procurement and Outsourcing",
              "EU AI Act": "Art. 28 — Third Parties"},
    tags=["OWASP", "NIST", "ISM", "EU"])

reg("GRM-05", "Regulatory Mapping and Compliance Reporting", "GRM",
    "Regulatory mapping ensures that every SHIELD-AI control is mapped to the regulatory frameworks "
    "the organisation must comply with, and that compliance status is reported on a regular cadence. "
    "This transforms compliance from a point-in-time audit exercise to a continuous process.",
    "Maintain an automated mapping of SHIELD-AI controls to applicable regulatory frameworks with "
    "continuous compliance monitoring and regular reporting.",
    [
        "No regulatory mapping. Compliance assessed informally.",
        "Manual mapping to primary regulatory frameworks. Periodic compliance reports.",
        "Automated regulatory mapping. Continuous compliance monitoring. Quarterly reporting.",
        "Real-time compliance dashboard. Automated impact assessment of regulatory changes. Continuous audit readiness.",
    ],
    [
        "Is there a documented mapping of SHIELD-AI controls to applicable regulatory frameworks?",
        "Is the mapping maintained when frameworks are updated?",
        "Are compliance reports generated automatically or manually?",
        "Are compliance findings tracked to remediation?",
        "Is there an automated compliance dashboard available to stakeholders?",
    ],
    [
        "Regulatory mapping matrix",
        "Framework version tracking (which ISM edition, which E8 baseline)",
        "Compliance report templates and recent reports",
        "Finding tracking and remediation records",
        "Compliance dashboard configuration",
        "Regulatory change monitoring configuration",
    ],
    mappings={"APRA CPS 234": "s.2 — Board reporting",
              "NIST AI RMF": "GOVERN (GV.OV)",
              "ISM": "Guidelines for Cyber Security Documentation"},
    tags=["CPS234", "NIST", "ISM"])

reg("GRM-06", "Board and Executive Reporting", "GRM",
    "Board and executive reporting provides a standardised dashboard giving the Board and executive "
    "team visibility into the organisation's AI security posture — maturity scores per pillar, open "
    "findings, regulatory compliance status, and risk acceptances — designed for non-technical audiences.",
    "Provide a standardised executive dashboard showing pillar maturity scores, open findings, "
    "regulatory compliance status, and risk acceptances, refreshed automatically.",
    [
        "No AI security reporting to executives.",
        "Manual AI security report prepared for executive meetings. Ad-hoc content.",
        "Automated compliance dashboard. Per-pillar maturity scores. Regular Board reporting.",
        "Real-time executive dashboard. Predictive risk scoring. Automated Board reporting with trend analysis.",
    ],
    [
        "Is there a standardised AI security dashboard for executives?",
        "Does the dashboard show maturity scores per pillar?",
        "Are open findings tracked with severity, owner, and status?",
        "Is regulatory compliance status visible (which frameworks are we compliant with?)",
        "Is the dashboard refreshed automatically or manually?",
    ],
    [
        "Executive dashboard configuration",
        "Recent dashboard snapshots or reports",
        "Finding tracking records",
        "Risk acceptance register",
        "Board reporting schedule and recent reports",
    ],
    mappings={"APRA CPS 234": "s.2 — Board accountability and reporting",
              "NIST AI RMF": "GOVERN (GV.OV)"},
    tags=["CPS234", "NIST"])


# ──────────────────────────────────────────────
# OUTPUT GENERATION
# ──────────────────────────────────────────────

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def build_schema():
    """Build the full SHIELD-AI control schema dictionary."""
    schema = {
        "meta": {
            "framework": "SHIELD-AI",
            "version": FRAMEWORK_VERSION,
            "date": FRAMEWORK_DATE,
            "description": "Sovereign Australian Framework for Secure Agentic AI Deployment",
            "pillar_count": len(PILLARS),
            "control_count": len(CONTROLS),
        },
        "pillars": {
            pid: {
                "id": pid,
                "name": name,
                "order": PILLAR_ORDER.index(pid) + 1,
                "control_count": sum(1 for c in CONTROLS.values() if c["pillar"] == pid),
                "control_ids": sorted([c["id"] for c in CONTROLS.values() if c["pillar"] == pid]),
            }
            for pid, name in PILLARS.items()
        },
        "controls": dict(sorted(CONTROLS.items())),
    }

    # Add pillar references to each control
    for cid, ctrl in schema["controls"].items():
        ctrl["pillar_name"] = PILLARS[ctrl["pillar"]]

    return schema


def generate_json(output_path=None):
    """Generate the SHIELD-AI control schema JSON file."""
    schema = build_schema()
    if output_path is None:
        output_path = os.path.join(REPO_ROOT, "assets", "shield-ai-control-schema.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2, sort_keys=False)
    size = os.path.getsize(output_path)
    print(f"Generated: {output_path} ({size:,} bytes, {len(CONTROLS)} controls)")
    return output_path


def generate_rego_stubs(output_dir=None):
    """Generate Rego policy stubs for each control."""
    if output_dir is None:
        output_dir = os.path.join(REPO_ROOT, "policies")

    os.makedirs(output_dir, exist_ok=True)
    count = 0

    for cid in sorted(CONTROLS.keys()):
        ctrl = CONTROLS[cid]
        safe_name = ctrl["title"].lower().replace(" ", "_").replace("-", "_").replace(",", "").replace("(", "").replace(")", "").replace("&", "and")
        filename = f"shield_ai_{ctrl['pillar'].lower()}_{cid.lower()}.rego"
        filepath = os.path.join(output_dir, filename)

        package_name = f"shield_ai.{ctrl['pillar'].lower()}.{safe_name[:30]}"

        rego_code = f"""package {package_name}

# SHIELD-AI {cid}: {ctrl['title']}
# Pillar: {ctrl['pillar']} — {PILLARS[ctrl['pillar']]}
#
# {ctrl['objective']}
#
# Maturity indicators:
#   L1: {ctrl['maturity']['L1']}
#   L2: {ctrl['maturity']['L2']}
#   L3: {ctrl['maturity']['L3']}
#   L4: {ctrl['maturity']['L4']}
#
# Regulatory mappings:
{chr(10).join(f'#   {k}: {v}' for k, v in ctrl.get('regulatory_mappings', {}).items())}

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {{
#     agent := input.agents[_]
#     not agent.{ctrl['pillar'].lower()}_{cid.lower().replace('-', '_')}
#     msg := sprintf("{cid} violation: agent %v does not meet control requirements", [agent.id])
# }}
"""

        with open(filepath, "w") as f:
            f.write(rego_code)
        count += 1

    print(f"Generated: {count} Rego policy stubs in {output_dir}/")
    return output_dir


def main():
    generate_json()

    if "--rego" in sys.argv:
        generate_rego_stubs()

    # Summary
    schema = build_schema()
    print()
    print(f"SHIELD-AI Control Schema v{FRAMEWORK_VERSION}")
    print(f"{'─'*50}")
    for pid in PILLAR_ORDER:
        p = schema["pillars"][pid]
        print(f"  {pid}: {p['name']:<40s} {p['control_count']:>2d} controls")
    print(f"{'─'*50}")
    print(f"  Total: {schema['meta']['control_count']} controls across {schema['meta']['pillar_count']} pillars")


if __name__ == "__main__":
    main()
