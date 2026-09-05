# 0017 — Report Spearman for maximum binding versus accuracy

- **Status:** accepted
- **Date:** 2026-09-05

## Context

The manuscript reported Pearson correlations for global maximum attention binding versus ordinal accuracy. Both Pearson and Spearman already exist in `results/analysis/binding_accuracy_corr.csv`. The author approved switching to Spearman after reviewing the different numerical results. This is a reporting decision made after observing both statistics, not a new preregistered analysis.

## Decision

Report Spearman because the question concerns a monotonic relationship with ordered accuracy categories. Recalculation from `results/analysis/binding_vs_accuracy.csv` gives GPT-2 −0.059317 (196 rows), Pythia −0.125931 (294), and OLMo 0.107732 (147). The manuscript reports −0.059, −0.126, and 0.108. Preserve both statistics in the existing result artifact.

Describe weak associations with mixed directions across families, not an absence of all association. Treat these pooled correlations as descriptive because compounds recur across scales. Do not report ordinary independent-row significance tests as confirmatory evidence.

## Consequences

Pythia’s weak negative association must be acknowledged. The result does not support the proposed general positive relationship between maximum binding and accuracy; it does not establish causal irrelevance. The figure generator checks the saved coefficients against its actual plotted data.

**Depends on:** the current compound-scale table, ordered accuracy categories, per-family grouping, and maximum-binding definition. Changes to the data or measure require recalculation and manuscript reconciliation.
