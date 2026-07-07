# NEXT.md — Open work queue
Session-to-session work items. This file is the boot pointer: what's on
deck, not what's true (CLAIMS.md is the ledger; DECISIONS.md is the
record). Items leave this list by being done and committed, with a
pointer to the commit.

---

## Before submission

- [ ] **B4 denominator reconciliation (51 vs 49).** The trajectories
  file (`results/analysis/per_concept_trajectories.csv`) carries 51
  concepts; the Spearman set is n=49. Identify and document the two
  exclusions so the counts in B4's row (4/2/1 of 49) and Section 05's
  n agree on paper. The CLAIMS.md B4 row carries the note verbatim;
  a careful reviewer will count. (Flagged by CC at session close
  2026-07-06.)

## Cheap / cosmetic (optional)

- [ ] **Explicit artifact paths in the D6 verdict text.** Commit
  103bf81 bundles the verdict with its notebook and CSVs, so the
  record is atomic regardless — this is insurance for file moves, not
  structure. Add the two CSV paths + notebook path as a one-line
  cross-reference in the DECISIONS 2026-07-06 verdict entry if wanted.

## Tracked elsewhere (do not duplicate here)

- Open pre-submission experiments live as D-rows in
  `docs/findings/CLAIMS.md` §D (e.g., D1 BOS diagnostic — "cheap; do
  before submission"; D2 L29/H7 rigor pair). That table is their
  single source of truth; this file only points.
- D9's graduation condition is a ratified rule in DECISIONS.md
  (2026-07-07), not a task.
