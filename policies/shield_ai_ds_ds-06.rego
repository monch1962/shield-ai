package shield_ai.ds.output_validation

import rego.v1

# SHIELD-AI(TM) DS-06: Output Validation
# Pillar: DS -- Data Security
#
# Scan all model outputs for data leakage (PII, training data, system prompts, credentials) at the inference proxy layer before delivery to users or systems.
#
# Maturity indicators:
#   L1: No output validation for data leakage.
#   L2: Basic PII scanning on model outputs. Manual review of flagged outputs.
#   L3: Automated output scanning for PII, sensitive data, system prompts, memorised training data. Scanning at application layer.
#   L4: Real-time output scanning with automated blocking. Training data memorisation testing in CI/CD.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.output_scan = "clean" | "leak" | "pending".
# Fail closed: no scan result means no delivery.

deny contains msg if {
    input.action.kind == "output_delivery"
    not (input.action.output_scan == "clean")
    msg := "DS-06 deny: output not verified clean by the leakage scanner (fail closed)"
}

deny contains msg if {
    input.action.output_scan == "leak"
    msg := "DS-06 deny: output flagged for data leakage (PII, training data, system prompt, or credential)"
}

allow if {
    count(deny) == 0
}
