package shield_ai.grm.ai_risk_register

import rego.v1

# SHIELD-AI(TM) GRM-02: AI Risk Register
# Pillar: GRM -- Governance and Risk Management
#
# Maintain a dedicated AI risk register using a threat taxonomy that covers model, tool, data, identity, and pipeline risks, with defined owners, assessment methodology, and review cadence.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (G19 escalation:
# AI-speed campaign response and the exercised kill-switch are evidenced
# requirements, INC-23/35/36).
# Input model: input.governance.risk = {"registered": bool,
# "kill_switch_tested": bool}; input.action.high_risk_class (string).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.high_risk_class
    not input.governance.risk.registered
    msg := sprintf("GRM-02 deny: %s action not registered in the AI risk register", [input.action.high_risk_class])
}

deny contains msg if {
    input.action.high_risk_class
    not input.governance.risk.kill_switch_tested
    msg := "GRM-02 deny: kill-switch capability not exercised (AI-speed response requires one rehearsed red button)"
}

allow if {
    count(deny) == 0
}
