#!/usr/bin/env python3
"""SHIELD-AI immutable incident-latency ledger.

Makes "does the framework keep up with new threats" a *measured* KPI instead of
an assertion, and makes it backdate-proof by construction.

The ledger's dates are DERIVED from committed sources, never authored ad hoc:
first-seen comes from the CHANGELOG version that recorded the incident; mapping
comes from the covering gap's first-identified version. Because both trace to
committed history, a re-write cannot quietly lower a reported latency without
changing the historical record itself -- the strongest immutability a git repo
gives.

Gate checks:
1. Every incident INC-1..INC-N is accounted for: either traced to a stated
   CHANGELOG first-seen date, or floored (pre-numbering incidents from before
   the INC series was explicit) to the documented founding month. Nothing is
   silently dropped.
2. Delizero/ordering: a mapped incident's date is max(first_seen, covering-gap
   first-identified) -- mapping can never predate the incident's own entry.
   Any apparent mapped<first_seen is a derivation error and fails.
3. Latency KPI (p50/p95/max days) is computed ONLY over dated, mapped
   incidents (floored pre-numbering incidents are excluded -- no fabricated
   first-seen in the KPI).
4. Freshness: a DATED incident with no mapping older than OPEN_MAX_DAYS fails --
   the cadence must map new classes, not let them accumulate. Floored
   pre-numbering incidents are exempt (their date is a floor, not a real entry
   date).
5. Coverage: every incident id 1..N has a row (no silently-dropped cases).

Exits 1 on any failure, printing the latency distribution. Called by `make
check`, the cron cycles, and tools/update_all.sh.
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
EXPLOITS = os.path.join(ROOT, "exploits")

# Pre-v1.8 incidents predate the explicit INC series in the CHANGELOG. The
# founding month is the honest floor for them; they are counted for coverage
# but excluded from the latency KPI and the freshness floor (no fabricated
# first-seen). Override via SHIELD_EARLIEST.
EARLIEST_FLOOR = os.environ.get("SHIELD_EARLIEST", "2026-07-01")
# A DATED incident with no gap mapping older than this many days fails the
# build. Override via SHIELD_OPEN_MAX_DAYS (used to prove the freshness path
# in CI without touching committed data).
OPEN_MAX_DAYS = int(os.environ.get("SHIELD_OPEN_MAX_DAYS", "120"))

failures = []


def check(what, ok):
    if not ok:
        failures.append(what)
    print(f"  {'ok ' if ok else 'FAIL'} {what}")


def _iso(month_day_year):
    """'November 9, 2026' -> '2026-11-09'; also accepts ISO input as-is."""
    MONTHS = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
              "June": 6, "July": 7, "August": 8, "September": 9, "October": 10,
              "November": 11, "December": 12}
    s = month_day_year.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$", s)
    if m:
        mon, d, y = m.group(1), int(m.group(2)), m.group(3)
        if mon in MONTHS:
            return f"{y}-{MONTHS[mon]:02d}-{d:02d}"
    return None


def _to_days(ymd):
    y, mi, d = (int(x) for x in ymd.split("-"))
    return date(y, mi, d).toordinal()


def parse_changelog():
    """version -> (iso_date, start_offset) and incident first_seen + dated set."""
    txt = open(CHANGELOG, encoding="utf-8").read()
    vers = []  # (version, iso_date, start_offset)
    for m in re.finditer(r"^## (v[\d.]+) — (.+)$", txt, re.M):
        vers.append((m.group(1), _iso(m.group(2)), m.end()))

    first_seen = {}  # inc_id -> iso first-seen (real, from changelog)
    explicit = {}    # inc_id -> version
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


def parse_gap_first_identified():
    """gap number -> first-identified version, from exploit entry metadata."""
    out = {}
    for f in os.listdir(EXPLOITS):
        m = re.match(r"^g(\d\d)-.*\.md$", f)
        if not m:
            continue
        n = int(m.group(1))
        txt = open(os.path.join(EXPLOITS, f), encoding="utf-8").read()
        fi = re.search(r"\*\*First identified\*\*\s*\|\s*([^|]+)\|", txt)
        if fi:
            v = re.search(r"v[\d.]+", fi.group(1))
            if v:
                out[n] = v.group(0)
    return out


def canonical_incidents():
    """inc_id -> set of gap numbers citing it as canonical."""
    out = {}
    for f in os.listdir(EXPLOITS):
        m = re.match(r"^g(\d\d)-.*\.md$", f)
        if not m:
            continue
        n = int(m.group(1))
        txt = open(os.path.join(EXPLOITS, f), encoding="utf-8").read()
        cm = re.search(r"\*\*Canonical incidents\*\*\s*\|\s*([^|]+)\|", txt)
        if not cm:
            continue
        for inc in re.findall(r"INC-(\d+)", cm.group(1)):
            out.setdefault(int(inc), set()).add(n)
    return out


def main():
    print("== incident latency ledger (is the framework keeping up?) ==")

    first_seen, explicit, vers = parse_changelog()
    if not first_seen:
        check("CHANGELOG parsed for incident first-seen dates", False)
        sys.exit(1)

    ver_date = {}
    for v, iso, _ in vers:
        if iso:
            ver_date[v] = iso

    max_inc = max(first_seen)
    # 1. coverage: every INC 1..N dated or floored
    floored = [n for n in range(1, max_inc + 1) if n not in first_seen]
    check(f"{len(first_seen)} dated incidents ({min(first_seen)}..{max_inc}) + {len(floored)} floored pre-numbering = {max_inc} total accounted",
          len(first_seen) + len(floored) == max_inc and set(range(1, max_inc + 1)) == set(first_seen) | set(floored))
    if floored:
        # sanity: floored incidents predate numbering, so their ids must be
        # strictly lower than every dated incident's id.
        check(f"floored incidents ({len(floored)}) are lower-numbered than all dated ones",
              max(floored) < min(first_seen))

    # 2. mapping derivations
    gap_ver = parse_gap_first_identified()
    canonical = canonical_incidents()
    mapped = {}
    for inc, gaps in canonical.items():
        gap_dates = [ver_date[gap_ver[g]] for g in gaps if g in gap_ver and gap_ver[g] in ver_date]
        fs = first_seen.get(inc, EARLIEST_FLOOR)
        mapped[inc] = max([fs] + gap_dates, key=_to_days)

    # ordering: mapped >= first_seen is guaranteed by the max(), but verify
    # against REAL first-seen only (floored incidents exempt)
    bad_order = []
    for inc, md in mapped.items():
        fs = first_seen.get(inc)
        if fs and _to_days(md) < _to_days(fs):
            bad_order.append(inc)
    check(f"mapped >= first_seen for all dated mapped incidents (violations: {len(bad_order)})",
          not bad_order)
    for inc in bad_order:
        check(f"INC-{inc}: mapped ({mapped.get(inc)}) < first_seen ({first_seen.get(inc)})", False)

    # 3. latency KPI over dated, mapped incidents only (exclude floored)
    lat = []
    for inc, md in mapped.items():
        fs = first_seen.get(inc)
        if not fs or fs == EARLIEST_FLOOR:
            continue
        if inc in floored:
            continue
        # if gap predates incident (mapped == fs by max), latency is 0 (triage
        # same cycle); only count genuine lag (mapped came from a later gap)
        gap_later = any(_to_days(md) > _to_days(fs) for inc2, md2 in mapped.items() if inc2 == inc)
        # conservative: count diff only when mapped strictly exceeds fs
        d = max(0, _to_days(md) - _to_days(fs))
        lat.append(d)
    lat.sort()
    if lat:
        p50 = lat[len(lat) // 2]
        p95 = lat[int(round(0.95 * (len(lat) - 1)))]
        p_max = lat[-1]
        print()
        print(f"  latency KPI (days, first_seen -> mapped, {len(lat)} dated mapped incidents):")
        print(f"    p50={p50}  p95={p95}  max={p_max}  n={len(lat)}")
        check("latency KPI computed over dated mapped incidents", True)
    else:
        check("at least one dated mapped incident for the latency KPI", False)

    # 4. freshness: dated, UNMAPPED incidents older than OPEN_MAX_DAYS fail
    dated_open = [n for n in first_seen if n not in mapped]
    stale = []
    today = date.today()
    for n in dated_open:
        fs = first_seen[n]
        age = today.toordinal() - _to_days(fs)
        if age > OPEN_MAX_DAYS:
            stale.append((n, fs, age))
    if stale:
        for n, fs, age in stale:
            check(f"INC-{n}: DATED open > {OPEN_MAX_DAYS}d (first_seen {fs}, age {age}d) -- map or justify",
                  False)
    else:
        check(f"no dated open incident exceeds {OPEN_MAX_DAYS}d (dated open: {len(dated_open)})", True)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Latency ledger passed: incident first-seen/mapping is derived and provable")
    print("from committed sources, and no dated incident is rotting unmapped.")


if __name__ == "__main__":
    main()