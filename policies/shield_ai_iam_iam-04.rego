package shield_ai.iam.credential_isolation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) IAM-04: Credential Isolation
# Pillar: IAM -- Identity and Access
#
# Store, manage, and rotate agent credentials separately from human credentials with hardware-backed protection for critical agents and automated rotation on compromise signals.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.credentials = {"isolated": bool, "hardware_backed":
# bool}; input.agent.compromised (bool); input.agent.credentials.rotation_triggered
# (bool). Fail closed on missing isolation claims.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["IAM-04"])
}

deny contains msg if {
    not input.agent.credentials.isolated
    msg := sprintf("IAM-04 deny: agent %q credentials not isolated from human credentials", [input.agent.id])
}

deny contains msg if {
    input.agent.compromised == true
    not input.agent.credentials.rotation_triggered
    msg := sprintf("IAM-04 deny: agent %q compromise signal without credential rotation", [input.agent.id])
}

allow if {
    count(deny) == 0
}
