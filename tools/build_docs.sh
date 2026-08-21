#!/usr/bin/env bash
# ============================================================================
# SHIELD-AI document build script
# ----------------------------------------------------------------------------
# Regenerates the PDF and EPUB for each source document.
#
# Pipeline:  markdown -> pandoc HTML (styled) -> weasyprint PDF
#            markdown -> pandoc EPUB3 (styled with assets/style.css)
#
# Notes:
#   * The reader MUST be the default markdown reader (with yaml_metadata_block
#     and smart enabled). Using "-f markdown-yaml_metadata_block-smart" breaks
#     frontmatter parsing (the YAML block renders as body text) and disables
#     smart punctuation.
#   * EPUBs must be styled with --epub-stylesheet, otherwise pandoc's minimal
#     default stylesheet strips list indentation and markers.
#   * Bullet/ordered lists in the markdown MUST be preceded by a blank line.
#     Pandoc merges a list that directly follows a paragraph into that
#     paragraph ("Control areas: - MS-01 ... - MS-02 ..."), concatenating the
#     items onto one line in the PDF/EPUB. See tools/fix_list_spacing.py.
# ============================================================================
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

CSS="$REPO/assets/style.css"
DIAGRAMS="$REPO/assets/diagrams"
TMP="$REPO/.build_tmp.html"

build_doc() {
  local md="$1" title="$2"
  local base="${md%.md}"
  echo "== ${md} =="

  # --- PDF: markdown -> standalone styled HTML -> weasyprint ---
  # temp.html lives in the repo root so relative assets/diagrams/... paths
  # resolve when weasyprint loads it.
  pandoc "$md" -f markdown+yaml_metadata_block+smart -t html5 --standalone \
    --resource-path="$REPO:$DIAGRAMS" \
    -c "$CSS" \
    -o "$TMP"
  weasyprint "$TMP" "$base.pdf"

  # --- EPUB: markdown -> EPUB3 with the repo stylesheet ---
  # Note: pandoc >= 3.0 renamed --epub-stylesheet to --css.
  pandoc "$md" -f markdown+yaml_metadata_block+smart -t epub3 \
    --resource-path="$REPO:$DIAGRAMS" \
    --css "$CSS" \
    --metadata title="$title" \
    -o "$base.epub"

  echo "  -> $(basename "$base.pdf")  ($(stat -c%s "$base.pdf") bytes)"
  echo "  -> $(basename "$base.epub") ($(stat -c%s "$base.epub") bytes)"
}

build_doc framework/shield-ai-framework.md \
  "SHIELD-AI(TM): A Sovereign Australian Framework for Secure Agentic AI Deployment"
build_doc framework/shield-ai-gap-analysis.md \
  "SHIELD-AI(TM) Sandbox Escape Gap Analysis"
build_doc assessment-guide/shield-ai-assessment-guide.md \
  "SHIELD-AI(TM) Assessment Guide -- Consultant's Field Manual"
build_doc framework/shield-ai-implementation-architecture.md \
  "SHIELD-AI(TM) Implementation Architecture"
build_doc framework/shield-ai-deep-review-2026-08.md \
  "SHIELD-AI(TM) Monthly Deep Review -- August 2026"
# Any other deep-review editions (glob keeps this working as editions accrue;
# each monthly cycle adds framework/shield-ai-deep-review-YYYY-MM.md)
for review in framework/shield-ai-deep-review-*.md; do
  [ -e "$review" ] || continue
  case "$review" in
    *2026-08*) ;; # already built above
    *) build_doc "$review" "SHIELD-AI(TM) Monthly Deep Review" ;;
  esac
done
build_doc framework/shield-ai-watchlist.md \
  "SHIELD-AI(TM) Watchlist Report"
build_doc framework/shield-ai-tooling-map.md \
  "SHIELD-AI(TM) Tooling and Process Map"
build_doc framework/shield-ai-reference-architecture-walkthrough.md \
  "SHIELD-AI Reference Architecture Walkthrough -- Presenter's Guide"
build_doc presentations/what-is-shield-ai.md \
  "What is SHIELD-AI -- A Plain-English Briefing"
build_doc presentations/glossary.md \
  "SHIELD-AI Glossary -- Plain-Language Definitions"

# --- Exploit catalog: README index + all gNN entries, one combined document ---
# The catalog is a directory of per-type entries; the combined PDF/EPUB is the
# reading copy. Order is stable: README first, then g01..g23 alphabetically.
echo "== exploits/ (combined catalog) =="
CATALOG_DOCS=()
for f in exploits/README.md exploits/g*.md; do
  [ -e "$f" ] && CATALOG_DOCS+=("$f")
done
pandoc "${CATALOG_DOCS[@]}" -f markdown+yaml_metadata_block+smart -t html5 \
  --standalone --resource-path="$REPO:$DIAGRAMS" -c "$CSS" -o "$TMP"
weasyprint "$TMP" exploits/exploit-catalog.pdf
pandoc "${CATALOG_DOCS[@]}" -f markdown+yaml_metadata_block+smart -t epub3 \
  --resource-path="$REPO:$DIAGRAMS" --css "$CSS" \
  --metadata title="SHIELD-AI(TM) Novel AI Exploit Catalog" \
  -o exploits/exploit-catalog.epub
echo "  -> exploit-catalog.pdf  ($(stat -c%s exploits/exploit-catalog.pdf) bytes)"
echo "  -> exploit-catalog.epub ($(stat -c%s exploits/exploit-catalog.epub) bytes)"

# Catalog integrity gate: every G-ID has an entry, every link resolves.
# Stdlib-only checker: any python3 works (PY may be set by update_all.sh).
"${PY:-python3}" tools/check_exploit_catalog.py

rm -f "$TMP"
echo ""
echo "All documents rebuilt."
