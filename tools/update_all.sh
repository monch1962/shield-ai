#!/usr/bin/env bash
# ============================================================================
# SHIELD-AI full artifact update pipeline
# ----------------------------------------------------------------------------
# Regenerates EVERY derived artifact from its source, then runs the
# consistency gates. Both cron cycles (weekly lean scan and monthly deep
# review) MUST run this so no artifact family is silently left behind.
#
# What it covers:
#   1. Control schema JSON + Rego stubs   (tools/generate_control_schema.py)
#   2. Architecture + threat diagrams     (tools/generate_diagrams.py)
#   3. Implementation diagrams            (tools/generate_impl_diagrams.py)
#   4. Core docs -> PDF + EPUB            (tools/build_docs.sh)
#   5. HTML deck PDFs via decktape        (board, business, bridge, technical)
#   6. Client decks + walkthrough PPTX    (build_deck.py x5)
#   7. NBN deck PDF via LibreOffice container (podman lo-deck)
#   8. Gates: list-spacing, trademark, ai-tell
#   9. Count/version sweep report
#  10. Artifact verification              (tools/verify_artifacts.py)
#
# The script never commits: the calling cycle owns git + email + delivery.
# Run from anywhere: bash tools/update_all.sh
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"
FAILED=()

step() { echo; echo "=================================================================="; echo "== $1"; echo "=================================================================="; }

# --- Python selection -------------------------------------------------------
# Background/cron processes can resolve python3 to the Homebrew build, which
# lacks lxml (required by python-pptx) and lxml-adjacent deps. Prefer a python
# that has everything the pipeline needs; fall back to whatever python3 is.
PY=""
for cand in /usr/bin/python3 python3; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import lxml, pptx, pypdf" >/dev/null 2>&1; then
    PY="$cand"; break
  fi
done
[ -n "$PY" ] || PY="python3"
echo "using python: $PY"

# --- 1. Control schema + Rego stubs (canonical data lives in the generator) ---
step "1/10  Control schema JSON + Rego stubs"
"$PY" tools/generate_control_schema.py --rego || FAILED+=("schema-rego")
"$PY" - <<'EOF' || FAILED+=("schema-count")
import json, os
schema_doc = json.load(open("assets/shield-ai-control-schema.json", encoding="utf-8"))
schema = schema_doc.get("controls", schema_doc)
rego = len([f for f in os.listdir("policies") if f.endswith(".rego")])
print(f"  schema={len(schema)} rego={rego} (expect 60)")
if len(schema) != 60 or rego != 60:
    raise SystemExit(1)
EOF

# --- 2. Architecture + threat diagrams ---
step "2/10  Architecture diagrams"
"$PY" tools/generate_diagrams.py || FAILED+=("diagrams")

# --- 3. Implementation diagrams ---
step "3/10  Implementation diagrams"
"$PY" tools/generate_impl_diagrams.py || FAILED+=("impl-diagrams")

# --- 4. Core docs -> PDF + EPUB (deep-review glob included) ---
step "4/10  Core docs (PDF + EPUB)"
bash tools/build_docs.sh || FAILED+=("build-docs")

# --- 5. HTML deck PDFs (one decktape invocation per deck; loops break decktape) ---
step "5/10  HTML deck PDFs (decktape)"
export PUPPETEER_EXECUTABLE_PATH="$(ls -d ~/.cache/puppeteer/chrome/*/chrome-linux64/chrome 2>/dev/null | head -1)"
if [ -z "$PUPPETEER_EXECUTABLE_PATH" ]; then
  echo "  WARN: puppeteer chrome not found -- deck PDFs NOT rebuilt"
  FAILED+=("decktape-chrome")
else
  for deck in board-brief/shield-ai-deck-board business-deck/shield-ai-deck-business \
              buyers-journey-bridge/shield-ai-deck-bridge technical-deck/shield-ai-deck-technical; do
    echo "  decktape: $deck"
    npx --yes decktape reveal --size 1280x800 "presentations/$deck.html" "presentations/$deck.pdf" \
      >/tmp/decktape-$(basename "$deck").log 2>&1 || { FAILED+=("decktape-$deck"); tail -5 /tmp/decktape-$(basename "$deck").log; }
  done
