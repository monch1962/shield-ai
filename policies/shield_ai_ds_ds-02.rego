package shield_ai.ds.inference_data_protection

import rego.v1

# SHIELD-AI(TM) DS-02: Inference Data Protection
# Pillar: DS -- Data Security
#
# Encrypt all data in transit between user, agent, model, and tools with TLS 1.3 minimum, and secure inference endpoints within the organisation's trust boundary for sensitive workloads.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.data.inference = {"encrypted_e2e": bool, "tls13_min": bool,
# "endpoint_in_trust_boundary": bool}. Fail closed on missing encryption claims.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.data.inference.encrypted_e2e
    msg := "DS-02 deny: inference data not encrypted end-to-end"
}

deny contains msg if {
    not input.data.inference.tls13_min
    msg := "DS-02 deny: inference transport below TLS 1.3 minimum"
}

deny contains msg if {
    input.data.inference.sensitive == true
    not input.data.inference.endpoint_in_trust_boundary
    msg := "DS-02 deny: sensitive inference endpoint outside the organisation's trust boundary"
}

allow if {
    count(deny) == 0
}
