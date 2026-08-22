## 2. Binding tracks rarity, not knowledge

If the behavioral gap comes from a failure to combine the two words in a compound, binding strength should predict accuracy. Compounds with stronger constituent binding should be the ones the model gets right.

The global measure does not support that account. We take the maximum attention from the later constituent token to the earlier one across every layer and head. Its Pearson correlation with accuracy is 0.087 in GPT-2, −0.003 in Pythia, and 0.115 in OLMo. Maximum binding does not predict which compounds the model knows. Figure 2 shows the saturation: a dense band near 1.0 at every accuracy level.

![Scatter plot of maximum attention binding against behavioral accuracy for Pythia and GPT-2 compounds. Points form a dense vertical band near binding 1.0 at every accuracy level, and an annotation reports correlations near zero: binding saturates whether or not the model answers correctly.](figures/binding-vs-accuracy.png)

::: {.caption}
Figure 2. Maximum attention binding against behavioral accuracy, one point per compound per scale. Binding saturates near 1.0 regardless of accuracy. OLMo values appear in the text.
:::

The measure is also close to its ceiling. In GPT-2, 98% of compound pairs have a maximum attention score of at least 0.99. A measure with almost no remaining variance cannot distinguish compounds from one another. The null therefore rules out saturated, whole-network maximum attention as a knowledge measure. It does not rule out every form of constituent interaction.

We next restrict the analysis to the final third of each model and include the magnitude of the value write. For each head, value-weighted binding is the attention weight multiplied by the source token's value-write norm and divided by the target token's residual norm. We then take the 95th percentile across late-layer heads. This measure is negatively correlated with corpus frequency at all thirteen model-scale points. A shared-label aggregate permutation test (see Methods) gives $p = 0.0003$. The direction repeats under uniform prompts and after controlling for compound token count. Table 5 shows the primary natural-prompt correlations.

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

Rarer compounds receive stronger late-layer value-weighted writes. This is the opposite of what a knowledge-bearing account predicts. Common compounds are more likely to be answered correctly, but they receive less of the late-layer interaction measured here. The result is more consistent with unresolved or difficult processing than with successful composition.

The signal is distributed. It appears in the upper tail across many heads rather than in one head shared across models. Held-out head tests do not recover a small fixed set that carries the frequency relationship across compounds. This differs from the specialized rare-word head reported by Voita et al. (2019). Here the response is a population pattern, not a stable circuit.

The ablation results narrow the claim further. At each Pythia scale, we zero five frequency-sensitive heads at the second constituent and compare them with five layer-matched controls on 25 held-out compounds. Selected heads have larger effects than controls at four of six scales, but the absolute KL divergences are small. No intervention changes the top predicted token across 300 natural and uniform trials, and KL divergence does not vary consistently with compound frequency. The selected heads affect the output distribution, but this intervention does not show that they carry the behavioral effect.

Late value-weighted binding is real, distributed, and frequency-sensitive. Under the ablation tested here, it is not load-bearing. The pattern is consistent with difficulty, not with resolution.
