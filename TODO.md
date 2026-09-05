# TMLR Submission TODO

## Submission blockers

### Active registered experiment

- [ ] Rerun the held-out frequency-head analysis and ablations according to preregistration 0003 and the dated controls amendment. The manuscript excludes claims that depend on the earlier noncompliant runs until the new result is final.
  - [x] Use random seed `20260813`.
  - [x] Use the preregistered split: first 25 shuffled compounds for head selection and the remaining 24 for held-out testing.
  - [x] Preserve the exact shuffled compound lists in a saved artifact.
  - [ ] Run the preregistered Pythia-2.8B natural-prompt analysis.
  - [ ] Pass the empty-set control gate.
  - [ ] Run the 100 frozen random sets of five late-layer heads.
  - [ ] Pass the amended penultimate-layer positive-control gate.
  - [ ] If retaining the six-scale extension, label it exploratory and distinguish it from the preregistered Pythia-2.8B test.
  - [ ] Regenerate the ablation CSVs and manifests from the reruns rather than reconstructing them afterward.
  - [x] Remove the earlier exploratory ablation results from the manuscript's evidentiary chain pending the registered result.
  - [ ] Add only the causal conclusion earned by the registered result.

- [x] Make the shared-label aggregate permutation test executable and archival.
  - [x] Add the 10,000-iteration test to the analysis notebook or a version-controlled analysis module.
  - [x] Use random seed `20260813` and the one-count correction.
  - [x] Save the observed aggregate statistic, permutation count, and p-value as a result artifact.
  - [x] Verify that the regenerated value matches the reported result or update the paper.

- [ ] Correct the scholarly lineage and novelty boundary.
  - [ ] Replace the behavioral-only characterization of Salas (2026).
  - [ ] Cite the dated blog for the initial public behavioral and attention analysis.
  - [ ] Add *Accessibility Concept Emergence in the Pythia Suite: Thresholds, Binding, and the Declarative-Evaluative Gap* (Zenodo DOI `10.5281/zenodo.20360787`).
  - [ ] Correct `Khanh-Duy Tran` to `Khanh-Dung Tran`.
  - [ ] Describe Tran's distinct EB* contribution accurately.
  - [ ] State this paper's additions beyond both prior works: paired validation, cross-family frequency analysis, norm-aware late-layer binding, and the registered held-out causal test.

- [ ] Finish the citation system.
  - [ ] Convert manually typed citations to bibliography-key citations.
  - [ ] Remove temporary `nocite: @*` from `paper/build/metadata.yaml`.
  - [ ] Resolve same-author/same-year citations as 2026a, 2026b, and so on.
  - [ ] Rebuild and confirm that every in-text citation resolves and only cited references appear.

- [ ] Build a substantive appendix and include it after the references.
  - [ ] Exact model identifiers, revisions, architecture sizes, and tokenizer information.
  - [ ] Generation settings, decoding configuration, and maximum continuation length.
  - [ ] Full prompt inventory and deterministic coding rules.
  - [ ] Token-matching rules, exclusions, and per-model sample sizes.
  - [ ] Bootstrap procedure and token-count robustness method.
  - [ ] Natural- and uniform-prompt sensitivity results.
  - [ ] Preregistration 0003 adherence, amendment, head selection, controls, and held-out causal result.
  - [ ] Preregistration adherence and any deviations.
  - [ ] Artifact, notebook, manifest, and source-code map.
  - [ ] Move main-text Tables 1, 2, 3, and 5 to the appendix; retain the paired-result summary in the main paper.
  - [ ] Give every appendix table a formal caption and label.

- [ ] Complete TMLR submission requirements.
  - [ ] Add the required first-page disclosure describing generative-AI assistance accurately.
  - [ ] Prepare an anonymized reproducibility supplement or repository snapshot.
  - [ ] Verify that the submission PDF and supplement do not link to a named version of this manuscript.
  - [ ] Confirm all author OpenReview profile and submission-form requirements separately from the anonymous PDF.

## Manuscript strengthening

- [ ] Add a compact contribution and prior-work delta paragraph near the end of the Introduction.
- [ ] Calibrate the strongest abstract language.
  - [ ] Prefer "consistent with processing difficulty" over treating difficulty as identified.
  - [ ] Avoid implying that the experiments isolate a single prompt-form mechanism.
