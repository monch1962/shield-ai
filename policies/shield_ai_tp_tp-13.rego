package shield_ai.tp.agent_dependency_install_provenance

import rego.v1

import data.shield_ai.lib.bad_schema_version
import data.shield_ai.lib.field_undefined

# SHIELD-AI(TM) TP-13: Agent Dependency-Install Provenance Verification
# Pillar: TP -- Tool and Pipeline Security
#
# Verify registry-namespace and domain-ownership provenance before any agent-executed install derived from ingested content.
#
# Maturity indicators:
#   L1: Agents execute install commands found in documentation or llms.txt verbatim with no namespace checks.
#   L2: Install commands from ingested content run, but package/domain existence is only checked post-hoc.
#   L3: Pre-install provenance verification: registry existence, namespace ownership, domain registration; installs from untrusted content gated by an allowlist or human approval; dangling references blocked and logged via MIR-01.
#   L4: Continuous verification against live registry state; automated blocking of dangling references; documentation files never treated as authoritative install scripts; red-team testing of the docs-to-install path.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for Gateways

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-44 llms.txt
# dangling-install class; INC-85 AgentScope advisory-lag blind spot).
# Input model: input.action.kind == "dependency_install". Installation commands
# derived from ingested content must verify package registry existence / namespace
# ownership / domain registration before executing, gate untrusted-content installs
# by allowlist or human approval, and block dangling references.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["TP-13"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "dependency_install"
}


deny contains msg if {
    applicable
    input.action.dependency.registry_exists == false
    msg := sprintf("TP-13 deny: install by agent %q references a package not confirmed to exist in the intended registry", [input.agent.id])
}
deny contains msg if {
    applicable
    not field_undefined(input, ["action", "dependency"])
    field_undefined(input, ["action", "dependency", "registry_exists"])
    msg := "TP-13 deny: missing attestation for input.action.dependency.registry_exists (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.dependency.namespace_owned == false
    msg := sprintf("TP-13 deny: install by agent %q references a registry namespace not verified to belong to the documented vendor", [input.agent.id])
}
deny contains msg if {
    applicable
    not field_undefined(input, ["action", "dependency"])
    field_undefined(input, ["action", "dependency", "namespace_owned"])
    msg := "TP-13 deny: missing attestation for input.action.dependency.namespace_owned (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.dependency.domain_registered == false
    msg := sprintf("TP-13 deny: install by agent %q references an unclaimed or expired domain; dangling reference must block the install", [input.agent.id])
}
deny contains msg if {
    applicable
    not field_undefined(input, ["action", "dependency"])
    field_undefined(input, ["action", "dependency", "domain_registered"])
    msg := "TP-13 deny: missing attestation for input.action.dependency.domain_registered (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.dependency.from_ingested_content == true
    input.action.dependency.allowlisted_or_approved == false
    msg := sprintf("TP-13 deny: install by agent %q is derived from ingested content and is not gated by an allowlist or human approval", [input.agent.id])
}
deny contains msg if {
    applicable
    input.action.dependency.from_ingested_content == true
    not field_undefined(input, ["action", "dependency"])
    field_undefined(input, ["action", "dependency", "allowlisted_or_approved"])
    msg := "TP-13 deny: missing attestation for input.action.dependency.allowlisted_or_approved (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.dependency.doc_as_authoritative == true
    msg := sprintf("TP-13 deny: install by agent %q treats a documentation file as an authoritative install script; a doc file is never the install script", [input.agent.id])
}

deny contains msg if {
    applicable
    input.action.dependency.dangling_reference == true
    msg := sprintf("TP-13 deny: install by agent %q points at a dangling reference (unregistered package/unclaimed domain); blocked and logged via MIR-01", [input.agent.id])
}

allow if {
    count(deny) == 0
}