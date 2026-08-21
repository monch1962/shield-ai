package shield_ai.iam.transitive_delegation_chain_en_test

import rego.v1

import data.shield_ai.iam.transitive_delegation_chain_en.allow

test_two_hop_chain_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "delegation": {
      "hops": 2,
      "max_hops": 2,
      "chain_reconstructable": true
    }
  }
}
    allow with input as req
}

test_three_hop_chain_denied if {
    req := {
  "agent": {
    "id": "a1",
    "delegation": {
      "hops": 3,
      "max_hops": 2,
      "chain_reconstructable": true
    }
  }
}
    not allow with input as req
}

test_unreconstructable_chain_denied if {
    req := {
  "agent": {
    "id": "a1",
    "delegation": {
      "hops": 2,
      "max_hops": 2,
      "chain_reconstructable": false
    }
  }
}
    not allow with input as req
}
