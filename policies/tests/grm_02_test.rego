package shield_ai.grm.ai_risk_register_test

import rego.v1

import data.shield_ai.grm.ai_risk_register.allow

test_low_risk_action_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents"
  }
}
    allow with input as req
}

test_unregistered_high_risk_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "transfer_funds",
    "high_risk_class": "financial"
  },
  "governance": {
    "risk": {
      "registered": false,
      "kill_switch_tested": true
    }
  }
}
    not allow with input as req
}

test_registered_high_risk_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "transfer_funds",
    "high_risk_class": "financial"
  },
  "governance": {
    "risk": {
      "registered": true,
      "kill_switch_tested": true
    }
  }
}
    allow with input as req
}

test_untested_kill_switch_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "transfer_funds",
    "high_risk_class": "financial"
  },
  "governance": {
    "risk": {
      "registered": true,
      "kill_switch_tested": false
    }
  }
}
    not allow with input as req
}
