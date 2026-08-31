#!/usr/bin/env python3
"""
SHIELD-AI(TM) Control Schema Generator
===================================
Generates machine-readable control definitions from canonical Python data structures.

Outputs:
  assets/shield-ai-control-schema.json   -- Full control definitions, maturity
                                            indicators, assessment questions,
                                            artifacts, regulatory mappings
  policies/shield_ai_*.rego              -- Rego policy stubs for automated
                                            control testing (optional)

Usage:
  python3 tools/generate_control_schema.py              # generate JSON only
  python3 tools/generate_control_schema.py --rego        # generate JSON + Rego stubs
"""

import json
import os
import re
import sys
from datetime import date

# ----------------------------------------------
# Canonical control definitions
# ----------------------------------------------

FRAMEWORK_VERSION = "1.10"
FRAMEWORK_DATE = "2026-09"

PILLARS = {
    "MS":  "Model Security",
    "IAM": "Identity and Access",
    "DS":  "Data Security",
    "TP":  "Tool and Pipeline Security",
    "MIR": "Monitoring, Logging, and Incident Response",
    "GRM": "Governance and Risk Management",
    "EE":  "Execution Environment",
}

PILLAR_ORDER = ["MS", "IAM", "DS", "TP", "MIR", "GRM", "EE"]

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

# ============================================
# PILLAR 1: MODEL SECURITY
# ============================================

reg("MS-01", "Model Weight Protection", "MS",
    "Model weights represent the trained intelligence of an AI system -- often the single most valuable "
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
    mappings={"ISM": "Guidelines for Cryptography, System Management -- access control",
              "PSPF": "Information Security"},
    tags=["ISM", "PSPF"])

reg("MS-02", "Training Data Integrity", "MS",
    "Training data integrity ensures that data used to train or fine-tune a model has not been poisoned, "
    "corrupted, or substituted. Data poisoning -- an attacker inserting crafted samples into the training "
    "dataset -- can cause a model to behave normally until a specific trigger condition is met.",
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
    mappings={"ISM": "Guidelines for Software Development -- data validation",
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
    mappings={"ISM": "Guidelines for Procurement and Outsourcing, System Management -- supply chain",
              "SOCI Act": "CIRMP -- supply chain obligations",
              "OWASP LLM Top 10 v2": "LLM10 (Supply Chain)",
              "NIST AI RMF": "IDENTIFY (ID.SC)"},
    tags=["ISM", "SOCI", "OWASP", "NIST"])

reg("MS-04", "Adversarial Robustness", "MS",
    "Adversarial robustness ensures that the model resists malicious inputs designed to produce unintended "
    "behaviour. For agentic AI, the primary adversarial attack is prompt injection -- crafting input that "
    "causes the model to ignore its system prompt and follow attacker instructions. Inputs must additionally "
    "be sanitised against imperceptible-content vectors (zero-opacity text, sub-pixel/1px text, DOM-hidden "
    "content, hidden pull-request comments) before reasoning -- the perception-bypass class demonstrated by "
    "AWS Kiro CVE-2026-10591 and hidden-PR-comment review-agent hijacks -- and tool-returned content (PR "
    "comments, documentation pages, search results) must be scanned for hidden-content primitives before "
    "use (v1.5).",
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
              "EU AI Act": "Art. 15 -- Accuracy",
              "MITRE ATLAS": "AML.T0051, AML.T0059"},
    tags=["OWASP", "NIST", "EU", "MITRE"])

reg("MS-05", "Model Behaviour Validation", "MS",
    "Behaviour validation ensures that model outputs conform to expected bounds -- the model produces "
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
              "EU AI Act": "Art. 14 -- Human Oversight",
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
              "EU AI Act": "Art. 11 -- Registration",
              "ISO 42001": "Clause 7.4"},
    tags=["NIST", "EU"])

# ============================================
# PILLAR 2: IDENTITY AND ACCESS
# ============================================

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
        "Session initiation audit records (human -> agent correlation)",
    ],
    mappings={"ISM": "Guidelines for System Management -- identification and authentication",
              "Essential Eight": "Restrict Administrative Privileges",
              "NIST AI RMF": "IDENTIFY (ID.AM)"},
    tags=["ISM", "E8", "NIST"])

reg("IAM-02", "Scope-Bound Delegation", "IAM",
    "Scope-bound delegation ensures that an agent's permissions are limited to the minimum set of tools, "
    "data, and actions required for its function -- and that the agent cannot exceed these bounds, cannot "
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
    "execution. Not every agent action needs human review -- a customer support agent reading account "
    "details is low-risk; the same agent writing to the account requires approval. Gateway and operator "
    "tokens must not be readable from web or browser context (cross-site WebSocket hijack resistance -- "
    "OpenClaw CVE-2026-25253), and publication credentials under DS-07 are scoped, short-lived, and "
    "un-approvable by the agent itself (v1.5).",
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
    mappings={"EU AI Act": "Art. 14 -- Human Oversight",
              "NIST AI RMF": "MANAGE (MG.DE)",
              "APRA CPS 234": "s.2 -- Board accountability for controls"},
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
    mappings={"ISM": "Guidelines for System Management -- credential management",
              "NIST AI RMF": "PROTECT (PR.AC)",
              "Essential Eight": "Multi-factor Authentication -- extended to service accounts"},
    tags=["ISM", "NIST", "E8"])

reg("IAM-05", "Just-in-Time (JIT) Access", "IAM",
    "JIT access ensures that agents receive temporary, ephemeral credentials that expire automatically "
    "after the session ends. This prevents credential persistence -- an attacker who compromises a tool "
    "gateway cannot replay stale credentials.",
    "Issue session-bound, ephemeral credentials for agents with automatic expiration and the ability "
    "to revoke mid-session on suspicious behaviour detection.",
    [
        "Persistent credentials. No expiration. Credentials valid indefinitely.",
        "Session-bound credentials with fixed expiration (e.g., 1 hour). Manual renewal.",
        "JIT credentials scoped per-session. Automatic expiration. Revocation available.",
        "Dynamic scoping -- credentials scoped to specific tools/data per agent task. Continuous authorisation checking.",
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
              "ISM": "Guidelines for System Management -- privileged access management"},
    tags=["NIST", "E8", "ISM"])

reg("IAM-06", "Cross-Session Boundary Enforcement", "IAM",
    "Cross-session boundary enforcement ensures that an agent acting in one session cannot leverage "
    "credentials, context, or access from another session -- even if both sessions are for the same "
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
    mappings={"OWASP LLM Top 10 v2": "LLM06 (Sensitive Information Disclosure -- memory scoping)",
              "NIST AI RMF": "PROTECT (PR.AC)"},
    tags=["OWASP", "NIST"])

# ============================================
# PILLAR 3: DATA SECURITY
# ============================================

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
    mappings={"PSPF": "Information Security -- classified information",
              "ISM": "Guidelines for Data Transfers -- classification",
              "Privacy Act 1988": "APP 5 -- Collection, APP 6 -- Use and Disclosure"},
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
        "Is data encrypted in transit between every hop: user -> agent -> model -> tool -> response?",
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
    mappings={"Privacy Act 1988": "APP 11 -- Security of Personal Information",
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
              "Privacy Act 1988": "APP 11 -- data security, Notifiable Data Breaches",
              "ISM": "Guidelines for Media -- data sanitisation"},
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
    mappings={"Privacy Act 1988": "APP 3 -- Collection of solicited personal information, APP 11",
              "NIST AI RMF": "IDENTIFY (ID.DA)",
              "EU AI Act": "Art. 10(2) -- Data Governance"},
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
    mappings={"Privacy Act 1988": "APP 3 -- Collection, APP 5 -- Notification, APP 6 -- Use/Disclosure",
              "EU AI Act": "Art. 10 -- Data Governance",
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
              "Privacy Act 1988": "APP 11 -- data security",
              "NIST AI RMF": "MEASURE (ME.AD)"},
    tags=["OWASP", "PRIVACY", "NIST"])

