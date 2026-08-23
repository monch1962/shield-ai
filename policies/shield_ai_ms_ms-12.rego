package shield_ai.ms.mcp_discovery_metadata_and_sha

# SHIELD-AI(TM) MS-12: MCP Discovery-Metadata and Shared-Cache Integrity
# Pillar: MS -- Model Security
#
# Prevent MCP discovery metadata and shared caches from injecting instructions into agent system prompts.
#
# Maturity indicators:
#   L1: MCP servers connected without review; discovery responses folded into context as-is; responses cached across users.
#   L2: MCP servers inventoried; instructions field flagged as untrusted; no cross-user response caching.
#   L3: Instructions isolated from the trusted system prompt with explicit boundaries and length limits; cache keys bind to authenticated identity; cacheScope claims verified; tool metadata pinned to a baseline with drift alerting.
#   L4: Signed provenance required for cached metadata; default-deny on MCP server connections with provenance verification; active red-team testing of the discovery/cache path; protocol-level fixes (instructions as untrusted content, cacheScope verification) required of vendors.
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
#     not agent.ms_ms_12
#     msg := sprintf("MS-12 violation: agent %v does not meet control requirements", [agent.id])
# }
