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

The rename did not break the join. It exposed a normalization that was never there —
underscore-versus-space was already a live inconsistency between the frequency battery
and the elicitation batteries, and the rename simply added a third variant that made
the failure visible.

Worth noting how strong the completion-paradox result is *through* this broken join:
alt-text-only, 7 greater / 6 ties / 0 less, p = 0.0078.

## Decision

*(pending)*

**A. Write time.** Normalize keys in the battery writers. Requires regenerating
everything and leaves existing CSVs mismatched until they are.

**B. Load time.** One normalization function in `src/analysis.py`, applied to every
frame as it is loaded. Idempotent, fixes historical data, no regeneration needed.

Recommended: B. Canonical form to be chosen — lowercase with underscores
(`closed_captions`) matches the frequency battery and file naming conventions.

## Consequences

Joins across batteries start working. A3's completion paradox can be evaluated with
all four concepts rather than alt text alone. The frequency-to-elicitation join used
throughout Section III stops depending on the two batteries happening to agree.

Harder: load-time normalization means the on-disk key and the in-memory key differ,
which is mildly surprising when debugging. Mitigate by normalizing in exactly one
place and naming it obviously.

**Depends on:** the normalization being applied to *every* frame, not just
elicitation. A frame that skips it joins against nothing and produces an empty result
rather than an error — which is precisely how A3 stayed invisible.
