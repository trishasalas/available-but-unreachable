# Effective-binding run manifest

- Run time (UTC): 2026-08-13T22:37:04.028794+00:00
- Git commit: `aa6b375bd10ca60e0b344f570efc85577f407d4a`
- Working tree dirty at manifest time: `True`

## Experiment

- Model family: `gpt2`
- Model name: `gpt2-xl`
- Prompt condition: `uniform`
- Constituent direction: later compound token attends to earlier compound token
- Multi-token constituent rule: last subtoken represents the constituent
- Default scope: accessibility compounds with frozen frequency measurements

## Model

- Layers: 48
- Attention heads: 25
- Hidden size: 1600
- Vocabulary size: 50257
- Parameter count: 1,637,762,257
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

- Expected rows: 63,600
- Written rows: 63,600
- Difference: 0
- Rows in concatenated result frame: 63,600
- Unresolved compounds: 0

| domain | expected | written | output file | SHA-256 |
|---|---:|---:|---|---|
| accessibility | 63,600 | 63,600 | `gpt2-xl-uniform-accessibility.csv` | `6b3df2745bbad632ee91150a9ac29bc60c9274515b46c6805b14484644d4eac2` |

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
