# SHIELD-AI Threat Feed Manifest

This is the **exogenous intake manifest** for the evolution machinery. `collect_feed.py`
reads it as the set of trusted sources the weekly cadence sweeps. Every item that
enters the taxonomy is attributable to exactly one feed (its lineage), so the
misfit-rate can be reported **per lineage** — a narrow or vendor-biased feed cannot
masquerade as a healthy breadth signal.

The feed manifest is checked by `check_feed_misfits.py`: it verifies every listed
feed has a lineage, that the misfit ledger only cites feeds present here, and that
no single lineage dominates the open-misfit pool (selection-bias guard).

## Feed roster

| Feed ID | Lineage | Source | Why it is watched | first_added |
|---|---|---|---|---|
| FEED-01 | vendor | NVD / MITRE ATLAS agentic-AI CVE categories | CVE-grounded baseline; machine-readable | 2026-11-11 |
| FEED-02 | vendor | Vendor advisories (Google mcp-toolbox, Anthropic Git MCP, Rapid7) | First-party disclosure of agent-framework flaws | 2026-11-11 |
| FEED-03 | govt-cert | ACSC / ACSC-partner advisories | AU regulatory forcing function; national threat reporting | 2026-11-11 |
| FEED-04 | research | arXiv agent-security / trust-boundary studies | Long-range structural signal (NCSC-style research) | 2026-11-11 |
| FEED-05 | opensource | GitHub security-advisories for agent frameworks (OSV) | Ecosystem blind spots like the 17-CVE mega-cluster | 2026-11-11 |
| FEED-06 | in-the-wild | Honeypot / scout telemetry (Censys, ARMs, malware samples) | In-the-wild exploitation not yet vendor-labelled | 2026-11-11 |

## Lineage taxonomy

Misfit-rate is computed and gated **per lineage** so breadth is not a single opaque
number. `check_feed_misfits.py` fails if one lineage accounts for more than
`MAX_LINEAGE_SHARE` (default 60%) of open misfits — that would mean the intake is
vendor- or geography-biased and its low apparent misfit-rate is an artifact of a
narrow feed, not real coverage.

Lineages: `vendor`, `govt-cert`, `research`, `opensource`, `in-the-wild`.

## Discipline

- Add a feed by appending a row; first_added is the date the cadence began reading it.
- The misfit ledger (`framework/feed-misfits.md`) only cites Feed IDs from this table.
- Every misfit carries its lineage (provenance). Nothing is silently attributed.
- An item that fits an existing gap/control is NOT a misfit — it is absorbed and
  counted as normal intake. Only items that fit **no pillar** enter the misfit pool.