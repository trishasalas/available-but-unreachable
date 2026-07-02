## Limitations


### SUGGESTION: Known limitations to address

**Sample size.** The Spearman correlation runs on n=8 compounds (expanding to n=49). GPT-2 is significant at p=0.024; Pythia is a strong trend at p=0.12. Be transparent about the power limitation and the expansion plan.

**Evaluative prompts are hand-crafted.** The three evaluative prompts in tangent.ipynb (skip_link, screen_reader, alt_text/div_onclick) were chosen to illustrate the frequency gradient. They're not exhaustive. A reviewer could ask whether other evaluative framings produce different results.

**Accessibility domain only.** Trajectory classifications exist only for accessibility concepts. The frequency hypothesis predicts the same pattern in legal, medical, and financial domains, but that's untested in this paper. (Mitigated by the cross-domain infrastructure being ready.)

**Open-weight models only.** All results are on Pythia and GPT-2. The research agent synthesis noted that frontier models (GPT-4, Claude, Gemini) don't release training data, preventing direct corpus-auditing. Your findings may or may not generalize to RLHF'd models. State this explicitly.

**Tokenization across suites.** Pythia (NeoX tokenizer) and GPT-2 (BPE) split vocabulary differently. The frequency data comes from The Pile for both, which is correct for Pythia but only approximate for GPT-2 (trained on WebText). Acknowledge this asymmetry.

**The "correct token" framing.** Tracking ' users' as the "correct" token at the decision point is a simplification. Multiple tokens could lead to correct answers. The claim is that domain-relevant tokens as a group are outranked by generic function words, not that a single specific token must win.