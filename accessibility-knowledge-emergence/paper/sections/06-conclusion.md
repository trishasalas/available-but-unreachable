## Conclusion

We examined accessibility concept acquisition across six Pythia model
sizes (160M--12B) using mechanistic analysis, perplexity-based
recognition, and behavioral evaluation, with extended elicitation
robustness testing and entropy analysis at the scales where the
declarative-evaluative gap was first observed. Replication across the
GPT-2 model suite confirms the core findings hold across architectures
and training corpora.

Core accessibility concepts --- screen reader, alt text, skip link ---
emerge behaviorally at 2.8B parameters in Pythia. Foundational acronyms
require more scale (WCAG at 6.9B) or fail entirely (ARIA at all scales
tested). General accessibility vocabulary fails across all model sizes
in both model families, suggesting training data frequency as the
limiting factor rather than model capacity. Evaluative capability ---
identifying accessibility violations in code --- does not emerge within
the range tested, even in models that correctly define the relevant
concepts. The declarative-evaluative gap persists across 15 prompts
spanning three elicitation strategies, establishing that it is not an
artifact of prompt design but a genuine capability boundary.

Entropy analysis reveals that the gap has internal structure. Models
enter distinct failure states depending on how they are asked --- from
high-entropy stalling to low-entropy confident parroting --- even when
the behavioral outcome is the same. The structured failure profile is
specific to the scale where declarative knowledge is present.

The perplexity results show that recognition precedes generation: models
prefer correct definitions before they can produce them, with the
preference flipping between 410M and 1B in Pythia and between 406M and
838M in GPT-2, a remarkably consistent parameter range across different
architectures and training corpora. The attention binding analysis shows
that sustained binding of "screen reader" as a compound concept across
the full network is a mechanistic correlate of emergence --- present at
2.8B, 6.9B, and 12B in Pythia, absent at smaller scales. The same
binding jump replicates in GPT-2 at the transition between medium and
large, coinciding with the perplexity flip. Early binding is not
representational; late binding is. At 12B, a late-layer resurgence
pattern emerges --- a cluster of binding heads re-engaging near the
output layers that scales monotonically with model size --- alongside
increased specialization, where fewer heads participate in binding while
sustaining it deeper through the network.

Not all concepts benefit equally from scale. Skip link prefers the
incorrect definition even at 12B despite correct behavioral generation
at 2.8B, suggesting that training data representation imposes a floor
that scale alone cannot overcome.

For practitioners building accessibility tooling on language models, the
central implication is that behavioral success on definition tasks does
not predict success on evaluation tasks. The declarative-evaluative gap
observed here replicates across both model families and suggests that
reliable accessibility code review requires either substantially larger
models or domain-specific training data that goes beyond the web-scale
distribution.

For emergence researchers, accessibility concepts offer a useful probe
domain: rare enough to show scale sensitivity, concrete enough to
evaluate against ground truth, and distinct enough from general
knowledge to isolate domain-specific acquisition. The ARIA confabulation
pattern --- increasingly fluent wrong answers with scale --- illustrates
a failure mode that definition-based benchmarks would not detect. The
entropy-differentiated failure profiles at 2.8B suggest that emergence
boundaries are not uniform but structured, a finding that may generalize
beyond accessibility to other specialized domains.

The mechanistic findings here are correlational. Whether sustained
attention binding causes behavioral emergence or reflects a common
underlying factor requires causal analysis beyond the scope of this
study. The Socratic prompt's low-entropy confident failure and the
late-layer resurgence pattern identify specific targets for future
circuit-level investigation.