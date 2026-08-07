# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-07T22:16:36.198838+00:00
- Git commit: 5d9b2cf (DIRTY)

## Model

- Model name: OLMo-2-1124-7B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocab size: 100352
- Params: 7299.7M

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
| control | 44 | 44 | `OLMo-2-1124-7B-control.csv` |
| accessibility | 92 | 92 | `OLMo-2-1124-7B-accessibility.csv` |
| medical | 42 | 42 | `OLMo-2-1124-7B-medical.csv` |
| legal | 44 | 44 | `OLMo-2-1124-7B-legal.csv` |
| finance | 44 | 44 | `OLMo-2-1124-7B-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
