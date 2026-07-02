## Ruling Out Binding

Binding correlates with capability — looks like the mechanism. Systematically dismantle it:

- Heads are attention sinks and positional, not accessibility-specific
- MLPs do identical work on compounds the model gets right and wrong.
- *And furthermore*: the single most selective head is causally inert

Board cleared. Binding is a correlate, not a cause.

---

*Data we have:*
- `results/pythia/*-binding.csv` and `results/gpt2/*-binding.csv` — binding scores across all scales
- `results/analysis/binding_accuracy_corr.csv`, `binding_vs_accuracy.csv` — the correlation that makes it look like a mechanism
- `results/pythia/pythia-2.8b-head-characterization.csv` — head types (previous-token, sinks, positional)
- `results/pythia/pythia-2.8b-collocation.csv` — collocation data
- `docs/head-characterization-findings.md` — the full writeup you already have
- `results/lexical-head-results.md` — L29/H7, the nail in the coffin (KL = 1e-05)
- `notebooks/binding-head-characterization.ipynb`, `lexical-head-l29h7.ipynb`

*Figures needed:* binding-accuracy correlation (the thing that looks promising), then the head characterization table showing they're all sinks/positional, then the L29/H7 ablation result.


### SUGGESTION: This section is strong as-is

No new findings to add from today. The red team (Gemini) flagged the redundancy/backup circuit concern for the inert head claim — your blind study results (0.00–0.12 on induction diagnostic, classified as previous-token heads) are a stronger defense than ablation alone because they show the heads are doing a *different job*, not a redundant one. Consider making that distinction explicit: "We do not merely show ablation has no effect; we show the heads are mechanistically characterized as positional, not semantic."

The MLP equivalence claim needs precision (Gemini's attack #2). If you have cosine similarity numbers, state them. If the claim is qualitative, frame it that way and let the frequency hypothesis in Section 05 carry the explanatory weight.