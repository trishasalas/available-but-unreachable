## The Trajectory Taxonomy

Not all concepts fail the same way. 
Ten concepts, two architectures, four trajectory classes: 
- peak_regress
- monotonic_climb
- never_emerges
- mixed

The same concept can take different trajectories in different architectures. This is a core empirical contribution — the gap isn't uniform, it has structure.

---

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