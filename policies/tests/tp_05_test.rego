package shield_ai.tp.pipeline_integrity_test

import rego.v1

import data.shield_ai.tp.pipeline_integrity.allow

test_signed_deployment_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "pipeline": {
    "run_signed": true,
    "attested": true,
    "security_gate_passed": true,
    "artifact_registry_immutable": true
  }
}
    allow with input as req
}

test_unsigned_run_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "pipeline": {
    "run_signed": false,
    "attested": true,
    "security_gate_passed": true,
    "artifact_registry_immutable": true
  }
}
    not allow with input as req
}

test_unattested_run_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "pipeline": {
    "run_signed": true,
    "attested": false,
    "security_gate_passed": true,
    "artifact_registry_immutable": true
  }
}
    not allow with input as req
}

test_failed_gate_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "pipeline": {
    "run_signed": true,
    "attested": true,
    "security_gate_passed": false,
    "artifact_registry_immutable": true
  }
}
    not allow with input as req
}

test_mutable_artifact_registry_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "pipeline": {
    "run_signed": true,
    "attested": true,
    "security_gate_passed": true,
    "artifact_registry_immutable": false
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
