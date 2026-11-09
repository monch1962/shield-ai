# Source-Date Debt

Incidents whose `### INC-n` source blockquote does not carry a parseable
`Month D, YYYY` publication date, so the latency KPI cannot attribute a
publication→record lag for them.

**Tracking:** `tools/latency_ledger.py` enforces this file as a ratchet in the
same spirit as the misfit and freshness gates. A dated incident with no parseable
source date must be listed here, and every listed incident must still lack one.
When an entry gains a real `Month D, YYYY` publication date in its blockquote,
remove it from the table in the same commit — the gate then goes back to green.
Adding a date by fabrication is never acceptable; the debt file is how the
cadence owns the cleanup instead of hiding it.

**Advice for fixing a row:** many of these are incidents whose blockquote says
`reported Aug 29`, `patched Sept 28`, `disclosed Oct 19` (month-abbrev / no year
inline) rather than a full `November 5, 2026`. Add the publication date in that
full form to the source blockquote text and drop the row from this table.

**Cleared (Nov 2026).** The 17 historically-flagged incidents
(INC-37/38/39/43/50/55/61/78/79/80/81/82/83/84/87/88/89) each had their
publication date transcribed into their source blockquote from the primary
source (NVD publish dates for CVE-2026-25536/54769/54688/34742; arXiv
submission dates for 2606.27027, 2610.04195, 2611.03555, 2610.22301,
2609.04533; Ars Technica, Unit 42, Hunt.io, Radware, JFrog publication dates).
The latency KPI now attributes all 56 dated incidents, raising its coverage for
that pool to 100% while keeping every date verifiable — no date was invented.

| INC | first_seen (CHANGELOG) | why no parseable `Month D, YYYY` | action |
|-----|------------------------|-----------------------------------|--------|