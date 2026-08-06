# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-06T21:56:05.720327+00:00
- Git commit: 9d8bc02 (DIRTY)

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
| control | 44 | 44 | `pythia-1b-control.csv` |

**Total rows:** 44
**Domains completed:** 1 / 1
