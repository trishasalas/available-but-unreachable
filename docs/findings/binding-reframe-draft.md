# Binding-reframe draft — paste-ready blocks for the tmlr paper

Drafted 2026-06-28 (head-characterization session). Source numbers:
`results/pythia/pythia-2.8b-head-characterization.csv`,
`results/pythia/pythia-2.8b-collocation.csv`, `results/lexical-head-results.md`,
and `docs/head-characterization-findings.md`.

**The core reframe.** Paper 1 established, and this paper extends, an empirical
correlation: sustained late-layer attention binding of accessibility compounds tracks
behavioral capability. A mechanistic audit of those late-layer heads shows the binding
signal is a **correlate, not a cause** — the heads are attention sinks and positional
heads, the signal is not accessibility-specific, and the single most selective head is
causally inert. This *deepens* the result (we now know what the signal is) and converges
with the circuit-ablation work (binding is distributed and redundant). It does **not**
retract the correlation, and it does not touch the sealed Paper 1 — the refinement lives
here, in the follow-up.

These are voice-matched to the existing prose (declarative, bold lead-ins, "we"). Edit
to taste; everything is yours to rework in Obsidian.

---

## Edit 1 — Abstract (metadata.yaml)

The current abstract asserts a *necessary structural condition*. Soften the causal
language while keeping the empirical correlation. Two options:

**Tight (drop-in replacement for the first sentence):**

> Sustained deep-network attention binding of accessibility compounds co-varies with
> behavioral capability — present in every model that correctly defines core concepts,
> absent in every model that fails — but a head-level audit shows this binding is a
> correlate rather than a mechanism: the late-layer binding heads are attention sinks
> and positional heads, the signal is not accessibility-specific, and the most selective
> head is causally inert.

**One added clause (if you prefer to keep the original opening):** append to the existing
binding sentence:

> …; however, these late-layer binding heads are, on inspection, attention-sink and
> positional heads whose contribution is causally redundant, so the binding signal is
> best read as a scale-correlated marker of emergence rather than its mechanism.

Also consider the title: "…Thresholds, Binding, and the Declarative-Evaluative Gap" still
works — "Binding" now covers both the signal and its audit.

---

## Edit 2 — New Results subsection (place in 04-results.md, after Experiment 4)

### What the Late-Binding Heads Are

The binding analysis above establishes that sustained late-layer attention binding
co-varies with emergence. It does not establish what those late-layer heads compute. To
test whether the binding signal reflects concept-specific representation, we characterized
the top binding heads of Pythia-2.8B directly, deriving the head set from the binding sweep
(rather than fixing it a priori) and running each head through standard behavioral
diagnostics and a causal ablation.

**The top binding heads are not induction heads.** A prefix-matching induction test
(Olsson et al., 2022) on the derived top heads yields a maximum induction score of 0.02,
against the ≥0.5 expected of genuine induction heads. The pairing is not a generic copy
mechanism.

**The dominant binder is a previous-token head.** The single strongest binding head
(L1/H12) is the top binder for 7 of 11 compounds, yet scores 0.89 on a previous-token
diagnostic. Because the second token of a two-token compound is always adjacent to the
first, any previous-token head registers as "binding" every compound; its high binding
score reflects positional adjacency, not representation.

**The late-layer binders are attention sinks and structural heads.** Five of the six
late-layer (depth ≥ 10) top binders place 55–91% of their attention mass on the
beginning-of-sequence token — they are attention-sink heads, which read near-zero on every
content diagnostic while leaking signal into the binding score. The remaining late head
(L27/H24) attends to the first content position ("A"/"The"); its apparent binding is a
prompt artifact, collapsing from 0.98 to 0.006 for "due process" once a uniform template
no longer places the first word at that position.

**The binding signal is not accessibility-specific.** Measured across five domains under a
uniform template, the late heads fire on idiosyncratic, cross-domain subsets of compounds
(e.g., L28/H15 on "hedge fund" 0.94 and "stock market" 0.84; L30/H29 on "skip link" 0.98
and the weak-collocation control "bicycle wheel" 0.78). No head selects for accessibility;
the carve-outs are lexical, not semantic, and not collocation-strength-based.

**The most selective head is causally inert.** One head, L29/H7, does attend specifically
to "screen reader" (reader→screen attention 0.90, with the next compound at 0.21 and the
weight-level QK preference near zero — the selectivity is built through the layers, not
present in the embeddings). Yet zero-ablating this head's output at the "reader" position
changes the model's continuation of "A screen reader is …" by a KL divergence of 1×10⁻⁵;
the screen-reader-relevant continuation (" software") is unmoved. Direct logit attribution
of its output writes a "screen" word-sense direction (promoting "shoot"/"fire"/
"photographers", suppressing "screen"), not accessibility content — a write that is
functionally dead given the null ablation. The single most "screen reader–specific" head in
the network is a redundant representation, not a retrieval mechanism.

Taken together, the late-layer binding signal is real and scale-correlated but
mechanistically mundane: positional adjacency, attention-sink structure, and redundant
representation. This converges with our circuit-ablation results, where removing the
strongest binding heads moves mean binding by under 1% because compensator heads absorb the
loss. Attention binding marks emergence; it does not implement it.

*(Suggested figure: per-head bar of induction / previous-token / BOS-attention scores, or a
table — data in `results/pythia/pythia-2.8b-head-characterization.csv`.)*

---

## Edit 3 — Discussion reframe + Limitations note

**Discussion (drop-in thesis sentence):**

> Sustained late-layer attention binding scales with model size and tracks concept
> emergence, but it is a correlate rather than a mechanism: the late-binding heads are
> attention sinks and positional/structural heads, the signal is not accessibility-specific,
> and the single most selective head is causally inert. This is consistent with binding
> being distributed and redundant rather than localized, and it relocates the open question
> — what *does* compute these compounds — away from individual attention heads and toward
> distributed, likely MLP-mediated, computation.

**Connecting hypothesis (optional, Discussion):** the late-layer resurgence reported at 12B
may itself be partly an attention-sink phenomenon — a cluster of heads re-parking attention
on the BOS token near the output — rather than re-engaged concept binding. This is a
testable prediction: run the BOS-attention diagnostic on the 12B resurgence heads.

**Limitations (drop-in paragraph):**

> Our causal test of the binding signal is a single-head, single-position, single-prompt
> zero-ablation; it shows that the most selective binding head is not individually necessary,
> but it does not rule out a distributed ensemble in which no single head is necessary yet
> the population matters. The attention-binding metric also measures only attention
> patterns, not the value written; a head can attend strongly while contributing little, and
> conversely. We therefore frame late-layer binding as a correlate of emergence and defer the
> positive question of what computes these compounds — most plausibly MLP and multi-head
> ensemble effects — to future work.

---

## Integration notes (for you, not the paper)

- **Honesty guardrails:** keep the necessity claim scoped to *single heads* (pair it with
  the thatDangCircuit population ablations for the distributed claim); cite Paper 1's
  correlate and refine here — do not edit the sealed paper.
- **Same data:** the head-characterization uses the regenerated tmlr binding CSV, the same
  source as the Experiment-4 figures — so this audit is internally consistent with the rest
  of the paper, a strength worth stating.
- **Framing (per CLAUDE.md):** this is a claim about language/model internals; accessibility
  is the test domain. The reframe strengthens "the mechanism is domain-general."
- I left `paper/sections/sections/*` untouched (they're empty; you're drafting in Obsidian).
