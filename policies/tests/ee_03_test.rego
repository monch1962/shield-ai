package shield_ai.ee.resource_usage_limiting_test

import rego.v1

import data.shield_ai.ee.resource_usage_limiting.allow

test_within_limits_allowed if {
    req := {"agent": {"id": "agent-1", "resource_usage": {"cpu_pct": 30, "network_mbps": 2, "api_rate": 40}}}
    allow with input as req
}

test_cpu_exceeded_denied if {
    req := {"agent": {"id": "agent-1", "resource_usage": {"cpu_pct": 95, "network_mbps": 2, "api_rate": 40}}}
    not allow with input as req
}

test_network_exceeded_denied if {
    req := {"agent": {"id": "agent-1", "resource_usage": {"cpu_pct": 30, "network_mbps": 50, "api_rate": 40}}}
    not allow with input as req
}

test_api_rate_exceeded_denied if {
    req := {"agent": {"id": "agent-1", "resource_usage": {"cpu_pct": 30, "network_mbps": 2, "api_rate": 500}}}
    not allow with input as req
}
