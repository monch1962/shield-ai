package shield_ai.grm.ai_governance_body

import rego.v1

# SHIELD-AI(TM) GRM-01: AI Governance Body
# Pillar: GRM -- Governance and Risk Management
#
# Establish and charter an AI governance body with cross-functional membership (CISO, CRO, GC, data owner, AI lead) and defined decision authority over agentic AI deployments.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.governance.body = {"chartered": bool, "cross_functional":
# bool, "decision_authority": bool}. High-risk deployments require an active,
# chartered governance body.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "deployment"
    not input.governance.body.chartered
    msg := "GRM-01 deny: deployment without a chartered AI governance body"
}

deny contains msg if {
    input.action.kind == "deployment"
    not input.governance.body.cross_functional
    msg := "GRM-01 deny: AI governance body lacks cross-functional membership (CISO, CRO, GC, data owner, AI lead)"
}

deny contains msg if {
    input.action.kind == "deployment"
    not input.governance.body.decision_authority
    msg := "GRM-01 deny: AI governance body has no defined decision authority over agentic AI deployments"
}

allow if {
    count(deny) == 0
}
