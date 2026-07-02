## References

*Working reference list — organized by relevance to paper claims.*


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

- **Dung Tran (TMLR)** Related attention-binding work. Characterized our mechanistic work as "behavioral." Their EB* metric likely carries the same previous-token head confound we identified. Publication confirmed the venue is open for our submission.


---
*TODO: Get full citation details (volume, pages, DOIs) for arxiv papers before submission.*