fi

# --- 6. Client decks + walkthrough PPTX ---
step "6/10  Client decks + walkthrough (python-pptx builders)"
for b in client-specific/defence/build_deck.py client-specific/aware-super/build_deck.py \
         client-specific/nbn/build_deck.py client-specific/retailer/build_deck.py \
         presentations/reference-architecture-walkthrough/build_deck.py; do
  echo "  build: $b"
  "$PY" "$b" || FAILED+=("deck-build-$b")
done

# --- 7. NBN deck PDF via LibreOffice container ---
step "7/10  NBN deck PDF (podman lo-deck)"
if podman image exists localhost/lo-deck 2>/dev/null; then
  if timeout 240 podman run --rm -v "$REPO/client-specific/nbn:/work" localhost/lo-deck \
      soffice --headless --convert-to pdf --outdir /work /work/shield-ai-deck-nbn.pptx \
      >/tmp/nbn-pdf.log 2>&1; then
    echo "  converted shield-ai-deck-nbn.pdf"
  else
    FAILED+=("nbn-pdf")
    tail -5 /tmp/nbn-pdf.log
  fi
else
  echo "  WARN: lo-deck container missing -- NBN PDF NOT rebuilt (recreate: podman build -t localhost/lo-deck <lo-deck Dockerfile>)"
  FAILED+=("nbn-pdf-container")
fi

# --- 8. Gates ---
SKILL_SCRIPTS="$HOME/.hermes/profiles/sec-arch/skills/research/threat-informed-architecture-review/scripts"
step "8/10  Consistency gates"
echo "  -- list-spacing (pandoc list-merge risk)"
"$PY" "$SKILL_SCRIPTS/list_spacing_scan.py" "$REPO" || FAILED+=("list-spacing")
echo "  -- trademark marks in client decks"
"$PY" tools/check_client_decks_no_trademark.py || FAILED+=("trademark")
echo "  -- AI-tell scan on deck builders (report only; prose review is the agent's call)"
if [ -f tools/ai_tell_scan.py ]; then
  "$PY" tools/ai_tell_scan.py client-specific/defence/build_deck.py client-specific/aware-super/build_deck.py \
      client-specific/nbn/build_deck.py client-specific/retailer/build_deck.py \
      presentations/reference-architecture-walkthrough/build_deck.py || true
else
  "$PY" "$SKILL_SCRIPTS/ai_tell_scan.py" client-specific/defence/build_deck.py client-specific/aware-super/build_deck.py \
      client-specific/nbn/build_deck.py client-specific/retailer/build_deck.py \
      presentations/reference-architecture-walkthrough/build_deck.py || true
fi

# --- 9. Count/version sweep report ---
step "9/10  Count/version sweep (review these; version history legitimately contains old versions)"
"$PY" - <<'EOF'
import re, os
bad = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
    for fn in files:
        if not fn.endswith((".md", ".html", ".txt", ".json", ".yml", ".yaml")):
            continue
        p = os.path.join(root, fn)
        for i, ln in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            if re.search(r"(?<![\w/])(36|46|51|55|57|59)\s+controls", ln, re.I) and "v1." not in ln:
                bad.append(f"{p}:{i}: {ln.strip()[:130]}")
            for m in re.finditer(r"SHIELD-AI v1\.[0-9]+", ln):
                if m.group(0) != "SHIELD-AI v1.8":
                    bad.append(f"{p}:{i}: {ln.strip()[:130]}")
for b in bad:
    print("  STALE?", b)
print(f"  {len(bad)} candidate stale references (review, fix if current-state)")
EOF

# --- 10. Artifact verification ---
step "10/10  Artifact verification"
"$PY" tools/verify_artifacts.py || FAILED+=("verify-artifacts")

echo
echo "=================================================================="
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "ALL STEPS PASSED."
  exit 0
else
  echo "STEPS WITH ISSUES (${#FAILED[@]}):"
  for f in "${FAILED[@]}"; do echo "  - $f"; done
  exit 1
fi
