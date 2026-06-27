# Extended Gap Analysis — Instructions for CC

## Context
The base gap analysis (`src/gap_analysis.py` and `src/accuracy_coding.py`) is in place. It codes declarative and evaluative responses as correct/partial/incorrect and produces accuracy tables, gap scores, and emergence thresholds across all 10 models (Pythia 160M–12B, GPT-2 small–XL).

The following extensions use data already in `results/pythia/` and `results/gpt2/` — three CSVs per model: binding, entropy, and results. No new experiments needed.

## Extensions to build into `src/gap_analysis.py`

### 1. Entropy as a confidence metric ("fluent wrongness")
Compare last-token entropy on incorrect accessibility responses vs correct bicycle control responses. If the model is *more confident* (lower entropy) when wrong on accessibility than when right on bicycles, that's quantitative evidence of fluent wrongness. Produce a table: concept × scale × accuracy × mean_last_token_entropy.

### 2. Binding depth vs accuracy correlation
For each concept at each scale, pair the max binding score (from binding CSVs) with the accuracy code (from gap analysis). Test: do concepts with stronger late-layer binding produce more correct responses? A scatter or correlation table linking attention patterns to behavioral output.

### 3. Per-concept scaling curves
For each concept, plot accuracy score (incorrect=0, partial=1, correct=2) across all scales. Group into trajectory types:
- Monotonic climb (e.g., screen reader)
- Peak and regress / inverse scaling (e.g., skip link)
- Never emerges (e.g., ARIA)
Produce both a data table and a figure-ready CSV.

### 4. Entropy divergence between declarative and evaluative
At each scale, compute the mean entropy for declarative prompts vs evaluative prompts. At what scale does the gap between them widen? If the model's internal uncertainty on evaluative prompts increases with scale while declarative improves, it's internally signaling the gap.

### 5. Degenerate output detection
Automatically flag responses that contain degenerate repetition (e.g., "a link that is not a link that is not a link"). Metric: what percentage of responses are degenerate at each scale? Does degeneration correlate with specific compounds or prompt types?

### 6. The completion paradox
Few-shot code completion prompts (e.g., `<img src="photo.jpg"` after two examples with alt=) show models generating correct `alt="Photo"` at scales where they can't define what alt text is. Quantify: at each scale, does the model succeed at pattern-matching the syntax before it can explain the concept? Compare completion accuracy vs declarative accuracy per concept per scale.

## Output
All extensions should save to `results/analysis/` alongside the existing gap analysis CSVs. Each table should be reproducible from `python -m src.gap_analysis` or from the analysis notebook.

## Files to modify
- `src/gap_analysis.py` — add the new analysis functions
- `src/accuracy_coding.py` — may need `code_completion()` and `code_control()` additions for extensions 5 and 6
- `notebooks/analysis.ipynb` — import and display the new tables

## Notes
- The accuracy coding rules in `accuracy_coding.py` are the methodology. Any changes to coding criteria need a DECISIONS.md entry.
- Binding data has different column counts per model (different head counts per layer). Handle gracefully.
- The `_analysis/` directory (with underscore) is for Excel files and is excluded from blind study scope. The `results/analysis/` directory (no underscore) is for reproducible CSV outputs.
