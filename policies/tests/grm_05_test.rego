package shield_ai.grm.regulatory_mapping_and_complia_test

import rego.v1

import data.shield_ai.grm.regulatory_mapping_and_complia.allow

test_mapped_deployment_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "compliance": {
      "mapped": true,
      "quarterly_reported": true
    }
  }
}
    allow with input as req
}

test_unmapped_deployment_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "compliance": {
      "mapped": false,
      "quarterly_reported": true
    }
  }
}
    not allow with input as req
}

test_not_quarterly_reported_denied if {
    req := {
  "action": {
    "kind": "tool_call"
  },
  "governance": {
    "compliance": {
      "mapped": true,
      "quarterly_reported": false
    }
  }
}
    not allow with input as req
}
