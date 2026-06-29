\newpage

## Colophon

This paper is set in Atkinson Hyperlegible Regular, a typeface designed
by the Braille Institute to maximize legibility for readers with low
vision through distinctive letterforms and numerals that reduce
character misrecognition. Choosing it for a paper about accessibility is
not incidental.

The PDF was produced using Pandoc with LuaLaTeX. A custom template.tex
enables `\textbackslash{}`{=tex}DocumentMetadata tagging, producing a
document that conforms to both PDF/UA-2 (universal accessibility) and
PDF/A-4f (archival) standards. This ensures compatibility with screen
readers and other assistive technologies. One known limitation: Pandoc's
PDF tagging pipeline does not distinguish table header cells from data
cells, so all table cells are tagged as `<TD>` rather than the expected
`<TH>` for header rows. This is a tooling constraint, not an oversight.

This paper was written in collaboration with Claude (Anthropic). The
research, methodology, analysis, and conclusions are the author's own.
