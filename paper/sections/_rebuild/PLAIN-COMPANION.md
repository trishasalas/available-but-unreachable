# Plain Companion — §§2–6 (for Trisha's voice pass)

**What this is:** every paragraph of the dense sections, restated in one plain sentence. Your job per line: _does this match what I remember happening?_ ✅ = move on. ❌ or 🤔 = open the real section at that paragraph — the mismatch is either a writing bug or a memory bug, and the CSVs adjudicate.

**What this is not:** the paper. Nothing here is submission prose. If a plain line and the dense line ever disagree in _meaning_, that's a bug in the dense line — tell Fable.

---

## §2 — The Gap (02-behavioral-gap.md)

**One line:** Models can define accessibility concepts way better than they can use them, at every scale, in both families.

- ¶1 — The paper is about the difference between knowing a thing and applying it; we call that the declarative-evaluative gap.
- ¶2 — We asked matched "define it" and "use it" questions per concept, plus a small "complete the HTML" battery; everything got coded by fixed, version-controlled rules.
- ¶3 — The data appears in two cuts (the matched gap series, and the full-battery accuracies); both cuts agree the gap exists everywhere.
- ¶4 — The gap shows up in both model families; in GPT-2 it grows with scale, and in Pythia it only "closes" at 12B because the _defining_ ability decays down to meet the _using_ ability — decay, not mastery.
- ¶5 — One model, side by side: it defines skip link correctly, then when asked to _use_ that knowledge it answers in a circle (a tautology) — the knowledge doesn't survive the trip from definition to use.
- ¶6 — Bonus finding: tiny models can _complete_ accessibility markup long before they can define it (Pythia-160M writes perfect alt attributes while defining alt text at 0%) — form arrives before meaning, at all ten scale points.
- ¶7 — Honesty paragraph: that completion battery is small (8 prompts), was built for a different purpose, got coded after the fact, and was blind-recovered (T3) — so it proves the _direction_, not the _size_.
- ¶8 — Where the batteries overlap (alt text, captions), completion stays ahead of definition — alt text perfectly, captions with one reversal per family, both reported.
- **Your check:** does "define fine, use badly, and at 12B the defining rots too" match the lab you remember?

## §3 — Binding Isn't Causal (03-binding-not-causal.md)

**One line:** We ablated everything we could justify ablating, nothing changed, the model just rerouted — the binding signal is real but it isn't the mechanism.

- ¶1 — Binding was the best prior suspect (your Paper 1 found the correlation; this paper replicates it, and it generalizes across domains) — this section is the case against reading it as causal, in five moves.
- ¶2 — We took the top binding heads and asked what they actually _do_, instead of assuming.
- ¶3 — They're not induction heads (copy machines): induction score 0.02 vs the 0.5 expected.
- ¶4 — The biggest "binder" is just a previous-token head — compound words are always adjacent, so it "binds" everything; that's geometry, not meaning.
- ¶5 — The late-layer binders are mostly attention sinks (staring at the start-of-sequence token) plus one prompt artifact that collapses 0.98 → 0.006 when you move the word; the _metric_ is contaminated, which matters beyond this paper.
- ¶6 — No head cares about accessibility specifically — heads pick idiosyncratic word-sets across domains (one likes "hedge fund" and "stock market"); it's lexical, not semantic.
- ¶7 — The MLPs work equally hard on concepts the model gets right and wrong (4.437 vs 4.444) — failure isn't the network slacking.
- ¶8 — The one genuinely screen-reader-specific head does nothing when ablated (KL ≈ 10⁻⁵), and what it writes is the _movie_ sense of "screen" — a redundant copy, not a retrieval mechanism.
- ¶9 — Maybe the mechanism is a _team_ of heads? We pre-registered a joint ablation, earned each compound's set honestly, and ablated whole sets.
- ¶10 — Screen reader's earned pair: joint ablation ≈ single-head null; the excluded junk heads move the control 10× more, so the instrument works.
- ¶11 — Three more compounds, same design, every set lands ≥35× below the pre-registered bar; one compound (semantic HTML) degenerated for tokenization reasons and we say so.
- ¶12 — Population level (companion study, GPT-2 XL): remove the strongest binding heads and the binding signal itself barely moves (~1%) because compensator heads absorb it; and at Pythia-12B the compound stays perfectly bound while the sentence still dies — so whatever fails, fails after attention.
- ¶13 — Sum: the signal is real, general, and mundane (position + sinks + redundancy); remove the heads, the network reroutes, the outputs don't change; binding _marks_ emergence, it doesn't _implement_ it.
- **Your check:** this is your "we ablated everything and it didn't make a difference at all — the model just rerouted." Does every move sound like an experiment you ran?

## §4 — Frequency Predicts (04-frequency-predicts.md)

**One line:** How often a compound appears in the training corpus predicts whether, when, and how stably the model learns it — including which concepts get _worse_ with scale.

