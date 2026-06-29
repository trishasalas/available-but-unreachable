# Design: multi-head joint-ablation expansion of `lexical-head.ipynb`

**Date:** 2026-06-29
**Status:** approved (design); spec pending user review
**Notebook:** `notebooks/lexical-head.ipynb`
**Model under test:** `pythia-2.8b`

## Motivation

`lexical-head.ipynb` currently dissects a *single* head — `L29/H7`, the one
genuine lexically-selective binder for "screen reader" surfaced by head
characterization. Its three sections (QK selectivity, OV write, single-head
causal ablation) establish that the head *routes* and *writes* screen-reader
content selectively, yet ablating it changes the next-token distribution by
`KL ≈ 1e-5` — essentially nothing.

That null is the interesting part. A single-head ablation cannot distinguish "the
mechanism is elsewhere" from "the mechanism is distributed across a set of heads."
This expansion makes the move single-head analysis structurally cannot: **jointly
ablate an earned set of heads** to test whether the binding lives in a small
circuit or is genuinely distributed.

## Claim the notebook licenses

> Even the strongest lexical lead (screen reader) is **distributed** across heads,
> not a localized circuit.

Scope is deliberate. Screen reader is the *hardest case for the null to survive*
— it has the strongest single-head binding of the 11 compounds in the binding
sweep, so if even it is distributed, weaker compounds are distributed a fortiori.
The notebook is a **zoom-in** that sits inside a paper already carrying breadth
(binding sweeps across 11 compounds × 6 Pythia sizes in `results/pythia/`); it does
not need to re-establish generality. The prose must stay scoped to the exemplar —
"the strongest lexical lead is distributed," never the unscoped "compound binding
is distributed."

## The load-bearing design decision: *which* head set gets ablated

Raw top-binding heads for `screen_reader` are **early structural heads**
(`L1/H12` is top-1 for 9 of 11 compounds — domain-general previous-token
plumbing). Those are load-bearing for *everything*, so ablating them moves KL —
but that says nothing about *lexical* binding.

The claim concerns the **deep lexical binders** (the `L29/H7` family). Therefore:

- Stage A **excludes** early structural heads via a `min_layer` filter and keeps
  only deep + selective + non-sink heads. The cumulative ablation runs over *that
  earned set*, not the raw top-k.
- `min_layer` default = **10**, refined from the Stage A characterization table
  rather than hardcoded blindly. (Derived-not-hardcoded is the existing rule in
  `head_characterization.py`.)
- The excluded structural heads are not discarded — they become a **labeled
  contrast**: structural heads *do* move KL; the deep lexical set does not. That
  sharpens, rather than weakens, the distributed result.

## Stage A — earn the candidate set (new notebook section)

Reuse `src/head_characterization.py` unchanged:

1. Read `results/pythia/pythia-2.8b-binding.csv`, filter `compound == screen_reader`.
2. Drop early layers (`min_layer = 10`), take top-N deep heads by `binding_score`
   (N ≈ 15–20 so the deep tail is captured).
3. Characterize each candidate:
   - `characterize_heads` → induction / prev-token / dup-token scores + type.
   - `attention_to_bos` and `attention_to_position(position=1)` → sink / structural flags.
   - `collocation_scan` → selectivity = screen-reader score vs. max other-domain score.
4. Define the **earned lexical set** = deep ∧ selective ∧ not (sink ∨ structural).
   `L29/H7` is expected to be a member; the table reveals who else qualifies.

**Output:** `results/pythia/pythia-2.8b-candidate-heads.csv` (one row per candidate
head with all diagnostic columns and a boolean `in_lexical_set`).

## Stage B — joint ablation (new notebook section + new module functions)

New in `src/qk_ov.py`:

- `ablate_heads_at_position(model, prompt, heads, dest_word, top_k=10)` —
  generalizes the existing singular `ablate_head_at_position` to a **list** of
  `(layer, head)` tuples, all zeroed at the `dest_word` position in one forward
  pass. Returns `KL(base || ablated)` and top tokens before/after, same shape as
  the singular function.
