package shield_ai.ms.deployment_context_obfuscation_test

import rego.v1

import data.shield_ai.ms.deployment_context_obfuscation.allow

test_indistinguishable_eval_allowed if {
    req := {
  "action": {
    "kind": "evaluation_run"
  },
  "evaluation": {
    "env_indistinguishable": true,
    "behaviour_matches_production": true
  }
}
    allow with input as req
}

test_distinguishable_env_denied if {
    req := {
  "action": {
    "kind": "evaluation_run"
  },
  "evaluation": {
    "env_indistinguishable": false,
    "behaviour_matches_production": true
  }
}
    not allow with input as req
}

test_behaviour_divergence_denied if {
    req := {
  "action": {
    "kind": "evaluation_run"
  },
  "evaluation": {
    "env_indistinguishable": true,
    "behaviour_matches_production": false
  }
}
    not allow with input as req
}
