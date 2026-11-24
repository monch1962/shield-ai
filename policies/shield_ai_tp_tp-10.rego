package shield_ai.tp.agent_platform_inbound_control

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) TP-10: Agent Platform Inbound Control-Plane Protection
# Pillar: TP -- Tool and Pipeline Security
#
# Defend the agent platform's inbound listening surface from direct, model-independent attack.
#
# Maturity indicators:
#   L1: Listeners ungoverned; gateway tokens reachable from web/browser context.
#   L2: Listener inventory maintained; origin validation on gateway sessions; token scope review.
#   L3: Default-deny binding policy enforced; no standing allow rules; automated detection of new listeners; no operator-scope tokens readable from web context.
#   L4: Continuous adversarial testing of the inbound surface; binding-policy attestation in the audit trail; periodic re-certification of all allow rules.
#
# Regulatory mappings:
#   ISM: Web Application Hardening, Network Segmentation
#   OWASP: LLM09 (Misuse of System Access)
#   NIST AI RMF: PROTECT (PR.AC)
#   EU AI Act: Art. 14
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (OpenClaw
# CVE-2026-25253, Wiz exposed MCP, Ruflo/RufRoot CVE-2026-59726).
# Input model: input.action.kind == "binding"; input.action.target = listener;
# input.action.allowed_binding (pre-approved allow rule);
# input.action.origin (e.g. "web"); input.action.origin_validated (bool).
# Default deny: any binding without an explicit allow is denied; web-origin
# bindings additionally require origin validation (CSWSH class).

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["TP-10"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "binding"
}


deny contains msg if {
    applicable
    not input.action.allowed_binding
    msg := sprintf("TP-10 deny: listener binding %q is not on the approved binding list (default deny)", [input.action.target])
}

deny contains msg if {
    applicable
    input.action.origin == "web"
    not input.action.origin_validated
    msg := sprintf("TP-10 deny: web-origin binding %q without origin validation (CSWSH class)", [input.action.target])
}

allow if {
    count(deny) == 0
}
