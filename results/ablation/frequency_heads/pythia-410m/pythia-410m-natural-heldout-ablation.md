# Held-out frequency-head ablation manifest

**Record status: POST-RUN RECONSTRUCTION**

This manifest was created after the ablation completed because the original notebook wrote only the CSV.
File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.
Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.

- Manifest creation time (UTC): 2026-08-14T14:33:29.343106+00:00
- Repository commit at manifest creation: `1234c9a18c52e0977fcbba9a69804f4699b6bc43`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-410m`
- Prompt condition: `natural`
- Random seed: `42`
- Split: Sorted compound names, shuffled once; first half selection, second half held out
- Held-out compounds: 25
- Selected heads: `[(23, 12), (20, 12), (22, 3), (16, 15), (23, 14)]`
- Layer-matched random control heads: `[(23, 5), (20, 1), (22, 8), (16, 11), (23, 2)]`
- Intervention: zero each listed head's `hook_z` output at the later constituent position
- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded

## Model/runtime

- Live model object: not available during reconstruction
- Runtime device and dtype: not contemporaneously recorded by the ablation notebook

## Recovered artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Ablation CSV | `results/ablation/frequency_heads/pythia-410m/pythia-410m-natural-heldout-ablation.csv` | `4dc6e107be312e16f7b7867e4cfd8afee7415d5a91fe8386364ba9cbbdff4cb8` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_natural.csv` | `e3963a6c9ebdfd9ca61372c460b5015c48d3736179f8a55cd795735089c0abcf` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `f7814969765c770566f5935bad78ca895ef628af3e0c59ee91fdd594f9b7e3c0` |
| Intervention implementation | `src/qk_ov.py` | `945fdebe4f0f649e5922d8b95f1cb1a1431e2903f7aad3f81c0eb5de73b24a26` |
| Corresponding model manifest | `results/effective_binding/pythia/pythia-410m/natural/pythia-410m-natural-effective-binding.md` | `d1520d5df6f75166aa03f38585c62356ef84801fe7a222c38060adaa672e5abe` |

## Saved-result audit

- Rows: 25
- Selected KL mean / median: 0.00020496 / 0.000149
- Selected KL range: [2.5e-05, 0.001264]
- Control KL mean / median: 4.92e-06 / 2e-06
- Control KL range: [1e-06, 3.7e-05]
- Selected-minus-control mean / median: 0.00020004 / 0.000147
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
