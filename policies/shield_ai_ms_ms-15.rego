package shield_ai.ms.cross_tenant_agent_memory_and_

# SHIELD-AI(TM) MS-15: Cross-Tenant Agent Memory and State Isolation
# Pillar: MS -- Model Security
#
# Isolate multi-tenant agent memory and state per tenant as a hard boundary; keep the isolation key out of model control and gate retrieval/write by verified ownership.
#
# Maturity indicators:
#   L1: Shared/pooled vector store with soft metadata ownership and LLM-controllable namespace keys; cross-tenant reach demonstrable.
#   L2: Per-tenant partitioning or post-retrieval ownership gate applied; namespace keys removed from the tool schema; cross-user reach monitored.
#   L3: Hard post-retrieval and post-write ownership gating with default-deny; connection parameters bound at construction; cross-tenant hits alarmed as control violations.
#   L4: Memory isolation fail-closed and continuously exercised; cross-tenant write attempts denied and alarmed; pooled-store deployments require hard partitioning or ownership gating.
#
# Regulatory mappings:
#   OWASP: LLM12 (Memory Poisoning, cross-tenant variant)
#   NIST AI RMF: GOVERN + PROTECT (PR.AC)
#   EU AI Act: Art. 10 (Data Governance)
#   ISM: Guidelines for Cryptography and Data Protection
#   Essential Eight: Restrict Administrative Privileges

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.ms_ms_15
#     msg := sprintf("MS-15 violation: agent %v does not meet control requirements", [agent.id])
# }
