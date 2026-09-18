#!/usr/bin/env bash
# Build the manuscript with Pandoc, citeproc, and tagged LuaLaTeX.
set -euo pipefail
cd -- "$(dirname -- "$0")"
case "${1:-}" in
  ""|--debug) ;;
  *) echo "Usage: $0 [--debug]" >&2; exit 1 ;;
esac
for tool in pandoc latexmk lualatex; do
  command -v "$tool" >/dev/null || { echo "Required tool missing: $tool" >&2; exit 1; }
done
mkdir -p build-out
OUTPUT=available-but-unreachable
# Place the generated bibliography before the appendix. The historical
# hand-written references file stays in source but is not duplicated in the PDF.
printf '\n## References\n\n::: {#refs}\n:::\n' > build-out/references.md
SECTIONS=(
  sections/01-introduction.md
  sections/02-related.md
  sections/03-methods.md
  sections/04-the-behavioral-gap.md
  sections/05-binding-is-compensatory.md
  sections/06-frequency-is-the-floor.md
  sections/07-discussion.md
  sections/07a-conclusion.md
  sections/08-limitations.md
  sections/08a-broader-impact.md
  build-out/references.md
  sections/10-appendix.md
)
pandoc "${SECTIONS[@]}" \
  --from=markdown-implicit_figures+tex_math_single_backslash \
  --to=latex-smart --metadata-file=metadata.yaml --template=template.tex \
  --lua-filter=filters/legacy-citations.lua --citeproc \
  --lua-filter=filters/citation-style.lua \
  --lua-filter=filters/layout.lua \
  --lua-filter=filters/caption-style.lua \
  --shift-heading-level-by=-1 --wrap=none \
  -V documentclass=extarticle -V geometry:margin=1in \
  -V 'mainfont=Atkinson Hyperlegible Next' -V fontsize=14pt \
  -V csquotes=true -V linestretch=1.15 -V colorlinks=true \
  -o "build-out/$OUTPUT.tex"
latexmk -lualatex -interaction=nonstopmode -halt-on-error \
  -outdir=build-out "build-out/$OUTPUT.tex" > build-out/build.log 2>&1 || {
    tail -60 build-out/build.log >&2
    exit 1
  }
echo "Done: $(pwd)/build-out/$OUTPUT.pdf"
