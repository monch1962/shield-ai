#!/usr/bin/env python3
"""SHIELD-AI external threat-feed harvester + misfit-ratchet.

Pulls externally-sourced threat items (staged by the operator or a cron job as
a newline-delimited TSV/JSON feed, one row per item), classifies each against
the framework's seven pillars, and -- for items that fit NO pillar -- appends
them to the misfit ledger (framework/feed-misfits.md) as the measured signal
that a genuinely new attack class has surfaced.

The tool never fabricates intake and never auto-creates a gap: it ONLY records
misfits and the per-lineage intake counts. Absorbing a misfit into a gap/control
is a human decision recorded in the ledger and enforced by check_feed_misfits.py.

Feed format (tab-separated): feed_id<TAB>lineage<TAB>title
  feed_id / lineage must exist in framework/threat-feeds.md.
  A staged file, framework/feed-staging.tsv, is the default input; the cron or
  operator fills it from the sources in the feed manifest.

Classification keywords per pillar (rough scoring): if an item's title matches
no pillar's keywords, it is a misfit (no-pillar). Matching items are absorbed
intake (a "B" fit), not misfits -- only no-pillar items enter the (c) pool.

Exits 0 always (it is a collector, not a gate); the gate that consumes its
ledger is check_feed_misfits.py. Called by the weekly cron cadence.
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MANIFEST = os.path.join(ROOT, "framework", "threat-feeds.md")
LEDGER = os.path.join(ROOT, "framework", "feed-misfits.md")
STAGING = os.path.join(ROOT, "framework", "feed-staging.tsv")
# Consumed intake is archived so staging reflects PENDING intake only (a re-run
# does not re-classify the same rows forever). Kept append-only for audit.
ARCHIVE = os.path.join(ROOT, "framework", "feed-intake-archive.tsv")

# Pillar keyword classifiers (lowercased substring scoring). An item matches a
# pillar if any keyword appears in its title; a no-pillar item is a misfit.
PILLARS = {
    "MS":  ["model", "sandbox", "prompt", "template", "memory", "stegano"],
    "IAM": ["identity", "credential", "auth", "token", "session", "oauth",
            "mcp server auth", "multiten"],
    "DS":  ["data", "exfil", "database", "vector store", "leak", "memory store"],
    "TP":  ["tool", "mcp", "pipeline", "plugin", "skill", "extension",
            "dependency", "package", "launch path"],
    "MIR": ["monitoring", "telemetry", "audit", "incident", "response", "log"],
    "GRM": ["governance", "risk", "compliance", "policy", "regulat",
            "kill-switch", "assurance"],
    "EE":  ["execution", "harness", "sandbox escape", "chroot", "container",
            "localhost", "loopback", "environment"],
}


def parse_manifest():
    """feed_id -> {lineage, source} from framework/threat-feeds.md roster."""
    out = {}
    if not os.path.exists(MANIFEST):
        return out
    lines = open(MANIFEST, encoding="utf-8").read().splitlines()
    in_table = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("| Feed ID |"):
            in_table = True
            continue
        if in_table and not s:
            in_table = False
            continue
        if in_table and s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) >= 3 and re.match(r"^FEED-\d+$", cells[0]):
                out[cells[0]] = {"lineage": cells[1], "source": cells[2]}
    return out


def classify(title):
    """Return the pillar(s) an item titles as matching, or empty list if none."""
    t = title.lower()
    hits = [p for p, kws in PILLARS.items() if any(k in t for k in kws)]
    return hits


def read_ledger_rows():
    if not os.path.exists(LEDGER):
        return []
    lines = open(LEDGER, encoding="utf-8").read().splitlines()
    rows = []
    in_table = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("| Misfit ID |"):
            in_table = True
            continue
        if in_table and s.startswith("|") and not s.startswith("|-"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and re.match(r"^M-\d+$", cells[0]):
                rows.append(cells)
    return rows


def append_ledger_row(row):
    """Append a misfit row to the ledger's markdown table (after the header)."""
    with open(LEDGER, encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    # insert right after the header separator line (|---|--|...|)
    for i, ln in enumerate(lines):
        if ln.strip().startswith("|--") and "---" in ln and "Misfit ID" not in ln:
            lines.insert(i + 1, "| " + " | ".join(row) + " |")
            break
    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    feeds = parse_manifest()
    if not feeds:
        print("  no feeds in manifest; cannot classify intake")
        return

    if not os.path.exists(STAGING):
        print("  no staged feed items (framework/feed-staging.tsv) — collector idle")
        return

    today = date.today().isoformat()
    seen_titles = {c[3].lower() for c in read_ledger_rows()}
    intake = {"total": 0, "absorbed": 0, "misfit": 0, "per_lineage": {}}
    new_misfits = 0
    next_mid = max([int(c[0].split("-")[1]) for c in read_ledger_rows()] or [0]) + 1
    consumed, retained = [], []

    with open(STAGING, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            feed_id, lineage, title = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if feed_id not in feeds:
                # unknown feed is an operator error -- keep it staged, don't drop
                print(f"  skip: unknown feed_id {feed_id} (not in manifest) -- kept staged")
                retained.append(line)
                continue
            if feeds[feed_id]["lineage"] != lineage:
                print(f"  skip: lineage mismatch for {feed_id} ({feeds[feed_id]['lineage']} vs {lineage}) -- kept staged")
                retained.append(line)
                continue
            intake["total"] += 1
            intake["per_lineage"][lineage] = intake["per_lineage"].get(lineage, 0) + 1

            if classify(title):
                intake["absorbed"] += 1
                consumed.append((today, feed_id, lineage, title, "absorbed"))
                continue
            if title.lower() in seen_titles:
                consumed.append((today, feed_id, lineage, title, "duplicate"))
                continue
            # genuine no-pillar misfit; review_due defaults to 90 days out (one
            # review cadence) so the sunrise gate has a window to act on it.
            from datetime import timedelta
            intake["misfit"] += 1
            mid = f"M-{next_mid:03d}"
            next_mid += 1
            due = (date.fromisoformat(today) + timedelta(days=90)).isoformat()
            append_ledger_row([mid, feed_id, lineage, title, today, "open", due, ""])
            seen_titles.add(title.lower())
            new_misfits += 1
            consumed.append((today, feed_id, lineage, title, f"misfit {mid}"))

    # Drain consumed rows out of staging into the append-only archive, so a
    # re-run (or the next weekly cron tick) does not re-classify the same intake.
    # Only operator-error rows (unknown feed / lineage mismatch) stay staged.
    if consumed:
        with open(ARCHIVE, "a", encoding="utf-8") as af:
            if not os.path.exists(ARCHIVE) or os.path.getsize(ARCHIVE) == 0:
                af.write("# consumed_at\tfeed_id\tlineage\ttitle\toutcome\n")
            for row in consumed:
                af.write("\t".join(row) + "\n")
        with open(STAGING, "w", encoding="utf-8") as sf:
            if retained:
                sf.write("\n".join(retained) + "\n")
    else:
        print("  nothing consumed (staging empty or all rows retained) -- staging unchanged")

    print(f"  intake: {intake['total']} items ({intake['absorbed']} absorbed, {intake['misfit']} no-pillar misfits)")
    for lin, n in sorted(intake["per_lineage"].items()):
        print(f"    lineage {lin}: {n} items")
    print(f"  appended {new_misfits} new misfit(s) to framework/feed-misfits.md")
    print(f"  drained {len(consumed)} consumed row(s) to framework/feed-intake-archive.tsv; "
          f"{len(retained)} operator-error row(s) kept staged")
    print("  collector idle exit 0 (check_feed_misfits.py is the gate that consumes this)")


if __name__ == "__main__":
    main()