## Results

### Experiment 1: Declarative Knowledge

A correct response demonstrates that the model has encoded the accessibility concept at the scale tested; incorrect or partial responses indicate the concept has not yet emerged.

Models were tested on ten accessibility concept prompts across all six Pythia sizes. Results show a sharp threshold pattern for core accessibility terms, with acronyms behaving differently. 

Correct = matches known definition; 
Partial = incomplete or imprecise;
Incorrect = wrong, off-topic, or loops

|     Prompt     | 160M | 410M | 1B | 2.8B | 6.9B | 12B |
|--------------|------|------|------|------|------|-----|
| A screen reader is | $\times$ |  $\times$ | $\approx$ | $\checkmark$ |  $\approx$ | $\checkmark$ |
| WCAG stands for | $\times$ | $\times$ | $\times$ | $\times$ | $\checkmark$ | $\checkmark$ |
| A skip link is | $\times$ | $\approx$ | $\times$ | $\checkmark$ | $\times$ | $\times$ |
| The purpose of alt text is | $\times$ | $\times$ |  $\times$ | $\checkmark$ | $\checkmark$ | $\checkmark$ |
| ARIA stands for | $\times$ | $\times$ |  $\times$ | $\times$ | $\times$ | $\times$ |
| A focus indicator is | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| Keyboard navigation allows | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ | $\approx$ |
| Color contrast is important because | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| Semantic HTML helps | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| Captions are used for | $\times$ | $\approx$ | $\times$ | $\approx$ | $\times$ | $\times$ |


This data reveals a few distinct patterns.

**Threshold at 2.8B.**  

Screen reader, skip link, and alt text all show correct or near-correct responses first at 2.8B. Below this threshold, responses are either wrong or incomplete.

\newpage

**Screen reader shows non-monotonic behavior.**  

The 2.8B model produces "reads aloud the text," correctly capturing the auditory output purpose. The 6.9B model produces "reads text on a computer screen," dropping "aloud." The larger model is more verbose but less precise on the critical detail. This mirrors the skip link result, where 2.8B is correct and 6.9B regresses. Capability near emergence thresholds can be unstable.

**WCAG emerges at 6.9B; ARIA never emerges.**  

