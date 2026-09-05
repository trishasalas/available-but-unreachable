# Registered held-out frequency-head ablation manifest

**Record status: CONTEMPORANEOUS RUN RECORD**

- Manifest creation time (UTC): 2026-09-05T00:41:37.741859+00:00
- Repository commit at manifest creation: `ead4e0b0a14fa5bc6d6d0425729b5f36e61dd381`
- Working tree dirty at manifest creation: `True`

## Design

- Model: `pythia-2.8b`
- Prompt condition: `natural`
- Random seed: `20260813`
- Split: saved preregistered 25-compound selection / 24-compound held-out test split
- Selected heads: `[(28, 5), (30, 6), (28, 13), (22, 25), (30, 11)]`
- Positive-control heads: `[(30, 0), (30, 1), (30, 2), (30, 3), (30, 4), (30, 5), (30, 6), (30, 7), (30, 8), (30, 9), (30, 10), (30, 11), (30, 12), (30, 13), (30, 14), (30, 15), (30, 16), (30, 17), (30, 18), (30, 19), (30, 20), (30, 21), (30, 22), (30, 23), (30, 24), (30, 25), (30, 26), (30, 27), (30, 28), (30, 29), (30, 30), (30, 31)]`
- Random controls: 100 saved five-head sets drawn from late layers
- Directional permutations: 10,000
- Intervention: zero listed heads' `hook_z` output at the later constituent position
- Outcome: full-precision KL(base || ablated) at the final prompt position

## Model/runtime

- Layers: 32
- Attention heads: 32
- Hidden size: 2560
- Parameter count: 2,774,926,464
- Parameter dtype: `torch.float32`
- Device: `cuda:0`

## Artifacts

| artifact | path | SHA-256 |
|---|---|---|
| Primary compound results | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-primary.csv` | `d403e2e4ee7676aff03bca9d10353420ed9d13fc0b9a727d6f62061055720e41` |
| Random-control compound results | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-random-controls.csv` | `2678936b3fcf2926b9aa18c6cac1e2bc902ac64d30f424fb5ad2f692654b92d8` |
| Random-set statistical summaries | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-random-set-summary.csv` | `a03fc0bc5f8ecced19d09893b27f0a8ffd6d91cdcc51a9d504ac7dea34c1c573` |
| Frozen head sets | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-head-sets.csv` | `c312c734b182fc633cb0f888cf955979213dbb6bf8ccbe0e4e5000a565b8d657` |
| Statistical summary | `results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-summary.csv` | `2c10b2b5d992364e072497f4a2d7a8b6708c41cb488beb6f6771d93e06338219` |
| Frozen compound split | `results/analysis/effective_binding_compound_split.csv` | `d54badbfb913beb3b7bb0420554780fe508e501ace97d22c8104b9c90e9ffb0c` |
| Candidate-head table | `results/analysis/effective_binding_head_candidates_natural.csv` | `81842f39781f0e21c9057f0e3d4713929c698499d661614446e916396f29fdb5` |
| Preregistration amendment | `docs/preregistrations/0003-amendment-2026-09-04-ablation-controls.md` | `160589de57d7a546f85c1b886cb3dba103ad2c2b3e4d6c8fe1fe31dec2108f05` |
| Ablation notebook | `notebooks/frequency-head-ablation-pythia.ipynb` | `dd9a0f3d43c17d27aa908bbaa06013f7b34cdd5992fb260ea5704f44ae29190f` |
| Intervention implementation | `src/qk_ov.py` | `e908ea3bb436c16bedeacd1c7b16967875e3b39a0e40a1b1d70f0ed289becb47` |
| Effective-binding model manifest | `results/effective_binding/pythia/pythia-2.8b/natural/pythia-2.8b-natural-effective-binding.md` | `0133f9483d37d490ad823f85ed631a93251b0abd927cdbdf299f68935ab4396e` |

## Saved statistical summary

| field | value |
|---|---:|
| `model` | pythia-2.8b |
| `condition` | natural |
| `random_seed` | 20260813 |
| `n_selection` | 25 |
| `n_test` | 24 |
| `selected_rho_frequency_kl` | 0.03652173913043478 |
| `selected_permutation_p_one_sided` | 0.5626437356264373 |
| `n_permutations` | 10000 |
| `selected_mean_kl` | 2.1266434487188235e-05 |
| `selected_median_kl` | 1.622827403480187e-05 |
| `selected_top_changes` | 0 |
| `empty_max_abs_kl` | 0.0 |
| `positive_control_max_kl` | 0.001837609801441431 |
| `positive_control_median_kl` | 0.00011818399070762098 |
| `positive_control_top_changes` | 0 |
| `n_random_sets` | 100 |
| `n_finite_random_rhos` | 100 |
| `random_rho_median` | 0.15304347826086956 |
| `selected_rho_random_tail_p` | 0.24752475247524752 |

## Output schemas

- Primary: `compound`, `model`, `condition`, `selected_heads`, `positive_control_heads`, `selected_kl`, `selected_top_changed`, `empty_kl`, `empty_top_changed`, `positive_control_kl`, `positive_control_top_changed`, `baseline_top`, `selected_ablated_top`, `positive_control_ablated_top`, `bigram_count`, `log_frequency`
- Random controls: `compound`, `model`, `condition`, `set_id`, `heads`, `kl`, `top_changed`, `bigram_count`, `log_frequency`
- Random-set summaries: `set_id`, `heads`, `rho_frequency_kl`, `mean_kl`, `median_kl`, `top_changes`
- Head sets: `set_id`, `role`, `heads`, `n_heads`
- Summary: `model`, `condition`, `random_seed`, `n_selection`, `n_test`, `selected_rho_frequency_kl`, `selected_permutation_p_one_sided`, `n_permutations`, `selected_mean_kl`, `selected_median_kl`, `selected_top_changes`, `empty_max_abs_kl`, `positive_control_max_kl`, `positive_control_median_kl`, `positive_control_top_changes`, `n_random_sets`, `n_finite_random_rhos`, `random_rho_median`, `selected_rho_random_tail_p`

## Manifest-generation environment

- Python: `3.11.13`
- Platform: `Linux-6.6.122+-x86_64-with-glibc2.35`
- torch: `2.6.0+cu124`
- transformer-lens: `2.18.0`
- pandas: `2.0.3`
- numpy: `1.26.4`
