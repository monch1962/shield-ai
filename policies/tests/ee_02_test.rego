package shield_ai.ee.infrastructure_api_access_cont_test

import rego.v1

import data.shield_ai.ee.infrastructure_api_access_cont.allow

test_registered_tool_allowed if {
    req := {"action": {"tool": "search_documents", "registered_as_tool": true}}
    allow with input as req
}

test_infra_api_without_registration_denied if {
    req := {"action": {"tool": "iam", "registered_as_tool": false}}
    not allow with input as req
}

test_infra_api_missing_registration_fails_closed if {
    req := {"action": {"tool": "s3"}}
    not allow with input as req
}

test_infra_api_explicitly_registered_allowed if {
    req := {"action": {"tool": "kms", "registered_as_tool": true}}
    allow with input as req
}
