package shield_ai.iam.just_in_time_jit_access

# SHIELD-AI™ IAM-05: Just-in-Time (JIT) Access
# Pillar: IAM — Identity and Access
#
# Issue session-bound, ephemeral credentials for agents with automatic expiration and the ability to revoke mid-session on suspicious behaviour detection.
#
# Maturity indicators:
#   L1: Persistent credentials. No expiration. Credentials valid indefinitely.
#   L2: Session-bound credentials with fixed expiration (e.g., 1 hour). Manual renewal.
#   L3: JIT credentials scoped per-session. Automatic expiration. Revocation available.
#   L4: Dynamic scoping — credentials scoped to specific tools/data per agent task. Continuous authorisation checking.
#
# Regulatory mappings:
#   NIST AI RMF: PROTECT (PR.AC)
#   Essential Eight: Restrict Administrative Privileges
#   ISM: Guidelines for System Management — privileged access management

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_05
#     msg := sprintf("IAM-05 violation: agent %v does not meet control requirements", [agent.id])
# }
