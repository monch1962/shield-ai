# SHIELD-AI Reference Implementation (Milestone 2)

A runnable reference implementation of the deployable components described in
[`framework/shield-ai-implementation-architecture.md`](../framework/shield-ai-implementation-architecture.md):
the tool gateway / sidecar proxy, the OPA policy layer running the **full 59
control set**, and the telemetry pipeline (MIR-01..06). It turns "audit becomes
a test run" into an HTTP surface: every agent action is evaluated deny-override
against all 59 policies before it is permitted, and every verdict is an audit
event.

This is a *reference* implementation, not production tooling. It demonstrates
the enforcement model end-to-end with a deliberately small, dependency-free
codebase so the mapping to the framework stays visible. The gap list at the
bottom names what production would replace.

## Architecture mapping

| Reference-impl component | Implementation-architecture component | Zone | Controls demonstrated |
|--------------------------|---------------------------------------|------|-----------------------|
| `sidecar/` (Go, stdlib only) | Tool gateway / sidecar proxy (Group 5) | Zone 2 | TP-01..04, TP-08, TP-09, TP-12 |
| OPA server with `policies/` bundle | Policy decision points (Group 6) | Zone 3 | all 59, deny-override |
| `sidecar/` input enricher | Policy input documents (Section 3) | Zone 2 | agent, action, context, approval |
| JSONL audit events + SIEM forward | Telemetry and SIEM pipeline (Group 7) | Zone 2 | MIR-01, MIR-03, MIR-06 |
| `agents/`, `tools/`, `deployment.json` | Component configuration (Section 7) | Zone 2/3 | IAM, EE, GRM claims |

## How enforcement works

Every decision goes through one round trip to the decision point:

1. **Enrich** — the sidecar merges the request over three static claim sources:
   the organisation posture (`deployment.json`), the agent's identity and
   limits (`agents/*.json`), and the tool registry (`tools/*.json`). It then
   attests the fields it itself enforces: gateway controls (TP-02/03/08),
   audit-pipeline claims (MIR-01/03/06), tenant scoping (IAM-09), and dispatch
   provenance (TP-12).
2. **Evaluate** — `POST /v1/data/shield_ai` with the enriched input. All 59
   packages evaluate the same action.
3. **Aggregate** — deny wins over allow. A single deny anywhere blocks the
   action and its message is returned. `allow if count(deny) == 0` means a
   fired deny leaves `allow` undefined, so the aggregator treats any deny as a
   block. If the engine is unreachable, or no policy package evaluates, the
   action is blocked (fail closed).
4. **Audit** — one JSONL event per decision (identifiers + verdict, no
   prompt/response bodies) to stdout, forwarded to the SIEM sink when
   configured. Sensitive actions carry the captured/redacted prompt claims
   (MIR-03) so the policy set enforces them too.

## Run it

### Option A: containers

```bash
docker compose up -d --build     # podman: podman-compose up -d --build
```

### Option B: local processes (no containers)

```bash
make e2e     # builds, starts OPA + mock + sidecar, asserts all six verdicts
```

## Evaluate actions

```bash
curl -s -X POST localhost:8080/v1/decide -d @inputs/allow_benign.json
# {"allowed":true,"correlation_id":"cid-...","denies":[]}

curl -s -X POST localhost:8080/v1/decide -d @inputs/deny_unregistered_tool.json
# 403 {"allowed":false,"denies":["TP-01 deny: tool \"drop_database\" is not in the approved tool registry", ...]}
```

Sample matrix (asserted by `scripts/e2e.sh`):

| Input | Expected | Denies demonstrate |
|-------|----------|--------------------|
| `allow_benign.json` | 200 allow | none (clean registered tool call) |
| `allow_approved_transfer.json` | 200 allow | positive control: approved financial action passes all 59 |
| `deny_unregistered_tool.json` | 403 | TP-01, TP-09, TP-02 |
| `deny_unsandboxed_highrisk.json` | 403 | EE-01 (high-risk tool, unsandboxed) |
| `deny_injection.json` | 403 | MS-04 + MS-09 (imperceptible content, no fidelity snapshot) |
| `deny_infra_api.json` | 403 | EE-02 + TP-01 (infrastructure control plane) |

## Configuration

- `deployment.json` — organisation posture: governance body, risk register,
  compliance mapping, model/training/data claims, evaluation harness and
  pipeline attestations. These are the claims the operator asserts once; the
  policies turn them into gates.
- `agents/*.json` — per-agent identity, credentials, delegation bounds,
  resource limits, writable paths, tenant, and tool allowlist.
- `tools/*.json` — the explicit tool registry: endpoint, risk class,
  sensitivity, schema fields. A tool not registered here is
  `registered_as_tool: false` and fails TP-01/09/02.
- `inputs/*.json` — sample decision requests (agent + action + context +
  approval).

Merge order: deployment posture → agent claims → request → sidecar-attested
fields (gateway, audit, tenant, provenance).

## Endpoints

- `POST /v1/decide` — evaluate one action. 200 = allow, 403 = deny (denies in
  the body), 400 = malformed or missing agent.id / action.tool.
- `GET /v1/health` — sidecar liveness plus OPA reachability.

## Deliberate gaps (what production replaces)

| Reference choice | Production replacement |
|------------------|------------------------|
| Minted provenance (`"model_sig": "sidecar-minted"`) | Model-turn signature from the dispatch authenticator (TP-12) |
| Config-file agent identities | SPIFFE/SPIRE workload identities (IAM-01) |
| JSONL stdout + HTTP SIEM forward | OTLP exporter to the telemetry pipeline (MIR-01/03/06) |
| Static tool registry with schema fields | TUF-signed tool definitions, MCP gateway (MS-08, TP-01) |
| `mocktool` endpoints | Real registered tools behind the allow-listed gateway |
| Approval channel asserted by the caller | Approval console binding with out-of-band verification (IAM-03, MS-09) |
| No TLS on the sidecar | mTLS between agent, sidecar, and decision point |

## Keeping it honest

The 59 policies are the same files the framework ships in `policies/`; the
sidecar adds no second opinion of its own. If the policy set changes, the
bundle rebuild is one command (`make bundle`), and the e2e matrix re-asserts
the verdicts. That is the property the framework sells: the audit is the test
run.
