# Held-out frequency-head ablation manifest

**Record status: POST-RUN RECONSTRUCTION**

This manifest was created after the ablation completed because the original notebook wrote only the CSV.
File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.
Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.

- Manifest creation time (UTC): 2026-08-14T14:33:29.246053+00:00
- Repository commit at manifest creation: `1234c9a18c52e0977fcbba9a69804f4699b6bc43`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-160m`
- Prompt condition: `natural`
- Random seed: `42`
- Split: Sorted compound names, shuffled once; first half selection, second half held out
- Held-out compounds: 25
- Selected heads: `[(10, 9), (11, 1), (8, 4), (8, 11), (11, 5)]`
- Layer-matched random control heads: `[(10, 4), (11, 0), (8, 5), (8, 9), (11, 3)]`
- Intervention: zero each listed head's `hook_z` output at the later constituent position
- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded

## Model/runtime

- Live model object: not available during reconstruction
- Runtime device and dtype: not contemporaneously recorded by the ablation notebook

## Recovered artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Ablation CSV | `results/ablation/frequency_heads/pythia-160m/pythia-160m-natural-heldout-ablation.csv` | `0f4e92b89886510ff15a8cbbd807ae4a569f1d70c2c618a023990050b0631ec4` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_natural.csv` | `e3963a6c9ebdfd9ca61372c460b5015c48d3736179f8a55cd795735089c0abcf` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `f7814969765c770566f5935bad78ca895ef628af3e0c59ee91fdd594f9b7e3c0` |
| Intervention implementation | `src/qk_ov.py` | `945fdebe4f0f649e5922d8b95f1cb1a1431e2903f7aad3f81c0eb5de73b24a26` |
| Corresponding model manifest | `results/effective_binding/pythia/pythia-160m/natural/pythia-160m-natural-effective-binding.md` | `2b110acf1f70b24def3104d6f9ac7d6155ca30d7f29ffafbcf32e71609bdfbeb` |

## Saved-result audit

- Rows: 25
- Selected KL mean / median: 3.064e-05 / 2.3e-05
- Selected KL range: [4e-06, 9e-05]
- Control KL mean / median: 3.2e-06 / 2e-06
- Control KL range: [0, 2.7e-05]
- Selected-minus-control mean / median: 2.744e-05 / 1.9e-05
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
