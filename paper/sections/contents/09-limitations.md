## Limitations

We state limitations in the order a skeptical reader would raise them.

**Single domain, single prompt family in places.** The trajectory and gap results are established for accessibility concepts only; the frequency hypothesis predicts the same structure in legal, medical, and financial domains, and the compound inventory to test that exists, but this paper does not. Narrower still, the measurement-pathway divergence result (Section 7) is systematic across all six scales but was established on one prompt family — its claim of systematicity is across scale, not across prompts, and we say so rather than let the reader assume otherwise.

**The causal test of binding is scoped, and the scope is now three-layered.** Single-head necessity is ruled out directly; the earned deep-selective population is ruled out by a pre-registered joint ablation across four compounds (Section 3; protocol, disclosed amendment, and per-compound gate accounting in the public decision log); and cross-domain population necessity is ruled out by the companion ablations. Two caveats survive. The attention-binding metric measures only attention patterns, not the value written: a head can attend strongly while contributing little, and conversely. And one robustness compound (semantic HTML) degenerated at the set-earning stage — sentence-initial tokenization fragments its first word, so its candidate pool was nominated largely by fragment-merging attention; its over-inclusive thirteen-head set still ablates to 0.0015, but we report it per-compound rather than as a clean fourth replication. We therefore frame late-layer binding as a correlate of emergence and defer the positive question — what does compute these compounds, most plausibly MLP and ensemble effects outside the selective sets — to future work.

**The binding metric is contaminated at late layers.** Attention-sink and positional structure leak into the binding score at depth, which is why the head audit of Section 3 was necessary and why we recommend a uniform template for any cross-domain use of attention-pairing metrics. We treat this as a finding as well as a limitation, and note that it plausibly implicates unaudited attention-pairing metrics elsewhere.

**Small cells where stated.** The fluent-wrongness confidence gap rests on a thin control cell (n = 2–5 control-correct responses per scale); its sign is consistently non-negative across the suite and both families, but the magnitude carries that caveat everywhere we report it. The within-sense frequency correlation is undersampled by the phenomenon itself — more than 80% of compounds yield too few correct-domain responses to analyze — and the small-subsample result we report is labeled descriptive.

**The taxonomy is vocabulary, not a claim.** Class assignments survive a one-level coding perturbation in only 20 of 102 cases; the trajectory classes are used as names for curve shapes, and no result in this paper depends on a classification boundary.

**Coding is deterministic, not sophisticated.** The accuracy criteria are substring-and-rule based by design — auditable and re-runnable at the cost of nuance. A strictness audit of the criteria was run and its outcomes disclosed in the decision log; the criteria remain crude in the way that makes them checkable, and a differently-crude rubric could shift individual codes. The "correct token" framing at decision points carries the matching simplification: the claim is that domain-relevant tokens as a group are outranked by generic continuations, not that one specific token must win.

**Corpus and tokenizer asymmetries.** Frequency counts are measured on The Pile, which is exact for Pythia and a cross-corpus proxy for GPT-2 (WebText is not publicly indexed); the two families also tokenize compounds differently. That the correlation transfers anyway is evidence of robustness, but the GPT-2 result inherits the proxy status. The calibration counts additionally pass through the Infini-gram index's Llama-2 tokenizer at the string level, a documented mismatch we log rather than hide.

**Open-weight models only.** All results are on Pythia and GPT-2. Frontier models do not release training data, which forecloses the corpus-auditing this paper depends on; whether these findings survive instruction tuning and RLHF is unknown, and we make no claim that they do.

**One exhibit in this paper's history was retracted by its own protocol.** An earlier token-competition exhibit was withdrawn when a pre-registered gate showed it to be a measurement-pathway artifact; the retraction, the gate, and the generalized finding it produced are documented in Section 7 and in the public decision log. We list this here not as a live limitation but as the record of one: the remaining decision-point claims were re-derived on the true output pathway, and the episode is why every pathway in this paper is now stated explicitly.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     Superseded items from the suggestion block: the n=8 Spearman power
     limitation is DEAD (n=49 campaign, both suites significant, pre-registered
     threshold cleared — see Section 5); replaced above by the honest survivors.
     The distributed-ensemble paragraph adapts binding-reframe-draft.md Edit 3
     (blessed prose). D6 RUN + RATIFIED 2026-07-06 — paragraph shrunk per the D6
     plan same day (Fable); small-cell n corrected to 2–5 per the claims audit. -->


### SUGGESTION: Known limitations to address

**Sample size.** The Spearman correlation runs on n=8 compounds (expanding to n=49). GPT-2 is significant at p=0.024; Pythia is a strong trend at p=0.12. Be transparent about the power limitation and the expansion plan.

**Evaluative prompts are hand-crafted.** The three evaluative prompts in tangent.ipynb (skip_link, screen_reader, alt_text/div_onclick) were chosen to illustrate the frequency gradient. They're not exhaustive. A reviewer could ask whether other evaluative framings produce different results.

**Accessibility domain only.** Trajectory classifications exist only for accessibility concepts. The frequency hypothesis predicts the same pattern in legal, medical, and financial domains, but that's untested in this paper. (Mitigated by the cross-domain infrastructure being ready.)

**Open-weight models only.** All results are on Pythia and GPT-2. The research agent synthesis noted that frontier models (GPT-4, Claude, Gemini) don't release training data, preventing direct corpus-auditing. Your findings may or may not generalize to RLHF'd models. State this explicitly.

**Tokenization across suites.** Pythia (NeoX tokenizer) and GPT-2 (BPE) split vocabulary differently. The frequency data comes from The Pile for both, which is correct for Pythia but only approximate for GPT-2 (trained on WebText). Acknowledge this asymmetry.

**The "correct token" framing.** Tracking ' users' as the "correct" token at the decision point is a simplification. Multiple tokens could lead to correct answers. The claim is that domain-relevant tokens as a group are outranked by generic function words, not that a single specific token must win.
