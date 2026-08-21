package shield_ai.grm.third_party_ai_risk_management_test

import rego.v1

import data.shield_ai.grm.third_party_ai_risk_management.allow

test_no_vendor_action_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "vendor_used": false
  }
}
    allow with input as req
}

test_unassessed_vendor_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "vendor_used": true
  },
  "vendors": {
    "name": "acme-ai",
    "assessed": false,
    "contractual_controls": true,
    "right_to_audit": true
  }
}
    not allow with input as req
}

test_vendor_without_contractual_controls_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "vendor_used": true
  },
  "vendors": {
    "name": "acme-ai",
    "assessed": true,
    "contractual_controls": false,
    "right_to_audit": true
  }
}
    not allow with input as req
}

test_eval_vendor_without_audit_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "vendor_used": true,
    "vendor_type": "evaluation"
  },
  "vendors": {
    "name": "irregular-ctf",
    "assessed": true,
    "contractual_controls": true,
    "right_to_audit": false
  }
}
    not allow with input as req
}

test_fully_assessed_vendor_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "vendor_used": true,
    "vendor_type": "evaluation"
  },
  "vendors": {
    "name": "irregular-ctf",
    "assessed": true,
    "contractual_controls": true,
    "right_to_audit": true
  }
}
    allow with input as req
}
