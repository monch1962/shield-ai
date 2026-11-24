package shield_ai.ms.model_weight_protection

import rego.v1

import data.shield_ai.lib.bad_schema_version
import data.shield_ai.lib.field_undefined

# SHIELD-AI(TM) MS-01: Model Weight Protection
# Pillar: MS -- Model Security
#
# Ensure model weights are protected against exfiltration, cloning, and inversion attacks through encryption, access control, and integrity verification.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.model = {"weights_encrypted": bool,
# "key_management": "hsm" | "cloud_kms" | "none"}.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-01"])
}

deny contains msg if {
    input.model.weights_encrypted != true
    msg := sprintf("MS-01 deny: model %q weights not encrypted at rest and in transit", [input.model.id])
}

deny contains msg if {
    field_undefined(input, ["model", "weights_encrypted"])
    msg := sprintf("MS-01 deny: model %q encryption attestation missing (unobserved -> fail closed)", [input.model.id])
}

deny contains msg if {
    input.model.key_management == "none"
    msg := sprintf("MS-01 deny: model %q weights lack key management (HSM or cloud KMS required)", [input.model.id])
}

allow if {
    count(deny) == 0
}