# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:29:51.680847+00:00
- Git commit: d13650f (DIRTY)

## Model

- Model name: pythia-1b
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 16
- Heads: 8
- Hidden size: 2048
- Vocab size: 50304
- Params: 1011.7M

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
| control | 5632 | 5632 | `pythia-1b-control.csv` |
| accessibility | 6784 | 6784 | `pythia-1b-accessibility.csv` |
| medical | 5376 | 5376 | `pythia-1b-medical.csv` |
| legal | 5632 | 5632 | `pythia-1b-legal.csv` |
| finance | 5632 | 5632 | `pythia-1b-finance.csv` |

**Total rows:** 29056
**Domains completed:** 5 / 5
