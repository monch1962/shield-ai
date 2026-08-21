package shield_ai.tp.tool_output_validation_test

import rego.v1

import data.shield_ai.tp.tool_output_validation.allow

test_validated_output_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": true,
      "sanitised": true,
      "within_size_limit": true,
      "code_generation": false
    }
  }
}
    allow with input as req
}

test_unvalidated_output_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": false,
      "sanitised": true,
      "within_size_limit": true
    }
  }
}
    not allow with input as req
}

test_unsanitised_output_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": true,
      "sanitised": false,
      "within_size_limit": true
    }
  }
}
    not allow with input as req
}

test_oversized_output_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": true,
      "sanitised": true,
      "within_size_limit": false
    }
  }
}
    not allow with input as req
}

test_code_output_unsandboxed_denied if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": true,
      "sanitised": true,
      "within_size_limit": true,
      "code_generation": true,
      "code_sandboxed": false
    }
  }
}
    not allow with input as req
}

test_code_output_sandboxed_allowed if {
    req := {
  "action": {
    "kind": "tool_call",
    "tool": "search_documents",
    "tool_output": {
      "validated": true,
      "sanitised": true,
      "within_size_limit": true,
      "code_generation": true,
      "code_sandboxed": true
    }
  }
}
    allow with input as req
}
