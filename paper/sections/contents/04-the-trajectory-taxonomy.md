## The Trajectory Taxonomy

Not every concept fails the same way, and the differences have enough structure to deserve names. Plotting per-concept accuracy across scale for both families yields four recurring shapes. Monotonic climb: accuracy rises with scale and stays — screen reader, alt text, and WCAG follow this path in Pythia. Peak-regress: accuracy rises to a mid-scale peak and falls at maximum scale — skip link in Pythia is the canonical case. Never-emerges: zero correct responses at every scale in both families — ARIA, captions, and semantic HTML never arrive, across ten models and two architectures, with confabulation about them growing more confident as scale increases; focus indicator joins them in Pythia but scores correct twice in GPT-2 before regressing to zero at maximum scale — a peak-regress case there. Mixed covers the remainder. The same concept can take different trajectories in different architectures, which is itself informative: trajectory class is a property of the concept-architecture pair, not the concept alone (`results/analysis/per_concept_trajectories.csv`, `per_concept_scaling.csv`).

We treat this taxonomy as a descriptive vocabulary rather than a claim-bearing classification due to its high sensitivity. A stability audit we ran on our own scheme revealed that shifting a single response's accuracy code by just one level alters the framework so significantly that only 20 of the 102 class assignments remain unchanged. The class boundaries are too sensitive to individual coding decisions to carry empirical weight on their own. The structure that does carry weight in this paper is the continuous relationship of Section 5, which operates on accuracy directly and requires no thresholded classes. The taxonomy earns its keep as language: it lets us say "peak-regress" instead of re-describing a curve, and it names the phenomenon — inverse scaling on specific specialized concepts — that the rest of the paper investigates.

What the accuracy curves compress, the generations show: within a peak-regress trajectory, the quality of failure changes character across scale, not just its rate. Skip link at 2.8B fails by tautology — asked why a missing skip link is a problem, it answers that the skip link is not present. At 6.9B the failure is wrong but in-domain: "it is not a link." At 12B the generation has left the domain entirely, producing a structurally fluent 404-style error template. The model does not simply get worse at the concept; it fails in progressively more confident and less recoverable ways, a pattern Section 6 quantifies. (Generation quotes from the evaluative battery, true output pathway; camera-ready sourcing regenerates these mechanically per the provenance note in Methods.)

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     CALIBRATION NOTE: the manifest's "core empirical contribution" framing is
     superseded by the stability audit (20/102 assignments survive a one-level
     flip) — taxonomy demoted to descriptive vocabulary; Section 5's continuous
     relationship carries the empirical weight. CLAIMS row B3 demotion applied
     2026-07-06 (matches this prose); focus-indicator family error fixed same
     day per claims audit (GPT-2 labels it peak_regress, 2→1→2→0). -->

*Data we have:*
- `results/analysis/per_concept_trajectories.csv` — the classifications
- `results/analysis/per_concept_scaling.csv` — the scores behind them

*Figures needed:* multi-panel with one example per trajectory class, or a heatmap of all 10 concepts × scales × both suites. The visual that makes the four classes obvious.


### SUGGESTION: The tangent data illustrates peak_regress vividly

The trajectory taxonomy is currently defined by accuracy scores. The tangent notebook gives you qualitative texture for peak_regress specifically:

- skip_link at 2.8B: tautology ("because the skip link is not present")
- skip_link at 6.9B: wrong but in-domain ("it is not a link")
- skip_link at 12B: 404 error page (completely left the domain)

The quality of failure *changes* across the trajectory, not just the accuracy score. Peak_regress isn't just "accuracy goes down" — it's the model finding increasingly creative wrong answers as it scales. Consider a sidebar or example box showing the actual generations alongside the accuracy curve for peak_regress.
