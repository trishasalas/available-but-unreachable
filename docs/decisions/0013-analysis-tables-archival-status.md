# 0013 — Archival status of five `results/analysis` tables

- **Status:** proposed
- **Date:** 2026-08-09
- **Audit finding:** A11, A10

## Context

Five tables were archived out of `results/analysis` during the 2026-08-08 cleanup, but
they are still written by the pipeline, still read by a figure script, and still cited
by findings docs. The next run recreates them in their original location.

Affected files:

- `completion_paradox.csv`
- `criteria_strictness_audit.csv`
- `criteria_strictness_audit_full.csv`
- `emergence_thresholds.csv`
- `trajectory_stability_audit.csv`

Two of these are load-bearing. `completion_paradox.csv` is the evidence for A3's
completion-paradox claim, and `trajectory_stability_audit.csv` is cited by CLAIMS
B3/B6. CLAIMS' own shipping gate says claims whose evidence lives only in an archive
do not ship — which currently describes A4, A5, and D6 (audit A10).

As of 2026-08-09 these have been moved again, into `_Archive/_results/`, and are now
tracked in git. `paper/generate-figures/generate-fig-completion-paradox.py:51` reads a
path that no longer exists in either location.

## Status of the files as of 2026-08-09

Two have been **restored to `results/analysis/`** because CLAIMS cites them directly:

- `completion_paradox.csv` — A3's evidence
- `trajectory_stability_audit.csv` — B3's demotion evidence (the 20/102 stability
  finding that downgraded the trajectory taxonomy from empirical contribution to
  descriptive vocabulary)

Three remain archived, with **zero mentions in CLAIMS.md**:

- `criteria_strictness_audit.csv`
- `criteria_strictness_audit_full.csv`
- `emergence_thresholds.csv`

No claim depends on these three. That is the strongest available argument that
archiving them was right, and it is a weaker argument than a recorded rationale would
have been.

Separately, a set of files was already in `results/_archive/` **before** the 2026-08-08
cleanup and was only relocated to `_Archive/_results/` on 2026-08-09. Four of those
*are* cited by CLAIMS and constitute audit finding A10 in concrete form:
`pythia-2.8b-multihead-ablation.csv` and `pythia-2.8b-candidate-heads.csv` (D6/A5),
`pythia-2.8b-collocation.csv` (×2), `pythia-2.8b-head-characterization.csv` (×3).
CLAIMS' own shipping gate says a claim whose evidence lives only in an archive does
not ship. These need re-homing or the claims need re-scoping.

## Decision

*(pending)*

**Author's stated instinct, 2026-08-09:** "my first reaction is to put those files back
 and I don't know (or remember) why they were moved in the first place."

That is itself evidence. An archiving action whose rationale is unrecoverable a day
later is not a decision, it is a tidying reflex. The burden should therefore sit on
*keeping them archived* rather than on restoring them — if no one can reconstruct the
reason, the default is canonical.

**A. Archived.** Stop writing them, fix or retire the readers, re-home the evidence
that NAILED claims depend on.

**B. Canonical.** Move back to `results/analysis`, keep writing them, keep the figure
script pointed at them.

A hybrid is likely correct: files cited by CLAIMS return to canonical; uncited
diagnostics stay archived.

## Consequences

Under A, every reader must be fixed before the next run, or figures break silently at
generation time rather than loudly at load time.

Under B, `results/analysis` stays cluttered with one-off diagnostic output that is not
part of the paper's evidence chain — which is the condition that prompted the cleanup.

**Depends on:** knowing which claims cite which files. CLAIMS.md is the source of
truth here, and the mapping should be verified rather than assumed before anything is
deleted or stops being written.

## Process note

This decision exists because five files were moved without a recorded reason. The cost
showed up within 24 hours: the author could not reconstruct the rationale, a NAILED
claim's evidence went untracked, and a figure script broke silently.

The generalizable rule is not "archive less." It is that **moving a results file is a
decision**, because results files are cited. A one-line note at the moment of the move
— what was moved and why — would have made this entire entry unnecessary.
