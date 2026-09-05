# Appendix review notes

Status: historical review notes. The approved appendix was integrated into `paper/sections/10-appendix.md` and the canonical PDF on 2026-09-05. Items below describe the earlier review state; token-count wording and frequency-reference distinctions have since been resolved. See README.md.

## Proposed contents

`appendix-proposed.md` contains architecture and paired checkpoint tables; generation settings and provenance limits; coding and sensitivity caveats; binding population and token matching; bootstrap and natural/uniform results; exploratory head localization; registered ablation and adherence; the three pooled behavioral tables; the existing Measurement Pathways prose; and an artifact map.

`prompt-inventory.md` extracts exact prompts from the existing YAML files: 15 original battery items, 41 additional declarative probes, 16 paired items with existing expected judgments, and 53 natural/uniform binding pairs. This can accompany the appendix as a separate anonymous prompt supplement. It introduces no new ground-truth decisions.

## Evidence issues to resolve before final integration

1. Results and Discussion claim that the value-weighted binding direction survives token-count controls. No corresponding implementation or result was found in the effective-binding notebook or saved analysis tables. `results/frequency/spearman_partial.csv` concerns declarative accuracy. Do not cite it as binding robustness. A separate saved-data sensitivity check is needed to retain the binding claim; otherwise propose removing that clause.
2. The registered binding analysis reads the shared frozen frequency table for all models, as preregistration 0003 section 3 specifies. The declarative-accuracy analysis uses family-specific corpus tables. The main Methods corpus-frequency paragraph needs to make this distinction explicit. Do not change the registered predictor or rerun the primary test using another corpus without identifying it as a separate sensitivity analysis.
3. The source-specific tokenizer version is incompletely recorded. Paired resolved model revisions must not be used to fill earlier binding/ablation revision gaps. Original elicitation run settings should be checked against per-run manifests before calling their description fully audited.
4. Paired false-positive labels remain frozen. Reporting their effect is not permission to change the coding instrument or ground truth.

## Table and build changes after prose approval

- Move original main Table 1 to A5, Table 2 to A6, and Table 3 to A7, preserving cell values.
- Expand main Table 5 into A3 with natural/uniform correlations and intervals.
- Retain the paired summary in the main text, give it a formal caption and label, and update its number consistently.
- Add formal captions/labels to appendix tables and update the corresponding main-text references.
- Render the approved appendix separately and insert it after the bibliography via the template's include-after hook; appending to the current section list would put it before References.
- Check the rendered PDF for split tables, long checkpoint hashes, and full-prompt layout. No final layout approval is implied by this Markdown draft.

The detailed head audit is committed as bd7322e. Its appendix table is extracted from that artifact, with negative signs distinguished from BH-corrected associations.
