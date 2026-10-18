#!/usr/bin/env python3
"""Format-refine framework/shield-ai-gap-analysis.md incident entries.

Problem: 78 incident headings carry all their metadata (dates, CVEs, CVSS,
researchers, outlets) inline, making headings 100-511 chars and unscannable.

Change (content-preserving — no text deleted, only re-flowed):
1. For each `### INC-NN: <full>` heading that contains a ' — ' or ' (' delimiter,
   split into a SHORT title (heading, no '(') plus a metadata remainder.
2. Put the remainder verbatim on a one-line blockquote directly under the
   heading, so the outline stays scannable and metadata is still visible.
3. Leave incident bodies and all section headings untouched; tidy blank lines.

Idempotent: re-running on an already-formatted file is a no-op. Writes in place
after a content-preservation check. Run with /usr/bin/python3.
"""
import re
import sys
import io

PATH = "framework/shield-ai-gap-analysis.md"
txt = io.open(PATH, encoding="utf-8").read()

HEADING = re.compile(r"^(### INC-\d+: )(.*)$")
ANY_HEADING = re.compile(r"^#{1,6} ")

lines = txt.split("\n")
out = []
i = 0
n = len(lines)
changed = 0
# only reflow metadata-bearing headings
DELIM = re.compile(r" — | \(")
while i < n:
    line = lines[i]
    m = HEADING.match(line)
    if m and DELIM.search(m.group(2)):
        prefix, body = m.group(1), m.group(2)
        sp = DELIM.split(body, maxsplit=1)
        title = sp[0].strip()
        meta = sp[1].strip() if len(sp) > 1 else ""
        bal = meta.count("(") - meta.count(")")
        if bal == -1 and meta.endswith(")"):
            meta = meta[:-1].rstrip()   # drop the parenthetical's matching ')'
        out.append(f"{prefix}{title}")
        out.append("")
        out.append(f"> {meta}")
        out.append("")
        changed += 1
        # skip any original blank line(s) after the heading
        j = i + 1
        while j < n and lines[j].strip() == "":
            j += 1
        # copy body verbatim until the next markdown heading of any level
        k = j
        while k < n and not ANY_HEADING.match(lines[k]):
            out.append(lines[k])
            k += 1
        i = k
        continue
    # normal line (or already-formatted heading): emit as-is, advance one line
    out.append(line)
    i += 1

res = "\n".join(out)
res = re.sub(r"\n{3,}", "\n\n", res)

# ---- content-preservation verification ----
def ids(s):
    return (set(re.findall(r"CVE-\d{4}-\d+", s))
            | set(re.findall(r"GHSA-[A-Za-z0-9-]+", s))
            | set(re.findall(r"MCP-\d{4}-\d+", s)))
missing_ids = sorted(ids(txt) - ids(res))
missing_anchors = [w for w in ["INC-01", "INC-78", "Part 2: Gap Analysis",
                               "## 1.2 Common Attack Patterns", "OpenAI",
                               "Medicare"] if w not in res]
if missing_ids or missing_anchors:
    print("VERIFICATION FAILED — aborting, no write.")
    print("  missing ids :", missing_ids)
    print("  missing anch :", missing_anchors)
    sys.exit(1)

if changed == 0:
    print("no-op: no metadata-bearing INC heading found (already formatted)")
    sys.exit(0)

io.open(PATH, "w", encoding="utf-8").write(res)
print(f"OK: reformatted {changed} INC headings; content preserved.")
print(f"line count {txt.count(chr(10))+1} -> {res.count(chr(10))+1}")
with open("tools/_ga_reformat_preview.txt", "w", encoding="utf-8") as fh:
    # show every heading + its new quote line for diff review
    for ln in res.split("\n"):
        if ln.startswith("### INC-") or ln.startswith("> "):
            if ln.startswith("### INC"):
                fh.write("\n" + ln + "\n")
            else:
                fh.write("    " + ln + "\n")
print("preview written to tools/_ga_reformat_preview.txt")