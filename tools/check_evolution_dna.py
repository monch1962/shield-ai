#!/usr/bin/env python3
"""SHIELD-AI evolution DNA gate.

The game-proof, executable definition of "the framework can still evolve":
new threat classes must be absorbed into real, enforced controls or actively
re-attested — never left to rot unmeasured, and never given fake coverage.

Reads framework/evolution-canaries.md (the canary table, single source of
truth) and verifies, for every row:

1. Every canary has a non-empty external source (anti-fabrication).
2. first_seen and review_due are well-formed dates and review_due >= first_seen.
3. Sunrise discipline: if today is past review_due and the canary is still
   `open`, the build fails -- the taxonomy must re-attest or absorb on an
   event-driven cadence, not on calendar-and-memory.
4. Coverage must be earned: a `covered` canary must name a covering control
   whose policy file exists and is NOT a stub (real deny-override logic), and a
   gap (G-k) with an entry in exploits/.
5. No manufactured discovery: coverage is satisfied only by a real implemented
   policy, so the gate cannot be gamed to clear a discovery-rate target.

Exits 1 on any failure, printing the findings. Called by `make check`, the
weekly/monthly cron cycles, and tools/update_all.sh.
"""
import os
import re
import sys
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CANARIES = os.path.join(ROOT, "framework", "evolution-canaries.md")
POLICIES = os.path.join(ROOT, "policies")
EXPLOITS = os.path.join(ROOT, "exploits")
STUB_MARKER = "# TODO: Implement control test logic"

failures = []


def check(what, ok):
    if not ok:
        failures.append(what)
    print(f"  {'ok ' if ok else 'FAIL'} {what}")


def policy_implemented(control):
    pillar, _, num = control.partition("-")
    p = os.path.join(POLICIES, f"shield_ai_{pillar.lower()}_{pillar.lower()}-{num}.rego")
    if not os.path.exists(p):
        return False
    with open(p, encoding="utf-8") as f:
        return STUB_MARKER not in f.read()


def gap_exists(gap):
    m = re.match(r"^G(\d+)$", gap.strip())
    if not m:
        return False
    num = int(m.group(1))
    prefix = f"g{num:02d}-"
    return any(f.startswith(prefix) and f.endswith(".md")
               for f in os.listdir(EXPLOITS))


def parse_rows():
    with open(CANARIES, encoding="utf-8") as f:
        lines = [ln.rstrip() for ln in f]

    # locate the delimiter row and header
    header_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| Canary ID |"):
            header_idx = i
            break
    if header_idx is None:
        check("evolution-canaries.md has a canary table header", False)
        return []

    header = [c.strip() for c in lines[header_idx].strip("|").split("|")]
    rows = []
    for ln in lines[header_idx + 2:]:  # skip header + separator
        if not ln.strip().startswith("|") or not ln.strip().endswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) != len(header):
            check(f"canary row has {len(cells)} cells, expected {len(header)}",
                  False)
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def main():
    print("== evolution DNA gate (can the framework still evolve?) ==")

    if not os.path.exists(CANARIES):
        check(f"canary manifest missing: {os.path.relpath(CANARIES)}", False)
        print()
        print("FAILURES: canary manifest missing")
        sys.exit(1)

    rows = parse_rows()
    check(f"canary manifest parsed {len(rows)} canaries from {os.path.basename(CANARIES)}",
          True)

    today = date.today()

    for r in rows:
        cid = r.get("Canary ID", "?")
        src = r.get("External source", "")
        status = r.get("Status", "").strip().lower()
        fs = r.get("first_seen", r.get("first_seen_date", "")).strip()
        rd = r.get("review_due", r.get("review_due_date", "")).strip()
        ctrl = r.get("Covering control", "").strip()
        gap = r.get("Gap", "").strip()

        # 1. anti-fabrication
        if not src or src in ("—", "-", ""):
            check(f"{cid}: non-empty external source", False)
        else:
            check(f"{cid}: external source present", True)

        # 2. dates well-formed and ordered
        date_ok = True
        try:
            fs_date = datetime.strptime(fs, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            fs_date = None
            date_ok = False
        try:
            rd_date = datetime.strptime(rd, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            rd_date = None
            date_ok = False
        check(f"{cid}: first_seen={fs or 'MISSING'} review_due={rd or 'MISSING'} valid and ordered",
              date_ok and fs_date and rd_date and rd_date >= fs_date)

        # 3. sunrise discipline
        if date_ok and fs_date and rd_date:
            if status == "open" and today > rd_date:
                check(f"{cid}: OPEN but past review_due {rd} -- re-attest or absorb",
                      False)
            else:
                check(f"{cid}: within review window (status={status or 'open'})", True)

        # 4. coverage must be earned
        # Treat '—', '-', 'N/A' placeholders as absent.
        absent = {"", "—", "-", "n/a", "N/A", "(none)", "— (none)"}
        ctrl = "" if ctrl in absent else ctrl
        gap = "" if gap in absent else gap

        if status == "covered":
            earned = bool(re.match(r"^(MS|IAM|DS|TP|MIR|GRM|EE)-\d{1,2}$", ctrl)) \
                     and policy_implemented(ctrl)
            check(f"{cid}: covered -> control {ctrl or '(none)'} implemented non-stub",
                  earned)
            check(f"{cid}: covered -> gap {gap or '(none)'} has an entry",
                  bool(gap and gap_exists(gap)))
        else:
            # An OPEN canary must not name a covering control/gap (that would be
            # claiming coverage it hasn't earned). This is the 'no manufactured
            # discovery' guard in negative form.
            check(f"{cid}: open canary (no false coverage)", not ctrl and not gap)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Evolution DNA gate passed: every new class is either absorbed into an")
    print("implemented control or explicitly re-attested within its review window.")


if __name__ == "__main__":
    main()