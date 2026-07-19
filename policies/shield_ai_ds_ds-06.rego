package shield_ai.ds.output_validation

# SHIELD-AI™ DS-06: Output Validation
# Pillar: DS — Data Security
#
# Scan all model outputs for data leakage (PII, training data, system prompts, credentials) at the inference proxy layer before delivery to users or systems.
#
# Maturity indicators:
#   L1: No output validation for data leakage.
#   L2: Basic PII scanning on model outputs. Manual review of flagged outputs.
#   L3: Automated output scanning for PII, sensitive data, system prompts, memorised training data. Scanning at application layer.
#   L4: Real-time output scanning with automated blocking. Training data memorisation testing in CI/CD.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM02 (Insecure Output Handling)
#   Privacy Act 1988: APP 11 — data security
#   NIST AI RMF: MEASURE (ME.AD)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.ds_ds_06
#     msg := sprintf("DS-06 violation: agent %v does not meet control requirements", [agent.id])
# }
