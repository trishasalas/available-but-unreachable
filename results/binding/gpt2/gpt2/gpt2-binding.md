# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:15:06.205117+00:00
- Git commit: f95934d (DIRTY)

## Model

- Model name: gpt2
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocab size: 50257
- Params: 163.0M

## Server

- GPU: NVIDIA A100-SXM4-80GB

## Environment

- transformer_lens: 2.18.0
- transformers: 4.57.6
- torch: 2.11.0+cu128
- python: 3.12.13
- platform: Linux-6.6.122+-x86_64-with-glibc2.35

## Domains

| domain | expected | written | file |
|---|---|---|---|
| control | 6336 | 6336 | `gpt2-control.csv` |
| accessibility | 7632 | 7632 | `gpt2-accessibility.csv` |
| medical | 6048 | 6048 | `gpt2-medical.csv` |
| legal | 6336 | 6336 | `gpt2-legal.csv` |
| finance | 6336 | 6336 | `gpt2-finance.csv` |

**Total rows:** 32688
**Domains completed:** 5 / 5
