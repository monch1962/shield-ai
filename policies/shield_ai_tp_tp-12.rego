package shield_ai.tp.tool_call_provenance_and_dispa

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

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_12
#     msg := sprintf("TP-12 violation: agent %v does not meet control requirements", [agent.id])
# }
