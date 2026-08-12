#!/usr/bin/env python3
"""Guard: customer decks must never carry a trademark/service-mark notification.

User rule (Aug 2026): "(TM)" was stripped from the Defence and Aware Super
packs; mark notifications are irrelevant to prospects and must not appear in
any future customer presentation. Plain "SHIELD-AI", never "SHIELD-AI(TM)",
and no (R), (SM), or (RTM) either.

Scans:
  1. Builder sources (client-specific/*/build_deck.py) for the mark in any
     string literal.
  2. Client SVG diagram sources (client-specific/*/*-alignment.svg) — these
     embed into decks as rasterised PNGs, so a mark there is invisible to
     PPTX text scans but ships in the deck image.
  3. Built decks (client-specific/*/shield-ai-deck-*.pptx) for the mark in
     visible text, speaker notes, table cells, AND raw slide XML.

Usage:
    python3 tools/check_client_decks_no_trademark.py

Exit code 0 = clean. Exit code 1 = a hit found (printed with location).
Run after every client-deck rebuild, ideally before commit.
"""
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLIENT_DIRS = sorted((REPO / "client-specific").glob("*"))
MARK_RE = re.compile(r"\(\s*(?:TM|R|SM|RTM)\s*\)", re.IGNORECASE)


def scan_builder(path: Path) -> list[str]:
    hits = []
    try:
        src = path.read_text()
    except OSError as exc:
        hits.append(f"cannot read {path}: {exc}")
        return hits
    for i, line in enumerate(src.splitlines(), 1):
        if MARK_RE.search(line):
            hits.append(f"{path}:{i}: {line.strip()[:100]}")
    return hits


def scan_svg(path: Path) -> list[str]:
    hits = []
    try:
        src = path.read_text()
    except OSError as exc:
        hits.append(f"cannot read {path}: {exc}")
        return hits
    for i, line in enumerate(src.splitlines(), 1):
        if MARK_RE.search(line):
            hits.append(f"{path}:{i}: {line.strip()[:100]}")
    return hits


def scan_pptx(path: Path) -> list[str]:
    hits = []
    try:
        import pptx  # noqa: F401  (lazy import keeps the guard runnable anywhere)
        from pptx import Presentation
    except ImportError:
        # Fall back to a raw XML sweep so the guard still works without python-pptx.
        hits = _scan_pptx_xml(path)
        if not hits:
            return []
        hits.insert(0, f"{path}: python-pptx unavailable; raw XML sweep below")
        return hits

    prs = Presentation(str(path))
    for si, slide in enumerate(prs.slides, 1):
        texts = []
        for sh in slide.shapes:
            if sh.has_text_frame:
                texts.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                texts.append(" ".join(c.text for row in sh.table.rows for c in row.cells))
        if slide.has_notes_slide:
            texts.append(slide.notes_slide.notes_text_frame.text)
        for t in texts:
            m = MARK_RE.search(t)
            if m:
                hits.append(f"{path} slide {si}: {m.group(0)!r} in: {t.strip()[:90]}")
    # Belt-and-braces: raw XML catches anything python-pptx doesn't expose.
    hits.extend(f"{path} [xml]: {ctx}" for ctx in _scan_pptx_xml(path))
    return hits


def _scan_pptx_xml(path: Path) -> list[str]:
    hits = []
    try:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if not name.endswith(".xml"):
                    continue
                xml = z.read(name).decode("utf-8", "ignore")
                for m in MARK_RE.finditer(xml):
                    # Collapse whitespace in the snippet for readable output.
                    snippet = " ".join(xml[max(0, m.start() - 40): m.end() + 40].split())
                    hits.append(f"{path} {name}: {m.group(0)!r} in: {snippet}")
    except (OSError, zipfile.BadZipFile) as exc:
        hits.append(f"cannot read {path}: {exc}")
    return hits


def main() -> int:
    total = 0
    for client_dir in CLIENT_DIRS:
        builder = client_dir / "build_deck.py"
        if builder.exists():
            for hit in scan_builder(builder):
                print(hit)
                total += 1
        for svg in sorted(client_dir.glob("*-alignment.svg")):
            for hit in scan_svg(svg):
                print(hit)
                total += 1
        for pptx in sorted(client_dir.glob("shield-ai-deck-*.pptx")):
            for hit in scan_pptx(pptx):
                print(hit)
                total += 1
    print("CLEAN" if total == 0 else f"{total} trademark-mark hit(s) - remove before shipping")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
