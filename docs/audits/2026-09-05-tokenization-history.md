# Tokenization history and saved-span audit

Scope: existing source/history and saved token strings only. No model inference, retokenization, partial correlation, or new robustness test was run. Manuscript and primary result files are unchanged.

## Reconstructed development

- Initial historical notebook at commit 4083256, `accessibility-knowledge-emergence/notebooks/extended/add-compounds-across-all_Testing_Accessibility_Knowledge_Across_Pythia_Model_Sizes.ipynb`, prints token/index pairs before using explicit constituent indices for screen reader, alt text, and skip link. This documents inspection of realized positions rather than treating words as tokenizer-independent positions.
- DECISIONS.md records expansion from three to approximately eleven compounds on June 20, and a June 21 preliminary clean-versus-subword comparison. The latter explicitly requires further analysis before a claim.
- By commit 26c6a8d (June 27), `src/binding.py::find_token_index` already contains the current deliberate split-word handling: case-insensitive stripped exact-token matching first; otherwise concatenate adjacent stripped token strings, return the last subtoken of the first matching span. A failure returns None and the producer skips and warns. The later position attends to the earlier position. This selects a measurement location; it neither changes tokenizer segmentation nor aggregates all subtoken writes.
- `src/analysis.py::tokenization_comparison` groups eight named compounds as clean and three as split (keyboard navigation, closed captions, semantic HTML), then reports mean/max attention and head counts above .1. It does not control frequency or fit a partial correlation. ADR 0009 and the August audit explicitly mark its eleven-term mapping as stale for the 53-term battery.
- The July 2 inventory expansion (dd141cb) adds blocks explicitly labeled replacements for tokenization difficulties in legal, medical, and finance inventories. This supports deliberate inventory curation, but the inspected history does not provide a complete rejected-term-to-replacement ledger. Those domain comments are not an accessibility-specific exclusion list.
- The August 8 migration spec preserves the matcher unchanged while mechanically converting arrays to 227 YAML compounds, including 53 accessibility terms. The effective-binding notebooks use the same two-pass last-subtoken rule and record prompt/token/position metadata.
- Preregistration 0003 section 5 requires uniquely locatable constituents and exclusion of ambiguous/failed matches, plus a strict single-token subset sensitivity; section 10 additionally proposes component-word token-count controls where variation remains. Registration is a plan, not evidence of completed analyses. The implementation returns the first match without explicitly testing ambiguity; the present saved-span audit found no ambiguous constituent matches in any of the 26 files.

## Inclusion sets are distinct

The 51 declarative concepts map to 49 frequency compounds after excluding ARIA and WCAG as acronym concepts without two-word bigrams. Captions is retained as closed captions. The present effective-binding files each contain all 53 inventory compounds, with all recorded last-subtoken indices reproduced and no missing matches. Their 49-term frequency join excludes page_title, form_label, link_text, and empty_link because they lack entries in the frozen frequency table. They are present and measurable in the binding files. Thus those four exclusions should not be described as failed tokenization. A complete earlier accessibility rejection history could not be reconstructed from the inspected repository records.

## Remaining constituent-token variation

Counts below sum tokens belonging to the two matched constituents, excluding BOS and the surrounding prompt. Values are reconstructed directly from saved strings; all 1,378 compound/model/condition records were checked before selecting the 49-term frequency subset.

| Family and actual prompt text | Two tokens | Three tokens | Four tokens |
| --- | ---: | ---: | ---: |
| Pythia natural, all six scales | 40 | 8 | 1 |
| Pythia uniform, all six scales | 48 | 1 | 0 |
| GPT-2 natural text wherever saved | 39 | 7 | 3 |
| GPT-2 uniform text wherever saved | 48 | 1 | 0 |
| OLMo natural, all three scales | 46 | 2 | 1 |
| OLMo uniform, all three scales | 49 | 0 | 0 |

The residual uniform-prompt split in Pythia/GPT-2 is captions: ` capt` + `ions`. Natural prompts additionally split sentence-initial words such as Keyboard into Key + board and Semantic into Sem + antic. Counts vary materially in natural prompts (3–10 of 49 compounds have more than two tokens); uniform prompts leave no variation in OLMo and only one exception in Pythia/GPT-2. This inventory does not determine whether the variation explains the binding association.

## Prompt-label discrepancy uncovered during counting

- GPT-2-large natural-labeled file matches all 53 uniform templates, while its uniform-labeled file matches all 53 natural templates.
- GPT-2-medium uniform-labeled file matches all 53 natural templates. Its complete table equals the natural file on every column except prompt_condition.
- All other files match their stated condition's prompt inventory.
- Twenty-four inventory prompts are identical between conditions, so the discrepancy is established using the other 29 as well as full-inventory matches.

These are saved-data condition/provenance problems. Do not silently swap labels or treat the medium duplicate as an independent uniform replication. They affect the interpretation of condition-specific tables and require separate reconciliation before final submission. No corrected correlations were calculated in this audit.

## What supports the manuscript wording

The exact phrase “after controlling for compound token count” is already present when the binding section enters the current section layout in commit eac254a (August 22). The effective-binding analysis notebook contains bootstrap, aggregate permutations, and head-selection analyses but no corresponding partial-token-count implementation or strict-single-token subset result was located. The saved token-count partial correlations are in results/frequency/spearman_partial.csv and are generated by src/dual_spearman.py for declarative accuracy. That code uses GPT-2 tokenization of standalone compound strings for all families, not the saved model-specific prompt spans above.

Existing evidence supports deliberate token-aware measurement, preliminary clean/split attention comparisons, and declarative-frequency statistical controls. It does not currently substantiate the binding section's separate claim of surviving token-count controls. Conflation of these distinct analyses is the best-supported explanation for the wording, but the exact editorial origin of that conflation is not established. Do not describe a promised registered sensitivity as completed.

## Audit artifacts

- 2026-09-05-tokenization-inspect.py: descriptive saved-span reconstruction.
- 2026-09-05-tokenization-inventory.csv: per-model/condition/compound spans and counts, including the 53-to-49 inclusion flag.
- 2026-09-05-tokenization-inputs.csv: SHA-256 hashes of the 26 measurement inputs.
- 2026-09-05-tokenization-prompt-check.csv: per-file matches to natural/uniform inventories.

These new audit records are local and uncommitted; original artifacts are untouched.
