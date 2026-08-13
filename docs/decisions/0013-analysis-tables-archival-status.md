# 0013 — Archival status of five `results/analysis` tables

- **Status:** accepted
- **Date:** 2026-08-09
- **Audit finding:** A11, A10

## Context

Five tables were archived out of `results/analysis` during the 2026-08-08 cleanup, but they are still written by the pipeline, still read by a figure script, and still cited by findings docs. The next run recreates them in their original location.

Affected files:

- `completion_paradox.csv`
- `criteria_strictness_audit.csv`
- `criteria_strictness_audit_full.csv`
- `emergence_thresholds.csv`
- `trajectory_stability_audit.csv`

Two of these are load-bearing. `completion_paradox.csv` is the evidence for A3's completion-paradox claim, and `trajectory_stability_audit.csv` is cited by CLAIMS B3/B6. CLAIMS' own shipping gate says claims whose evidence lives only in an archive do not ship — which currently describes A4, A5, and D6 (audit A10).

As of 2026-08-09 these have been moved again, into `_Archive/_results/`, and are now tracked in git. `paper/generate-figures/generate-fig-completion-paradox.py:51` reads a path that no longer exists in either location.

## Status of the files as of 2026-08-09

Two have been **restored to `results/analysis/**` because CLAIMS cites them directly:

- `completion_paradox.csv` — A3's evidence
- `trajectory_stability_audit.csv` — B3's demotion evidence (the 20/102 stability  
finding that downgraded the trajectory taxonomy from empirical contribution to  
descriptive vocabulary)

Three remain archived, with **zero mentions in CLAIMS.md**:

- `criteria_strictness_audit.csv`
- `criteria_strictness_audit_full.csv`
- `emergence_thresholds.csv`

No claim depends on these three. That is the strongest available argument that archiving them was right, and it is a weaker argument than a recorded rationale would have been.

Separately, a set of files was already in `results/_archive/` **before** the 2026-08-08 cleanup and was only relocated to `_Archive/_results/` on 2026-08-09. Four of those *are* cited by CLAIMS and constitute audit finding A10 in concrete form:  
`pythia-2.8b-multihead-ablation.csv` and `pythia-2.8b-candidate-heads.csv` (D6/A5), `pythia-2.8b-collocation.csv` (×2), `pythia-2.8b-head-characterization.csv` (×3). CLAIMS' own shipping gate says a claim whose evidence lives only in an archive does  
not ship. These need re-homing or the claims need re-scoping.

## Decision

**Chosen: adhoc, not archive.** The four archived files that CLAIMS cites move to named investigation directories under `results/adhoc/`, matching their `src/` modules:

- `results/adhoc/d6_multihead_ablation/` — `pythia-2.8b-multihead-ablation.csv`,  
`pythia-2.8b-candidate-heads.csv`
- `results/adhoc/head_characterization/` — `pythia-2.8b-head-characterization.csv`, `pythia-2.8b-collocation.csv`

The two CLAIMS-cited analysis tables have already been restored to `results/analysis/` (2026-08-09): `completion_paradox.csv` and `trajectory_stability_audit.csv`.

The three uncited audit tables stay archived: `criteria_strictness_audit.csv`, `criteria_strictness_audit_full.csv`, `emergence_thresholds.csv`.

### The rule this rests on

**Every results directory is written by a notebook.** The distinction is what kind:

- **Pipeline notebooks** — in the regeneration path, rerun when the data changes — write top-level directories: `elicitation`, `entropy`, `binding`, `frequency`, `analysis`.
- **Investigation notebooks** — one-off, question-shaped, run once — write under `results/adhoc/` in a directory named for the investigation. This already holds `d8_frequency_prior/`, `d1_bos_diagnostic/`, and `gap-paper-replication/`.

So `adhoc/` is not "miscellaneous" and not "results with no notebook." It is results from notebooks that are not part of the regeneration path.

The four orphaned files fit this exactly. D6 and the head-characterization work each had an investigation notebook; those notebooks have since been archived, which is why the results looked orphaned rather than adhoc. The results were always adhoc. Archiving  
them was a category error, not a deliberate demotion.

