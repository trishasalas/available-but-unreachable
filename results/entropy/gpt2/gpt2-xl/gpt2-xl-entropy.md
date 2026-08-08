# Model data captured during Entropy Battery

- Run (UTC): 2026-08-08T16:46:51.444656+00:00
- Git commit: ad3f997 (DIRTY)

## Model

- Model name: gpt2-xl
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 48
- Heads: 25
- Hidden size: 1600
- Vocab size: 50257
- Params: 1637.8M

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
| control | 44 | 44 | `gpt2-xl-control.csv` |
| accessibility | 92 | 92 | `gpt2-xl-accessibility.csv` |
| medical | 42 | 42 | `gpt2-xl-medical.csv` |
| legal | 44 | 44 | `gpt2-xl-legal.csv` |
| finance | 44 | 44 | `gpt2-xl-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
