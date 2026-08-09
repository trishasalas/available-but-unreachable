# Pending decisions — 2026-08-08

Drafted as DECISIONS.md entries. Each needs adjudication **before** the next pipeline
run, because a rerun either silently undoes the decision or entrenches the current
behavior as if it had been chosen.

Numbering starts at D9 — note that DECISIONS.md currently has **two entries labeled D7**
(`Binding battery consolidated across domains (2026-08-08)` collides with the
pre-existing `Single-token-ban counterfactual`). CLAIMS A2/C6/D7 refer to the token-ban
one, so the new entry is the one that should be renumbered.

---

## D9 — Source flag for expansion compounds (A6)

**Problem.** `gap_analysis.py:76-78` filters `source == 'original'` with a comment
explaining that the 41 frequency-stratified expansion compounds must not be pooled into
the declarative/evaluative paradigm means. `analysis.py:66` hardcodes
`source = 'original'` on every loaded row. Elicitation CSVs carry no `source` column, so
the filter has never removed anything. The intent survives perfectly in a comment; the
enforcement does not exist.

**Impact.** Declarative pivots are computed over 51 concepts; the headline gap compares
a 51-concept declarative mean against a 5-concept evaluative mean. Pythia-160M
declarative over all 51 = 0.7059 (matches the shipped table); restricted to the 10
original concepts = 0.5. Twenty points, on one side of a difference-of-means.

**Decision needed.** Interim hardcoded set in `analysis.py`, or a real `source` field
propagated from `data/binding/*.yaml` through the battery writers?

**Recommendation.** Hardcoded set now (unblocks Phase 2 today), YAML field folded into
the Phase 4 regeneration. Record the interim as a decision so it doesn't become another
comment that outlives its enforcement.

---

## D10 — Gap estimand: pooled means or paired concepts?

**Problem.** Separate from D9 but exposed by it. Even with a working source filter, a
difference of pooled means compares two different concept populations. The evaluative
battery covers 5 concepts; the declarative battery covers many more.

**Decision needed.** Is the gap (a) declarative mean minus evaluative mean over the
original concept set, or (b) a paired comparison restricted to concepts that have both a
declarative and an evaluative item?

**Recommendation.** (b). It resolves the estimand problem and the power problem in the
same move, and it matches the claim actually being made — a floor on evaluative
capability, not an average difference. Under (b), 5 items × 13 models = 65 observations
supporting a uniformity claim, which is the right shape.

---

## D11 — OLMo x-corpus for the frequency battery (A4)

**Problem.** The OLMo robustness battery mixes corpora: partial correlation, Kendall,
and bootstrap use Pile x-values while the primary uses Dolma. Four contradictory
OLMo-1B rhos currently exist on disk.

**Decision needed.** Does OLMo correlate against Dolma (its actual training corpus,
methodologically correct, but not comparable to the Pile-based pythia/gpt2 numbers) or
against the Pile (comparable, but wrong corpus for that family)?

**Notes.** Whichever is chosen, the corpus must be recorded in a column on the output
file — the current `frequency_table.csv` has no corpus/index column, so provenance is
unrecoverable from the artifact itself. Reporting both is defensible if the primary is
clearly designated.

---

## D12 — Archival status of the five `results/analysis` tables (A11)

**Problem.** Five tables were archived out of `results/analysis` this week, but they are
still written by the pipeline, read by a figure script, and cited by findings docs. The
next run recreates them.

**Files:** `completion_paradox.csv`, `criteria_strictness_audit.csv`,
`criteria_strictness_audit_full.csv`, `emergence_thresholds.csv`,
`trajectory_stability_audit.csv` (all currently untracked in `results/_archive/`).

**Decision needed.** Archived (stop writing them, fix the readers) or canonical (move
back, keep writing)? Note that `completion_paradox.csv` is A3's evidence and
`trajectory_stability_audit.csv` is cited by CLAIMS B3/B6 — those two may need to come
back regardless of the general policy.

---

## D13 — `pythia-13b` vs `pythia-12b` naming (A15)

**Problem.** The binding battery names the largest Pythia checkpoint `pythia-13b`;
elicitation and entropy call the same checkpoint `pythia-12b`. `analysis.py` has an
alias handling the 13b case, which works but hides the inconsistency.

**Decision needed.** Standardize on one. The upstream/published name is
`pythia-12b`, which argues for renaming the binding outputs and retiring the alias.

**Why now.** The next binding run re-entrenches whichever name is in the notebook.

---

## D14 — Concept key normalization (A3 root cause)

**Problem.** One concept currently has three spellings across batteries:
`closed_captions` (frequency), `closed captions` (declarative, post-`7f84365`),
`captions` (completion). Only `alt text` survives the completion/declarative join as a
result, and `page title` / `script` have no declarative counterpart at all.

**Decision needed.** Canonical key form, and where normalization happens — at write time
in the battery writers, or at load time in `analysis.py`?

**Recommendation.** Load time, one function in `analysis.py`, applied to every frame.
Write-time normalization means regenerating everything and leaves existing CSVs
mismatched. Load-time is idempotent and fixes historical data too.
