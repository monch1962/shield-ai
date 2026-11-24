package shield_ai.tp.tool_output_validation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) TP-04: Tool Output Validation
# Pillar: TP -- Tool and Pipeline Security
#
# Validate all tool outputs against known-good schemas before passing to agent context, with content-type verification, size limits, and sandboxed execution for code-generation tools.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.tool_output = {"validated": bool, "sanitised": bool,
# "within_size_limit": bool}; input.action.tool_output.code_generation (bool);
# input.action.tool_output.code_sandboxed (bool).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["TP-04"])
}

deny contains msg if {
    not input.action.tool_output.validated
    msg := sprintf("TP-04 deny: tool %q output not validated against a known-good schema", [input.action.tool])
}

deny contains msg if {
    not input.action.tool_output.sanitised
    msg := sprintf("TP-04 deny: tool %q output not sanitised before entering agent context", [input.action.tool])
}

deny contains msg if {
    not input.action.tool_output.within_size_limit
    msg := sprintf("TP-04 deny: tool %q output exceeds the size limit", [input.action.tool])
}

deny contains msg if {
    input.action.tool_output.code_generation == true
    not input.action.tool_output.code_sandboxed
    msg := sprintf("TP-04 deny: code-generation output of tool %q not executed in a sandbox", [input.action.tool])
}

allow if {
    count(deny) == 0
}
