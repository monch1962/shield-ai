package shield_ai.tp.explicit_tool_registration

import rego.v1

# SHIELD-AI(TM) TP-09: Explicit Tool Registration
# Pillar: TP -- Tool and Pipeline Security
#
# Eliminate implicit tool exposure in agent frameworks.
#
# Maturity indicators:
#   L1: Frameworks auto-expose internal functions; no registry enforcement.
#   L2: Explicit registry for critical tools; auto-registration partially disabled.
#   L3: Auto-registration disabled by default; all callables audited; unregistered callables blocked.
#   L4: Continuous callable-audit in CI/CD; automated blocking of implicitly exposed tools.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: IDENTIFY (ID.AM)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Semantic Kernel /
# .NET SDK implicit exposure, INC-17).
# Input model: input.action.kind in {"tool_call","dispatch"};
# input.action.registration ("explicit" | "auto"); input.action.tool.
# Fail closed: a tool invocation without explicit registration is denied.

deny contains msg if {
    input.action.kind in {"tool_call", "dispatch"}
    not (input.action.registration == "explicit")
    msg := sprintf("TP-09 deny: tool %q was not explicitly registered (implicit exposure class)", [input.action.tool])
}

deny contains msg if {
    input.action.registration == "auto"
    msg := sprintf("TP-09 deny: tool %q auto-registered by framework mechanism; explicit registration required", [input.action.tool])
}

allow if {
    count(deny) == 0
}
