## Introduction

Give Pythia-12B three prompts of identical shape, and watch it complete them three different ways. An image without alt text is not accessible because "it has no text alternative" — correct, and substantively so. A website without screen reader support is not accessible because "it does not have a text alternative" — fluent, confident, and subtly wrong: screen reader support is not reducible to text alternatives, a conflation most readers outside this domain cannot detect. A long navigation menu without a skip link is not accessible because "of the following error: The page you are trying to reach is not available in the current context" — a fluent 404 template, confidently wrong. Same model, same prompt shape. The difference tracks corpus frequency. Alt text appears 23,306 times as a compound in the model’s training corpus; screen reader, 32,100; skip link, 662. This paper asks what corpus frequency predicts, how far that prediction reaches inside the model, and what it does not explain.
<!-- src: results/logits/pythia-12b_because_generations.csv -->
<!-- src: results/frequency/frequency_table.csv -->

Digital accessibility is an unusually good test domain for these questions, for reasons unrelated to accessibility in particular. Its concepts are concrete enough to code deterministically. The definition of "skip link" is right or wrong by a practitioner's standard, not a matter of taste; the compounds themselves are rare enough in web text to expose frequency effects that broad-capability benchmarks average away. The mechanism under study, however, concerns words and their documentation density; accessibility is where we measured it, not what it is about.

The paper makes five contributions. First, we establish the declarative-evaluative gap behaviorally. Across six Pythia scales and four GPT-2 scales, models that correctly define accessibility concepts fail to apply them. In GPT-2 the gap widens with scale. In Pythia it closes at 12B — but only because declarative knowledge regresses to meet evaluative failure, convergence from the wrong side. Second, we audit this program's own best mechanism candidate and demote it. Sustained late-layer attention binding tracks emergence, but it is a correlate, not a cause. The binding heads are attention sinks and positional structure; the signal is not domain-specific; the most selective head is causally inert. The binding survives intact at the scale where generation collapses. Third, we show corpus frequency predicts the failure structure. Across 49 compounds, Spearman correlations reach 0.57 in Pythia and 0.51 in GPT-2. Both clear the pre-registered threshold of 0.4 and survive confound controls. At the decision point, the correct continuation's rank tracks corpus counts directly. The knowledge is present and outranked, not absent. Fourth, we show the failure is confident. The entropy penalty for wrong domain answers shrinks toward zero with scale. At the largest scales, wrong answers arrive with nearly the confidence of right ones. We state the consequence as a design constraint for any tool built on such models. Fifth, a correction we caught in our own work generalizes into a methods contribution. A common normalization-skipping measurement shortcut severs the one term in the output computation where these models store their frequency prior — a bias vector correlated with corpus frequency at ρ up to 0.78. Autoregressive rollouts through that shortcut fabricate trajectories within seven steps at every scale we tested. The retraction, the pre-registered gate that caught it, and the mechanism behind it are all in the record.

We are equally explicit about what this paper does not claim. Frequency predicts; corpus-level causality requires intervention on training data and is future work. All results are on open-weight base models whose training corpora can be audited; whether the findings survive instruction tuning is unknown. The mechanistic finding is largely negative. Attention binding marks emergence without implementing it, and the failure does not condense into a findable circuit. We document that vacancy with controls at three levels and regard it as informative: the knowledge in this frequency regime behaves like a statistical property of distributed weights, not like localized machinery.

The paper proceeds as interleaved investigations in the order of the contributions above, each stating its method with its result; related work and discussion follow. Every accuracy judgment is produced by deterministic, version-controlled criteria; every threshold in the paper was committed to the repository before its result was computed; and one exhibit that failed those standards is documented rather than absent.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     The three-prompt hook from the suggestion block opens the section; the
     "rank 12" second beat is NOT used in the intro (rank numbers live in §5;
     note the suggestion's rank-12 is the 2.8B value — 12B is rank 14).
     G1 DEBT FLAG: metadata.yaml abstract still asserts the March
     necessary-structural-condition thesis — binding-reframe-draft.md Edit 1
     must be applied to the abstract to match this intro's contribution #2.
     Section numbering in the final paragraph assumes the 06a placement
     decision — update with the renumber. "Twenty-five years" of practice:
     VERIFY the number Trisha wants public (30+ years front-end dev, 5 in
     consulting — the intro currently says 25; her call on the framing). -->

Rewrite the intro

### New sections

01-introduction.md
02-the-gap.md
03-ruling-out-binding.md
04-the-trajectory-taxonomy.md
05-what-predicts-trajectory.md
06-entropy-fluent-wrongness.md
07-related-work.md
08-discussion.md
09-limitations.md
10-references.md
11-colophon.md

### Notes

Results are in the named sections. Each section is "here's what we did and here's what we found." That's a legitimate structure for interpretability papers — interleaved method and result per investigation rather than all methods then all results.

---

What's NOT accounted for yet:

- `docs/cc-extended-gap-analysis.md` — haven't read it, might fit in the gap or discussion
- `docs/results-significance.md` — probably discussion or limitations
- `docs/binding-reframe-draft.md` — probably folds into the binding section [DONE — assembled into 03, Fable pass 2026-07-05]
- `_analysis/Pythia.xlsx` and the visual analysis xlsx — your working spreadsheets
- `results/analysis/emergence_thresholds.csv` — could go in the gap section or trajectory taxonomy


### New work needed before you can write:

- Infini-gram runs (Section 5) [DONE — n=49 campaign complete]
- Token competition traces beyond skip_link (Section 5) [PARTIAL — tangent tables used; keyboard_navigation gap noted in 06 manifest]
- Figures for everything [OPEN]


### SUGGESTION: Opening example from tangent.ipynb

Three evaluative prompts, same structure, same model (Pythia 12B), three completely different failure modes:

- screen_reader (32,100 bigrams): "it does not have a text alternative" — correct
- skip_link (662 bigrams): 404 error page — confidently wrong
- div/onclick (no compound): "not in the same document" — fluently wrong from a different domain

This is the hook. Reader immediately sees the phenomenon and wants to know why. Then: "The answer turns out to be a single number — how often the compound appears in the training corpus."

Could also use the logit ranking at the decision point as a second beat: the correct answer (' users') was right there at rank 12. It didn't win.
