## The Gap

Accessibility knowledge is present in the residual stream but fails to surface in behavior. Two model families (Pythia, GPT-2), same pattern. Models can define "skip link" but can't apply the concept. Establish the phenomenon behaviorally with the elicitation data across scales.

---

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