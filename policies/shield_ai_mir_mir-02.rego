package shield_ai.mir.behavioural_anomaly_detection

import rego.v1

# SHIELD-AI(TM) MIR-02: Behavioural Anomaly Detection
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Establish per-agent and per-agent-class behaviour baselines for tool usage, data access, memory access, and decision patterns, with automated alerting on deviation.
#
# Maturity indicators:
#   L1: No anomaly detection. Signature-based monitoring only (if any).
#   L2: Basic per-agent baselines. Manual alert review.
#   L3: Per-agent and per-class baselines. Automated alerting. Integration with SOC. Regular tuning.
#   L4: Continuous baseline learning. Cross-agent anomaly correlation. Predictive anomaly detection.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Hugging Face
# swarm campaign INC-01; adversary-owned autonomous agents INC-23/35).
# Input model: input.action.anomaly_flag (bool) -- the platform's baseline
# deviation detector fired; input.agent.ephemeral (bool) -- short-lived
# sandbox; input.action.campaign_correlated (bool).
# Fail closed: a flagged deviation blocks the action; ephemeral-sandbox
# high-value actions must be campaign-correlated (swarm-campaign class).

sensitive_tools := {
    "transfer_funds",
    "write_file",
    "shell_exec",
    "send_email_draft",
    "delete_objects",
}

deny contains msg if {
    input.action.anomaly_flag == true
    msg := sprintf("MIR-02 deny: action by agent %q deviates from its behaviour baseline", [input.agent.id])
}

deny contains msg if {
    input.agent.ephemeral == true
    input.action.tool in sensitive_tools
    not input.action.campaign_correlated
    msg := sprintf("MIR-02 deny: sensitive tool %q from ephemeral sandbox agent %q without campaign correlation (swarm class)", [input.action.tool, input.agent.id])
}

allow if {
    count(deny) == 0
}
