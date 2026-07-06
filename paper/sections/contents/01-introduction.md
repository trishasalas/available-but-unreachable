## Introduction

Ask Pythia-12B three questions of identical structure and stakes, and watch it fail three different ways. Why is an image without alt text not accessible? "It does not have a text alternative" — correct, and substantively so. Why is a long navigation menu without a skip link not accessible? "Because of the following error: The page you are trying to reach is not available in the current context" — a fluent 404 template, confidently wrong. Why is a div with an onclick handler not accessible? An answer imported wholesale from a different domain. Same model, same prompt shape, same distance from the training distribution's center — except for one number. Alt text appears roughly 23,000 times as a compound in the model's training corpus; screen reader, 32,000; skip link, 662. This paper is about that number: what it predicts, how far the prediction reaches inside the model, and what it does not explain.

Digital accessibility is an unusually good test domain for these questions, for reasons that have nothing to do with accessibility in particular. Its concepts are concrete enough to code deterministically — a definition of "skip link" is right or wrong by a practitioner's standard, not a matter of taste — and rare enough in web text to expose frequency effects that broad-capability benchmarks average away. One author's twenty-five years of professional practice in the domain supplies the evaluation standard directly. The mechanism under study, however, is about words and their documentation density; accessibility is where we measured it, not what it is about.

The paper makes five contributions. First, we establish the declarative-evaluative gap behaviorally: across six Pythia scales and four GPT-2 scales, models that correctly define accessibility concepts fail to apply them, with the gap widening with scale in GPT-2 and, in Pythia, closing at 12B only because declarative knowledge regresses to meet evaluative failure — convergence from the wrong side. Second, we audit this program's own best mechanism candidate and demote it: sustained late-layer attention binding tracks emergence but is a correlate, not a cause — the binding heads are attention sinks and positional structure, the signal is not domain-specific, the most selective head is causally inert, and the binding survives intact at the scale where generation collapses. Third, we show corpus frequency predicts the failure structure: across 49 compounds, Spearman correlations of 0.57 (Pythia) and 0.51 (GPT-2) against a pre-registered threshold of 0.4, surviving confound controls, with the correct continuation's rank at the decision point tracking corpus counts directly — the knowledge is present and outranked, not absent. Fourth, we show the failure is confident: output entropy falls as correctness fails past the emergence threshold, so that the largest models are more certain of wrong domain answers than of right control answers, which we state as a design constraint for any tool built on such models. Fifth, a correction we caught in our own work generalizes into a methods contribution: a common normalization-skipping measurement shortcut severs the one term in the output computation where these models store their frequency prior — a bias vector correlated with corpus frequency at ρ up to 0.78 — and autoregressive rollouts through that shortcut fabricate trajectories within seven steps at every scale we tested. The retraction, the pre-registered gate that caught it, and the mechanism behind it are all in the record.

We are equally explicit about what this paper does not claim. Frequency predicts; corpus-level causality requires intervention on training data and is future work. All results are on open-weight base models whose training corpora can be audited; whether they survive instruction tuning is unknown. And the mechanistic finding is largely negative — attention binding marks emergence without implementing it, and the failure does not condense into a findable circuit — a vacancy we document with controls at three levels and regard as informative: the knowledge in this frequency regime behaves like a statistical property of distributed weights, not like localized machinery.

The paper proceeds as interleaved investigations, each stating its method with its result: the gap (Section 2), the binding audit (Section 3), the trajectory vocabulary (Section 4), the frequency relationship (Section 5), confidence and fluent wrongness (Section 6), the measurement-pathway correction (Section 6a), related work (Section 7), and discussion. Every accuracy judgment is produced by deterministic, version-controlled criteria; every threshold in the paper was committed to the repository before its result was computed; and one exhibit that failed those standards is documented rather than absent.

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
