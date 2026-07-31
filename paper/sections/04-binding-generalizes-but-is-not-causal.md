## Binding Generalizes but Is Not Causal

Attention binding is the leading prior candidate for a mechanism underlying the gap. Salas (2026) established the correlation — sustained deep-network binding of accessibility compounds tracks behavioral capability across scale — and this paper's expanded eleven-compound sweep replicates it across four professional domains and a matched control. The same three-tier attention architecture appears in every domain measured. A correlation that clean and that general risks being conflated with causation. It should not be.

The case against the causal reading has five layers: the metric is contaminated by positional and sink structure; the signal is not domain-specific; the most selective single head is causally unnecessary; the earned deep-selective population is jointly unnecessary; and the binding signal survives population-level ablation across domains.

**The top binding heads are not induction heads.** A prefix-matching induction test yields a maximum induction score of 0.02, against the ≥0.5 expected of genuine induction heads. The pairing is not a generic copy mechanism.

**The dominant binder is a previous-token head.** The single strongest binding head (L1/H12) is the top binder for 7 of 11 compounds, yet scores 0.89 on a previous-token diagnostic. Because the second token of a two-token compound is always adjacent to the first, any previous-token head registers as binding every compound. The high score reflects positional adjacency, not representation.

**The late-layer binders are attention sinks and structural heads.** Five of the six late-layer top binders place 55–91% of their attention mass on the beginning-of-sequence token. The remaining late head (L27/H24) attends to the first content position; its apparent binding collapses from 0.98 to 0.006 once a uniform template no longer places the compound's first word at that position. The binding measurement is contaminated in the late layers by sink and positional structure. This caveat plausibly generalizes to other attention-pairing metrics.

**The binding signal is not accessibility-specific.** Measured across five domains, the late heads fire on idiosyncratic cross-domain subsets. L28/H15 attends to "hedge fund" and "stock market"; L30/H29 attends to "skip link" and the weak-collocation control "bicycle wheel." No audited head selects for accessibility. The specializations are lexical, not semantic.

**MLP contribution does not distinguish success from failure.** Late-layer MLP-to-attention contribution ratios are near-identical for compounds the model defines correctly and those it fails (4.437 versus 4.444 at 6.9B). The network spends the same effort either way.

**The most selective head is causally unnecessary.** L29/H7 attends specifically to "screen reader" (reader→screen: 0.90; next compound: 0.21). The selectivity is built through the layers. Yet ablating this head's output shifts the continuation by a KL divergence of 1×10⁻⁵ — effectively zero. Direct logit attribution shows it writes a wrong-sense "screen" direction, promoting projection-and-cinema vocabulary rather than accessibility content. The most screen-reader-specific head in the network is a redundant representation, not a retrieval mechanism.

**The earned deep-selective population is jointly unnecessary.** For screen reader, the earned set consists of two heads: L29/H7 and L27/H10. Jointly ablating both shifts the output by a KL divergence of 2.2×10⁻⁵, indistinguishable from the single-head null. A three-compound robustness panel repeats the design — alt text and stock market each earn compound-specific three-head sets with zero overlap. Every joint ablation lands at least a factor of 35 below the pre-registered 0.01-nat bar. No earned set is causally necessary.

Two results address the remaining alternatives. First, population redundancy: under population ablation across four domains, removing the strongest binding heads moves mean binding by approximately 1%, because compensator heads absorb the loss. The architecture is demonstrably present, demonstrably general, and demonstrably redundant. Second, the dissociation: at Pythia-12B, generation of the skip link compound collapses into a degenerate loop while the binding signal remains intact — peak binding 0.978, at the same early layer as every smaller scale. Whatever fails at 12B fails downstream of attention.

The late-layer binding signal is real, general, and scale-correlated. It is also mechanistically mundane: positional adjacency, attention-sink structure, redundant representation. Remove the heads we tested and the outputs do not change. Attention binding marks emergence. Nothing we ablated is necessary to it.

The sole late-layer head exhibiting binding resurgence at Pythia-12B is sink-dominated (mean BOS attention 0.96), indicating that the late-layer signal reflects attention-sink behavior rather than renewed semantic selectivity.
