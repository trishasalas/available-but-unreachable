# Task brief — land decision 0015 (concept key normalization)

> Paste into Claude Code. Written 2026-08-10.  
> Decision: `docs/decisions/0015-concept-key-normalization.md` — **already ruled and**  
> **accepted.** This brief implements it. Do not re-open the design.  
> Prior work: `docs/task-analysis-py-fix.md` and its session log; commit `aa7e1bb`.

---

## Read first

- `docs/decisions/0015-concept-key-normalization.md` — the ruling
- `src/analysis.py` — `_canonical_concept` already exists here, currently used only for the `source` membership test. The module docstring records this deferral explicitly.
- `src/gap_analysis.py` — the consumer that must change
- `src/accuracy_coding.py` — **read, do not edit.** Understand how `code_response`dispatches before touching anything upstream of it.

## The ruling being implemented

Normalize at load time, with the coding layer insulated:

- `src/analysis.py` sets `concept_raw` to the on-disk spelling, then normalizes `concept` in place using the existing `_canonical_concept`.
- `src/gap_analysis.py` passes **`concept_raw`** to `code_response`, not `concept`.
- Canonical form is lowercase with underscores (`closed_captions`), matching the frequency battery and file naming.

## Why it cannot be a plain in-place normalization

`src/accuracy_coding.py`'s `code_declarative` dispatches on a 52-key rules dict in **space form, case-sensitively** (`'WCAG'`, `'semantic HTML'`). A miss falls through `rules.get(concept, {})` and returns `'incorrect'` rather than raising.

**Zero of those 52 keys survive canonicalization.** Normalizing `concept` without routing `concept_raw` to the coding layer would silently code every declarative row incorrect — declarative mean 0.0, not 0.5, with no error anywhere.

`src/accuracy_coding.py` is effectively a public API. Any change to it requires its own DECISIONS entry, because it retroactively changes every table and figure in the paper.

## Pass conditions

Run and report. **Do not adjust code to make a number match — report the mismatch.**

1. **pythia-160M declarative == 0.5.** Unchanged from `aa7e1bb`. If normalization has leaked into the coding path this collapses toward 0.0 and is immediately visible.
2. **Declarative pivot n=10**, exactly the ten Experiment 1 originals including `closed captions`. **Evaluative pivot n=5**, unchanged.
3. **Full 6×3 gap table byte-identical** to the current output. This change is a no-op on every existing number; it only makes joins possible that previously failed. Compare against `_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv` for population, and against the current on-disk tables for values.
4. **Report the normalization's effect on the concept vocabulary** — how many distinct `concept` values before and after, and which collapsed into which. The three-way `closed_captions` / `closed captions` / `captions` collapse should be visible.
5. **`source` derivation unchanged.** Row counts should stay at elicitation 2925/533, entropy 2751/533, binding 1723904/426240.

## Constraints

- **Do not edit **`src/accuracy_coding.py`**.** Note that its line ~295 comment documents a condition that has since reversed — it claims declarative data uses `captions` and that `closed captions` appears "only as control", while the data has 6 declarative `closed captions` rows and zero `captions`. Report it; do not fix it. That is its own decision.
- **Do not touch anything under **`results/`**.** This is a loader and consumer change; no regeneration.
- **Do not re-open the design.** 0015 is accepted. If implementation reveals the ruling is wrong, stop and report rather than choosing differently.
- Work inline. No subagents, no worktrees under `.claude/`.
- Show the diff before committing.

## After it lands — do not do this in the same changeset

The completion/declarative join (audit A3) becomes possible once keys normalize. That is separate work with its own verification: currently the join resolves on `alt text `alone and reports 7 greater / 6 ties / 0 less, p = 0.0078 — significant *through a broken join*. What it does with all four concepts is an open empirical question, not a bug fix, and it should not be bundled with a change whose pass condition is "nothing moved."

## Report

1. The diff.
2. The five pass-condition results.
3. The concept vocabulary before/after.
4. Anything found while reading that is not in this brief. The last three briefs each
  surfaced a real defect that way, and it was more valuable than the assigned work.
