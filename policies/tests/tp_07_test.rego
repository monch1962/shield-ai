package shield_ai.tp.cross_tool_dependency_analysis_test

import rego.v1

import data.shield_ai.tp.cross_tool_dependency_analysis.allow

test_analysed_toolset_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "tools": {
    "chain_analysed": true,
    "escape_chain": false
  }
}
    allow with input as req
}

test_unanalysed_toolset_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "tools": {
    "chain_analysed": false,
    "escape_chain": false
  }
}
    not allow with input as req
}

test_escape_chain_without_acceptance_denied if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "tools": {
    "chain_analysed": true,
    "escape_chain": true,
    "risk_accepted": false
  }
}
    not allow with input as req
}

test_escape_chain_accepted_allowed if {
    req := {
  "action": {
    "kind": "deployment"
  },
  "tools": {
    "chain_analysed": true,
    "escape_chain": true,
    "risk_accepted": true
  }
}
    allow with input as req
}
