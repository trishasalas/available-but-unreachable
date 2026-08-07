# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-07T23:04:50.237628+00:00
- Git commit: f58ef5d (DIRTY)

## Model

- Model name: OLMo-2-1124-13B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 40
- Heads: 40
- Hidden size: 5120
- Vocab size: 100352
- Params: 13717.9M

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
| control | 44 | 44 | `OLMo-2-1124-13B-control.csv` |
| accessibility | 92 | 92 | `OLMo-2-1124-13B-accessibility.csv` |
| medical | 42 | 42 | `OLMo-2-1124-13B-medical.csv` |
| legal | 44 | 44 | `OLMo-2-1124-13B-legal.csv` |
| finance | 44 | 44 | `OLMo-2-1124-13B-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
