#!/usr/bin/env python3
"""Re-point every exploit-catalog link that targets framework/shield-ai-gap-
analysis.md onto the NEW short INC-heading anchor.

Two link styles exist in the catalog:
  A. full-fragment:  [INC-63](...gap-analysis.md#inc-63-openai-agent-...)
  B. nickname:       [INC-33](...gap-analysis.md#ghostjacking)

Both identify the target incident by the INC id in the LINK LABEL. This script
resolves that id against the reformatted headings and rewrites the fragment to
`#<gh_anchor(short title)>`. Only the fragment changes; text and other tokens
are untouched. Idempotent; verifies every rewritten target resolves.
"""
import glob
import io
import re
import unicodedata
import sys

GA = "framework/shield-ai-gap-analysis.md"
txt = io.open(GA, encoding="utf-8").read()
HEADING = re.compile(r"^### (INC-\d+): (.*)$")


def gh_anchor(text):
    text = unicodedata.normalize("NFKD", text.lower())
    kept = [ch for ch in text if ch.isalnum() or ch in " _-"]
    return "".join(kept).replace(" ", "-")


inc_anchor = {}
for ln in txt.split("\n"):
    m = HEADING.match(ln)
    if m:
        # The gate computes anchors from the FULL heading text (prefix + ': ' +
        # title), e.g. "INC-33: GhostJacking" -> "inc-33-ghostjacking". Match that.
        inc_anchor[m.group(1)] = gh_anchor(f"{m.group(1)}: {m.group(2).strip()}")
if not inc_anchor:
    print("no INC headings found"); sys.exit(1)

LINK = re.compile(r"\[([^\]]*(?:INC-\d+)[^\]]*)\]\(\.\./framework/shield-ai-gap-analysis\.md#([A-Za-z0-9\-]+)\)")
changed_files, unresolved = [], []
for f in sorted(glob.glob("exploits/*.md")):
    s = io.open(f, encoding="utf-8").read()
    def repl(m):
        label, anchor = m.group(1), m.group(2)
        idm = re.search(r"INC-(\d+)", label)
        if not idm:
            unresolved.append((f, "no INC id in label", label, anchor))
            return m.group(0)
        incid = "INC-" + idm.group(1)
        if incid not in inc_anchor:
            unresolved.append((f, "unknown INC", incid, anchor))
            return m.group(0)
        new = inc_anchor[incid]
        return f"[{label}](../framework/shield-ai-gap-analysis.md#{new})"
    out = LINK.sub(repl, s)
    if out != s:
        io.open(f, "w", encoding="utf-8").write(out)
        changed_files.append(f)

print("rewrote links in", len(changed_files), "files")
if unresolved:
    print("UNRESOLVED:")
    for u in unresolved:
        print("  ", u)
    sys.exit(1)
for f in changed_files:
    print("  ", f)
print("OK")