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

| INC | first_seen (CHANGELOG) | why no parseable `Month D, YYYY` | action |
|-----|------------------------|-----------------------------------|--------|
| INC-37 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-38 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-39 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-43 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-50 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-55 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-61 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-78 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-79 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-80 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-81 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-82 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-83 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-84 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-87 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-88 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |
| INC-89 |  | non-standard date form in source | add `Month D, YYYY` to blockquote |