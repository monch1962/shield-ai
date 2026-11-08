package shield_ai.ms.cross_tenant_agent_memory_and_state

import rego.v1

# SHIELD-AI(TM) MS-15: Cross-Tenant Agent Memory and State Isolation
# Pillar: MS -- Model Security
#
# Isolate multi-tenant agent memory and state per tenant as a hard boundary; keep the isolation key out of model control and gate retrieval/write by verified ownership.
#
# Maturity indicators:
#   L1: Shared/pooled vector store with soft metadata ownership and LLM-controllable namespace keys; cross-tenant reach demonstrable.
#   L2: Per-tenant partitioning or post-retrieval ownership gate applied; namespace keys removed from the tool schema; cross-user reach monitored.
#   L3: Hard post-retrieval and post-write ownership gating with default-deny; connection parameters bound at construction; cross-tenant hits alarmed as control violations.
#   L4: Memory isolation fail-closed and continuously exercised; cross-tenant write attempts denied and alarmed; pooled-store deployments require hard partitioning or ownership gating.
#
# Regulatory mappings:
#   OWASP: LLM12 (Memory Poisoning, cross-tenant variant)
#   NIST AI RMF: GOVERN + PROTECT (PR.AC)
#   EU AI Act: Art. 10 (Data Governance)
#   ISM: Guidelines for Cryptography and Data Protection
#   Essential Eight: Restrict Administrative Privileges

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (MemLeak
# arXiv 2610.04195 cross-tenant semantic leakage 70-100% incidental /
# 90-100% adversarial placement, INC-81; Strands Agents Tools memory-namespace
# IDOR GHSA-mpxq-953j-42m4, INC-81; Ryvane CVE-2026-2018/2104 cross-tenant
# write, INC-81; Beta9/Beam pooled-execution escapes, INC-82).
#
# Input model:
#   input.action.kind          == "memory_read" | "memory_write"
#   input.action.pooled_store  (bool) -- multiple tenants share one index/store
#   input.action.ownership_verified   (bool) -- hard post-retrieval/post-write ownership gate
#   input.action.cross_tenant_hit     (bool) -- a hit/write names/produces another tenant
#   input.action.namespace_model_controllable (bool) -- namespace/cluster/collection is an LLM tool argument
#   input.action.connection_params_bound    (bool) -- cluster URI/db/collection bound at construction
#   input.agent.memory.write_auth (string) -- verified writer identity for writes
#
# Semantics (deny-override): a single deny blocks the action. Cross-tenant
# retrieval/write, model-controllable isolation keys, unbound connection
# parameters, and unverifiable ownership all fail closed.

deny contains msg if {
    input.action.kind == "memory_read"
    input.action.pooled_store == true
    input.action.cross_tenant_hit == true
    msg := sprintf("MS-15 deny: pooled memory_read by agent %q returned a cross-tenant hit (owner != querying principal); hard ownership gate must drop it", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_read"
    input.action.pooled_store == true
    not input.action.ownership_verified
    msg := sprintf("MS-15 deny: pooled memory_read by agent %q could not verify ownership of a hit; fail closed per default-deny (semantic similarity is not an admissibility proxy)", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_write"
    input.action.cross_tenant_hit == true
    msg := sprintf("MS-15 deny: cross-tenant memory_write by agent %q (attempted write outside the writing principal's tenant); denied and alarmed", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_write"
    not input.agent.memory.write_auth
    msg := sprintf("MS-15 deny: memory_write by agent %q is not authenticated to a verified writer identity", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_read"
    input.action.namespace_model_controllable == true
    msg := sprintf("MS-15 deny: memory_read by agent %q uses an LLM-controllable namespace/tenant key; the isolation key must never be a model-controllable tool argument", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_write"
    input.action.namespace_model_controllable == true
    msg := sprintf("MS-15 deny: memory_write by agent %q uses an LLM-controllable namespace/tenant key; removed from the tool schema", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_read"
    input.action.connection_params_bound == false
    msg := sprintf("MS-15 deny: memory_read by agent %q passes connection parameters (cluster/collection) per call; must be bound at construction", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_write"
    input.action.connection_params_bound == false
    msg := sprintf("MS-15 deny: memory_write by agent %q passes connection parameters (cluster/collection) per call; must be bound at construction", [input.agent.id])
}

allow if {
    count(deny) == 0
}