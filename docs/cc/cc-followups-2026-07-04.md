# CC follow-ups — post-review closeout (2026-07-04)

> Source: `docs/findings/spearman-review-verdicts-2026-07-03.md` (ratified
> by Trisha 2026-07-04), open items 1–4. Blind window is CLOSED — no
> masking constraints remain. Standard rules: deterministic outputs,
> DECISIONS entry per anything criteria-adjacent, no criteria semantic
> changes.

## 1. Strictness audit, full worksheet
Extend `criteria_strictness_audit.csv` from the 12 prediction-flagged
compounds to ALL 41 authored rows (same two columns: incorrect_marker
count + predicted class where one exists; blank class for unflagged
compounds is fine). Purpose: the paper footnote must say "across the full
worksheet," not "across the predicted subset."

## 2. Scorecard base rates
The 4/7 attractor hit rate needs its chance-firing denominator: across
all 41 expansion compounds, what fraction exhibited the same
failure signature the 7 candidates were predicted to show? Emit a small
CSV (compound, fired y/n, predicted y/n) + the base rate, so the
scorecard reads "4/7 predicted vs X/41 base" and hit rate above chance is
computable. Same definition of "fired" as the scorecard used — state it
in the output header.

## 3. Name the failed ceiling anchors
From `compound_accuracy_table.csv`: identify which 2 of the 4 ceiling
anchors (sign_language, text_formatting, form_field, responsive_design)
failed to ceiling, per suite. One-paragraph plain statement for the
findings folder — these are reported as evidence AGAINST the frequency
thesis per rubric 4.3, same font as the hits.

## 4. S4 PMI robustness read
Compute Spearman using PMI (from the frequency table's unigram columns)
in place of raw bigram count, compound level, both suites, all-rows
split. One CSV + two sentences: does association strength tell the same
story as raw exposure? Divergence is reportable, not a problem.

## Sequencing
Run AFTER Trisha's ratification commit lands (verdicts + D7
pre-registration). Items are independent; any order. Deliverables to
`results/frequency/` (items 2, 4) and `results/analysis/` (item 1), prose
to `docs/findings/`. One labeled commit at the end; DECISIONS entry only
if anything surprising surfaces — these are closeout computations, not
new experiments.

## NOT in scope
- D7 (pre-registered separately, DECISIONS 2026-07-04; Trisha runs it)
- Any rerun of the primary Spearman
- Any criteria edits
