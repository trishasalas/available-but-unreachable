# GPT-2 condition reconciliation

## Scope

Audit of existing saved effective-binding measurements, not a new token-count sensitivity or model run. Original result CSVs, manifests, summaries, manuscript text, and figures are preserved. Reconciled derivative tables are explicitly named audit outputs.

## Recovery and provenance

GPT-2-medium natural first appears in 7ec64dc (August 13); its uniform-labeled duplicate and both GPT-2-large files first appear in 4d4c560 the same day. All four current CSVs are byte-identical to their first committed versions and match the hashes in their corresponding run manifests. This rules out later editing as the source of these discrepancies; it does not establish the precise notebook execution error.

All reachable Git history contains only the two known GPT-2-medium paths, with no recovered distinct uniform run. The checked notebook snapshots retain an unexecuted/default GPT-2-natural configuration rather than an execution log resolving these runs. No absent run is inferred from commit titles.

Every raw file was classified by exact agreement with all 53 natural or uniform inventory prompts. GPT-2-large natural-labeled measurements are assigned to uniform in the audit; uniform-labeled measurements are assigned to natural. GPT-2-medium's uniform-labeled measurements equal its natural table in every column except prompt_condition and are omitted as a duplicate. The remaining 23 files agree with their labels.

## Recomputed effects

The audit recomputes 95th-percentile late-layer measures from raw measurements for the same 49 frozen frequency compounds. Spearman correlations and 2,000-resample bootstrap intervals use the original seed 20260813. It reproduces the original natural aggregate before applying condition reconciliation, using the same shared-label 10,000 permutations and one-count correction. Rank-product computation is checked against individual SciPy Spearman correlations.

- GPT-2-large natural rho changes from -0.3620408163 to -0.3496938776; interval [-0.5962560940, -0.0428362450].
- GPT-2-large uniform rho is -0.3620408163; interval [-0.5864966043, -0.0697372614].
- All thirteen reconciled natural correlations remain negative.
- Natural aggregate mean Fisher z changes from -0.3504419592 to -0.3493544488. Both have two extreme permutations, so p remains 3/10001, reported as 0.0003.
- Twelve verified uniform model results remain, all with negative correlations. The registered thirteen-model uniform aggregate is not recomputed on a reduced set or represented as complete.
- The original natural-prompt head-localization audit also used the mislabeled GPT-2-large file; its model-specific head counts must be reconciled before appendix integration. Pythia's registered intervention artifacts are unaffected.

## Outputs and next action

The script writes the mapping with input hashes, reconciled compound measures, correlations and bootstrap intervals, and original/reconciled natural aggregate comparison. Original records remain authoritative evidence of what was saved; the mapping documents their corrected interpretation.

Only GPT-2-medium uniform is missing from the condition matrix. A targeted rerun should validate actual prompt text against condition before measuring and writing, and preserve a contemporaneous manifest. No new run was performed in this audit.

The proposed manuscript corrections are in docs/reviews/2026-09-05-condition-corrections.md. They remain unapplied pending author approval; if the missing run is recovered or completed, review the uniform-coverage language again first.
