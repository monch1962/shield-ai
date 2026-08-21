package shield_ai.ms.model_weight_protection_test

import rego.v1

import data.shield_ai.ms.model_weight_protection.allow

test_weights_encrypted_hsm_allowed if {
    req := {
  "model": {
    "id": "m1",
    "weights_encrypted": true,
    "key_management": "hsm"
  }
}
    allow with input as req
}

test_unencrypted_weights_denied if {
    req := {
  "model": {
    "id": "m1",
    "weights_encrypted": false,
    "key_management": "hsm"
  }
}
    not allow with input as req
}

test_no_key_management_denied if {
    req := {
  "model": {
    "id": "m1",
    "weights_encrypted": true,
    "key_management": "none"
  }
}
    not allow with input as req
}
