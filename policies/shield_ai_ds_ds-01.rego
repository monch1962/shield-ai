package shield_ai.ds.data_classification_and_labell

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) DS-01: Data Classification and Labelling
# Pillar: DS -- Data Security
#
# Classify all data entering the AI system at ingestion using an automated pipeline that feeds into downstream encryption, retention, and access controls.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.data = {"classified": bool, "label": string}.
# Fail closed: unclassified data is not ingested into the AI system.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["DS-01"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "ingestion"
}


deny contains msg if {
    applicable
    not input.data.classified
    msg := "DS-01 deny: data ingestion without automated classification (fail closed)"
}

deny contains msg if {
    applicable
    not input.data.label
    msg := "DS-01 deny: data ingestion with no classification label"
}

allow if {
    count(deny) == 0
}
