package shield_ai.ds.data_minimisation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) DS-04: Data Minimisation
# Pillar: DS -- Data Security
#
# Filter data at the retrieval layer (field-level, not document-level) and enforce attribute-based access control at query time to ensure agents receive only the minimum data required.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.data.access = {"bulk": bool, "field_filtered": bool,
# "abac_enforced": bool}. Bulk data access is denied; retrieval without
# field-level filtering or ABAC fails closed.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["DS-04"])
}

deny contains msg if {
    input.data.access.bulk == true
    msg := "DS-04 deny: bulk data access by agent (field-level filtering required)"
}

deny contains msg if {
    input.action.kind == "retrieval"
    not input.data.access.field_filtered
    msg := "DS-04 deny: retrieval without field-level filtering (document-level only)"
}

deny contains msg if {
    input.action.kind == "retrieval"
    not input.data.access.abac_enforced
    msg := "DS-04 deny: retrieval without attribute-based access control at query time"
}

allow if {
    count(deny) == 0
}
