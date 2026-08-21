package shield_ai.ms.model_inventory_and_lineage_tr_test

import rego.v1

import data.shield_ai.ms.model_inventory_and_lineage_tr.allow

test_registered_model_deploy_allowed if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "inventory": {
      "registered": true,
      "lineage_tracked": true,
      "versioned": true
    }
  }
}
    allow with input as req
}

test_unregistered_model_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "inventory": {
      "registered": false,
      "lineage_tracked": true,
      "versioned": true
    }
  }
}
    not allow with input as req
}

test_no_lineage_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "inventory": {
      "registered": true,
      "lineage_tracked": false,
      "versioned": true
    }
  }
}
    not allow with input as req
}

test_unversioned_model_denied if {
    req := {
  "action": {
    "kind": "model_deploy"
  },
  "model": {
    "id": "m1",
    "inventory": {
      "registered": true,
      "lineage_tracked": true,
      "versioned": false
    }
  }
}
    not allow with input as req
}
