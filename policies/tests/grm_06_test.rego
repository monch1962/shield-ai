package shield_ai.grm.board_and_executive_reporting_test

import rego.v1

import data.shield_ai.grm.board_and_executive_reporting.allow

test_dashboard_active_allowed if {
    req := {
  "governance": {
    "reporting": {
      "dashboard": true,
      "risk_acceptance_logged": true
    },
    "risk_acceptance": false
  }
}
    allow with input as req
}

test_no_dashboard_denied if {
    req := {
  "governance": {
    "reporting": {
      "dashboard": false,
      "risk_acceptance_logged": true
    },
    "risk_acceptance": false
  }
}
    not allow with input as req
}

test_risk_acceptance_not_logged_denied if {
    req := {
  "governance": {
    "reporting": {
      "dashboard": true,
      "risk_acceptance_logged": false
    },
    "risk_acceptance": true
  }
}
    not allow with input as req
}

test_risk_acceptance_logged_allowed if {
    req := {
  "governance": {
    "reporting": {
      "dashboard": true,
      "risk_acceptance_logged": true
    },
    "risk_acceptance": true
  }
}
    allow with input as req
}
