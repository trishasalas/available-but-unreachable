## Experiments

Perfect—then I would preserve that workflow.

I’d duplicate the three existing binding notebooks:

- `binding-pythia.ipynb` → `effective-binding-pythia.ipynb`
- `binding-gpt2.ipynb` → `effective-binding-gpt2.ipynb`
- `binding-olmo.ipynb` → `effective-binding-olmo.ipynb`

They would retain the same setup, model loading, compound lists, progress messages, and output conventions. I’d only replace the measurement cell so each row additionally records:

```plaintext
attention_weight
value_write_norm
effective_binding
relative_effective_binding

```

Then I’d add one analysis notebook that:

1. loads those new CSVs;
2. selects the final third of each model;
3. merges them with `frequency_table.csv`;
4. produces correlations and figures;
5. identifies candidate heads for ablation.

The existing `d6-multihead-ablation.ipynb` can also be adapted rather than replaced. Its instrumentation already works; we would change how the head set is selected and evaluate whether ablation effects are stronger for rare compounds.

That is safer and more comfortable: the notebooks will look and behave like the ones you already use, with each new cell explained in ordinary language. ALTI can remain a later, separate notebook because it is the only part that genuinely requires a different analysis structure.

---

## Pre-registration

I would make the value-weighted test confirmatory, keep head localization exploratory, and preregister one held-out ablation test. Crucially, the document must disclose that the hypothesis was generated after seeing the raw-attention result.

Here is a ready-to-adapt draft.

---

# Preregistration: Frequency and Effective Late-Layer Compound Binding

**Date:** [YYYY-MM-DD]  
**Status:** Registered before computing or inspecting any value-weighted binding results.

## 1. Motivation and disclosure

Previous analyses measured compound binding as the raw attention weight from the later compound token to the earlier token. In the 49-compound accessibility set, late-layer raw binding was negatively correlated with corpus bigram frequency in all 13 tested models.

These results have already been observed and are not confirmatory evidence for the present hypotheses.

The present study was motivated by those observations and by prior work showing that raw attention weights may not reflect the magnitude of information transmitted by an attention head. We will test whether the inverse frequency relationship survives when binding incorporates the value vector and output projection.

Previous head-ablation results have also been observed. They generally found that selected high-attention binding heads were not causally necessary. The new ablation analysis therefore uses a different, frequency-derived head-selection rule and a held-out compound set.

No value-weighted binding results will be inspected before this registration is frozen.

## 2. Models

The study will use the same 13 model-scale combinations as the existing binding analysis:

- Pythia: 160M, 410M, 1B, 2.8B, 6.9B, and 12B
- GPT-2: small, medium, large, and XL
- OLMo-2: 1B, 7B, and 13B

Models will use the same revisions, tokenizer settings, prompts, and loading code as the existing binding notebooks.

## 3. Stimuli and frequency measure

The primary stimuli are the 49 accessibility compounds in the frozen frequency table.

The frequency variable is:

\[ F_c = \log(1 + \text{bigram count}_c) \]

Counts will be read from the existing frozen `frequency_table.csv`. No compounds or frequency values will be changed after the analysis begins.

Because the primary analysis uses Spearman correlation, applying the logarithm does not affect rank order; it is retained for interpretability and plotting.

## 4. Prompt conditions

### Primary condition

Each compound will be measured in its existing natural declarative prompt, identical to the prior binding analysis.

### Uniform-template robustness condition

Each compound will also be measured in:

```plaintext
A {word1} {word2} is

```

This condition controls prompt length, compound position, and surrounding lexical material.

## 5. Tokenization rule

Token indices will be determined before examining effective-binding values.

The primary analysis will use compounds for which both component words can be uniquely located in the tokenized prompt. Ambiguous or failed matches will be excluded for that model and listed explicitly.

A sensitivity analysis will be conducted on the stricter subset in which each component word corresponds to exactly one tokenizer token.

No exclusion will depend on frequency, accuracy, attention, or effective-binding values.

## 6. Binding measures

For layer \(l\), head \(h\), source token \(s\), and target token \(t\), raw binding is:

\[ A_{l,h,t,s} \]

The unscaled source write is:

\[ W_{l,h,s} = V_{l,h,s}W^O_{l,h} \]

Value-write magnitude is:

\[ N_{l,h,s} = \lVert W_{l,h,s} \rVert_2 \]

Effective binding is:

\[ E_{l,h,t,s} = A_{l,h,t,s} \cdot N_{l,h,s} \]

The primary normalized measure is:

\[ R_{l,h,t,s} = \frac{E_{l,h,t,s}} {\lVert r^{pre}_{l,t} \rVert_2} \]

where \(r^{pre}_{l,t}\) is the residual stream at the target position before layer \(l\).

All four component values will be saved:

- raw attention;
- value-write norm;
- effective binding;
- residual-normalized effective binding.

## 7. Definition of late layers

For a model with \(L\) layers, the late-layer region begins at:

