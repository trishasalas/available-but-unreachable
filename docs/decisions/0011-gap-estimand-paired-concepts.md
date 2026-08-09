# 0011 — Gap estimand: pooled means or paired concepts

- **Status:** accepted
- **Date:** 2026-08-09
- **Related:** 0010 (exposed this, but is a separate decision)

## Context

Even with a working source filter, a difference of pooled means compares two different
concept populations. The evaluative battery covers 5 concepts; the declarative battery
covers 10 originals (51 with expansion compounds pooled in).

The claim the paper actually makes is a **floor**: evaluative accuracy does not emerge,
at any scale, in any family. Floor claims are carried by uniformity, not by sample
size. "Never, anywhere, across three families" is stronger at n=5 than "sometimes, on
average" would be at n=50. A difference-of-pooled-means framing makes 5-vs-51 look like
a power problem; a paired framing makes it a uniformity claim, which is what it is.

The 5 evaluative prompts do not map cleanly onto the 10 declarative concepts. Alt text
pairs directly. "Click here" is link text, which is not among the ten. Unlabeled input
has no declarative counterpart. Forcing a mapping is possible but strained.

## Decision

**Chosen: A — pooled paradigm means, over the Paper 1 batteries only.**

The gap at each scale is:

> mean declarative accuracy over the **ten** Experiment 1 concepts
> − mean evaluative accuracy over the **five** Experiment 2a concepts

Stated as a difference of paradigm means, not a matched per-concept comparison.
The paper says so explicitly rather than letting a reader assume pairing.

**Pre-registered switch.** Paired within-concept becomes the primary estimand
once the expanded evaluative battery (preregistration 0002, plan step 7) has
been authored, frozen, and run. The switch condition is recorded here, before
either result is known, so it is not chosen later on the basis of which answer
looks better. Until then, pooled is primary and any paired numbers are
reported as illustrative.

### Considered and rejected

**B — paired within-concept, now.** Rejected on sample size. The five
evaluative concepts are `alt text`, `empty link`, `form label`, `link text`,
and `semantic HTML`; only two of those are among the ten declarative
originals. That is n=2. Worse, `semantic HTML` never reaches `correct`
declaratively at any scale — it codes `partial` at five of six scales and
`incorrect` at 1B — so that pair measures the distance between "sort of" and
"no." The usable paired set is effectively n=1, which cannot carry Section I.

**Forcing a wider mapping** (e.g. treating `empty link` and `link text` as
proxies for concepts in the declarative ten). Rejected: the mapping would be
authored after seeing the data, which is the failure the pre-registration
discipline exists to prevent.

## Consequences

The comparison is now like-for-like in a way it was not before 0010: both arms
are Paper 1 batteries, both accessibility, both hand-authored for the same
study. The 51-vs-5 mismatch that produced the impossible negative gap is
resolved by concept population, not by changing the estimand.

The strongest current result does not depend on this decision at all. The 12B
declarative regression — `keyboard navigation` and `skip link` going correct →
incorrect, declarative peaking at 6.9B and dropping — is a **within-arm**
finding. It needs no pairing and no evaluative comparison.

Harder: the paper reports a difference of means over non-identical concept
sets, and must say so. A reviewer may reasonably ask why the arms were not
matched. The answer is that they were not matched in Paper 1 either, and the
matched battery is being built — which is a better answer than a forced
mapping.

**Depends on:** the ten declarative and five evaluative concepts remaining the
Paper 1 batteries. If either arm grows without the other, the comparison stops
being like-for-like — which is precisely what the 41 expansion compounds did
to the declarative arm and what 0010 corrected. Any change to either battery
requires re-examining this decision.

**Who else reads this:** `src/gap_analysis.py` computes both pivots and the
gap; anything reading `pythia_gap.csv`, `gpt2_gap.csv`, or `olmo_gap.csv`
inherits this estimand whether or not it knows it. The figures and Section I
prose both assume it.