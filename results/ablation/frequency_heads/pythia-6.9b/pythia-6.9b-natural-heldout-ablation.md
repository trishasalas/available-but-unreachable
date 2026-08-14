# Held-out frequency-head ablation manifest

**Record status: POST-RUN RECONSTRUCTION**

This manifest was created after the ablation completed because the original notebook wrote only the CSV.
File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.
Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.

- Manifest creation time (UTC): 2026-08-14T14:33:29.374712+00:00
- Repository commit at manifest creation: `1234c9a18c52e0977fcbba9a69804f4699b6bc43`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-6.9b`
- Prompt condition: `natural`
- Random seed: `42`
- Split: Sorted compound names, shuffled once; first half selection, second half held out
- Held-out compounds: 25
- Selected heads: `[(25, 12), (22, 14), (22, 2), (22, 13), (30, 14)]`
- Layer-matched random control heads: `[(25, 11), (22, 3), (22, 17), (22, 26), (30, 5)]`
- Intervention: zero each listed head's `hook_z` output at the later constituent position
- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded

## Model/runtime

- Live model object: not available during reconstruction
- Runtime device and dtype: not contemporaneously recorded by the ablation notebook

## Recovered artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Ablation CSV | `results/ablation/frequency_heads/pythia-6.9b/pythia-6.9b-natural-heldout-ablation.csv` | `3dc96c68d96a237b3c342df84795b86152443f028628cb5600e28d87729c00f2` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_natural.csv` | `e3963a6c9ebdfd9ca61372c460b5015c48d3736179f8a55cd795735089c0abcf` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `f7814969765c770566f5935bad78ca895ef628af3e0c59ee91fdd594f9b7e3c0` |
| Intervention implementation | `src/qk_ov.py` | `945fdebe4f0f649e5922d8b95f1cb1a1431e2903f7aad3f81c0eb5de73b24a26` |
| Corresponding model manifest | `results/effective_binding/pythia/pythia-6.9b/natural/pythia-6.9b-natural-effective-binding.md` | `256cafa99c8e4bbc48f6f99e6a8ca56bce5ac58601ee70ee8a943d80ba3b8ad3` |

## Saved-result audit

- Rows: 25
- Selected KL mean / median: 6.72e-06 / 6e-06
- Selected KL range: [1e-06, 2.9e-05]
- Control KL mean / median: 6e-06 / 4e-06
- Control KL range: [1e-06, 2.6e-05]
- Selected-minus-control mean / median: 7.2e-07 / 0
- Selected > control / equal / selected < control: 12 / 5 / 8
- Selected top-token changes: 0 / 25
- Control top-token changes: 0 / 25

## Output schema

`compound`, `model`, `condition`, `selected_heads`, `control_heads`, `selected_kl`, `control_kl`, `selected_minus_control_kl`, `selected_top_changed`, `control_top_changed`, `bigram_count`, `log_frequency`

## Manifest-generation environment

- Python: `3.12.13`
- Platform: `Linux-6.6.122+-x86_64-with-glibc2.35`
- torch: `2.11.0+cu128`
- transformer-lens: `2.18.0`
- pandas: `2.2.2`
- numpy: `1.26.4`
