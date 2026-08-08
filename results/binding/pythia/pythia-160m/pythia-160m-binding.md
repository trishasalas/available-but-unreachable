# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:31:15.123198+00:00
- Git commit: 73bc982 (DIRTY)

## Model

- Model name: pythia-160m
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocab size: 50304
- Params: 162.3M

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
| control | 6336 | 6336 | `pythia-160m-control.csv` |
| accessibility | 7632 | 7632 | `pythia-160m-accessibility.csv` |
| medical | 6048 | 6048 | `pythia-160m-medical.csv` |
| legal | 6336 | 6336 | `pythia-160m-legal.csv` |
| finance | 6336 | 6336 | `pythia-160m-finance.csv` |

**Total rows:** 32688
**Domains completed:** 5 / 5
