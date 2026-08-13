# Effective-binding run manifest

- Run time (UTC): 2026-08-13T23:08:25.240099+00:00
- Git commit: `5029b855518ed4d7d27a16f71418e745a8fb0c69`
- Working tree dirty at manifest time: `True`

## Experiment

- Model family: `pythia`
- Model name: `pythia-160m`
- Prompt condition: `natural`
- Constituent direction: later compound token attends to earlier compound token
- Multi-token constituent rule: last subtoken represents the constituent
- Default scope: accessibility compounds with frozen frequency measurements

## Model

- Layers: 12
- Attention heads: 12
- Hidden size: 768
- Vocabulary size: 50304
- Parameter count: 162,334,848
- Parameter dtype: `torch.float32`
- Device: `cuda:0 (NVIDIA A100-SXM4-80GB)`

## Measurements

| column | definition |
|---|---|
| `binding_score` | Raw attention from the later compound token to the earlier token (compatibility alias). |
| `attention_weight` | Raw attention from the later compound token to the earlier token. |
| `ov_write_norm` | L2 norm of the earlier token's head-specific value vector after W_O. |
| `weighted_ov_norm` | attention_weight multiplied by ov_write_norm. |
| `relative_weighted_ov_norm` | weighted_ov_norm divided by the later token's resid_pre L2 norm. |
| `target_residual_norm` | L2 norm of resid_pre at the later compound token. |

The norm-aware measures are source-specific, head-specific writes. They are not a complete ALTI decomposition through all residual and normalization paths.

## Completeness

- Expected rows: 7,632
- Written rows: 7,632
- Difference: 0
- Rows in concatenated result frame: 7,632
- Unresolved compounds: 0

| domain | expected | written | output file | SHA-256 |
|---|---:|---:|---|---|
| accessibility | 7,632 | 7,632 | `pythia-160m-natural-accessibility.csv` | `d1ca706ff7e97a8e643e071427c66c3be405290066be10bdd815abc73cb880d2` |

## Inputs

| prompt file | SHA-256 |
|---|---|
| `data/binding/accessibility.yaml` | `642e891fedc32e5b01486a13f1b166d1850fad781230299b1b87047217a1000e` |

## Output schema

`compound`, `layer`, `head`, `binding_score`, `attention_weight`, `ov_write_norm`, `weighted_ov_norm`, `relative_weighted_ov_norm`, `target_residual_norm`, `word1`, `word2`, `prompt`, `prompt_condition`, `tokens`, `word1_idx`, `word2_idx`, `domain`, `family`, `model`

## Environment

- Python: `3.12.13`
- Platform: `Linux-6.6.122+-x86_64-with-glibc2.35`
- torch: `2.11.0+cu128`
- transformer-lens: `2.18.0`
- transformers: `4.57.6`
- pandas: `2.2.2`
- numpy: `1.26.4`
- PyYAML: `6.0.3`