- ¶1 — Concepts sort into trajectory shapes: emerges-and-holds, peak-then-regress (skip link is the poster child), never-emerges (ARIA, captions, semantic HTML — and the confabulation about them gets more confident with scale).
- ¶2 — The taxonomy is vocabulary; the real result is continuous and doesn't need the classes.
- ¶3 — Skip link is rare in the corpus ("skip" and "link" are common; the _compound_ is rare) — and it's the compound that degrades at max scale in both families.
- ¶4 — We pre-registered the test (ρ ≥ 0.4 threshold, committed before computing anything; DECISIONS 2026-07-03).
- ¶5 — Result: corpus frequency correlates with accuracy at ρ = 0.57 (Pythia) / 0.51 (GPT-2), n = 49, and survives the partial-correlation controls.
- ¶6 — The word-sense cut: restricted to compounds whose corpus hits are actually in the accessibility sense, Pythia hits ρ = 0.86 (n = 9); GPT-2's filtered set shrinks to just 6 compounds — too few for the correlation to mean anything, in either direction.
- ¶7 — Zoom into the decision point: the correct token's _rank_ in the model's head tracks corpus frequency, and skip link's rank rises then sinks in step with its behavioral arc — the knowledge is in the distribution; what scale changes is whether it _wins_.
- ¶8 — The generations show failure changing _character_ with scale, not just rate — more confident, less recoverable.
- ¶9 — This fits the frequency literature (Kandpal, Razeghi et al.); they describe the force, we photograph where it lands.
- ¶10 — Correlation, not causation — intervention on training data is future work (INTERCEPT); and the frequency ordering shows up again _inside_ the model's own output machinery (→ §6).
- **Your check:** rare-in-corpus → late, unstable, or never; frequent → early and stable. Match?

## §5 — Fluent Wrongness (05-fluent-wrongness.md)

**One line:** Small models are _nervous_ when they're wrong; big models are wrong with total confidence — the uncertainty signal collapses exactly where deployment is likely.

- ¶1 — Question: when the model is wrong about accessibility, does it _feel_ uncertain? Answer: only when small.
- ¶2 — We measure confidence as output entropy (the real distribution, true pathway — §6 explains why that matters); entropy replicated our accuracy structure at r ≈ 0.96, perplexity didn't (r ≈ 0.18).
- ¶3 — The central result: the wrong-answer entropy penalty collapses with scale (Pythia 0.97 → 0.07 by 6.9B; GPT-2 monotone 0.68 → 0.07) — past the threshold, wrong answers look just like right ones from inside; one thin-cell caveat stated.
- ¶4 — Qualitatively: 12B answers the rare-concept question wrongly _in the confident style of_ a frequent answer — fluent wrongness isn't a mystery riding beside the frequency story, it _is_ the frequency story, in behavior.
- ¶5 — And it compounds: where capability regresses, calibration regresses with it — the deployment-sized models are the ones whose wrong answers you can't tell apart.
- ¶6 — Practical, and scoped carefully: this is about what a *product* shows a *user*, not about entropy as a technique. At deployment scale in this domain, a model's per-answer confidence (low entropy, fluency) says nothing about whether it's right — so a tool shouldn't show a confidence badge as a reason to trust an answer, and shouldn't auto-accept on certainty. Entropy itself stays useful: it's the instrument that detected this, and small models' uncertainty is still honest. The model is certain about the wrong thing, for a reason the corpus predicts.
- **Your check:** small model hedges, big model bluffs. Match?

## §6 — Measurement Pathways (06-measurement-pathways.md)

**One line:** Our own pre-registered gate caught one of our exhibits being an artifact of a common measurement shortcut — and the autopsy produced a general finding about where models keep their frequency prior.

- ¶1 — This section documents a correction and the architectural finding it produced; it's a section, not a footnote, because the mechanism is quantitative and the vulnerability is field-wide. (It's also the narrowed form of the one claim the blind study didn't recover — T4.)
- ¶2 — The retraction: an exploratory trace (using the common skip-the-final-LayerNorm shortcut) showed a dramatic token competition at 12B; the pre-registered gates required reproducing it _and_ verifying it on the true pathway before intervening — gate two failed; on the model's real output, the reported election never happens; claim withdrawn (decision log, 2026-07-04).
- ¶3 — It's systematic, not a one-off: the shortcut's rollouts leave the true trajectory within seven tokens at _every_ scale, diverging exactly at thin-margin decisions and then fabricating; sometimes worse than reality, sometimes "better" — either way, fiction. Important acquittal: the accused is the skip-the-normalization _variant_ plus the practice of putting any approximation inside the generation loop — the canonical logit lens (which applies the normalization) is explicitly not the target, and our own DLA did it correctly throughout.
- ¶4 — The mechanism: the folded bias b_U is where a model without output biases keeps its unigram frequency prior — b_U correlates with corpus frequency at ρ = 0.664–0.779 (strongest at 12B), while the term the shortcut _keeps_ is frequency-dead (|ρ| < 0.01) — so the shortcut severs exactly the frequency channel, and in all six observed divergences the true pathway picked the more frequent token.
- ¶5 — Practice: three rules (true forward pass for generation claims; exact centering + realized scale for projections — which our DLA already used, keeping the artifact isolated; report margins, not just winners).
- ¶6 — The loop closes: corpus statistics (§4) and the weights (b_U) tell the same frequency story from opposite ends — the broken instrument failed precisely by cutting the wire between them.
- **Your check:** the gate halted the experiment, the claim came out, and the autopsy found the frequency prior living in b_U. Match?

---

_Companion drafted by Fable, 2026-07-12, from the current \_rebuild texts. Meaning-accurate to the dense versions as of tonight; if the dense text changes, the companion is stale until regenerated. This file never ships — it exists so the author can verify her own paper without fighting the register her reviewers require._
