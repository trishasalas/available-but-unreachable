## What Predicts Trajectory -- The Frequency Hypothesis

Skip_link motivates the question: why does this compound regress when others don't? 

"Skip" is an absurdly common word. The compound's correct completion loses to higher-frequency competitors. 

Infini-gram corpus measurements across all compounds — does component/competitor frequency predict which trajectory class a concept falls into? 

Spearman correlation. This is where the MLP token-competition work lives — the "displayed vs click" trace as the mechanistic illustration of how frequency competition plays out inside the model.

---

*Data we have:*
- `results/mlp_investigation/` — all the decomposition, logit lens, vocab projection, skip_link_steps across every scale in both suites
- `results/analysis/completion_paradox.csv`

*Data you need:*
- Infini-gram frequency counts for each compound and their competitors
- Token competition traces for compounds beyond skip_link (keyboard_navigation at 12B is the priority)

*Figures needed:* the skip_link token competition trace ("displayed" vs "click"), frequency table with trajectory class, and ideally the Spearman result.


### SUGGESTION: This section gets the most new material

The tangent notebook provides the mechanistic illustrations this section was asking for:

**The logit ranking tables.** Three prompts, three frequency levels, same decision point ("because"). The correct domain token's rank maps directly onto corpus frequency:
- alt_text (23,306 bigrams): ' alt' at rank 4 at 12B, correct generation
- screen_reader (32,100 bigrams): ' screen' at rank 2 at 12B, correct generation  
- skip_link (662 bigrams): ' users' at rank 14 at 12B, 404 error

**The cross-scale tracking for skip_link.** ' users' rank across Pythia sizes:
- 2.8B: rank 12, gap 3.8 → tautology
- 6.9B: rank 7, gap 2.7 → "it is not a link"
- 12B: rank 14, gap 4.1 → 404 error

That's peak_regress visible in the token rankings — the domain token climbs at mid-scale and falls back at 12B.

**Cross-architecture convergence.** GPT-2 Medium/Large/XL show the same frequency gradient with different specific wrong answers. Same mechanism, independent model family.

**The Spearman update.** GPT-2 bigram Spearman is r=0.78, p=0.024 (significant). Pythia is r=0.63, p=0.12 (strong trend, underpowered at n=8). Expanding to n=49 with additional accessibility compounds is in progress.

**Literature grounding from the research agent.** Kandpal et al. (2023, ICML), Razeghi et al. (2022, EMNLP), and Mallen et al. (2023, ACL) establish that frequency predicts recall. Your contribution: showing the mechanism at the token level and connecting it to scaling trajectories. They have the economics, you have the physics.

**Data we now have (new):**
- `tangent.ipynb` / `tangent.md` — evaluative generation + logit rankings across 5 models
- `results/frequency/` — frequency table, Spearman summary
- `src/frequency.py` — 225 compounds across 5 domains (49 accessibility for this paper)