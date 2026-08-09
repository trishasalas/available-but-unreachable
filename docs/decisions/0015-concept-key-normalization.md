# 0015 — Concept key normalization across batteries

- **Status:** proposed
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
