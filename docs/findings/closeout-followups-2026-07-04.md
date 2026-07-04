# Post-review closeout findings (2026-07-04)

> Four closeout computations from the ratified Spearman review verdicts
> (`spearman-review-verdicts-2026-07-03.md`), run over already-frozen
> artifacts (pipeline commit ca0319e, worksheet commit 42695be). Code:
> `src/closeout_followups.py` (`PYTHONPATH=. python -m src.closeout_followups`);
> it does not touch the primary pipeline. The frozen 12-row strictness
> counts and the primary Spearman ρ (Pythia 0.5715 / GPT-2 0.5052) are
> reproduced exactly as regression guards.

## 1. Criteria strictness across the full worksheet

Extended `criteria_strictness_audit.csv` from the 12 prediction-flagged
compounds to all 41 authored rows → `results/analysis/
criteria_strictness_audit_full.csv`. Incorrect-marker counts run **3–6,
mean 3.80** across the full worksheet. The compounds pre-registered to
fail (never_emerges) average **4.1**; the ceiling anchors average **3.5**;
the 29 unflagged compounds occupy the same 3–5 band (five carry 5 —
character_key, accessibility_tree, accessible_description, semantic_markup,
input_purpose — none of them prediction-flagged). The lone 6 is
status_message, itself a predicted-fail that did *not* fail. There is no
gradient by predicted class once the whole worksheet is in view: the
authoring bar did not track the predictions. The paper footnote may now
read "across the full worksheet," not "across the predicted subset."

## 2. Prediction-scorecard base rate (the chance-firing denominator)

`results/frequency/scorecard_base_rate.csv` (definition stated in its
header). The reviewer's question (verdict 4 / rubric 4.1): a 4/7 attractor
hit rate means little without the rate at which *any* compound fails the
same way. The pre-registered failure signature the seven token-competition
candidates were predicted to show is **never_emerges**; computed per suite
over all 41 compounds the base rate is **20/41 (Pythia), 26/41 (GPT-2),
18/41 both-suites, 28/41 either-suite** — the field never-emerges roughly
half the time. The seven candidates never-emerge at **3/7 both-suites**
(≈ the 0.44 both-suites base rate — *not* above chance) and **6/7
either-suite** (0.86 vs the 0.68 base rate — modestly above). So bare
never-emergence does not single out the predicted compounds.

**A load-bearing caveat, surfaced for Trisha.** The scorecard's original
"4/7 fired" was a *stronger and different* claim than never-emergence: it
recorded whether each compound's **specific predicted foreign domain**
surfaced in the outputs (food-science for sensory_characteristics,
database-dedup for redundant_entry, C/C++ for pointer_cancellation,
geographic for landmark_region). That event is **not mechanically
reproducible from the frozen CSVs and is not any accuracy/trajectory
threshold** — the cleanest proof is that landmark_region (scorecard-fired)
and focus_management (scorecard-not-fired) have *identical* strict accuracy
and both touch never_emerges in one suite; only reading the outputs
separates them. Consequently the never_emerges base rate above is a
**conservative ceiling** on the true chance-firing rate: landing in a
*pre-named* wrong domain is far rarer than merely failing, so the null for
the attractor-level 4/7 is lower than these numbers, and 4/7 is more
informative than the never_emerges denominator alone implies. The honest
report is two-tiered: the *shape* signature (never_emerges) is at the field
base rate for these compounds; the *content* signature (predicted attractor)
is the one that discriminates but is only establishable by output
inspection, not by the pipeline. This is a methodology note, not a criteria
change.

## 3. The two ceiling anchors that did not ceiling

Of the four deliberately high-frequency ceiling anchors — chosen to ceiling
*if* corpus frequency drives retrievability — **two held and two failed,
and the two failures are reported here in the same font as the hits**
(rubric 4.3). **sign_language** (log₁₀ bigram 5.06) and **form_field**
(4.71) ceiling cleanly: form_field reaches 1.0 in both suites; sign_language
reaches 1.0 at max scale in both. The two that failed are **text_formatting**
(log₁₀ bigram 4.46) and **responsive_design** (4.55). text_formatting is
flat at 0.0 across all GPT-2 scales and only mixed in Pythia (all-scales
mean 0.50) — vague filler continuations, never the concept. responsive_design
plateaus at 0.50 in *both* suites and never reaches ceiling in GPT-2. Both
failed anchors sit near the top of the frequency range yet do not resolve to
the target meaning: high corpus frequency is **not sufficient** for correct
retrieval. This is evidence *against* a pure frequency account and is why
the headline is "frequency predicts," not "frequency determines" — the
anchors that should have been easy on frequency alone were not.

## 4. PMI robustness (association strength vs raw exposure)

`results/frequency/spearman_pmi_robustness.csv`. Substituting PMI
(association strength, from the frozen unigram columns; rank-invariant to
corpus size) for raw log₁₀ bigram count, association tells the *same* story
as raw exposure in Pythia (ρ = 0.51 vs 0.57, both clearing the 0.4 support
line) but **diverges in GPT-2, where PMI attenuates to ρ = 0.36 — below the
0.4 threshold that raw exposure (0.51) clears**. Raw corpus exposure is thus
the more robust predictor of retrievability than pointwise association,
especially in the proxy suite, consistent with the reading that the unit of
learning is the bound compound's own corpus life rather than the surprise of
its two words co-occurring (PMI and raw ordering correlate at only ρ = 0.72,
so the reranking is real, not cosmetic).
