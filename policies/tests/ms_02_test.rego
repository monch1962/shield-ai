package shield_ai.ms.training_data_integrity_test

import rego.v1

import data.shield_ai.ms.training_data_integrity.allow

test_verified_training_run_allowed if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "provenance_tracked": true,
    "sanitised": true,
    "poison_scan": "clean"
  }
}
    allow with input as req
}

test_untracked_provenance_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "provenance_tracked": false,
    "sanitised": true,
    "poison_scan": "clean"
  }
}
    not allow with input as req
}

test_unsanitised_dataset_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "provenance_tracked": true,
    "sanitised": false,
    "poison_scan": "clean"
  }
}
    not allow with input as req
}

test_poison_flagged_denied if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "provenance_tracked": true,
    "sanitised": true,
    "poison_scan": "flagged"
  }
}
    not allow with input as req
}

test_missing_poison_scan_fails_closed if {
    req := {
  "action": {
    "kind": "training_run"
  },
  "training": {
    "provenance_tracked": true,
    "sanitised": true
  }
}
    not allow with input as req
}
