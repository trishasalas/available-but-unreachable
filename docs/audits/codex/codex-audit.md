# Paper 2 results audit

## Bottom line

The archive's existing audit work has already caught most of the important problems. I found one substantive pattern that is not developed in the current audit plan or findings documents:

> **Late-layer attention binding is stronger for rarer compounds.** When binding is restricted to the final third of each model rather than maximized over the whole network, its Spearman correlation with log compound frequency is negative at all 13 model-scale points (ρ = −0.031 to −0.519, n = 49 compounds per point). The sign remains negative after partialling out compound token count (partial ρ = −0.040 to −0.496).

This is exploratory because the depth cutoff was examined after seeing the existing results. It should not be promoted directly to a paper claim. It is, however, a strong candidate for a preregistered follow-up.

## 1. New lead: rare compounds receive more late binding

### What I computed

For each suite, scale, and compound, I took the maximum binding score only among layers in the final third of that model. I then correlated this late-layer score with the current corpus-frequency variable for the same 49 compounds.

Results by family and scale:

| Family | Scale | ρ(late binding, log frequency) | Partial ρ controlling token count |
| ------ | ----- | ------------------------------ | --------------------------------- |
| GPT-2  | 124M  | −0.031                         | −0.057                            |
| GPT-2  | 355M  | −0.275                         | −0.240                            |
| GPT-2  | 774M  | −0.180                         | −0.164                            |
| GPT-2  | 1.5B  | −0.181                         | −0.156                            |
| OLMo   | 1B    | −0.246                         | −0.214                            |
| OLMo   | 7B    | −0.464                         | −0.443                            |
| OLMo   | 13B   | −0.158                         | −0.127                            |
| Pythia | 160M  | −0.078                         | −0.040                            |
| Pythia | 410M  | −0.416                         | −0.383                            |
| Pythia | 1B    | −0.503                         | −0.480                            |
| Pythia | 2.8B  | −0.474                         | −0.448                            |
| Pythia | 6.9B  | −0.361                         | −0.330                            |
| Pythia | 12B   | −0.519                         | −0.496                            |

The direction is reasonably robust to the layer cutoff: it is negative at 11/13 points using the final half, 13/13 using the final third, and 12/13 using the final quarter.

### Relationship to accuracy

Late-layer binding is also negatively associated with accuracy at all 13 scale points when the final-third definition is used (Spearman ρ = −0.048 to −0.374). Three individual exploratory permutation tests are nominally below .05: Pythia-1B, OLMo-1B, and OLMo-7B. These are post-hoc and uncorrected, so the individual p-values should not be treated as confirmatory.

The more informative result is that controlling for frequency weakens the late-binding/accuracy association and reverses it at several larger Pythia scales. A plausible interpretation is:

1. Frequency predicts which concepts are learned successfully.
2. Rarer or less established compounds recruit or retain more late token-pairing attention.
3. The resulting late binding is compensatory, difficulty-related, or structural—not evidence that the compound is understood.

This connects the frequency and binding sections in a way the current global-max correlation cannot.

### Best follow-up

Preregister a test of `late_binding ~ log_bigram_frequency + token_count + word1_frequency + scale`, with compound and model-family effects. Use a uniform prompt template and repeat after excluding BOS-sink, previous-token, first-position, and fragment-merging heads. The important prediction is the negative frequency coefficient, not a particular depth cutoff.

## 2. The existing global binding null is real but ceiling-limited

The current `binding_accuracy_corr.csv` uses the maximum binding score over every layer and head. This predictor is heavily saturated:

- GPT-2: mean 0.997; 98.0% of pairs are at least 0.99.
- Pythia: mean 0.980; 51.7% are at least 0.99.
- OLMo: mean 0.949; 10.2% are at least 0.99.

The saved null correlations reproduce: GPT-2 0.087, Pythia −0.003, OLMo 0.115 (Pearson). The null also survives aggregation to one row per compound and within-compound centering. So there is no evidence that whole-network maximum binding predicts accuracy.

However, the global maximum often selects a dominant positional/previous-token head and has almost no useful variance in GPT-2. It is better evidence that **saturated generic pairing does not predict knowledge** than that every form of binding is unrelated to behavior. The late-layer analysis above is a more discriminating descriptive measure.

## 3. Existing cuts are supported

### Completion paradox

