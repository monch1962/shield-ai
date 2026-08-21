package shield_ai.ee.resource_usage_limiting

import rego.v1

# SHIELD-AI(TM) EE-03: Resource Usage Limiting
# Pillar: EE -- Execution Environment
#
# Bound agent resource consumption with runtime enforcement.
#
# Maturity indicators:
#   L1: No resource limits; agents share unbounded resources.
#   L2: Basic limits configured; policy-only enforcement.
#   L3: Runtime-enforced limits (CPU, memory, storage, network, API rate); exceeding limits alerts and may terminate.
#   L4: Continuous anomaly detection on resource usage; automated termination for abuse patterns.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Alibaba
# crypto-mining resource abuse, INC-10).
# Input model: input.agent.resource_usage = {"cpu_pct": n, "network_mbps": n,
# "api_rate": n}. Limits below are deployment-defined defaults; the exceeding
# action is denied and the exceedance also trips MIR-02.

resource_limits := {
    "cpu_pct_max": 80,
    "network_mbps_max": 10,
    "api_rate_max": 100,
}

deny contains msg if {
    input.agent.resource_usage.cpu_pct > resource_limits.cpu_pct_max
    msg := sprintf("EE-03 deny: agent %q CPU usage %v%% exceeds limit %v%%", [input.agent.id, input.agent.resource_usage.cpu_pct, resource_limits.cpu_pct_max])
}

deny contains msg if {
    input.agent.resource_usage.network_mbps > resource_limits.network_mbps_max
    msg := sprintf("EE-03 deny: agent %q network usage %v Mbps exceeds limit %v Mbps", [input.agent.id, input.agent.resource_usage.network_mbps, resource_limits.network_mbps_max])
}

deny contains msg if {
    input.agent.resource_usage.api_rate > resource_limits.api_rate_max
    msg := sprintf("EE-03 deny: agent %q API rate %v exceeds limit %v", [input.agent.id, input.agent.resource_usage.api_rate, resource_limits.api_rate_max])
}

allow if {
    count(deny) == 0
}
