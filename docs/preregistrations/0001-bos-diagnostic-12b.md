# D1 Pre-registration — BOS-attention diagnostic on the Pythia-12B late-layer binding resurgence

**Status:** REGISTERED. Committed before the run. Thresholds frozen below.  
**Runs on:** Trisha's Colab lane (12B). Notebook: `notebooks/d1-bos-diagnostic.py`.  
**Origin:** CLAIMS §D row D1 (stakes raised 2026-07-06); §8's stated prediction: "the late-layer binding resurgence we observe at 12B is itself a candidate attention-sink phenomenon, a testable prediction we state rather than assume."

## Hypothesis

The late-layer binding "resurgence" at Pythia-12B is dominated by attention-sink and positional structure, as its 6.9B counterparts were (five of six late-layer top binders placed 55–91% of attention mass on the BOS token; the sixth was positional). If so, Paper 1's "sustained late binding" column at maximum scale reads as sink/positional plumbing, not re-engaged concept binding — consistent with §3's contamination caveat and §8's prediction.

## Frozen definitions

- **Head set:** derived, not hardcoded — `get_top_binding_heads()` on the frozen `results/pythia/pythia-12b-binding.csv`, filtered to **late layers = final**  
**quarter of depth: layer ≥ 27** (Pythia-12B has 36 layers; 27/36 = 0.75).
- **Sink-dominated:** mean attention to the BOS token ≥ **0.5** (the module's `SINK_THRESHOLD`, unchanged).
- **Structural:** mean attention to position 1 (the template's "A"/"The" token) ≥ **0.5** (the module's `STRUCTURAL_THRESHOLD`, unchanged).
- A head counts toward the prediction if it is sink-dominated OR structural.

## Pre-registered prediction (P1)

**At least half** of the late-layer top-binding heads at 12B are sink-dominated or structural under the frozen thresholds.

## Outcome mapping (all branches ship)

- **CONFIRMED** (≥ 50% of late binders sink-or-structural): §8's sentence upgrades from stated prediction to tested finding; §3 gains one supporting sentence at the 12B dissociation; the intro's "dominated by attention-sink and positional behavior" sentence stands fully supported; Paper 1's late-binding column reading is corrected in §3/§7 where referenced.
- **PARTIAL** (> 0 but < 50%): reported as measured; §8's prediction-stated-not-assumed sentence stands unchanged (it was written for this branch); no text strengthens.
- **NOT CONFIRMED** (0 heads qualify): reported at full strength per house policy; §8's prediction is reported as falsified; the resurgence reading stays open and is said to stay open.

## Secondary (descriptive only, no prediction)

Induction and previous-token scores for the same heads, from the same forward pass — for continuity with the 6.9B characterization table. Reported, not adjudicated.

## Instrument

`transformer-lens==2.17.0` (pinned; the pin is load-bearing). One characterization forward pass; deterministic. Outputs to `results/d1_bos_diagnostic/` (per-head CSV + `VERDICT.md`).

## Freeze

This document is frozen at commit time. Any change after the run begins is recorded in DECISIONS.md with rationale, per house policy.
