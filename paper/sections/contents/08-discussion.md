## Discussion

- Frequency as falsifiable prediction (Paper 2 can test it quantitatively)
- Temporal/unlearning trajectory → explicit Paper 2 hook
- Accessibility as test domain but the mechanism is about words, not about accessibility


### SUGGESTION: New discussion points from today

**"Accessibility as test domain" now has teeth.** The research agent synthesis established that frequency-recall correlation is well-documented across factual QA (Kandpal), numerical reasoning (Razeghi), and popularity-stratified knowledge (Mallen). Your contribution isn't "frequency matters" — it's the mechanistic resolution. Frame the discussion as: prior work established the macro-economics; this paper provides the micro-physics. They counted documents; you tracked tokens through layers.

**The practical implication.** The tangent data showed that 12B produces a *worse* answer than 2.8B for skip_link. This has a direct practical consequence: for specialized domains with low corpus frequency, smaller models may outperform larger ones. This connects to PubMedBERT (Gu et al., 2021) showing domain-specialized small models beating larger general models. Don't overstate this — note it as a hypothesis for future work (Paper 2 / INTERCEPT).

**The training data quality angle (for discussion, not claims).** You noted last night that the internet is mostly inaccessible — so the training data isn't just low-frequency for accessibility, it's actively skewed toward bad practices. This is the "anti-causal contamination" gap identified in the research agent synthesis. Mention it as a direction, not a finding.

**Cross-domain generalization.** You built 225 compounds across five domains. The frequency data is there even if the trajectories aren't (yet). Note in the discussion that the mechanism predicts the same pattern should hold for legal, medical, and financial domain knowledge — and the infrastructure to test it exists.