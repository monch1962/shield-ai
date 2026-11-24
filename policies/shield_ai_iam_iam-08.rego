package shield_ai.iam.credential_scope_narrowing

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) IAM-08: Credential Scope Narrowing
# Pillar: IAM -- Identity and Access
#
# Ensure credentials in agent environments are minimal, short-lived, and revocable.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.credentials = {"per_tool_scope": bool,
# "broad_role": bool, "short_lived": bool}. Broad service roles are denied;
# credentials without per-tool scope or short lifetimes fail closed.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["IAM-08"])
}

deny contains msg if {
    input.agent.credentials.broad_role == true
    msg := sprintf("IAM-08 deny: agent %q holds a broad service role instead of per-tool scoped credentials", [input.agent.id])
}

deny contains msg if {
    not input.agent.credentials.per_tool_scope
    msg := sprintf("IAM-08 deny: agent %q credentials are not scoped per registered tool", [input.agent.id])
}

deny contains msg if {
    not input.agent.credentials.short_lived
    msg := sprintf("IAM-08 deny: agent %q credentials are not short-lived", [input.agent.id])
}

allow if {
    count(deny) == 0
}
