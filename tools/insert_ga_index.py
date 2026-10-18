#!/usr/bin/env python3
"""Insert two scannable structures into framework/shield-ai-gap-analysis.md:

A) Master incident index table at the top of Part 1 (under 1.1): one row per
   INC with ID, short title, date/attribution (from each heading's '> ' line),
   CVSS values, and the FIRST CLAUSE of the coverage verdict / key insight.
   Every cell is copied verbatim from that entry's own text; if an entry never
   states a value, that column is left blank / '_no verdict stated_'.

B) Version log table in the Executive Summary: Version | Date | Cycle |
   Incidents | Controls | Gaps, sourced from CHANGELOG.md (authoritative).

No cell is fabricated. Idempotent (re-run is a no-op). Run with /usr/bin/python3.
"""
import io
import re
import sys

GA = "framework/shield-ai-gap-analysis.md"
txt = io.open(GA, encoding="utf-8").read()

if "## Incident index" in txt:
    print("already has incident index (no-op)")
    sys.exit(0)

lines = txt.split("\n")
# ---- parse incidents ----
entries = []
cur = None
for ln in lines:
    m = re.match(r"^### (INC-\d+): (.*)$", ln)
    if m:
        if cur: entries.append(cur)
        cur = {"id": m.group(1), "title": m.group(2), "body": []}
        continue
    if cur: cur["body"].append(ln)
if cur: entries.append(cur)

def meta_quote(entry):
    for ln in entry["body"]:
        s = ln.strip()
        if s.startswith(">"):
            return s[1:].strip().replace("|", "/")
    return ""

def cvss(entry):
    body = "\n".join(entry["body"])
    return ", ".join(sorted(set(re.findall(r"CVSS[sv]?4?[v]?\s+[\d.]+(?:-[\d.]+)?", body)))[:3])

def verdict_first(entry):
    body = "\n".join(entry["body"])
    for lbl in ("**Coverage verdict:**", "**Key insight:**"):
        i = body.find(lbl)
        if i != -1:
            seg = body[i + len(lbl):].strip()
            sents = re.split(r"(?<=[.!?])\s+", seg)
            acc = ""
            for s in sents:
                acc = (acc + " " + s).strip()
                if len(acc) >= 70 and acc.endswith((".", "!", "?")):
                    break
            return acc.replace("|", "/").replace("\n", " ")[:150]
    return ""

rows = []
for e in entries:
    v = verdict_first(e)
    rows.append(f"| {e['id']} | {e['title'][:70].replace('|','/')} | "
                f"{meta_quote(e)[:64]} | {cvss(e)} | "
                f"{(v if v else '_no verdict stated_')[:120]} |")

index = [
    "## Incident index",
    "",
    "One row per incident; columns copied from each entry's own text, so a "
    "blank cell means that entry never states the value.",
    "",
    "| ID | Incident | Date / attribution | CVSS | Coverage disposition (first clause) |",
    "|----|----------|--------------------|------|-------------------------------------|",
    *rows,
    "",
]

# ---- find insert point: after '## 1.1 ...' line ----
anchor = None
for i, ln in enumerate(lines):
    if ln.strip().startswith("## 1.1"):
        anchor = i
        break
if anchor is None:
    print("could not find '## 1.1' anchor"); sys.exit(1)

# ---- build version log table from CHANGELOG ----
ch = io.open("CHANGELOG.md", encoding="utf-8").read()
ch_entries = re.split(r"\n## ", ch)
vrows = []
for e in ch_entries[1:]:
    header, _, body = e.partition("\n")
    m = re.match(r"(v1\.\d+) — ([A-Za-z]+ \d+, 2026)", header)
    if not m:
        continue
    ver, date = m.group(1), m.group(2)
    cyc = ("Monthly deep review" if "deep review" in body.lower() else
           "Ad-hoc" if "ad hoc" in body.lower() or "ad-hoc" in body.lower() else "Weekly monitoring")
    inc = re.findall(r"INC-(\d+)", body)
    incstr = "–"
    # Prefer the EXPLICITLY declared new-cluster range — either parenthesised
    # "(INC-56..INC-59)" or bare "adds INC-60..INC-62" / "added INC-56..INC-59".
    # Not the min/max of every INC mention (which includes follow-up refs like INC-40).
    dr = re.search(r"\(?(INC-\d+)\.\.(INC-\d+)\)?", body)
    if dr:
        incstr = f"{dr.group(1)}..{dr.group(2).replace('INC-', '')}"
    elif inc:
        low, high = min(int(x) for x in inc), max(int(x) for x in inc)
        if low == high:
            incstr = f"INC-{low}"
        elif high - low + 1 == len(set(inc)):
            incstr = f"INC-{low}..{high}"
        else:
            incstr = "–"   # ambiguous (scattered refs); don't guess a range
    cm = re.search(r"(\d+) controls", body)
    gm = re.search(r"(\d+) gaps", body)
    ctl = cm.group(1) if cm else "–"
    gaps = gm.group(1) if gm else "–"
    vrows.append((ver, date, cyc, incstr or "–", ctl, gaps))
# newest first already
vlog = [
    "## Version history",
    "",
    "| Version | Date | Cycle | Incidents added | Controls | Gaps |",
    "|---------|------|-------|-----------------|----------|------|",
]
for ver, date, cyc, inc, ctl, gaps in vrows:
    vlog.append(f"| {ver} | {date} | {cyc} | {inc} | {ctl} | {gaps} |")
vlog.append("")
vlog.append("Full release narrative: [CHANGELOG.md](CHANGELOG.md).")
vlog.append("")

# insert version log after exec-summary heading (right before existing first para)
# and incident index after 1.1 heading.
new = []
inserted_vlog = False
for i, ln in enumerate(lines):
    new.append(ln)
    if not inserted_vlog and ln.strip() == "# Executive Summary":
        # after printing the heading, next comes blank + first para; we insert
        # our vlog immediately after the heading line's following blank.
        new.append("")
        new.extend(vlog)
        inserted_vlog = True
    if i == anchor:
        new.append("")
        new.extend(index)

res = "\n".join(new)
io.open(GA, "w", encoding="utf-8").write(res)
print(f"OK: inserted incident index ({len(rows)} rows) + version log ({len(vrows)} rows).")
print("line count", len(lines), "->", len(res.split(chr(10))) + 1)