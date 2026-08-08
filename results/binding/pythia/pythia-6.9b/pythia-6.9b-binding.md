# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:27:38.587953+00:00
- Git commit: 95bd8ec (DIRTY)

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
| control | 45056 | 45056 | `pythia-6.9b-control.csv` |
| accessibility | 54272 | 54272 | `pythia-6.9b-accessibility.csv` |
| medical | 43008 | 43008 | `pythia-6.9b-medical.csv` |
| legal | 45056 | 45056 | `pythia-6.9b-legal.csv` |
| finance | 45056 | 45056 | `pythia-6.9b-finance.csv` |

**Total rows:** 232448
**Domains completed:** 5 / 5
