# Held-out frequency-head ablation manifest

**Record status: POST-RUN RECONSTRUCTION**

This manifest was created after the ablation completed because the original notebook wrote only the CSV.
File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.
Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.

- Manifest creation time (UTC): 2026-08-14T14:33:29.327490+00:00
- Repository commit at manifest creation: `1234c9a18c52e0977fcbba9a69804f4699b6bc43`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-2.8b`
- Prompt condition: `uniform`
- Random seed: `42`
- Split: Sorted compound names, shuffled once; first half selection, second half held out
- Held-out compounds: 25
- Selected heads: `[(22, 11), (26, 19), (29, 9), (29, 10), (29, 16)]`
- Layer-matched random control heads: `[(22, 12), (26, 2), (29, 15), (29, 26), (29, 5)]`
- Intervention: zero each listed head's `hook_z` output at the later constituent position
- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded

## Model/runtime

- Live model object: not available during reconstruction
- Runtime device and dtype: not contemporaneously recorded by the ablation notebook

## Recovered artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Ablation CSV | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-uniform-heldout-ablation.csv` | `a5121e1ac246333fea2c4c8fb1f7cb9305200a3a899bad0f1a71b4e29073ebfd` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_uniform.csv` | `b6fc759acb6a50f968fa94fc226c8afe0be37b3604fba13aeeb1fa13c6dbb126` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `f7814969765c770566f5935bad78ca895ef628af3e0c59ee91fdd594f9b7e3c0` |
| Intervention implementation | `src/qk_ov.py` | `945fdebe4f0f649e5922d8b95f1cb1a1431e2903f7aad3f81c0eb5de73b24a26` |
| Corresponding model manifest | `results/effective_binding/pythia/pythia-2.8b/uniform/pythia-2.8b-uniform-effective-binding.md` | `428b7c6b3026e96d1d890e4a30b31f146473b24e18256cdbc532cb2423fe730e` |

## Saved-result audit

- Rows: 25
- Selected KL mean / median: 1.672e-05 / 1e-05
- Selected KL range: [3e-06, 9.3e-05]
- Control KL mean / median: 5.08e-06 / 3e-06
- Control KL range: [0, 3.7e-05]
- Selected-minus-control mean / median: 1.164e-05 / 7e-06
- Selected > control / equal / selected < control: 25 / 0 / 0
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
