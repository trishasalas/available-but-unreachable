# Effective-binding run manifest

- Run time (UTC): 2026-08-13T22:07:17.239604+00:00
- Git commit: `9026bf76df175db3f5d1fb75ff8ed053bdef359b`
- Working tree dirty at manifest time: `True`

## Experiment

- Model family: `gpt2`
- Model name: `gpt2`
- Prompt condition: `natural`
- Constituent direction: later compound token attends to earlier compound token
- Multi-token constituent rule: last subtoken represents the constituent
- Default scope: accessibility compounds with frozen frequency measurements

## Model

- Layers: 12
- Attention heads: 12
- Hidden size: 768
- Vocabulary size: 50257
- Parameter count: 163,049,041
- Parameter dtype: `torch.float32`
- Device: `cpu`

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
| accessibility | 7,632 | 7,632 | `gpt2-natural-accessibility.csv` | `c92b67da9f6c34f6a42be5a1b4428af064bc659341118aae9202713ef78242e6` |

## Inputs

| prompt file | SHA-256 |
|---|---|
| `data/binding/accessibility.yaml` | `642e891fedc32e5b01486a13f1b166d1850fad781230299b1b87047217a1000e` |

## Output schema

`compound`, `layer`, `head`, `binding_score`, `attention_weight`, `ov_write_norm`, `weighted_ov_norm`, `relative_weighted_ov_norm`, `target_residual_norm`, `word1`, `word2`, `prompt`, `prompt_condition`, `tokens`, `word1_idx`, `word2_idx`, `domain`, `family`, `model`

## Environment

- Python: `3.11.14`
- Platform: `macOS-26.5.2-arm64-arm-64bit`
- torch: `2.10.0`
- transformer-lens: `2.18.0`
- transformers: `4.57.6`
- pandas: `2.0.3`
- numpy: `1.26.4`
- PyYAML: `6.0.3`
