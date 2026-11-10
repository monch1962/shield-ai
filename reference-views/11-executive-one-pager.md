# 11 · Executive One-Pager

A one-page view for a board member or senior executive, derived from the committed framework and incident evidence.

## The picture in numbers

- **69 controls** across the seven pillars that protect the model, identity, data, tools, monitoring, and governance of agentic AI.
- **69 controls (100%)** already have an executable verification policy enforcing **195** fail-closed conditions.
- **912 control-incident references** in the catalogue (92 events) show where real-world risk actually surfaces.

## Top controls to harden

- **MS-08: MCP** - Verify that mcp holds under agent action (61 incident refs). Evidence: [incident summary](07-incident-summaries.md#inc-12-mcp-protocol-layer-vulnerabilities).
- **EE-01: Execution environment boundary enforcement** - Verify that execution environment boundary enforcement holds under agent action (51 incident refs). Evidence: [incident summary](07-incident-summaries.md#inc-11-pillar-security-week-of-sandbox-escapes).
- **TP-15: In-process code-execution sandbox sufficiency** - Verify that in-process code-execution sandbox sufficiency holds under agent action (49 incident refs). Evidence: [incident summary](07-incident-summaries.md#inc-58-in-process-denylistblocklist-code-execution-sandbox-bypass).

## Recommended next steps

- Close the highest-evidenced gaps first - the controls most often shown up by real incidents are where hardening pays fastest.
- Raise each pillar toward **L3** (automated, board-reported security), the level regulated Australian entities target.
- Keep every control verified by an executable policy so posture is measured, not asserted.

## Where we stand

- **EE (Execution Environment):** target seccomp/apparmor, host file-injection prevention, fail-closed sandbox operation,.
- **MS (Model Security):** target Adversarial testing programme, imperceptible-content sanitisation, memory tamper.
- **IAM (Identity & Access):** target JIT access, approval gates, delegation chain enforcement.
- **DS (Data Security):** target End-to-end inference encryption, artifact publication pipeline.
- **TP (Tool & Pipeline Security):** target API gateway with schema validation, infrastructure-isolation mode, explicit tool.
- **MIR (Monitoring, Logging & IR):** target Anomaly detection, IR playbooks.
- **GRM (Governance & Risk):** target Board reporting, regulatory mapping.
