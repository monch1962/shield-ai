package shield_ai.tp.in_process_code_execution_sand

# SHIELD-AI(TM) TP-15: In-Process Code-Execution Sandbox Sufficiency
# Pillar: TP -- Tool and Pipeline Security
#
# Route all LLM-generated or untrusted code execution to an OS/VM-isolated execution environment; never rely on an in-process denylist/blocklist interpreter gate as the boundary.
#
# Maturity indicators:
#   L1: Agent frameworks run LLM-generated code in an in-process denylist/blocklist sandbox as the sole containment; host code-execution primitives reachable.
#   L2: Code-execution tools identified and routed to an OS/VM-level sandbox (EE-01); in-process gates flagged and scheduled for replacement.
#   L3: In-process sandboxes locked in the HIGH-RISK dependency class (TP-06) with automated blocking on critical findings; model-generated code executes only in the EE sandbox.
#   L4: No in-process gate deployed for untrusted code; all model-generated execution is OS/VM-isolated with provenance receipts (TP-12); red-teamed object-graph bypass attempts in CI.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for Software Development, Application Control

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_15
#     msg := sprintf("TP-15 violation: agent %v does not meet control requirements", [agent.id])
# }
