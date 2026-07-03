# Coding criteria for the n=49 expansion — DRAFT worksheet

> **Status: DRAFT** — skeleton by Claude (Fable 5), 2026-07-01. Trisha authors
> the actual criteria. **Discipline: keep `results/frequency/` CLOSED while
> writing criteria.** Criteria are about semantics; authoring them blind to
> bigram counts is the pre-registration that protects the Spearman.

## Where coding happens (the answer to "where do I do the coding")

You never hand-label responses. The criteria ARE code:

1. Author criteria per compound **in this file** (from elicitation outputs only).
2. Translate them into `src/accuracy_coding.py` (concept-specific rules, documented inline — existing convention).
3. Paste the completed DECISIONS entry below into `DECISIONS.md` (your 2026-06-28 policy: criteria changes require an entry).
4. Run `python -m src.gap_analysis` (or `notebooks/analysis.ipynb`).
5. `results/analysis/per_concept_trajectories.csv` regenerates with the new compounds' trajectory classes → rerun the Spearman → `results/frequency/spearman_summary.csv` at n=49.

No GPU. All local.

## Policy decision to make FIRST (applies to every compound uniformly)

Several new compounds have a dominant **non-accessibility sense** in general
text: `sign_language`, `menu_bar`, `form_field`, `target_size`, `character_key`,
`low_vision`, `combo_box`, `tool_tip`, `reading_order`, `responsive_design`.

Decide once, write it once, apply everywhere:

- [x] **Option A — general technical sense counts as `correct`** (consistent
      with how a practitioner would accept "a menu bar is a GUI element…").
- [ ] **Option B — accessibility-specific sense required** (stricter; risks
      coding real knowledge as `partial`).

**DECIDED 2026-07-02 (Trisha + Fable 5): Option A, with sense recording.**
Rationale: A matches the original 8's practitioner standard. Addendum
(protects the Spearman): the ambiguous compounds are disproportionately the
high-frequency ones, and generic definitions are exactly what high frequency
buys — so Option A alone would let those rows flatter the frequency↔accuracy
correlation. Mitigation: each coded response ALSO records observed sense
(a11y / generic), mechanized via per-compound `a11y_sense_markers` (authored
in `_analysis/criteria_authoring.csv`, esp. AMBIGUOUS rows). Analysis reports
the Spearman both ways — all rows and a11y-sense-only — pre-answering the
menu_bar reviewer from either direction. Carry into the DECISIONS entry.

## DECISIONS.md entry skeleton (fill, then paste)

```markdown
### 2026-07-__ — Coding criteria for 41 expansion compounds (n=49 frequency analysis)

**Decision:** Added concept-specific coding criteria for the 41 compounds
introduced in the frequency expansion (`src/frequency.py`). Criteria authored
blind to corpus frequency values (frequency_table.csv not consulted during
authoring; authored in docs/findings/coding-criteria-draft.md, committed
[COMMIT HASH] before gap_analysis was rerun).

**Sense policy:** [Option A / B from worksheet, one sentence].

**Coding scheme:** unchanged (correct / partial / incorrect, per 2026-06-28
framework entry). Criteria are concept-specific; see src/accuracy_coding.py.

**Scope of change:** elicitation_coded.csv gains rows for the 41 new concepts;
the original 8 compounds' coding is UNTOUCHED (regression check: their rows in
per_concept_trajectories.csv must be byte-identical before/after).

**Downstream:** per_concept_scaling.csv, per_concept_trajectories.csv,
spearman_summary.csv regenerate at n=49.
```

## Criteria template (one block per compound)

```markdown
### {compound} ({domain sense policy note if ambiguous})
- correct: output demonstrates [core meaning — one sentence, practitioner test]
  · marker tokens/patterns: [e.g., contains "announce" or "assistive" or …]
- partial: right domain, misses the key point [what's the key point?]
- incorrect: wrong domain / circular / degenerate / nonsense
- notes: [ambiguity risks, WCAG SC number if applicable, known confusions]
```

Illustrative example (NOT final — check against actual elicitation outputs):

```markdown
### live_region
- correct: dynamic page area whose content changes are announced to assistive
  tech / screen readers without focus moving
  · markers: announce/announced, screen reader, update/dynamic + assistive
- partial: "part of a page that updates" with no announcement/AT connection
- incorrect: geography, broadcasting, "a region that is live"
- notes: ARIA concept; watch for circular "a live region is a region that is live"
  (degenerate detector should catch loops, but circularity ≠ repetition)
```

## The 41 new compounds (from frequency_table.csv, a11y domain, minus the original 8)

keyboard_interaction · section_heading · text_alternative · audio_description ·
sign_language · sensory_characteristics · input_purpose · target_size ·
touch_target · drag_movement · focus_appearance · consistent_help ·
redundant_entry · accessible_authentication · text_spacing · status_message ·
error_identification · pointer_cancellation · character_key ·
accessibility_tree · accessible_name · accessible_description · live_region ·
tab_panel · radio_group · tree_grid · menu_bar · tool_tip · **combo_box** ·
semantic_markup · focus_management · reading_order · text_formatting ·
form_field · landmark_region · low_vision · cognitive_disabilities ·
universal_design · decorative_image · informative_image · responsive_design

**Count verified 41 against docs/findings/coding_coverage.csv (path updated
2026-07-03), 2026-07-02 (Fable 5):**
the original transcription above had 40 entries — combo_box was dropped
(present in the sense-policy list, missing from the enumeration). Restored.
Authoring worksheet `docs/findings/criteria_authoring.csv` carries all 41.

## Carry-forward (analysis decisions, NOT coding — separate session)

- Ordinal encoding: justify mixed=1 < peak_regress=2, or robustness-swap.
- GPT-2 word1 confound (0.73 vs 0.78 at n=8): n=49 is the test; report both.
- Original 8 rows must be byte-identical post-rerun (regression guard above).

---

## STATUS: AUTHORING COMPLETE 2026-07-03

All 41 criteria AUTHORED in `docs/findings/criteria_authoring.csv` (moved
from gitignored `_analysis/` 2026-07-03; coverage map moved alongside).
Canonical
record: **tmlr/DECISIONS.md entry 2026-07-03** (sense policy, five-plank
coding doctrine, pre-registered predictions, three placements awaiting
Trisha ratify/veto). Pipeline + role assignments:
`docs/findings/criteria-handoff-2026-07-03.md`. This draft file is now
provenance; the worksheet + DECISIONS entry are the source of truth.
