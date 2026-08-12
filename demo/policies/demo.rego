package shield_ai.demo

# ============================================================================
# SHIELD-AI demo entrypoint: deny-override evaluation of agent actions.
#
# This is a REDUCED demo bundle for prospect self-run. It mirrors three real
# controls (MS-04 adversarial robustness, TP-01 tool registry, EE-01 execution
# boundary) plus the framework's core evaluation rule: ANY deny wins over any
# allow, and the system fails closed. Full control logic lives in policies/
# at the repo root; this bundle exists to be runnable in five minutes.
# ============================================================================

import rego.v1

# ---------------------------------------------------------------------------
# Allow path: the action is permitted only if every control passes.
# Note: deny is a SET rule, so it is always defined (empty when clean).
# `not deny` would never fire; compare its size instead.
# ---------------------------------------------------------------------------
allow if {
    count(deny) == 0
}

# ---------------------------------------------------------------------------
# MS-04: adversarial robustness -- reject prompt-injection content.
# The agent acts on content it read; injection markers in that content mean
# the action was not what the user asked for.
# ---------------------------------------------------------------------------
deny contains msg if {
    some item in input.context.content
    some marker in injection_markers
    contains(item, marker)
    msg := sprintf("MS-04 deny: prompt-injection marker %q found in agent-visible content", [marker])
}

injection_markers := {
    "ignore previous instructions",
    "ignore all prior instructions",
    "you are now",
    "disregard your instructions",
    "system prompt:",
    "new system prompt",
}

# ---------------------------------------------------------------------------
# TP-01: tool registry -- the agent may only call registered, approved tools.
# ---------------------------------------------------------------------------
deny contains msg if {
    not input.action.tool in registered_tools
    msg := sprintf("TP-01 deny: tool %q is not in the approved tool registry", [input.action.tool])
}

registered_tools := {
    "search_documents",
    "send_email_draft",
    "read_calendar",
    "create_meeting",
    "summarise_thread",
}

# ---------------------------------------------------------------------------
# EE-01: execution boundary -- high-risk actions require a sandboxed agent.
# Fail closed: absence of a sandbox attestation is a deny, not a question.
# ---------------------------------------------------------------------------
deny contains msg if {
    input.action.tool in high_risk_tools
    not input.agent.sandboxed
    msg := sprintf("EE-01 deny: tool %q is high-risk and agent %q is not sandboxed", [input.action.tool, input.agent.id])
}

high_risk_tools := {
    "shell_exec",
    "write_file",
    "install_package",
    "transfer_funds",
}

# ---------------------------------------------------------------------------
# Deny-override proof: an allow that passes while a deny also fires must lose.
# This rule documents the framework's evaluation semantics for the demo.
# ---------------------------------------------------------------------------
# allow_if_registered = true would pass TP-01 alone, but MS-04/EE-01 denials
# still win. The client evaluates `allow` (deny-override), so a single deny
# blocks the action regardless of how many other checks pass.