- Refactor `ablate_head_at_position` into a thin wrapper calling the plural with
  `[(layer, head)]` — preserves existing cells 12–13 and gives a free regression
  test.
- `cumulative_ablation(model, prompt, ordered_heads, dest_word)` →
  `DataFrame[n_ablated, heads, kl]` by ablating growing prefixes of
  `ordered_heads`. Heads are ordered by `binding_score` descending (knock out the
  strongest binders first). This one function yields the cumulative-knockout curve
  **and its own positive control**: extend the set into the late layer and KL must
  eventually rise — if it only rises there (not within the lexical set), that is
  simultaneously the distributed result and proof the ablation hook works.

Controls:

- **Negative (specificity):** the earned screen-reader set ablated on
  `"A bicycle wheel is"` at the `wheel` position → expect flat (these heads do not
  bind there). Reuses the existing notebook control compound.
- **Positive (validity):** the right tail of the cumulative curve (set grown into
  a late layer) → KL must climb, proving the instrument can detect an effect.

## §C — robustness panel (new notebook section)

Repeat Stage A + Stage B for 3 additional compounds spanning domains and binding
depths, drawn from the binding CSV:

- `alt_text` — another a11y compound.
- one non-a11y compound — default `stock_market` (finance); swappable for
  `blood_pressure` (medical) if its tokens resolve more cleanly in Stage A.
- `semantic_html` — binds *deep* at `L30`, a different locus from screen reader;
  the strongest available test that the null is not a quirk of one layer.

Expected outcome: four near-flat cumulative curves. This is *support* for the
exemplar claim, not the claim itself — it removes a reviewer's "does it
generalize?" objection without the headline depending on it.

## Outputs

- `results/pythia/pythia-2.8b-candidate-heads.csv` — Stage A characterization table.
- `results/pythia/pythia-2.8b-multihead-ablation.csv` — cumulative KL curves for
  all compounds + controls (columns: `compound`, `n_ablated`, `heads`, `kl`,
  `role` ∈ {primary, neg_control, robustness}).
- Figure via a `generate-figures/` script (reproducible from the CSV per repo
  convention, never hand-drawn): cumulative-KL-vs-set-size for screen reader +
  negative control + 3 robustness compounds. Atkinson Hyperlegible font, navy /
  light-blue palette.

## Notebook structure

Keeps the current three-section rhythm, extended:

1. Setup — unchanged, plus load `pythia-2.8b-binding.csv`.
2. §1 QK selectivity — unchanged (already multi-compound via `collocation_scan`).
3. §2 **Earn the candidate set** (new) — Stage A table.
4. §3 OV write — keep the `L29/H7` exemplar logit-lens.
5. §4 **Joint ablation + controls** (new) — cumulative curve, negative + positive controls.
6. §5 **Robustness panel** (new) — 3 additional compounds.
7. §6 Save CSVs.

## Error handling

- `find_token_index` returns `None` for absent tokens; `collocation_scan` already
  warns and skips. New ablation paths guard the same way — skip a compound whose
  `word2` is not locatable rather than indexing `None`.
- Multi-token second words: destination index uses `find_token_index` (subword
  aware), consistent with existing modules; if a compound's word2 spans multiple
  tokens, ablate at its final sub-token position and note it.
- Single model load; no inter-model memory churn needed in this notebook.

## Testing

In-notebook sanity asserts on the new module functions:

- `ablate_heads_at_position(model, SR_PROMPT, [], "reader")` → `KL == 0`.
- `ablate_heads_at_position(model, SR_PROMPT, [(29, 7)], "reader")` reproduces the
  existing singular `ablate_head_at_position` KL (regression on the refactor).
- A large late-layer head set → `KL > 0` (positive control fires; the instrument
  is not silently inert).

## Out of scope (YAGNI)

- All-11-compound sweep — the paper's broad binding sweep already covers breadth;
  the robustness panel's 3 compounds are sufficient insurance.
- Path patching / activation patching — joint zero-ablation answers the
  localized-vs-distributed question; richer causal methods are a separate study.
- Cross-model replication of the joint ablation — single-model (`pythia-2.8b`)
  here; other sizes are future work.
