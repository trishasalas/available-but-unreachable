## 2. Binding tracks rarity, not knowledge

If the behavioral gap comes from a failure to combine the two words in a compound, binding strength should predict accuracy. Compounds with stronger constituent binding should be the ones the model gets right.

The global measure does not support that account. We take the maximum attention from the later constituent token to the earlier one across every layer and head. We use Spearman correlation because accuracy is ordered categorical data and the question concerns a monotonic association. Across compound-scale observations, Spearman $\rho$ is -0.059 in GPT-2, -0.126 in Pythia, and 0.108 in OLMo. These weak associations differ in direction across families; Pythia shows a weak negative relationship. They do not support the proposed positive relationship between maximum binding and accuracy. These are descriptive pooled correlations: the same compounds recur across scales, so the observations are not independent. Figure 4 shows the saturation: a dense band near 1.0 at every accuracy level.

![Scatter plot of maximum attention binding against behavioral accuracy for Pythia, GPT-2, and OLMo 2 compounds. Points form a dense band near binding 1.0 at every accuracy level; vertical position within each accuracy band is jittered for legibility.](figures/binding-vs-accuracy.png)

::: {.caption}
Figure 4. Maximum attention binding against behavioral accuracy, one point per compound per scale. Binding saturates near 1.0 regardless of accuracy; vertical jitter within bands is cosmetic. Per-family Spearman correlations are reported in the text.
:::

The measure is also close to its ceiling. In GPT-2, 98% of compound pairs have a maximum attention score of at least 0.99. This concentration near the ceiling limits the measure’s ability to distinguish compounds. The weak, mixed-direction associations do not support using whole-network maximum attention as a general indicator of knowledge. They do not rule out other forms of constituent interaction.

We next restrict the analysis to the final third of each model and include the magnitude of the value write. For each head, value-weighted binding is the attention weight multiplied by the source token's value-write norm and divided by the target token's residual norm. We then take the 95th percentile across late-layer heads. This measure is negatively correlated with corpus frequency at all thirteen model-scale points. A shared-label aggregate permutation test (see Methods) gives $p = 0.0003$. The direction repeats under uniform prompts at all thirteen model-scale points. Table 5 shows the primary natural-prompt correlations, and Figure 5 plots them with bootstrap confidence intervals.

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

![Dot plot of thirteen Spearman correlations between log bigram frequency and late-layer value-weighted binding, grouped by family, with confidence interval whiskers. Every dot sits left of zero; some intervals cross zero.](figures/binding-frequency-forest.png)

::: {.caption}
Figure 5. Spearman correlation between log bigram frequency and 95th-percentile late-layer value-weighted binding, one point per model, with bootstrap confidence intervals. All thirteen are negative; aggregate significance comes from the preregistered shared-label permutation test (Methods).
:::

Rarer compounds receive stronger late-layer value-weighted writes. This is the opposite of what a knowledge-bearing account predicts. Common compounds are more likely to be answered correctly, but they receive less of the late-layer interaction measured here. The result is more consistent with unresolved or difficult processing than with successful composition.

The frequency association is distributed across multiple late-layer heads. It appears in the upper tail of late-layer value-weighted writes. @voita2019analyzing identify a specialized rare-word head in an encoder model; the present analysis examines associations across heads in decoder-only models. Here the response is a population pattern, not evidence of a stable circuit.

The registered held-out ablation did not support the predicted greater perturbation for rarer compounds. Across 24 test compounds, frequency and selected-set KL had Spearman $\rho = 0.037$ (one-sided permutation $p = 0.563$). The selected correlation was not unusually negative relative to the 100 random sets (empirical one-sided tail probability 0.248). Mean KL was $2.13 \times 10^{-5}$, and no highest-probability token changed. Both control gates passed: the empty intervention produced zero KL for every compound, and the penultimate-layer control exceeded the registered KL threshold for all 24 compounds. These results do not show that the selected heads have no effect; they show that the measured perturbation did not increase with rarity as predicted.

Late value-weighted binding is real, distributed, and frequency-sensitive. The pattern is consistent with difficulty, not with resolution; the present evidence does not establish its causal role.
