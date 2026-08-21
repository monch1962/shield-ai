package shield_ai.grm.regulatory_mapping_and_complia

import rego.v1

# SHIELD-AI(TM) GRM-05: Regulatory Mapping and Compliance Reporting
# Pillar: GRM -- Governance and Risk Management
#
# Maintain an automated mapping of SHIELD-AI controls to applicable regulatory frameworks with continuous compliance monitoring and regular reporting.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.governance.compliance = {"mapped": bool,
# "quarterly_reported": bool}. Compliance posture must be machine-mapped and
# reported on the framework's cadence.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "deployment"
    not input.governance.compliance.mapped
    msg := "GRM-05 deny: deployment without an automated regulatory mapping (ISM, E8, SOCI, CPS 234, PSPF, Privacy Act)"
}

deny contains msg if {
    not input.governance.compliance.quarterly_reported
    msg := "GRM-05 deny: compliance posture not reported on the quarterly cadence"
}

allow if {
    count(deny) == 0
}