\[ \left\lceil \frac{2L}{3} \right\rceil \]

using zero-indexed layer numbers.

This definition will not be adjusted by model or after inspecting results.

## 8. Compound-level outcome

The primary outcome for each compound and model is the 95th percentile of residual-normalized effective binding across all heads and layers in the final third.

The following secondary outcomes will also be reported:

- maximum normalized effective binding;
- maximum unnormalized effective binding;
- mean of the five largest normalized effective-binding values;
- maximum raw attention.

The 95th percentile is primary because it captures strong late-layer activity without depending entirely on a single extreme head.

## 9. Confirmatory hypothesis

### H1: Effective late binding and frequency

Within models, rarer compounds will exhibit stronger late-layer effective binding.

For each model, we will calculate:

\[ \rho_m = \operatorname{Spearman} (F_c, R^{95}_{m,c}) \]

The directional prediction is:

\[ \rho_m < 0 \]

### Primary cross-model test

The model correlations will be combined as:

\[ T_{\text{observed}} = \frac{1}{13} \sum_m \operatorname{atanh}(\rho_m) \]

Frequency labels will be permuted across compounds 10,000 times. The same permutation will be used for every model during each iteration, preserving the dependence created by testing the same compounds across related models.

The one-sided permutation p-value will be:

\[ p = \frac{ 1 + \#(T_{\text{permuted}} \le T_{\text{observed}}) }{ 10{,}001 } \]

The random seed will be `20260813`.

H1 will be considered supported if the permutation test gives \(p < .05\) and the observed aggregate effect is negative.

Per-model correlations and bootstrap confidence intervals will be reported regardless of the aggregate result.

## 10. Robustness analyses

The following analyses will not replace the primary test:

1. Repeating H1 with the uniform-template prompts.
2. Repeating H1 on the strict single-token subset.
3. Using maximum and mean-top-five aggregation.
4. Testing raw attention and value-write norm separately.
5. Reporting results separately for Pythia, GPT-2, and OLMo.
6. Controlling for component-word token counts where variation remains.

A negative raw-attention relationship combined with a null effective-binding relationship will be interpreted as evidence that the original result did not reflect stronger information transfer.

## 11. Exploratory head localization

For every late-layer head, Spearman correlation will be calculated across compounds between frequency and normalized effective binding.

These analyses are exploratory because no individual head has been specified in advance.

We will report:

- the layer and head;
- its frequency correlation;
- bootstrap stability across compound resamples;
- false-discovery-rate-adjusted p-values;
- the distribution of correlations by relative layer depth.

Head identities will not be assumed to correspond across architectures or scales.

## 12. Held-out causal ablation

The causal analysis will use Pythia-2.8B only.

Compounds will be divided deterministically into equal selection and test subsets using random seed `20260813`.

### Head selection

Using only the selection compounds:

1. calculate each late head’s frequency–effective-binding correlation;
2. rank heads from most negative to most positive;
3. select the five most negatively correlated heads.

This head set will be frozen before evaluating any test compound.

### Intervention

The five selected heads will be jointly zero-ablated at the second compound word’s position using the existing `hook_z` intervention.

The primary causal outcome will be:

\[ KL(P_{\text{baseline}} \parallel P_{\text{ablated}}) \]

at the final prompt position.

### Causal prediction

Under the compensatory-binding hypothesis, ablation should perturb rarer compounds more strongly:

\[ \operatorname{Spearman} (F_c, KL_c) < 0 \]

This directional association will be evaluated using an exact or permutation-based Spearman test on the held-out compounds.

### Controls

The study will include:

- an empty-set ablation, which must produce zero or numerical-negligible KL;
- 100 randomly selected sets of five late-layer heads;
- a positive-control late-layer set demonstrating that the intervention can alter the output distribution.

## 13. Interpretation branches

Results will be interpreted according to the following frozen branches:

- **Raw and effective relationships are negative:** rare compounds receive stronger late-layer information transfer.
- **Raw is negative, effective is null:** the original relationship is confined to normalized attention allocation.
- **Raw is negative, effective is positive:** value magnitude reverses the apparent attention relationship.
- **Effective binding is negative and ablation affects rare compounds more:** evidence for compensatory, load-bearing late processing.
- **Effective binding is negative but ablation is flat:** late activity is frequency-sensitive but not causally necessary under this intervention.
- **Ablation improves rare-compound behavior:** evidence consistent with late interference rather than compensation.

No branch will be omitted.

## 14. ALTI analysis

ALTI will not be part of this preregistration because its exact implementation has not yet been frozen.

If pursued, its implementation, layer-composition rule, outcome measure, exclusions, and predictions will be registered in a dated amendment before any ALTI results are inspected.

---

That final ALTI clause is important. I would not preregister “we’ll run ALTI somehow.” First get its code working on synthetic examples, freeze precisely what constitutes word-to-word contribution, and then register it as a separate extension.
