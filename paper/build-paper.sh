#!/bin/bash

# build-sections.sh
# Run from sections-1/ directory
# Requires: pandoc, lualatex (MacTeX)
#   brew install pandoc
#   brew install --cask mactex
#
# Produces a tagged PDF/UA-2 + PDF/A-4f document via the template in
# sections/template.tex, which enables \DocumentMetadata tagging. This
# requires a TeX Live 2022+ / MacTeX 2022+ installation.
#
# Accessibility checklist before building:
#   - All figures referenced with descriptive alt text: ![Describe what a
#     sighted reader sees](../figures/filename.png)
#   - sections/metadata.yaml has: title, author, date, abstract, lang
#   - sections/10-colophon.md is written
#
# Usage:
#   ./build-sections.sh           # normal build
#   ./build-sections.sh --debug   # two-step build, keeps intermediate .tex,
#                               # verbose pandoc output, full lualatex log

set -e

OUTPUT="tmlr-untitled.pdf"
SECTIONS="sections"
DEBUG_DIR="build-debug"
INTERMEDIATE="$DEBUG_DIR/paper-intermediate.tex"
DEBUG=false

if [[ "$1" == "--debug" ]]; then
  DEBUG=true
  mkdir -p "$DEBUG_DIR"
  echo "=== DEBUG MODE ==="
  echo "Debug output → $DEBUG_DIR/"
  echo ""
fi

PANDOC_FLAGS=(
  # tex_math_single_backslash: the manuscript writes inline math as \( ... \).
  # Pandoc's default markdown reader does NOT enable this, and silently reads
  # \( as an escaped paren — dropping every \rho and doubling nested parens.
  --from markdown-implicit_figures+tex_math_single_backslash
  --metadata-file=build/metadata.yaml
  --lua-filter=build/filters/caption-style.lua
  --template=build/template.tex
  --wrap=none
  --citeproc
  -V documentclass=extarticle
  -V geometry:margin=1in
  -V "mainfont=Atkinson Hyperlegible Next"
  -V fontsize=14pt
  -V linestretch=1.15
  -V colorlinks=true
)

SECTION_FILES=(
  "$SECTIONS/01-introduction.md"
  "$SECTIONS/02-related.md"
  "$SECTIONS/03-methods.md"
  "$SECTIONS/04-the-behavioral-gap.md"
  "$SECTIONS/05-binding-is-compensatory.md"
  "$SECTIONS/06-frequency-is-the-floor.md"
  "$SECTIONS/07-discussion.md"
  "$SECTIONS/08-limitations.md"
  "$SECTIONS/09-references.md"
  "$SECTIONS/10-colophon.md"
)

if $DEBUG; then
  # --- Step 1: Markdown → LaTeX ---
  echo "Step 1: pandoc → .tex"
  echo ""
  pandoc \
    "${PANDOC_FLAGS[@]}" \
    "${SECTION_FILES[@]}" \
    -o "$INTERMEDIATE" \
    --verbose 2>&1 | tail -20

  echo ""
  echo "Pandoc succeeded → $INTERMEDIATE"
  echo ""

  # --- Step 2: LaTeX → PDF ---
  echo "Step 2: lualatex → .pdf"
  echo ""
  lualatex -interaction=nonstopmode -halt-on-error -output-directory="$DEBUG_DIR" "$INTERMEDIATE"

  echo ""
  echo "Done: $DEBUG_DIR/paper-intermediate.pdf"
  echo ""
  echo "Debug files in $DEBUG_DIR/:"
  echo "  paper-intermediate.tex  ← check LaTeX line numbers here"
  echo "  paper-intermediate.log  ← full lualatex log"
  echo ""
  echo "Tip: When lualatex reports an error on line N, run:"
  echo "  sed -n 'Np' $INTERMEDIATE"

else
  # --- Single-step build (normal) ---
  pandoc \
    "${PANDOC_FLAGS[@]}" \
    "${SECTION_FILES[@]}" \
    -o "$OUTPUT" \
    --pdf-engine=lualatex

  echo "Done: $OUTPUT"
fi