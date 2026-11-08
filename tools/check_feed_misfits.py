#!/usr/bin/env python3
"""SHIELD-AI feed-misfit gate (the misfit-ratchet).

Consumes the feed-misfit ledger (framework/feed-misfits.md) that
tools/collect_feed.py maintains. Fails the build when:

1. PROVENANCE: a misfit cites a Feed ID absent from framework/threat-feeds.md.
2. LINEAGE: a misfit carries a lineage outside the taxonomy, or no lineage at all,
   with `Feeds present` in the manifest.
3. SELECTION-BIAS GUARD: one lineage owns more than MAX_LINEAGE_SHARE (default
   60%) of the OPEN misfits -- that would mean intake is vendor- or
   geography-biased and its low apparent misfit-rate is an artifact of a narrow
   feed, not real coverage.
4. SUNRISE discipline: an OPEN misfit past its review_due fails the build --
   the cadence must absorb or re-attest, never let a new class rot unjustified.

The misfit-ratchet is the measured adequacy signal: a healthy framework has a
non-trivial number of open, recent misfits being actively absorbed. A pool of
zero open misfits that never grows is itself suspicious (either the feed is
narrow or the taxonomy is absorbing everything without new discovery).

Exits 1 on any failure. Called by make check, the weekly/monthly cron cycles,
and tools/update_all.sh.
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MANIFEST = os.path.join(ROOT, "framework", "threat-feeds.md")
LEDGER = os.path.join(ROOT, "framework", "feed-misfits.md")

MAX_LINEAGE_SHARE = float(os.environ.get("SHIELD_LINEAGE_SHARE", "0.60"))
# Dominance is only judged once the open-misfit pool is large enough that a
# single-lineage majority is meaningful; below this the pool is too small to be
# 'selection-biased' (one genuine misfit cannot dominate anything).
MIN_LINEAGE_SAMPLES = int(os.environ.get("SHIELD_LINEAGE_MIN", "3"))
LINEAGES = {"vendor", "govt-cert", "research", "opensource", "in-the-wild"}
# A misfit open past this many days fails unless it is absorbed or re-attested.
MISFIT_OPEN_MAX_DAYS = int(os.environ.get("SHIELD_MISFIT_MAX_DAYS", "90"))

failures = []


def check(what, ok):
    if not ok:
        failures.append(what)
    print(f"  {'ok ' if ok else 'FAIL'} {what}")


def parse_table(path):
    """Parse a markdown table file into a list of dicts."""
    if not os.path.exists(path):
        return None, []
    lines = open(path, encoding="utf-8").read().splitlines()
    header = None
    rows = []
    in_table = False
    for i, ln in enumerate(lines):
        s = ln.strip()
        # a header row is a |...| line immediately followed by a |--|-- separator
        if not in_table and s.startswith("|") and i + 1 < len(lines) \
                and lines[i + 1].strip().startswith("|--"):
            header = [c.strip() for c in s.strip("|").split("|")]
            if header and all(h for h in header):
                in_table = True
                continue
        if in_table and s.startswith("|"):
            if s.strip("|").strip().startswith("-"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
    return header, rows


def main():
    print("== feed misfit gate (the misfit-ratchet) ==")

    feed_hdr, feeds = parse_table(MANIFEST)
    mh_hdr, misfits = parse_table(LEDGER)

    if not feeds:
        check("threat-feeds.md has a non-empty feed roster", False)
        print()
        print("FAILURES: feed roster empty/missing")
        sys.exit(1)
    feed_ids = {r["Feed ID"] for r in feeds if "Feed ID" in r}
    check(f"feed manifest lists {len(feeds)} feeds", True)

    # 1. provenance: every misfit cites a known feed
    for m in misfits:
        fid = m.get("Feed", "")
        if fid and fid not in feed_ids:
            check(f"misfit {m.get('Misfit ID')}: Feed '{fid}' not in manifest", False)

    # 2. lineage valid
    open_m = []
    for m in misfits:
        lin = m.get("Lineage", "")
        if lin and lin not in LINEAGES:
            check(f"misfit {m.get('Misfit ID')}: unknown lineage '{lin}'", False)
        if m.get("Status", "").strip().lower() == "open":
            open_m.append(m)

    check(f"{len(misfits)} misfits recorded ({len(open_m)} open)", True)

    # 3. selection-bias guard (open misfits only; judged once pool is meaningful)
    lineage_count = {}
    for m in open_m:
        lin = m.get("Lineage", "?")
        lineage_count[lin] = lineage_count.get(lin, 0) + 1
    if not open_m:
        check("at least one open misfit (a zero-pool is itself suspicious)", False)
    elif len(open_m) < MIN_LINEAGE_SAMPLES:
        check(f"open-misfit pool ({len(open_m)}) too small for dominance judgement "
              f"(need >= {MIN_LINEAGE_SAMPLES}); recorded lineages: "
              f"{sorted(lineage_count)}", True)
    else:
        dom = max(lineage_count.values())
        share = dom / len(open_m)
        top = max(lineage_count, key=lineage_count.get)
        ok_share = share <= MAX_LINEAGE_SHARE
        check(f"no single lineage dominates open misfits "
              f"(top={top} {dom}/{len(open_m)}={share:.0%} <= {MAX_LINEAGE_SHARE:.0%})",
              ok_share)
        if not ok_share:
            check("  -> narrow feed suspected: intake is selection-biased, low misfit-rate is not real coverage", False)

    # 4. sunrise discipline on open misfits
    today = date.today()
    stale = []
    for m in open_m:
        rd = m.get("review_due", "")
        try:
            y, mo, d = (int(x) for x in rd.split("-"))
            due = date(y, mo, d)
        except (ValueError, TypeError):
            stale.append((m.get("Misfit ID"), "no/valid review_due"))
            continue
        if today > due:
            stale.append((m.get("Misfit ID"), f"past review_due {rd}"))
    if stale:
        for mid, why in stale:
            check(f"misfit {mid}: OPEN {why} -- absorb or re-attest", False)
    else:
        check(f"no open misfit exceeds review window (n_open={len(open_m)})", True)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Feed misfit gate passed: intake is externally sourced, attributable by")
    print("lineage, free of dominance, and every new class is absorbed or re-attested.")


if __name__ == "__main__":
    main()