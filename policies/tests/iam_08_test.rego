package shield_ai.iam.credential_scope_narrowing_test

import rego.v1

import data.shield_ai.iam.credential_scope_narrowing.allow

test_per_tool_scoped_credentials_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "per_tool_scope": true,
      "broad_role": false,
      "short_lived": true
    }
  }
}
    allow with input as req
}

test_broad_role_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "per_tool_scope": true,
      "broad_role": true,
      "short_lived": true
    }
  }
}
    not allow with input as req
}

test_unscoped_credentials_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "per_tool_scope": false,
      "broad_role": false,
      "short_lived": true
    }
  }
}
    not allow with input as req
}

test_standing_credentials_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "per_tool_scope": true,
      "broad_role": false,
      "short_lived": false
    }
  }
}
    not allow with input as req
}
