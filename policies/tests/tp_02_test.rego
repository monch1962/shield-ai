package shield_ai.tp.tool_access_control_test

import rego.v1

import data.shield_ai.tp.tool_access_control.allow

test_authenticated_agent_tool_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_auth": {
      "agent_authenticated": true,
      "human_session": false
    },
    "tool_allowed": true
  }
}
    allow with input as req
}

test_unauthenticated_call_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_auth": {
      "agent_authenticated": false,
      "human_session": false
    },
    "tool_allowed": true
  }
}
    not allow with input as req
}

test_human_session_auth_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_auth": {
      "agent_authenticated": true,
      "human_session": true
    },
    "tool_allowed": true
  }
}
    not allow with input as req
}

test_not_on_allowlist_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "drop_database",
    "tool_auth": {
      "agent_authenticated": true,
      "human_session": false
    },
    "tool_allowed": false
  }
}
    not allow with input as req
}
