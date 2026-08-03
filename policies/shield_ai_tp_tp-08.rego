package shield_ai.tp.api_gateway_infrastructure_iso

# SHIELD-AI(TM) TP-08: API Gateway Infrastructure-Isolation Mode
# Pillar: TP -- Tool and Pipeline Security
#
# Prevent agents from reaching cloud infrastructure control planes.
#
# Maturity indicators:
#   L1: Agents can reach infrastructure APIs directly or via default routing.
#   L2: Gateway present; infrastructure APIs blocked by policy but untested.
#   L3: Explicit allow-list excluding control-plane APIs; blocked attempts logged and alerted.
#   L4: Continuous testing of the allow-list against provider endpoint inventories; automated block-list updates.
#
# Regulatory mappings:
#   ISM: Guidelines for Gateways
#   NIST AI RMF: PROTECT (PR.PT)
#   EU AI Act: Art. 15(b)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_08
#     msg := sprintf("TP-08 violation: agent %v does not meet control requirements", [agent.id])
# }