This makes "does this fit anywhere else" checkable rather than a judgment call: **is the notebook that produced this in the regeneration path?** If yes, top-level. If no, `adhoc/` under the investigation's name.

### Archived notebooks are out of scope

The notebooks moved to `_Archive/_notebooks/` on 2026-08-09 — `mlp.ipynb`, `tangent.ipynb`, `trajectory-class.ipynb`, `frequency-olmo.ipynb` — are **no longer part of the paper's scope.** They are not rerun, not maintained, and their results are  
not evidence for any shipping claim.

This is a scope statement, not a deletion: the notebooks stay in git and their outputs stay wherever they are. But nothing in the regeneration path should depend on them, and a claim citing their output needs re-scoping rather than a path fix.

The four files being moved to `adhoc/` are the exception, and only because CLAIMS cites them. Their notebooks are archived; their results are still evidence.

### A note on running `src/` modules directly

Modules under `src/` are libraries called by notebooks, not entry points. If one is run directly — which has happened, by an agent rather than by the author — its output has no legitimate home under this rule, because there is no notebook to classify.

That is an argument for the loader **flagging** unexpected paths rather than skipping them silently. The skip counter added in `aa7e1bb` is the first half of this; asserting the notebook-to-directory correspondence would be the second.

### Considered and rejected

**Leave archived, downgrade the claims.** Rejected: the files are evidence for claims that are otherwise sound, and the archiving had no recorded rationale (see below).

**Restore to a flat **`results/`** root.** Rejected: flat-and-weird is the condition the 2026-08-08 cleanup was reacting to. `results/peak_regress_lens.csv` is a surviving instance and should also move to `adhoc/`.

**Delete.** Rejected on principle. Deletion is the only irreversible action on the audit response list; an unneeded file costs clutter, a deleted one costs a reconstruction. This applies to A20's "dead" `src/` modules as well — move to `_Archive/_src/` rather than removing.

## Consequences

Claims A5/D6 and the head-characterization claims keep citable evidence at a stable path, so CLAIMS' shipping gate is satisfied without downgrading anything.

`results/analysis/` stays what it is — derived tables written by the analysis notebook — rather than accumulating one-off diagnostic output. The clutter that prompted the 2026-08-08 cleanup does not return.

`results/adhoc/` gains a stated rule instead of being a place things land. That is worth more than the file moves: an escape hatch with no rule becomes the flat-and-weird problem one level down.

Harder: `adhoc/` now has a convention that has to be maintained by hand, and loose files at its top level are the first sign of drift. `results/peak_regress_lens.csv` is already misfiled and should move under a named investigation directory.

**Depends on:** the pipeline-versus-investigation distinction staying legible. If a top-level `results/{X}/` directory exists whose notebook is not in the regeneration path, either the rule has been broken or the directory belongs in `adhoc/`. This is checkable and would make a reasonable assertion in the loader alongside the skip counter.

Also depends on knowing which claims cite which files. CLAIMS.md is the source of truth and the mapping should be verified rather than assumed before anything is moved.

**Who else reads this:** `paper/generate-figures/*` reads from `results/analysis/`; findings docs cite paths directly; `src/analysis.py` walks `results/{elicitation,entropy,binding}/` and will silently skip anything that does not match the `{suite}/{model}/{model}-{domain}.csv` shape.

## Sequencing note

Figure scripts are downstream of everything here and should be fixed **last**. The figures are generated from data that is being regenerated; repairing a figure script's paths before the data settles is the same category of error as updating prose before  
the numbers stabilised, which is why prose was scoped out on 2026-08-08. Order is: data, then claims, then figures.

## Process note

This decision exists because five files were moved without a recorded reason. The cost showed up within 24 hours: the author could not reconstruct the rationale, a NAILED claim's evidence went untracked, and a figure script broke silently.

The generalizable rule is not "archive less." It is that **moving a results file is a decision**, because results files are cited. A one-line note at the moment of the move — what was moved and why — would have made this entire entry unnecessary.
