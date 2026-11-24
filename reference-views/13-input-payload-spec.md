# 13 · Input Payload Specification: Generating Evaluable JSON for the Policies

How the **69 REGO policies** map to input JSON, and how to generate that JSON in
common cloud and container environments. This is the collector's companion to the
[technical verification field guide](06-controls-technical.md) and the
[deep dives](12-control-deep-dives.md): doc 06 says *what must hold*, doc 12 says
*what to look for*, this document says **exactly what JSON to emit so OPA can judge it**.

Contents

- [1 · Why a shared input envelope](#1-why-a-shared-input-envelope)
- [2 · The canonical envelope](#2-the-canonical-envelope)
- [3 · Fail-closed semantics: verified against OPA](#3-fail-closed-semantics-verified-against-opa)
- [4 · Three-plane enforcement model](#4-three-plane-enforcement-model)
- [5 · Per-platform payload generation](#5-per-platform-payload-generation)
- [6 · Field inventory: what the policies actually read](#6-field-inventory-what-the-policies-actually-read)

---

## 1 · Why a shared input envelope

The 69 policies are **not** the blocker to a consistent input format -- they already
read a coherent family of `input.*` shapes. The obstacle is that this family is
undocumented as a whole: the policies were written independently, so `input.action.*`
handles the work item, `input.agent.*` the principal, `input.data.*` the datum, and so
on -- but nothing states that contract, and evaluators have to re-derive it by reading
the `.rego`. This document makes that contract explicit and machine-traceable.

> **Inventory (derived from the policies, not invented):** the 69 policies reference **138 distinct `input.*` paths** across **16 top-level sections**. The bulk sits under `input.action` (318 field references) and `input.agent` (149 references). Everything the collector must produce is a member of exactly these sections.

**Design decision (from the architecture review):** one canonical, **sparse** envelope for every evaluation. A policy reads only the slice of the envelope that is *its* concern; a collector emits the whole envelope but omits any field it cannot truthfully attest (fail-closed under `not` -- see section 3). No per-control bespoke payloads, no schema redesign of the existing paths.

---

## 2 · The canonical envelope

One JSON document, versioned, is the single input contract. Every adapter below emits this shape (empty sections omitted or emitted as `null`); every OPA call evaluates the same envelope regardless of environment.

```json
{
  "schema_version": "1",
  "env": { "platform": "k8s | ecs | lambda | aci | cloudrun | container | other",
            "plane": "runtime | admission | build-ci",
            "observed_at": "<RFC3339>" },
  "action":   { "kind": "...", "tool": "...", "egress": "...", "code": {...}, ... },
  "agent":    { "id": "...", "sandboxed": bool, "credentials": {...}, ... },
  "model":    { "inventory": {...}, "supply_chain": {...}, ... },
  "data":     { "classified": bool, "label": "...", ... },
  "governance": { "body": {...}, "risk": {...}, "compliance": {...}, ... },
  "training": { "provenance_tracked": bool, ... },
  "approval": { "present": bool, "channel": "...", ... },
  "tenant":   { "id": "...", "scoped": bool },
  "pipeline": { "run_signed": bool, ... },
  "dependencies": { "scanned": bool, ... },
  "tools":    { "chain_analysed": bool, ... },
  "incident": { "playbook": "...", ... },
  "context":  { "content": [...], ... },
  "evaluation": {"env_indistinguishable": bool, ...}
}
```

Each section groups the fields one pillar family reads, so **you can populate the envelope section-by-section as your telemetry allows** -- a CI scanner may never produce `agent.sandbox_attestation`, and that is fine as long as it omits the field (fail-closed under `not`) rather than fabricating a safe-looking value (section 3).

**Mapping from pillars to envelope sections** (derived from which sections each pillar's controls read):

- **EE · Execution Environment** reads `agent`(9), `harness`(8), `action`(7).
- **MS · Model Security** reads `action`(27), `model`(8), `agent`(8), `approval`(5), `training`(4).
- **IAM · Identity & Access** reads `agent`(18), `action`(4), `approval`(3), `tenant`(2).
- **DS · Data Security** reads `action`(10), `data`(5), `agent`(3), `training`(3), `approval`(3).
- **TP · Tool & Pipeline Security** reads `action`(39), `dependencies`(6), `pipeline`(5), `tools`(4), `approval`(4).
- **MIR · Monitoring, Logging & IR** reads `action`(14), `agent`(5), `incident`(5).
- **GRM · Governance & Risk** reads `action`(8), `governance`(6), `vendors`(5), `agent`(1).

---

## 3 · Fail-closed semantics: verified against OPA

**This is the single correctness invariant of the whole implementation, and it is subtler than intuition suggests -- so it was verified empirically with the OPA engine before being written into this document.** A deny rule *fails closed* by using `not` (101 rules) or an explicit `!=`/`== false` (39 rules) to block an action when a safety condition is absent. The hazard is a collector that emits a value which makes a deny *condition* false -- silently allowing an action the policy intended to block.

Testing `input.agent.sandboxed` under the two dominant rule forms (versus the engine):

| `input.agent.sandboxed` | rule `not input.agent.sandboxed` | rule `input.agent.sandboxed != true` |
|---|---|---|
| *(omitted / `undefined`)* | **denies** (fail closed) ✓ | does not fire ✗ |
| `false` | **denies** ✓ | **denies** ✓ |
| `"unobserved"` (truthy string) | does **not** fire ✗ (silent bypass) | **denies** ✓ |
| `true` | no deny ✓ | no deny ✓ |

**Two concrete conclusions:**

- **Omitting a field is *fail-closed* under `not input.X`** (the dominant 101-rule form): Rego treats `not <undefined>` as satisfied, so the deny fires. A collector that simply cannot attest a `not`-guarded field is safe to omit it.
- **Emitting a truthy sentinel string like `"unobserved"` is the exact trap:** it makes `not input.X` *false*, so the deny does **not** fire -- a silent bypass. Never overload a bool/enum field the policy guards with a sentinel string.

**Safe realisation rules:**

- **A truthy, non-real value must never be placed in a field the policy guards with `not` or `== false`.** If you want to record *"could not attest"* distinctly, do it in a sibling provenance field (e.g. `agent.sandboxed: false` + `agent.sandbox_observed: false`), never by making the guarded field itself truthy.
- **For `!= true` / `== false` guarded fields, emit `false`** (not a string): `false != true` denies and `not false` denies, so boolean `false` fails closed under *both* rule forms. It is the only value that is safe across the whole policy set.
- **Enforce an envelope pre-check as defense-in-depth** -- a meta-rule denies any request whose plane-attested section is incomplete (e.g. the runtime plane requires `agent.sandboxed` to be present-or-`false`, never an unexpected type). This catches collector bugs regardless of rule form.

The invariant that must never be violated: **a collector must never fabricate a safe-looking value for a fail-closed field it could not attest.**

---

## 4 · Three-plane enforcement model

Payloads are produced at three distinct moments, each populating the sections the platform can truthfully attest at that moment. All three emit the same envelope; they differ only in which sections are populated vs omitted (the omitted ones fail closed under `not`, per section 3).

### 4a · Runtime plane (live gate) -- `plane: runtime`

OPA is evaluated **pre-call** at the invocation point (a sidecar/interceptor in front of the agent's model, tool, and code-execution calls). The envelope is built from the **live request** + platform attestation; anything not attestable at call time is omitted so it fails closed. This is where the agent-native controls live:

- **Controls:** `DS-06`, `DS-07`, `EE-01`, `EE-06`, `GRM-03`, `IAM-03`, `IAM-10`, `MIR-01`, `MIR-02`, `MIR-03`, `MIR-05`, `MIR-06`, `MS-04`, `MS-05`, `MS-08`, `MS-09`, `MS-10`, `MS-11`, `TP-01`, `TP-02`, `TP-03`, `TP-04`, `TP-08`, `TP-09`, `TP-10`, `TP-11`, `TP-12`, `TP-14`, `TP-15`, `TP-16`.
- **Example:** a tool call arrives; the interceptor fills `action.kind="tool_call"`, `action.tool`, `agent.id`, `agent.sandboxed` from the request + attestation service; it MUST **omit** `sandboxed` (or emit `false`, never a truthy string) if the runtime cannot prove the agent was in an isolated boundary.

### 4b · Admission plane (pre-deploy) -- `plane: admission`

Gatekeeper/Webhook (Kubernetes) or an IaC admission check evaluates **declared** configuration before a workload is admitted. Populates the declarative sections: `agent.identity/delegation/config`, `action.gateway/egress`, `data.*`, `tenant`, `governance.*`.

- **Controls:** `EE-02`, `EE-05`, `EE-07`, `IAM-01`, `IAM-02`, `IAM-04`, `IAM-05`, `IAM-06`, `IAM-07`, `IAM-08`, `IAM-09`, `DS-01`, `DS-03`, `DS-04`, `TP-05`, `TP-08`, `GRM-01`, `GRM-02`, `GRM-04`, `GRM-05`, `GRM-06`.
- **Example:** a Deployment manifest is the input; the adapter maps `spec.template.spec.containers[].securityContext` → `agent.sandboxed`/`config`, RBAC → `agent.delegation`, namespace → `tenant`.

### 4c · Build / CI plane -- `plane: build-ci`

Conftest or a CI scanner evaluates pipeline configuration and artifacts (SBOM, dependencies, image policies) at build time. Populates `training*`, `model.supply_chain/
inventory`, `dependencies*`, `pipeline*`, `tools*`, `vendors*`, `governance*`.

- **Controls:** `MS-01`, `MS-02`, `MS-03`, `MS-06`, `MS-07`, `MS-12`, `MS-13`, `MS-14`, `MS-15`, `DS-02`, `DS-05`, `DS-08`, `TP-05`, `TP-06`, `TP-07`, `TP-13`, `GRM-04`.
- **Example:** a container image is scanned in CI; the adapter maps the SBOM → `dependencies`, image provenance → `model.supply_chain`, configured secrets → `training.sanitised`.

---

## 5 · Per-platform payload generation

Every common environment exposes a native context (event shape, manifest, API call) that a small **adapter** maps onto the canonical envelope. One envelope, many normalisers. The adapters below are the 90% of real deployments; other platforms are the same pattern.

### 5a · Kubernetes (admission + runtime)

- **Source:** `AdmissionReview` (admission), workload/RBAC manifests (admission), kube-apiserver audit + container runtime events (runtime).
- **Map:** `userInfo`/`spec.serviceAccount` → `agent.identity`; `spec.template.spec.containers[].securityContext` + `runtimeClass` → `agent.sandboxed`/`config`; RBAC Role/ClusterRole → `agent.delegation`; namespace → `tenant.id`; NetworkPolicy/egress → `action.egress`.

### 5b · Docker / containerd / OCI (runtime)

- **Source:** containerd/runc events, image OCI config, `docker inspect`, cgroup/caps.
- **Map:** container capabilities + seccomp/apparmor profile → `agent.config` / `agent.sandbox_attestation`; host mounts → `agent.config.path_writable`; runtime `exec`/`spawn` events → `action.kind="code_execution"`, `action.code.*`.

### 5c · AWS (ECS/Fargate, Lambda, Bedrock)

- **Source:** ECS task definitions (admission), Lambda event + execution env (runtime), Bedrock agent invocation events (runtime).
- **Map:** task roles/policies → `agent.delegation`/`identity`; Lambda runtime + IAM → `agent.sandboxed`/`config`; Bedrock `agentAliasId`/tool definitions → `agent.id`, `action.tool`, `action.tool_def_signed`.

### 5d · Azure (ACI / Container Apps / AI Foundry)

- **Map:** ACI container group identity + image → `agent.identity`/`model.supply_chain`; Container Apps ingress → `action.gateway`/`egress`; managed-identity scopes → `agent.delegation`.

### 5e · GCP (Cloud Run / Vertex)

- **Map:** Cloud Run service account + image digest → `agent.identity` + `model.supply_chain`; request metadata → `action.*` (kind/tool/target); IAM binding → `agent.delegation`.

### 5f · Generic container (containerd-compatible)

- **Source:** runtime event stream (type:image-create / type:container-start / type:exec), OCI config, capability list.
- **Map:** to `action.kind`, `action.code`, `agent.config`, `agent.sandboxed`.
Cache attestations so an `exec` event can be judged against the container's actual `sandboxed` state, not a claim from image metadata.

---

## 6 · Field inventory: what the policies actually read

The authoritative field list (derived from the .rego, so it cannot drift):

**138 distinct `input.*` paths** across **16** sections.

- **`input.action`** (318 references): `input.action.kind`, `input.action.tool`, `input.action.skill`, `input.action.egress`, `input.action.record`, `input.action.outbound`, `input.action.high_risk_class`, `input.action.tool_output`, `input.action.discovery`, `input.action.dependency`, `input.action.target`, `input.action.code`, `input.action.gateway`, `input.action.transcript`, `input.action.connection`, `input.action.provenance`, `input.action.trigger`, `input.action.high_impact`, `input.action.tool_auth`, `input.action.vendor_used`, `input.action.output_scan`, `input.action.pooled_store`, `input.action.cross_tenant_hit`, `input.action.namespace_model_controllable`, `input.action.connection_params_bound`, `input.action.sensitive`, `input.action.prompt_captured`, `input.action.registration`, `input.action.server`, `input.action.audit_record`, `input.action.launch`, `input.action.tool_allowed`, `input.action.vendor_type`, `input.action.ownership_verified`, `input.action.anomaly_flag`, `input.action.campaign_correlated`, `input.action.registered_as_tool`, `input.action.prompt_redacted`, `input.action.incident`, `input.action.reporting_triggered`, `input.action.guardrail_evaluated`, `input.action.scope_compliant`, `input.action.allowed_binding`, `input.action.origin`, `input.action.origin_validated`, `input.action.user_controlled_object_id`, `input.action.acceptable`, `input.action.reconstructible`, `input.action.tool_def_signed`, `input.action.server_registry`, `input.action.cross_origin`, `input.action.privileged`, `input.action.document_sanitized`, `input.action.log_storage`, `input.action.writes_execution_bearing`, `input.action.token_access`
- **`input.agent`** (149 references): `input.agent.id`, `input.agent.credentials`, `input.agent.delegation`, `input.agent.memory`, `input.agent.resource_usage`, `input.agent.config`, `input.agent.sandbox_attestation`, `input.agent.identity`, `input.agent.session`, `input.agent.ephemeral`, `input.agent.sandboxed`, `input.agent.compromised`, `input.agent.session_expired`
- **`input.approval`** (26 references): `input.approval.present`, `input.approval`, `input.approval.channel`, `input.approval.bound_tool`, `input.approval.snapshot_fidelity_verified`, `input.approval.attestation_source`
- **`input.model`** (20 references): `input.model.id`, `input.model.supply_chain`, `input.model.inventory`, `input.model`, `input.model.weights_encrypted`, `input.model.key_management`
- **`input.governance`** (17 references): `input.governance.body`, `input.governance.compliance`, `input.governance.reporting`, `input.governance.risk`, `input.governance.risk_acceptance`, `input.governance.policy`
- **`input.data`** (12 references): `input.data.inference`, `input.data.access`, `input.data`, `input.data.classified`, `input.data.label`
- **`input.training`** (11 references): `input.training.governance`, `input.training.personal_data`, `input.training.consent_verified`, `input.training`, `input.training.provenance_tracked`, `input.training.sanitised`, `input.training.poison_scan`
- **`input.harness`** (8 references): `input.harness`, `input.harness.isolation_verified`, `input.harness.production_network_path`, `input.harness.can_modify_production`, `input.harness.egress_block_verified`, `input.harness.target_collision_checked`, `input.harness.run_isolated`
- **`input.incident`** (8 references): `input.incident.class`, `input.incident.acknowledged`, `input.incident`, `input.incident.playbook`, `input.incident.containment`
- **`input.context`** (8 references): `input.context.content`, `input.context.stream`
- **`input.vendors`** (7 references): `input.vendors.name`, `input.vendors`, `input.vendors.assessed`, `input.vendors.contractual_controls`, `input.vendors.right_to_audit`
- **`input.dependencies`** (7 references): `input.dependencies.critical_finding`, `input.dependencies`, `input.dependencies.scanned`, `input.dependencies.critical_blocked`, `input.dependencies.sandbox_library`, `input.dependencies.alternative_approved`
- **`input.pipeline`** (5 references): `input.pipeline`, `input.pipeline.run_signed`, `input.pipeline.attested`, `input.pipeline.security_gate_passed`, `input.pipeline.artifact_registry_immutable`
- **`input.tools`** (4 references): `input.tools`, `input.tools.chain_analysed`, `input.tools.escape_chain`, `input.tools.risk_accepted`
- **`input.evaluation`** (3 references): `input.evaluation`, `input.evaluation.env_indistinguishable`, `input.evaluation.behaviour_matches_production`
- **`input.tenant`** (3 references): `input.tenant.scoped`, `input.tenant`

### Per-control input paths (each `### CID` maps to its envelope section)

| Control | Input paths it reads |
|---|----------------------|
| `DS-01` | `input.data`, `input.action.kind`, `input.data.classified`, `input.data.label` |
| `DS-02` | `input.data.inference` |
| `DS-03` | `input.action.kind`, `input.agent.id`, `input.agent.memory` |
| `DS-04` | `input.action.kind`, `input.data.access` |
| `DS-05` | `input.action.kind`, `input.training.consent_verified`, `input.training.governance`, `input.training.personal_data` |
| `DS-06` | `input.action.kind`, `input.action.output_scan` |
| `DS-07` | `input.approval`, `input.action.kind`, `input.action.target`, `input.approval.channel`, `input.approval.present` |
| `DS-08` | `input.action.egress`, `input.action.kind`, `input.agent.id` |
| `EE-01` | `input.action.tool`, `input.agent.id`, `input.agent.sandboxed` |
| `EE-02` | `input.action.registered_as_tool`, `input.action.tool` |
| `EE-03` | `input.agent.id`, `input.agent.resource_usage` |
| `EE-04` | `input.harness`, `input.action.kind`, `input.harness.can_modify_production`, `input.harness.isolation_verified`, `input.harness.production_network_path` |
| `EE-05` | `input.action.kind`, `input.agent.config`, `input.agent.id` |
| `EE-06` | `input.action.kind`, `input.agent.id`, `input.agent.sandbox_attestation` |
| `EE-07` | `input.agent.config` |
| `EE-08` | `input.harness`, `input.action.kind`, `input.harness.egress_block_verified`, `input.harness.run_isolated`, `input.harness.target_collision_checked` |
| `GRM-01` | `input.action.kind`, `input.governance.body` |
| `GRM-02` | `input.action.high_risk_class`, `input.governance.risk` |
| `GRM-03` | `input.action.acceptable`, `input.action.high_risk_class`, `input.action.tool`, `input.agent.id`, `input.governance.policy` |
| `GRM-04` | `input.vendors`, `input.action.vendor_type`, `input.action.vendor_used`, `input.vendors.assessed`, `input.vendors.contractual_controls`, `input.vendors.name`, `input.vendors.right_to_audit` |
| `GRM-05` | `input.action.kind`, `input.governance.compliance` |
| `GRM-06` | `input.governance.reporting`, `input.governance.risk_acceptance` |
| `IAM-01` | `input.agent.id`, `input.agent.identity` |
| `IAM-02` | `input.agent.delegation`, `input.agent.id` |
| `IAM-03` | `input.approval`, `input.action.high_risk_class`, `input.agent.id`, `input.approval.channel`, `input.approval.present` |
| `IAM-04` | `input.agent.compromised`, `input.agent.credentials`, `input.agent.id` |
| `IAM-05` | `input.agent.credentials`, `input.agent.id`, `input.agent.session_expired` |
| `IAM-06` | `input.agent.id`, `input.agent.session` |
| `IAM-07` | `input.agent.delegation`, `input.agent.id` |
| `IAM-08` | `input.agent.credentials`, `input.agent.id` |
| `IAM-09` | `input.tenant`, `input.action.user_controlled_object_id`, `input.tenant.scoped` |
| `IAM-10` | `input.action.kind`, `input.action.record`, `input.agent.id` |
| `MIR-01` | `input.action.audit_record`, `input.action.log_storage`, `input.action.tool`, `input.agent.id` |
| `MIR-02` | `input.action.anomaly_flag`, `input.action.campaign_correlated`, `input.action.tool`, `input.agent.ephemeral`, `input.agent.id` |
| `MIR-03` | `input.action.prompt_captured`, `input.action.prompt_redacted`, `input.action.sensitive` |
| `MIR-04` | `input.incident`, `input.incident.acknowledged`, `input.incident.class`, `input.incident.containment`, `input.incident.playbook` |
| `MIR-05` | `input.action.incident`, `input.action.reporting_triggered`, `input.agent.id` |
| `MIR-06` | `input.action.high_impact`, `input.action.reconstructible`, `input.action.tool`, `input.agent.id` |
| `MS-01` | `input.model`, `input.model.id`, `input.model.key_management`, `input.model.weights_encrypted` |
| `MS-02` | `input.training`, `input.action.kind`, `input.training.poison_scan`, `input.training.provenance_tracked`, `input.training.sanitised` |
| `MS-03` | `input.action.kind`, `input.model.id`, `input.model.supply_chain` |
| `MS-04` | `input.context.content` |
| `MS-05` | `input.action.guardrail_evaluated`, `input.action.kind`, `input.action.scope_compliant`, `input.agent.id` |
| `MS-06` | `input.action.kind`, `input.model.id`, `input.model.inventory` |
| `MS-07` | `input.evaluation`, `input.action.kind`, `input.evaluation.behaviour_matches_production`, `input.evaluation.env_indistinguishable` |
| `MS-08` | `input.action.kind`, `input.action.server`, `input.action.server_registry`, `input.action.tool_def_signed`, `input.action.writes_execution_bearing` |
| `MS-09` | `input.approval`, `input.approval.attestation_source`, `input.approval.present`, `input.approval.snapshot_fidelity_verified`, `input.context.content` |
| `MS-10` | `input.action.kind`, `input.agent.id`, `input.agent.memory` |
| `MS-11` | `input.action.high_impact`, `input.action.trigger`, `input.approval.present`, `input.context.stream` |
| `MS-12` | `input.action.discovery`, `input.action.kind`, `input.agent.id` |
| `MS-13` | `input.action.kind`, `input.action.transcript`, `input.agent.id` |
| `MS-14` | `input.action.kind`, `input.action.outbound`, `input.agent.id` |
| `MS-15` | `input.action.connection_params_bound`, `input.action.cross_tenant_hit`, `input.action.kind`, `input.action.namespace_model_controllable`, `input.action.ownership_verified`, `input.action.pooled_store`, `input.agent.id`, `input.agent.memory` |
| `TP-01` | `input.action.tool` |
| `TP-02` | `input.action.tool`, `input.action.tool_allowed`, `input.action.tool_auth` |
| `TP-03` | `input.action.gateway`, `input.action.tool` |
| `TP-04` | `input.action.tool`, `input.action.tool_output` |
| `TP-05` | `input.pipeline`, `input.action.kind`, `input.pipeline.artifact_registry_immutable`, `input.pipeline.attested`, `input.pipeline.run_signed`, `input.pipeline.security_gate_passed` |
| `TP-06` | `input.dependencies`, `input.action.kind`, `input.dependencies.alternative_approved`, `input.dependencies.critical_blocked`, `input.dependencies.critical_finding`, `input.dependencies.sandbox_library`, `input.dependencies.scanned` |
| `TP-07` | `input.tools`, `input.action.kind`, `input.tools.chain_analysed`, `input.tools.escape_chain`, `input.tools.risk_accepted` |
| `TP-08` | `input.action.gateway`, `input.action.tool` |
| `TP-09` | `input.action.kind`, `input.action.registration`, `input.action.tool` |
| `TP-10` | `input.action.allowed_binding`, `input.action.kind`, `input.action.origin`, `input.action.origin_validated`, `input.action.target` |
| `TP-11` | `input.action.cross_origin`, `input.action.document_sanitized`, `input.action.kind`, `input.action.privileged`, `input.action.token_access`, `input.action.tool`, `input.approval.present` |
| `TP-12` | `input.approval`, `input.action.kind`, `input.action.provenance`, `input.action.tool`, `input.approval.bound_tool`, `input.approval.present` |
| `TP-13` | `input.action.dependency`, `input.action.kind`, `input.agent.id` |
| `TP-14` | `input.action.kind`, `input.action.skill`, `input.agent.id` |
| `TP-15` | `input.action.code`, `input.action.kind`, `input.agent.id` |
| `TP-16` | `input.action.connection`, `input.action.kind`, `input.action.launch`, `input.agent.id` |

---

**How to use this document:** start from doc 06 (what must hold) and doc 12 (what to look for), then build the `send my data as the envelope; omit what I cannot attest` collector for each plane you enforce. The inventory above is regenerated from the policies, so it stays current as controls evolve.
