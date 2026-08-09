# 0011 — Gap estimand: pooled means or paired concepts

- **Status:** proposed
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

*(pending)*

**A.** Declarative mean minus evaluative mean, over the original concept set only.

**B.** Paired comparison restricted to concepts that have both a declarative and an
evaluative item.

Recommended: B. It resolves the estimand problem and the population-mismatch problem
in one move, and it matches the claim being made — a within-concept statement that the
model defines a concept and cannot apply it.

Note that B is substantially more attractive if the evaluative battery is extended to
cover the declarative concepts (see `docs/preregistrations/`), which would give clean
pairs instead of a forced mapping.

## Consequences

The gap becomes a within-concept measure, which is a stronger and more defensible
claim than a difference of two pooled means over non-overlapping concept sets.

Harder: requires an explicit concept mapping between the declarative and evaluative
batteries, which is itself a judgment call and should be recorded. Under B the paper
reports fewer, better-grounded numbers rather than more, weaker ones — reviewers who
expect the pooled framing may need the choice explained.

**Depends on:** 0010 landing first. There is no meaningful pairing while the
declarative side silently includes 41 expansion compounds.
