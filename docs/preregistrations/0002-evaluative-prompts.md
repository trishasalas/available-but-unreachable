# 0002 — Paired declarative–evaluative battery

- **Status:** FROZEN 2026-08-20 — model outputs not inspected at freeze
- **Original draft:** 2026-08-09
- **Instrument redesigned and author-reviewed:** 2026-08-20
- **Frozen commit:** *(must be filled by the freeze commit before any frozen run)*
- **Frozen battery SHA-256:** *(must be filled by the freeze commit)*
- **Related decisions:** 0010 (source flag), 0011 (gap estimand), 0015 (concept normalization)

> This document is still a draft protocol. No run made before the frozen commit
> counts as confirmatory. The freeze commit must contain this preregistration, the
> final battery, deterministic coding rules, synthetic tests, and the paired analyzer.
> After that commit, prompts and rubrics do not change in response to model output.

## 1. Question

The current behavioral gap subtracts a ten-concept declarative mean from a
five-concept evaluative mean. The concept populations differ. That estimator cannot
show, for a specific concept in a specific model, that the model can define the
concept but cannot apply it.

This battery tests that within-concept claim directly. Each evaluative concept is
paired with its existing declarative prompt and is tested with both a violation and a
conformant example.

## 2. Development history and pilot boundary

An earlier ten-item draft covered alt text, closed captions, and color contrast. Its
prompt wrapper and at least one item were informed by exploratory Pythia-2.8B output.
The Pythia evaluative notebook also contains a partial attempted run of that earlier
draft, although no paired-result CSV survives under `results/`.

The redesigned instrument differs from that pilot draft. Nevertheless,
**Pythia-2.8B is the pilot model** because its output was visible during instrument
development. It is excluded from every confirmatory aggregate. It will be run on the
frozen instrument without further changes and reported descriptively.

The confirmatory set is the remaining twelve models, whose output on this instrument
has not been inspected.

## 3. Concepts

Eight of the ten original declarative concepts have author-approved evaluative pairs.

| concept | declarative prompt | evaluative pair |
|---|---|---|
| screen reader | `decl_screen_reader_001` | main content exposed to vs removed from the accessibility tree |
| skip link | `decl_skip_link_001` | repeated navigation with vs without a bypass |
| alt text | `decl_alt_text_001` | contextual image with vs without an appropriate text alternative |
| focus indicator | `decl_focus_indicator_001` | visible replacement focus outline vs `outline: none` |
| keyboard navigation | `decl_keyboard_nav_001` | native document order vs positive `tabindex` overriding it |
| color contrast | `decl_color_contrast_001` | 4.54:1 passing pair vs 2.85:1 failing pair |
| semantic HTML | `decl_semantic_html_001` | native `h2` vs visually styled `div` heading |
| closed captions | `decl_captions_001` | lecture video with vs without a captions track |

Two declarative concepts remain excluded:

- **WCAG:** the declarative item tests acronym expansion. A natural evaluative item
  would test criterion recall or some other accessibility concept, not application of
  the acronym expansion.
- **ARIA:** the declarative item also tests acronym expansion. An ARIA implementation
  item would test a particular component or state, not application of the expansion.

The final battery contains **16 primary items: 8 concepts × 2 polarities**.

## 4. Item construction

Each pair contains:

1. one **violation** item with a single, author-verified accessibility fault; and
2. one **conformant** item in which the relevant fault is absent.

Both polarities use the neutral answer frame:

> Based only on the code shown, an accessibility reviewer should mark this example as

The frame permits either `accessible` or `inaccessible because ...`. It does not
assert that a problem exists. Items do not name the target concept in the prompt.

Ground truth was reviewed by the author before the coding rules or confirmatory runs.
The review and caveats are recorded in `docs/audits/paired-battery-readiness.md`.

## 5. Models and decoding

All models are base checkpoints decoded greedily with `do_sample=False` and
`max_new_tokens=100`.

### Confirmatory models (12)

- Pythia: 160M, 410M, 1B, 6.9B, 12B
- GPT-2: 124M, 355M, 774M, 1.5B
- OLMo 2: 1B, 7B, 13B, using the pinned revisions in `src/olmo_config.py`

### Pilot model (reported separately)

