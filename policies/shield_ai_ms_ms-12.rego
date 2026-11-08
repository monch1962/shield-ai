package shield_ai.ms.mcp_discovery_metadata_shared_cache_integrity

import rego.v1

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

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (MCP-2026-008 cache
# poisoning, MCP-2026-015 instructions-field injection, Context7 CVE-2026-75130,
# INC-37). Input model: input.action.kind == "mcp_discovery"; a discovery
# response must keep server-supplied instructions untrusted and isolated,
# length-limited, bind caches to a verified authenticated identity with signed
# provenance across auth contexts, and validate tool metadata against its
# baseline as an aggregate set.

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.instructions_length_limited == false
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q carries unbounded server-supplied instructions; must be length-limited", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.instructions_isolated == false
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q folds server-supplied instructions into the trusted system prompt; must be isolated as untrusted content", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.shared_cache_cross_auth == true
    input.action.discovery.cache_provenance_signed == false
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q is served from a shared cache across authentication contexts without signed provenance", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.cache_scope_verified == false
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q trusts a server cacheScope claim without verification", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.cache_key_bound_to_identity == false
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q uses a cache key not bound to the authenticated identity", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "mcp_discovery"
    input.action.discovery.tool_metadata_baseline_drifted == true
    msg := sprintf("MS-12 deny: MCP discovery response for agent %q tool metadata drifted from the operator-approved baseline; alert via MIR-01", [input.agent.id])
}

allow if {
    count(deny) == 0
}