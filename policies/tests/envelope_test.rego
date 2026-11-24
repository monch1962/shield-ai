package shield_ai.envelope_test

import rego.v1

import data.shield_ai.lib.bad_schema_version

# The envelope version guard lives in the shared registry as a PURE function
# (bad_schema_version(input)) so policies can deny with it and tests can drive
# it directly. A payload that CARRIES a schema_version disagreeing with the
# registry is fabricated or drifted and must be rejected; omitting the field
# is not a version failure (fail-closed is handled by the rules themselves,
# per doc 13 section 3).
test_match_version_ok if {
    not bad_schema_version({"schema_version": "1"})
}

test_wrong_major_mismatch if {
    bad_schema_version({"schema_version": "0"})
}

test_wrong_minor_mismatch if {
    bad_schema_version({"schema_version": "1.0"})
}

test_missing_is_no_version_failure if {
    not bad_schema_version({})
}