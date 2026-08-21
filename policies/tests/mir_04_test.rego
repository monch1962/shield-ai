package shield_ai.mir.incident_response_playbooks_test

import rego.v1

import data.shield_ai.mir.incident_response_playbooks.allow

test_no_incident_allowed if {
    req := {
  "incident": {
    "acknowledged": false
  }
}
    allow with input as req
}

test_acknowledged_without_playbook_denied if {
    req := {
  "incident": {
    "acknowledged": true,
    "class": "prompt_injection",
    "playbook": "",
    "containment": true
  }
}
    not allow with input as req
}

test_acknowledged_without_containment_denied if {
    req := {
  "incident": {
    "acknowledged": true,
    "class": "tool_abuse",
    "playbook": "ir-tool-abuse",
    "containment": false
  }
}
    not allow with input as req
}

test_fully_handled_incident_allowed if {
    req := {
  "incident": {
    "acknowledged": true,
    "class": "model_compromise",
    "playbook": "ir-model-compromise",
    "containment": true
  }
}
    allow with input as req
}
