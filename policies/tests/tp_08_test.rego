package shield_ai.tp.api_gateway_infrastructure_iso_test

import rego.v1

import data.shield_ai.tp.api_gateway_infrastructure_iso.allow

test_allowlisted_tool_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "allowlist_active": true,
      "infra_isolation": true
    }
  }
}
    allow with input as req
}

test_allowlist_inactive_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "allowlist_active": false,
      "infra_isolation": true
    }
  }
}
    not allow with input as req
}

test_infra_api_not_blocked_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "iam",
    "gateway": {
      "allowlist_active": true,
      "infra_isolation": false
    }
  }
}
    not allow with input as req
}

test_infra_api_missing_isolation_fails_closed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "s3",
    "gateway": {
      "allowlist_active": true
    }
  }
}
    not allow with input as req
}
