# Effective-binding run manifest

- Run time (UTC): 2026-08-13T23:59:22.769371+00:00
- Git commit: `efcc771807750eadda0adb46d498710adce8e07a`
- Working tree dirty at manifest time: `True`

## Experiment

- Model family: `olmo`
- Model name: `OLMo-2-0425-1B`
- Prompt condition: `uniform`
- Constituent direction: later compound token attends to earlier compound token
- Multi-token constituent rule: last subtoken represents the constituent
- Default scope: accessibility compounds with frozen frequency measurements

## Model

- Layers: 16
- Attention heads: 16
- Hidden size: 2048
- Vocabulary size: 100352
- Parameter count: 1,485,312,000
- Parameter dtype: `torch.float32`
- Device: `cuda:0 (NVIDIA A100-SXM4-80GB)`
- Requested model revision: `stage1-step1907359-tokens4001B`

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
For OLMo, the source-specific write is measured immediately before the attention-branch RMS normalization.

## Completeness

- Expected rows: 13,568
- Written rows: 13,568
- Difference: 0
- Rows in concatenated result frame: 13,568
- Unresolved compounds: 0

| domain | expected | written | output file | SHA-256 |
|---|---:|---:|---|---|
| accessibility | 13,568 | 13,568 | `OLMo-2-0425-1B-uniform-accessibility.csv` | `e196eecf64f971ed999cdca6732ab4b1c130af9067c67d5a97e8716c06d9b582` |

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
