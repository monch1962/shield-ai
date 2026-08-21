package shield_ai.ee.agent_control_plane_configurat_test

import rego.v1

import data.shield_ai.ee.agent_control_plane_configurat.allow

test_workspace_writes_allowed if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace"], "loaded_from_world_writable": false}}}
    allow with input as req
}

test_control_plane_path_writable_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace", "/workspace/.claude/settings.json"], "loaded_from_world_writable": false}}}
    not allow with input as req
}

test_codex_config_self_poison_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace/.codex/config.toml"], "loaded_from_world_writable": false}}}
    not allow with input as req
}

test_world_writable_config_load_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace"], "loaded_from_world_writable": true}}}
    not allow with input as req
}
