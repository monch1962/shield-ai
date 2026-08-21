package shield_ai.tp.tool_call_provenance_and_dispa

import rego.v1

# SHIELD-AI(TM) TP-12: Tool-Call Provenance and Dispatch Verification
# Pillar: TP -- Tool and Pipeline Security
#
# Ensure no tool executes without verified provenance from an authorised model turn or caller.
#
# Maturity indicators:
#   L1: Dispatch executes any data shaped like a tool call; no provenance checks.
#   L2: Tool calls carry basic session identifiers; dispatch verifies call structure only.
#   L3: Tool calls carry cryptographically bound provenance (session, turn, model signature) verified before dispatch; session/event history authenticated; approval records bind to tool name and arguments and verify against the human approver channel; fail closed on unverifiable provenance.
#   L4: Continuous provenance attestation on all dispatches; red-team testing of the dispatch layer (CoreBreak class); automated blocking of provenance-less tool calls across all harnesses and MCP servers.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.AC)
#   EU AI Act: Art. 14(b)
#   ISM: Guidelines for Gateways
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (CoreBreak
# CVE-2026-18830 / CVE-2026-18236 / CVE-2026-64650-51, INC-34).
# Input model: input.action.kind == "dispatch"; input.action.provenance =
# {"session": string, "turn": string, "model_sig": string};
# input.approval = {"present": bool, "bound_tool": string}.
# Fail closed: no provenance, no dispatch. Approval records must bind to the
# exact tool being dispatched (forged-approval class).

deny contains msg if {
    input.action.kind == "dispatch"
    not input.action.provenance.session
    msg := "TP-12 deny: dispatch without session provenance (fail closed)"
}

deny contains msg if {
    input.action.kind == "dispatch"
    not input.action.provenance.turn
    msg := "TP-12 deny: dispatch without turn provenance (fail closed)"
}

deny contains msg if {
    input.action.kind == "dispatch"
    not input.action.provenance.model_sig
    msg := "TP-12 deny: dispatch without model signature (fail closed)"
}

deny contains msg if {
    input.action.kind == "dispatch"
    input.approval.present == true
    input.approval.bound_tool != input.action.tool
    msg := sprintf("TP-12 deny: approval bound to %q does not match dispatched tool %q (forged-approval class)", [input.approval.bound_tool, input.action.tool])
}

allow if {
    count(deny) == 0
}
