package shield_ai.ms.self_replication_barrier

# SHIELD-AI(TM) MS-14: Self-Replication Barrier
# Pillar: MS -- Model Security
#
# Prevent an injected instruction from being re-emitted through the agent's own output channels to propagate to other agents.
#
# Maturity indicators:
#   L1: No detection of re-emitted instruction text in outbound content.
#   L2: Automated near-verbatim detection of source-prompt n-grams in outbound payloads; documentation of the replication kill-chain.
#   L3: Fingerprint matching quarantine with human approval; one-channel-per-write and human-signoff-on-broadcast; blast-radius cap per hop.
#   L4: Worm-emulation drills prove replication is blocked; automated channel-kill and incident-response triggers on any matching propagation signal.
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for System Monitoring

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.ms_ms_14
#     msg := sprintf("MS-14 violation: agent %v does not meet control requirements", [agent.id])
# }
