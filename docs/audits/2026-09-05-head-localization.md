# Within-model head-localization audit

Status: analysis complete; approved manuscript changes applied. Detailed quantitative reporting remains scheduled for the appendix.

## Scope and method

This exploratory audit uses existing natural-prompt measurements for all thirteen model-scale points and all 49 compounds with corpus-frequency measurements. The raw files contain 53 compounds; `page_title`, `link_text`, `empty_link`, and `form_label` lack corpus-frequency rows and are excluded by the same inner join as the primary analysis. No new model inference was run. The registered causal test and its 25/24 split are unchanged. The existing `effective_binding_all_head_correlations_natural.csv` contains selection-only correlations for 25 compounds; it is not the source of these all-compound results.

For each model, retain zero-indexed layers at or above ceil(2L/3), calculate each head's Spearman correlation between log(1 + bigram count) and normalized value-weighted binding, and apply two-sided Benjamini–Hochberg correction within that model over finite correlations. Constant heads are retained with undefined correlations and excluded from the correction denominator. There are 13 such heads in Pythia-12B and two in Pythia-6.9B.

Bootstrap stability uses 2,000 compound resamples, seed 20260905, with paired frequency/write rows and shared resamples across heads within each model. The saved head table includes percentile 95% intervals, the proportion of finite resamples with negative correlation, and valid-resample counts. These marginal intervals are not corrected for multiple comparisons and must not be used as counts of discoveries. The depth table reports median and quartile correlations by (layer + 1)/L. These implement the descriptive outputs requested by preregistration 0003 section 11; the bootstrap count/seed and within-model correction family are explicitly recorded audit choices, not frozen confirmatory specifications.

The upper-tail inventory counts heads at or above each compound's 95th percentile. Tail membership describes write magnitude, not frequency sensitivity. The number of tail members per compound is largely determined by the percentile and model size; it is not independent evidence of distributed computation.

## Verification and interpretation

Recomputed 95th-percentile values match every saved compound/model primary value to numerical tolerance. All thirteen primary correlations reproduce. Every finite vectorized per-head correlation also matches SciPy's individual Spearman calculation.

Negative correlations occur in 33.3%–85.0% of heads with defined correlations. Counts passing within-model BH q < .05 range from zero to eight. None pass in GPT-2 at any of its four scales, or in Pythia-160M and Pythia-410M. This is evidence for heterogeneous head-level associations; neither these failures to pass correction nor the positive correlations establish causal irrelevance. Across the 49 compounds, 14–191 distinct heads per model enter the upper tail, but that inventory alone does not show which heads generate its frequency relationship.

The current prose infers distribution from different strongest-head identities across model scales. Section 11 explicitly says that head identities will not be assumed to correspond across architectures or scales. That argument should be removed. Following author discussion, retain “distributed” to describe the observed association across multiple heads. The aggregate upper-tail finding remains supported; circuit organization, absence of specialized heads, and causal role are not established. The initial recommendation to remove “distributed” everywhere conflated this descriptive usage with a mechanistic claim and has been superseded.

## Counter-proposal provenance review

In response to the author's provenance questions, all 14 saved input hashes were rechecked and matched. A fresh execution of the audit script reproduced all five CSV outputs byte-for-byte. This is new audit code using existing saved measurements, not an execution of the original notebook. The all-compound exploratory analysis is motivated by preregistration 0003 section 11; its particular implementation choices are documented above. The script, tables, and audit report are present locally but remain untracked and uncommitted at this review point. They are not yet part of an archived supplement.

Editorial recommendation: place the detailed counts and correction results in the appendix with the analysis method. Retain the descriptive distributed claim and section-specific prose. Cross-model head-identity comparisons cannot establish either absence of a shared circuit or absence of specialization; adding an observational guardrail does not supply a head-correspondence analysis.

## Artifacts

- `2026-09-05-head-localization-check.py`: reproducible CPU analysis; run from repository root.
- `2026-09-05-head-localization-models.csv`: model-level counts and upper-tail inventory.
- `2026-09-05-head-localization-heads.csv`: all heads, correlations, adjusted p-values, bootstrap stability, and tail membership.
- `2026-09-05-head-localization-depths.csv`: correlation distribution by relative layer depth.
- `2026-09-05-head-localization-inputs.csv`: raw measurement and frequency-file SHA-256 hashes.

The audit did not change primary result artifacts. Approved manuscript changes are recorded in `docs/reviews/2026-09-05-head-localization-prose.md`. The appendix should include the model-level count table and this method, with detailed head/depth data in the anonymized supplement.
