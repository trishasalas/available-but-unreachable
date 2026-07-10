## Entropy and Fluent Wrongness

The findings so far describe what models get wrong at scale. This section measures how they get it wrong, and the answer is the paper's most practitioner-relevant result: not with hesitation, but with confidence that grows as correctness fails.

Output entropy is the behavioral uncertainty measure throughout this paper. In head-to-head comparison, entropy replicated our accuracy structure at r ≈ 0.96 while perplexity managed r ≈ 0.18; perplexity is accordingly demoted to supplementary material, where the recognition-precedes-generation pattern it suggested is preserved at suggestive strength (Supplementary; DECISIONS 2026-06-20). Entropy here is computed from the model's true output distribution — softmax of the full forward pass — a pathway note that Section 7 explains is not pedantry.

The central result is a sign flip. We define the confidence gap as the difference between a model's output entropy when it is wrong about accessibility concepts and its entropy when it is right about matched control concepts. At 160M the gap is +0.37: the small model is measurably more uncertain when wrong, which is the calibration one would hope for. The gap crosses zero near 2.8B — the same scale as the emergence threshold — and by 12B it is −0.37: the largest model is more confident when producing wrong accessibility answers than when producing correct control answers (`results/analysis/entropy_confidence.csv`, `fluent_wrongness.csv`). One caveat is mandatory and we state it rather than bury it: the control-correct cell is thin, with n ≈ 2 control-correct responses per scale, so the gap's magnitude should be read cautiously even though its sign and trajectory are consistent across the suite.

The qualitative face of the flip is best seen in one model answering two questions. Pythia-12B, asked why an image without alt text is not accessible, answers: "it has no text alternative. The alt text is a short description of the image" — correct, substantive, low-entropy for the right reason. The same model, asked why a long navigation menu without a skip link is not accessible, answers: "of the following error: The page you are trying to reach is not available in the current context" — a structurally coherent 404-style error template, delivered with equal fluency and comparable confidence. The model is not confused on the second question. It is confidently following the highest-probability continuation available to it, and for a compound documented 662 times in its training corpus against alt text's 23,306, that continuation is web boilerplate rather than accessibility knowledge. The failure is not an absence of an answer; it is the presence of a stronger, wrong one.

The scaling direction makes this worse, not better. At 2.8B the skip link answer is a tautology — wrong, but in the concept's neighborhood, and delivered with more hedging. At 12B the answer has left the neighborhood entirely and the confidence has increased. Where capability regresses, calibration regresses with it, and the two regressions compound: the scales most likely to be deployed are the scales whose wrong answers are least distinguishable, by any fluency or confidence signal, from right ones.

This is the finding with the most direct consequence for practice, and we state it as a design constraint rather than an observation: for specialized domains in this frequency regime, model confidence carries no usable signal about correctness, and any tool that surfaces generation confidence to a user as a trust indicator is surfacing noise at best and anti-signal at worst. An accessibility practitioner cannot tell a 12B-class model's knowledge from its fluency, because past the threshold scale the model itself no longer marks the difference. The entropy data is also the third leg of the frequency story: Section 5 showed frequency predicts which compounds fail and where in the ranking the correct token sits; this section shows the winning high-frequency continuation arrives with full confidence. The model is not uncertain about skip links. It is certain about the wrong thing, for a reason the corpus predicts.

---

<!-- Planning manifest preserved below (pre-drafting state; Fable pass 2026-07-05).
     NOTE: the figure request below ("displayed vs click" trace) was RETRACTED
     2026-07-04 (see DECISIONS D7 verdict; CLAIMS A2). This section's figure
     should instead be the confidence-gap-by-scale line (entropy_confidence.csv)
     plus the paired 12B alt_text/skip_link quotations. The 12B skip_link
     evaluative quote used above is from tangent.md (true-pathway generation);
     camera-ready sourcing should regenerate it mechanically via
     src/logit_export.py per the tangent.md paste-wound disclosure.
     keyboard_navigation-at-12B remains an open gap, not claimed.
     A candidate addition NOT used (no committed artifact yet): the per-scale
     skip_link decision-point entropy vs. other-declarative baseline table
     computed conversationally 2026-07-05 — requires landing as a committed
     analysis artifact before any prose may cite it. -->

*Data we have:*

- `results/mlp_investigation/` — all the decomposition, logit lens, vocab projection, skip_link_steps across every scale in both suites
- `results/analysis/completion_paradox.csv`

*Data we need:*

- Infini-gram frequency counts for each compound and their competitors
- Token competition traces for compounds beyond skip_link (keyboard_navigation at 12B is the priority)

*Figures needed:* the skip_link token competition trace ("displayed" vs "click") [RETRACTED — see note above], frequency table with trajectory class, and ideally the Spearman result.


### SUGGESTION: 12B skip_link as the star example of fluent wrongness

The 12B skip_link generation is the best fluent wrongness example you have:

"A long navigation menu without a skip link is not accessible because of the following error: The page you are trying to reach is not available in the current context."

The model isn't uncertain. It generates a structurally coherent 404-style error template with full confidence. The entropy is low *because* the high-frequency web error pattern dominates. This directly supports the frequency story: the model isn't confused, it's confidently following the highest-probability path, and that path leads to web boilerplate instead of accessibility knowledge.

Contrast with alt_text at 12B: "it has no text alternative. The alt text is a short description of the image." Same model, same structure, correct and substantive. The difference is corpus frequency.

The sign-flip (confidence grows as correctness fails) has a concrete illustration now: skip_link at 12B is *more* confident than at 2.8B, and *more* wrong. The tautology at 2.8B was at least in the right neighborhood.

Also note: the "data we need" list above is partially addressed — tangent.ipynb has competition traces for three concepts across five models. keyboard_navigation at 12B is still a gap.
