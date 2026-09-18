# Available but Unreachable

Build the manuscript from its existing Markdown sources:

```bash
bash paper/build-paper.sh
```

The script also works from inside `paper/` or by absolute path. Output is
`paper/build-out/available-but-unreachable.pdf`; the intermediate LaTeX and
`build.log` are retained there. `--debug` is accepted for compatibility; both
modes retain diagnostics.

Requires Pandoc 3.9+, a current TeX Live/MacTeX with LuaLaTeX and latexmk
(tested with TeX Live 2026), and the Atkinson Hyperlegible Next font.

The layout is adapted from `how-models-think/accessibility-knowledge-emergence`:
14 pt Atkinson Hyperlegible Next, one-inch margins, and 1.15 line spacing.
The template uses current Pandoc LaTeX partials to retain compatibility with
current tagging and citation support. Tables use 11 pt text; captions use
12 pt italics and stay with their figures.

It enables PDF tagging and requests PDF/UA-2 and PDF/A-4f. Those declarations
and a tagged PDF are not, by themselves, conformance certification.
Pandoc passes the manuscript's image descriptions to native graphics alt text.

`metadata.yaml` holds the title, author, and abstract.
`sections/`, `figures/`, and `references.bib` remain the content sources.
Citeproc generates References before the appendix; `09-references.md` remains
in source but is excluded to avoid a duplicate reference list. The citation
filters support the existing raw `\citealp` commands without editing prose.

The build has no venue-specific style, anonymous submission mode, or
camera-ready mode. Historical research and review records retain their
original names and content.
