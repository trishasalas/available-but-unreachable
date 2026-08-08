# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:39:46.582513+00:00
- Git commit: 076d3ad (DIRTY)

## Model

- Model name: OLMo-2-1124-13B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 40
- Heads: 40
- Hidden size: 5120
- Vocab size: 100352
- Params: 13717.9M

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
| control | 70400 | 70400 | `OLMo-2-1124-13B-control.csv` |
| accessibility | 84800 | 84800 | `OLMo-2-1124-13B-accessibility.csv` |
| medical | 67200 | 67200 | `OLMo-2-1124-13B-medical.csv` |
| legal | 70400 | 70400 | `OLMo-2-1124-13B-legal.csv` |
| finance | 70400 | 70400 | `OLMo-2-1124-13B-finance.csv` |

**Total rows:** 363200
**Domains completed:** 5 / 5
