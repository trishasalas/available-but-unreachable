# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:25:24.028267+00:00
- Git commit: 5640569 (DIRTY)

## Model

- Model name: pythia-13b
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 36
- Heads: 40
- Hidden size: 5120
- Vocab size: 50688
- Params: 11845.4M

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
| control | 63360 | 63360 | `pythia-13b-control.csv` |
| accessibility | 76320 | 76320 | `pythia-13b-accessibility.csv` |
| medical | 60480 | 60480 | `pythia-13b-medical.csv` |
| legal | 63360 | 63360 | `pythia-13b-legal.csv` |
| finance | 63360 | 63360 | `pythia-13b-finance.csv` |

**Total rows:** 326880
**Domains completed:** 5 / 5
