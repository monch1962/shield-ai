package shield_ai.grm.third_party_ai_risk_management

# SHIELD-AI™ GRM-04: Third-Party AI Risk Management
# Pillar: GRM — Governance and Risk Management
#
# Assess and monitor third-party AI providers for security controls, with contractual security requirements and right-to-audit provisions in all AI-related procurement.
#
# Maturity indicators:
#   L1: No third-party AI risk assessment. Providers used without evaluation.
#   L2: Basic vendor assessments for model providers. Contractual requirements in some contracts.
#   L3: Comprehensive vendor assessment programme for all AI providers. Right-to-audit. Ongoing monitoring.
#   L4: Continuous vendor security monitoring. Automated vendor risk scoring. Vendor decommissioning playbooks exercised.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM10 (Supply Chain)
#   NIST AI RMF: IDENTIFY (ID.SC)
#   ISM: Guidelines for Procurement and Outsourcing
#   EU AI Act: Art. 28 — Third Parties

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.grm_grm_04
#     msg := sprintf("GRM-04 violation: agent %v does not meet control requirements", [agent.id])
# }
