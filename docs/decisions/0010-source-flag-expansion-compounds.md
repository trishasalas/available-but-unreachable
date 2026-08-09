# 0010 — Source flag for expansion compounds

- **Status:** accepted
- **Date:** 2026-08-09
- **Audit finding:** A6

## Context

`gap_analysis.py:76-78` filters `source == 'original'`, with a comment explaining that
the frequency-stratified expansion compounds must not be pooled into the
declarative/evaluative paradigm means. `src/analysis.py:66` hardcodes
`df['source'] = 'original'` on every loaded row, unguarded — note that the adjacent
`domain` assignment two lines above *is* guarded (`if 'domain' not in df.columns`).

Elicitation CSVs carry no `source` column at all. Confirmed: `elicitation_coded.csv`
source value_counts is `{'original': 3458}`. The filter has never removed a single
row. It has been decorative since the per-domain layout landed.

**Impact.** Declarative pivots are computed over 51 concepts, so the headline gap
compares a 51-concept declarative mean against a 5-concept evaluative mean. Pythia
160M declarative over all 51 = 0.7059, matching the shipped `pythia_gap.csv`;
restricted to the 10 original concepts = 0.5. Twenty points, on one side of a
difference of means. This is also the source of the impossible negative gap at
Pythia-6.9B.

The concept split is unambiguous in `data/accessibility.yaml`, which separates
"DECLARATIVE — Original Paper 1 Experiment 1 prompts" from "DECLARATIVE (expansion)"
by section comment. The ten originals are: screen reader, WCAG, skip link, alt text,
ARIA, focus indicator, keyboard navigation, color contrast, semantic HTML, closed
captions (`decl_captions_001`, renamed from `captions` in commit `7f84365`).

**The decision was already recorded, correctly, and was never enforced.** See
`DECISIONS.md`, "Gap-table sampling-frame partition" (2026-07-03):

> The declarative-evaluative GAP is a paradigm-level mean over the
> elicitation-experiment concept set (declarative over 10 concepts, evaluative over 5
> — never a matched per-concept pair). The 41 expansion compounds are
> frequency-stratified probes carrying only the declarative arm; pooling them would
> depress the baseline BY CONSTRUCTION. `load_all_results` tags each row `source` in
> {original, expansion}; `gap_analysis` restricts only the gap pivots to
> `source=='original'`.

That entry states the rationale, names the mechanism, and names the exact function
that implements it. `load_all_results` does not tag rows in {original, expansion} — it
hardcodes `'original'`. The decision, the comment in `gap_analysis.py`, and the
implementation diverged silently and nothing failed.

Worth noting the prediction was also directionally wrong: pooling was expected to
*depress* the baseline. It inflated it (160M declarative 0.5 → 0.7059), because the
frequency-stratified expansion set spans a frequency range that includes easier
high-frequency concepts. This is a second reason the enforcement mattered — the error
did not look like the anticipated error.

### Amendment, 2026-08-09 — the discriminator is not concept membership

Found while implementing, before the Decision section had been filled in. The
framing above ("the ten originals ... everything else is expansion") is stated in
terms of *concepts*, and that is not sufficient.

The evaluative arm has five concepts: `alt text`, `empty link`, `form label`,
`link text`, `semantic HTML`. **Only two of them are in the ten originals.** A
`source` flag derived from bare concept membership therefore tags `empty link`,
`form label` and `link text` as `expansion`, and `gap_analysis`'s filter cuts the
evaluative pivot from five concepts to two — moving the *other* side of the same
difference of means this decision exists to correct.

It would not have been caught. The verification named below is
`pythia-160M declarative == 0.5`, which passes regardless, because the declarative
arm is unaffected by what happens to the evaluative arm. A second silent error,
inside the fix for the first one, behind a green check.

What makes it visible is that
`_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv` carries an evaluative
column too — `0.2, 0.4, 0.2, 0.6, 1.0, 1.0` — byte-identical to the current
(wrong) run. Evaluative is *already* correct at five concepts and must not move.
The reference is a 6×3 oracle, not a single number.

The correct discriminator is the YAML **section**, not the concept. All 41
expansion prompts are `accessibility` + `declarative`. The evaluative prompts are
Paper 1 originals that happen to name concepts outside the declarative ten.

## Decision

**We will take option A, with the membership test scoped to the declarative arm.**

