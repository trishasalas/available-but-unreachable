# Amendment to preregistration 0003: causal-ablation controls

**Date:** 2026-09-04  
**Status:** Frozen before executing or inspecting the new registered ablation outputs.

## Reason for the amendment

Section 12 of preregistration 0003 specifies an empty-set control, 100 random five-head late-layer sets, and a positive-control late-layer set, but it does not fully operationalize those controls or the permutation count for the held-out directional test. This amendment fixes those details before the registered Pythia-2.8B run.

Earlier six-scale ablation outputs have already been observed. They used a different split and control design and are exploratory. They will not be used as confirmatory evidence for the run specified here.

## Frozen implementation

- Model: `EleutherAI/pythia-2.8b`.
- Prompt condition: natural declarative prompts only.
- Compound split: the saved `effective_binding_compound_split.csv`, generated with seed `20260813`; 25 selection compounds and 24 held-out test compounds.
- Selected set: the five late-layer heads with the most negative frequency--normalized-effective-binding Spearman correlations on the 25 selection compounds, as saved by `effective-binding-analysis.ipynb`.
- Intervention: jointly zero each specified head's `hook_z` output at the second compound word's token position.
- Outcome: full-precision KL divergence, $KL(P_{baseline}\|P_{ablated})$, at the final prompt position. Top-token changes are descriptive secondary outcomes.

## Controls

- **Empty set:** no heads are zeroed. The run must produce finite KL no greater than `1e-8` for every held-out compound. Failure stops interpretation of the remaining conditions.
- **Random sets:** sample 100 sets of five distinct heads uniformly from the final third of Pythia-2.8B, excluding the five selected heads. Sets may overlap one another. Sampling uses NumPy seed `20260813`, and the complete sampled sets are saved before their results are summarized.
- **Positive control:** jointly zero all heads in the penultimate layer at the same second-word position. This set is data-independent and is used only to show that the intervention and KL outcome can register a consequential late-layer perturbation. It passes if at least one held-out compound has finite KL greater than `1e-6`. Failure stops causal interpretation and triggers an implementation audit.

## Held-out tests and summaries

The registered directional test is Spearman correlation between log bigram frequency and selected-set KL across the 24 held-out compounds. A one-sided 10,000-permutation test will count permuted correlations less than or equal to the observed correlation and use the one-count correction:

\[
p = \frac{1 + \#(\rho_{permuted} \le \rho_{observed})}{10{,}001}.
\]

Permutation generation uses NumPy seed `20260813`, independently reinitialized from random-set generation.

For the random controls, the same frequency--KL correlation is computed for each set. The selected set is compared descriptively with that distribution and with an empirical one-sided random-set tail probability using a one-count correction. If a random set has constant KL and therefore an undefined correlation, it is retained in the saved output but excluded from the tail comparison; the denominator is one plus the number of finite random-set correlations. Mean and median KL, top-token changes, and the complete compound-level outputs are also saved for the selected, empty, positive-control, and random conditions.

If selected-set KL is constant, its correlation is reported as undefined and the directional permutation $p$-value is set to 1; it is not converted into evidence for an association.
