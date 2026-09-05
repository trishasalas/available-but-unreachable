\clearpage
\setcounter{table}{0}
\renewcommand{\thetable}{A\arabic{table}}

## Appendix

### A. Models and generation

All thirteen models are base models. Table A1 reports architecture dimensions from the saved paired-run manifests. Model names follow the identifiers used by the loaders: Pythia models use the `EleutherAI/` namespace and OLMo 2 models use `allenai/`. GPT-2 model names are the TransformerLens loader identifiers.


| Model | Layers | Heads/layer | Hidden size | Model vocabulary |
| --- | --- | --- | --- | --- |
| gpt2 | 12 | 12 | 768 | 50257 |
| gpt2-large | 36 | 20 | 1280 | 50257 |
| gpt2-medium | 24 | 16 | 1024 | 50257 |
| gpt2-xl | 48 | 25 | 1600 | 50257 |
| OLMo-2-0425-1B | 16 | 16 | 2048 | 100352 |
| OLMo-2-1124-13B | 40 | 40 | 5120 | 100352 |
| OLMo-2-1124-7B | 32 | 32 | 4096 | 100352 |
| pythia-12b | 36 | 40 | 5120 | 50688 |
| pythia-160m | 12 | 12 | 768 | 50304 |
| pythia-1b | 16 | 8 | 2048 | 50304 |
| pythia-2.8b | 32 | 32 | 2560 | 50304 |
| pythia-410m | 24 | 16 | 1024 | 50304 |
| pythia-6.9b | 32 | 32 | 4096 | 50432 |

Table: Architecture dimensions recorded for the paired evaluative runs. Vocabulary sizes describe the model configuration. \label{tab:models}



| Model | Requested revision | Resolved commit in paired manifest |
| --- | --- | --- |
| gpt2 | main | 607a30d783df |
| gpt2-large | main | 32b71b12589c |
| gpt2-medium | main | 6dcaa7a952f7 |
| gpt2-xl | main | 15ea56dee5df |
| OLMo-2-0425-1B | stage1-step1907359-tokens4001B | 9d3e43659f00 |
| OLMo-2-1124-13B | stage1-step596057-tokens5001B | 08d2aca2e28a |
| OLMo-2-1124-7B | stage1-step928646-tokens3896B | c0371f4281bf |
| pythia-12b | main | bb1e3e710cdf |
| pythia-160m | main | Not recorded |
| pythia-1b | main | f73d7dcc545c |
| pythia-2.8b | main | 2a259cdd96a4 |
| pythia-410m | main | Not recorded |
| pythia-6.9b | main | c0e3eee36dc4 |

Table: Checkpoint provenance (12-character commit prefixes; full hashes are recorded in the manifests) for the paired evaluative runs. These records do not retrospectively pin separate earlier experiments. \label{tab:revisions}


The paired runner disables sampling and allows up to 100 new tokens. It preserves the raw continuation, including leading whitespace. The original elicitation helper supplies `temperature=0` and the per-prompt continuation limit; the current accessibility inventory specifies 100 tokens for the declarative and evaluative items. Binding and ablation measurements evaluate fixed prompts without generating continuations.

The OLMo revision labels are `stage1-step1907359-tokens4001B` (1B), `stage1-step928646-tokens3896B` (7B), and `stage1-step596057-tokens5001B` (13B). These requested labels are also recorded in the effective-binding manifests. The paired-run resolved commits are shown separately in Table A2. Earlier Pythia and GPT-2 binding runs do not record resolved model revisions; the registered Pythia-2.8B ablation likewise does not record a resolved checkpoint commit. Those omissions limit exact checkpoint reconstruction and are not filled using later runs.

The inference notebooks use TransformerLens tokenization. Binding result rows preserve the realized token strings and constituent indices. A separate tokenizer revision is not recorded in these manifests. Runtime versions and device/dtype information are retained per run rather than assumed identical across experiments.

### B. Prompt populations and coding

The original pooled comparison contains ten declarative and five evaluative prompts per model. Correct, partial, and incorrect responses receive 1, 0.5, and 0 in those battery means. The corpus-frequency analysis instead uses strict declarative accuracy across scales, assigning partial and incorrect responses zero. These are different estimands.

The paired battery contains sixteen prompts: a violation and a conformant item for each of eight concepts. WCAG and ARIA acronym-expansion items are excluded because application examples would test different knowledge. The battery was frozen on August 20, 2026. Pythia-2.8B remains development-exposed and is reported separately. The twelve confirmatory models contribute 192 item responses and 96 pairs; the pilot contributes sixteen responses and eight pairs.

