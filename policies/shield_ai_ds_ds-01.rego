package shield_ai.ds.data_classification_and_labell

import rego.v1

# SHIELD-AI(TM) DS-01: Data Classification and Labelling
# Pillar: DS -- Data Security
#
# Classify all data entering the AI system at ingestion using an automated pipeline that feeds into downstream encryption, retention, and access controls.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.data = {"classified": bool, "label": string}.
# Fail closed: unclassified data is not ingested into the AI system.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "ingestion"
    not input.data.classified
    msg := "DS-01 deny: data ingestion without automated classification (fail closed)"
}

deny contains msg if {
    input.action.kind == "ingestion"
    not input.data.label
    msg := "DS-01 deny: data ingestion with no classification label"
}

allow if {
    count(deny) == 0
}
