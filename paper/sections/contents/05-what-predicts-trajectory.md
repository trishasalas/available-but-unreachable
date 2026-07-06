## What Predicts Trajectory — The Frequency Hypothesis

The trajectory taxonomy is descriptive vocabulary; the question that matters is what determines membership. Skip link motivates the hypothesis. Its components are unremarkable English — "skip" and "link" common words alone, but the compound itself is rare: 662 bigram occurrences in The Pile, against 32,100 for screen reader and 23,306 for alt text (Infini-gram, Pile-train index; `results/frequency/frequency_table.csv`). Skip link is also the compound whose behavior degrades at maximum scale in both model families. The hypothesis is that corpus frequency of the compound predicts the trajectory. Concepts documented densely enough climb and stay while rarer concepts peak, regress, or never arrive.

We tested this on all 49 accessibility compounds in the elicitation battery. Compound bigram frequencies were measured with Infini-gram against The Pile — Pythia's training corpus — and correlated against per-compound accuracy from the deterministic coding pipeline (Section 2; `src/accuracy_coding.py`). The analysis was pre-registered with a success threshold of Spearman ρ ≥ 0.4, committed to the repository before any correlation was computed (DECISIONS.md, 2026-07-01 lineage).

Both architectures clear the threshold. Pythia: ρ = 0.5715, p < 0.0001, n = 49. GPT-2: ρ = 0.5052, p = 0.0002, n = 49 (`results/frequency/spearman_summary.csv`). The GPT-2 result carries a caveat worth stating plainly: the frequency measurements are Pile counts, and GPT-2 was trained on WebText, which is not publicly indexed. That the correlation transfers across corpora is consistent with compound-documentation density being a stable property of web text generally rather than an artifact of one corpus — but the GPT-2 correlation is strictly a cross-corpus proxy result, and we label it as such.

Two confounds were tested and dissolved. If the correlation were driven by the frequency of the compound's first word alone (skip, screen, alt as common words), partialling out word1 unigram frequency would collapse it; instead, the Pythia partial ρ rises to 0.5913 and GPT-2 holds at 0.4857. Partialling out compound token count (tokenization length) leaves ρ at 0.5603 and 0.4896 respectively (`results/frequency/spearman_partial.csv`). The association is carried by the compound as a unit, not by its pieces or its tokenization.

A subtlety in the sense analysis is itself evidence of the phenomenon. We attempted to recompute the correlation restricted to responses coded as using the compound's accessibility sense, and for more than 80% of compounds there were too few correct-domain responses across the suite to analyze — the models so rarely produce the accessibility sense that the within-sense correlation is undersampled by construction. On the small subsample where analysis was possible, the Pythia accessibility-sense correlation is ρ = 0.8581 (n = 9, p = 0.003), reported here as descriptive given the sample size; the GPT-2 subsample (n = 6) is uninformative. The scarcity that motivates the paper also bounds this analysis, and we prefer to report that boundary rather than pretend it away.

The correlation is the economics; the decision point is the physics. At the generation step immediately following an evaluative prompt ("...is not accessible because"), the rank of the correct domain token tracks corpus frequency directly: at Pythia 12B, ' alt' sits at rank 4 for the alt text prompt (correct generation follows), ' screen' at rank 2 for screen reader (correct), and ' users' at rank 14 for skip link, where generation collapses into an error-page pattern. Tracked across scale, the skip link domain token's rank traces the peak_regress arc in miniature — rank 12 at 2.8B, rank 7 at 6.9B, rank 14 at 12B — climbing toward the surface at mid-scale and sinking again at maximum scale, in step with the behavioral regression. These rank tables were computed on the model's true output distribution (full forward pass, final normalization applied); we flag measurement pathway explicitly because this paper documents, in Section 7, how easily decision-point rankings are distorted by a common shortcut. The declarative decision point shows the same structure with cleaner stakes: at 6.9B the correct continuation ('displayed') wins the election outright, verified on the true pathway; at 12B it is present at rank 5 but loses to a degenerate self-reference continuation. The knowledge is in the distribution at every scale that has it. What changes with scale — and what frequency predicts — is whether it wins.

