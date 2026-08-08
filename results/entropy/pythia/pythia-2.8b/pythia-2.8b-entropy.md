# Model data captured during Entropy Battery

- Run (UTC): 2026-08-08T17:01:47.861614+00:00
- Git commit: 8a8732f (DIRTY)

## Model

- Model name: pythia-2.8b
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 32
- Heads: 32
- Hidden size: 2560
- Vocab size: 50304
- Params: 2774.9M

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
| control | 44 | 44 | `pythia-2.8b-control.csv` |
| accessibility | 92 | 92 | `pythia-2.8b-accessibility.csv` |
| medical | 42 | 42 | `pythia-2.8b-medical.csv` |
| legal | 44 | 44 | `pythia-2.8b-legal.csv` |
| finance | 44 | 44 | `pythia-2.8b-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