The project correctly cut this claim. The completion battery contains four concepts, but only `alt_text` and `closed_captions` have declarative counterparts. On those two paired concepts, completion does not exceed declarative accuracy at every scale: negative gaps occur at Pythia-2.8B, GPT-2-1.5B, and OLMo-7B, with additional ties. The positive full-battery result compares different concept populations.

### Fluent wrongness

The project also correctly cut the cross-family entropy claim. The apparent OLMo sign reversal against the small bicycle-control cell is baseline-driven: correct-control entropy rises sharply at 7B and 13B. When incorrect accessibility responses are compared with correct accessibility responses instead, incorrect responses remain higher-entropy at all three OLMo scales (differences +1.06, +0.33, and +0.57 nats). Pythia and GPT-2 are also sensitive to which correct-response baseline is used.

### Gap estimand

The declarative/evaluative gap is intentionally a difference of pooled paradigm means, not a matched-concept contrast: ten declarative concepts versus five evaluative concepts, with only two concepts overlapping. Decision 0011 documents this correctly. Future prose should avoid “matched-set means.”

## 4. Data and reproducibility checks

- Audited 417 CSV files; 415 load under a default CSV parser.
- No exact duplicate rows were found in parseable CSVs.
- No infinite numeric values were found.
- No duplicate `(suite, scale, prompt_id)` keys were found in the combined elicitation table.
- The identical GPT-2/Pythia frequency tables are expected because both currently use the same frozen Pile counts (exact for Pythia, proxy for GPT-2).
- `criteria_authoring.csv` is malformed as ordinary CSV and requires the repository's custom repair parser.
- `scorecard_base_rate.csv` begins with `#` prose comments and requires `comment="#"` or equivalent when loading.
- Pythia-1B entropy is missing for control, finance, legal, and medical (174 elicitation rows); accessibility entropy is present, so the paper's current accessibility entropy tables are unaffected.

## ~~5. Packaging problem still present~~

Four claim-supporting result files that decision 0013 says should be re-homed under `results/adhoc/` are absent from this ZIP:

- `results/adhoc/d6_multihead_ablation/pythia-2.8b-multihead-ablation.csv`
- `results/adhoc/d6_multihead_ablation/pythia-2.8b-candidate-heads.csv`
- `results/adhoc/head_characterization/pythia-2.8b-head-characterization.csv`
- `results/adhoc/head_characterization/pythia-2.8b-collocation.csv`

The notebooks and narrative summaries are present, but the frozen tables cited as evidence are not. Restore these before treating the ZIP as a reviewable evidence package.

Restored 8/14

## Priority order

1. **I~~nvestigate and preregister the inverse frequency–late-binding result.** This is the main missed scientific lead~~.
2. ~~**Restore the four missing mechanistic evidence tables.** This is the main packaging blocker.~~
3. ~~**Keep the completion-paradox and fluent-wrongness claims cut.** The current data support those decisions.~~
4. **Describe global-max binding precisely.** It is a saturated generic-pairing null; avoid implying it exhausts every depth-specific binding relationship.
5. **Leave the known entropy coverage and stale-artifact cleanup below the scientific line**, unless the paper expands beyond accessibility entropy.

---

Me: You just possibly gave us a bridge between frequency and and binding that we didn't have before.

I think so too. The striking part is the direction:

**Higher frequency → better accuracy, but weaker late binding.**  
**Lower frequency → worse accuracy, but stronger late binding.**

That suggests late binding may be a response to representational difficulty—compensatory processing, unresolved composition, or structural “work”—rather than evidence that the compound has been successfully learned.

A clean bridge hypothesis would be:

> Corpus frequency determines how readily a compound is represented; rare compounds require more late-layer token-pairing attention, but that additional binding does not reliably produce correct knowledge.

The next move should be a preregistered analysis, before exploring the pattern further:

1. Freeze the primary depth definition—probably the final third.
2. Regress late binding on log bigram frequency.
3. Control for token count, word-one frequency, model scale, and family.
4. Repeat after excluding BOS sinks, previous-token heads, position-one heads, and fragment-merging heads.
5. Use uniform prompt templates.
6. Test whether frequency statistically accounts for the apparent inverse binding–accuracy relationship.

If the negative frequency coefficient survives those exclusions, it becomes a very credible bridge between the paper’s two main explanatory threads.