Prior work establishes the macro-level relationship: pretraining document frequency predicts factual recall (Kandpal et al., 2023), term frequency predicts few-shot numerical reasoning on this same model suite (Razeghi et al., 2022), and scaling mainly improves recall of popular knowledge while the long tail lags (Mallen et al., 2023). Zhang et al. (2026) formalize the competitive version of this as knowledge overshadowing, a log-linear law at the logit level. Our contribution is resolution and specificity: token-level rank evidence in a specialized professional domain, tied to scaling trajectories per compound, with the frequency measurement taken against the actual training corpus and the accuracy measurement deterministic and re-runnable. They describe the force; this section photographs where it lands.

We are explicit about the strength of the claim: frequency *predicts* trajectory. The correlation survives its pre-registered threshold, its confound controls, and cross-architecture replication, but corpus-level causality is not established here — that requires intervention on training data composition, which is beyond this paper's scope. One interior observation points the same direction and is developed in the Discussion: the frequency ordering measured here in the corpus is echoed, at comparable or greater strength, inside the models' own output machinery.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     NOTE: the "displayed vs click" trace referenced below was RETRACTED
     2026-07-04 (lens-pathway artifact; see DECISIONS D7 verdict + CLAIMS A2).
     The Spearman numbers below are superseded by the n=49 campaign above.
     The tangent.ipynb rank tables survive (true-pathway); camera-ready
     regeneration via src/logit_export.py required per tangent.md
     paste-wound disclosure. -->

*Data we have:*
- `results/mlp_investigation/` — all the decomposition, logit lens, vocab projection, skip_link_steps across every scale in both suites
- `results/analysis/completion_paradox.csv`

*Data you need:*
- Infini-gram frequency counts for each compound and their competitors
- Token competition traces for compounds beyond skip_link (keyboard_navigation at 12B is the priority)

*Figures needed:* the skip_link token competition trace ("displayed" vs "click") [RETRACTED — replace with: true-pathway rank-vs-frequency table across three compounds, and the cross-scale ' users' rank arc], frequency table with trajectory class, and ideally the Spearman result.


### SUGGESTION: This section gets the most new material

The tangent notebook provides the mechanistic illustrations this section was asking for:

**The logit ranking tables.** Three prompts, three frequency levels, same decision point ("because"). The correct domain token's rank maps directly onto corpus frequency:
- alt_text (23,306 bigrams): ' alt' at rank 4 at 12B, correct generation
- screen_reader (32,100 bigrams): ' screen' at rank 2 at 12B, correct generation  
- skip_link (662 bigrams): ' users' at rank 14 at 12B, 404 error

**The cross-scale tracking for skip_link.** ' users' rank across Pythia sizes:
- 2.8B: rank 12, gap 3.8 → tautology
- 6.9B: rank 7, gap 2.7 → "it is not a link"
- 12B: rank 14, gap 4.1 → 404 error

That's peak_regress visible in the token rankings — the domain token climbs at mid-scale and falls back at 12B.

**Cross-architecture convergence.** GPT-2 Medium/Large/XL show the same frequency gradient with different specific wrong answers. Same mechanism, independent model family.

**The Spearman update.** GPT-2 bigram Spearman is r=0.78, p=0.024 (significant). Pythia is r=0.63, p=0.12 (strong trend, underpowered at n=8). Expanding to n=49 with additional accessibility compounds is in progress.

**Literature grounding from the research agent.** Kandpal et al. (2023, ICML), Razeghi et al. (2022, EMNLP), and Mallen et al. (2023, ACL) establish that frequency predicts recall. Your contribution: showing the mechanism at the token level and connecting it to scaling trajectories. They have the economics, you have the physics.

**Data we now have (new):**
- `tangent.ipynb` / `tangent.md` — evaluative generation + logit rankings across 5 models
- `results/frequency/` — frequency table, Spearman summary
- `src/frequency.py` — 225 compounds across 5 domains (49 accessibility for this paper)
