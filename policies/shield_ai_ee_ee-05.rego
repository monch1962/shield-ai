package shield_ai.ee.host_trusted_configuration_fil

import rego.v1

# SHIELD-AI(TM) EE-05: Host-Trusted Configuration File Injection Prevention
# Pillar: EE -- Execution Environment
#
# Prevent indirect sandbox escape via host-trusted file injection.
#
# Maturity indicators:
#   L1: Agents can write anywhere including host-trusted paths.
#   L2: Write-path allowlist for critical paths; manual review.
#   L3: Host-trusted paths excluded from agent writes; FIM on host-trusted directories; content scanning.
#   L4: Host-side isolation preventing agent-written file execution; continuous FIM; automated response.
#
# Regulatory mappings:
#   ISM: Guidelines for System Hardening
#   Essential Eight: Application Control
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Pillar Security
# indirect-escape class, INC-11).
# Input model: input.agent.config.path_writable = paths the agent can write.
# Fail closed on missing write-path reporting: a coding agent MUST report its
# writable paths; absence means the platform cannot attest the allowlist.

# Host-trusted files the host later executes or loads as trusted configuration.
host_trusted_paths := {
    ".zshrc",
    ".bashrc",
    ".profile",
    ".vscode/settings.json",
    ".vscode/tasks.json",
    ".git/config",
    ".gitattributes",
    "bin/python",
    "node_modules/.bin",
    "crontab",
    "/etc/systemd/",
}

deny contains msg if {
    some path in input.agent.config.path_writable
    some trusted in host_trusted_paths
    contains(path, trusted)
    msg := sprintf("EE-05 deny: agent can write host-trusted path %q (indirect escape class)", [path])
}

deny contains msg if {
    input.action.kind == "file_write"
    not input.agent.config.path_writable
    msg := sprintf("EE-05 deny: agent %q file write with no reported write-path allowlist (fail closed)", [input.agent.id])
}

allow if {
    count(deny) == 0
}
