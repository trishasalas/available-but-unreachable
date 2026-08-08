# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:43:00.766067+00:00
- Git commit: 3222371 (DIRTY)

## Model

- Model name: OLMo-2-1124-7B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocab size: 100352
- Params: 7299.7M

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
| control | 45056 | 45056 | `OLMo-2-1124-7B-control.csv` |
| accessibility | 54272 | 54272 | `OLMo-2-1124-7B-accessibility.csv` |
| medical | 43008 | 43008 | `OLMo-2-1124-7B-medical.csv` |
| legal | 45056 | 45056 | `OLMo-2-1124-7B-legal.csv` |
| finance | 45056 | 45056 | `OLMo-2-1124-7B-finance.csv` |

**Total rows:** 232448
**Domains completed:** 5 / 5
