package shield_ai.ds.data_classification_and_labell_test

import rego.v1

import data.shield_ai.ds.data_classification_and_labell.allow

test_classified_ingestion_allowed if {
    req := {
  "action": {
    "kind": "ingestion"
  },
  "data": {
    "classified": true,
    "label": "official"
  }
}
    allow with input as req
}

test_unclassified_ingestion_denied if {
    req := {
  "action": {
    "kind": "ingestion"
  },
  "data": {
    "classified": false,
    "label": "official"
  }
}
    not allow with input as req
}

test_missing_label_denied if {
    req := {
  "action": {
    "kind": "ingestion"
  },
  "data": {
    "classified": true
  }
}
    not allow with input as req
}

test_non_ingestion_action_not_gated if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents"
  }
}
    allow with input as req
}
