package shield_ai.ms.operational_data_stream_integr

import rego.v1

# SHIELD-AI(TM) MS-11: Operational Data-Stream Integrity
# Pillar: MS -- Model Security
#
# Prevent poisoned logs, alerts, and observability feeds from commanding the agent.
#
# Maturity indicators:
#   L1: Agents consume logs/alerts as-is; operational content treated as trusted.
#   L2: Log/alert content flagged as untrusted; agent actions from log triggers require review.
#   L3: Agent-visible operational content sanitised for instruction-bearing payloads before reasoning; independent non-log verification for log-triggered actions; ingestion pipelines authenticate producers; MIR-02 flags log-origin agent actions.
#   L4: Continuous red-team testing of the observability stream (GhostJacking class); provenance attestation on all agent-consumed feeds; fail-closed on stream integrity doubt.
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for System Monitoring
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (GhostJacking
# observability-stream poisoning, INC-33).
# Input model: input.action.trigger == "log_alert" when the action's proximate
# cause is log/alert content; input.context.stream = {"verified_producer": bool,
# "instruction_bearing": bool, "independent_verification": bool};
# input.action.high_impact (bool); input.approval.present (bool).
# Three gates: producer authenticated, no instruction-bearing payload acted on
# without independent non-log verification, high-impact log-triggered actions
# require human approval.

deny contains msg if {
    input.action.trigger == "log_alert"
    not input.context.stream.verified_producer
    msg := "MS-11 deny: agent action triggered by log/alert content from an unverified producer"
}

deny contains msg if {
    input.action.trigger == "log_alert"
    input.context.stream.instruction_bearing == true
    not input.context.stream.independent_verification
    msg := "MS-11 deny: instruction-bearing operational content acted on without independent non-log verification"
}

deny contains msg if {
    input.action.trigger == "log_alert"
    input.action.high_impact == true
    not input.approval.present
    msg := "MS-11 deny: high-impact agent action triggered by log/alert content without human approval"
}

allow if {
    count(deny) == 0
}
