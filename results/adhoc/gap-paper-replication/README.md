# paper1-replication — frozen D9 evidence (Exp 2b Socratic flip)

Frozen 2026-07-07 by Fable (claude.ai) at Trisha's direction. These CSVs
freeze the 2026-07-06 reproduction of the Paper 1 Exp 2b entropy result
that D9 (CLAIMS.md §D) points at: last-token − mean entropy under
Socratic elicitation flips **+0.74 (Pythia-1B) → −0.38 (Pythia-2.8B)**.

## Files

- `pythia-1b-exp2b-entropy.csv` — all three prompt types, 1B
- `pythia-2.8b-exp2b-entropy.csv` — all three prompt types, 2.8B
- `exp2b-socratic-flip-summary.csv` — the D9 flip, both endpoints
- `elicitation-robustness-v2-checkpoint-frozen.ipynb` — verbatim copy of
  the source checkpoint (see Preservation, below; PENDING until copied)

## Provenance — read this before trusting the source notebook

Source of both endpoints:
`how-models-think/accessibility-knowledge-emergence/notebooks/.ipynb_checkpoints/elicitation-robustness-v2-checkpoint.ipynb`
— a Jupyter checkpoint, NOT the saved notebook. Session exec counts
17–30: cell 7 (exec 17) loads pythia-2.8b (32 layers, 2774.9M params —
verified in cell output); cell 13 (exec 25) is the 2.8B entropy table;
cell 20 (exec 28) loads pythia-1b; cell 25 (exec 30) is the 1B table.

**The saved `elicitation-robustness-v2.ipynb` does NOT contain the 2.8B
run.** Its current state is a later single-kernel session (exec 1–15)
in which BOTH model slots load pythia-1b (`model_name =
"EleutherAI/pythia-1b"` sits under the "## Pythia 2.8B" heading; the
load-cell output confirms 16 layers / 1011.7M). Its two entropy tables
are byte-identical 1B results, matching the checkpoint's 1B table
exactly — so the 1B endpoint was independently reproduced twice; the
2.8B endpoint exists only in the checkpoint. Discovered 2026-07-07
during this freeze; near-miss class: one further save of the notebook
in Jupyter would have overwritten the checkpoint and destroyed the
−0.38 evidence.

Numbers were extracted programmatically from the notebooks' saved HTML
output tables (styled pandas `<td>` cells; regex extraction), not
recomputed. Values carry the notebook's own 4-decimal formatting.
`last_minus_mean_bits` computed from the two extracted columns.

Observed, not interpreted: at 2.8B, Direct Question stays positive
(+0.7752) while Socratic flips negative — the flip is
elicitation-format-specific, consistent with D9's construct.

SHA-256 of the source files as read 2026-07-07 (computed on transport
copies Claude-side; re-verify on-machine when the checkpoint is copied):

- checkpoint: b8148a8d2479f48d75e8982a5ba151cf54a366d1107fbdec4bcceb025bee99f3
- saved v2:   65ec8382653d3ee251b37ba1ed8bc3c952090bd12fe783b5038a9eb7b061f82e

## Preservation — COMPLETE, VERIFIED ON-MACHINE

Checkpoint copied verbatim to
`elicitation-robustness-v2-checkpoint-frozen.ipynb` via `cp` on Trisha's
machine, 2026-07-07 ~13:59 local. On-machine `shasum -a 256` of the
frozen copy:

```
b8148a8d2479f48d75e8982a5ba151cf54a366d1107fbdec4bcceb025bee99f3
```

Exact match with the transport-copy hash recorded above — the frozen
copy is bit-identical to the source checkpoint as read during the
2026-07-07 freeze. Verified by Trisha in-terminal; recorded here by
Fable same day.

## Scope

D9 remains PRELIM: two scales, pre-deterministic-coding era.
Claim-strength requires its own pre-registration (DECISIONS 2026-07-07,
ratified) — six scales on TL2 entropy CSVs under deterministic coding.
This directory freezes the reproduction; it does not upgrade the claim.
