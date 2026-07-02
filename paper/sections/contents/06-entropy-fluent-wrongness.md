## Entropy and Fluent Wrongness

Entropy as the reliable behavioral measure (r≈0.96, perplexity cut). 

The 2.8B sign-flip — confidence grows as correctness fails. 

Models don't just fail, they fail fluently. 

This supports the frequency story: the model isn't uncertain, it's confidently wrong because the high-frequency completion feels right.

---

*Data we have:*

- `results/mlp_investigation/` — all the decomposition, logit lens, vocab projection, skip_link_steps across every scale in both suites
- `results/analysis/completion_paradox.csv`

*Data we need:*

- Infini-gram frequency counts for each compound and their competitors
- Token competition traces for compounds beyond skip_link (keyboard_navigation at 12B is the priority)

*Figures needed:* the skip_link token competition trace ("displayed" vs "click"), frequency table with trajectory class, and ideally the Spearman result.


### SUGGESTION: 12B skip_link as the star example of fluent wrongness

The 12B skip_link generation is the best fluent wrongness example you have:

"A long navigation menu without a skip link is not accessible because of the following error: The page you are trying to reach is not available in the current context."

The model isn't uncertain. It generates a structurally coherent 404-style error template with full confidence. The entropy is low *because* the high-frequency web error pattern dominates. This directly supports the frequency story: the model isn't confused, it's confidently following the highest-probability path, and that path leads to web boilerplate instead of accessibility knowledge.

Contrast with alt_text at 12B: "it has no text alternative. The alt text is a short description of the image." Same model, same structure, correct and substantive. The difference is corpus frequency.

The sign-flip (confidence grows as correctness fails) has a concrete illustration now: skip_link at 12B is *more* confident than at 2.8B, and *more* wrong. The tautology at 2.8B was at least in the right neighborhood.

Also note: the "data we need" list above is partially addressed — tangent.ipynb has competition traces for three concepts across five models. keyboard_navigation at 12B is still a gap.