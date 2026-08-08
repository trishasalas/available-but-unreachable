**Task: Refactor `src/frequency.py` to remove trajectory dependencies and token competition code.**

**Context:** The paper's estimand changed from trajectory ordinal to mean accuracy. The trajectory taxonomy has been demoted. Token competition tracing is moving to an archived notebook. This file needs to reflect what the frequency analysis actually does now: correlate corpus frequency with compound-level accuracy using Spearman, with partial-correlation controls.

**What to keep (unchanged):**
- `COMPOUNDS` list (lines 40–99)
- `DOMAIN_COMPOUNDS` list (lines 110–363ish)
- `COMPOUND_DOMAINS` dict (lines ~365–590)
- `query_infinigram()` function
- `build_frequency_table()` function
- `save_frequency_results()` function

**What to remove entirely:**
- `import torch` and `import torch.nn.functional as F` — no model code belongs here
- `load_trajectories()` — trajectory CSV is superseded
- `CONCEPT_TO_COMPOUND` mapping (if it exists, I didn't see it but the load_trajectories function references it)
- `query_competitor_frequency()` — token competition, archive
- The orphaned docstring/code block inside `query_competitor_frequency` (lines 774–836) — that's a `token_competition_trace` function body that got pasted inside another function's return statement
- `compare_tokens_across_scales()` — token competition, archive
- `save_competition_trace()` — token competition, archive

**What to rewrite:**
- `frequency_trajectory_correlation()` → `frequency_accuracy_correlation(freq_df, accuracy_df, suite="pythia")`. Instead of merging with trajectory ordinals and correlating against them, merge with mean accuracy per compound (from the elicitation results) and correlate against that. Keep the same Spearman structure but replace `traj_ordinal` with `mean_accuracy`. Keep partial correlations for constituent frequency and tokenization length.
- `run_frequency_analysis()` → update to call `frequency_accuracy_correlation` instead of `frequency_trajectory_correlation`. Remove the `load_trajectories` call. Accept an `accuracy_df` parameter or a path to the elicitation results.

**What to update in the docstring/usage block at the top:**
- Remove `load_trajectories` from the import example
- Replace `frequency_trajectory_correlation` with `frequency_accuracy_correlation`
- Remove any mention of trajectory classes

**Important:** The `CONCEPT_TO_COMPOUND` mapping referenced in `load_trajectories` — check if it's defined elsewhere in the file (I may have missed it in the truncated view). If it exists only to serve `load_trajectories`, remove it. If it's used by anything that's staying, keep it.

---

That covers everything. The compound lists and Infinigram functions are solid — the rot is in the analysis layer that still thinks the dependent variable is trajectory class.