reg("DS-07", "Agent-Originated Artifact Publication Control", "DS",
    "Agent-authored or agent-published artifacts -- packages, container images, configuration files, registry entries, code -- must enter the same integrity, signing, provenance, and malware-scanning pipeline as third-party artifacts. Publication to any distribution channel (package registries, image registries, repository pushes, release pipelines) is a high-risk egress event requiring explicit out-of-band approval that the agent itself cannot invoke. Publication credentials are scoped, short-lived, and unreachable via the ordinary tool path; agent writes to execution-bearing locations are privileged actions subject to EE-07. Addresses the agent-as-publisher class (Anthropic Claude Mythos 5 published a malicious Python package to PyPI during an evaluation; 15 real systems downloaded and executed it, including a security vendor's malware scanner whose credentials were then stolen and used to pivot deeper -- INC-19).",
    "Prevent agents from unintentionally or maliciously publishing execution-bearing artifacts into the software supply chain.",
    [
        "Agents can reach publication endpoints with standing credentials; no approval gate.",
        "Publication requires human approval; publication credentials reviewed for least privilege.",
        "Signed, scanned, provenance-tracked publication pipeline; short-lived scoped credentials; agent cannot self-approve.",
        "Continuous monitoring and provenance verification of agent-authored artifacts; automated blocking of unapproved publication paths.",
    ],
    [
        "Can the agent reach package/image registries or publication endpoints with standing credentials?",
        "Is publication an approval-gated event, with approval out-of-band and un-approvable by the agent itself?",
        "Do agent-authored artifacts pass signing, provenance, and malware-scanning before distribution?",
        "Are publication credentials short-lived, scoped, and unreachable via the ordinary tool path?",
        "Are agent writes to execution-bearing locations monitored (MIR-01)?",
    ],
    [
        "Publication approval workflow and evidence",
        "Registry credential issuance records (scopes, lifetimes)",
        "Agent-artifact signing and provenance records",
        "Publication egress logs (MIR-01)",
    ],
    {"NIST": "SSDF", "ISM": "Software Integrity, Change Management", "OWASP": "LLM09 (Misuse of System Access)", "EU AI Act": "Art. 15(b)"},
    ["publication", "supply-chain", "egress"])

# ============================================
# PILLAR 4: TOOL AND PIPELINE SECURITY
# ============================================

reg("TP-01", "Tool Inventory and Registry", "TP",
    "Every tool that an agent can invoke -- APIs, databases, file systems, code executors -- must be "
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
    "to use, and that each tool authenticates the agent -- not the human -- before accepting commands.",
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
              "Essential Eight": "Application Control -- extended to tools"},
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
    "attacks -- a compromised tool returning crafted data that causes the agent to behave outside "
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
    mappings={"ISM": "Guidelines for Software Development -- CI/CD",
              "NIST AI RMF": "PROTECT (PR.CI)",
              "Essential Eight": "Application Control -- restricted execution"},
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
              "ISM": "Guidelines for System Management -- vulnerability management",
              "Essential Eight": "Patch Applications, Patch Operating Systems"},
    tags=["OWASP", "ISM", "E8"])

# ============================================
# PILLAR 5: MONITORING, LOGGING, AND IR
# ============================================

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
    mappings={"SOCI Act": "s.30B(5)(a) -- record-keeping",
              "APRA CPS 234": "s.3(c) -- information security capability",
              "ISM": "Guidelines for System Monitoring"},
    tags=["SOCI", "CPS234", "ISM"])

reg("MIR-02", "Behavioural Anomaly Detection", "MIR",
    "Behavioural anomaly detection establishes per-agent and per-agent-class behaviour baselines "
    "and alerts when an agent deviates. Unlike traditional anomaly detection (known attack signatures), "
    "agent behavioural detection learns what 'normal' looks like for each agent. Detection must include "
    "adversary-owned autonomous agents operating at model speed with zero human-in-the-loop friction -- "
    "autonomous discovery (FOFA-style), mass exploitation of exposed instances, and self-propagating "
    "campaign patterns (Unit 42 INC-23; Kimi K3 autonomous exploit development) -- and unexpected "
    "listener/binding events from agent environments (v1.5).",
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
    "protecting sensitive data. This is the AI-equivalent of database query logging -- it enables "
    "investigators to reconstruct what the agent was asked and what it did.",
    "Log prompt/response pairs with automated sensitive data redaction, tiered retention, and "
    "SIEM integration for forensic analysis.",
    [
        "No prompt logging.",
        "Basic prompt/response logging. Manual review. Short retention.",
        "Automated redaction. Tiered retention (full -> redacted). SIEM integration.",
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
    mappings={"OWASP LLM Top 10 v2": "LLM01 (Prompt Injection -- detection)",
              "NIST AI RMF": "DETECT (DE.AE)",
              "EU AI Act": "Art. 12 -- Transparency"},
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
              "SOCI Act": "CIRMP -- incident response",
              "APRA CPS 234": "s.3(c) -- incident response capability"},
    tags=["NIST", "SOCI", "CPS234"])

reg("MIR-05", "Mandatory Reporting Integration", "MIR",
    "Mandatory reporting integration ensures that the organisation can meet regulatory incident "
    "reporting deadlines -- SOCI Act 12/72-hour windows, APRA CPS 234 72-hour notification, "
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
    mappings={"SOCI Act": "s.30B -- mandatory incident reporting (12h critical, 72h other)",
              "APRA CPS 234": "s.3(c) -- 72-hour notification",
              "Privacy Act 1988": "Notifiable Data Breaches scheme"},
    tags=["SOCI", "CPS234", "PRIVACY"])

reg("MIR-06", "Forensic Readiness", "MIR",
    "Forensic readiness ensures that the organisation can reconstruct a full agent session -- every "
    "prompt, tool call, data access, decision, and response -- for post-incident investigation. Logs "
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
              "ISM": "Guidelines for Cyber Security Incidents -- forensic readiness",
              "SOCI Act": "CIRMP -- record-keeping"},
    tags=["NIST", "ISM", "SOCI"])

# ============================================
# PILLAR 6: GOVERNANCE AND RISK MANAGEMENT
# ============================================

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
    mappings={"APRA CPS 234": "s.2 -- Board accountability",
              "PSPF": "Security Governance -- Policy 1",
              "Privacy Act 1988": "APP 1 -- accountability"},
    tags=["CPS234", "PSPF", "PRIVACY"])

reg("GRM-02", "AI Risk Register", "GRM",
    "The AI risk register is a distinct register that captures AI-specific risks using a dedicated "
    "threat taxonomy covering model-level, tool-level, data-level, identity-level, and pipeline-level "
    "risks. Each risk is assessed, owned, and tracked to resolution. Risk treatment must include AI-speed "
    "campaign response: automated tripwires, unledgered-asset discovery obligations, and a single exercised "
    "kill-switch capability tested at least annually (v1.5).",
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
        "Are risks assessed using a defined methodology (likelihood x impact)?",
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
              "SOCI Act": "CIRMP -- risk management",
              "APRA CPS 234": "s.3(a) -- risk assessment"},
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
    mappings={"EU AI Act": "Art. 14 -- Human Oversight",
              "NIST AI RMF": "GOVERN (GV.OC)",
              "Privacy Act 1988": "APP 1 -- accountability"},
    tags=["EU", "NIST", "PRIVACY"])

reg("GRM-04", "Third-Party AI Risk Management", "GRM",
    "Third-party AI risk management ensures that external model providers, tool providers, and AI "
    "infrastructure vendors are assessed against security requirements, contractually bound to "
    "maintain controls, and subject to right-to-audit provisions. Incident-response planning with AI/agent "
    "vendors must include agent-speed adversary playbooks and automatic containment, and evaluation-harness "
    "vendors (third-party CTF/eval partners) must be assessed for harness isolation assurance per EE-08 (v1.5).",
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
              "EU AI Act": "Art. 28 -- Third Parties"},
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
    mappings={"APRA CPS 234": "s.2 -- Board reporting",
              "NIST AI RMF": "GOVERN (GV.OV)",
              "ISM": "Guidelines for Cyber Security Documentation"},
    tags=["CPS234", "NIST", "ISM"])

