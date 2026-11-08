package shield_ai.ds.destination_and_emergent_channel_egress_inventory

import rego.v1

# SHIELD-AI(TM) DS-08: Destination and Emergent-Channel Egress Inventory
# Pillar: DS -- Data Security
#
# Enumerate and control every outbound destination and channel that can carry agent data out of the boundary, using payload-blind allow-lists rather than classifiers.
#
# Maturity indicators:
#   L1: No inventory; agents reach arbitrary destinations; egress relies on automatic HTTP controls only.
#   L2: Destination allow-list for URLs; DNS egress and rendered rich-media sources uncontrolled.
#   L3: Full channel inventory (URLs, DNS, image/render sources, messaging/unfurl, browser) each mapped to an explicit control; allow-list verification is payload-blind.
#   L4: Continuous egress-channel discovery and attestation; automatic blocking of any un-inventoried sink; active red-team testing of rendered-content and DNS exfiltration paths.
#
# Regulatory mappings:
#   NIST: SSDF
#   ISM: Guidelines for Network Management
#   OWASP: LLM01 (Prompt Injection)
#   EU AI Act: Art. 15(b)

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-72 SalesBleed
# DNS/image-tag exfiltration and Trusted-URLs parse-quirk bypass; Framing Gap
# arXiv 2608.27092 ROT13 classifier defeat). Input model:
# input.action.kind == "egress"; every outbound sink an agent can reach (URL/DNS/
# rendered rich media/messaging-unfurl/browser) must be mapped to an explicit
# control, verified by a payload-blind hard allow-list, not a content classifier.

deny contains msg if {
    input.action.egress.destination_allowlisted == false
    msg := sprintf("DS-08 deny: agent %q egress to destination not on the payload-blind allow-list", [input.agent.id])
}

deny contains msg if {
    input.action.egress.channel_inventoried == false
    msg := sprintf("DS-08 deny: agent %q egress through an un-inventoried sink (channel not enumerated/mapped to a control)", [input.agent.id])
}

deny contains msg if {
    input.action.egress.classifier_based == true
    msg := sprintf("DS-08 deny: agent %q egress rely on a content classifier rather than a payload-blind hard allow-list", [input.agent.id])
}

deny contains msg if {
    input.action.egress.channel == "messaging"
    input.action.egress.invoker_attributed == false
    msg := sprintf("DS-08 deny: agent %q messaging egress lacks invoker attribution and user confirmation", [input.agent.id])
}

deny contains msg if {
    input.action.egress.channel == "dns"
    input.action.egress.dns_resolver_allowlisted == false
    msg := sprintf("DS-08 deny: agent %q DNS egress is not restricted to allow-listed resolvers with inspected names", [input.agent.id])
}

deny contains msg if {
    input.action.egress.channel == "rendered_media"
    input.action.egress.render_source_allowlisted == false
    msg := sprintf("DS-08 deny: agent %q rendered rich-media source is not on the destination allow-list", [input.agent.id])
}

allow if {
    count(deny) == 0
}