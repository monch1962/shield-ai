# SHIELD-AI demo: policy-as-code in five minutes

This is the self-run demo we hand to prospects. It shows the framework's
core differentiator in practice: **60 controls, expressed as executable
policy, evaluated deny-override**. The full control suite lives in
`policies/` at the repo root (60 Rego policies; 59 implemented, MS-12 stub pending). This bundle is a reduced,
runnable subset of three controls so you can see enforcement working in
under five minutes.

## What you will see

The demo evaluates an **agent action** (a tool call) against three controls:

| Control | What it checks | What gets denied |
|---------|----------------|------------------|
| **MS-04** (adversarial robustness) | Agent-visible content for prompt-injection markers | Actions driven by "ignore previous instructions" style content |
| **TP-01** (tool registry) | The called tool is in the approved registry | Calls to unregistered tools (e.g. `drop_database`) |
| **EE-01** (execution boundary) | High-risk tools come only from sandboxed agents | `transfer_funds` / `write_file` from an unsandboxed agent |

And the rule that makes it a framework rather than a checklist: **deny
wins over allow**. If any control denies, the action is blocked, even when
every other check passes. If the engine is unreachable, the action is
blocked too (fail closed). This is why an audit becomes a test run: the
same evaluation that gates production also produces the evidence.

## Run it

### Option A: Docker (no local OPA needed)

```bash
docker compose up -d
```

Then evaluate an action:

```bash
# Benign: registered tool, sandboxed agent, clean content -> allowed
curl -s localhost:8181/v1/data/shield_ai/demo/allow -d @inputs/allow_benign.json
# -> {"result": true}

# Prompt injection: hidden instruction in the content -> denied
curl -s localhost:8181/v1/data/shield_ai/demo/allow -d @inputs/deny_injection.json
# -> {"result": []}   (denied)

# See WHY it was denied:
curl -s localhost:8181/v1/data/shield_ai/demo/deny -d @inputs/deny_injection.json
# -> {"result": ["MS-04 deny: prompt-injection marker ..."]}
```

Try the other inputs too: `deny_unregistered_tool.json`,
`deny_unsandboxed_highrisk.json`.

### Option B: Standalone OPA binary

```bash
opa run --server --bundle policies/
```

Then the same curl commands against `localhost:8181`.

### Verify the test suite (always green)

```bash
opa test policies tests -v
# PASS: 5/5
```

## The input shape

Each evaluation is one agent action:

```json
{
  "agent":  {"id": "agent-1", "sandboxed": true},
  "action": {"tool": "summarise_thread"},
  "context": {"content": ["text the agent read before acting"]}
}
```

The production engine evaluates the same shape against all 60 controls
plus request parsing, rate limiting, and audit logging. See
`framework/shield-ai-implementation-architecture.md` for the full
component model and `policies/` for the complete control set.

## Notes

- This is a reduced demo, not the production bundle. The repo's
  `policies/` stubs are the complete control contract; the demo bundle
  implements three controls with real logic so it runs end to end.
- Deny messages are returned to the caller for transparency. In a live
  deployment they go to the audit pipeline (MIR-01) and alerting (MIR-02)
  instead.
