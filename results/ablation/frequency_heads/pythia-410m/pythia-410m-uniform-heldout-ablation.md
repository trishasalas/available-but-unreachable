# Held-out frequency-head ablation manifest

**Record status: POST-RUN RECONSTRUCTION**

This manifest was created after the ablation completed because the original notebook wrote only the CSV.
File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.
Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.

- Manifest creation time (UTC): 2026-08-14T14:33:29.358432+00:00
- Repository commit at manifest creation: `1234c9a18c52e0977fcbba9a69804f4699b6bc43`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-410m`
- Prompt condition: `uniform`
- Random seed: `42`
- Split: Sorted compound names, shuffled once; first half selection, second half held out
- Held-out compounds: 25
- Selected heads: `[(22, 6), (23, 12), (16, 15), (23, 7), (19, 14)]`
- Layer-matched random control heads: `[(22, 5), (23, 1), (16, 7), (23, 13), (19, 2)]`
- Intervention: zero each listed head's `hook_z` output at the later constituent position
- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded

## Model/runtime

- Live model object: not available during reconstruction
- Runtime device and dtype: not contemporaneously recorded by the ablation notebook

## Recovered artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Ablation CSV | `results/ablation/frequency_heads/pythia-410m/pythia-410m-uniform-heldout-ablation.csv` | `64c6ecd5529577eee24a9aa7941269dc70c29b8713d22bffb2ecafce03e0d430` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_uniform.csv` | `b6fc759acb6a50f968fa94fc226c8afe0be37b3604fba13aeeb1fa13c6dbb126` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `f7814969765c770566f5935bad78ca895ef628af3e0c59ee91fdd594f9b7e3c0` |
| Intervention implementation | `src/qk_ov.py` | `945fdebe4f0f649e5922d8b95f1cb1a1431e2903f7aad3f81c0eb5de73b24a26` |
| Corresponding model manifest | `results/effective_binding/pythia/pythia-410m/uniform/pythia-410m-uniform-effective-binding.md` | `2cbeb4e3f3aca9ef69e4aa97bed9f58bc96c5daef873d12a1dcb24036f0cea5e` |

## Saved-result audit

- Rows: 25
- Selected KL mean / median: 0.0001832 / 0.000144
- Selected KL range: [2.4e-05, 0.000559]
- Control KL mean / median: 5.808e-05 / 4.2e-05
- Control KL range: [1.5e-05, 0.000213]
- Selected-minus-control mean / median: 0.00012512 / 8.8e-05
- Selected > control / equal / selected < control: 24 / 0 / 1
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
