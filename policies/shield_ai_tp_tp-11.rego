package shield_ai.tp.agent_browser_and_content_rend

import rego.v1

# SHIELD-AI(TM) TP-11: Agent Browser and Content-Rendering Isolation
# Pillar: TP -- Tool and Pipeline Security
#
# Prevent untrusted rendered content from commanding the agent.
#
# Maturity indicators:
#   L1: Agent uses browser/document rendering as-is; no content classification.
#   L2: Hidden-content scanning on rendered pages and uploaded documents; cross-origin actions flagged for review.
#   L3: Origin isolation preserved in agent browser runtimes; no cross-origin token access; imperative action gating (approval required for financial and credential operations); document uploads sanitised before assistant processing.
#   L4: Continuous adversarial testing of the rendering layer; origin-isolation attestation; red-team validation against zero-click chains (PleaseFix/Intent Collision class).
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection)
#   NIST AI RMF: PROTECT (PR.AC)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Zenity Intent
# Collision INC-30, ChatMate RPE INC-29, AISI INC-27).
# Input model: input.action.cross_origin (bool), input.action.privileged (bool),
# input.action.kind == "document_render", input.action.document_sanitized (bool),
# input.approval.present (bool). Fail closed on missing flags.

deny contains msg if {
    input.action.cross_origin == true
    input.action.privileged == true
    not input.approval.present
    msg := sprintf("TP-11 deny: cross-origin privileged action %q from rendered content without approval", [input.action.tool])
}

deny contains msg if {
    input.action.kind == "document_render"
    not input.action.document_sanitized
    msg := "TP-11 deny: document upload rendered without sanitisation before assistant processing"
}

deny contains msg if {
    input.action.token_access == true
    not input.approval.present
    msg := "TP-11 deny: token access from rendered content without approval (credential-layer isolation)"
}

allow if {
    count(deny) == 0
}
