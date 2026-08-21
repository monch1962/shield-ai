package shield_ai.mir.prompt_audit_log

import rego.v1

# SHIELD-AI(TM) MIR-03: Prompt Audit Log
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Log prompt/response pairs with automated sensitive data redaction, tiered retention, and SIEM integration for forensic analysis.
#
# Maturity indicators:
#   L1: No prompt logging.
#   L2: Basic prompt/response logging. Manual review. Short retention.
#   L3: Automated redaction. Tiered retention (full -> redacted). SIEM integration.
#   L4: Real-time prompt scanning for security events. Automated incident triggering from prompt analysis.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.sensitive (bool) -- the action involves sensitive
# prompt content; input.action.prompt_captured (bool);
# input.action.prompt_redacted (bool). Sensitive prompt/response pairs must
# be captured and redacted before SIEM ingestion.

deny contains msg if {
    input.action.sensitive == true
    not input.action.prompt_captured
    msg := "MIR-03 deny: sensitive prompt/response pair not captured for the audit log"
}

deny contains msg if {
    input.action.sensitive == true
    input.action.prompt_captured == true
    not input.action.prompt_redacted
    msg := "MIR-03 deny: captured prompt/response pair not redacted before SIEM ingestion"
}

allow if {
    count(deny) == 0
}
