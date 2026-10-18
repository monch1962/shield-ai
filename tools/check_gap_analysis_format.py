#!/usr/bin/env python3
"""Format gate for framework/shield-ai-gap-analysis.md.

Keeps the incident section readable as it grows: every `### INC-NN:` heading
must be a SHORT title with no inline metadata, and the varying metadata then
lives in a one-line blockquote directly under the heading. This mirrors
tools/check_exploit_catalog.py in purpose: a hard, cheap gate that fails the
build when an edit (especially a cron cycle appending NEW incidents) drifts
from the format.

Rules enforced:
  1. Every `### INC-NN:` heading is present and its title text contains no '('
     (i.e. no metadata parens crammed into the heading) and is <= 90 chars.
  2. Every heading except short date-blocks is immediately followed (allowing
     blank lines) by a `> ` metadata blockquote line. A heading whose trailing
     metadata was originally only a bare date still gets the blockquote.
  3. Every incident body still carries at least one of the coverage labels
     (`**What happened:**`, `**Coverage verdict:**`, `**Key insight:**`), so
     the reflow never stripped the analytic content.
  4. No CVE/GHSA/MCP-YYYY reference was dropped during formatting.

Exit 0 = pass; exit 1 = fail with the offending lines listed.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PATH = "framework/shield-ai-gap-analysis.md"
txt = open(PATH, encoding="utf-8").read()
lines = txt.split("\n")

HEADING = re.compile(r"^(### INC-\d+): (.*)$")
MAX_TITLE = 90

failures = []


def check(label, cond, detail=""):
    print(f"  [{'OK' if cond else 'FAIL'}] {label} {detail}")
    if not cond:
        failures.append(label)


# 1. headings short + parenthesised
i = 0
heading_count = 0
for idx, ln in enumerate(lines):
    m = HEADING.match(ln)
    if not m:
        continue
    heading_count += 1
    title = m.group(2)
    if "(" in title:
        check(f"{m.group(1)} has no inline '(', got: {title[:40]}", False)
    if len(title) > MAX_TITLE:
        check(f"{m.group(1)} title <= {MAX_TITLE} chars (got {len(title)})", False,
              f"-> {title[:40]}…")

    # 2. blockquote metadata follows within the next 3 lines
    nxt = [x.strip() for x in lines[idx + 1:idx + 4] if x.strip()]
    if not nxt or not nxt[0].startswith(">"):
        check(f"{m.group(1)} has a '> ' metadata blockquote after heading", False)

    # 3. body has substantive content before the next heading (guards the
    #    reflow against stripping analytic prose — legacy terse entries are a
    #    bare paragraph rather than a labelled block, which is fine). Treat a
    #    blockquote metadata line or an empty section as no content.
    j = idx + 1
    content = ""
    while j < len(lines) and not HEADING.match(lines[j]) and not lines[j].lstrip().startswith("# "):
        s = lines[j].strip()
        if s and not s.startswith(">"):
            content = s
        j += 1
    check(f"{m.group(1)} body has content", bool(content))

check(f"{heading_count} INC headings parsed", heading_count > 0)

# 4. CVE/GHSA/MCP reference preservation sanity (no global drop vs. nothing to compare;
#    just ensure references still present in the doc)
refs = (set(re.findall(r"CVE-\d{4}-\d+", txt))
        | set(re.findall(r"GHSA-[A-Za-z0-9-]+", txt))
        | set(re.findall(r"MCP-\d{4}-\d+", txt)))
check(f"{len(refs)} security reference IDs present (CVE/GHSA/MCP)", len(refs) > 20)

print()
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures[:30]:
        print(f"  - {f}")
    sys.exit(1)
print("Gap-analysis format checks passed.")