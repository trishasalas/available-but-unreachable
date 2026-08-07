# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-07T19:01:52.535766+00:00
- Git commit: 0905eed (DIRTY)

## Model

- Model name: OLMo-2-0425-1B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 16
- Heads: 16
- Hidden size: 2048
- Vocab size: 100352
- Params: 1485.3M

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
| accessibility | 92 | 92 | `OLMo-2-0425-1B-accessibility.csv` |
| medical | 42 | 42 | `OLMo-2-0425-1B-medical.csv` |
| legal | 44 | 44 | `OLMo-2-0425-1B-legal.csv` |
| finance | 44 | 44 | `OLMo-2-0425-1B-finance.csv` |

**Total rows:** 222
**Domains completed:** 4 / 4
