## References

*Working reference list — organized by relevance to paper claims.*


### Measurement pathways and the lens family (C6 / D8)

These establish that the lens family has reliability and frequency-directional problems. Our contribution: the severance chain — in bias-free architectures the frequency prior relocates into ln_final β (b_U only under folding); the ubiquitous resid @ W_U shortcut severs it; autoregressive shortcut rollouts exit the true trajectory within ≤7 steps at all six Pythia scales, directionally against frequent tokens (6/6 flips), producing our retracted A2 exhibit — caught by a pre-registered gate.

- **nostalgebraist (2020)** "interpreting GPT: the logit lens." LessWrong. The origin of the method; caveats about intermediate-layer decoding present from day one. https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens

- **Belrose et al. (2023)** "Eliciting Latent Predictions from Transformers with the Tuned Lens." Nora Belrose, Zach Furman, Logan Smith, Danny Halawi, Igor Ostrovsky, Lev McKinney, Stella Biderman, Jacob Steinhardt. Documents logit lens as unreliable and systematically biased toward some vocabulary items (their Fig. 3, KL-based); rogue high-variance dimensions as a lens hazard. They measured the bias's existence; C6 names its structure and its rollout casualty. https://arxiv.org/abs/2303.08112

- **Gupta et al. (2025)** "How Do LLMs Use Their Depth?" Akshat Gupta, Jay Yeung, Gopala Anumanchipalli, Anna Ivanova. Guess-then-Refine: early layers propose high-frequency tokens (Pythia-6.9B among test models), refined >70% of the time by depth. MUST CITE AND DISTINGUISH: their Appendix D shows LogitLens (norm applied) underestimates probability mass of high-frequency tokens at EARLY layers, and their probe-bias controls conclude early-layer frequency dominance is real information content. Different layer regime (intermediate vs. our final-layer shortcut), different variant (norm applied vs. skipped), different consequence (readout fidelity vs. rollout fabrication) — same wounded channel: frequency. https://arxiv.org/abs/2510.18871

