package shield_ai.ds.memory_sanitisation_test

import rego.v1

import data.shield_ai.ds.memory_sanitisation.allow

test_non_persistent_memory_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "memory": {
      "persists_classified": false
    }
  },
  "action": {
    "kind": "tool_call"
  }
}
    allow with input as req
}

test_persisting_classified_denied if {
    req := {
  "agent": {
    "id": "a1",
    "memory": {
      "persists_classified": true
    }
  },
  "action": {
    "kind": "tool_call"
  }
}
    not allow with input as req
}

test_session_end_without_wipe_denied if {
    req := {
  "agent": {
    "id": "a1",
    "memory": {
      "persists_classified": false
    }
  },
  "action": {
    "kind": "session_end"
  }
}
    not allow with input as req
}

test_session_end_with_wipe_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "memory": {
      "persists_classified": false,
      "wiped_between_sessions": true
    }
  },
  "action": {
    "kind": "session_end"
  }
}
    allow with input as req
}