A row is `expansion` iff **all** of: `domain == 'accessibility'`, `prompt_type ==
'declarative'`, and its concept is outside the ten originals. Everything else is
`original`. Frames with no `prompt_type` (binding) fall back to concept membership
alone, which is the intended reading there — every non-original compound in the
binding battery is an expansion compound.

The ten originals live as a frozenset in `src/analysis.py`, derived from the
section boundary in `data/accessibility.yaml` rather than transcribed. The
assignment is guarded (`if 'source' not in df.columns`) like the adjacent `domain`
line; the unguarded write was the original defect and is not reproduced. Load
emits original/expansion counts per frame.

**Option B remains the durable fix** — an explicit `source:` field on each YAML
entry, propagated through the battery writers, so the intent lives in data rather
than in a comment. Folded into the Phase 4 frequency regeneration. A is superseded
at that point.

The two rejected alternatives, recorded so they are not re-proposed: bare concept
membership (amputates the evaluative arm, above), and filtering on `prompt_id`
prefix (`decl_*` covers both original and expansion declarative prompts, so it
does not discriminate).

## Consequences

Gap tables become re-derivable against a known concept population. Verified
2026-08-09 against the full reference table, not just the headline cell:

| scale | decl (ref → got) | eval (ref → got) |
|-------|------------------|------------------|
| 160M  | 0.5 → **0.5** ✓  | 0.2 → **0.2** ✓  |
| 410M  | 0.8 → **0.8** ✓  | 0.4 → **0.4** ✓  |
| 1B    | 0.6 → **0.6** ✓  | 0.2 → **0.2** ✓  |
| 2.8B  | 1.0 → 1.2        | 0.6 → **0.6** ✓  |
| 6.9B  | 1.4 → 1.3        | 1.0 → **1.0** ✓  |
| 12B   | 1.0 → 0.9        | 1.0 → **1.0** ✓  |

The declarative pivot is now n=10 and the evaluative n=5. The impossible negative
gap at Pythia-6.9B (−0.0392) is gone (+0.3).

The three declarative residuals are **not** attributable to this decision and were
not adjusted to. A source filter selects a concept population identically at every
scale; three scales reproduce exactly, and the population verifies correct. The
reference is byte-identical to `results/analysis/pythia_gap.csv` at `0f116a5`
(2026-06-27), which predates both `ca0319e` (the 41 expansion criteria and coding
doctrine, 2026-07-03) and `ca01b59` (`max_tokens` standardized 10/20 → 100,
2026-08-05). Both the coding rules and the underlying generations changed beneath
it. Whether the June 27 table or the current pipeline is authoritative is a
separate question and is **not** settled here.

Harder: option A puts a concept list in code that must be kept in sync with the
YAML by hand. That is exactly the failure mode this decision is fixing, which is
why it is explicitly interim rather than quietly permanent.

Also harder: `source` is now a flag whose meaning is only defined inside the
accessibility domain. Control, medical, legal and finance rows are tagged
`original` because the original/expansion axis does not apply to them, not because
they are Paper 1 originals. Every consumer filters on `domain` first, so this is
currently harmless — but `original` on a medical row is not a claim about Paper 1
and must not be read as one.

**Depends on:**

- `ORIGINAL_CONCEPTS` in `src/analysis.py` staying in sync with
  `data/accessibility.yaml` **by hand**. Nothing enforces this. Adding an
  eleventh original concept to the YAML silently excludes it from the gap tables.
  Includes `closed captions`, **not** `captions` — getting that wrong drops to
  nine concepts with no error.
- The 41 expansion prompts remaining declarative-only. If an expansion compound
  ever gains an evaluative prompt, the `prompt_type == 'declarative'` clause stops
  discriminating and that row pollutes the evaluative mean.
- Every consumer of `source` filtering on `domain` first — otherwise the
  non-accessibility `original` rows described above become a real error.
- `gap_analysis.py` continuing to apply the filter only to the gap pivots. It is
  deliberately not applied to the emergence-threshold table or the extended
  analyses, which characterize the full 51-concept population on purpose.
- **Not** on concept-key normalization (0015), contrary to the original draft of
  this line. Normalization is applied inside the membership test via
  `_canonical_concept`; the `concept` column itself is left un-normalized because
  `accuracy_coding.py` dispatches on it in space form, case-sensitively. The two
  decisions are now independent — 0015 can be ruled either way without moving
  these numbers.