The frozen coder lowercases and normalizes whitespace in the complete continuation. Empty or repetitively degenerate responses are incorrect. A violation is correct when the response contains both a negative accessibility classification and a concept-specific reason; either alone is partial. An affirmative classification on a violation is incorrect. A conformant item is correct with an affirmative classification unless the rule detects a contradictory reason; a negative classification is incorrect and an unclassified response is partial. The exact concept-specific string rules are preserved in `src/paired_evaluative.py`, and the original battery coding is preserved in `src/gap_analysis.py` and `src/accuracy_coding.py`. A pair passes only when both items are correct.

The frozen mechanical labels contain two documented conformant-item false positives: OLMo-2-1B focus indicator and GPT-2 alt text. Neither has a correct paired violation, so correcting these labels cannot produce a confirmatory pair pass. Removing exact prompt copies from the 21 confirmatory continuations containing them changes no item label. The reported item counts retain the frozen labels. In the pilot skip-link pair, the continuation supplies the classification but repeats prompt language that satisfies the reason rule; an independently generated explanation is not established.

The accompanying prompt inventory reproduces the fifteen original battery prompts, the 41 additional declarative probes, all sixteen frozen paired items and their expected judgments, and all 53 binding prompts. It is an extraction of the existing inventories, not a revision of the instrument.

### C. Binding measurement and coverage

The binding inventory contains 53 accessibility compounds. All thirteen models have saved natural- and uniform-prompt measurements. The frequency analysis retains the 49 compounds present in the frozen frequency table; `page_title`, `link_text`, `empty_link`, and `form_label` are excluded because that table contains no count for them. This exclusion is not a token-matching failure.

Natural prompts use the inventory text. Uniform prompts use `A {word1} {word2} is`. Matching first searches for a complete token after removing surrounding whitespace and ignoring case, then searches concatenated adjacent token strings. A split constituent is represented by its last subtoken. The earlier matched position supplies the value vector and the later position supplies the attention query and residual normalization. Unresolved constituents are reported by the producer.

For a head, the measure is its attention from the later position to the earlier position multiplied by the L2 norm of the earlier position's value vector after that head's output projection. This quantity is divided by the later position's pre-attention residual L2 norm, with a numerical lower bound of $10^{-12}$. For OLMo, the source-specific write is measured before attention-branch RMS normalization. This is not a complete decomposition of information flow through all normalization and residual paths.

The late-layer set uses zero-indexed layers $l \geq \lceil 2L/3 \rceil$. The primary statistic is the 95th percentile across all heads in that set for each compound. The maximum attention, maximum weighted write, maximum normalized write, and mean of the five largest normalized writes are retained as alternative summaries.

### D. Statistical procedures and prompt sensitivity

The binding confidence intervals use 2,000 paired compound bootstrap resamples with seed 20260813. Each resample draws 49 rows with replacement and recomputes Spearman correlation; nonfinite estimates are omitted. The endpoints are the 2.5th and 97.5th percentiles. These are per-model intervals, not simultaneous confidence intervals.

The shared-label test uses 10,000 permutations with seed 20260813. The same compound-frequency permutation is applied to every model. The statistic is the mean Fisher-transformed correlation, and the lower-tail probability uses the one-count correction. Natural prompts have two permuted statistics at least as negative as the observed statistic, giving $3/10001 = 0.000300$; uniform prompts have three, giving $4/10001 = 0.000400$. The observed mean Fisher transforms are -0.349354 for natural prompts and -0.364767 for uniform prompts.

The saved effective-binding analysis uses `results/frequency/frequency_table.csv` for all thirteen model-scale points. This shared frequency reference must be distinguished from the family-matched corpus counts used in the declarative-accuracy analysis.


| Model | Natural rho | 95% bootstrap interval | Uniform rho | 95% bootstrap interval |
| --- | --- | --- | --- | --- |
| gpt2 | -0.284 | [-0.549, 0.029] | -0.314 | [-0.554, -0.011] |
| gpt2-large | -0.350 | [-0.596, -0.043] | -0.362 | [-0.586, -0.070] |
| gpt2-medium | -0.342 | [-0.594, -0.048] | -0.430 | [-0.648, -0.153] |
| gpt2-xl | -0.152 | [-0.436, 0.140] | -0.240 | [-0.498, 0.049] |
| OLMo-2-0425-1B | -0.165 | [-0.433, 0.131] | -0.442 | [-0.645, -0.187] |
| OLMo-2-1124-13B | -0.254 | [-0.519, 0.063] | -0.217 | [-0.507, 0.094] |
| OLMo-2-1124-7B | -0.276 | [-0.544, 0.027] | -0.347 | [-0.615, -0.048] |
| pythia-12b | -0.369 | [-0.582, -0.110] | -0.452 | [-0.636, -0.227] |
| pythia-160m | -0.318 | [-0.541, -0.047] | -0.266 | [-0.523, 0.027] |
| pythia-1b | -0.451 | [-0.633, -0.198] | -0.310 | [-0.545, -0.045] |
| pythia-2.8b | -0.485 | [-0.685, -0.232] | -0.368 | [-0.594, -0.099] |
| pythia-410m | -0.420 | [-0.634, -0.134] | -0.413 | [-0.625, -0.133] |
| pythia-6.9b | -0.450 | [-0.659, -0.186] | -0.352 | [-0.577, -0.087] |

