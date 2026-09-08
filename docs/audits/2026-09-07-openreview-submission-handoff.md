# OpenReview submission handoff — 2026-09-07

Local handoff only. Nothing was uploaded, entered into a submission form, or submitted. The manuscript and supplement were not rebuilt or modified. This handoff contains local paths and author-completion notes; it is not part of the anonymous supplement.

## Files to select

### tmlr-submission.pdf

- Exact path: `/Users/trishasalas/Repos/research/tmlr/paper/build-out/tmlr-submission.pdf`
- Size: 2,011,372 bytes
- SHA-256: `5a75cb738147d129dcfdbf7e3498e450a548633968602277a70a46b75bf7693c`

### tmlr-anonymous-supplement.zip

- Exact path: `/Users/trishasalas/Repos/research/tmlr/paper/build-out/tmlr-anonymous-supplement.zip`
- Size: 55,337,031 bytes
- SHA-256: `1c3fa85dbb81e716cc22e67259744879ddf2d9eb1eadfc78cbadcaf0a7f79253`

The PDF includes the appendix; no separate appendix upload is needed. The ZIP is 55.34 MB (decimal). Select these two files, not historical review files or manuscript source files.

## Verification and provenance

Verified directly on 2026-09-07:

- PDF: 20 pages; PDF Author metadata is empty; extracted first-page text identifies “Anonymous authors” and “Paper under double-blind review.” Title and abstract match the canonical metadata source.
- ZIP: 494 files; archive CRC integrity passes. All 493 entries in `SHA256SUMS.json` match their packaged bytes. The checksum manifest itself is the remaining file and is covered by the external ZIP checksum above.
- Repository HEAD at handoff: `df90f0be5bef6830c09893fe83f546f13b366bb8`. Working tree was clean before adding this handoff. Generated upload artifacts are identified by their hashes, not by the commit alone.

The [final assembly audit](/Users/trishasalas/Repos/research/tmlr/docs/audits/2026-09-05-final-assembly.md) records the full visual inspection, numerical and reference checks, anonymization scan, registered-artifact verification, and extracted-package figure smoke tests. Those full checks were not rerun for this handoff. The audit reports references on pages 13–14 and appendix on pages 15–20. Canonical prose is [paper/sections/](/Users/trishasalas/Repos/research/tmlr/paper/sections); title, abstract, and disclosure come from [metadata.yaml](/Users/trishasalas/Repos/research/tmlr/paper/build/metadata.yaml).

These hashes identify the files currently on disk. Any rebuild or replacement requires fresh hashes and an updated handoff.

## Form mapping and current guidance

