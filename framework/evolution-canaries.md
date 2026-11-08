# SHIELD-AI Evolution Canaries (DNA-test source)

This file is the **game-proof DNA test** of the framework's ability to evolve.
Each row is a structurally-real threat class that is **not yet a structural gap
(G1..G34)** but is externally sourced and tracked. The `check_evolution_dna.py`
gate refuses the build if the taxonomy drifts on these:

- a canary claims **coverage** without a real, implemented (non-stub) control —
  coverage has to be earned, not asserted;
- a canary stays **open past its `review_due`** — the taxonomy must actively
  re-attest or absorb new classes on an event-driven cadence, not on
  calendar-and-memory.

First-seen dates are the cycle dates the class entered the watchlist (version /
edition dates in the repo), never authored ad hoc. `review_due` advances one
monthly deep-review cycle at a time and is bumped by the operator each cycle.

To add a canary: append a row. To mark one covered: set Status to `covered` and
name the covering control (must be an implemented non-stub policy) and gap. The
gate derives nothing about the threat itself — it only verifies the taxonomy and
the enforcement answered it.

| Canary ID | Threat class | External source | first_seen | review_due | Status | Covering control | Gap |
|---|---|---|---|---|---|---|---|
| C-01 | **MCP→A2A cross-protocol trust propagation** — trust learned over MCP being replayed over A2A to peer agents with no identity propagation; internal Google/Rapid7/JP Morgan deployments. | Rapid7 CVE-2026-97228; Google mcp-toolbox (CVSS 8.0, no CheckRedirect); arXiv 2610.22301 / 2611.03555 (INC-88) | 2026-11-08 | 2026-12-09 | open | — | — |
| C-02 | **Agent-originated artifact quarantine-window abuse / delayed activation** — a skill/package passes install checks, then exfiltrates or activates 24-48h later, defeating time-based supply-chain defences. | Watchlist scenario B (quarantine-window abuse); TrapDoor-class registry campaigns | 2026-11-09 | 2026-12-09 | open | — | — |
| C-03 | **NOOA↔SHIELD-AI attestation conflict** — NOOA (NVIDIA Open Secure AI Alliance, launched 27 Jul 2026) defining controls that contradict SHIELD-AI EE/IAM; forces a client choice and undermines a coverage claim. | The Hacker News, "NVIDIA Forms 37-Member Open Secure AI Alliance" (27 Jul 2026) | 2026-11-09 | 2026-12-09 | open | — | — |
| C-04 | **AI-gateway MCP endpoint exposure** — an AI gateway shipping MCP endpoints enabled-by-default inheriting gateway credentials; CSWSH-style WebSocket takeover; systemic MCP data-plane flaw. | OX Security systemic MCP flaw; INC-76 mcp-contextforge-gateway CVE-2026-53710; MCP/WebSocket upgrade path (INC-78) | 2026-11-09 | 2026-12-09 | open | — | — |
| C-05 | **Guardrail-erosion as initial access** — a month-long slow-erosion campaign converting an enterprise coding agent into an intrusion platform, via bug-bounty/Mexico-class intrusion. | Bloomberg/Gambit Security Mexico breach (25 Feb 2026); CSA "When AI Agents Attack" (INC-49/INC-40 reconstruction) | 2026-11-09 | 2026-12-09 | open | — | — |
| C-06 | **Backdated provenance of agent-originated artifacts** — forged provenance timestamps defeat time-correlation analysis of agent-published packages. | Watchlist scenario C (backdated provenance); DS-07/TP-14 quarantine interactions | 2026-11-09 | 2026-12-09 | open | — | — |

## Discipline

The gate reads this file only. It verifies:

1. **Every canary has a non-empty external source** (anti-fabrication).
2. **Dates are well-formed** and `review_due >= first_seen`.
3. **Sunrise discipline:** if today is past `review_due` and the row is still
   `open`, the build fails — the canary must be re-attested (bump `review_due`
   one cycle) or absorbed (Status → `covered`). This is the event-driven trigger
   that replaces calendar-and-memory.
4. **Coverage must be earned:** a `covered` canary must name a covering control
   whose policy file exists and is not a stub, plus a gap (G-k). You cannot mark
   a class covered without real, testable deny-override logic.
5. **No manufactured discovery:** the gate never treats an assertion as
   coverage; only a real, implemented policy satisfies it, so it cannot be gamed
   to clear a discovery-rate target.

This is the executable definition of "the framework can still evolve": absorb
genuinely new classes into real, enforced controls, or actively re-attest the
open ones — never let them rot unmeasured.