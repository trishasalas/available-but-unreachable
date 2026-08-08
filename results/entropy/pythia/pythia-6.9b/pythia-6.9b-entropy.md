# Model data captured during Entropy Battery

- Run (UTC): 2026-08-08T17:04:21.325832+00:00
- Git commit: fee8b71 (DIRTY)

## Model

- Model name: pythia-6.9b
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocab size: 50432
- Params: 6856.8M

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
| control | 44 | 44 | `pythia-6.9b-control.csv` |
| accessibility | 92 | 92 | `pythia-6.9b-accessibility.csv` |
| medical | 42 | 42 | `pythia-6.9b-medical.csv` |
| legal | 44 | 44 | `pythia-6.9b-legal.csv` |
| finance | 44 | 44 | `pythia-6.9b-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
