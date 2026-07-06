## The Gap

The phenomenon this paper investigates is a dissociation between knowing and applying. A model that correctly defines an accessibility concept when asked directly can fail completely when asked to use that same concept to evaluate a situation — and the two failures scale differently. We call the difference between declarative accuracy (define the concept) and evaluative accuracy (apply it to a case) the declarative-evaluative gap, and this section establishes it behaviorally across both model families before the rest of the paper asks what drives it.

The measurement is the elicitation battery described in Methods: matched declarative, evaluative, and completion prompts per concept, across six Pythia scales (160M–12B) and four GPT-2 scales (117M–1.5B). Responses are coded by the deterministic, version-controlled criteria of src/accuracy_coding.py. Zero of 510 responses went uncoded, and every criteria change is gated through the decision log. Accuracy by prompt type and scale is in results/analysis/accuracy_by_prompt_type.csv and the gap series in `pythia_gap.csv` and `gpt2_gap.csv`.

The gap is real in both architectures and behaves differently in each. In GPT-2, it widens with scale, reaching 50 points at 1.5B. Declarative knowledge accumulates faster than the ability to deploy it, and the largest model in the family knows the most while applying it proportionally least. In Pythia, the gap persists at every scale with one exception, and the exception is the finding. At 12B, the gap closes, but from the wrong side. Declarative accuracy regresses to meet evaluative accuracy rather than evaluative rising to meet declarative. The model does not learn to apply what it knows; it partially loses the ability to state what it knew. Convergence by decay is not mastery, and treating a shrinking gap as progress would misread the suite's largest model as its most balanced.

One generation pair makes the abstraction concrete. Pythia-2.8B, asked declaratively, defines the concept correctly: "A skip link is a link that is used to skip a section of a web page." The same model, asked why a long navigation menu without a skip link is not accessible, answers: "because the skip link is not present." Both sentences are fluent; both use the vocabulary; only one contains the concept doing work. The evaluative answer is a tautology — the words arranged in the shape of a reason, with the reasoning absent. This is what the gap looks like from inside a single model at a single scale: not ignorance, but knowledge that does not survive the trip from definition to use. (Generation quotes from the evaluative battery, true output pathway; regenerated mechanically for camera-ready per Methods.)

The gap also has an internal structure that the accuracy numbers alone do not show. Models enter distinct failure states depending on how they are asked, from high-entropy stalling at small scales to low-entropy confident parroting at large ones. The character of evaluative failure changes systematically along a concept's scaling trajectory. Those two structures are the subjects of the next two sections: first the shapes the trajectories take, then what a single corpus statistic predicts about which concepts take which shape.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     The 2.8B declarative/evaluative pair from the suggestion block is used as
     the section's concrete illustration; regeneration-for-camera-ready note
     attached per tangent.md provenance. The 12B "gap closes via declarative
     regression" beat is drawn from CLAIMS A1. -->

*Data we have:*
- `results/analysis/per_concept_scaling.csv` — declarative scores by concept and scale, both suites
- `results/analysis/pythia_gap.csv`, `gpt2_gap.csv` — the gap itself
- `results/analysis/accuracy_by_prompt_type.csv`
- `results/analysis/elicitation_coded.csv`
- All the raw `*-results.csv` files in `results/pythia/` and `results/gpt2/`

*Figures needed:* scaling curves per concept showing declarative vs evaluative divergence. The gap visualized.


### SUGGESTION: The tangent notebook examples strengthen this section

The declarative-evaluative gap is abstract when stated as accuracy scores. The evaluative prompts from tangent.ipynb make it visceral:

- Pythia 2.8B can define "A skip link is a link that is used to skip a section of a web page" (correct, declarative)
- Same model, evaluative: "A long navigation menu without a skip link is not accessible because the skip link is not present" (tautology — knows the words, can't reason about them)

Consider adding one concrete generation pair per concept to illustrate the gap alongside the accuracy curves. The reader should see what the gap *looks like*, not just what it measures.
