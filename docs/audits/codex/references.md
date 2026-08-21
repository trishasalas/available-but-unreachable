# References

- [Voita et al. (2019), “Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned”](https://aclanthology.org/P19-1580/). 
They identify attention heads specialized for rare words. That gives you published evidence for the missing conceptual step:

### Papers I would definitely cite

- [Kandpal et al. (2023), “Large Language Models Struggle to Learn Long-Tail Knowledge”](https://proceedings.mlr.press/v202/kandpal23a.html)  
  Establishes the frequency → behavioral accuracy side: factual performance is strongly related to the amount of relevant pretraining evidence.

- [Kobayashi et al. (2023), “Transformer Language Models Handle Word Frequency in Prediction Head”](https://aclanthology.org/2023.findings-acl.276/)  
  Shows that corpus frequency is encoded directly in the prediction machinery. This supports treating frequency as a mechanistic variable rather than merely a dataset covariate.

- [Miletić and Schulte im Walde (2023), “A Systematic Search for Compound Semantics in Pretrained BERT Architectures”](https://aclanthology.org/2023.eacl-main.110/)  
  Especially relevant to your stimuli. They find that frequency affects compound representations and that compositional information is concentrated mostly in earlier layers.

- [Miletić and Schulte im Walde (2024), “Semantics of Multiword Expressions in Transformer-Based Models: A Survey”](https://aclanthology.org/2024.tacl-1.33/)  
  The best broad citation for framing compounds as multiword expressions. The survey concludes that MWE processing is inconsistent and often depends on surface patterns or memorized information.

- [Vig and Belinkov (2019), “Analyzing the Structure of Attention in a Transformer Language Model”](https://aclanthology.org/W19-4808/)  
  Provides precedent for interpreting attention by depth in GPT-2, including differences between local, syntactic, and longer-distance behavior across layers.

### Methodological papers that now matter a lot

- [Kobayashi et al. (2020), “Attention is Not Only a Weight”](https://aclanthology.org/2020.emnlp-main.574/)  
  This is the most important follow-up for your analysis. Raw attention weights do not necessarily measure actual token contribution because the transformed value-vector norms also matter. Crucially, they report frequency-related regulation through those norms.

- [Ferrando et al. (2022), “Measuring the Mixing of Contextual Information in the Transformer”](https://aclanthology.org/2022.emnlp-main.595/)  
  Introduces ALTI, which incorporates attention, value transformations, residual connections, and layer normalization. Repeating the frequency analysis with ALTI or a similar contribution measure would make the mechanistic claim much stronger.

- [Jain and Wallace (2019), “Attention is not Explanation”](https://aclanthology.org/N19-1357/)  
  The standard caution against equating attention weights with causal importance.

- [Michel et al. (2019), “Are Sixteen Heads Really Better than One?”](https://papers.neurips.cc/paper_files/paper/2019/hash/2c601ad9d2ff9bc8b282670cdd54f69f-Abstract.html)  
  Motivates head ablation: many heads can be removed harmlessly, so the heads carrying the rarity effect should be tested for causal necessity.

### Useful adjacent work

[Merullo, Wiegreffe, and Elazar (2024), “The Mutual Relationship between Corpus Frequency and Linear Representations in Language Models”](https://neurips.cc/virtual/2024/105361) directly connects corpus frequency to the formation and robustness of factual representations. It is highly relevant conceptually, though it was presented at a NeurIPS workshop rather than the main conference.

[Oh et al. (2024), “Frequency Explains the Inverse Correlation of Large Language Models’ Size, Training Data Amount, and Surprisal’s Fit to Reading Times”](https://aclanthology.org/2024.eacl-long.162/) is useful if you discuss rare expressions as requiring different contextual processing.

A defensible related-work synthesis would be:

> Prior work has separately shown that exposure frequency predicts language-model knowledge, that some attention heads specialize in rare tokens, and that frequency influences representations of compound expressions. Our results connect these strands: across model families and scales, rarer compounds elicit stronger late-layer cross-token attention despite being answered less accurately.

The strongest novelty claim is therefore not “frequency matters” or “rare tokens receive distinctive attention.” It is the conjunction:

> Compound-level corpus rarity predicts increased late-layer binding across decoder-only language models, and this same frequency dependence explains much of the apparent relationship between late binding and behavioral failure.

Before leaning heavily on “binding,” I would rerun the analysis using value-weighted attention or ALTI. If the inverse-frequency pattern survives that test, the bridge becomes considerably harder to dismiss as an artifact of normalized attention weights.