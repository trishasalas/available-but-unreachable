## 3. Frequency is the floor, not the ceiling

The binding result shows that corpus frequency is related to what happens between a compound's constituents during inference. This section asks how much frequency explains at the behavioral level.

Bigram frequency predicts declarative accuracy in all three model families. Spearman $\rho$ is 0.5875 in Pythia, 0.5194 in GPT-2, and 0.5823 in OLMo, with $p$ < 0.001 and $n$ = 49 compounds in each family. The Pythia count comes from its training corpus. GPT-2 reproduces the relationship using Pile counts as a cross-corpus proxy, and OLMo reproduces it using OLMo-Mix counts. The OLMo result is unchanged after pinning and rerunning the model checkpoints. Figure 6 shows all 49 compounds in each family.

![Three scatter panels, one per family, plotting log bigram count against mean declarative accuracy for 49 compounds. Accuracy trends upward with frequency in every panel, with wide vertical spread at similar counts, including zero-accuracy compounds across most of the frequency range.](figures/frequency-floor.png)

::: {.caption}
Figure 6. Log bigram count against mean declarative accuracy, 49 compounds per family. Frequency sets the floor; the vertical spread at similar counts is what it leaves unexplained.
:::

Frequency is the strongest measured predictor in this study, but it is not a complete explanation. Correlations of $\rho$ = 0.52–0.59 are substantial but leave much unexplained: compounds with similar counts follow different trajectories, and the same concept can succeed or fail when the task changes.

One Pythia-2.8B diagnostic makes the framing problem concrete. Asked, `What accessibility attribute is missing from this HTML: <img src='photo.jpg'>?`, the model produces two newlines and starts a new paragraph. Given the cloze prompt, `<img src='photo.jpg'> is missing the attribute`, it produces `alt`. The model, weights, concept, and corpus count are unchanged. Only the answer position changes.

The paired battery extends the point beyond one diagnostic. Across the twelve confirmatory models, 35 model-by-concept cells have a correct declarative response. All 35 fail the violation/conformant evaluative pair for that same concept. The compound and its corpus frequency are fixed; what changes is the form in which the model must use it. This does not isolate one prompt feature—the declarative and evaluative tasks differ in more than wording—but it rules out frequency as a sufficient explanation of whether available knowledge will be reached by a particular task.

The frequency and binding results point in opposite behavioral directions. More frequent compounds are answered more accurately. Less frequent compounds receive stronger late-layer value-weighted writes. The additional interaction does not compensate enough to reverse the accuracy relationship.

To our knowledge, prior work has not reported this inverse relationship between multiword-expression frequency and late-layer, norm-aware constituent interaction across autoregressive model families. What is new here is the combination: frequency predicts which concepts are learned, rarity predicts stronger late interaction, and neither result alone explains whether the model will apply the concept correctly.

Frequency sets a floor. More exposure makes knowledge more likely to appear, but it does not guarantee that the knowledge will be available in the form a task requires. What lies above that floor remains unresolved.
