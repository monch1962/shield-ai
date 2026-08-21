package shield_ai.iam.human_oversight_controls

import rego.v1

# SHIELD-AI(TM) IAM-03: Human Oversight Controls
# Pillar: IAM -- Identity and Access
#
# Implement risk-tiered human approval gates for agent actions, with documented break-glass procedures for urgent situations.
#
# Maturity indicators:
#   L1: No human oversight. Agent acts autonomously on all actions.
#   L2: High-risk actions flagged for human review. Manual approval process.
#   L3: Risk-based approval tiers. Automated approval gates. Time-limited approvals. Break-glass procedures documented.
#   L4: Context-aware approval requirements. Multi-party approval for critical actions. Oversight mechanism independently audited.
#
# Regulatory mappings:
#   EU AI Act: Art. 14 -- Human Oversight
#   NIST AI RMF: MANAGE (MG.DE)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (OpenClaw approval
# disable INC-21, AISI sockpuppet INC-27, CoreBreak forged approval INC-34).
# Input model: input.action.high_risk_class ("financial" | "data_write" |
# "impersonation" | "publication" | other); input.approval = {"present": bool,
# "channel": "human_console" | "agent" | "session_history" | ...}.
# Approval evidence from session/event history is never valid (forged-approval
# class); agent-invoked approvals never cover financial actions.

deny contains msg if {
    input.action.high_risk_class
    not input.approval.present
    msg := sprintf("IAM-03 deny: %s action by agent %q without human approval", [input.action.high_risk_class, input.agent.id])
}

deny contains msg if {
    input.approval.present == true
    input.approval.channel == "session_history"
    msg := "IAM-03 deny: approval evidence from session history is not human approval (forged-approval class)"
}

deny contains msg if {
    input.action.high_risk_class == "financial"
    input.approval.present == true
    input.approval.channel == "agent"
    msg := "IAM-03 deny: financial action approved on the agent channel; human-console approval required"
}

allow if {
    count(deny) == 0
}
