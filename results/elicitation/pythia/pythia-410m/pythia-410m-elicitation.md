# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-06T20:50:24.268136+00:00
- Git commit: f5f1a95

## Model

- Model name: pythia-410m
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 24
- Heads: 16
- Hidden size: 1024
- Vocab size: 50304
- Params: 405.3M

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
| finance | 44 | 44 | `pythia-410m-finance.csv` |

**Total rows:** 44
**Domains completed:** 1 / 1