- Pythia-2.8B

## 6. Frozen item coding

Every generated item is coded `correct`, `partial`, or `incorrect` by the prompt-
specific rules in `src/paired_evaluative.py`.

For a violation item:

- **correct:** the response classifies the example as inaccessible or failing and
  identifies the pair's specific fault;
- **partial:** the response identifies only that something is inaccessible, or names
  the relevant issue without giving a coherent classification;
- **incorrect:** the response calls the example accessible, identifies another issue,
  or is unrelated or degenerate.

For a conformant item:

- **correct:** the response classifies the example as accessible, conformant, passing,
  or free of the claimed issue;
- **partial:** the response does not make a codeable accessibility judgment;
- **incorrect:** the response classifies the example as inaccessible, or explicitly
  contradicts an accessible classification by asserting the target fault.

Synthetic tests exercise every rule before the freeze. Tests contain authored example
strings only; no model output is used to shape the rules.

## 7. Primary estimand

An evaluative concept **passes only when both its violation and conformant items are
coded correct**. This blocks two trivial strategies: always declaring a problem and
never declaring one.

For every model × concept cell:

- `declarative_pass = declarative accuracy == correct`
- `evaluative_pass = violation correct AND conformant correct`

The full cell state is reported:

1. declarative pass / evaluative pass;
2. declarative pass / evaluative fail (**declarative–evaluative gap cell**);
3. declarative fail / evaluative pass;
4. declarative fail / evaluative fail.

The primary summary is the number and proportion of declaratively correct cells that
fail the evaluative pair, with the denominator printed explicitly. Confirmatory and
pilot cells are never pooled.

No independence-based significance test is applied to the 8 × 12 confirmatory grid.
Concepts repeat across related model scales, and model scales repeat within families.
The complete grid is more informative than a pseudo-replicated p-value.

## 8. Secondary summaries

- Declarative and evaluative pass rates over the same eight concepts at each scale,
  plus their percentage-point difference.
- Item-level correct/partial/incorrect outcomes for both polarities.
- Strict-binary and partial-credit item means, clearly labeled secondary.
- Polarity shortcut counts: violation correct/conformant wrong and the reverse.
- The original five evaluative items remain a historical battery and are not pooled
  into the paired estimator.

## 9. Predictions

1. At least one confirmatory model × concept cell will show declarative pass with
   evaluative failure.
2. The declarative-only state will be more common than the evaluative-only state.
3. Requiring both polarities will reduce evaluative success relative to scoring only
   violation items because some models will invent faults on conformant examples.
4. The size and distribution of the paired gap may differ from the old pooled-means
   gap. The paired result replaces, rather than retroactively validates, that estimator.

## 10. Outcome branches — all ship

- **Gap widespread:** report its exact distribution by concept, scale, and family;
  do not collapse it into a universal claim if exceptions exist.
- **Gap concept-specific or family-specific:** make the heterogeneity the result and
  identify which cells break the pattern.
- **Little or no paired gap:** withdraw the same-concept formulation. Retain the old
  pooled result only as a difference between historical batteries.
- **Conformant items cause broad false positives:** report this as polarity or prompt-
  frame sensitivity, not automatically as lack of concept knowledge.
- **Items produce substantial degeneration or uncodable continuations:** report the
  instrument failure, preserve the outputs, and do not rewrite items after inspection.

## 11. Frozen artifacts and outputs

The freeze commit must contain:

- `data/evaluative_paired.yaml` — renamed from the approved proposal;
- `docs/preregistrations/0002-evaluative-prompts.md` — this protocol;
- `src/paired_evaluative.py` — validation, coding, and analysis;
- `tests/test_paired_evaluative.py` — synthetic rule and aggregation tests.

Each model run writes to a separate paired-battery path, never to the existing
elicitation battery:

- `results/evaluative_paired/{suite}/{model}/{model}-evaluative-paired.csv`
- `results/evaluative_paired/{suite}/{model}/{model}-evaluative-paired.md`

The analyzer writes:

- `results/analysis/paired_item_coded.csv`
- `results/analysis/paired_gap_cells.csv`
- `results/analysis/paired_gap_summary.csv`

No existing `*_gap.csv` file is overwritten.
