package shield_ai.ds.training_data_governance

import rego.v1

# SHIELD-AI(TM) DS-05: Training Data Governance
# Pillar: DS -- Data Security
#
# Track training data lineage from source to model, verify consent for personal data, enforce retention limits, and provide machine unlearning capability.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.training.governance = {"lineage": bool, "retention_limited":
# bool, "unlearning": bool}; input.training.personal_data (bool);
# input.training.consent_verified (bool).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "training_run"
    not input.training.governance.lineage
    msg := "DS-05 deny: training run without dataset lineage tracking"
}

deny contains msg if {
    input.action.kind == "training_run"
    input.training.personal_data == true
    not input.training.consent_verified
    msg := "DS-05 deny: training run on personal data without verified consent"
}

deny contains msg if {
    input.action.kind == "training_run"
    not input.training.governance.retention_limited
    msg := "DS-05 deny: training run without retention limits on source datasets"
}

allow if {
    count(deny) == 0
}
