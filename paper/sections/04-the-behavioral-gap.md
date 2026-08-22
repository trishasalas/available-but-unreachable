## 1. The Behavioral Gap

The demonstrations above were run using the same model, prompted in the same way. The model produces correct, plausible-but-wrong, and incoherent completions depending on the concept. The question is whether this pattern generalizes.

We define declarative accuracy as whether or not a model can correctly state a concept's definition. Evaluative accuracy measures whether the model can use accessibility knowledge to perform a task. We first summarize the difference between the mean scores of the original ten-concept declarative battery and five-concept evaluative battery. This pooled estimate compares paradigms, not the same concept item by item. A separate paired test below asks the stronger same-concept question. The pooled pattern is not specific to Pythia. It reproduces across thirteen models in three families: Pythia, GPT-2, and OLMo 2.

Table 1 presents the original Pythia battery means at six scales. Declarative accuracy rises with scale, reaching a peak at 6.9B. Evaluative accuracy lags behind at every scale. The gap opens at 160M, widens to a maximum at 2.8B, and persists through 6.9B where the model's declarative knowledge is strongest.

| Scale | Declarative | Evaluative | Gap |
| ----- | ----------- | ---------- | --- |
| 160M  | 25%         | 10%        | 15% |
| 410M  | 40%         | 20%        | 20% |
| 1B    | 30%         | 10%        | 20% |
| 2.8B  | 60%         | 30%        | 30% |
| 6.9B  | 65%         | 50%        | 15% |
| 12B   | 45%         | 50%        | -5% |

At 12B, the gap closes — but not from below. Declarative accuracy drops. Three concepts answered correctly at earlier scales regress to incorrect by maximum scale: keyboard navigation, skip link, and closed captions. Table 2 shows the per-concept declarative trajectory; `cor`, `part`, and `inc` denote correct, partial, and incorrect. These are not averages obscuring noise — individual concepts flip from correct to incorrect. Each scale is a separately trained model, so the regression runs across scale, not across time within one training run. Convergence by decay is not mastery.

| Concept             | 160M | 410M | 1B   | 2.8B | 6.9B | 12B |
| ------------------- | ---- | ---- | ---- | ---- | ---- | --- |
| ARIA                | inc  | inc  | inc  | inc  | inc  | inc |
| WCAG                | inc  | inc  | inc  | inc  | cor  | cor |
| alt text            | inc  | part | part | cor  | cor  | cor |
| closed captions     | inc  | inc  | inc  | cor  | inc  | inc |
| color contrast      | part | cor  | part | part | cor  | cor |
| focus indicator     | part | inc  | inc  | inc  | inc  | inc |
| keyboard navigation | part | cor  | cor  | cor  | cor  | inc |
| screen reader       | part | part | cor  | cor  | cor  | cor |
| semantic HTML       | part | part | inc  | part | part | part|
| skip link           | inc  | part | inc  | cor  | cor  | inc |

The pattern is not specific to Pythia. In GPT-2 the gap widens with scale, reaching 55 points at 1.5B — declarative knowledge accumulates faster than the ability to deploy it. OLMo replicates the dissociation across three scales. Table 3 gives the family results not shown in Table 1.

| Family | Scale | Declarative | Evaluative | Gap |
| --- | ---: | ---: | ---: | ---: |
| GPT-2 | 124M | 35% | 20% | 15% |
| GPT-2 | 355M | 45% | 20% | 25% |
| GPT-2 | 774M | 50% | 30% | 20% |
| GPT-2 | 1.5B | 65% | 10% | 55% |
| OLMo 2 | 1B | 50% | 30% | 20% |
| OLMo 2 | 7B | 75% | 40% | 35% |
| OLMo 2 | 13B | 75% | 60% | 15% |

The gap reproduces across three model families trained on different corpora with different tokenizers and different architectures. It also differs in character across families. In Pythia, incorrect responses remain high-entropy; in GPT-2, confidence in errors grows with scale. At OLMo 7B and 13B, incorrect accessibility responses have lower entropy than correct bicycle-control responses, although that reversal does not hold against correct accessibility responses. Figure 1 shows the accuracy and entropy gaps across scale.

![Four line charts in two rows. Top row: declarative accuracy climbs with model scale while evaluative accuracy stays lower in both Pythia and GPT-2, with the shaded gap between the lines persisting at every scale. Bottom row: last-token entropy on evaluative prompts stays high across scale while declarative entropy falls.](figures/gap-behavioral-internal.png)

::: {.caption}
Figure 1. The gap in behavior and in uncertainty. Top: declarative and evaluative accuracy across scale for Pythia and GPT-2. Bottom: last-token entropy for the same prompt types. Evaluative uncertainty stays high even as declarative accuracy improves. OLMo values appear in Table 3 and the text.
:::

### A same-concept test

The pooled comparison leaves an obvious objection: the declarative and evaluative batteries contain different concepts. We therefore froze a second battery covering eight of the declarative concepts. Each concept receives two evaluative items with the same neutral answer frame: one example contains the accessibility violation, and one conformant example removes it. A concept passes only if the model gets both polarities right. Always finding a problem and never finding one both fail.

The result is harsher than the pooled gap. Across twelve untouched confirmatory models, none passes a single evaluative pair. The test contains 96 model-by-concept cells. Eighty-five pass neither item, seven pass only the conformant item, four pass only the violation item, and zero pass both. Table 4 separates those results from the development-exposed pilot.

| Set | Model-concept cells | Declarative passes | Evaluative pair passes | Declarative pass / evaluative fail |
| --- | ---: | ---: | ---: | ---: |
| Confirmatory models | 96 | 35 | 0 | 35 |
| Pythia-2.8B pilot | 8 | 5 | 1 | 4 |

The 35 confirmatory cells with a correct declarative response all fail the evaluative pair for that same concept. Pythia-160M contributes no cells to this conditional result because it has no declarative passes among the eight paired concepts. The paired test therefore supports the stronger mismatch directly: when declarative knowledge is present in the confirmatory set, no concept survives both application polarities.

Pythia-2.8B is reported separately because its behavior informed instrument development before the battery was frozen. It produces the only pair pass, on skip link. It classifies the violation as inaccessible and the conformant example as accessible, then repeats much of the prompt. Skip link is also the battery's only prose-described concept; the other seven require interpreting HTML or CSS. The result is consistent with framing-dependent reachability, but it does not separate framing from concept.

The gap is real, cross-family, and persistent. The original result does not reduce to a single confidence profile or a single failure mode, and the paired result does not reduce to a difference between concept inventories. A single corpus statistic — the bigram frequency of each compound in the training data — predicts which concepts take which path. The next two sections ask how far that prediction reaches and what it does not explain.
