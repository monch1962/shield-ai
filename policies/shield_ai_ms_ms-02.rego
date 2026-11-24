package shield_ai.ms.training_data_integrity

import rego.v1

import data.shield_ai.lib.bad_schema_version

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

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-02"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "training_run"
}


deny contains msg if {
    applicable
    not input.training.provenance_tracked
    msg := "MS-02 deny: training run with untracked dataset provenance"
}

deny contains msg if {
    applicable
    not input.training.sanitised
    msg := "MS-02 deny: training run with unsanitised dataset (PII or sensitive content)"
}

deny contains msg if {
    applicable
    not (input.training.poison_scan == "clean")
    msg := "MS-02 deny: training run without a clean poison-detection scan (fail closed)"
}

allow if {
    count(deny) == 0
}
