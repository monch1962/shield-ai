package shield_ai.ee.infrastructure_api_access_cont

# SHIELD-AI(TM) EE-02: Infrastructure API Access Control
# Pillar: EE -- Execution Environment
#
# Ensure agents cannot reach infrastructure control planes implicitly.
#
# Maturity indicators:
#   L1: Agents inherit infrastructure credentials or can reach control planes.
#   L2: Infrastructure credentials not mounted; network path blocked but untested.
#   L3: Explicit tool registration required for infrastructure access; metadata service disabled; blocked attempts logged.
#   L4: Continuous verification of credential scoping; automated alerting on any infrastructure API attempt.
#
# Regulatory mappings:
#   ISM: Guidelines for Gateways
#   NIST AI RMF: PROTECT (PR.AC)
#   EU AI Act: Art. 15(b)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.ee_ee_02
#     msg := sprintf("EE-02 violation: agent %v does not meet control requirements", [agent.id])
# }
