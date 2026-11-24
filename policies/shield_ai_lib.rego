package shield_ai.lib

import rego.v1

# SHIELD-AI(TM) shared policy registry
# ====================================
# Authoritative named risk/tool/API sets that controls reference via
# `import data.shield_ai.lib.<set>`. Centralising these means the collector
# (reference-views/13-input-payload-spec.md), the control policies, and the
# exploit/gap coverage all agree on ONE classification -- no duplicated or
# drifted tool lists across policies.
#
# Add new named sets here as controls need them; do NOT re-declare a set
# inline in a control policy.

# Tools that must only ever run from inside the execution boundary (EE-01).
high_risk_tools := {
    "shell_exec",
    "write_file",
    "install_package",
    "transfer_funds",
    "delete_objects",
}

# Tools considered sensitive for baseline-deviation detection (MIR-02).
sensitive_tools := {
    "transfer_funds",
    "write_file",
    "shell_exec",
    "send_email_draft",
    "delete_objects",
}

# Infrastructure control-plane APIs that must be allow-listed per agent (EE-02, TP-08).
infrastructure_apis := {
    "ec2",
    "iam",
    "lambda",
    "s3",
    "kms",
    "cloudformation",
    "azure_rbac",
    "azure_vm",
    "azure_resource_manager",
    "gcp_iam",
    "gcp_compute",
    "gcp_cloud_resource_manager",
}

# Current input-envelope schema version (see reference-views/13-input-payload-spec.md).
SCHEMA_VERSION := "1"

# Envelope version guard. A payload that CARRIES schema_version but disagrees
# with the registry is fabricated or drifted input and must be rejected by
# calling policies. Omitting schema_version is NOT a version failure: a slim
# collector that cannot version its input is left to the individual
# fail-closed rules (doc 13 section 3), never blanket-blocked as a schema
# error. Pure function so policies can `deny` on it and tests can drive it.
bad_schema_version(inp) if {
    inp.schema_version != SCHEMA_VERSION
}

# Missing-field detector for the require_attested convention (doc 13 section 3).
# Returns true when the field at the dotted `path` (array) is UNDEFINED in `inp`.
# A deny that guards safety with `X == false` / `X != true` silently allows a
# payload that omits X; pairing the guard with `field_undefined(input, path)`
# closes that hole, so an un-attestable field fails closed instead of passing.
field_undefined(inp, path) if {
    object.get(inp, path, "__shield_ai_missing__") == "__shield_ai_missing__"
}