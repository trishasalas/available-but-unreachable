# 0012 — OLMo x-corpus for the frequency battery

- **Status:** superseded by [0016](0016-olmo-checkpoint-pinning.md)
- **Date:** 2026-08-09
- **Superseded:** 2026-08-11
- **Audit finding:** A4

> **Superseded 2026-08-11.** This decision describes the wrong problem. A4 is not a
> corpus finding — `SUITE_INDEX` always mapped OLMo to `v4_olmo-mix-1124_llama`
> correctly, and the corpus columns in both contradictory result sets are
> byte-identical. The divergence was entirely in `mean_accuracy`, and the real defect
> was `rowlevel_bootstrap` building its x-vector via `drop_duplicates('compound')`
> across all suites. The remaining reproducibility gap was checkpoint pinning, which
> [0016](0016-olmo-checkpoint-pinning.md) resolves. The body below is left unedited as
> a record of the reasoning at the time.

## Context

The OLMo robustness battery mixes corpora. Partial correlation, Kendall, and bootstrap use Pile x-values while the primary uses Dolma. Four contradictory OLMo-1B rho values currently exist on disk as a result.

The tension is real in both directions. Dolma is OLMo's actual training corpus, so correlating OLMo accuracy against Dolma frequencies is the methodologically correct move — but it produces a number that is not comparable to the Pile-based pythia and gpt2 figures. Correlating against the Pile keeps the cross-family comparison clean while using the wrong corpus for that family.

This is upstream of the frequency regeneration. Whatever is not decided here gets entrenched by the next run.

## Decision

*(pending)*

**A.** OLMo correlates against Dolma throughout. Cross-family comparison is qualified  
in prose.

**B.** OLMo correlates against the Pile throughout, for comparability. The corpus  
mismatch is disclosed as a limitation.

**C.** Report both, with one clearly designated as primary.

C is defensible and is what the current data half-accidentally already contains — the  
problem is not that both exist, it is that neither is labelled.

## Consequences

Whichever is chosen, the corpus **must** be recorded as a column on the output file. `results/frequency/frequency_table.csv` currently has no corpus or index column (`compound, domain, word1, word2, bigram_count, word1_count, word2_count, conditional_prob`), so provenance is unrecoverable from the artifact itself. This is also what makes A1's clobbering damaging rather than merely annoying — with a corpus column, an overwritten file would be detectably wrong instead of silently plausible.

**Depends on:** the frequency pipeline writing per-suite filenames (audit A1) so that Dolma and Pile results can coexist rather than overwrite each other. Note that `{suite}_frequency_accuracy.csv` files are already per-suite; it is specifically`frequency_table.csv` and `spearman_summary.csv` that use fixed names.