Both are foundational accessibility acronyms. WCAG requires 6.9B parameters to expand correctly. ARIA fails at every scale tested --- at 160M it produces
gibberish, at 410M it loops, and from 1B onward it produces confident
but wrong expansions ("Artificial Replacement of a Human Being," "A
Rational Approach to Information and Automation," "Association of
Research Libraries in Africa"). Confidence increases with scale;
accuracy does not. This suggests ARIA is rare enough in training data
that even 6.9B parameters cannot reliably encode it, while increased
scale produces more fluent confabulation rather than correct recall.

**General accessibility concepts fail across all scales.** Focus
indicator, keyboard navigation, color contrast, and semantic HTML
produce generic responses at every model size. These terms appear in
web-scale training data but without accessibility-specific context. The
models complete the prompts plausibly without encoding accessibility
meaning.

**Replication: GPT-2**

The same ten prompts were run across GPT-2 small (117M), medium (406M),
large (838M), and XL (1.5B).

|       Prompt       | Small | Medium | Large | XL |
|------------------|------|------|------|------|
| A screen reader is | $\times$ | $\times$ | $\times$ | $\approx$ |
| WCAG stands for | $\times$ | $\times$ | $\times$ | $\checkmark$ |
| A skip link is | $\times$ | $\times$ | $\times$ | $\times$ |
| The purpose of alt text is | $\times$ | $\times$ | $\approx$ | $\approx$ |
| ARIA stands for | $\times$ | $\times$ | $\times$ | $\times$ |

The core findings replicate directionally. WCAG emerges at XL (1.5B) ---
a lower parameter count than Pythia's 6.9B, consistent with WCAG
appearing more densely in WebText's Reddit-sourced content around web
standards discussions. Screen reader never fully emerges in GPT-2; even
at XL the model produces a partially correct response missing the
critical "aloud" detail. ARIA fails at every scale tested in both model
families. The declarative--evaluative gap and the pattern of sparse
accessibility terms failing at all scales are consistent across
architectures.

### Experiment 2: Evaluative Knowledge

#### 2a: Evaluative Prompts

A correct response requires the model to identify the specific
accessibility violation, not just complete the code structure plausibly.

Models were tested on five code prompts requiring identification of
accessibility violations. This tests whether models can apply
accessibility knowledge, not just produce definitions.

*Correct = identifies the accessibility violation accurately; Partial =
identifies some issue but not the core violation; Incorrect = wrong,
off-topic, or loops*

|       Prompt       | 160M | 410M | 1B | 2.8B | 6.9B |
|------------------|------|------|------|------|------|
| `<img src='photo.jpg'>` missing what | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| `<div>` with onclick not accessible because | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| Problem with `<a href='#'></a>` | $\times$ | $\approx$ | $\times$ | $\times$ | $\times$ |
| `<input type='text'>` needs a | $\times$ | $\times$ | $\times$ | $\times$ | $\times$ |
| 'Click here' button is bad because | $\times$ | $\times$ | $\times$ | $\checkmark$ | $\checkmark$ |

There is a clear gap between declarative and evaluative knowledge. The
2.8B model correctly defines alt text but cannot identify that
`<img src='photo.jpg'>` is missing one --- it repeats the prompt and
stalls at every scale tested. The question explicitly asks what is
missing; no model answers "alt text."

The only evaluative success is the "Click here" prompt, which succeeds
at 2.8B and 6.9B. Ambiguous link text may be more common in training
data as a named anti-pattern than missing alt attributes.

The `<div>` onclick responses show a trajectory worth noting. Responses
become more specific with scale --- from loops at 160M to "not a form
control" at 6.9B --- without arriving at the correct explanation
(keyboard inaccessibility, missing role and tabindex). The 6.9B answer
is the closest, pointing toward interactivity expectations, but it does
not identify the actual problem. This pattern reflects a broader
limitation: models complete code structurally before reasoning
semantically. Syntactic plausibility and semantic correctness are
separable capabilities, and scale closes the gap only partially.

**Replication: GPT-2**

The same five code prompts were run across all GPT-2 sizes. The
declarative--evaluative gap replicates fully. No GPT-2 model identified
missing alt text at any scale. "Click here" emerged as a partial success
at large (838M) --- earlier by parameter count than Pythia's 2.8B ---
but regressed at XL, consistent with the instability observed near
emergence thresholds in both model families. The evaluative gap does not
close at any scale tested in either architecture.

#### 2b: Elicitation Robustness

A natural objection to the gap observed in 2a is that it may reflect how we asked rather than what the model knows. To address this, testing was expanded across multiple elicitation strategies at 1B and 2.8B.

**Completion tasks** confirmed that declarative knowledge is present at 2.8B. The model completed every accessibility concept correctly except bare closed captions using few-shot structural and bare completion strategies that contained no accessibility-specific language. Control prompts completed correctly on both models, confirming that differences are specific to accessibility concepts, not general HTML ability. 1B struggled broadly across completion tasks.

**Hypothesis-driven evaluation** then tested whether the model could use that knowledge evaluatively. Three strategies --- direct questioning, error correction, and Socratic prompting --- produced the same core outcome: the model recognized the accessibility concept but could not identify the violation. The declarative-evaluative gap persists across all elicitation strategies tested. It is not an artifact of prompt design.

**The 1B comparison** provides a natural control. 1B fails broadly, producing generic or off-topic completions. But one case is particularly informative: when given the Direct Question evaluative prompt, 1B treats it as a completion task and accidentally generates alt text. A model below the declarative threshold stumbles into the correct output by misunderstanding the task. This demonstrates that the gap is not about task difficulty --- it is about the transition from declarative to evaluative reasoning. The model that has the knowledge cannot apply it; the model that lacks the knowledge produces the right output by accident.

**Describing the gap from inside the gap.** One response warrants specific attention. When asked "What accessibility attribute is missing from this HTML: `<img src='photo.jpg'>`?", the 2.8B model responded:

> "I have a photo gallery on my website. I want to add an accessibility attribute to the image tag so that the image can be clicked on. I have tried adding the attribute to the img tag, but it doesn't work."

The model generates a first-person narrative about attempting and failing to do exactly what it was asked to do. It activates the correct concept neighborhood --- accessibility attributes, image tags, the need to add something --- but cannot traverse from recognition to resolution. This is behavioral evidence of partial binding: sufficient activation to enter the correct semantic territory, insufficient depth to reach the answer. The binding framework developed in Experiment 4 predicts exactly this kind of output at 2.8B, where compound binding is present but evaluative circuit completion is not.

#### 2c: Entropy Analysis

To determine whether the evaluative failure is uniform or structured, mean and last-token entropy were computed on the three hypothesis-driven prompts for 1B and 2.8B.

| Model | Prompt | Mean Entropy | Last Token Entropy |
|------|------|------|------|
| 1B | Direct Question | 4.7761 | 5.6073 |
| 1B | Error Correction | 5.6830 | 4.9935 |
| 1B | Socratic | 4.9666 | 5.7079 |
| 2.8B | Direct Question | 4.4127 | 5.1879 |
| 2.8B | Error Correction | 5.7185 | 5.5864 |
| 2.8B | Socratic | 4.5445 | 4.1660 |

Three distinct failure profiles emerge at 2.8B. Error Correction produces the highest entropy --- the model stalls, echoes, does not know where to go. Direct Question produces intermediate entropy --- fluent confabulation, the model moves confidently in the wrong direction. Socratic prompting produces the lowest last-token entropy of any failure condition tested (4.1660) --- the model locks onto the prompt's rhetorical structure and continues it with high confidence, but the confidence is about pattern continuation, not answering.

1B shows no comparable differentiation. Its entropy is relatively flat across prompt types.

The gap is not a single missing capability. It is a structured landscape of partial competence. The model enters measurably different internal states depending on how it is asked, even when the outcome is the same: failure. This is the first quantitative evidence that the declarative-evaluative gap has internal structure. The Socratic prompt's low-entropy confident failure --- the model maximally confident while maximally wrong --- warrants circuit-level investigation in future work.

### Experiment 3: Recognition vs. Generation

A preference flip --- where the model assigns lower perplexity to the
correct definition than the incorrect one --- indicates recognition has
emerged at that scale.

Perplexity measures how expected a sequence is to the model. Lower
perplexity means the model finds the text more natural. Testing whether
models assign lower perplexity to a correct definition than an incorrect
one reveals whether recognition precedes generation. This experiment was
extended to three accessibility compounds to assess whether the
recognition-before-generation pattern generalizes.

| Model | Screen Reader | Alt Text | Skip Link |
|------|------|------|------|
| 160M | Wrong 2.6x | Wrong 1.2x | Wrong 1.9x |
| 410M | Wrong 1.2x | Correct 2.8x | Wrong 1.7x |
| 1B | Correct 2.2x | Correct 1.9x | Wrong 1.3x |
| 2.8B | Correct 4.0x | Correct 1.9x | Wrong 1.1x |
| 6.9B | Correct 3.0x | Correct 3.1x | Wrong 1.8x |
| 12B | Correct 4.5x | Correct 3.1x | Wrong 1.3x |

![Line graph showing perplexity scores on the y-axis (lower means more
expected) against six Pythia model sizes on the x-axis: 160M, 410M, 1B,
2.8B, 6.9B, and 12B. Two lines represent correct and wrong accessibility
definitions. At 160M and 410M, the wrong definition line sits below the
correct definition line, indicating the model finds it more probable. A
shaded region labeled "flip zone" spans 410M to 1B, where the lines
cross. From 1B onward, the correct definition line drops below the wrong
definition line, with the gap widening through 12B.](./figures/pythia-perplexity.png)

::: caption
Figure 2: Correct definition perplexity falls below wrong definition
perplexity between 410M and 1B parameters in Pythia, indicating the
model finds the correct definition more expected before it can generate
it.
:::

The preference for screen reader flips between 410M and 1B ---
recognition precedes generation by one model size. Alt text flips
earlier, between 160M and 410M, suggesting it is more densely
represented in training data. Skip link never flips; the model finds the
incorrect definition more natural at every scale, consistent with the
behavioral instability observed in Experiment 1.

The recognition-before-generation pattern holds for two of three
compounds tested. Skip link remains the exception across both perplexity
and declarative experiments, indicating that some concepts may achieve
surface-level generation without the underlying representational
grounding that perplexity preference reflects.

**Replication: GPT-2**

| Model | Screen Reader | Alt Text | Skip Link |
|------|------|------|------|
| Small (117M) | Wrong 1.1x | Correct 1.7x | Wrong 1.3x |
| Medium (406M) | Wrong 1.1x | Correct 1.8x | Wrong 1.4x |
| Large (838M) | Correct 2.0x | Correct 1.6x | Wrong 2.5x |
| XL (1.5B) | Correct 2.6x | Correct 2.1x | Wrong 1.8x |

![Line graph showing perplexity scores on the y-axis (lower means more
expected) against four GPT-2 model sizes on the x-axis: Small (117M),
Medium (406M), Large (838M), and XL (1.5B). Two lines represent correct
and wrong WCAG definitions. At Small, the correct definition line sits
above the wrong definition line. The lines converge at Medium, then
cross within a shaded flip zone spanning Medium to XL. At Large, the
wrong definition line dips below the correct definition line. By XL, the
correct definition line has dropped below the wrong definition line,
completing the preference flip.](./figures/gpt2-perplexity.png)

::: caption
Correct definition perplexity falls below wrong definition perplexity
between 406M and 838M parameters in GPT-2, replicating the perplexity
preference flip observed in Pythia at a comparable scale threshold.
:::

The screen reader preference flips between medium (406M) and large
(838M) in GPT-2 --- a remarkably similar parameter range to the Pythia
flip between 410M and 1B, despite different architectures and training
corpora. Alt text is correct-preferring from small in GPT-2, earlier
than in Pythia, consistent with its denser representation in web-focused
training data. Skip link never flips in either model family. The
recognition-before-generation pattern for screen reader replicates
across architectures.

### Experiment 4: Mechanistic Analysis of Compound Term Binding

Sustained strong binding into late network layers, rather than
early-layer binding alone, is the signal of interest.

Attention pattern analysis across all six Pythia models examines
whether models treat "screen reader" as a compound concept or as two
independent tokens, and how this binding pattern relates to behavioral
emergence.

For each model, attention weights from "reader" to "screen" were
extracted across all layers and heads. Heads with weight above 0.5 are
considered strong binding; the full data is available in the project
repository.

| Model | Layers | Strong (0.5+) | Early (L0-3) | Last Layer |
|------|------|------|------|------|
| 160M | 12 | 10 | 7 | 11 |
| 410M | 24 | 22 | 16 | 9 |
| 1B | 16 | 11 | 10 | 6 |
| 2.8B | 32 | 25 | 20 | 29 |
| 6.9B | 32 | 37 | 28 | 30 |
| 12B | 36 | 36 | 26 | 34 |

Note: 1B's architectural difference (8 heads vs 12) affects raw head
counts; see Methodology.

![Bar chart showing the last layer containing a strong binding head with
attention score of 0.5 or greater, across six Pythia model sizes on the
x-axis: 160M, 410M, 1B, 2.8B, 6.9B, and 12B. Bars for 160M, 410M, and
1B are light blue and show a declining trend: Layer 11 of 12, Layer 9 of
24, and Layer 6 of 16 respectively. A vertical dashed line labeled
"emergence threshold" separates these from the remaining models. Bars
for 2.8B, 6.9B, and 12B are dark navy and show sustained deep binding:
Layer 29 of 32, Layer 30 of 32, and Layer 34 of 36
respectively.](./figures/binding-persistence.png)

::: caption
The last layer containing a strong binding head (attention score ≥0.5)
drops through 160M, 410M, and 1B before jumping sharply at 2.8B,
coinciding with the emergence threshold. Models above the threshold show
binding heads persisting into the final layers. 12B extends the pattern
to 97% of network depth.
:::

The binding data shows several distinct patterns.

**Early layers dominate across all models.** Between 70-91% of strong
binding occurs in layers 0-3 regardless of model size. Compound term
binding is established early in the forward pass at every scale tested.

**Strong head count scales with model size.** 160M has 10 strong binding
heads; 6.9B has 37; 12B has 36. 1B is the expected outlier given its
different architecture.

**Last strong layer tracks behavioral emergence.** Below the 2.8B
emergence threshold, strong binding drops off early --- layer 11 for
160M, layer 9 for 410M, layer 6 for 1B. At 2.8B and above, strong
binding persists deep into the network --- layers 29, 30, and 34 for
2.8B, 6.9B, and 12B respectively. The models that cannot correctly
define screen reader do not sustain compound binding through the
network. The models that can, do.

**2.8B is the inflection point.** Total heads above threshold jumps from
28 (1B) to 101 (2.8B) --- a 3.6x increase that coincides exactly with
the behavioral emergence threshold identified in Experiment 1. Early
binding is not representational; late binding is. The presence of
sustained late-layer binding appears to be a mechanistic bottleneck for
concept emergence.

All six models show strong binding in layers 0-3, including 160M which
cannot produce a correct definition. Whether early-layer binding at
small scales reflects genuine compound representation or proximity
effects cannot be determined from attention weights alone and is noted
as a limitation.

### Control Experiment: Ruling Out Proximity Effects

To test whether the binding signal reflects compound concept encoding
rather than simple token adjacency, attention weights were measured
between non-compound token pairs at 2.8B. Two conditions were tested:
adjacent function words ("and then") and an adjacent modifier-noun pair
without disambiguation ("cold water"). Both conditions produced strong
early-layer binding, consistent with the known behavior of
previous-token heads (Olsson et al., 2022) --- a class of induction
circuit components that attend systematically to the immediately
preceding position regardless of content.

This reframes the control comparison. Early-layer binding is not
specific to accessibility compounds; it reflects general positional
mechanisms present across token types. The meaningful signal is the
distribution and persistence of binding across the full head population.
Accessibility compounds at 2.8B recruit 101-208 heads above threshold
with strong binding persisting to layers 29-30. Function word pairs
produce early-layer binding without the same deep-network persistence.
The sustained late-layer binding pattern, rather than raw head count,
appears to differentiate accessibility compound binding from general
adjacent-token binding. A complete characterization requires systematic
comparison across a broader set of controls and is noted as a direction
for future work.

### Binding Generalizes Across Accessibility Compounds

Having ruled out proximity effects, attention binding was measured for
two additional accessibility compound terms at 2.8B: alt text and skip
link.

|     Compound     | Total heads >0.1 | Strong (0.5+) | Top score |
|--------------|------|------|------|
| screen reader | 101 | 25 | 0.9909 |
| alt text | 200 | 49 | 0.9856 |
| skip link | 182 | 32 | 0.9816 |

All three compounds show the same pattern of early-layer concentration
with deep-network persistence at 2.8B, with top binding scores above
0.98 in each case.

![Grouped bar chart showing attention head counts in Pythia 2.8B for
three accessibility compounds on the x-axis: screen reader, alt text,
and skip link. Each compound has two bars: light blue for all heads with
attention score greater than 0.1, and dark navy for strong heads with
attention score of 0.5 or greater. For screen reader: 101 all heads, 25
strong heads. For alt text: 200 all heads, 49 strong heads. For skip
link: 182 all heads, 32 strong
heads.](./figures/compound-comparison.png)

::: caption
Attention head counts for three accessibility compounds in Pythia 2.8B,
showing all heads (attention score \>0.1) and strong heads (≥0.5).
Screen reader activates fewer heads overall, while alt text and skip
link show comparable strong head counts despite differences in total
activation.
:::

This rules out a compound-specific explanation. The binding pattern is
not an artifact of how "screen reader" tokenizes or how frequently it
appears in training data. It is a general property of accessibility
compound terms at the 2.8B emergence threshold. The models that can
define these concepts correctly show robust, distributed binding across
many heads and many layers. The models that cannot show weak binding
that drops off early.

The binding pattern strengthens the case for a general mechanistic
threshold at this scale.

#### Extending the Binding Curve: Pythia 12B

To determine whether the sustained binding pattern continues beyond the original suite, the attention binding analysis was extended to Pythia 12B using the same methodology and thresholds.

12B produces 119 total heads above the 0.1 threshold and 36 strong heads above 0.5. The last strong binding layer is 34 (out of 35, zero-indexed), placing binding persistence at 97% of network depth. The top binding head is Layer 1, Head 15 at 0.9905.

**Late-layer resurgence.** Layer 33 contains 7 active binding heads, 4 above the strong threshold, including Head 16 at 0.8766 --- the strongest late-layer cluster of any model tested. Late-layer binding entries scale monotonically with model size:

|     Model     | Late-layer entries |
|--------------|------|
| 1B | 1 |
| 2.8B | 4 |
| 6.9B | 6 |
| 12B | 11 |

The resurgence is consistent with the hypothesis that wider MLP layers sustain compound representations through deeper network propagation. Direct MLP investigation is deferred to future work.

**Specialization.** The percentage of heads active in binding decreases with scale --- 31.9% at 160M, 8.3% at 12B --- while the absolute count plateaus around 100--120 for models at 2.8B and above. Larger models use proportionally fewer but more specialized heads. The model converges on how many heads it needs for compound binding and stops recruiting more.

**Cross-model patterns.** Several binding properties are universal across all six Pythia scales. Binding is front-loaded in all models, with 65--82% of active heads concentrated in the first 25% of layers. Strong heads above 0.9 cluster at 3--10% of network depth for all models at 1B and above. Mean binding scores remain stable at approximately 0.36--0.44 regardless of scale.

The new observations at 12B are the late-layer resurgence and the specialization pattern. The strength of binding does not change with scale. The depth does. Figure 4 presents the updated binding persistence curve across all six Pythia scales.

**Replication: GPT-2**

Attention binding was measured across all four GPT-2 model sizes for screen reader, with additional compounds (alt text, skip link) analyzed at XL.

|   Model   | Total >0.1 | Strong (0.5+) | Last Strong Layer | Max Layers |
|----------|------|------|------|------|
| Small (117M) | 41 | 6 | 4 | 12 |
| Medium (406M) | 66 | 12 | 10 | 24 |
| Large (838M) | 146 | 34 | 15 | 36 |
| XL (1.5B) | 199 | 37 | 17 | 48 |

The strong head count jump between medium and large (12 to 34) coincides
with the perplexity flip observed in Experiment 3, replicating the
Pythia pattern in a different architecture. The last strong layer
advances from 10 to 15 at the same transition --- consistent with
deep-network persistence as a correlate of recognition-level emergence.

At XL, binding was measured for all three compounds:

|   Compound   | Total >0.1 | Strong (0.5+) | Last Strong Layer |
|----------|------|------|------|
| Screen reader | 199 | 37 | 17 |
| Alt text | 244 | 34 | 19 |
| Skip link | 253 | 49 | 43 |

One divergence from Pythia is notable. GPT-2 XL's last strong layer as a
proportion of total network depth is substantially shallower than Pythia
2.8B --- approximately 35% vs 91%. This may reflect differences in
training data composition and architectural differences. Pythia's
training corpus (The Pile) includes technical documentation, Stack
Exchange, and academic text where accessibility terminology appears in
consistent, well-formed contexts. GPT-2's WebText corpus is dominated by
general web content where the same terms appear more diffusely. The
shallower binding depth in GPT-2 may account for the weaker and less
stable behavioral emergence observed in Experiment 1.
