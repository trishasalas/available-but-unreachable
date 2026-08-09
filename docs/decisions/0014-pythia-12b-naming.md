# 0014 — `pythia-13b` vs `pythia-12b` naming

- **Status:** proposed
- **Date:** 2026-08-09
- **Audit finding:** A15

## Context

The binding battery names the largest Pythia checkpoint `pythia-13b`. Elicitation and
entropy call the same checkpoint `pythia-12b`. `src/analysis.py` carries an alias that
maps `pythia-13b` to 12,000,000,000 for sorting purposes, which works and therefore
hides the inconsistency rather than surfacing it.

The upstream and published name is `pythia-12b`. `pythia-13b` appears to be a local
artifact.

## Decision

*(pending)*

Standardize on `pythia-12b`: rename the binding outputs, retire the alias in
`_extract_scale`.

## Consequences

One name for one checkpoint across all batteries. Joins across binding, elicitation,
and entropy stop depending on an alias to succeed. Removing the alias means a future
stray `pythia-13b` file fails loudly (scale 0, sorts first, obvious) instead of being
silently absorbed.

Harder: any committed artifact, figure, or doc referencing `pythia-13b` needs updating,
and the rename touches file names in `results/binding/`.

**Depends on:** doing this *before* the next binding run, which will otherwise
re-entrench whichever name the notebook currently uses.
