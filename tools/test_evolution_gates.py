#!/usr/bin/env python3
"""Versioned tests for the evolution gates.

Replays the antagonism paths of the durability gates so make check proves they
STILL fire after every edit -- a future refactor that silently disables a gate
cannot pass CI. Each test mutates a COPY of the committed artifact, verifies the
target gate exits non-zero (it fired), then restores the original.

Gates under test (each via a fresh subprocess, cwd at repo root):
1. check_feed_misfits.py   -- sunrise (past review_due), provenance (unknown feed)
2. check_evolution_dna.py  -- past review_due on open canary
3. check_evolution_dna.py  -- false coverage (bogus control + gap)
4. latency_ledger.py       -- freshness via SHIELD_OPEN_MAX_DAYS override
5. source-date debt        -- an incident missing from the debt file fires
6. source-date debt        -- a stale (now-dated) entry in the debt file fires

Exits 1 if any gate fails to fire (i.e., a protection was lost). Wired into
`make test-gates`.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def run_gate(gate, args=(), env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(
        [sys.executable, os.path.join("tools", gate)] + list(args),
        capture_output=True, text=True, env=e)
    return p.returncode


def copy_restore(path):
    """Context-manager style helper: yield a temp copy path; caller restores."""
    tmp = path + ".testbak"
    shutil.copy(path, tmp)
    return tmp


def restore(tmp, path):
    shutil.copy(tmp, path)
    os.remove(tmp)


def main():
    failures = []
    fired = 0

    # --- 1. feed-misfit sunrise: past review_due ---------------------------
    can = "framework/feed-misfits.md"
    tmp = copy_restore(can)
    d = open(can).read()
    d = re.sub(r"open \| 20\d\d-\d\d-\d\d \|", "open | 2026-11-01 |", d, count=1)
    open(can, "w").write(d)
    rc = run_gate("check_feed_misfits.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} feed-misfit sunrise fires (rc={rc})")
    if rc == 0:
        failures.append("feed-misfit sunrise did not fire")

    # --- 2. evolution-dna: past review_due ---------------------------------
    can = "framework/evolution-canaries.md"
    tmp = copy_restore(can)
    d = open(can).read()
    d = re.sub(r"\| 2026-12-09 \| open \|", "| 2026-11-01 | open |", d, count=1)
    open(can, "w").write(d)
    rc = run_gate("check_evolution_dna.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} evolution-dna past-review_due fires (rc={rc})")
    if rc == 0:
        failures.append("evolution-dna past-review_due did not fire")

    # --- 3. evolution-dna: false coverage ----------------------------------
    can = "framework/evolution-canaries.md"
    tmp = copy_restore(can)
    d = open(can).read()
    d = d.replace("| 2026-12-09 | open |", "| 2026-12-09 | covered | MS-99 | G99 |", 1)
    open(can, "w").write(d)
    rc = run_gate("check_evolution_dna.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} evolution-dna false-coverage fires (rc={rc})")
    if rc == 0:
        failures.append("evolution-dna false-coverage did not fire")

    # --- 4. latency ledger: freshness via override -------------------------
    rc = run_gate("latency_ledger.py", env={"SHIELD_OPEN_MAX_DAYS": "1"})
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} latency freshness override fires (rc={rc})")
    if rc == 0:
        failures.append("latency freshness override did not fire")

    # --- 5. feed-misfit provenance: unknown feed ---------------------------
    can = "framework/feed-misfits.md"
    tmp = copy_restore(can)
    d = open(can).read()
    d = re.sub(r"\bFEED-\d+\b", "FEED-99", d, count=1)
    open(can, "w").write(d)
    rc = run_gate("check_feed_misfits.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} feed-misfit provenance fires (rc={rc})")
    if rc == 0:
        failures.append("feed-misfit provenance did not fire")

    # --- 5. source-date debt: incident missing from the debt file ----------
    can = "framework/source-date-debt.md"
    tmp = copy_restore(can)
    d = open(can).read()
    d = d.replace("| INC-37 |", "| INC-37Z |", 1)  # evict one dateless incident
    open(can, "w").write(d)
    rc = run_gate("latency_ledger.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} source-date debt missing-entry fires (rc={rc})")
    if rc == 0:
        failures.append("source-date debt missing-entry did not fire")

    # --- 6. source-date debt: stale (now-dated) entry in the debt file -----
    can = "framework/source-date-debt.md"
    tmp = copy_restore(can)
    d = open(can).read()
    # Inject a row for a dated incident that DOES have a parseable date (INC-90);
    # a debt listing for a dated incident is stale and must fail.
    d = d.replace("| INC-89 |",
                  "| INC-90 | 2026-11-06 | placeholder | placeholder |\n| INC-89 |", 1)
    open(can, "w").write(d)
    rc = run_gate("latency_ledger.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} source-date debt stale-entry fires (rc={rc})")
    if rc == 0:
        failures.append("source-date debt stale-entry did not fire")

    # restore any stray backups
    for f in ["framework/feed-misfits.md.testbak",
              "framework/evolution-canaries.md.testbak",
              "framework/source-date-debt.md.testbak"]:
        if os.path.exists(f):
            os.remove(f)

    print(f"\n  {fired}/7 evolution-gate antagonisms fire correctly.")
    if failures:
        print("Evolution gate tests FAILED:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Evolution gate tests passed: every durability protection still fires.")


if __name__ == "__main__":
    main()