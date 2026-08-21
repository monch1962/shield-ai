package shield_ai.ms.training_data_integrity

import rego.v1

# SHIELD-AI(TM) MS-02: Training Data Integrity
# Pillar: MS -- Model Security
#
# Ensure training and fine-tuning datasets are verified for integrity, provenance, and freedom from poisoning or corruption before use.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.training = {"provenance_tracked": bool, "sanitised": bool,
# "poison_scan": "clean" | "flagged"}. Fail closed: unverified training data
# never reaches a fine-tune or deployment.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "training_run"
    not input.training.provenance_tracked
    msg := "MS-02 deny: training run with untracked dataset provenance"
}

deny contains msg if {
    input.action.kind == "training_run"
    not input.training.sanitised
    msg := "MS-02 deny: training run with unsanitised dataset (PII or sensitive content)"
}

deny contains msg if {
    input.action.kind == "training_run"
    not (input.training.poison_scan == "clean")
    msg := "MS-02 deny: training run without a clean poison-detection scan (fail closed)"
}

allow if {
    count(deny) == 0
}
