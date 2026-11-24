package shield_ai.grm.third_party_ai_risk_management

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) GRM-04: Third-Party AI Risk Management
# Pillar: GRM -- Governance and Risk Management
#
# Assess and monitor third-party AI providers for security controls, with contractual security requirements and right-to-audit provisions in all AI-related procurement.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Irregular
# evaluation-vendor pattern INC-26; eval vendors are critical suppliers).
# Input model: input.vendors = {"assessed": bool, "contractual_controls": bool,
# "right_to_audit": bool}; input.action.vendor_used (bool);
# input.action.vendor_type ("evaluation" | "model" | "tool" | other).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["GRM-04"])
}

deny contains msg if {
    input.action.vendor_used == true
    not input.vendors.assessed
    msg := sprintf("GRM-04 deny: action using third-party vendor %q without security assessment", [input.vendors.name])
}

deny contains msg if {
    input.action.vendor_used == true
    not input.vendors.contractual_controls
    msg := sprintf("GRM-04 deny: vendor %q without contractual security control obligations", [input.vendors.name])
}

deny contains msg if {
    input.action.vendor_type == "evaluation"
    not input.vendors.right_to_audit
    msg := sprintf("GRM-04 deny: evaluation vendor %q without right-to-audit (harness egress must be independently verified, never self-attested)", [input.vendors.name])
}

allow if {
    count(deny) == 0
}
