# Model data captured during Binding Battery

- Run (UTC): 2026-08-08T18:16:51.807258+00:00
- Git commit: d6839b7 (DIRTY)

## Model

- Model name: gpt2-large
- Model dtype: torch.float32
- Device: cuda:0
- Layers: 36
- Heads: 20
- Hidden size: 1280
- Vocab size: 50257
- Params: 838.2M

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
| control | 31680 | 31680 | `gpt2-large-control.csv` |
| accessibility | 38160 | 38160 | `gpt2-large-accessibility.csv` |
| medical | 30240 | 30240 | `gpt2-large-medical.csv` |
| legal | 31680 | 31680 | `gpt2-large-legal.csv` |
| finance | 31680 | 31680 | `gpt2-large-finance.csv` |

**Total rows:** 163440
**Domains completed:** 5 / 5
