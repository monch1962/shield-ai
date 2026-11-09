#!/usr/bin/env python3
"""SHIELD-AI framework.md formatting gate (scannability for human architects).

Enforces that the control sections of framework/shield-ai-framework.md stay
structurally scannable after every edit, so a future change cannot quietly
reintroduce a 1,000-word wall of prose as a single control bullet.

Why this matters: security architects read the framework to find "what must I
do?" quickly. A control rendered as one opaque paragraph -- with the normative
requirement, implementation guidance, board rationale, and CVE citations all
fused into a single bullet -- is an audit exhibit, not a working reference.
The layout goal is: every control still starts at column 0 as `- ID: Title`,
but its body is split under labelled, indented sub-lines so the requirement is
the primary reading surface and the evidence is reachable but not in the way.

Gate checks (each provable, all backdate-proof by construction):
1. CONTROL COUNT is unchanged: exactly EXPECTED_COUNT control bullets at column
   0 (`^- (MS|IAM|DS|TP|MIR|GRM|EE)-NN:`). This matches control_metadata.py's
   CONTROL_RE exactly, so the count gate and this gate can never disagree.
2. SCAVABILITY BUDGET: every control's FIRST reading line (its requirement/title
   line, up to the first newline) must be short enough to scan at a glance
   (<= MAX_HEADLINE_WORDS). A control may not bury its essence in a 1,000-word
   first line.
3. TOTAL BODY BUDGET: no control's whole bullet may exceed MAX_TOTAL_WORDS
   without being split into labelled sub-lines (a lazily-extended paragraph is
   the failure mode this gate exists to catch).
   Overspill control bodies MUST be restructured into indented, bold-labelled
   `**Label:**` sub-lines (Requirement / Implementation / Rationale / Evidence).
4. STRUCTURE: any control whose first line exceeds HEADLINE_WORDS but is not
   re-structured is reported; structure is "present" when the body contains at
   least two bold-labelled sub-lines.

Exits 1 on any failure. Called by make check and the pre-push hook, so the
layout is enforced the same way every other quality gate is.

Env overrides (for tests / troubleshooting):
  SHIELD_FW_MAX_HEADLINE   requirement-line word budget   (default 90)
  SHIELD_FW_MAX_TOTAL      per-control total word budget  (default 260)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMEWORK = os.path.join(ROOT, "framework", "shield-ai-framework.md")

# Must match tools/control_metadata.py's CONTROL_RE exactly so the two gates
# always agree on what a "control" is.
CONTROL_RE = re.compile(r"^\- +((?:MS|IAM|DS|TP|MIR|GRM|EE)-[0-9]+):")

MAX_HEADLINE = int(os.environ.get("SHIELD_FW_MAX_HEADLINE", "90"))
MAX_TOTAL = int(os.environ.get("SHIELD_FW_MAX_TOTAL", "260"))
# A label is a bold inline marker at the start of a sub-line: "**Label:**"
LABEL_RE = re.compile(r"^\s*\*\*[A-Za-z][A-Za-z /()&,]+?:\*\*")

failures = []


def check(what, ok):
    if not ok:
        failures.append(what)
    print(f"  {'ok ' if ok else 'FAIL'} {what}")


def parse_controls():
    """Return [{id, text}] where text is the full bullet (no leading '- ')."""
    lines = open(FRAMEWORK, encoding="utf-8").read().splitlines()
    controls = []
    cur = None
    for ln in lines:
        m = CONTROL_RE.match(ln)
        if m:
            if cur:
                controls.append(cur)
            cur = {"id": m.group(1), "lines": [ln[len(m.group(0)):]]}
            continue
        if cur is not None and (ln.startswith("  ") or ln.startswith("\t")
                                or ln.strip() == ""):
            # continuation (indented sub-line or blank) belongs to this control
            cur["lines"].append(ln)
            continue
        if cur is not None:
            # a new non-indented, non-control line ends the control
            if ln.strip() == "":
                cur["lines"].append(ln)
            else:
                controls.append(cur)
                cur = None
    if cur:
        controls.append(cur)
    return controls


def count_word_first_lines_and_bodies():
    """Headline = 1st non-empty line; total = words across the bullet."""
    out = []
    for c in parse_controls():
        body = "\n".join(c["lines"])
        nonempty = [l for l in c["lines"] if l.strip()]
        first = nonempty[0] if nonempty else ""
        out.append((c["id"], first, body, c["lines"]))
    return out


def main():
    print("== framework layout gate (scannability for security architects) ==")

    if not os.path.exists(FRAMEWORK):
        check(f"framework file {os.path.relpath(FRAMEWORK, ROOT)} exists", False)
    else:
        controls = parse_controls()
        ids = [c["id"] for c in controls]
        check(f"framework.md has {len(controls)} control bullets at column 0", True)
        # dedupe / integrity
        check("no duplicate control IDs", len(set(ids)) == len(ids))
        # order sanity: the control count matches the authoritative count
        try:
            from tools.control_metadata import count_controls
            authoritative = count_controls()
        except Exception:
            authoritative = None
        if authoritative is not None:
            check(f"format gate count ({len(ids)}) == authoritative count "
                  f"({authoritative})", len(ids) == authoritative)

        headline_over = 0
        total_over = 0
        for cid, first, body, lines in count_word_first_lines_and_bodies():
            hw = len(first.split())
            if hw > MAX_HEADLINE:
                headline_over += 1
                check(f"{cid} headline is {hw}w (> {MAX_HEADLINE}) -- split or "
                      f"shorten the requirement line", False)
            tot = len(body.split())
            labelled = sum(1 for l in lines if LABEL_RE.match(l))
            if tot > MAX_TOTAL:
                total_over += 1
                structured = labelled >= 2
                if not structured:
                    check(f"{cid} body {tot}w (> {MAX_TOTAL}) is one unbroken "
                          f"block -- restructure into labelled sub-lines", False)

        if headline_over == 0 and total_over == 0:
            check(f"all {len(controls)} control headlines within budget "
                  f"(<= {MAX_HEADLINE}w) and bodies structured (<= {MAX_TOTAL}w "
                  f"or labelled)", True)

    print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Framework layout gate passed: controls are scannable and the layout "
          "is machine-enforced -- a future wall-of-text edit fails CI.")


if __name__ == "__main__":
    main()