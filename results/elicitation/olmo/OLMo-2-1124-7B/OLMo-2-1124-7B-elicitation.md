# Model data captured during Elicitation Battery

- Run (UTC): 2026-08-11T22:06:54.382074+00:00
- Git commit: aa73523

## Model

- Model name: OLMo-2-1124-7B
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 32
- Heads: 32
- Hidden size: 4096
- Vocab size: 100352
- Params: 7299.7M
- Revision: stage1-step928646-tokens3896B

## Server

- GPU: NVIDIA A100-SXM4-80GB

## Generation

- do_sample: False
- verbose: False

## Environment

- transformer_lens: 2.18.0
- transformers: 4.57.6
- torch: 2.11.0+cu128
- python: 3.12.13
- platform: Linux-6.6.122+-x86_64-with-glibc2.35

## Hugging Face

- Commit SHA: 7df9a82518afdecae4e8c026b27adccc8c1f0032
- Revision: stage1-step928646-tokens3896B

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
