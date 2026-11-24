package shield_ai.ms.supply_chain_security

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) MS-03: Supply Chain Security
# Pillar: MS -- Model Security
#
# Verify the provenance and integrity of model weights, ML libraries, training infrastructure, and deployment tooling throughout the AI supply chain.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.model.supply_chain = {"sbom": bool, "signature_verified": bool,
# "checkpoint_signed": bool}. Fail closed: unsigned or uninventoried artifacts
# are not deployed.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-03"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "model_deploy"
}


deny contains msg if {
    applicable
    not input.model.supply_chain.sbom
    msg := sprintf("MS-03 deny: model %q deployed without an ML component SBOM", [input.model.id])
}

deny contains msg if {
    applicable
    not input.model.supply_chain.signature_verified
    msg := sprintf("MS-03 deny: model %q provenance signature not verified", [input.model.id])
}

deny contains msg if {
    applicable
    not input.model.supply_chain.checkpoint_signed
    msg := sprintf("MS-03 deny: model %q checkpoints not signed", [input.model.id])
}

allow if {
    count(deny) == 0
}
