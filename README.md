# Available but Unreachable: The Declarative-Evaluative Gap in Language Models.

Language models can define a concept fluently and then fail to apply it — producing *fluent wrongness*. This paper asks what explains that gap across model scale and architecture, using accessibility concepts as a test domain where ground truth is concrete and training-data frequency varies cleanly.

**Cross-architecture:** Pythia (6 scales), GPT-2 (4), OLMo-2 (3) — 13 models total, base checkpoints, greedy decoding.

**Three main findings:**

1. **The gap exists and is systematic.** Models produce correct definitions alongside incorrect applications, with high-confidence wrong answers (low entropy).
2. **Compound binding is compensatory, not causal.** A three-tier binding architecture (lexical, positional, hybrid heads) is statistically real but does not drive the gap — ablation shows the model routes around it.
3. **Corpus frequency is the floor, not the ceiling.** Frequency predicts which concepts a model will fail on, but does not explain all the variance in how it fails.

## Repository layout

```
data/                Prompt batteries (YAML): accessibility, control, medical, legal, finance
data/binding/        Compound-binding batteries: 227 compounds across 5 domains
src/                 Analysis modules (see below)
results/             Experimental outputs by battery type
notebooks/           Experiment notebooks (one per model suite × battery)
paper/               Manuscript, figures, and build tooling
paper/generate-figures/  Figure scripts — each reads from results/ CSVs
docs/                Decisions, preregistrations, findings, audit records
scripts/             Build and review utilities
_archive/            Historical notebooks, results, source — tracked, not active
```

## `src/` modules

| Module | Role |
|---|---|
| `analysis.py` | Central loader — `load_all_results` returns elicitation, entropy, and binding frames |
| `gap_analysis.py` | Accuracy coding and gap tables |
| `accuracy_coding.py` | Grading rules — changes require a DECISIONS entry |
| `elicitation.py` | Declarative and evaluative elicitation runner |
| `entropy.py` | Token-level entropy extraction |
| `binding.py` | Compound-binding battery runner |
| `frequency.py` | Infini-gram corpus frequency pipeline |
| `manifest.py` | Data-integrity layer (expected == written == actual) |
| `logit_lens.py`, `decompose.py`, `qk_ov.py` | Mechanistic analysis tooling |
| `head_characterization.py`, `heads.py`, `probe.py` | Head-level and probing analysis |
| `d6_multihead_ablation.py`, `d7_token_ban.py`, `d8_frequency_prior.py` | Registered experiments |
| `tl217_olmo2_adapter.py`, `olmo_config.py` | OLMo-2 support for TransformerLens |

## Setup

**Conda environment** (no venv):

```bash
conda activate mechinterp
```

**Dependencies:**

```bash
pip install -r requirements.txt
```

Key packages: PyTorch, TransformerLens (2.18), HuggingFace Transformers, pandas, matplotlib.

**Running experiments** from the repo root:

```bash
PYTHONPATH=. python -m src.elicitation   # or any src module
```

Notebooks are in `notebooks/` and are designed to run on either local (MPS/CUDA) or Colab.

## Building the paper

```bash
cd paper && bash build-paper.sh
```

Figures are generated from results CSVs by scripts in `paper/generate-figures/`.

## Research documentation

- `DECISIONS.md` — methodological decision ledger (numbered, cited from findings)
- `docs/decisions/` — ADR-format decisions, one per file, immutable once accepted
- `docs/preregistrations/` — committed before results are seen; timestamps are evidence
- `docs/findings/CLAIMS.md` — claim ledger linking findings to evidence files

## Author

Trisha Salas
