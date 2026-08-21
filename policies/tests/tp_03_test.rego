package shield_ai.tp.api_gateway_security_test

import rego.v1

import data.shield_ai.tp.api_gateway_security.allow

test_gateway_controlled_call_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "rate_limited": true,
      "schema_validated": true,
      "audited": true
    }
  }
}
    allow with input as req
}

test_unrate_limited_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "rate_limited": false,
      "schema_validated": true,
      "audited": true
    }
  }
}
    not allow with input as req
}

test_unvalidated_payload_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "rate_limited": true,
      "schema_validated": false,
      "audited": true
    }
  }
}
    not allow with input as req
}

test_unaudited_call_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "gateway": {
      "rate_limited": true,
      "schema_validated": true,
      "audited": false
    }
  }
}
    not allow with input as req
}
