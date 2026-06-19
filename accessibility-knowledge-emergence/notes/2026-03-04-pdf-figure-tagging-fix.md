# Session Log: PDF Figure Tagging Fix

**Date:** 2026-03-04

## Problem

Figures in the tagged PDF were broken in two ways:

1. **Figures grouped at end of tag tree.** LaTeX's `\begin{figure}[htbp]` float mechanism caused tagpdf to collect all five figures into a `/figures` container at the very end of the document structure (child #12 of Document, after all 11 content sections). A screen reader would encounter all figures only after the entire document.

2. **Tag order reversed.** Switching to the `float` package with `[H]` (exact placement) fixed the positioning — figures appeared inline — but reversed the internal tag order to caption > title > image instead of image > caption.

3. **Duplicate content.** Pandoc's `implicit_figures` extension generated both `alt=` on `\includegraphics` and a `\caption{}` with identical text, since both derive from the `![alt text](path)` markdown syntax.

## Root Cause

LaTeX's float mechanism (both `htbp` and `float` package `[H]`) is incompatible with correct PDF structure tagging via tagpdf. The float system either defers figures to end-of-document or reverses content order during box capture.

## Fix

Two changes:

### 1. `build-paper.sh` — added `--from markdown-implicit_figures`

Disables Pandoc's automatic `\begin{figure}` + `\caption{}` wrapping. Images now produce only `\includegraphics[alt={...}]{path}` — no float environment, no caption. Pandoc 3.9 generates the `alt=` attribute automatically from the markdown `![alt text](path)` syntax.

### 2. `paper/template.tex` — removed `\usepackage{float}`

Reverted to stock `\def\fps@figure{htbp}` (which is now inert since no figure environments are generated).

## Result

- Figures appear inline in the tag tree at their logical reading-order position
- Each image is tagged as `/Figure` with full alt text from the markdown
- Tag structure: `/Part` > `/Sect` > `/P` > `/Figure[alt text]` — valid PDF/UA-2
- Visible captions are now written as regular markdown text below each image, allowing alt text and captions to differ
- PAC validation passes

## What We Tried (and Why It Didn't Work)

| Approach | Outcome |
|---|---|
| `\def\fps@figure{htbp}` (original) | Figures grouped at end of tag tree |
| `\usepackage{float}` + `\def\fps@figure{H}` | Correct position, reversed tag order (caption > title > image) |
| Custom non-floating `figure` environment via `\@captype` | Still had ordering issues |
| **`-implicit_figures` + no float** | Correct position, correct order, clean tags |
