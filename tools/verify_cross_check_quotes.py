#!/usr/bin/env python3
"""Verify that every cross_check evidence quote in crosswalk/shield-ai-to-800-53r5.json
appears in the source document it cites.

The source documents are NOT in the repo (PDFs and web pages). Supply them as plain-text files:

    python3 tools/verify_cross_check_quotes.py --src sp2400=sp2400.txt --src nccoe=nccoe.txt ...

Comparison is letters-only and case-insensitive, so PDF line breaks, soft hyphens, smart quotes and
bracketed citation numbers do not cause false misses. Sources with no file supplied are skipped
(reported), never counted as passes. Exit 1 if any quote is not found in a supplied source.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def letters(s):
    s = re.sub(r"\[\d+(?:,\s*\d+)*\]", "", s)          # drop [121] style citation markers
    return re.sub(r"[^a-z]", "", s.lower().replace("\u00ad", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", action="append", default=[], metavar="KEY=FILE")
    a = ap.parse_args()
    files = dict(x.split("=", 1) for x in a.src)
    cw = json.load(open(os.path.join(ROOT, "crosswalk", "shield-ai-to-800-53r5.json")))
    text = {k: letters(open(os.path.expanduser(f), errors="ignore").read()) for k, f in files.items()}
    ok = miss = skipped = 0
    for cid, e in cw["controls"].items():
        for ev in (e.get("cross_check") or {}).get("evidence", []):
            k = ev["source"]
            if k not in text:
                skipped += 1
                continue
            if letters(ev["quote"]) in text[k]:
                ok += 1
            else:
                miss += 1
                print(f"MISS  {cid} [{k}] {ev['quote'][:100]}")
    print(f"quotes verified: {ok}  missing: {miss}  skipped (no source file given): {skipped}")
    if skipped:
        print("skipped sources:", sorted({ev['source'] for e in cw['controls'].values()
              for ev in (e.get('cross_check') or {}).get('evidence', []) if ev['source'] not in text}))
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
