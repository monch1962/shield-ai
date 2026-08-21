package shield_ai.ee.execution_environment_boundary

import rego.v1

# SHIELD-AI(TM) EE-01: Execution Environment Boundary Enforcement
# Pillar: EE -- Execution Environment
#
# Enforce a hard execution boundary around every agent.
#
# Maturity indicators:
#   L1: Agents run on shared infrastructure with no boundary enforcement.
#   L2: Container per agent; basic isolation; shared mounts documented.
#   L3: No shared host mounts or namespaces; immutable infrastructure; fail-closed on breach.
#   L4: Runtime boundary verification (attestation); automated response on any isolation breach.
#
# Regulatory mappings:
#   ISM: Guidelines for System Hardening
#   Essential Eight: Application Control
#   ASD: Container Security Guidance
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.tool, input.agent.sandboxed (bool).
# Fail closed: a missing sandboxed flag is treated as not sandboxed.

# High-risk tools that must only ever run from inside the execution boundary.
high_risk_tools := {
    "shell_exec",
    "write_file",
    "install_package",
    "transfer_funds",
    "delete_objects",
}

deny contains msg if {
    input.action.tool in high_risk_tools
    not input.agent.sandboxed
    msg := sprintf("EE-01 deny: tool %q is high-risk and agent %q is not sandboxed (fail closed)", [input.action.tool, input.agent.id])
}

allow if {
    count(deny) == 0
}