Table: Frequency correlations for the 95th-percentile normalized value-weighted binding measure, with 49 compounds per model and condition. This expands the former main-text Table 5. \label{tab:binding-sensitivity}


The declarative-frequency token-count sensitivity uses GPT-2 tokenization as a common count measure across families and partial Spearman correlation: variables are ranked and the first-order partial-correlation formula is applied to their Pearson rank correlations. The saved family-level partial correlations controlling compound token count are 0.5807 for Pythia, 0.5092 for GPT-2, and 0.5810 for OLMo. These results concern declarative accuracy and do not establish token-count robustness for value-weighted binding.

### E. Exploratory head localization

For each late-layer head, frequency is correlated with normalized value-weighted binding across all 49 compounds under natural prompts. This exploratory analysis is separate from the 25-compound selection procedure used for intervention. Head identities are not aligned across models.

Two-sided Spearman p-values receive Benjamini–Hochberg correction within each model over heads with defined correlations. Constant measurements yield undefined correlations: thirteen heads in Pythia-12B and two in Pythia-6.9B are excluded from that denominator. Bootstrap stability uses 2,000 paired compound resamples with seed 20260905, shared across heads within each model. The detailed tables report percentile intervals, the fraction of finite resamples with negative correlation, and correlation distributions by relative layer depth. The bootstrap intervals are marginal and are not corrected for multiple comparisons. These implementation choices are recorded as exploratory audit choices.


| Model | Late heads | Defined correlations | Negative correlations | Negative with BH q < .05 |
| --- | --- | --- | --- | --- |
| gpt2 | 48 | 48 | 16 | 0 |
| gpt2-large | 240 | 240 | 132 | 0 |
| gpt2-medium | 128 | 128 | 78 | 0 |
| gpt2-xl | 400 | 400 | 252 | 0 |
| OLMo-2-0425-1B | 80 | 80 | 49 | 6 |
| OLMo-2-1124-13B | 520 | 520 | 307 | 1 |
| OLMo-2-1124-7B | 320 | 320 | 192 | 8 |
| pythia-12b | 480 | 467 | 307 | 7 |
| pythia-160m | 48 | 48 | 28 | 0 |
| pythia-1b | 40 | 40 | 34 | 1 |
| pythia-2.8b | 320 | 320 | 252 | 5 |
| pythia-410m | 128 | 128 | 101 | 0 |
| pythia-6.9b | 320 | 318 | 218 | 6 |

Table: Exploratory head-level frequency associations. Negative signs and corrected statistical support are reported separately; these counts do not establish causal contributions. \label{tab:head-localization}


### F. Registered intervention and adherence

The registered natural-prompt Pythia-2.8B test sorts the 49 compound names, shuffles with seed 20260813, assigns the first 25 to selection and the remaining 24 to testing, and preserves the ordered split. The five selected zero-indexed (layer, head) pairs are (28, 5), (30, 6), (28, 13), (22, 25), and (30, 11). The intervention zeros their head outputs at the later constituent's last subtoken. The outcome is KL divergence from the baseline to the ablated full-vocabulary next-token distribution at the final prompt position.

The September 4 controls amendment specifies an empty intervention, 100 random five-head sets excluding the selected heads, and all 32 heads in layer 30 as the positive control. The registered run records all sets and 2,400 compound-by-random-set outcomes. The empty intervention yields zero KL on every compound. The positive control exceeds $10^{-6}$ for all 24 compounds. Both control gates pass.

For the selected set, frequency–KL Spearman correlation is 0.037, with one-sided permutation p = 0.563. Its empirical lower-tail probability among the random sets is 0.248. Mean KL is $2.13 \times 10^{-5}$ and median KL is $1.62 \times 10^{-5}$; no highest-probability token changes. The registered prediction of greater perturbation for rarer compounds is not supported. This does not establish that the selected heads have no effect.

A saved-artifact audit reproduces the split, head selection, random sets, statistical tests, and all eleven manifest hashes. The full baseline and intervened vocabulary distributions were not saved, so KL cannot be independently reconstructed from the CSVs alone. Earlier six-scale exploratory ablations used a different split and control design and are excluded from the manuscript's evidence.

The paired protocol's header retains unfilled freeze fields; the separate paired-results audit identifies the freeze commit and battery hash. The reproducibility record preserves that documentary distinction rather than rewriting the original preregistration retrospectively.

