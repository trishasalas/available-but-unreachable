## Related Work

Our work sits at the intersection of three literatures that rarely cite each other, plus a fourth this paper's correction obligates us to join.

**Frequency and capability.** That training-data frequency predicts model capability is established at the macro level. Kandpal et al. (2023) link pretraining document frequency to factual QA accuracy directly; Razeghi et al. (2022) extend the effect to few-shot numerical reasoning on the same Pythia suite used here; Mallen et al. (2023) show scaling mainly improves recall of popular knowledge while the long tail lags. Closer to the behavioral surface, Giulianelli et al. (2024) quantify a preference for high-frequency tokens in grammaticality judgments, and Chen et al. (2025) show fine-tuning amplifies reliance on frequency patterns in inference tasks. Zhang et al. (2026) formalize the competitive framing as knowledge overshadowing, a log-linear law relating hallucination to relative knowledge frequency, with model scale worsening the effect. These studies establish the economics of frequency at the document and benchmark level; our contribution is token-level resolution in a specialized professional domain, with frequency measured against the actual training corpus, tied to per-concept scaling trajectories, and carried through pre-registered thresholds.

**Knowledge that exceeds behavior.** A separate line documents that models internally encode more than they output. Probing studies recover knowledge from hidden states that generation fails to surface, and Jain et al. (2026) describe the production-side failure in security code generation as statistical pressure toward common training-distribution patterns suppressing task-relevant representations — nearly our thesis, in a neighboring domain, addressed there with inference-time steering. Our decision-point results give this gap a concrete face: the correct continuation is present in the output distribution at every scale that has the knowledge, at a rank corpus frequency predicts, and the failure is losing the final election rather than lacking a candidate.

**Accessibility and AI.** The accessibility literature's engagement with machine learning is overwhelmingly tool-focused — whether automated systems can detect accessibility failures — and the answer to date is partial coverage requiring human judgment. To our knowledge, no prior work has asked what language models know about accessibility, at what scale that knowledge arrives, or by what mechanism it fails to surface; this paper treats accessibility as a test domain precisely because its concepts are concrete enough to code deterministically and rare enough to expose frequency effects, and because one author's professional practice supplies the evaluation standard that a benchmark would otherwise approximate.

**Measurement pathways.** The correction in Section 6a joins an existing literature on lens reliability. The logit lens (nostalgebraist, 2020) is known to be unreliable on several model families, and Belrose et al. (2023) document it as systematically biased toward some vocabulary items, motivating the learned tuned lens; Gupta et al. (2025) show lens readouts underestimate high-frequency token probability at early layers and carefully separate probe bias from representation content in that regime. On the storage side, Kobayashi et al. (2023) establish that prediction-head bias terms encode word frequency in models that have them, and Cho et al. (2024) locate a causally steerable frequency direction in output embeddings, emerging early in training on this same model family. Our contribution connects the two shelves: in bias-free architectures the frequency prior relocates into the folded normalization bias, the ubiquitous normalization-skipping shortcut severs exactly that term, and the consequence — directional, compounding fabrication in autoregressive rollouts — is measured at six scales and caught, in our own work, by a pre-registered gate. The geometry was known; the casualty was not.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     The three-literature framing from the suggestion block is used and a fourth
     (measurement pathways) added per this weekend's findings. Patel et al.
     (probing) referenced generically as "probing studies" — verify/attach the
     specific citation from 10-references.md before camera-ready or keep generic.
     Fuglerud / López-Gil (accessibility-AI) not named in prose pending
     metadata verification — "tool-focused" characterization stands either way.
     Zhang et al. 2026 here is Yuji Zhang (overshadowing, arXiv 2502.16143) —
     NOT the fact-recall Zhang, which remains out of this paper by decree. -->


### SUGGESTION: Related work framing

This section should be restructured as proper related work rather than an appendix. The reference list in 10-references.md provides the organized source material. The narrative should establish three things:

1. **Frequency bias is well-documented** (Giulianelli, Chen, Kandpal, Razeghi, Mallen). Prior work establishes that models favor high-frequency tokens and that training data frequency predicts factual recall. These studies operate at the behavioral/benchmark level.

2. **Internal knowledge can exceed output behavior** (Patel et al., SPARK). Linear probes show models encode knowledge they don't output. SPARK calls it "statistical pressure toward common training-distribution patterns." These studies document the gap but don't explain the mechanism at the token level.

3. **AI for accessibility is tool-focused** (Fuglerud, López-Gil). The field asks "can AI test for accessibility" not "what does AI know about accessibility and how." Nobody has examined accessibility knowledge mechanistically.

Your paper sits at the intersection: you take the documented frequency effect, show the documented internal-vs-output gap, and connect them mechanistically in a domain nobody else is examining at this level.
