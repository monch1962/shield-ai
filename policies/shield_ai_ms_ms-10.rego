package shield_ai.ms.agent_memory_store_integrity

import rego.v1

# SHIELD-AI(TM) MS-10: Agent Memory-Store Integrity
# Pillar: MS -- Model Security
#
# Ensure agent persistent memory cannot be silently poisoned to steer future behaviour.
#
# Maturity indicators:
#   L1: Memory persisted without integrity controls; no tamper awareness.
#   L2: Memory-store access authenticated; write logging; basic integrity checks.
#   L3: Tamper-evident memory (append-only or immutable snapshots); anomaly detection on memory writes via MIR-02; retrieval-layer filtering of flagged entries; documented post-incident memory audit-and-clean procedure.
#   L4: Continuous memory integrity attestation; automated quarantine of poisoned entries; red-team testing of memory-poisoning persistence and recovery.
#
# Regulatory mappings:
#   OWASP: LLM03 (Training Data Poisoning, runtime variant)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 10 (Data Governance)
#   ISM: Guidelines for System Monitoring
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Ruflo/RufRoot
# CVE-2026-59726 memory poisoning, INC-31).
# Input model: input.action.kind == "memory_write";
# input.agent.memory = {"write_auth": string, "tamper_evidence": bool}.
# Writes must be authenticated and tamper-evident; a store with tamper evidence
# is treated as compromised.

deny contains msg if {
    input.action.kind == "memory_write"
    not input.agent.memory.write_auth
    msg := sprintf("MS-10 deny: memory-store write by agent %q is unauthenticated", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "memory_write"
    input.agent.memory.tamper_evidence == true
    msg := sprintf("MS-10 deny: memory-store write by agent %q carries tamper evidence; store must be treated as compromised", [input.agent.id])
}

allow if {
    count(deny) == 0
}
