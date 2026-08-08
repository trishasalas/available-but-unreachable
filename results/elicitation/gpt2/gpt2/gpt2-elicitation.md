# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-07T01:14:44.147905+00:00
- Git commit: 6221d65 (DIRTY)

## Model

- Model name: gpt2
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 12
- Heads: 12
- Hidden size: 768
- Vocab size: 50257
- Params: 163.0M

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
| control | 44 | 44 | `gpt2-control.csv` |
| accessibility | 92 | 92 | `gpt2-accessibility.csv` |
| medical | 42 | 42 | `gpt2-medical.csv` |
| legal | 44 | 44 | `gpt2-legal.csv` |
| finance | 44 | 44 | `gpt2-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
