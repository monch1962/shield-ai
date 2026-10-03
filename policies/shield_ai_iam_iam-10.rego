package shield_ai.iam.taint_tracked_least_privilege_

# SHIELD-AI(TM) IAM-10: Taint-Tracked Least-Privilege Subagent Scoping
# Pillar: IAM -- Identity and Access
#
# Taint-track externally-submitted records and bind subagent permission scoping to that taint plus field-level least privilege.
#
# Maturity indicators:
#   L1: Subagents process externally-submitted records with the same broad grants as internally-trusted data; no taint marking.
#   L2: Externally-submitted records flagged as untrusted; manual review of subagent scope when processing them.
#   L3: Taint-marked at ingestion; record-handling subagents scoped to only required tables/fields/tools; tainted reads prevented from cascading into untainted sensitive collections.
#   L4: Automated taint propagation through the workflow graph; least-privilege subagent scope enforced by policy-as-code; any tainted-to-sensitive read blocked with alerting.
#
# Regulatory mappings:
#   NIST AI RMF: PROTECT (PR.AC)
#   OWASP: LLM08 (Excessive Agency)
#   EU AI Act: Art. 14(b)
#   ISM: Guidelines for System Management

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_10
#     msg := sprintf("IAM-10 violation: agent %v does not meet control requirements", [agent.id])
# }