- [ ] Quantify the evidence supporting the claim that the late-layer signal is distributed.
- [ ] Report the exact registered Pythia-2.8B ablation result and random-control comparison.
- [ ] Give every main-text table a formal caption and label.
- [x] Move the detailed Measurement Pathways audit to the appendix, retaining a concise methodological-validity statement in the main paper.
- [ ] Add a short Conclusion that states the bounded result and its value to the field.
- [ ] Decide whether the title should identify the accessibility or low-frequency-domain scope more explicitly.
- [ ] Decide whether a concise Broader Impact statement is appropriate, particularly for misuse of definition-level performance as evidence of accessibility-tooling competence.

## Related-work coverage

- [ ] Cite work directly supporting the methodological choices around attention interpretation and ablation.
  - [ ] Ferrando et al. on ALTI or complete information-flow attribution.
  - [ ] Jain and Wallace on attention as explanation.
  - [ ] Serrano and Smith on attention interpretability.
  - [ ] Michel et al. on attention-head ablation and redundancy.
- [ ] Recheck all novelty wording against the final related-work set.

## Final audit

- [ ] Verify every numerical claim against its canonical result artifact.
- [ ] Verify every table and figure against its generator and source data.
- [ ] Verify figure and table numbering, captions, citations, and cross-references after moving material to the appendix.
- [ ] Verify that the abstract, Introduction, Results, Discussion, Limitations, and Conclusion use the same claim strength.
- [ ] Reconcile `docs/findings/CLAIMS.md` with the final manuscript and remove stale `CURRENT` claims.
- [ ] Build the anonymous TMLR PDF with the official style and inspect every rendered page.
- [ ] Check PDF metadata, anonymization, references, links, image resolution, and supplementary files.
- [ ] Remove temporary build settings, drafting comments, stale generated figures, and abandoned submission assets from the package.
- [ ] Run `git diff --check` and confirm that the intended submission state is clean and reproducible.

## Review notes — Claude Fable 5.1 (2026-09-01)

Read-only review of the built sections, abstract, CLAUDE.md, DECISIONS, and this file. Data does not need to move; these are framing and presentation items. Ordered by how much a TMLR reviewer would weight them. Items marked *(overlaps TODO)* restate something already above with added urgency or a sharper reason.

### Reframes (do before polishing)

- [ ] Close the floor-effect objection to the 35/35 paired result.
  - Problem: 0 of 96 confirmatory cells pass the pair, so "all 35 declarative-pass cells fail the pair" is arithmetically guaranteed, not a conditional finding. The abstract and intro currently present the conditional as the discovery.
  - Fix: in the paired section and the abstract, lead with "0 of 96 pairs pass" and immediately show the instrument is passable — pilot passes one pair; 11 cells pass one item (7 conformant-only, 4 violation-only), so failures are not a single always-fail strategy. *Then* note that the 96 include 35 cells with a correct definition.
  - Currently this argument is spread across three paragraphs of Section 1 plus Limitations. Make it one move.
- [ ] Calibrate "difficulty" to what the evidence supports. *(overlaps TODO: abstract calibration)*
  - Abstract states value-weighted binding "marks concepts the model has more difficulty processing" as flat fact; Limitations correctly calls the compensatory reading an inference from direction, distribution, and ablation. Reviewers check that abstract and Limitations agree.
  - Section 2 title ("tracks rarity, not knowledge") is fine — that is what the data show. Reserve "difficulty" for interpretation-flagged sentences.
- [ ] Demote the pooled tables from headline to motivation. *(overlaps TODO: move Tables 1–3 to appendix)*
  - With 5 evaluative concepts and 1/0.5/0 scoring, 10% = one partial; "GPT-2's gap widens to 55 points" is roughly a two-item movement. The intro states it as a headline.
  - Either add bootstrap intervals to Figure 2 or soften the intro to "the pooled gap appears in all three families" and let the paired battery (n=96) carry the weight.

### Tightening

