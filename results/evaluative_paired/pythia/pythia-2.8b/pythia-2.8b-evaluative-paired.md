# Paired evaluative run manifest

- Run time (UTC): 2026-08-20T23:51:41.606147+00:00
- Git commit: `81cc2efa99aaa233fddbb801afa7ae601eb51242`
- Working tree dirty at run time: `True`
- Battery: `data/evaluative_paired.yaml`
- Battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Result CSV: `results/evaluative_paired/pythia/pythia-2.8b/pythia-2.8b-evaluative-paired.csv`
- Result SHA-256: `597f4b952cc008ba271782d0f57b278b2ad04906b3fdf8c7616f9d007c8108e2`

## Model

- Requested model: `pythia-2.8b`
- Frozen model key: `pythia-2.8b`
- Suite: `pythia`
- Scale: `2.8B`
- Parameter dtype: `torch.float32`
- Device: `cuda:0`
- Layers: 32
- Heads: 32
- Hidden size: 2560
- Vocabulary size: 50304
- Requested revision: `main`
- Resolved Hugging Face commit: `2a259cdd96a4beb1cdf467512e3904197345f6a9`

## Generation

- `do_sample=False`
- `max_new_tokens=100`
- Raw continuation preserved without stripping leading whitespace
- Expected rows: 16
- Written rows: 16

## Environment

- Python: `3.12.13`
- torch: `2.11.0+cu128`
- transformers: `4.57.6`
- transformer-lens: `2.18.0`