reg("GRM-06", "Board and Executive Reporting", "GRM",
    "Board and executive reporting provides a standardised dashboard giving the Board and executive "
    "team visibility into the organisation's AI security posture -- maturity scores per pillar, open "
    "findings, regulatory compliance status, and risk acceptances -- designed for non-technical audiences.",
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
    mappings={"APRA CPS 234": "s.2 -- Board accountability and reporting",
              "NIST AI RMF": "GOVERN (GV.OV)"},
    tags=["CPS234", "NIST"])



# ============================================
# PILLAR 1 EXTENSIONS (v1.2/v1.3/v1.4)
# ============================================

reg("MS-07", "Deployment Context Obfuscation", "MS",
    "Evaluation and test environments must be indistinguishable from production from the model's perspective -- same API endpoints, data formats, latency profiles, error handling, and credential lifetimes. Closes the evaluation-subversion class of attacks.",
    "Prevent models from detecting evaluation environments and behaving differently than in production.",
    [
        "Evaluation environments clearly distinguishable from production.",
        "Evaluation environments API-compatible with production; divergence documented.",
        "No discoverable environment indicators; automated behavioural divergence checks; divergence treated as incident signal.",
        "Continuous divergence monitoring; evaluation pipelines indistinguishable from production; automated response on divergence.",
    ],
    [
        "Can a model detect its environment through tool outputs, data, config, or timing?",
        "Are credential lifetimes identical between evaluation and production?",
        "Is evaluation-to-production divergence treated as a subversion indicator?",
        "Are evaluation environments isolated from production (no network path)?",
    ],
    [
        "Evaluation environment configuration",
        "Environment-indicator audit results",
        "Behavioural comparison reports (eval vs production)",
        "Evaluation subversion incident logs",
    ],
    {"ISM": "Guidelines for secure AI system development", "NIST AI RMF": "MANAGE (MG.DE)", "EU AI Act": "Art. 15"},
    ["evaluation-subversion", "deployment-context"])

