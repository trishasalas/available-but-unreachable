# Model data captured during Entropy Battery

- Run (UTC): 2026-08-08T17:09:29.223847+00:00
- Git commit: c1fb15e (DIRTY)

## Model

- Model name: pythia-12b
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
| control | 44 | 44 | `pythia-12b-control.csv` |
| accessibility | 92 | 92 | `pythia-12b-accessibility.csv` |
| medical | 42 | 42 | `pythia-12b-medical.csv` |
| legal | 44 | 44 | `pythia-12b-legal.csv` |
| finance | 44 | 44 | `pythia-12b-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
