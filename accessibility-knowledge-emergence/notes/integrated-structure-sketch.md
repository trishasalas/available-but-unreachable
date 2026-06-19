# Integrated Structure Sketch

This maps where each piece of Extended Analysis content should land in the existing paper, what changes in each section, and what stays the same. Sections marked **[unchanged]** don't need editing. Sections marked **[expand]** get new material folded in. Sections marked **[revise]** need rewriting to absorb new scope.

---

## Abstract **[revise]**

Current abstract mentions Pythia 160M–6.9B. Now the binding analysis extends to 12B — that's a headline addition. Also: the gap is now validated across 15 prompt types, not just the original set. And entropy analysis provides the first quantitative evidence that the gap has internal structure.

**Add:**

- "...extended to Pythia 12B" in the model range
- Mention elicitation robustness (gap persists across multiple prompt strategies)
- One sentence on entropy signatures showing structured failure, not uniform failure
- Late-layer resurgence as a new binding observation

---

## Introduction **[light touch]**

Add one sentence acknowledging the expanded scope — something like "We further test the robustness of the evaluative gap across multiple elicitation strategies and extend the binding analysis to Pythia 12B."

The figure caption for Figure 1 (binding depth / emergence chart) should note that 12B data is now included, or flag that an updated figure follows later.

---

## Related Work **[unchanged]**

Nothing new to add here unless you want to cite entropy-based interpretability work. Optional, not necessary.

---

## Methodology — Models **[expand]**

**Add Pythia 12B** to the model list. Note its architecture (36 layers, 32 heads — check exact specs from your Appendix B). One sentence: "12B was added to extend the binding analysis beyond the original suite."

---

## Methodology — Experiments **[expand]**

After the existing Experiment 1–4 descriptions, add a new subsection:

### Experiment 5: Elicitation Robustness

Brief description of the expanded prompt battery. Three categories:

- Completion tasks (few-shot structural, bare completion) — 2 strategies × 4 concepts + controls
- Hypothesis-driven evaluation (direct question, error correction, Socratic) — 3 strategies
- Validation prompts (direct completion, instructional correction, functional Socratic, confabulation controls)

State that testing was limited to 1B and 2.8B, the two scales where the gap was originally observed. Reference Appendix C for full prompt list.

### Experiment 6: Entropy Analysis

One paragraph. Mean and last-token entropy computed on hypothesis-driven prompts for 1B and 2.8B. Explain what entropy measures here (model uncertainty/confidence at the point of generation).

Note: the 12B binding extension isn't a new experiment — it's an extension of Experiment 4 using the same methodology. It goes in the Results under Experiment 4, not as a separate experiment.

---

## Results — Experiment 1: Declarative Knowledge **[unchanged]**

No new data here.

---

## Results — Experiment 2: Evaluative Knowledge **[expand — this is where the biggest payoff is]**

The existing section ends with the gap observation and GPT-2 replication. This is where the new elicitation work lands, because it directly answers the question "is this gap real or an artifact?"

### After existing Experiment 2 results, add:

**Elicitation Robustness**

The completion tasks first. 2.8B completes every accessibility concept correctly (except bare closed captions). 1B struggles broadly. Controls pass on both models. This re-establishes the declarative knowledge is present.

Then the hypothesis-driven evaluation. Three strategies, same outcome: model recognizes concept, fails to identify violation. Lead with the finding, not the method: "Across direct questioning, error correction, and Socratic prompting, 2.8B recognized the accessibility concept but could not identify the violation."

Then the kill shot — state it cleanly: "The declarative-evaluative gap persists across all elicitation strategies tested. It is not an artifact of prompt design."

**The 1B Comparison**

This is its own beat. 1B fails broadly — generic, off-topic completions. But: the specific case where 1B treats the evaluative Direct Question prompt as a completion task and accidentally generates alt text. This proves the gap from the opposite direction. A model below the declarative threshold stumbles into the correct output by misunderstanding the task. Frame this as a natural control — it shows the gap isn't about task difficulty but about the transition from declarative to evaluative reasoning.

**The "Describing Its Own Gap" Response**

Give this its own paragraph or mini-subsection. The 2.8B response to the instructional correction prompt: "I have a photo gallery on my website. I want to add an accessibility attribute to the image tag...I have tried adding the attribute...but it doesn't work."

Don't just call it "striking." Unpack it: The model generates a first-person narrative about attempting and failing to do exactly what it was asked to do. It has enough access to the concept topology to know what kind of thing is needed, but cannot traverse from recognition to resolution. It's describing its own gap from inside the gap. This is behavioral evidence of partial binding — the model can activate the neighborhood of the correct answer without reaching the answer itself.

**Entropy Analysis**

Present the table. Then the interpretation — and this is where you need to slow down and let the reader feel the weight:

Three distinct failure profiles at 2.8B:

- High entropy (Error Correction): stalling, echoing — the model doesn't know where to go
- Intermediate entropy (Direct Question): fluent confabulation — the model goes somewhere wrong with moderate confidence
- Low entropy (Socratic): confident parroting — the model locks onto the prompt's rhetorical structure and continues it with high confidence, but the confidence is about *pattern continuation*, not *answering*

1B shows no comparable differentiation. Its entropy is relatively flat across prompt types.

