# Post-rerun condition verification

The local repository contains commit 780f639, the GPT-2-medium uniform verified rerun. Its manifest records checkpoint 6dcaa7a952f72f9298047fd5137cd6e4f05f41da and run time 2026-09-05T17:23:12.287553+00:00.

Validation passed: 53 compounds, 20,352 unique compound/layer/head rows, all expected uniform prompts, matching constituent names and last-subtoken indices, finite nonnegative measurements, complete 24-layer/16-head coverage, and matching result/input SHA-256 hashes. The previous duplicate remains preserved under docs/audits/2026-09-05-gpt2-medium-uniform-original/.

The post-rerun script reuses the condition-reconciliation calculation, requires thirteen models in both conditions, and continues to interpret GPT-2-large by actual prompt text rather than its reversed labels. The previous incomplete-coverage audit is preserved. No token-count sensitivity was run.

Results:

- GPT-2-medium uniform rho = -0.4296938776, percentile bootstrap 95% interval [-0.648076, -0.152749].
- Natural: thirteen negative correlations; mean Fisher z = -0.3493544488; 2 extreme permutations; one-sided p = 3/10001 = 0.0002999700.
- Uniform: thirteen negative correlations; mean Fisher z = -0.3647669406; 3 extreme permutations; one-sided p = 4/10001 = 0.0003999600.
- The earlier extra GPT-2-small natural rerun leaves its p95 correlation and the reconciled natural aggregate unchanged at the reported precision.

These are derived audit outputs, not yet replacements for the canonical results/analysis tables or manuscript figures. Remaining integration includes the explicit GPT-2-large condition mapping, refreshing affected head-localization details, and applying author-approved wording. The revised prose proposal is docs/reviews/2026-09-05-condition-corrections.md.