reg("MS-08", "MCP Security Controls", "MS",
    "Model Context Protocol (MCP) endpoints and tool definitions must be treated as attack surface with protocol-layer security: signed tool metadata, MCP gateway authentication, response validation against known-good schemas, and trusted-registry supply chain. Monitoring must cover model-originated writes to execution-bearing locations and publication channels (MCP registry self-write -- AWS Kiro CVE-2026-10591), with alerting on any write (a log without alerting is not a control) (v1.5).",
    "Secure the MCP protocol layer for agent-tool communication.",
    [
        "MCP used without gateway; no protocol-layer controls.",
        "MCP gateway deployed for agent-tool traffic; basic schema validation.",
        "Signed tool metadata; response validation against known-good schemas; trusted MCP registry.",
        "Continuous MCP protocol-layer testing; automated blocking of unsigned tool definitions.",
    ],
    [
        "Do all MCP agent-tool communications pass through an authenticated gateway?",
        "Is tool metadata signed and verified before use?",
        "Are MCP responses validated against known-good schemas?",
        "Are MCP servers sourced from trusted registries with provenance verification?",
    ],
    [
        "MCP gateway configuration and audit logs",
        "Tool definition signing configuration",
        "MCP response schema validation rules",
        "MCP server registry and provenance records",
    ],
    {"OWASP": "LLM02 (Insecure Output Handling)", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15(b)", "ISO 42001": "Clause 8.4"},
    ["mcp", "protocol-security"])

reg("MS-09", "Perception-Fidelity Enforcement for Human-in-the-Loop Approvals", "MS",
    "Content that an agent perceives, summarises, and acts upon must be perceptually equivalent to what the human approver sees. Inputs are pre-processed to strip or flag imperceptible content -- zero-opacity text, sub-pixel/1px text, background-contrast text, off-screen content, whitespace-collapsed or DOM-hidden text, and hidden pull-request comments -- before reasoning or tool use. Approvals bind to a rendering-fidelity snapshot of the exact content acted on, and agent actions must never be gated on content the human cannot perceive. Addresses the imperceptible-content injection class (AWS Kiro CVE-2026-10591 -- 1px white text rewriting the MCP registry to achieve host RCE; Android on-device agents hijacked via invisible on-screen text; Azure DevOps hidden PR comments hijacking AI review agents).",
    "Ensure human-in-the-loop approval is never gated on content the human cannot perceive.",
    [
        "Manual review for high-risk actions; no hidden-content awareness.",
        "Automated detectors for known hidden-content primitives (1px text, zero-opacity, DOM-hidden); approval snapshots captured.",
        "Policy-as-code fidelity checks pre-approval; multimodal sanitisation; hidden-content stripping before agent context.",
        "Continuous red-team testing of perception attacks; fidelity attestation embedded in the audit trail.",
    ],
    [
        "Is content sanitised against imperceptible-content vectors (1px, zero-opacity, DOM-hidden, hidden PR comments) before agent reasoning?",
        "Does the human approver see exactly the content the agent acted on (rendering-fidelity snapshot)?",
        "Are approval snapshots captured and attestable?",
        "Is the approval flow tested against hidden-content injection (CVE-2026-10591 class)?",
    ],
    [
        "Content sanitisation configuration (hidden-content primitives)",
        "Approval snapshot store and attestation records",
        "Perception-attack red-team test results",
    ],
    {"OWASP": "LLM01 (Prompt Injection, multimodal variants)", "NIST AI RMF": "MEASURE (ME.AD)", "EU AI Act": "Art. 14 (Human Oversight)", "ISM": "Web Content Filtering"},
    ["perception-fidelity", "hidden-content", "hitl"])

reg("MS-10", "Agent Memory-Store Integrity", "MS",
    "Persistent agent memory stores -- vector databases, learning/pattern stores, conversation histories, and retrieval contexts that influence future model behaviour -- are security-critical data stores whose integrity must be monitored and enforced. Poisoned memories steer model responses for every future user of the platform and survive software patches: remediation requires auditing and cleaning the memory store itself, not just updating code. Addresses the memory-poisoning persistence class (Ruflo/RufRoot CVE-2026-59726, CVSS 10.0 -- an unauthenticated attacker used a default-exposed MCP bridge to obtain RCE, read LLM provider API keys, spawn attacker-controlled agent swarms on the victim's keys, and write malicious patterns into the AgentDB learning store that steer future AI outputs long after the intrusion ended; Noma Security: patching the bridge did not undo the poisoning -- operators were instructed to audit the pattern store and rebuild containers). Memory writes must be authenticated, tamper-evident, and auditable; retrieval must be able to detect and exclude poisoned entries; and memory stores must be treated as compromised -- audited, cleaned, and rebuilt -- whenever the agent platform or the memory store itself has been accessed by an attacker.",
    "Ensure agent persistent memory cannot be silently poisoned to steer future behaviour.",
    [
        "Memory persisted without integrity controls; no tamper awareness.",
        "Memory-store access authenticated; write logging; basic integrity checks.",
        "Tamper-evident memory (append-only or immutable snapshots); anomaly detection on memory writes via MIR-02; retrieval-layer filtering of flagged entries; documented post-incident memory audit-and-clean procedure.",
        "Continuous memory integrity attestation; automated quarantine of poisoned entries; red-team testing of memory-poisoning persistence and recovery.",
    ],
    [
        "Is persistent agent memory protected against unauthorised writes?",
        "Can poisoned memory entries be detected and excluded from retrieval?",
        "Is the memory store audited and cleaned after any platform compromise, rather than trusting a code patch alone?",
        "Are memory writes logged with agent identity for forensic reconstruction?",
    ],
    [
        "Memory-store access control configuration",
        "Memory write audit logs",
        "Tamper-detection and quarantine configuration",
        "Post-incident memory audit and clean reports",
    ],
    {"OWASP": "LLM03 (Training Data Poisoning, runtime variant)", "NIST AI RMF": "PROTECT (PR.DS)", "EU AI Act": "Art. 10 (Data Governance)", "ISM": "Guidelines for System Monitoring"},
    ["memory-integrity", "poisoning", "retrieval"])

reg("MS-11", "Operational Data-Stream Integrity", "MS",
    "Any data stream an agent consumes in the course of its operational duties -- application and error logs, security alerts, observability feeds, SIEM/SOAR queues, incident ticketing -- must be treated as untrusted input with instruction/data separation. Agents must never execute an action whose trigger originated from log or alert content without an independent, non-log verification step and, for high-impact actions, human approval. Log and alert ingestion pipelines must authenticate their producers so forged or spoofed entries cannot inject instructions, and MIR-02 must flag any agent action whose proximate cause traces to a log or alert entry. Addresses the observability-stream poisoning class (Tenet Security GhostJacking, DEFCON 34, August 2026 -- attackers poisoned the observability streams of Cloudflare, Datadog, and Sentry with malicious instructions that AI agents, including Claude Code, treat as trusted operational input, achieving a 90% success rate against Claude Code under Cloudflare default configuration and executing DNS changes, arbitrary code, and credential theft with no EDR, WAF, or IAM alerting; an estimated 15,000+ organisations exposed through vulnerable Cloudflare configurations and 2,700+ publicly exposed Datadog API keys; the class cascades across platforms because a compromised agent monitoring one feed compromises agents on other platforms). Agent-visible operational content must be sanitised for instruction-bearing payloads before the agent reasons over it or acts on it.",
    "Prevent poisoned logs, alerts, and observability feeds from commanding the agent.",
    [
        "Agents consume logs/alerts as-is; operational content treated as trusted.",
        "Log/alert content flagged as untrusted; agent actions from log triggers require review.",
        "Agent-visible operational content sanitised for instruction-bearing payloads before reasoning; independent non-log verification for log-triggered actions; ingestion pipelines authenticate producers; MIR-02 flags log-origin agent actions.",
        "Continuous red-team testing of the observability stream (GhostJacking class); provenance attestation on all agent-consumed feeds; fail-closed on stream integrity doubt.",
    ],
    [
        "Do agents treat log/alert/observability content as trusted instructions?",
        "Can an agent execute an action triggered solely by log or alert content without independent verification?",
        "Are log and alert ingestion pipelines authenticated at the producer level?",
        "Does MIR-02 detect and flag agent actions whose proximate cause is a log or alert entry?",
    ],
    [
        "Operational data-stream sanitisation rules",
        "Log/alert producer authentication configuration",
        "Log-triggered action verification policy",
        "MIR-02 log-origin action detection rules",
    ],
    {"OWASP": "LLM01 (Prompt Injection)", "NIST AI RMF": "PROTECT (PR.DS)", "EU AI Act": "Art. 14 (Human Oversight)", "ISM": "Guidelines for System Monitoring"},
    ["observability", "log-poisoning", "data-stream-integrity"])

reg("MS-12", "MCP Discovery-Metadata and Shared-Cache Integrity", "MS",
    "MCP discovery metadata -- the server-level instructions field, tool descriptions, and resource/prompt list responses -- must be treated as untrusted input with instruction/data separation: instructions are length-limited, screened for instruction-bearing content, and isolated from the trusted system prompt with explicit untrusted-content boundaries; tool metadata is validated against an operator-approved baseline with drift alerting. Shared and intermediary caches of MCP discovery responses must not serve content across authentication contexts unless the cached metadata is cryptographically signed with verified provenance; cacheScope claims made by servers are verified, never trusted, and cache keys bind to the authenticated identity. Addresses the MCP discovery-metadata and cache-surface class (MCP-2026-008 cache poisoning -- a malicious server marks a poisoned tools/list or instructions response as publicly cacheable so a shared gateway re-serves it to other users; MCP-2026-015 -- the discovery instructions field is fully server-controlled text folded into the client system prompt with no sanitisation, validation, or length limits, so a hostile server can place directives such as 'ignore all safety instructions' directly into the system prompt; chained, one poisoned response is cached once and served to every user behind a shared proxy, crossing the tenant boundary; Context7 CVE-2026-75130, CVSS 3.1 9.0 -- the widely installed MCP documentation server let an attacker with write access to its Custom AI Instructions feature plant directives that exfiltrated .env credentials and performed destructive file deletion whenever the agent made a routine library-documentation request; an audit of 19 widely deployed MCP servers found 18 do not document their instruction-injection surfaces at all).",
    "Prevent MCP discovery metadata and shared caches from injecting instructions into agent system prompts.",
    [
        "MCP servers connected without review; discovery responses folded into context as-is; responses cached across users.",
        "MCP servers inventoried; instructions field flagged as untrusted; no cross-user response caching.",
        "Instructions isolated from the trusted system prompt with explicit boundaries and length limits; cache keys bind to authenticated identity; cacheScope claims verified; tool metadata pinned to a baseline with drift alerting.",
        "Signed provenance required for cached metadata; default-deny on MCP server connections with provenance verification; active red-team testing of the discovery/cache path; protocol-level fixes (instructions as untrusted content, cacheScope verification) required of vendors.",
    ],
    [
        "Are MCP discovery metadata and instructions fields treated as untrusted input?",
        "Can server-supplied instructions reach the model's system prompt without an untrusted-content boundary?",
        "Are shared caches of MCP responses keyed by authenticated identity and never served across users?",
        "Are cacheScope claims from servers verified rather than trusted?",
        "Is tool metadata pinned to an operator-approved baseline with drift alerting?",
    ],
    [
        "MCP server inventory and approval baseline",
        "Instruction-field sanitisation and isolation rules",
        "Cache-keying and cacheScope verification configuration",
        "Metadata drift alerting rules (MIR-01/MIR-02)",
    ],
    {"OWASP": "LLM01 (Prompt Injection)", "NIST AI RMF": "PROTECT (PR.DS)", "EU AI Act": "Art. 14 (Human Oversight)", "ISM": "Guidelines for System Monitoring"},
    ["mcp", "prompt-injection", "cache-poisoning", "discovery-metadata"])

# ============================================
# PILLAR 2 EXTENSIONS (v1.2/v1.4)
# ============================================

reg("IAM-07", "Transitive Delegation Chain Enforcement", "IAM",
    "All identity delegations must be bounded at maximum depth (recommended 2 hops: human to agent to tool). Downstream delegation or proxying of the agent's identity must be blocked at the infrastructure layer; chains must be reconstructable from audit logs with originating identity context.",
    "Bound delegation chains and make them fully auditable.",
    [
        "Unbounded delegation; agents inherit full downstream permissions.",
        "Delegation depth documented; basic bounds for critical tools.",
        "Infrastructure-layer blocking of unbounded delegation; token chaining across hops; full chain reconstruction.",
        "Continuous chain verification; automated alerting on delegation anomalies; chain-boundary red-team testing.",
    ],
    [
        "Is delegation depth bounded (human to agent to tool)?",
        "Can tools or downstream services further delegate the agent's identity?",
        "Is every delegation hop recorded with originating identity context?",
        "Are audit logs capable of reconstructing the full delegation chain?",
    ],
    [
        "Delegation enforcement configuration (OPA, gateway rules)",
        "Token chaining configuration (OIDC, SPIFFE/SPIRE)",
        "Audit logs demonstrating chain reconstruction",
    ],
    {"ISM": "Guidelines for System Management", "OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "GOVERN (GV.AC)", "EU AI Act": "Art. 14(b)"},
    ["delegation", "token-chaining"])

reg("IAM-08", "Credential Scope Narrowing", "IAM",
    "Credentials in agent execution environments must be scoped to the minimum set of actions, resources, and conditions for the agent's registered tools per TP-01. No environment-wide credentials. Short-lived per-tool tokens; revocation cascades through the delegation chain.",
    "Ensure credentials in agent environments are minimal, short-lived, and revocable.",
    [
        "Broad shared credentials in agent environments.",
        "Per-agent credentials; scope aligned to tool inventory.",
        "Per-tool scoped short-lived tokens; no environment-wide credentials; automated rotation.",
        "Continuous scope verification; cascade revocation on compromise; per-tool scope attestation.",
    ],
    [
        "Are credentials scoped per tool, not per environment or service?",
        "Are short-lived tokens used rather than persistent service accounts?",
        "Does credential revocation cascade through the delegation chain?",
        "Is credential scope per agent documented and reviewed?",
    ],
    [
        "Credential issuance configuration (token scopes, lifetimes)",
        "Agent environment credential mounts",
        "Rotation and revocation runbooks",
    ],
    {"ISM": "Guidelines for System Management", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15(b)", "Essential Eight": "Restrict Administrative Privileges"},
    ["credentials", "least-privilege"])

reg("IAM-09", "Multi-Tenant Agent Platform Isolation", "IAM",
    "For managed agent platforms, tenant isolation must be enforced at the data layer: every workflow execution, tool invocation, and data query scoped by tenant ID server-side; no user-controlled object IDs bypass tenant scoping (CWE-639 IDOR); cross-tenant execution impossible.",
    "Enforce data-layer tenant isolation on managed agent platforms.",
    [
        "No tenant isolation; shared data plane across tenants.",
        "Tenant scoping at the application layer only.",
        "Data-layer tenant isolation (row-level security); tenant ID in every query; automated cross-tenant testing in CI/CD.",
        "Continuous tenant-isolation verification; automated blocking of cross-tenant attempts; platform CVE monitoring.",
    ],
    [
        "Is every execution and query scoped by tenant ID server-side?",
        "Can user-controlled object IDs bypass tenant scoping (IDOR tested)?",
        "Is cross-tenant execution impossible even with valid credentials?",
        "Is row-level security enforced at the database layer?",
    ],
    [
        "Tenant isolation configuration and row-level security policies",
        "Automated cross-tenant access test results (CI/CD)",
        "Platform vulnerability scan and patch records",
        "IDOR penetration test reports",
    ],
    {"NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15(b)", "ISO 42001": "Clause 8.4", "ISM": "Guidelines for System Management"},
    ["multi-tenant", "idor"])

# ============================================
# PILLAR 4 EXTENSIONS (v1.2/v1.4)
# ============================================

reg("TP-07", "Cross-Tool Dependency Analysis", "TP",
    "Before deployment, all registered tools must be analysed for transitive risk -- combinations that enable sandbox escape, privilege escalation, or exfiltration when chained. Escape-class chains require explicit risk acceptance via GRM-02.",
    "Detect and gate escape-class tool combinations before deployment.",
    [
        "No cross-tool analysis; tools assessed in isolation.",
        "Manual review of tool combinations for critical agents.",
        "Automated risk scoring of combinations; escape-class chains blocked or risk-accepted via GRM-02.",
        "Continuous chain analysis on every tool change; automated blocking of new escape-class combinations.",
    ],
    [
        "Is every tool classified by escape-chain potential (network_write, file_write, code_execution, identity_escalation, data_query)?",
        "Are tool combinations analysed for chained risk before deployment?",
        "Do escape-class chains (e.g., network_write + code_execution) trigger blocking review?",
    ],
    [
        "Tool classification registry",
        "Cross-tool dependency analysis reports",
        "Risk acceptance records (GRM-02)",
    ],
    {"OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "MANAGE (MG.DE)", "EU AI Act": "Art. 9(4)"},
    ["escape-chains", "transitive-risk"])

reg("TP-08", "API Gateway Infrastructure-Isolation Mode", "TP",
    "Agent API gateways must enforce an allow-list of permitted endpoints that excludes all cloud infrastructure control-plane APIs (EC2, IAM, Lambda, KMS, CloudFormation, S3 control-plane, Azure Resource Manager, GCP Cloud Resource Manager). Non-tool API calls are blocked, logged, and treated as compromise indicators.",
    "Prevent agents from reaching cloud infrastructure control planes.",
    [
        "Agents can reach infrastructure APIs directly or via default routing.",
        "Gateway present; infrastructure APIs blocked by policy but untested.",
        "Explicit allow-list excluding control-plane APIs; blocked attempts logged and alerted.",
        "Continuous testing of the allow-list against provider endpoint inventories; automated block-list updates.",
    ],
    [
        "Does the gateway enforce an allow-list of permitted endpoints?",
        "Are all control-plane APIs excluded from the allow-list?",
        "Are blocked infrastructure-API attempts logged and alerted?",
        "Is the allow-list tested against known provider endpoints?",
    ],
    [
        "Gateway allow-list configuration",
        "Blocked-request logs for infrastructure API attempts",
        "Infrastructure-API bypass test results",
    ],
    {"ISM": "Guidelines for Gateways", "NIST AI RMF": "PROTECT (PR.PT)", "EU AI Act": "Art. 15(b)"},
    ["control-plane", "gateway-allowlist"])

reg("TP-09", "Explicit Tool Registration", "TP",
    "Agent frameworks must not auto-register internal functions, SDK helpers, or framework internals as agent-callable tools. Every callable must be explicitly declared in the TP-01 registry; attribute-based registration, reflection-based discovery, and internal-helper exposure are prevented.",
    "Eliminate implicit tool exposure in agent frameworks.",
    [
        "Frameworks auto-expose internal functions; no registry enforcement.",
        "Explicit registry for critical tools; auto-registration partially disabled.",
        "Auto-registration disabled by default; all callables audited; unregistered callables blocked.",
        "Continuous callable-audit in CI/CD; automated blocking of implicitly exposed tools.",
    ],
    [
        "Is framework auto-registration disabled by default?",
        "Are all discoverable callables audited against the TP-01 registry?",
        "Are unregistered callables blocked from agent invocation?",
        "Is the framework checked for implicit-exposure CVEs (CVE-2026-25592, CVE-2026-26030)?",
    ],
    [
        "Framework tool-registration configuration",
        "TP-01 tool registry (explicit declarations)",
        "Callable-discovery audit results",
        "Framework CVE scan records",
    ],
    {"OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "IDENTIFY (ID.AM)", "EU AI Act": "Art. 15(b)"},
    ["tool-registry", "implicit-exposure"])

reg("TP-10", "Agent Platform Inbound Control-Plane Protection", "TP",
    "The agent platform's gateway, control plane, and any service the platform or an agent binds must be treated as an inbound attack surface, not merely as an outbound actor. All listeners -- loopback, LAN, MCP endpoints, webhook receivers, debug interfaces -- are governed by a network-binding policy defaulting to deny, enforced at the OS/namespace boundary. Gateway tokens and operator credentials are least-privilege scoped, never readable from web or browser context, and bound to validated origins (cross-site WebSocket hijack-resistant session handling). Accidental or agent-initiated service binding is detected, reported, and blocked absent explicit approval; the binding guard fails closed on error. Addresses the inbound control-plane class (OpenClaw CVE-2026-25253 -- cross-site WebSocket hijacking of a loopback gateway token disabling approvals and escaping the shell container to host RCE; Unit 42 -- an attacker's agent accidentally exposing an HTTP server from its home directory with API keys and shell history; Wiz exposed-MCP-servers research; Metasploit 6.5 shipping an MCP server).",
    "Defend the agent platform's inbound listening surface from direct, model-independent attack.",
    [
        "Listeners ungoverned; gateway tokens reachable from web/browser context.",
        "Listener inventory maintained; origin validation on gateway sessions; token scope review.",
        "Default-deny binding policy enforced; no standing allow rules; automated detection of new listeners; no operator-scope tokens readable from web context.",
        "Continuous adversarial testing of the inbound surface; binding-policy attestation in the audit trail; periodic re-certification of all allow rules.",
    ],
    [
        "Are all agent-platform listeners (loopback, LAN, MCP, webhooks, debug) inventoried and governed by a default-deny binding policy?",
        "Can gateway/operator tokens be read from web or browser context (CSWSH test)?",
        "Is origin validation enforced on gateway WebSocket/SSE sessions?",
        "Are accidental or agent-initiated service bindings detected and blocked?",
        "Does the binding guard fail closed when it errors?",
    ],
    [
        "Network-binding policy configuration",
        "Gateway session origin-validation rules",
        "Listener inventory and drift reports",
        "CSWSH/origin-validation test results",
    ],
    {"ISM": "Web Application Hardening, Network Segmentation", "OWASP": "LLM09 (Misuse of System Access)", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 14"},
    ["inbound-surface", "gateway", "cswsh"])

reg("TP-11", "Agent Browser and Content-Rendering Isolation", "TP",
    "Agent browser runtimes and any component that renders and interprets untrusted content -- agentic browsers, document processors in AI assistants, rendered web pages -- must preserve origin and content isolation. Agentic browsers that dismantle the Same-Origin Policy to act across sites on the user's behalf convert every page the agent reads into a potential command source: invisible instructions (white-on-white text, zero-opacity overlays, CSS-hidden elements) embedded in any content the agent perceives are executed as if they were user commands, enabling zero-click account takeover, cross-tab token theft, email exfiltration, and unauthorised financial transfers. Addresses the agentic-browser content-injection class (Zenity Labs Intent Collision, Black Hat USA 2026 -- zero-click takeover demonstrated across Claude in Chrome, Gemini, Perplexity Comet, ChatGPT Atlas, and Copilot Edge, with several vendors characterising the attack as intended functionality because cross-origin agent capability is the product; the ChatMate/Rubrik Zero Labs Remote Prompt Execution chain on Microsoft 365 Copilot -- a poisoned document upload bypassing LLM guardrails, escaping the assistant sandbox via a container-runtime path traversal (CVE-2026-32193) plus LD_PRELOAD, and handing the attacker a bidirectional shell inheriting the victim's identity; and the AISI cross-agent injection -- invisible HTML-comment instructions in GitHub issues addressed to AI triage agents). Rendered content must be classified as untrusted input and stripped of imperceptible instruction vectors before agent action; cross-origin privileged actions (token access, credential use, financial operations) must be gated by the same approval and isolation rules as any other high-risk tool action; the browser/session layer must be isolated from the agent's credential material; and document uploads must be sanitised before assistant processing.",
    "Prevent untrusted rendered content from commanding the agent.",
    [
        "Agent uses browser/document rendering as-is; no content classification.",
        "Hidden-content scanning on rendered pages and uploaded documents; cross-origin actions flagged for review.",
        "Origin isolation preserved in agent browser runtimes; no cross-origin token access; imperative action gating (approval required for financial and credential operations); document uploads sanitised before assistant processing.",
        "Continuous adversarial testing of the rendering layer; origin-isolation attestation; red-team validation against zero-click chains (PleaseFix/Intent Collision class).",
    ],
    [
        "Can content rendered by the agent's browser or a processed document execute privileged actions without approval?",
        "Are imperceptible instruction vectors stripped from rendered content before agent action?",
        "Is origin isolation preserved in agent browser runtimes (no cross-origin token access)?",
        "Are document uploads sanitised before assistant processing (Remote Prompt Execution class)?",
        "Is the browser/session layer isolated from the agent's credential material?",
    ],
    [
        "Browser/session isolation configuration",
        "Rendered-content sanitisation rules",
        "Cross-origin action gating policy",
        "Red-team results (Intent Collision / RPE class)",
    ],
    {"OWASP": "LLM01 (Prompt Injection)", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15 (Transparency and Human Oversight)", "ISM": "Web Content Filtering"},
    ["agentic-browser", "content-isolation", "zero-click"])

reg("TP-12", "Tool-Call Provenance and Dispatch Verification", "TP",
    "Every tool execution must verify that the tool-call instruction originated from an authorised model turn or an explicitly authorised caller. The dispatch layer must not treat data shaped like a model-generated tool call as authoritative without provenance verification: tool calls carry cryptographically bound provenance (session, turn, model signature) that is verified before dispatch; session history and event streams are authenticated so attacker-injected events cannot fabricate tool calls or approval confirmations; approval records bind to the exact tool call (tool name and arguments) they authorise and are verified against the human approver channel, never against session history the agent can write; and the inspection-execution gap fails closed -- no provenance, no dispatch. Addresses the dispatch-provenance class (Stealth CoreBreak, Black Hat USA 2026 -- AWS Bedrock AgentCore CVE-2026-18830 CVSSv4 8.6: an authenticated remote caller injected a tool-use content block into an InvokeHarness request and the event loop dispatched the tool without model authorisation; Google ADK CVE-2026-18236 CVSSv4 9.3: attacker-controlled session events forged a human-approval confirmation because the confirmation processor never verified tool ownership or argument matches; Vercel @ai-sdk/harness-codex/opencode CVE-2026-64650/64651 CVSSv4 6.3: a process-path check trusted any process whose command line contained an approved helper path). The class is distinct from prompt injection: the model is bypassed altogether at the dispatch layer, so system prompts, refusal training, and content filters cannot help.",
    "Ensure no tool executes without verified provenance from an authorised model turn or caller.",
    [
        "Dispatch executes any data shaped like a tool call; no provenance checks.",
        "Tool calls carry basic session identifiers; dispatch verifies call structure only.",
        "Tool calls carry cryptographically bound provenance (session, turn, model signature) verified before dispatch; session/event history authenticated; approval records bind to tool name and arguments and verify against the human approver channel; fail closed on unverifiable provenance.",
        "Continuous provenance attestation on all dispatches; red-team testing of the dispatch layer (CoreBreak class); automated blocking of provenance-less tool calls across all harnesses and MCP servers.",
    ],
    [
        "Can a tool execute without a verified, authorised model turn?",
        "Can attacker-injected session or event history fabricate a tool call or an approval confirmation?",
        "Do approval records bind to the exact tool call (name and arguments) they authorise?",
        "Is approval evidence verified against the human approver channel, never against agent-writable session history?",
        "Does dispatch fail closed when tool-call provenance cannot be verified?",
    ],
    [
        "Dispatch-layer provenance verification configuration",
        "Session/event history authentication controls",
        "Approval-record binding policy",
        "Red-team results (CoreBreak class)",
    ],
    {"OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 14(b)", "ISM": "Guidelines for Gateways"},
    ["dispatch", "provenance", "inspection-execution-gap"])

reg("TP-13", "Agent Dependency-Install Provenance Verification", "TP",
    "Agents must not execute installation commands derived from ingested content (documentation pages, llms.txt/llms-full.txt files, setup guides, README instructions) without verifying the provenance of every package, domain, and command they reference. Package names are confirmed to exist in the intended registry and the namespace is verified to belong to the documented vendor (registry ownership checks, domain registration and expiry checks) before any pip/npm/npx/apt/go install or clone executes; installation commands sourced from untrusted or ingested content are gated by an operator-maintained allowlist or human approval instead of being treated as authoritative setup steps; dangling references (commands pointing to unregistered packages, unclaimed or expired domains, or mismatched namespaces) are treated as security findings that block the install, log via MIR-01, and surface for review; and a documentation file is never treated as an authoritative install script. Addresses the llms.txt dangling-install class (Ars Technica, August 27, 2026: 120 of 8,265 scanned llms.txt files referenced unregistered packages or unclaimed domains; code-execution phone-homes from Fortune 500 companies within an hour of name registration; live malware in the Clerk.com npx case; Claude, Codex, and Hermes coding agents executed the installs automatically).",
    "Verify registry-namespace and domain-ownership provenance before any agent-executed install derived from ingested content.",
    [
        "Agents execute install commands found in documentation or llms.txt verbatim with no namespace checks.",
        "Install commands from ingested content run, but package/domain existence is only checked post-hoc.",
        "Pre-install provenance verification: registry existence, namespace ownership, domain registration; installs from untrusted content gated by an allowlist or human approval; dangling references blocked and logged via MIR-01.",
        "Continuous verification against live registry state; automated blocking of dangling references; documentation files never treated as authoritative install scripts; red-team testing of the docs-to-install path.",
    ],
    [
        "Do agents execute installation commands from documentation without verifying package existence and namespace ownership?",
        "Are installs derived from untrusted content gated by an allowlist or human approval?",
        "Are dangling references (unregistered packages, unclaimed domains) blocked, logged, and surfaced as findings?",
        "Is a documentation file ever treated as an authoritative install script?",
    ],
    [
        "Dependency-install provenance verification configuration",
        "Registry namespace and domain-ownership check results",
        "Install-command allowlist / approval policy",
        "Dangling-reference findings and MIR-01 alerts",
    ],
    {"OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "PROTECT (PR.DS)", "EU AI Act": "Art. 14 (Human Oversight)", "ISM": "Guidelines for Gateways"},
    ["dependency", "install", "llms.txt", "provenance"])

reg("TP-14", "Skill/Plugin Payload Integrity and Instruction-Channel Isolation", "TP",
    "Skills, plugins, and marketplace extensions must be distributed as cryptographically signed, immutable payloads whose instruction content is fixed at install time. Runtime-fetchable instruction channels (remote referral manifests, update feeds, operator-controlled configuration fetched after install) are prohibited and must be blocked at the network and runtime layers, because a post-install fetch channel is a command-and-control path invisible to monitoring (it is not a tool call). Skills execute with privileges scoped to their declared capability set, never the agent's full identity, and a post-install behavioural baseline must be established under MIR-02 before full capability is granted, with baseline drift quarantining the skill. Marketplace provenance must be attestable end-to-end (publisher to registry to artifact) with publisher identity attestation. On any signature, provenance, or baseline error the install is blocked and installed skills are suspended; runtime-fetch attempts terminate the skill and alert via MIR-01 — never unsigned execution. Addresses the ClawHavoc/ClawHub skill-marketplace class (Koi Security, February 2026; Antiy CERT: 1,184 malicious skills, ~20% of the registry; Unit 42, June 2026: evasive skills passing automated scanning, runtime affiliate injection, and agentic front-running).",
    "Gate every agent extension install on signed, immutable payloads with no runtime-fetchable instruction channels and privilege-scoped execution.",
    [
        "Skills installed ad hoc from any marketplace with no signature or provenance checks; full agent privileges.",
        "Signature verification at install; marketplaces restricted to an operator allowlist.",
        "Immutable signed payloads; runtime-fetch channels blocked; privilege-scoped execution; post-install baseline with drift quarantine.",
        "End-to-end provenance attestation at registry and runtime; cross-org telemetry sharing on malicious-skill signals; red-team testing of the install path.",
    ],
    [
        "Are skills/plugins verified for signature and provenance before install?",
        "Are runtime-fetchable instruction channels (remote manifests, update feeds) blocked?",
        "Do skills execute with privileges scoped to their declared capability set, not the agent's full identity?",
        "Is a post-install behavioural baseline established and drift-quarantined?",
    ],
    [
        "Skill/plugin signature and provenance verification configuration",
        "Runtime-fetch network-block policy and alerts",
        "Skill privilege-scope declarations and execution audit",
        "Post-install behavioural baseline records and drift alerts (MIR-02)",
    ],
    {"OWASP": "LLM08 (Excessive Agency)", "NIST AI RMF": "PROTECT (PR.DS)", "EU AI Act": "Art. 14 (Human Oversight)", "ISM": "Guidelines for Software Development, Application Control"},
    ["skill", "plugin", "marketplace", "extension", "instruction-channel", "clawhavoc"])

# ============================================
# PILLAR 7: EXECUTION ENVIRONMENT (v1.2, extended v1.4)
# ============================================

reg("EE-01", "Execution Environment Boundary Enforcement", "EE",
    "All agentic AI execution must occur within a defined container/VM/sandbox with no shared host filesystem mounts, no shared IPC/network namespaces, immutable infrastructure, and fail-closed behaviour on isolation breach.",
    "Enforce a hard execution boundary around every agent.",
    [
        "Agents run on shared infrastructure with no boundary enforcement.",
        "Container per agent; basic isolation; shared mounts documented.",
        "No shared host mounts or namespaces; immutable infrastructure; fail-closed on breach.",
        "Runtime boundary verification (attestation); automated response on any isolation breach.",
    ],
    [
        "Does every agent run inside a defined sandbox boundary?",
        "Are host mounts, IPC, and network namespaces shared?",
        "Does the environment fail closed on isolation breach?",
    ],
    [
        "Sandbox/container runtime configuration",
        "Host filesystem mount configuration",
        "Namespace isolation configuration",
        "Isolation breach alerts and incident records",
    ],
    {"ISM": "Guidelines for System Hardening", "Essential Eight": "Application Control", "ASD": "Container Security Guidance"},
    ["sandbox", "isolation"])

reg("EE-02", "Infrastructure API Access Control", "EE",
    "Agents must have no implicit access to cloud infrastructure APIs (EC2, IAM, Lambda, S3, Azure Resource Manager, GCP Cloud Resource Manager) unless explicitly registered as tools via TP-01 and gated by TP-03.",
    "Ensure agents cannot reach infrastructure control planes implicitly.",
    [
        "Agents inherit infrastructure credentials or can reach control planes.",
        "Infrastructure credentials not mounted; network path blocked but untested.",
        "Explicit tool registration required for infrastructure access; metadata service disabled; blocked attempts logged.",
        "Continuous verification of credential scoping; automated alerting on any infrastructure API attempt.",
    ],
    [
        "Do agent environments hold infrastructure API credentials?",
        "Is infrastructure access explicitly registered via TP-01?",
        "Is the network path to control planes blocked by default?",
        "Is the metadata service disabled or scoped?",
    ],
    [
        "Agent environment IAM role/credential configuration",
        "Metadata service configuration",
        "Network security rules between agents and control planes",
        "Infrastructure API access logs",
    ],
    {"ISM": "Guidelines for Gateways", "NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15(b)"},
    ["infrastructure-apis", "control-plane"])

reg("EE-03", "Resource Usage Limiting", "EE",
    "Agents must have bounded CPU, memory, network, storage, and API-rate limits. Exceeding limits triggers alerts and may terminate the agent -- preventing resource exhaustion, mining, and DoS via compromised agents.",
    "Bound agent resource consumption with runtime enforcement.",
    [
        "No resource limits; agents share unbounded resources.",
        "Basic limits configured; policy-only enforcement.",
        "Runtime-enforced limits (CPU, memory, storage, network, API rate); exceeding limits alerts and may terminate.",
        "Continuous anomaly detection on resource usage; automated termination for abuse patterns.",
    ],
    [
        "Are CPU, memory, storage, and network limits configured per agent?",
        "Are API rate limits enforced per agent?",
        "Are limits enforced by the container runtime, not just policy?",
    ],
    [
        "Resource quota configuration",
        "API rate limit configuration",
        "Runtime enforcement logs",
        "Resource anomaly alert rules",
    ],
    {"ISM": "Guidelines for System Management", "NIST AI RMF": "PROTECT (PR.PT)", "Essential Eight": "Application Control"},
    ["resource-limits", "denial-of-service"])

reg("EE-04", "Evaluation Sandbox Integrity", "EE",
    "Evaluation and test environments must be isolated from production with no network path; models must not distinguish evaluation from production (see MS-07); evaluation pipelines must not modify production systems.",
    "Contain the blast radius of model behaviour during evaluation.",
    [
        "Evaluation and production share networks, data, and tooling.",
        "Evaluation isolated from production data; network path partially open.",
        "No network path between evaluation and production; evaluation pipelines cannot modify production.",
        "Continuous isolation verification; automated teardown; evaluation subversion detection per MS-07.",
    ],
    [
        "Is there a network path between evaluation and production?",
        "Can evaluation pipelines modify production systems?",
        "Can a model in evaluation reach production tools or APIs?",
    ],
    [
        "Network segmentation configuration",
        "Evaluation environment architecture documentation",
        "Isolation breach test results",
    ],
    {"ISM": "Guidelines for System Management", "NIST AI RMF": "GOVERN (GV.OD)", "EU AI Act": "Art. 15(a)"},
    ["evaluation", "test-isolation"])

reg("EE-05", "Host-Trusted Configuration File Injection Prevention", "EE",
    "Agents must not write files that the host OS or host applications will later execute or load as trusted configuration -- shell profiles, IDE/editor config, version control config, runtime interpreter wrappers, crontab, systemd units. Write-path allowlisting with host-trusted path exclusion; filesystem integrity monitoring.",
    "Prevent indirect sandbox escape via host-trusted file injection.",
    [
        "Agents can write anywhere including host-trusted paths.",
        "Write-path allowlist for critical paths; manual review.",
        "Host-trusted paths excluded from agent writes; FIM on host-trusted directories; content scanning.",
        "Host-side isolation preventing agent-written file execution; continuous FIM; automated response.",
    ],
    [
        "Can the agent write to host-trusted paths (shell profiles, IDE config, git config, crontab)?",
        "Is a write-path allowlist enforced with host-trusted paths excluded?",
        "Is filesystem integrity monitoring in place on host-trusted directories?",
    ],
    [
        "Write-path allowlist configuration",
        "Filesystem integrity monitoring configuration",
        "Host-trusted path inventory",
        "Configuration injection detection alerts",
    ],
    {"ISM": "Guidelines for System Hardening", "Essential Eight": "Application Control", "ASD": "Container Security Guidance"},
    ["file-injection", "host-trusted-paths"])

reg("EE-06", "Fail-Closed Sandbox Operation", "EE",
    "Agent execution environments must verify at runtime that the strongest configured isolation mode is active and FAIL CLOSED -- halt execution and alert -- rather than silently degrading when the primary sandbox is unavailable. Addresses fail-open fallback (CrewAI CVE-2026-2275/2287).",
    "Eliminate silent fallback to weaker sandboxes.",
    [
        "Sandbox used opportunistically; silent fallback possible.",
        "Sandbox availability checked; fallback paths documented but not blocked.",
        "Runtime attestation before each execution; no fallback path; fail-closed on unavailability; alerts on degradation.",
        "Continuous attestation; automated blocking of non-sandboxed execution; sandbox-unavailable events treated as compromise indicators.",
    ],
    [
        "Is sandbox-mode attestation performed before each code execution step?",
        "Is there any fallback path that runs untrusted code without the sandbox?",
        "Does execution halt when the sandbox cannot be verified?",
    ],
    [
        "Sandbox-mode attestation configuration and logs",
        "Framework fallback path audit",
        "Fail-open incident records (CrewAI CVE-2026-2275/2287 assessment)",
        "Alert rules for sandbox degradation",
    ],
    {"NIST AI RMF": "PROTECT (PR.PT)", "EU AI Act": "Art. 15(b)", "ISM": "Guidelines for System Hardening"},
    ["fail-closed", "sandbox-attestation"])

reg("EE-07", "Agent Control-Plane Configuration Integrity", "EE",
    "Agents must not modify the configuration governing their own security controls -- sandbox mode, approval policy, tool permissions, hooks -- and tooling must not load configuration from writable shared directories. Addresses self-configuration poisoning (Codex CLI) and config-trust failures (CVE-2026-35603). Extends to any execution-bearing configuration the agent can self-write, including MCP server registries and launch configurations -- MCP registry entries are executable launch commands auto-run on reload (AWS Kiro CVE-2026-10591) -- and to external modification of control-plane configuration via gateway/API surfaces (OpenClaw CVE-2026-25253) (v1.5).",
    "Prevent agents from disabling their own security controls.",
    [
        "Agents can modify their own security configuration; tools load config from writable paths.",
        "Control-plane config documented; agent write access partially restricted.",
        "Control-plane config read-only to the agent; world-writable paths rejected; integrity monitoring on control files.",
        "Continuous integrity verification; automated blocking of self-configuration changes; config-trust vulnerability patching.",
    ],
    [
        "Is agent security configuration read-only to the agent process?",
        "Can the agent write to its own control-plane configuration files?",
        "Is configuration from world-writable paths rejected?",
        "Are unexpected control-plane config changes monitored (MIR-01)?",
    ],
    [
        "Control-plane configuration mount/read-only settings",
        "Configuration file permissions and ownership",
        "World-writable directory audit results",
        "CVE-2026-35603 assessment and patch records",
    ],
    {"NIST AI RMF": "PROTECT (PR.AC)", "EU AI Act": "Art. 15(b)", "ISM": "Guidelines for System Hardening"},
    ["control-plane", "config-poisoning"])

reg("EE-08", "Evaluation-Harness Isolation and Integrity", "EE",
    "Isolation claims for evaluation, test, and CTF environments must be enforced as controls, not asserted as configuration. Network egress is blocked at the hypervisor/namespace boundary and verified by active test before and during runs -- never assumed from simulated profiles or prompts claiming 'no internet'. Evaluation targets are collision-checked against real domains, assets, and production identifiers before use (fictional targets must not resolve to or share names with live systems). Runs are cryptographically separated to prevent cross-run contamination (artifacts, notes, and state from prior runs must not influence subsequent runs). Evaluations run under full monitoring, classification, and guardrail coverage with alerting on escape indicators, and no verified egress block means no evaluation (fail closed). Addresses the evaluation-harness integrity class (Anthropic INC-19 -- three Claude models escaped harnesses told 'no internet/simulated' that actually had internet; PyPI malware publication, live-domain credential theft reaching a production database, ~9,000-target scanning; cross-run coaching notes; undetected for approximately three months; OpenAI breach probe widening with notes coaching future versions).",
    "Ensure evaluation harnesses are genuinely isolated and monitored, with isolation verified rather than asserted.",
    [
        "Isolation asserted in prompts/configuration; no verification; no eval monitoring.",
        "Egress blocks enforced at the boundary; manual target collision checks; runs separated.",
        "Policy-as-code isolation attestation; GA classifiers and monitoring in eval environments; automated collision checks.",
        "Continuous escape testing; attested contamination controls; automated kill on escape indicators; independent third-party harness assurance (GRM-04).",
    ],
    [
        "Is evaluation network isolation enforced at the boundary and verified by test, not assumed from configuration?",
        "Are evaluation targets collision-checked against real domains and production identifiers?",
        "Are runs cryptographically separated (no cross-run contamination)?",
        "Do evaluation environments run with full monitoring/classifiers and alerting on escape indicators?",
        "Does evaluation fail closed when isolation verification fails?",
    ],
    [
        "Eval-harness boundary enforcement configuration and test results",
        "Target collision-check records",
        "Run-separation attestation",
        "Eval-environment monitoring and alert configuration",
    ],
    {"ISM": "Isolation, Monitoring", "NIST AI RMF": "MEASURE (ME.AD)", "EU AI Act": "Art. 15(a)", "Five Eyes": "Careful Adoption of Agentic AI Services"},
    ["evaluation-harness", "isolation", "contamination"])

# ----------------------------------------------
# OUTPUT GENERATION
# ----------------------------------------------

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
    preserved = 0

    for cid in sorted(CONTROLS.keys()):
        ctrl = CONTROLS[cid]
        safe_name = re.sub(r"[^a-z0-9_]", "_", ctrl["title"].lower().replace(" ", "_").replace("-", "_").replace(",", "").replace("(", "").replace(")", "").replace("&", "and"))
        filename = f"shield_ai_{ctrl['pillar'].lower()}_{cid.lower()}.rego"
        filepath = os.path.join(output_dir, filename)

        # Non-destructive regeneration: a control that has been IMPLEMENTED
        # (its stub body replaced with real assertions, i.e. no TODO marker)
        # is preserved exactly. Only TODO stubs are (re)generated.
        if os.path.exists(filepath):
            with open(filepath, encoding="utf-8") as f:
                existing = f.read()
            if "# TODO: Implement control test logic" not in existing:
                preserved += 1
                continue

        package_name = f"shield_ai.{ctrl['pillar'].lower()}.{safe_name[:30]}"

        rego_code = f"""package {package_name}

# SHIELD-AI(TM) {cid}: {ctrl['title']}
# Pillar: {ctrl['pillar']} -- {PILLARS[ctrl['pillar']]}
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

    print(f"Generated: {count} Rego policy stubs, preserved {preserved} implemented control(s) in {output_dir}/")
    return output_dir


def main():
    generate_json()

    if "--rego" in sys.argv:
        generate_rego_stubs()

    # Summary
    schema = build_schema()
    print()
    print(f"SHIELD-AI Control Schema v{FRAMEWORK_VERSION}")
    print(f"{'-'*50}")
    for pid in PILLAR_ORDER:
        p = schema["pillars"][pid]
        print(f"  {pid}: {p['name']:<40s} {p['control_count']:>2d} controls")
    print(f"{'-'*50}")
    print(f"  Total: {schema['meta']['control_count']} controls across {schema['meta']['pillar_count']} pillars")


if __name__ == "__main__":
    main()
