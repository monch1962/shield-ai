package shield_ai.ds.data_minimisation

# SHIELD-AI DS-04: Data Minimisation
# Pillar: DS — Data Security
#
# Filter data at the retrieval layer (field-level, not document-level) and enforce attribute-based access control at query time to ensure agents receive only the minimum data required.
#
# Maturity indicators:
#   L1: Full documents passed to model context. No data filtering at retrieval.
#   L2: Basic excerpt extraction. Tool response limits configured.
#   L3: Field-level filtering. ABAC at retrieval. Tool response minimisation enforced.
#   L4: Dynamic minimisation based on task context and sensitivity. Continuous monitoring of effectiveness.
#
# Regulatory mappings:
#   Privacy Act 1988: APP 3 — Collection of solicited personal information, APP 11
#   NIST AI RMF: IDENTIFY (ID.DA)
#   EU AI Act: Art. 10(2) — Data Governance

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.ds_ds_04
#     msg := sprintf("DS-04 violation: agent %v does not meet control requirements", [agent.id])
# }