### G. Original pooled behavioral tables


| Scale | Declarative | Evaluative | Gap |
| ----- | ----------- | ---------- | --- |
| 160M  | 25%         | 10%        | 15% |
| 410M  | 40%         | 20%        | 20% |
| 1B    | 30%         | 10%        | 20% |
| 2.8B  | 60%         | 30%        | 30% |
| 6.9B  | 65%         | 50%        | 15% |
| 12B   | 45%         | 50%        | -5% |

Table: Pythia original-battery means. Correct, partial, and incorrect are scored 1, 0.5, and 0; gaps are percentage points. \label{tab:pooled-pythia}



| Concept             | 160M | 410M | 1B   | 2.8B | 6.9B | 12B |
| ------------------- | ---- | ---- | ---- | ---- | ---- | --- |
| ARIA                | inc  | inc  | inc  | inc  | inc  | inc |
| WCAG                | inc  | inc  | inc  | inc  | cor  | cor |
| alt text            | inc  | part | part | cor  | cor  | cor |
| closed captions     | inc  | inc  | inc  | cor  | inc  | inc |
| color contrast      | part | cor  | part | part | cor  | cor |
| focus indicator     | part | inc  | inc  | inc  | inc  | inc |
| keyboard navigation | part | cor  | cor  | cor  | cor  | inc |
| screen reader       | part | part | cor  | cor  | cor  | cor |
| semantic HTML       | part | part | inc  | part | part | part|
| skip link           | inc  | part | inc  | cor  | cor  | inc |

Table: Pythia declarative trajectories. cor, part, and inc denote correct, partial, and incorrect. \label{tab:trajectories}



| Family | Scale | Declarative | Evaluative | Gap |
| --- | ---: | ---: | ---: | ---: |
| GPT-2 | 124M | 35% | 20% | 15% |
| GPT-2 | 355M | 45% | 20% | 25% |
| GPT-2 | 774M | 50% | 30% | 20% |
| GPT-2 | 1.5B | 65% | 10% | 55% |
| OLMo 2 | 1B | 50% | 30% | 20% |
| OLMo 2 | 7B | 75% | 40% | 35% |
| OLMo 2 | 13B | 75% | 60% | 15% |

Table: GPT-2 and OLMo 2 original-battery means, using the same scoring as Table A5. \label{tab:pooled-other}



### H. Measurement-pathway validation

A decision-point analysis initially appeared to show the correct continuation for skip link losing to a higher-frequency competitor between Pythia-6.9B and Pythia-12B. The analysis projected the final residual stream directly through the unembedding matrix, omitting the model's final LayerNorm. A preregistered gate required the resulting trace to agree with the true forward pass. It did not, and the competition claim was withdrawn.

An audit of the saved rollouts found the same failure at all six Pythia scales: the shortcut left the true greedy trajectory within seven tokens. Under weight folding, the final LayerNorm bias becomes an effective unembedding bias, $b_U$, whose correlation with log Pile unigram frequency ranges from 0.664 to 0.779 across scales. The shortcut omits this frequency-ordered term; in all six observed divergences, the true pathway selected the more frequent token. This is a finding about measurement validity, not an explanation of the behavioral gap.



\clearpage

### I. Artifact map

The reproducibility materials preserve separate roles for the stimulus inventories, producers, result tables, and audit records.


| Purpose | Repository-relative artifact |
| --- | --- |
| Original prompt inventory | data/accessibility.yaml |
| Paired prompts and expected judgments | data/evaluative_paired.yaml |
| Binding prompt inventory | data/binding/accessibility.yaml |
| Paired generation and coding | src/paired_evaluative_runner.py; src/paired_evaluative.py |
| Original battery analysis | src/gap_analysis.py |
| Binding producers | notebooks/effective-binding-{pythia,gpt2,olmo}.ipynb |
| Binding summaries, bootstrap, aggregate tests | notebooks/effective-binding-analysis.ipynb; results/analysis/effective_binding_*.csv |
| Corpus accuracy and partial correlations | src/dual_spearman.py; results/frequency/spearman_partial.csv |
| Registered intervention | notebooks/frequency-head-ablation-pythia.ipynb; src/qk_ov.py |
| Registered run outputs and contemporaneous manifest | results/ablation/frequency_heads/pythia-2.8b/pythia-2.8b-natural-registered-* |
| Exploratory head audit | docs/audits/2026-09-05-head-localization-* |
| Protocols and controls amendment | docs/preregistrations/0002-evaluative-prompts.md; 0003-frequency-and-effective-late-layer-binding.md; 0003-amendment-2026-09-04-ablation-controls.md |

Table: Reproducibility artifact map. \label{tab:artifact-map}

