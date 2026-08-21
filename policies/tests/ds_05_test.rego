package shield_ai.ds.training_data_governance_test

import rego.v1

import data.shield_ai.ds.training_data_governance.allow

test_governed_training_allowed if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "governance": {
      "lineage": true,
      "retention_limited": true
    },
    "personal_data": false
  }
}
    allow with input as req
}

test_no_lineage_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "governance": {
      "lineage": false,
      "retention_limited": true
    },
    "personal_data": false
  }
}
    not allow with input as req
}

test_personal_data_without_consent_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "governance": {
      "lineage": true,
      "retention_limited": true
    },
    "personal_data": true
  }
}
    not allow with input as req
}

test_no_retention_limit_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "governance": {
      "lineage": true,
      "retention_limited": false
    },
    "personal_data": false
  }
}
    not allow with input as req
}