- **Kobayashi et al. (2023, Findings of ACL)** "Transformer language models handle word frequency in prediction head." Goro Kobayashi, Tatsuki Kuribayashi, Sho Yokoi, Kentaro Inui. pp. 4523–4535 (per Cho et al.'s bibliography; verify against the ACL Anthology before camera-ready). THE prior art for D8-H1's geometry: LM-head bias correlates with output token probability/frequency; removing it diversifies generation. D8's residual novelty: Pythia has NO head bias — the prior relocates into ln_final β, visible as b_U only after folding, severed by the naked shortcut. Replication + relocation + casualty, not discovery.

- **Cho et al. (2024)** "Understanding Token Probability Encoding in Output Embeddings." Hakaze Cho, Yoshihiro Sakai, Kenshiro Tanaka, Mariko Kato, Naoya Inoue (JAIST/RIKEN). Extends Kobayashi from the bias term to the embedding matrix: output probabilities encoded log-linearly in a common, sparse direction of output embeddings; causally steerable up to 20×; frequency encoding emerges at very early Pythia training steps, before visible convergence. Adjacent prior art for D8-H2 (colsum side). https://arxiv.org/abs/2406.01468

- **Timkey & van Schijndel (2021, EMNLP)** "All Bark and No Bite: Rogue Dimensions in Transformer Language Models Obscure Representational Quality." pp. 4527–4546. Rogue dimensions dominate similarity measures; type/position-specific activation. The measurement-distortion genre C1/C6 belong to.

- **Gao et al. (2019, ICLR)** "Representation Degeneration Problem in Training Natural Language Generation Models." Jun Gao, Di He, Xu Tan, Tao Qin, Liwei Wang, Tie-Yan Liu. Root of the frequency-geometry literature: embeddings degenerate into a narrow anisotropic cone shaped by token frequency. (Cho et al.'s bibliography dates this 2018; accepted venue is ICLR 2019 — verify against OpenReview before camera-ready.)

<!-- TODO (writing pass): verify authors for Puccetti et al. (2022, Findings of EMNLP?) "Outlier Dimensions that Disrupt Transformers Are Driven by Frequency" arXiv:2205.11380 before adding — links outlier params to token frequency AND model performance; shelf-one support. Do not add unverified. -->


### Frequency predicts factual recall (corpus-auditing studies)

These establish the macro-level relationship. Our contribution: token-level resolution and scaling trajectory prediction.

- **Kandpal et al. (2023, ICML)** "Large Language Models Struggle to Learn Long-Tail Knowledge." Direct causal link between pretraining document frequency and QA accuracy. BLOOM-176B accuracy jumps from 25% to 55% as relevant documents increase from 10¹ to 10⁴. Entity-linking pipeline across ROOTS (1.6T tokens). The foundational corpus-auditing paper.

- **Razeghi et al. (2022, EMNLP)** "Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning." Extends frequency effect beyond entity recall into structured reasoning on Pythia models. Phase change at 65,000 training steps (45% through training) where models ≥2.8B start showing frequency-accuracy correlation. Directly relevant: uses Pythia suite and The Pile.

- **Mallen et al. (2023, ACL)** "When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories." PopQA benchmark: 14,000 questions stratified by Wikipedia popularity. Scaling from 6B to 175B yields only 4pp accuracy gain on tail knowledge. "Scaling mainly improves memorization of popular knowledge." Directly supports our peak_regress finding.


### Frequency bias in language models

These establish that frequency bias exists. Our contribution: connecting it to scaling trajectories and domain knowledge emergence.

- **Giulianelli et al. (2024)** "Mitigating Frequency Bias and Anisotropy in Language Model Pre-Training with Syntactic Smoothing." Show that models favor higher-frequency tokens in grammaticality judgments (BLiMP). Frequency bias is quantified but not connected to domain knowledge or scaling. https://arxiv.org/pdf/2410.11462

- **Chen et al. (2025)** "LLMs are Frequency Pattern Learners in Natural Language Inference." Demonstrate that fine-tuned LLMs exploit frequency bias during inference, and fine-tuning amplifies reliance on it. https://arxiv.org/html/2505.21011v1

- **Yuan et al. (2025)** "Incorporating Domain Knowledge into Materials Tokenization." Frequency-centric tokenization misrepresents low-frequency domain terms in materials science — same structural problem, different domain. https://arxiv.org/pdf/2506.11115


### Competition of mechanisms / factual recall

Closest to our mechanistic story. Zhang et al. proposes knowledge overshadowing as a log-linear law; we provide token-level resolution and trajectory prediction.

- **Ortu et al. (2024)** "Competition of Mechanisms: Tracing How Language Models Handle Facts and Counterfactuals." Find that pre-training frequency affects factual recall ability. Localize information flow at attention map level. Broader prompt set than prior work. Key difference from ours: they study factual recall in controlled settings, not domain knowledge emergence across scale. https://arxiv.org/html/2402.11655v1

- **Zhang et al. (2026, ACL)** "Law of Knowledge Overshadowing." Dominant knowledge suppresses less prevalent knowledge at the logit level; hallucination rate follows a log-linear law with frequency, length, and model size. Model size makes overshadowing *worse*. Proposed CoDA (contrastive decoding) as a fix. Our closest neighbor — they describe the force; we photograph the collision. Their law is behavioral; we show the specific tokens competing, at which ranks, at which scales. Held for Paper 2 (INTERCEPT): their two-stage training → rote memorization finding motivates OLMo intervention.

- **SPARK — Jain et al. (2026)** "Security Knowledge Priming and Representation-Guided Knowledge Activation for LLM-based Secure Code Generation." Key finding: "without an explicit and brief cue, statistical pressure toward common training-distribution patterns suppresses the model's safety-relevant representations." Nearly identical thesis to ours, applied to security. They solve it with inference-time steering; we diagnose the mechanism. https://arxiv.org/pdf/2606.16244


### Internal knowledge vs. output behavior (the gap)

These confirm that models know more than they show. Our contribution: explaining *why* via frequency competition, not just documenting the gap.

- **Patel et al. (2026)** "Interpretability without Actionability: Mechanistic Methods Cannot Correct Language Model Errors Despite Near-Perfect Internal Representations." Linear probes show 98.2% AUROC on hazard detection while output behavior is 53 points worse. Steering methods correct only a minority of errors. Direct evidence for declarative-evaluative dissociation. https://arxiv.org/pdf/2603.18353

- **Berglund et al. (2024, ICLR)** "The Reversal Curse: LLMs trained on 'A is B' fail to learn 'B is A'." Directionally encoded storage — models trained on "A is B" cannot retrieve "B is A". Frequency of ordering in training data determines which direction works. Connects the gap to corpus frequency and training data structure. Complementary to our finding: they show directional encoding breaks retrieval; we show frequency competition blocks output.

- **Chuang et al. (2024, ICLR)** "DoLa: Decoding by Contrasting Layers Improves Factuality." Contrasts early-layer distributions (high-frequency, generic) against late-layer distributions (factual) to amplify correct signal. 12-17pp improvement on TruthfulQA. Mechanistic evidence that early layers are frequency-dominated and late layers add factual content — exactly the layer-by-layer dynamic we observe. Intervention validates our diagnosis.

- **Press & Wolf (2017)** "Using the Output Embedding to Improve Language Models" / **Chen et al. (2026)** "Weight Tying Biases Token Embeddings Towards the Output Space." Weight tying optimizes embeddings for output prediction, compromising input representation. Mechanistic evidence for why late layers favor frequency. https://arxiv.org/pdf/2603.26663


### AI for accessibility testing

Establishes the applied context. Nobody in this space is asking the mechanistic question.

- **Fuglerud et al. (2024)** "Exploring the Use of AI for Enhanced Accessibility Testing of Web Solutions." Four prototypes using open-source ML for WCAG testing (CLIP for alt text, OCR for images of text, NLP for language detection). AI as black-box tool, no interrogation of internal representations. doi:10.3233/SHTI241041

- **López-Gil & Pereira (2024)** "Turning manual web accessibility success criteria into automatic: an LLM-based approach." LLM-based scripts for 1.1.1, 2.4.4, 3.1.2. Found LLMs catch issues WCAG checkers miss. Called for replication with open-source models. doi:10.1007/s10209-024-01108-z


### Mechanistic interpretability methods

- **nostalgebraist (2020)** "The logit lens." Projects intermediate layer representations through the unembedding matrix to track how predictions evolve across layers. Core method we use.

- **Elhage et al. (2021)** "A Mathematical Framework for Transformer Circuits." Foundation for residual stream analysis.

- **Geva et al. (2021, EMNLP)** "Transformer Feed-Forward Layers Are Key-Value Memories." FFN layers operate as key-value stores where keys correlate with textual patterns and values promote distributions over vocabulary. Foundational for understanding how factual knowledge is stored.

- **Geva et al. (2023, EMNLP)** "Dissecting Recall of Factual Associations in Auto-Regressive Language Models." Three-step factual recall circuit: (1) MLP enrichment of subject, (2) relation propagation, (3) attention-based attribute extraction. Failure can occur at any step. Important for our story: we show the failure happens *after* all three steps succeed — at the output layer competition.

- **Meng et al. (2022, NeurIPS)** "Locating and Editing Factual Associations in GPT (ROME)." Causal mediation shows mid-layer MLPs are decisive for factual predictions. Establishes directional asymmetry in weight encoding — the architectural explanation for the Reversal Curse.

- **Olsson et al. (2022)** "In-context Learning and Induction Heads." Characterizes induction heads. Our blind study falsified the induction head hypothesis for accessibility binding — top binding heads scored 0.00–0.12 on induction diagnostic.

- **Nanda et al. (2023)** "Indirect Object Identification (IOI)." The tutorial where substituting an accessibility sentence started this whole program.


### Scaling and emergence

- **Zhang et al. (May 2026)** Two-stage training → rote memorization; mixed-format training → representation consistency. Held for Paper 2 (INTERCEPT/OLMo). Provides mechanistic vocabulary for the training data composition story.


### Attention binding (ruled out as causal)

- **Salas (2026)** "Accessibility Concept Emergence in the Pythia Suite: Thresholds, Binding, and the Declarative-Evaluative Gap." Zenodo. doi:10.5281/zenodo.20360787. Paper 1 of this program. Established the binding-emergence correlation this paper audits (§3) and first characterized the declarative-evaluative gap this paper generalizes (§2). ANONYMITY RULE (TMLR double-blind): cite in third person throughout submission prose — "Salas (2026) established" — never "our previous work" / "Paper 1" / "this program's." Reference itself stays unblinded per standard double-blind convention.

- **Dung Tran (TMLR)** Related attention-binding work. Characterized our mechanistic work as "behavioral." Their EB* metric likely carries the same previous-token head confound we identified. Publication confirmed the venue is open for our submission.


---
*TODO: Get full citation details (volume, pages, DOIs) for arxiv papers before submission.*