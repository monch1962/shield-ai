package shield_ai.iam.credential_scope_narrowing

# SHIELD-AI(TM) IAM-08: Credential Scope Narrowing
# Pillar: IAM -- Identity and Access
#
# Ensure credentials in agent environments are minimal, short-lived, and revocable.
#
# Maturity indicators:
#   L1: Broad shared credentials in agent environments.
#   L2: Per-agent credentials; scope aligned to tool inventory.
#   L3: Per-tool scoped short-lived tokens; no environment-wide credentials; automated rotation.
#   L4: Continuous scope verification; cascade revocation on compromise; per-tool scope attestation.
#
# Regulatory mappings:
#   ISM: Guidelines for System Management
#   NIST AI RMF: PROTECT (PR.AC)
#   EU AI Act: Art. 15(b)
#   Essential Eight: Restrict Administrative Privileges

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_08
#     msg := sprintf("IAM-08 violation: agent %v does not meet control requirements", [agent.id])
# }
