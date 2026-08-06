# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-06T20:22:39.825460+00:00
- Git commit: 020e211

## Model

- Model name: pythia-160m
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocab size: 50304
- Params: 162.3M

## Generation

- do_sample: False
- verbose: False

## Environment

- transformer_lens: 2.18.0
- transformers: 4.57.6
- torch: 2.11.0+cu128
- python: 3.12.13
- platform: Linux-6.6.122+-x86_64-with-glibc2.35

## Domains

| domain | expected | written | file |
|---|---|---|---|
| control | 44 | 44 | `pythia-160m-control.csv` |
| accessibility | 92 | 92 | `pythia-160m-accessibility.csv` |
| medical | 42 | 42 | `pythia-160m-medical.csv` |
| legal | 44 | 44 | `pythia-160m-legal.csv` |
| finance | 44 | 44 | `pythia-160m-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
