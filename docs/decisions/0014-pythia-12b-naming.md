# 0014 — `pythia-13b` vs `pythia-12b` naming

- **Status:** accepted
- **Date:** 2026-08-09
- **Audit finding:** A15

## Context

The binding battery names the largest Pythia checkpoint `pythia-13b`. Elicitation and entropy call the same checkpoint `pythia-12b`. `src/analysis.py` carries an alias that maps `pythia-13b` to 12,000,000,000 for sorting purposes, which works and therefore hides the inconsistency rather than surfacing it.

The upstream and published name is `pythia-12b`. `pythia-13b` appears to be a local artifact.

## Decision

Standardize on `pythia-12b`: rename the binding outputs, retire the alias in `_extract_scale`.

## Consequences

One name for one checkpoint across all batteries. Joins across binding, elicitation, and entropy stop depending on an alias to succeed. Removing the alias means a future stray `pythia-13b` file separates loudly instead of being silently absorbed.

Harder: any committed artifact, figure, or doc referencing `pythia-13b` needs updating, and the rename touches file names in `results/binding/`.

**Depends on:** doing this *before* the next binding run, which will otherwise re-entrench whichever name the notebook currently uses.

---

## Amendment — 2026-08-10

Two factual corrections found during implementation. The decision stands; these correct the reasoning recorded above.

**1. The stated failure mode was wrong.** Consequences claimed a stray `pythia-13b` would get "scale 0, sorts first, obvious." It does not. With the alias removed, `_extract_scale`'s generic parser reads `13b` as 13,000,000,000. Verified:

```
pythia-13b -> 13000000000
pythia-12b -> 12000000000
```

The intended outcome still holds — a stray file separates loudly in every groupby rather than merging into `pythia-12b` — but by a different mechanism, and it sorts *last* among Pythia rather than first. The code comment in `src/analysis.py` describes the real behavior.

**2. The "Depends on" line is not fully satisfiable in code.** It assumed the notebook holds a model list that a rerun would re-entrench. It does not: `notebooks/binding-pythia.ipynb` cell 8 is a hand-typed `model_name = "..."`, and its markdown header already says 12b. `pythia-13b` originated as a typed value in a single Colab session, not from anything persistent on disk.

So there is nothing to fix in the notebook, and the guard is wetware rather than disk. The warning lives in CLAUDE.md instead. The notebook was left alone as a lab record.

**Follow-up this suggests (not part of this decision).** The durable fix for this class is a known-checkpoints set that the battery writers validate model names against. A name that is not a real checkpoint should fail at write time rather than propagate into filenames, a `model` column, and every downstream groupby. Renaming fixes this instance; an assertion fixes the class.

## Implementation — 2026-08-10

- `results/binding/pythia/pythia-13b/` → `pythia-12b/`; 5 CSVs and 1 manifest renamed
- `model` column rewritten in-file, 326,880 rows, byte-level with asserted per-file counts (76320/63360/63360/63360/60480) matching the manifest exactly. `pythia-13b` was verified to appear only in the `model` column and never in prompt text before any edit.
- Alias retired at `src/analysis.py:267`, replaced by a comment stating the dependency
- Verified: total binding rows unchanged at 2,150,144; no `pythia-13b` remains in binding; binding Pythia models match elicitation models; skip list and gpt2 collision report byte-identical to baseline

`OLMo-2-1124-13B` is a genuinely different model and was matched at every step. All `13B` strings in `results/analysis/*.csv` and the notebooks belong to it.