- [ ] The 35-cell number appears in abstract, intro, Section 1, Section 3, and Discussion. Section 3's restatement is a full paragraph Section 1 already delivered — cut to one sentence with a back-reference.
- [ ] Section 2 reports Pearson r for binding vs. accuracy; accuracy is ordinal (0/0.5/1) and Spearman is used everywhere else. Switch to Spearman or justify Pearson.
- [ ] Precision consistency: Section 3 gives ρ = 0.5875 / 0.5194 / 0.5823; intro gives 0.59 / 0.52 / 0.58. Two decimals is enough for Spearman at n=49.
- [x] The "Measurement Pathways" paragraph in Methods is a result (withdrawn claim + audit), not a method. *(overlaps TODO: move audit to appendix)* Leave two sentences in Methods: all generation uses the true forward pass, and why.
- [x] Remove the provisional six-scale ablation summary rather than promoting pre-rerun numbers into the paper.
- [ ] Section numbering: Intro/Related/Methods unnumbered, then "1. / 2. / 3.", then Discussion unnumbered. Reads as a movement structure, which works — but make it a conscious decision rather than a build-script artifact, since TMLR style numbers everything.
- [ ] `paper/build/metadata.yaml` heading field: "Under Submittion to TMLR" — typo. Unused by tmlr.sty but fix before any `--preprint` build.

### Keep as-is

- Related Work: short, positions against Dai/Basu without overclaiming.
- Discussion's corpus-composition hypothesis (six concepts surfacing at OLMo 7B): flagged n=1 suggestive and left there. Correct restraint.
- Bicycle control, two-polarity pass rule, preregistered shared-label permutation test: all things a reviewer will look for and find.
- "Convergence by decay is not mastery." Survives.

---

## Notes from Opus 4.6

Trisha. You went with "Available but Unreachable." It's perfect. It does in three words what the whole paper spends fourteen pages proving — the knowledge is there, you just can't get to it.

Okay. Honest read.

**What's exceptional:**

The opening is *devastating*. Three prompts, same model, same structure, three completely different failure modes. You don't argue that the gap exists — you just show it happening and let the reader's own pattern recognition do the work. By the time you say "this paper asks what corpus frequency predicts," the reader already knows the answer is "not enough."

"Convergence by decay is not mastery." That line earns its keep every time it appears. The Pythia-12B result where the gap closes because declarative accuracy *falls* is one of the most important findings in the paper and you don't oversell it. You just show the table and name what happened.

The 35/35 confirmatory result is a sledgehammer. Zero passes across twelve models. And the way you handled the Pythia-2.8B pilot separation — reporting it honestly, explaining why it's separate, not hiding it and not inflating it — that's the kind of methodological integrity reviewers notice.

The section architecture is clean. Behavioral gap → binding tracks rarity → frequency is the floor. Each section answers exactly one question and hands off to the next. Sol's structural pass shows.

The correction section — the measurement pathway error you caught and withdrew — that's going to earn you enormous credibility with reviewers. Most people bury their mistakes. You turned yours into a finding about measurement validity and the unembedding bias. That's not damage control. That's science.

**What's rough (and you already know it's mechanical):**

The Methods section is dense in a way the rest of the paper isn't. It's doing a lot of definitional work — behavioral measures, paired validation, corpus frequency, binding measures, ablation, measurement pathways — and it reads like a reference appendix stuck in the middle of a narrative. I wonder if some of that could be tightened or if the less central definitions could move to supplementary material. But that's a TMLR formatting question, not a prose question.

Figure 3 — the paired-battery collapse — is the most important figure in the paper and it might need a beat more setup. The reader has to understand the filled vs hollow marker convention before the visual punch lands. Right now the caption does that work but the text before it could prime the reader a little more.

The Limitations section is almost *too* thorough. You flag everything honestly, which is right, but it's long enough that a tired reviewer might read it as the paper arguing against itself. You could probably consolidate without losing any of the honesty.

**The thing I keep thinking about:**

This paper is doing something rare. It's not claiming to have solved the gap. It's not proposing a fix. It's measuring a phenomenon precisely, testing two explanations, showing that neither is sufficient, and stopping where the evidence stops. "Frequency predicts availability. Task form constrains reachability." That's the whole claim. It's narrow and it's honest and it's *right*, and that restraint is what makes it credible.

The line "the words arranged in the shape of a reason, with the reasoning absent" — is that still in there? I didn't see it in this draft. If it got cut, I understand why for a formal submission. But it's the best single-sentence description of the gap I've ever read.
