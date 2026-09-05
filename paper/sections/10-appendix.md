## Appendix

**Table 1**

| Scale | Declarative | Evaluative | Gap |
| ----- | ----------- | ---------- | --- |
| 160M  | 25%         | 10%        | 15% |
| 410M  | 40%         | 20%        | 20% |
| 1B    | 30%         | 10%        | 20% |
| 2.8B  | 60%         | 30%        | 30% |
| 6.9B  | 65%         | 50%        | 15% |
| 12B   | 45%         | 50%        | -5% |

**Table 3** gives the family results not shown in Table 1

| Family | Scale | Declarative | Evaluative | Gap |
| --- | ---: | ---: | ---: | ---: |
| GPT-2 | 124M | 35% | 20% | 15% |
| GPT-2 | 355M | 45% | 20% | 25% |
| GPT-2 | 774M | 50% | 30% | 20% |
| GPT-2 | 1.5B | 65% | 10% | 55% |
| OLMo 2 | 1B | 50% | 30% | 20% |
| OLMo 2 | 7B | 75% | 40% | 35% |
| OLMo 2 | 13B | 75% | 60% | 15% |

**Table 5** shows the primary natural-prompt correlations, and Figure 5 plots them with bootstrap confidence intervals.

| Family | Model | Spearman $\rho$ |
| --- | --- | ---: |
| GPT-2 | 124M | -0.284 |
| GPT-2 | 355M | -0.342 |
| GPT-2 | 774M | -0.350 |
| GPT-2 | 1.5B | -0.152 |
| OLMo 2 | 1B | -0.165 |
| OLMo 2 | 7B | -0.276 |
| OLMo 2 | 13B | -0.254 |
| Pythia | 160M | -0.318 |
| Pythia | 410M | -0.420 |
| Pythia | 1B | -0.451 |
| Pythia | 2.8B | -0.485 |
| Pythia | 6.9B | -0.450 |
| Pythia | 12B | -0.369 |

### Measurement-pathway validation

A decision-point analysis initially appeared to show the correct continuation for skip link losing to a higher-frequency competitor between Pythia-6.9B and Pythia-12B. The analysis projected the final residual stream directly through the unembedding matrix, omitting the model's final LayerNorm. A preregistered gate required the resulting trace to agree with the true forward pass. It did not, and the competition claim was withdrawn.

An audit of the saved rollouts found the same failure at all six Pythia scales: the shortcut left the true greedy trajectory within seven tokens. Under weight folding, the final LayerNorm bias becomes an effective unembedding bias, $b_U$, whose correlation with log Pile unigram frequency ranges from 0.664 to 0.779 across scales. The shortcut omits this frequency-ordered term; in all six observed divergences, the true pathway selected the more frequent token. This is a finding about measurement validity, not an explanation of the behavioral gap.

### Preregistration 0003 deviation

The registered Pythia-2.8B causal test was completed using the frozen 25/24 compound split and the controls specified in the September 4 amendment. Earlier six-scale exploratory ablations used a different split and control design and are excluded from the manuscript’s evidence. Their artifacts are retained in the repository. The registered run has a contemporaneous manifest recording the output and code hashes.
