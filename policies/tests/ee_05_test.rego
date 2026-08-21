package shield_ai.ee.host_trusted_configuration_fil_test

import rego.v1

import data.shield_ai.ee.host_trusted_configuration_fil.allow

test_workspace_only_writes_allowed if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace/src"]}}, "action": {"kind": "file_write"}}
    allow with input as req
}

test_shell_startup_file_write_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace", "/home/agent/.zshrc"]}}, "action": {"kind": "file_write"}}
    not allow with input as req
}

test_git_config_write_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/repo/.git/config"]}}, "action": {"kind": "file_write"}}
    not allow with input as req
}

test_vscode_settings_write_denied if {
    req := {"agent": {"id": "agent-1", "config": {"path_writable": ["/workspace/.vscode/settings.json"]}}, "action": {"kind": "file_write"}}
    not allow with input as req
}

test_file_write_without_reported_paths_fails_closed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "file_write"}}
    not allow with input as req
}
