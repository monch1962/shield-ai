package shield_ai.ms.supply_chain_security_test

import rego.v1

import data.shield_ai.ms.supply_chain_security.allow

test_fully_verified_deploy_allowed if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "supply_chain": {
      "sbom": true,
      "signature_verified": true,
      "checkpoint_signed": true
    }
  }
}
    allow with input as req
}

test_missing_sbom_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "supply_chain": {
      "sbom": false,
      "signature_verified": true,
      "checkpoint_signed": true
    }
  }
}
    not allow with input as req
}

test_unverified_signature_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "supply_chain": {
      "sbom": true,
      "signature_verified": false,
      "checkpoint_signed": true
    }
  }
}
    not allow with input as req
}

test_unsigned_checkpoint_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "supply_chain": {
      "sbom": true,
      "signature_verified": true,
      "checkpoint_signed": false
    }
  }
}
    not allow with input as req
}

test_non_deploy_action_not_gated if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents"
  }
}
    allow with input as req
}
