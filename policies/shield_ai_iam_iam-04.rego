package shield_ai.iam.credential_isolation

# SHIELD-AI IAM-04: Credential Isolation
# Pillar: IAM — Identity and Access
#
# Store, manage, and rotate agent credentials separately from human credentials with hardware-backed protection for critical agents and automated rotation on compromise signals.
#
# Maturity indicators:
#   L1: Agent and human credentials stored together. No rotation. No isolation.
#   L2: Agent credentials in separate secret store. Manual rotation on schedule.
#   L3: Automated credential rotation. Automatic rotation on compromise. Hardware-backed for critical agents.
#   L4: Just-in-time credential issuance. Continuous credential verification. Credential-less authentication (SPIFFE).
#
# Regulatory mappings:
#   ISM: Guidelines for System Management — credential management
#   NIST AI RMF: PROTECT (PR.AC)
#   Essential Eight: Multi-factor Authentication — extended to service accounts

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_04
#     msg := sprintf("IAM-04 violation: agent %v does not meet control requirements", [agent.id])
# }
