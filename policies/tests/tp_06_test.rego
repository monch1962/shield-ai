package shield_ai.tp.dependency_scanning_test

import rego.v1

import data.shield_ai.tp.dependency_scanning.allow

test_clean_dependencies_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": true,
    "critical_finding": false
  }
}
    allow with input as req
}

test_unscanned_dependencies_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": false,
    "critical_finding": false
  }
}
    not allow with input as req
}

test_critical_finding_unblocked_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": true,
    "critical_finding": true,
    "critical_blocked": false
  }
}
    not allow with input as req
}

test_critical_finding_blocked_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": true,
    "critical_finding": true,
    "critical_blocked": true
  }
}
    allow with input as req
}

test_sandbox_library_without_alternative_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": true,
    "critical_finding": true,
    "critical_blocked": true,
    "sandbox_library": true,
    "alternative_approved": false
  }
}
    not allow with input as req
}

test_sandbox_library_with_alternative_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "dependencies": {
    "scanned": true,
    "critical_finding": true,
    "critical_blocked": true,
    "sandbox_library": true,
    "alternative_approved": true
  }
}
    allow with input as req
}
