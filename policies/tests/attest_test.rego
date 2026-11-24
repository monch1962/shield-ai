package shield_ai.attest_test

import rego.v1

import data.shield_ai.lib.field_undefined

# A fail-closed deny that uses `X == false` (or `X != true`) silently ALLOWS a
# payload that OMITS X -- undefined != true is not a failing condition in OPA.
# The require_attested convention closes that hole by denying when the field is
# undefined, so a collector that cannot attest the field fails closed.
test_omitted_field_is_undefined if {
    field_undefined({"model": {"id": "m1"}}, ["model", "weights_encrypted"])
}

test_present_field_not_undefined if {
    not field_undefined({"model": {"weights_encrypted": true}}, ["model", "weights_encrypted"])
}

test_false_is_not_undefined if {
    not field_undefined({"model": {"weights_encrypted": false}}, ["model", "weights_encrypted"])
}

test_deep_omitted if {
    field_undefined({"agent": {"id": "a1"}}, ["agent", "sandbox_attestation", "present"])
}