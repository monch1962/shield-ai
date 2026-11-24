package shield_ai.attest_test

import rego.v1

import data.shield_ai.lib.attestation_deny
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

# --- attestation_deny: the centralized companion-deny predicate ---
# Returns the fail-closed message only when the field's PARENT context exists
# but the field itself is undefined (a slim collector that never reports the
# context at all is out of scope here and left to the policy's own guards).
test_attestation_deny_fires_on_missing_subfield if {
    attestation_deny(
        {"action": {"egress": {}}},
        "DS-08",
        ["action", "egress"],
        ["action", "egress", "channel_inventoried"],
    ) == "DS-08 deny: missing attestation for input.action.egress.channel_inventoried (unobserved -> fail closed)"
}

test_attestation_deny_silent_when_parent_absent if {
    # no egress context at all -> the deny must NOT fire (non-egress action)
    not attestation_deny(
        {"action": {"kind": "tool_call", "tool": "search_documents"}},
        "DS-08",
        ["action", "egress"],
        ["action", "egress", "channel_inventoried"],
    )
}

test_attestation_deny_silent_when_present if {
    not attestation_deny(
        {"action": {"egress": {"channel_inventoried": true}}},
        "DS-08",
        ["action", "egress"],
        ["action", "egress", "channel_inventoried"],
    )
}

test_attestation_deny_silent_when_false if {
    # field is PRESENT and false: handled by the original ==false deny, not the
    # omission companion, so attestation_deny stays quiet.
    not attestation_deny(
        {"action": {"egress": {"channel_inventoried": false}}},
        "DS-08",
        ["action", "egress"],
        ["action", "egress", "channel_inventoried"],
    )
}