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
7. check_framework_format.py -- a re-introduced wall-of-text control fires

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


_MTIMES = {}  # tmp path -> original mtime, for mtime-preserving restores


def copy_restore(path):
    """Context-manager style helper: yield a temp copy path; caller restores.

    Records the original mtime so restore() can put the file back byte-for-byte
    AND timestamp-for-timestamp. Without the mtime preservation, restoring a
    *source* doc (framework.md, gap-analysis.md) leaves it freshly-touched, so
    the verify gate sees the source as newer than its derived PDF/EPUB and the
    next `make check` fails spuriously.
    """
    tmp = path + ".testbak"
    shutil.copy(path, tmp)
    _MTIMES[tmp] = os.stat(path).st_mtime
    return tmp


def restore(tmp, path):
    shutil.copy(tmp, path)
    # Restore the original mtime so a restored source doc is not "newer" than
    # its derived artifacts (see copy_restore docstring).
    if tmp in _MTIMES:
        os.utime(path, (_MTIMES[tmp], _MTIMES[tmp]))
        del _MTIMES[tmp]
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

    # --- 5. source-date debt: a dated incident with no source date is not
    #        listed in the debt file -> must fire. With the debt pool cleared
    #        (all 56 dated incidents carry a date), the authentic antagonist is
    #        to strip a real publication date from a source blockquote and NOT
    #        list it: a dateless incident the cadence failed to track.
    ga = "framework/shield-ai-gap-analysis.md"
    tmp = copy_restore(ga)
    d = open(ga).read()
    # Strip the appended ' (published ...)' clause from INC-37's source
    # blockquote (a blank line may sit between the heading and the quote, so
    # operate per-line like the ledger itself does). INC-37 then has no
    # parseable date and is NOT listed in the (now empty) debt file -> fires.
    lines = d.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"^### INC-37:", ln):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("> "):
                j += 1
            if j < len(lines):
                lines[j] = re.sub(r"\s+\(published [^)]+\)$", "", lines[j])
            break
    open(ga, "w").write("\n".join(lines) + "\n")
    rc = run_gate("latency_ledger.py")
    restore(tmp, ga)
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
    d = d.replace("|-----|------------------------|-----------------------------------|--------|",
                  "|-----|------------------------|-----------------------------------|--------|\n"
                  "| INC-90 | 2026-11-06 | placeholder | placeholder |", 1)
    open(can, "w").write(d)
    rc = run_gate("latency_ledger.py")
    restore(tmp, can)
    fired += (rc != 0)
    print(f"  {'ok ' if rc != 0 else 'FAIL'} source-date debt stale-entry fires (rc={rc})")
    if rc == 0:
        failures.append("source-date debt stale-entry did not fire")

    # --- 7. framework layout gate: a re-introduced wall-of-text control -----
    # Mutate a COPY of the framework so one control collapses to a single
    # >90-word headline (unscannable). The layout gate must fire.
    ga = "framework/shield-ai-framework.md"
    tmp = copy_restore(ga)
    d = open(ga).read()
    # Fold MS-02's body into its headline line (removing its structure) to
    # create a deliberately unscannable single-line control.
    closed = re.search(r"- MS-02: .*", d)
    if closed:
        d = d.replace(closed.group(0),
                      "- MS-02: Training data integrity and poison detection across the data "
                      "pipeline, requiring provenance tracking, data sanitisation, adversarial "
                      "robustness testing, and continuous scanning of the biomorphic multi-tenant "
                      "vectorised memory store with sub-pixel attack surface, imperceptible-content "
                      "vectors, hidden pull-request comments, DOM-hidden content, and zero-opacity "
                      "text all sanitised before reasoning, tool-returned content scanned for "
                      "hidden-content primitives, agentic browser renders isolated, uploaded "
                      "documents treated as untrusted seeds, the whole pipeline validated against "
                      "the Rubrik Zero Labs Remote Prompt Execution chain and the AWS Kiro "
                      "CVE-2026-10591 perception-bypass class and the Zenity Labs Intent Collision "
                      "research, with every one of these requirements expressed as a single "
                      "unbroken textual wall so that the layout gate must reject this control "
                      "as unscannable and the build must fail loudly",
                      1)
        open(ga, "w").write(d)
        rc = run_gate("check_framework_format.py")
        restore(tmp, ga)
        fired += (rc != 0)
        print(f"  {'ok ' if rc != 0 else 'FAIL'} framework layout wall-of-text fires (rc={rc})")
        if rc == 0:
            failures.append("framework layout wall-of-text did not fire")
    else:
        print("  SKIP framework layout gate: MS-02 not found in framework.md")

    # restore any stray backups
    for f in ["framework/feed-misfits.md.testbak",
              "framework/evolution-canaries.md.testbak",
              "framework/source-date-debt.md.testbak",
              "framework/shield-ai-framework.md.testbak"]:
        if os.path.exists(f):
            os.remove(f)

    print(f"\n  {fired}/8 evolution+format-gate antagonisms fire correctly.")
    if failures:
        print("Evolution gate tests FAILED:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Evolution gate tests passed: every durability protection still fires.")


if __name__ == "__main__":
    main()