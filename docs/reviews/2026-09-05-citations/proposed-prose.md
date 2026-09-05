# Citation and lineage revisions — approved and applied 2026-09-05

## Related Work: replace the paragraph beginning “That question requires more than raw attention” with these two paragraphs

Attention weights alone are an incomplete account of a model’s use of information. Jain and Wallace (2019) and Serrano and Smith (2019) show that attention magnitude can mislead as an indicator of importance. Kobayashi et al. (2020) incorporate the norm of transformed value vectors, while Ferrando et al. (2022) account for residual connections and layer normalization when aggregating token interactions. Head-pruning results also show that removing individual heads need not impair performance (Michel et al., 2019). We therefore distinguish raw attention, value-weighted writes, and the effects of intervention. Prior work on compounds and multiword expressions further motivates examining where these interactions occur across depth (Miletić & Schulte im Walde, 2023, 2024; Vig & Belinkov, 2019).

Salas’s January 2026 report examined accessibility definitions, evaluative failures, and attention between compound constituents. A subsequent preprint developed the analysis of binding across depth and the declarative-evaluative gap (Salas, 2026). Tran (2026) studies checkpoint dynamics and head ablations using EB*, which takes the maximum across layers of the strongest head’s within-term attention above its layer mean. The value-weighted measure used here includes projected value-vector magnitude and target residual normalization.

Citation placement: the January report uses `salas2026testing`; the subsequent preprint uses `salas2026emergence`; Tran uses `tran2026attention`. Use bibliography-generated year suffixes. All references to prior work are third-person; none identifies an author of this submission.

## Introduction: insert before the final paragraph

The study combines a frozen same-concept violation/conformant validation, corpus-frequency analyses across three model families, and late-layer binding measurements that include value-write magnitude and residual normalization. A registered held-out intervention tests whether removing frequency-selected heads perturbs rarer compounds more strongly. These analyses distinguish the relationship between frequency and declarative accuracy from success on application tasks.

Prior-work attribution is established in Related Work; this paragraph states the present study’s contribution without repeating author names or implying that it extends Tran’s method.

## Frequency section: replace the paragraph beginning “To our knowledge”

The contribution is the joint test of corpus frequency, late-layer value-weighted binding, and same-concept application failure across model families. Corpus frequency predicts declarative accuracy, while rarity predicts stronger late value-weighted writes. The paired battery shows that correct definitions do not ensure success on the tested application pairs. The registered Pythia-2.8B ablation did not support the predicted greater perturbation for rarer compounds.

This replaces the broad priority claim with the specific combination established in this paper. Prior-work citations remain in Related Work.

## Anonymity and application notes

- This revision supersedes the longer proposed lineage paragraph and removes repeated Tran citations from the proposed Introduction and Frequency paragraphs. It does not remove the relevant citation from Related Work.
- The methodological-support paragraph above remains part of the pending proposal.
- Do not use first-person links to prior work, personal communications, acknowledgments, or professional-biography details to establish attribution.
- Cite the two public Salas works as separate third-party sources. Their bibliography year suffixes are generated automatically.
- The current submission and its supplement must not link to a named version of this manuscript. Prior-work citations and submission-artifact links require separate inspection at packaging time.
- Official sources checked 2026-09-05: https://jmlr.org/tmlr/author-guide.html and https://jmlr.org/tmlr/faq.html . TMLR requires anonymous submissions and supplements, permits public preprints, and prohibits linking the submission to a named version of itself. These pages do not provide an explicit self-citation syntax rule; third-person citation is the implementation chosen here to avoid identifying the submitting author.
- Approved by the author and applied on 2026-09-05. Retained as the reviewed wording record; `paper/` remains authoritative.
