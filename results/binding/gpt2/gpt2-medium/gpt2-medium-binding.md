# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:15:46.882625+00:00
- Git commit: 3bb4640 (DIRTY)

## Model

- Model name: gpt2-medium
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 24
- Heads: 16
- Hidden size: 1024
- Vocab size: 50257
- Params: 406.2M

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
| control | 16896 | 16896 | `gpt2-medium-control.csv` |
| accessibility | 20352 | 20352 | `gpt2-medium-accessibility.csv` |
| medical | 16128 | 16128 | `gpt2-medium-medical.csv` |
| legal | 16896 | 16896 | `gpt2-medium-legal.csv` |
| finance | 16896 | 16896 | `gpt2-medium-finance.csv` |

**Total rows:** 87168
**Domains completed:** 5 / 5
