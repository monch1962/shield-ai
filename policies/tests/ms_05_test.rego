package shield_ai.ms.model_behaviour_validation_test

import rego.v1

import data.shield_ai.ms.model_behaviour_validation.allow

test_guardrailed_output_allowed if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "output_delivery",
    "guardrail_evaluated": true,
    "scope_compliant": true
  }
}
    allow with input as req
}

test_unguardrailed_output_denied if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "output_delivery",
    "scope_compliant": true
  }
}
    not allow with input as req
}

test_out_of_scope_output_denied if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "output_delivery",
    "guardrail_evaluated": true,
    "scope_compliant": false
  }
}
    not allow with input as req
}
