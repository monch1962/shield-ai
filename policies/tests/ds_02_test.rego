package shield_ai.ds.inference_data_protection_test

import rego.v1

import data.shield_ai.ds.inference_data_protection.allow

test_encrypted_inference_allowed if {
    req := {
  "data": {
    "inference": {
      "encrypted_e2e": true,
      "tls13_min": true,
      "sensitive": false
    }
  }
}
    allow with input as req
}

test_unencrypted_inference_denied if {
    req := {
  "data": {
    "inference": {
      "encrypted_e2e": false,
      "tls13_min": true,
      "sensitive": false
    }
  }
}
    not allow with input as req
}

test_old_tls_denied if {
    req := {
  "data": {
    "inference": {
      "encrypted_e2e": true,
      "tls13_min": false,
      "sensitive": false
    }
  }
}
    not allow with input as req
}

test_sensitive_outside_trust_boundary_denied if {
    req := {
  "data": {
    "inference": {
      "encrypted_e2e": true,
      "tls13_min": true,
      "sensitive": true,
      "endpoint_in_trust_boundary": false
    }
  }
}
    not allow with input as req
}

test_sensitive_in_trust_boundary_allowed if {
    req := {
  "data": {
    "inference": {
      "encrypted_e2e": true,
      "tls13_min": true,
      "sensitive": true,
      "endpoint_in_trust_boundary": true
    }
  }
}
    allow with input as req
}
