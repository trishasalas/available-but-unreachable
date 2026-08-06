# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-06T22:19:52.485462+00:00
- Git commit: 69da9a4 (DIRTY)

## Model

- Model name: pythia-1b
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 16
- Heads: 8
- Hidden size: 2048
- Vocab size: 50304
- Params: 1011.7M

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
| accessibility | 92 | 92 | `pythia-1b-accessibility.csv` |
| medical | 42 | 42 | `pythia-1b-medical.csv` |
| legal | 44 | 44 | `pythia-1b-legal.csv` |
| finance | 44 | 44 | `pythia-1b-finance.csv` |

**Total rows:** 222
**Domains completed:** 4 / 4
