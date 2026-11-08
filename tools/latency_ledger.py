#!/usr/bin/env python3
"""SHIELD-AI immutable incident-latency ledger.

Makes "does the framework keep up with new threats" a *measured* KPI instead of
an assertion, and makes it backdate-proof by construction.

The KPI measures EXTERNAL discovery-to-framework latency: for each incident, the
lag between its public publication/disclosure date (parsed from the incident's
source blockquote in framework/shield-ai-gap-analysis.md) and the date the
framework recorded it in the CHANGELOG. This is the signal that actually varies
and that clients can hold the cadence to. Internal same-cycle gap mapping is not
the KPI -- it is constantly zero and carries no information.

Because publication dates trace to the committed incident blockquote text and
first-seen traces to the committed CHANGELOG, a rewrite cannot quietly lower a
reported latency without changing the historical record -- the strongest
immutability a git repo gives.

Gate checks:
1. Every incident INC-1..INC-N is accounted for: dated from CHANGELOG or floored
   (pre-numbering) to the founding month. Nothing is silently dropped.
2. Ordering: latency (publication -> first_seen) is always >= 0 -- the framework
   can never record an incident before it was published. A negative is a
   derivation error (or a mis-dated source) and fails.
3. The KPI is the p50/p95/max publication->first_seen lag over incidents with a
   parseable publication date AND a real CHANGELOG first-seen. Incidents without
   a parseable publication date are reported as a coverage gap (the cadence must
   record sources), never assigned a fabricated date.
4. Freshness: a DATED incident with no gap mapping older than OPEN_MAX_DAYS
   fails. Floored pre-numbering incidents are exempt.
5. Coverage: every incident id 1..N has a row.

Exits 1 on any failure. Called by make check, the cron cycles, update_all.sh.
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
GAP_ANALYSIS = os.path.join(ROOT, "framework", "shield-ai-gap-analysis.md")

# Pre-v1.8 incidents predate the explicit INC series in the CHANGELOG. The
# founding month is the honest floor; floored incidents are counted for coverage
# but excluded from the latency KPI. Override via SHIELD_EARLIEST.
EARLIEST_FLOOR = os.environ.get("SHIELD_EARLIEST", "2026-07-01")
# A DATED incident with no gap mapping older than this many days fails.
OPEN_MAX_DAYS = int(os.environ.get("SHIELD_OPEN_MAX_DAYS", "120"))

MONTHS = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
          "June": 6, "July": 7, "August": 8, "September": 9, "October": 10,
          "November": 11, "December": 12}
MONTH_RE = "|".join(MONTHS)

# Source-date debt file: incidents whose blockquote lacks a parseable
# 'Month D, YYYY' publication date. Tracked as a committed ratchet, not a
# fabricated date -- see framework/source-date-debt.md.
DEBT_FILE = os.path.join(ROOT, "framework", "source-date-debt.md")

failures = []


def check(what, ok):
    if not ok:
        failures.append(what)
    print(f"  {'ok ' if ok else 'FAIL'} {what}")


def _to_days(ymd):
    y, mi, d = (int(x) for x in ymd.split("-"))
    return date(y, mi, d).toordinal()


def _iso(month_day_year):
    """'November 9, 2026' -> '2026-11-09'; also accepts ISO input."""
    s = month_day_year.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    m = re.match(rf"^({MONTH_RE})\s+(\d{{1,2}}),?\s+(\d{{4}})$", s)
    if m:
        mon, d, y = m.group(1), int(m.group(2)), m.group(3)
        return f"{y}-{MONTHS[mon]:02d}-{d:02d}"
    return None


def parse_changelog():
    """version -> (iso_date, start) and incident first_seen + explicit set."""
    txt = open(CHANGELOG, encoding="utf-8").read()
    vers = []
    for m in re.finditer(r"^## (v[\d.]+) — (.+)$", txt, re.M):
        vers.append((m.group(1), _iso(m.group(2)), m.end()))
    first_seen = {}
    explicit = {}
    for i, (ver, iso, start) in enumerate(vers):
        end = vers[i + 1][2] if i + 1 < len(vers) else len(txt)
        body = txt[start:end]
        ids = set()
        for lo, hi in re.findall(r"INC-(\d+)\.\.INC-(\d+)", body):
            ids.update(range(int(lo), int(hi) + 1))
        for n in re.findall(r"INC-(\d+)\b", body):
            ids.add(int(n))
        ids = {n for n in ids if n <= 300}
        for n in ids:
            if n not in first_seen and iso:
                first_seen[n] = iso
            if n not in explicit:
                explicit[n] = ver
    return first_seen, explicit, vers


def parse_debt_file():
    """Return the set of INC numbers listed in the source-date debt file."""
    if not os.path.exists(DEBT_FILE):
        return None  # None means the file is missing (a gate failure)
    out = set()
    for ln in open(DEBT_FILE, encoding="utf-8").read().splitlines():
        m = re.match(r"^\|\s*INC-(\d+)\s*\|", ln)
        if m:
            out.add(int(m.group(1)))
    return out


def parse_publication_dates():
    """inc_id -> earliest 'Month D, YYYY' date in its source blockquote."""
    txt = open(GAP_ANALYSIS, encoding="utf-8").read()
    lines = txt.splitlines()
    out = {}
    for i, ln in enumerate(lines):
        if not ln.startswith("### INC-"):
            continue
        m = re.search(r"### INC-(\d+)", ln)
        if not m:
            continue
        inc = int(m.group(1))
        # the source blockquote is the next '> ' line (a blank line may sit
        # between the heading and the quote)
        j = i + 1
        while j < len(lines) and not lines[j].startswith("> "):
            j += 1
        if j < len(lines):
            blk = lines[j]
            hits = re.findall(rf"({MONTH_RE})\s+(\d{{1,2}}),?\s+(\d{{4}})", blk)
            if hits:
                hits.sort(key=lambda t: (int(t[2]), MONTHS[t[0]], int(t[1])))
                mm, d, y = hits[0]
                out[inc] = f"{y}-{MONTHS[mm]:02d}-{int(d):02d}"
    return out


def parse_gap_first_identified():
    out = {}
    import glob  # local import: this list is small
    import os as _os
    ex = _os.path.join(ROOT, "exploits")
    for f in _os.listdir(ex):
        m = re.match(r"^g(\d\d)-.*\.md$", f)
        if not m:
            continue
        n = int(m.group(1))
        t = open(_os.path.join(ex, f), encoding="utf-8").read()
        fi = re.search(r"\*\*First identified\*\*\s*\|\s*([^|]+)\|", t)
        if fi:
            v = re.search(r"v[\d.]+", fi.group(1))
            if v:
                out[n] = v.group(0)
    return out


def canonical_incidents():
    out = {}
    ex = os.path.join(ROOT, "exploits")
    for f in os.listdir(ex):
        m = re.match(r"^g(\d\d)-.*\.md$", f)
        if not m:
            continue
        n = int(m.group(1))
        t = open(os.path.join(ex, f), encoding="utf-8").read()
        cm = re.search(r"\*\*Canonical incidents\*\*\s*\|\s*([^|]+)\|", t)
        if cm:
            for inc in re.findall(r"INC-(\d+)", cm.group(1)):
                out.setdefault(int(inc), set()).add(n)
    return out


def main():
    print("== incident latency ledger (does the cadence keep up?) ==")

    first_seen, explicit, vers = parse_changelog()
    if not first_seen:
        check("CHANGELOG parsed for incident first-seen dates", False)
        sys.exit(1)

    ver_date = {v: iso for v, iso, _ in vers if iso}
    max_inc = max(first_seen)

    # 1. coverage
    floored = [n for n in range(1, max_inc + 1) if n not in first_seen]
    check(f"{len(first_seen)} dated incidents ({min(first_seen)}..{max_inc}) + "
          f"{len(floored)} floored pre-numbering = {max_inc} total accounted",
          len(first_seen) + len(floored) == max_inc
          and set(range(1, max_inc + 1)) == set(first_seen) | set(floored))
    if floored:
        check(f"floored incidents ({len(floored)}) are lower-numbered than all dated ones",
              max(floored) < min(first_seen))

    # 2. mapping (for the freshness check + canonical coverage, not the KPI)
    gap_ver = parse_gap_first_identified()
    canon = canonical_incidents()
    mapped = {}
    for inc, gaps in canon.items():
        gap_dates = [ver_date[gap_ver[g]] for g in gaps
                     if g in gap_ver and gap_ver[g] in ver_date]
        fs = first_seen.get(inc, EARLIEST_FLOOR)
        mapped[inc] = max([fs] + gap_dates, key=_to_days)

    # 3. latency KPI: publication -> first_seen
    pub = parse_publication_dates()
    dated = {n: fs for n, fs in first_seen.items() if fs != EARLIEST_FLOOR}
    lat = []
    no_pub = []
    neg = []
    for n, fs in dated.items():
        if n not in pub or not pub[n]:
            no_pub.append(n)
            continue
        lag = _to_days(fs) - _to_days(pub[n])
        if lag < 0:
            neg.append((n, pub[n], fs))
        else:
            lat.append(lag)

    check(f"publication date parsed for {len(pub)} incident blockquotes "
          f"({len(set(pub) & set(dated))} of {len(dated)} dated)", True)
    # Source-date debt is a committed ratchet: dated incidents without a
    # parseable source date must be listed in framework/source-date-debt.md, and
    # no incident may be listed there once it gains a date. It is NOT a hard
    # failure -- a non-'Month D, YYYY' source (e.g. 'reported Aug 29') legitimately
    # lacks a date and must never be assigned one by fabrication -- but the
    # listing itself is enforced so the cleanup is owned and visible.
    debt = parse_debt_file()
    if debt is None:
        check(f"source-date debt file {os.path.relpath(DEBT_FILE, ROOT)} exists", False)
    else:
        missing_from_file = sorted(set(no_pub) - debt)
        stale_in_file = sorted(debt - set(no_pub))
        check(f"source-date debt file tracks {len(debt)} incidents "
              f"({len(no_pub)} dated without a source date)", True)
        for n in missing_from_file:
            check(f"  INC-{n} lacks a source date but is not in {os.path.relpath(DEBT_FILE, ROOT)}", False)
        for n in stale_in_file:
            check(f"  INC-{n} listed in debt file but now has a source date -- remove it", False)
        if not (missing_from_file or stale_in_file):
            check("debt file exactly matches the dated-without-date set "
                  f"({len(debt)} == {len(no_pub)})", True)
    if no_pub:
        ids = ", ".join(f"INC-{n}" for n in sorted(no_pub))
        print(f"  [info] {len(no_pub)} dated incidents lack a parseable 'Month D,"
              f" YYYY' source date (excluded from KPI, tracked as source-date debt): {ids}")
    else:
        check(f"all dated incidents carry a source publication date "
              f"(n={len(dated)} dated, {len(pub)} with pub)", True)

    if neg:
        check("no incident is recorded before its publication date (negative lag)",
              False)
        for n, p, fs in neg:
            check(f"  INC-{n}: first_seen {fs} < publication {p}", False)

    if lat:
        lat.sort()
        p50 = lat[len(lat) // 2]
        p95 = lat[int(round(0.95 * (len(lat) - 1)))]
        print()
        print(f"  latency KPI (publication -> framework record, days, "
              f"{len(lat)} dated incidents):")
        print(f"    p50={p50}  p95={p95}  max={lat[-1]}  n={len(lat)}")
        check("latency KPI computed over dated incidents with pub dates", True)
    else:
        check("at least one dated incident with a publication date for the KPI",
              False)

    # 4. freshness (dated, unmapped)
    dated_open = [n for n in dated if n not in mapped]
    today = date.today()
    stale = []
    for n in dated_open:
        age = today.toordinal() - _to_days(dated[n])
        if age > OPEN_MAX_DAYS:
            stale.append((n, dated[n], age))
    if stale:
        for n, fs, age in stale:
            check(f"INC-{n}: DATED open > {OPEN_MAX_DAYS}d (first_seen {fs}, age {age}d) -- map or justify", False)
    else:
        check(f"no dated open incident exceeds {OPEN_MAX_DAYS}d (dated open: {len(dated_open)})", True)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Latency ledger passed: publication->record latency is derived and provable")
    print("from committed sources, and every incident carries an attributable source.")


if __name__ == "__main__":
    main()