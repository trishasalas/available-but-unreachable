# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:46:44.457057+00:00
- Git commit: 1f4f0d3 (DIRTY)

## Model

- Model name: OLMo-2-0425-1B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 16
- Heads: 16
- Hidden size: 2048
- Vocab size: 100352
- Params: 1485.3M

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
| control | 11264 | 11264 | `OLMo-2-0425-1B-control.csv` |
| accessibility | 13568 | 13568 | `OLMo-2-0425-1B-accessibility.csv` |
| medical | 10752 | 10752 | `OLMo-2-0425-1B-medical.csv` |
| legal | 11264 | 11264 | `OLMo-2-0425-1B-legal.csv` |
| finance | 11264 | 11264 | `OLMo-2-0425-1B-finance.csv` |

**Total rows:** 58112
**Domains completed:** 5 / 5
