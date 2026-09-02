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
| GPT-2 | 774M | -0.362 |
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