Start at [TMLR on OpenReview](https://openreview.net/group?id=TMLR). The public “TMLR Submission” control required login when inspected on 2026-09-07. No login was performed, so exact form labels, requiredness, character limits, dropdown choices, and any additional attestations remain unverified. The blocks below are a draft bank, not a claim that every heading is a live form field.

The [TMLR author guide](https://jmlr.org/tmlr/author-guide.html), checked on 2026-09-07, calls for active, complete author profiles, affiliations/conflicts/publication history, appropriate action-editor information, human-subject reporting, funding, and competing interests. It allows anonymous PDF/ZIP supplements up to 100 MB and specifies CC BY 4.0 for submissions. Author attestations and license acceptance must be completed by the author.

## Paste-ready manuscript fields

### Title — exact

```text
Available but Unreachable: The Declarative-Evaluative Gap in Language Models
```

### Abstract — exact wording, math converted to plain Unicode

Use the full manuscript abstract, rather than a newly shortened version. Paragraph breaks below follow the metadata source; the rendered PDF joins them.

```text
A language model can state what an accessibility concept means and still fail to apply it. We measure this declarative-evaluative gap in thirteen models from three families: Pythia, GPT-2, and OLMo 2. In the original behavioral batteries, the gap opens early and persists across families. At Pythia-12B, it closes because declarative accuracy falls. Three concepts answered correctly at smaller scales regress to incorrect at 12B. Convergence by decay is not mastery. In a frozen same-concept validation, none of 96 confirmatory model-concept cells passes both a violation and a conformant application item. Eleven cells pass one item; a development-exposed pilot, reported separately, passes one pair. The 96 confirmatory cells include 35 with correct definitions.

We test two possible explanations for the gap. The global maximum of attention between a compound’s constituents has weak associations with accuracy that differ in direction across families. When the measure is restricted to late-layer, value-weighted binding, a consistent pattern appears: rarer compounds receive stronger distributed value-weighted writes at all thirteen model-scale points (p = 0.0003). This is the opposite of what we would expect if stronger binding indicated knowledge. The pattern is consistent with processing difficulty, although the experiments do not identify what computation the stronger writes perform.

Corpus frequency is the strongest measured predictor of accuracy across 49 compounds (Spearman ρ = 0.52–0.59 across families), but it leaves most compound-to-compound variation unexplained. The same concept can be available to definition and unreachable in application, even though its corpus frequency has not changed. Frequency predicts availability. Task form constrains reachability.
```

### TL;DR / short summary — derived draft, if requested

```text
Across thirteen base models, correct accessibility definitions do not ensure successful application; frequency predicts declarative accuracy, while stronger value-weighted binding does not establish competence.
```

### Keywords — derived draft, if requested

```text
language models, mechanistic interpretability, knowledge application, attention, corpus frequency, digital accessibility
```

### Subject area / editor expertise — derived draft, if requested

Match the actual form's available categories; this is an expertise description, not a verified dropdown value.

```text
Language model evaluation and mechanistic interpretability, with emphasis on knowledge application, attention and value-weighted representations, corpus-frequency effects, and controlled behavioral experiments.
```

### Contribution / significance summary — derived draft, if requested

```text
The study separates definition-level success from concept application across thirteen base models in three families. A frozen same-concept battery yields zero passing application pairs across 96 confirmatory model-concept cells, including 35 with correct definitions. Corpus frequency predicts declarative accuracy across 49 compounds, while rarer compounds receive stronger late-layer value-weighted writes. A registered held-out ablation does not support greater output perturbation for rarer compounds. These findings distinguish behavioral availability, measured constituent interactions, and application success under the tested prompts.
```

### Supplement description / code and data availability — derived draft, if requested

```text
The anonymous supplement contains the exact prompt inventory, frozen corpus counts, coding rules, saved results, analysis code, anonymous inference notebooks, preregistrations, and provenance records. README.md identifies the canonical evidence tables; SHA256SUMS.json verifies the packaged files, and ANONYMIZATION.json records transformations and original/packaged hashes. No model weights are included.
```

### Reproducibility limitations / additional material notes — derived draft, if requested

```text
Saved-data checks and figure-generation smoke tests passed during assembly; model inference notebooks were not rerun. Anonymization changes the registered notebook's bytes, so the package provides a separately named checker for ten unchanged original hashes and the anonymous notebook hash, with the exception explicitly recorded. Full vocabulary distributions were not saved, so the original KL values cannot be independently reconstructed from CSVs alone.
```

Do not invent a public code URL. The local ZIP is the prepared anonymous artifact; a repository URL is not established here as suitable for anonymous review.

### Limitations — derived concise draft, if requested

```text
The original behavioral batteries are small and not concept-matched. The paired validation uses eight concepts with one violation and one conformant item each, and establishes failure under this instrument rather than every application prompt. The analyses cover 49 accessibility compounds and base models up to 13B parameters; they do not establish generalization to other domains, larger models, or instruction-tuned models. GPT-2 frequency estimates use a cross-corpus proxy. Value-weighted binding is a partial measure, and its association with rarity does not identify the computation performed or establish a causal role in application failure.
```

### Broader impact — derived concise draft, if requested

```text
Distinguishing knowledge available in definitions from knowledge reachable in application can guide research on training-data composition and transfer across task forms. Testing internal measures against behavior and interventions can also reduce the risk of treating stronger activity as evidence of competence. The potential benefit is a more precise basis for developing models whose demonstrated knowledge translates into reliable use. Accessibility is the empirical setting; generalization to other domains remains untested.
```

This summarizes the existing Broader Impact section; it does not replace an author judgment about risks or any live ethics attestation.

### Generative-AI assistance disclosure — exact approved wording, if requested

```text
Generative AI tools assisted with code development, analysis verification, and manuscript preparation. The research, methodology, analysis, and conclusions are the author’s own, and the author is responsible for the final content.
```

This wording is already in the PDF's title-linked first-page footnote. The final assembly audit records it as voluntary and author-approved, not as a mandatory separate form field.

## Author-completion items from the final assembly audit

Do not infer missing declarations from silence in the manuscript.

| Item | Available information / draft | Author action still needed |
| --- | --- | --- |
| OpenReview profile and author identity | Local build metadata lists Trisha Salas. | Confirm the complete author list and order, select the correct active OpenReview profile(s), and confirm corresponding contact information. Profile IDs are not established here. |
| Affiliations and conflicts | Not derivable from the manuscript. | Complete current and historical affiliations, publication history, and relevant relationships in each profile; report additional conflicts not captured by institutional history. Do not substitute “None” without checking. |
| Funding | Not established in the manuscript. | Provide funder names, grant identifiers, and relevant support. If accurate after review, a concise declaration is: “This research received no external funding.” |
| Competing interests | Not established in the manuscript. | Disclose relevant financial and nonfinancial interests. If accurate after review, a concise declaration is: “The author declares no competing interests.” |
| Human-subject reporting / IRB | The described methods evaluate pretrained models on constructed prompts and corpus-frequency counts; no participant study is described. | Confirm whether any human-subject activity occurred and provide the appropriate reporting/approval information. The conditional draft below is a study-description draft, not an IRB determination. |

Human-subject reporting — use only after author confirmation:

```text
The reported experiments evaluate pretrained language models using constructed accessibility prompts and corpus-frequency counts. No human participants were recruited and no participant-level data were collected for this study.
```

If the form separately asks for IRB status, exemption, or approval identifiers, the author must supply the actual status; this handoff does not establish an exemption or approval.

## Other author choices and attestations

- **Action editors:** the current author guide requests appropriate action-editor information. Use the expertise draft above to identify suitable editors in the live form, then check conflicts. No editor names or conflict-free status have been inferred.
- **Originality, concurrent submission, prior submission, related work:** answer any live questions from the actual publication/submission history. The manuscript cites an earlier blog post, but that fact alone does not establish the answer to an overlap or prior-publication question.
- **Licensing, author consent, policy/ethics confirmations, reviewer obligations, or certification requests:** complete any live controls personally after reading them. These are not manuscript-derived factual fields. No certification has been selected or claimed.
- **Unlisted required fields:** use the drafts only where their meaning matches the live prompt; resolve administrative facts before submitting. Exact field coverage cannot be certified without access to the authenticated form.

## Final manual handoff

1. Complete the author items and inspect the authenticated form's actual required fields and limits.
2. Recheck the two SHA-256 values if either artifact has changed since this handoff.
3. Select the canonical PDF for the manuscript and the anonymous ZIP for supplementary material; paste the exact title and abstract and any applicable derived drafts.
4. Review the submission preview and author-entered declarations, then submit only when ready.

No upload or submission was performed during this preparation.
