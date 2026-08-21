package shield_ai.grm.ethical_use_policy_test

import rego.v1

import data.shield_ai.grm.ethical_use_policy.allow

test_acceptable_action_allowed if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "acceptable": true
  }
}
    allow with input as req
}

test_unacceptable_action_denied if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "acceptable": false
  }
}
    not allow with input as req
}

test_high_risk_without_hitl_denied if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "tool_call",
    "tool": "transfer_funds",
    "acceptable": true,
    "high_risk_class": "financial"
  },
  "governance": {
    "policy": {
      "hitl_by_risk": false
    }
  }
}
    not allow with input as req
}

test_high_risk_with_hitl_allowed if {
    req := {
  "agent": {
    "id": "a1"
  },
  "action": {
    "kind": "tool_call",
    "tool": "transfer_funds",
    "acceptable": true,
    "high_risk_class": "financial"
  },
  "governance": {
    "policy": {
      "hitl_by_risk": true
    }
  }
}
    allow with input as req
}
