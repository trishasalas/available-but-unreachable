#!/bin/bash
#
# build-paper.sh — TMLR submission build
#
# Markdown sections -> pandoc -> LaTeX -> latexmk (pdflatex + bibtex) -> PDF,
# formatted by build/tmlr.sty and build/tmlr.bst.
#
# Requires: pandoc, MacTeX (pdflatex, bibtex, latexmk)
#
# Usage:
#   ./build-paper.sh              # anonymous, double-blind (what you submit)
#   ./build-paper.sh --preprint   # named authors, no venue running head
#   ./build-paper.sh --accepted   # camera-ready
#
# Notes on this build, because they are not obvious:
#
#   * tmlr.sty owns the layout — page dimensions, 10pt Latin Modern body, title
#     block, abstract environment, section styles, running head. Do NOT pass
#     -V geometry / fontsize / mainfont / documentclass here; they fight it.
#
#   * Under the default (anonymous) option tmlr.sty DISCARDS the author block
#     and prints "Anonymous authors / Paper under double-blind review". The name
#     and email in metadata.yaml only render under --preprint or --accepted.
#
#   * Sections are authored with `##` as their top heading, so headings shift up
#     one level to become \section. Section numbering is left OFF because the
#     section titles carry their own manual numbers ("## 1. The Behavioral Gap").
#
#   * References come from references.bib via BibTeX, NOT from
#     sections/09-references.md, which is deliberately excluded below. Keeping
#     both in the build would produce two reference lists that drift apart.
#
#   * Only bibliography-key citations used in the manuscript are printed.
#     Same-author/year suffixes are assigned by BibTeX.

set -e
cd -- "$(dirname -- "$0")"

TMLR_OPTION=""
OUTNAME="tmlr-submission"

case "$1" in
  --preprint) TMLR_OPTION="preprint"; OUTNAME="correct-definitions-failed-applications" ;;
  --accepted) TMLR_OPTION="accepted"; OUTNAME="tmlr-camera-ready" ;;
  "")         ;;
  *) echo "Unknown option: $1 (expected --preprint or --accepted)" >&2; exit 1 ;;
esac

OUTDIR="build-out"
TEX="$OUTDIR/$OUTNAME.tex"

mkdir -p "$OUTDIR"
python3 build/prepare-appendix.py

# Let LaTeX and BibTeX find tmlr.sty / tmlr.bst in build/, and references.bib
# in the paper root. The trailing colon means "then search the normal paths".
export TEXINPUTS="./build:"
export BSTINPUTS="./build:"
export BIBINPUTS=".:"

SECTIONS="sections"
SECTION_FILES=(
  "$SECTIONS/01-introduction.md"
  "$SECTIONS/02-related.md"
  "$SECTIONS/03-methods.md"
  "$SECTIONS/04-the-behavioral-gap.md"
  "$SECTIONS/05-binding-is-compensatory.md"
  "$SECTIONS/06-frequency-is-the-floor.md"
  "$SECTIONS/07-discussion.md"
  "$SECTIONS/07a-conclusion.md"
  "$SECTIONS/08-limitations.md"
  "$SECTIONS/08a-broader-impact.md"
  # 09-references.md is intentionally omitted — BibTeX generates the list.
)

PANDOC_FLAGS=(
  # tex_math_single_backslash: the manuscript writes inline math as \( ... \).
  # Pandoc's default markdown reader does NOT enable this, and silently reads
  # \( as an escaped paren — dropping every \rho and doubling nested parens.
  --from markdown-implicit_figures+tex_math_single_backslash
  --metadata-file=build/metadata.yaml
  # No --lua-filter. caption-style.lua emits \figurecaptionfont, a fontspec
  # macro that only exists in the lualatex template. The two ::: {.caption}
  # divs render as plain paragraphs without it, which is fine for now.
  --template=build/template-tmlr.tex
  --shift-heading-level-by=-1
  --wrap=none
  # --natbib (not --citeproc): emits \citep{}/\citet{} and \bibliography{},
  # which is what tmlr.bst needs. @key citations in markdown become natbib
  # citations; plain-prose citations are left untouched.
  --natbib
  --include-after-body="$OUTDIR/appendix.tex"
  -V "tmlr-option=$TMLR_OPTION"
  -V colorlinks=true
)

# --- Step 1: Markdown -> LaTeX ---
echo "Step 1: pandoc -> $TEX"
pandoc "${PANDOC_FLAGS[@]}" "${SECTION_FILES[@]}" -o "$TEX"

# --- Step 2: LaTeX + BibTeX -> PDF ---
echo "Step 2: latexmk (pdflatex + bibtex) -> $OUTDIR/$OUTNAME.pdf"
latexmk -pdf -interaction=nonstopmode -halt-on-error \
        -outdir="$OUTDIR" "$TEX"

echo ""
echo "Done: $OUTDIR/$OUTNAME.pdf"
echo "Intermediate LaTeX: $TEX"
echo "Full log:           $OUTDIR/$OUTNAME.log"
