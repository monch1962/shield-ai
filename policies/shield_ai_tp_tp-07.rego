package shield_ai.tp.cross_tool_dependency_analysis

import rego.v1

# SHIELD-AI(TM) TP-07: Cross-Tool Dependency Analysis
# Pillar: TP -- Tool and Pipeline Security
#
# Detect and gate escape-class tool combinations before deployment.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (tool-chain
# escalation INC-01/04).
# Input model: input.tools = {"chain_analysed": bool, "escape_chain": bool,
# "risk_accepted": bool}. Tool combinations that enable a multi-step escape
# chain are denied unless explicitly risk-accepted via GRM-02.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "deployment"
    not input.tools.chain_analysed
    msg := "TP-07 deny: deployment without cross-tool dependency (transitive risk) analysis"
}

deny contains msg if {
    input.tools.escape_chain == true
    not input.tools.risk_accepted
    msg := "TP-07 deny: tool combination enables an escape-class chain without explicit risk acceptance (GRM-02)"
}

allow if {
    count(deny) == 0
}
