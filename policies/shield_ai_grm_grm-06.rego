package shield_ai.grm.board_and_executive_reporting

import rego.v1

# SHIELD-AI(TM) GRM-06: Board and Executive Reporting
# Pillar: GRM -- Governance and Risk Management
#
# Provide a standardised executive dashboard showing pillar maturity scores, open findings, regulatory compliance status, and risk acceptances, refreshed automatically.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.governance.reporting = {"dashboard": bool,
# "risk_acceptance_logged": bool}; input.governance.risk_acceptance (bool) --
# a risk acceptance decision was recorded this cycle.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.governance.reporting.dashboard
    msg := "GRM-06 deny: no executive dashboard for AI security posture (maturity, findings, compliance, risk acceptances)"
}

deny contains msg if {
    input.governance.risk_acceptance == true
    not input.governance.reporting.risk_acceptance_logged
    msg := "GRM-06 deny: risk acceptance decision not logged in the executive reporting trail"
}

allow if {
    count(deny) == 0
}