The point: the gap isn't a single missing capability. It's a structured landscape of partial competence. The model enters measurably different internal states depending on how you ask, even when the outcome is the same: failure. This is the first quantitative evidence that the declarative-evaluative gap has internal structure.

Connect to future work: the Socratic prompt's low entropy at 2.8B (4.1660 last-token) is the lowest of any failure condition tested. The model is maximally confident while maximally wrong. This warrants circuit-level investigation.

---

## Results — Experiment 3: Recognition vs. Generation **[unchanged]**

No new data.

---

## Results — Experiment 4: Mechanistic Analysis **[expand — 12B integration]**

After the existing Pythia 160M–6.9B results and GPT-2 replication, add:

### Extending the Binding Curve: Pythia 12B

Present the 12B results:

- 119 total heads above 0.1, 36 strong heads above 0.5
- Last strong binding layer: 34 (out of 35) = 97% depth
- Top binding head: Layer 1, Head 15 at 0.9905

**Late-layer resurgence.** This is the new finding. Layer 33 has 7 active binding heads (4 above 0.5), including Head 16 at 0.8766 — the strongest late-layer cluster of any model tested. Present the scaling progression:


| Model | Late-layer entries |
| ----- | ------------------ |
| 1B    | 1                  |
| 2.8B  | 4                  |
| 6.9B  | 6                  |
| 12B   | 11                 |


This scales monotonically. Update your Figure 3 (the bar chart) to include the 12B data point — it extends the scaling curve with a sixth bar.

**Specialization.** % of heads active in binding decreases with scale (31.9% at 160M → 8.3% at 12B) while absolute count plateaus around 100–120 for models ≥2.8B. The model converges on how many heads it needs and stops recruiting more. Larger models use proportionally fewer, more specialized heads.

**Cross-model universals vs. new observations:**

- Universal: front-loaded binding (65–82% in first 25% of layers)
- Universal: strong heads (>0.9) cluster at 3–10% depth for all models ≥1B
- Universal: mean binding scores stable (~0.36–0.44) regardless of scale
- NEW: late-layer resurgence scales with model size
- NEW: specialization (fewer participating heads, same binding strength, deeper penetration)

Frame the key point clearly: the strength of binding doesn't change with scale. The depth does. 12B extends this curve and adds the resurgence observation.

---

## Discussion **[revise]**

### "The 2.8B Threshold Is Meaningful, Not Arbitrary" **[expand]**

Now you can add the elicitation robustness as further evidence. The threshold survives 15 prompt types across 3 elicitation strategies. Also note the entropy differentiation at 2.8B as evidence that the threshold represents a qualitative shift in internal processing, not just a behavioral boundary.

### "The Declarative-Evaluative Gap Is Not Closed at Any Scale Tested" **[revise — this is now much richer]**

The original version says: gap exists, "Click here" is the only success, knowing ≠ applying.

Now you can say:

- Gap persists across all elicitation strategies (not just the original 5 prompts)
- Gap has internal structure — entropy analysis shows three distinct failure modes
- The "describing its own gap" response provides behavioral evidence of partial concept access without resolution capability
- The 1B accidental success provides a natural control showing the gap isn't about task difficulty
- The Socratic prompt's low-entropy confident failure is a specific prediction for future circuit work

This section should be substantially rewritten to carry the weight of the new evidence.

### "Attention Binding as a Mechanistic Correlate of Emergence" **[expand]**

Add the 12B findings: late-layer resurgence extends the correlational claim to a sixth data point. The specialization finding (fewer but deeper heads) is consistent with the hypothesis that wider MLP layers sustain compound representations through deeper propagation.

Note the connection between entropy profiles and binding depth — different entropy signatures at 2.8B may reflect different degrees of partial binding activation. This is speculative but worth flagging as a connection point for future causal work.

### "Not All Concepts Benefit Equally from Scale" **[new subsection or expand existing]**

Skip link prefers the wrong definition even at 12B. This suggests training data representation imposes a floor that scale alone cannot overcome. This is an honest, credibility-building observation. Pair it with the ARIA confabulation discussion — both show limits of scaling.

---

## Conclusion **[revise]**

Update to reflect the expanded scope:

- Pythia 160M–12B (not just 6.9B)
- Gap validated across 15 prompt types, 3 elicitation strategies
- Entropy analysis reveals structured failure, not uniform failure
- 12B extends binding curve, introduces late-layer resurgence and specialization
- Skip link as a scaling limit

---

## Appendices

**Appendix A:** Unchanged (original prompts).

**Appendix B:** Add 12B architecture row to the Pythia table (may already be there in v2).

**Appendix C:** Unchanged — this is already well-organized with the completion, hypothesis-driven, and validation prompt tables.

---

## What Gets Cut

The "Extended Analysis" section header and its introduction/discussion framing. All the content from those 6 pages is absorbed into the sections above. No data is lost. The "Additional Discussion" subsection on pages 32–33 is redundant once findings are integrated into the main Discussion — its key points get distributed across the relevant Discussion subsections.

---

## Version Note

Add a footnote or acknowledgment line: "This version integrates extended elicitation robustness testing, entropy analysis, and 12B binding results that appeared as a separate addendum in the previous version."