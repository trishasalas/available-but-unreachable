# Model data captured during Entropy Battery

- Run (UTC): 2026-08-08T16:28:20.494803+00:00
- Git commit: 1d2abd1 (DIRTY)

## Model

- Model name: OLMo-2-0425-1B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 16
- Heads: 16
- Hidden size: 2048
- Vocab size: 100352
- Params: 1485.3M
- Revision: stage1-step1907359-tokens4001B

## Server

- GPU: NVIDIA A100-SXM4-80GB

## Environment

- transformer_lens: 2.18.0
- transformers: 4.57.6
- torch: 2.11.0+cu128
- python: 3.12.13
- platform: Linux-6.6.122+-x86_64-with-glibc2.35

## Hugging Face

- Commit SHA: a1847dff35000b4271fa70afc5db10fd29fedbdf
- Revision: stage1-step1907359-tokens4001B

## Domains

| domain | expected | written | file |
|---|---|---|---|
| control | 44 | 44 | `OLMo-2-0425-1B-control.csv` |
| accessibility | 92 | 92 | `OLMo-2-0425-1B-accessibility.csv` |
| medical | 42 | 42 | `OLMo-2-0425-1B-medical.csv` |
| legal | 44 | 44 | `OLMo-2-0425-1B-legal.csv` |
| finance | 44 | 44 | `OLMo-2-0425-1B-finance.csv` |

**Total rows:** 266
**Domains completed:** 5 / 5
