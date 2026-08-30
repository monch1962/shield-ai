package shield_ai.tp.agent_dependency_install_prove

# SHIELD-AI(TM) TP-13: Agent Dependency-Install Provenance Verification
# Pillar: TP -- Tool and Pipeline Security
#
# Verify registry-namespace and domain-ownership provenance before any agent-executed install derived from ingested content.
#
# Maturity indicators:
#   L1: Agents execute install commands found in documentation or llms.txt verbatim with no namespace checks.
#   L2: Install commands from ingested content run, but package/domain existence is only checked post-hoc.
#   L3: Pre-install provenance verification: registry existence, namespace ownership, domain registration; installs from untrusted content gated by an allowlist or human approval; dangling references blocked and logged via MIR-01.
#   L4: Continuous verification against live registry state; automated blocking of dangling references; documentation files never treated as authoritative install scripts; red-team testing of the docs-to-install path.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for Gateways

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_13
#     msg := sprintf("TP-13 violation: agent %v does not meet control requirements", [agent.id])
# }
