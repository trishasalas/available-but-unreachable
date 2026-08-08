# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:18:11.192036+00:00
- Git commit: ea2b260 (DIRTY)

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
| control | 52800 | 52800 | `gpt2-xl-control.csv` |
| accessibility | 63600 | 63600 | `gpt2-xl-accessibility.csv` |
| medical | 50400 | 50400 | `gpt2-xl-medical.csv` |
| legal | 52800 | 52800 | `gpt2-xl-legal.csv` |
| finance | 52800 | 52800 | `gpt2-xl-finance.csv` |

**Total rows:** 272400
**Domains completed:** 5 / 5
