## Limitations

We report findings from a first investigation into accessibility concept
emergence across the Pythia model suite, with replication across GPT-2.
Several limitations should be considered when interpreting the results.

### Prompt Design

All declarative experiments used completion-style prompts ("A screen
reader is," "WCAG stands for") rather than instruction or question
formats. Prompt framing is known to affect retrieval in language models,
and our own findings support that sensitivity. The alt text retrieval
experiment demonstrated that the HTML-framed prompt ("In HTML, the alt
attribute provides a text description of an") performed worse than the
simpler framing despite testing identical knowledge. Results reported
here reflect one prompt design choice and may not generalize to other
framings.

The declarative prompts were adapted from attention binding experiments
rather than designed independently for behavioral testing. Future work
should compare multiple prompt formulations to establish which results
are robust across framings.

### Evaluative Experiment Prompts

The original evaluative experiment (Experiment 2a) used zero-shot code
completion prompts. The image missing alt attribute result --- where
models loop the prompt rather than identify the missing attribute ---
may reflect document completion behavior rather than a knowledge
failure. Models trained on code repositories may interpret
`<img src='photo.jpg'>` as the beginning of a code listing and complete
accordingly.

The elicitation robustness experiments (Experiment 2b) partially address
this limitation by testing the same underlying knowledge across multiple
prompt formats, including direct questioning and error correction
strategies that do not rely on code completion framing. The gap persists
across all strategies tested, reducing the likelihood that the original
finding was an artifact of completion-style prompting. However,
instruction-tuned models may produce different results, and this remains
a direction for future work.

### Entropy Analysis

The entropy analysis (Experiment 2c) was computed on three
hypothesis-driven prompts at two model scales. The three distinct
failure profiles at 2.8B are a suggestive finding, but the small number
of prompts per condition limits the statistical power of the
observation. Whether the entropy differentiation generalizes across a
broader set of evaluative prompts and additional model scales has not
been tested. The entropy values reported are descriptive rather than
inferential --- no statistical significance tests were applied.

### Perplexity Experiment Scope

Recognition versus generation was tested using three sentence pairs
across screen reader, alt text, and skip link. The preference flip is a
clear finding for screen reader and alt text, but skip link fails to
flip in either model family, suggesting the
recognition-before-generation pattern does not hold uniformly across all
accessibility compounds. A broader set of correct/incorrect pairs across
additional concepts would further characterize which compounds follow
this pattern and which do not.

### Attention Binding Methodology

The proximity control experiment was run at 2.8B only. Control testing
revealed that adjacent token pairs --- including function word pairs and
modifier-noun pairs without disambiguation --- produce strong binding at
L1H12, which was subsequently confirmed as a previous-token head
attending systematically to the immediately preceding position
regardless of content. This finding limits the interpretation of L1H12's
consistent appearance across accessibility compounds. Whether other
heads show accessibility-specific binding patterns that do not appear in
non-compound controls has not been fully characterized and is noted as a
direction for future work. Early-layer binding at 160M (including Layer
11 Head 8 at score 1.0) remains ambiguous. Whether this reflects genuine
compound representation or positional attention at small scales cannot
be determined from attention weights alone.

The compound generalization finding --- that alt text and skip link show
comparable binding to screen reader at 2.8B --- is based on head counts
above the 0.1 threshold across all three compounds.

The 12B binding extension uses the same methodology and thresholds as
the original experiment. The late-layer resurgence observation is based
on head counts in the final layers and has not been tested with
additional compound terms at 12B. Whether the resurgence pattern
generalizes beyond "screen reader" at this scale is unknown.

### Cross-Architecture Comparison

GPT-2 models vary in both layer count and head count across sizes,
making direct per-head comparisons across model sizes less controlled
than Pythia's uniform architecture. The binding depth comparison between
GPT-2 and Pythia is expressed as a proportion of total network depth to
account for this, but the architectures are not directly commensurable.
Additional replication on architectures with controlled scaling (such as
other Pythia-style suites) would strengthen the cross-architecture
claims.

### Greedy Decoding

All experiments were run with temperature=0 for deterministic outputs.
Greedy decoding ensures reproducibility but may suppress partial
knowledge that stochastic decoding could surface. Models with partial
accessibility encoding may perform differently under sampling-based
generation. This is noted as a direction for future exploration.

### Hardware and Reproducibility

All experiments were run on Google Colab with an A100 GPU. All notebooks
are available in the project repository for independent verification.

### Scale Coverage

Declarative testing covers 160M through 12B for Pythia and 117M through
1.5B for GPT-2. The evaluative experiments (Experiment 2a) cover 160M
through 6.9B for Pythia. The binding analysis extends to Pythia 12B. ARIA fails to emerge at any scale tested in either model
family. Whether ARIA would emerge at larger scales is unknown. The
evaluative gap --- models that define concepts cannot identify violations
--- was not tested beyond 6.9B. Both findings may reflect limitations of
the scale range rather than fundamental properties of these concepts.