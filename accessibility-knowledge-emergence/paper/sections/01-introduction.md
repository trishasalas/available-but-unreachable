## Introduction

Digital accessibility guidelines represent a narrow, specialized domain in web-scale training data. Terms like WCAG, ARIA, and alt text appear far less frequently than general web vocabulary, and their correct usage requires understanding both syntax and intent. This makes accessibility an unusual test case for studying emergence because the concepts are concrete enough to evaluate and rare enough to show scale sensitivity.

Most emergence research uses broad capability benchmarks like arithmetic, chain-of-thought reasoning, and multilingual translation. These are useful but can be noisy. Accessibility concepts offer something different: a small, well-defined vocabulary with unambiguous answers and direct relevance to real-world tooling decisions.

### Binding Depth and Behavioral Emergence Follow the Same Shape

![Line chart that shows binding depth and behavioral emergence using a
normalized score across the Pythia model suite. Binding depth is
represented with a dark blue solid line and behavioral emergence with a
light blue dashed line. The two lines follow the same shape.](./figures/fig-01-summary.png)

::: caption
Figure 1: Binding depth and behavioral emergence score rise at the same 2.8B parameter threshold across the Pythia model suite. ARIA scores negative at 1B--6.9B reflecting fluent confabulation rather than absence of response.
:::

The findings are specific: accessibility knowledge emerges at 2.8B parameters for core concepts, later or not at all for acronyms, and evaluative capability lags behind declarative knowledge even at maximum scale tested. The declarative-evaluative gap is robust across multiple elicitation strategies and prompt structures, ruling out prompt design as an explanation. Entropy analysis reveals that the gap has internal structure: models enter distinct failure states depending on how they are asked. Attention pattern analysis across all six Pythia scales (160M–12B) shows mechanistic encoding of compound terms before full behavioral competence appears, internal representation that is not reducible to output accuracy. At larger scales, a late-layer resurgence pattern emerges: binding heads re-engage near the output layers, scaling monotonically with model size. Replication across the GPT-2 model suite confirms that the core patterns --- recognition preceding generation, deep-network binding persistence as a correlate of emergence, and the declarative-evaluative gap --- hold across architectures and training corpora.

A preliminary version of these findings appeared as a blog post (Salas, 2026); we present the complete experimental results with extended analysis and cross-architecture replication.
