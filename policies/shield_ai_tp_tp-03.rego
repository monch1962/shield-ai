package shield_ai.tp.api_gateway_security

# SHIELD-AI TP-03: API Gateway Security
# Pillar: TP — Tool and Pipeline Security
#
# Deploy a gateway between agents and tools that enforces rate limiting, schema validation, audit logging, and MCP protocol awareness where applicable.
#
# Maturity indicators:
#   L1: No gateway. Agents call tools directly.
#   L2: Basic reverse proxy between agents and tools. Rate limiting configured.
#   L3: Gateway with schema validation, rate limiting, and audit logging. MCP-aware. Fail-closed tested.
#   L4: Intelligent gateway with dynamic rate limiting, anomaly-based blocking, and auto-discovery.
#
# Regulatory mappings:
#   ISM: Guidelines for Gateways, Guidelines for Networking
#   Essential Eight: Application Control

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_03
#     msg := sprintf("TP-03 violation: agent %v does not meet control requirements", [agent.id])
# }
