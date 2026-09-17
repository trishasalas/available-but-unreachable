# Model-review revisions, September 12, 2026

The user approved revisions in the main `tmlr` repository using the original `paper/build-paper.sh` build. The copied `tmlr-pdf` experiment is not the source for this revision.

## Later decision: compact publication version

The user subsequently chose the original presentation with only the essential evidence corrections. The seven-request implementation below is a historical record, not the current manuscript state. The current source removes the added related-work paragraphs and their three bibliography entries, the item-deletion analysis from Methods/Results/tables, and the extra review-driven exposition. The original methods and table layout are restored.

Retained: the new title; named preprint and descriptive filename; explicit eight-concept/sixteen-item scope in the abstract and paired results; the verified aggregation caveat in Results and Appendix C (8/13 and 10/13 for normalized maximum, 11/13 and 12/13 for top-five mean); and softened processing-difficulty language. The obsolete reference to “unreachable” in the title remains removed. Supporting sensitivity scripts/CSVs remain available as audit records but the item-deletion results are no longer presented in the manuscript.

Both original build modes were rebuilt. The publication PDF is `paper/build-out/correct-definitions-failed-applications.pdf`: 20 pages, with 12 main-content pages, references on 13–14, and appendix on 15–20. Its name/email and absence of anonymous/TMLR review labels were verified. All pages were rendered and visually inspected; all six figure captions share pages with their images. Both build logs have no unresolved references/citations or overfull boxes; `git diff --check` passes. Existing ZIP supplements still predate these edits. Nothing was uploaded.

## Disposition of the seven requests

1. **Paired-battery scope:** The abstract now specifies eight concepts and one violation/conformant pair per concept. Results and Discussion explicitly bound the 96-cell finding to these sixteen application items across twelve confirmatory models. Broad opening/closing language in the behavioral section was narrowed to the tested tasks and models.
2. **Quantitative gap characterization:** Added post hoc, descriptive single-item-deletion ranges to existing Tables A5 and A7, with methods in Methods and Appendix G. Each model has fifteen omissions: one of ten declarative items or one of five evaluative items, with the affected mean recomputed. These are sensitivity ranges, not confidence intervals. A paired Wilcoxon/permutation test on the original unmatched batteries was not added. Eleven models retain positive gaps under every omission; OLMo-13B can reach zero and Pythia-12B can change sign. Figure 2's shading is explicitly identified as separation between means, not uncertainty.
3. **Processing difficulty:** Replaced the assertion that binding “marks where the model has difficulty” with a possible interpretation of a frequency correlate. Results and Discussion connect the causal limit to the unsupported registered rarity-dependent perturbation prediction. This does not establish that the heads have no effect.
4. **Metric rationale and alternatives:** Methods and Appendix C explain the common relative-depth rule and the registered rationale for the 95th percentile. Existing saved secondary results were reproduced: negative signs for normalized maximum occur in 8/13 natural and 10/13 uniform conditions; top-five means in 11/13 and 12/13; the primary 95th percentile in 13/13 under both. The universal sign pattern does not survive every aggregation. Counts are descriptive, not significance counts. These saved comparisons do not test a final-quarter cutoff. No preregistration was changed.
5. **Related work:** Added a paragraph on questionnaire–scenario value divergence and one on web correction/PDF accessibility evaluation. Existing clinical-triage and knowing–using citations remain. Three new BibTeX entries were checked against primary sources listed below.
6. **Pythia-12B regression:** The existing named concepts and Table A6 reference were retained; the text now makes the denominator explicit (“three of the ten declarative concepts”). These regressions are relative to earlier scales, not all relative to 6.9B.
7. **Attention saturation:** Results now explicitly connect the near-ceiling band across response categories to poor discrimination and cite Jain & Wallace and Serrano & Smith. The numeric 98% statistic remains restricted to GPT-2.

## Reproduction

`scripts/review-sensitivity.py` requires Python 3.10 or later and only the standard library. It reads existing results without running inference or modifying notebooks. It verifies all thirteen original model gaps against the saved family tables and independently recomputes 78 Spearman correlations from the compound summaries before writing:

- `results/analysis/original_gap_item_deletion.csv`
- `results/analysis/effective_binding_aggregation_signs.csv`

Executed with the bundled Python runtime. The original `bash paper/build-paper.sh` command rebuilds the revised manuscript. Existing notebooks, raw results, preregistrations, figure images, template and style settings remain unchanged.

## Primary literature checked

- Huang et al. (2026), *Knowing But Not Doing: Convergent Morality and Divergent Action in LLMs*: https://arxiv.org/html/2601.07972v1 — value questionnaire versus scenario-based choices; these are not observed real-world actions.
- Huang et al. (2024), *ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections*: https://arxiv.org/abs/2401.16450 — web-page correction task and author metadata.
- Kumar, Padath, and Wang (2025), *Benchmarking PDF Accessibility Evaluation*: https://arxiv.org/html/2509.18965v1 and https://doi.org/10.1145/3663547.3746380 — expert-annotated criteria, five-model evaluation, and alternative-text applicability/information limits; ASSETS 2025 bibliographic details.

## Build and layout

The final log contains no unresolved citations/references or overfull boxes. Figure 2 and its existing caption are kept together in a minipage. The forced page break before the artifact map was removed because it produced a nearly empty page after the new text. No margins, font sizes, or global spacing were changed. Final PDF: 21 pages, main text through page 13, references on pages 13–15, appendix on pages 16–21.

This revision updates manuscript source and its built PDF. Existing supplement/code-review ZIPs were not rebuilt and predate these revisions. Nothing was uploaded or submitted.

Final verification: all 21 pages rendered; changed pages inspected after the final layout fix; all six figure captions occur on pages containing their figures; all thirteen deletion ranges match the generated CSV; `git diff --check` passes.
