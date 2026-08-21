package shield_ai.ee.agent_control_plane_configurat

import rego.v1

# SHIELD-AI(TM) EE-07: Agent Control-Plane Configuration Integrity
# Pillar: EE -- Execution Environment
#
# Prevent agents from disabling their own security controls.
#
# Maturity indicators:
#   L1: Agents can modify their own security configuration; tools load config from writable paths.
#   L2: Control-plane config documented; agent write access partially restricted.
#   L3: Control-plane config read-only to the agent; world-writable paths rejected; integrity monitoring on control files.
#   L4: Continuous integrity verification; automated blocking of self-configuration changes; config-trust vulnerability patching.
#
# Regulatory mappings:
#   NIST AI RMF: PROTECT (PR.AC)
#   EU AI Act: Art. 15(b)
#   ISM: Guidelines for System Hardening
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Codex config
# self-poisoning INC-14, CVE-2026-35603 config-trust INC-15).
# Input model: input.agent.config = {"path_writable": [..],
# "loaded_from_world_writable": bool}. Missing config claims are treated as no
# writable claims; the world-writable load direction is enforced separately.

# Agent control-plane paths: writing to any of these self-disarms the agent's
# security controls (sandbox mode, approval policy, hooks, MCP launch config).
control_plane_paths := {
    ".codex/",
    ".claude/",
    ".cursor/",
    "managed-settings.json",
    "mcp.json",
    ".mcp.json",
    "settings.json",
}

deny contains msg if {
    some path in input.agent.config.path_writable
    some cp in control_plane_paths
    contains(path, cp)
    msg := sprintf("EE-07 deny: agent control-plane path %q is writable by the agent", [path])
}

deny contains msg if {
    input.agent.config.loaded_from_world_writable == true
    msg := "EE-07 deny: agent configuration loaded from a world-writable location (config-trust class)"
}

allow if {
    count(deny) == 0
}
