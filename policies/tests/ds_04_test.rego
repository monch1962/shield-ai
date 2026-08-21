package shield_ai.ds.data_minimisation_test

import rego.v1

import data.shield_ai.ds.data_minimisation.allow

test_field_filtered_retrieval_allowed if {
    req := {
  "action": {
    "kind": "retrieval"
  },
  "data": {
    "access": {
      "bulk": false,
      "field_filtered": true,
      "abac_enforced": true
    }
  }
}
    allow with input as req
}

test_bulk_access_denied if {
    req := {
  "action": {
    "kind": "retrieval"
  },
  "data": {
    "access": {
      "bulk": true,
      "field_filtered": true,
      "abac_enforced": true
    }
  }
}
    not allow with input as req
}

test_document_level_only_denied if {
    req := {
  "action": {
    "kind": "retrieval"
  },
  "data": {
    "access": {
      "bulk": false,
      "field_filtered": false,
      "abac_enforced": true
    }
  }
}
    not allow with input as req
}

test_no_abac_denied if {
    req := {
  "action": {
    "kind": "retrieval"
  },
  "data": {
    "access": {
      "bulk": false,
      "field_filtered": true,
      "abac_enforced": false
    }
  }
}
    not allow with input as req
}
