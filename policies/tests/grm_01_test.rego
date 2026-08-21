package shield_ai.grm.ai_governance_body_test

import rego.v1

import data.shield_ai.grm.ai_governance_body.allow

test_chartered_body_deployment_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "body": {
      "chartered": true,
      "cross_functional": true,
      "decision_authority": true
    }
  }
}
    allow with input as req
}

test_unchartered_body_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "body": {
      "chartered": false,
      "cross_functional": true,
      "decision_authority": true
    }
  }
}
    not allow with input as req
}

test_not_cross_functional_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "body": {
      "chartered": true,
      "cross_functional": false,
      "decision_authority": true
    }
  }
}
    not allow with input as req
}

test_no_decision_authority_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "governance": {
    "body": {
      "chartered": true,
      "cross_functional": true,
      "decision_authority": false
    }
  }
}
    not allow with input as req
}

test_non_deployment_action_not_gated if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents"
  }
}
    allow with input as req
}
