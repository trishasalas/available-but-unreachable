# 0015 — Concept key normalization across batteries

- **Status:** accepted
- **Date:** 2026-08-09
- **Audit finding:** A3 (root cause)

## Context

One concept currently has three spellings across three batteries:

| Battery | Key |
|---------|-----|
| Frequency | `closed_captions` |
| Declarative (`data/accessibility.yaml`) | `closed captions` |
| Completion | `captions` |

The declarative form changed in commit `7f84365` (`captions` → `closed captions`).
Only `alt text` survives the completion/declarative concept join as a result, and
`page title` / `script` have no declarative counterpart at all.

The rename did not break the join. It exposed a normalization that was never there — underscore-versus-space was already a live inconsistency between the frequency battery and the elicitation batteries, and the rename simply added a third variant that made the failure visible.

Worth noting how strong the completion-paradox result is *through* this broken join: alt-text-only, 7 greater / 6 ties / 0 less, p = 0.0078.

## Decision

**Chosen: B — normalize at load time**, with the coding layer insulated.

`_canonical_concept` in `src/analysis.py` normalizes `concept` in place.
The on-disk spelling is preserved as `concept_raw`,and `gap_analysis`passes `concept_raw` to `code_response`. Canonical form is lowercase with underscores (`closed_captions`), matching the frequency battery and file-naming conventions.

### Considered and rejected

**A — normalize at write time, in the battery writers.** Require sregenerating every battery, and leaves existing CSVs mismatched unti lthat happens. Load-time normalization is idempotent and fixe shistorical data.

**C — re-key `accuracy_coding.py` to the canonical form.** Rejected :changing the rules table retroactively changes every table and figure in the paper, and DECISIONS requires its own entry for any change there. The 1293-line table is effectively a public API.

## Consequences

Joins across batteries start working. A3's completion paradox can be evaluated with all four concepts rather than alt text alone. The frequency-to-elicitation join used throughout Section III stops depending on the two batteries happening to agree.

Harder: load-time normalization means the on-disk key and the in-memory key differ, which is mildly surprising when debugging. Mitigate by normalizing in exactly one place and naming it obviously.

**Depends on:** `src/accuracy_coding.py` continuing to receive the raw spelling. It dispatches on a 52-key dict in space form, case-sensitively, and `rules.get(concept, {})` returns 'incorrect' on a miss rather than raising. Zero of those 52 keys survive canonicalization — so if any consumer starts passing normalized `concept` to `code_response`, every declarative row codes incorrect and the declarative mean goes to 0.0 with no error.

**Who else reads this:** any code path calling `code_response` or reading `concept` for dispatch rather than joining. Check before changing either column.

---

## Amendment — 2026-08-11

Three factual corrections found during implementation. The decision stands; these
correct the reasoning recorded above.

**1. The commit citation is wrong.** Context says the declarative form changed in
`7f84365`. It did not. `7f84365` is "add missing compounds + make suite iteration
dynamic" — it widened `COMPOUNDS` from 49 to 53 and de-hardcoded `dual_spearman`'s
suite list. The `captions` → `closed captions` rename is in **`ca01b59`** (2026-08-05,
"rearrange results directory structure"). This is the same misattribution CLAUDE.md
already corrected on 2026-08-09, inherited here because this ADR was drafted from the
audit rather than from `git log -S`. The correct commit is now cited in
`src/analysis.py:62` as well.

**2. "All four concepts" overstates what the join gains.** Consequences say A3 "can be
evaluated with all four concepts rather than alt text alone." Post-normalization the
completion battery carries `alt_text`, `closed_captions`, `page_title`, `script`, but
only the first two have a declarative counterpart. `page_title` and `script` are
syntactic controls with *no* declarative arm by design — `code_completion`'s docstring
says so explicitly. Normalization takes the paired set from **1 to 2**, not 1 to 4.
Whether two paired concepts can carry the completion-paradox claim is a live question,
not a foregone gain.

**3. The "three spellings" table is cross-battery, not within-frame.** Inside the
loaded frames the collapse is **2 → 1** (`captions` + `closed captions` →
`closed_captions`, vocabulary 233 → 232). The third spelling lives in the frequency
tables, which the canonical key now *matches* rather than merges. Same fix, smaller
in-frame footprint than the table implies.

**Also incomplete: "Who else reads this."** It names the class correctly but no
instances, and the implementing brief named only `gap_analysis`. There are **two**
dispatching consumers, with four call sites total: `src/gap_analysis.py` (row coding;
and the emergence-threshold loop, which passed its normalized *loop variable*) and
`src/dual_spearman.py` (`code_response` **and** `observe_sense` — the latter dispatches
on `A11Y_SENSE_MARKERS`, also space-form, also silent on a miss). Missing
`dual_spearman` would have zeroed the frequency correlation's `y` and flipped every row
to `generic` sense, with no error. The instance list now lives in `src/analysis.py`'s
module docstring, next to the code, where it can be checked against `grep`.

**Follow-up this suggests (not part of this decision).** The dispatch/join distinction
is load-bearing and enforced entirely by comments. The durable fix is for
`code_response` to raise on an unknown concept instead of returning `'incorrect'` —
then a leaked normalized key fails at the first row rather than at the mean. That is a
change to `accuracy_coding.py` and needs its own decision.

## Implementation — 2026-08-11

- `src/analysis.py`: `_normalize_concept_column` sets `concept_raw` to the on-disk
  spelling and canonicalizes `concept`, in one place, after concat. Returns a
  vocabulary report printed on every load (`233 -> 232`, collapses listed by canonical
  form) rather than documented once.
- `compound` (binding) deliberately left alone — all 227 values verified already
  canonical, so normalizing there would be a no-op that reads as a safeguard.
- `src/gap_analysis.py` (2 sites) and `src/dual_spearman.py` (2 sites) pass
  `concept_raw` to the coding layer. `src/accuracy_coding.py` untouched.
- Verified no-op on every number: `pythia_gap` / `gpt2_gap` / `olmo_gap` byte-identical
  to a pre-change baseline; declarative pivot n=10 and evaluative n=5 with identical
  members; pythia-160M declarative 0.5; `source` counts unchanged (elicitation
  2925/533, entropy 2751/533, binding 1723904/426240); `dual_spearman` reproduces the
  frozen `compound_accuracy_table.csv` with 0 differing cells across all three suites.
- Strongest guard: `elicitation_coded` joined before/after on `(model, prompt_id)` —
  3458/3458 rows, **accuracy changed on 0 rows**.
- Label-only changes in the pivots and per-concept tables; genuine merges confined to
  the one collapsed concept in `emergence_thresholds` (59→58, dropping a phantom
  `captions` row that read `never/never/never`), `degenerate_by_concept` (233→232),
  `entropy_confidence` (897→881), and `completion_paradox` (702→689). Every other row
  in each verified identical.
- `results/` not regenerated, per the implementing brief. Note that
  `results/analysis/*.csv` predate `aa7e1bb` and so do not match current code output —
  the baseline for "byte-identical" was a fresh pre-change run, not the on-disk tables.
- Reported, not fixed: `src/accuracy_coding.py` ~line 295 claims declarative data uses
  `captions` and that `closed captions` appears "only as control", calling its
  `'closed captions'` rule a no-op. Reversed — there are 13 declarative
  `closed captions` rows (pythia 6, gpt2 4, olmo 3) and zero declarative `captions`, so
  that rule is the only one doing any work for the concept. Its own decision.
