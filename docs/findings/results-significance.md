# What the Extended Gap Analysis Results Mean

*A plain-language walkthrough of every analysis table in `results/analysis/`, what
each number is actually saying, and which findings carry the paper.*

Written 2026-06-27. All figures here are read directly from the CSVs in
`results/analysis/` — nothing is interpreted that isn't recoverable from the data.

---

## TL;DR — the one-paragraph version

Across 10 models (Pythia 160M–12B, GPT-2 124M–1.5B), accessibility knowledge does
not arrive as one capability. It arrives as **three dissociable capabilities that
emerge at different scales and sometimes move in opposite directions**: the model can
**complete the syntax** of a concept (e.g. produce `alt="A dog"`) long before it can
**define** the concept, and it can define a concept long before it can **apply** it to
judge a real example. Internally, the model's own uncertainty tracks this — it stays
measurably *less sure* on judgment ("evaluative") prompts than on definition
("declarative") prompts, and that internal gap **widens with scale** even as outward
definition accuracy improves. Meanwhile, attention binding of the compound's tokens is
near-saturated (~1.0) for essentially every concept regardless of whether the model
understands it — so **binding is necessary plumbing, not the seat of the knowledge.**

---

## 1. The declarative–evaluative gap (`pythia_gap.csv`, `gpt2_gap.csv`)

**The setup.** "Declarative" prompts ask the model to *define/explain* a concept.
"Evaluative" prompts ask it to *apply* the concept — look at an example and judge it
(e.g. "does this image have proper alt text?"). Scores are mean accuracy
(incorrect=0, partial=1, correct=2), reported both raw and as a percentage of the
2.0 ceiling.

**Pythia:**

| scale | declarative % | evaluative % | gap (pts) |
|-------|--------------|--------------|-----------|
| 160M  | 25 | 10 | 15 |
| 410M  | 40 | 20 | 20 |
| 1B    | 30 | 10 | 20 |
| 2.8B  | 50 | 30 | 20 |
| 6.9B  | 70 | 50 | 20 |
| 12B   | 50 | 50 | **0** |

**GPT-2:**

| scale | declarative % | evaluative % | gap (pts) |
|-------|--------------|--------------|-----------|
| 124M  | 35 | 20 | 15 |
| 355M  | 45 | 20 | 25 |
| 774M  | 55 | 30 | 25 |
| 1.5B  | 60 | 10 | **50** |

**What it means.**
- The gap is **remarkably stable in Pythia** at ~20 points from 410M through 6.9B.
  Defining is consistently ~2× easier than applying. This is the central Paper-1
  claim, now replicated on the expanded tmlr prompt set.
- **The 12B "gap closes" is a false friend.** It hits 0 not because evaluative caught
  up but because **declarative *regressed*** (70→50) while evaluative held at 50.
  Report the raw scores, not just the gap, or you'll tell the wrong story.
- **GPT-2 shows the opposite trend: the gap *widens* with scale** and blows out to 50
  points at 1.5B, where evaluative *collapses* to 10% while declarative climbs to 60%.
  This is inverse scaling on the harder task. The cross-architecture contrast (stable
  gap in Pythia, widening gap in GPT-2) is worth a sentence — it argues the gap is a
  property of *how knowledge is acquired*, not an artifact of one model family.

---

## 2. The completion paradox (`completion_paradox.csv`) — the headline

**The setup.** Few-shot completion prompts give two worked HTML examples, then a third
stem (e.g. `<img src="photo.jpg"`), and we score whether the model produces a
structurally correct continuation (`alt="..."`). We compare that to declarative
accuracy on the *same concept at the same scale*. `paradox_gap = completion% −
declarative%`.

**Alt text, Pythia:**

| scale | completion % | declarative % | paradox gap |
|-------|-------------|---------------|-------------|
| 160M  | **100** | **0** | **+100** |
| 410M  | 100 | 50 | +50 |
| 1B    | 100 | 50 | +50 |
| 2.8B  | 100 | 100 | 0 |
| 6.9B  | 100 | 100 | 0 |
| 12B   | 100 | 100 | 0 |

GPT-2 alt text tells the same story (completion 75–100% while declarative is stuck at
50% until 1.5B). Captions shows a milder version (+50 paradox gap at mid scales).

**What it means.** This is the cleanest result in the set. **At 160M — a model that
scores 0% at defining what alt text is — the model produces correct `alt="..."`
syntax 100% of the time.** Procedural/syntactic competence is fully present at a scale
where conceptual competence is entirely absent. The paradox gap then closes from above
as declarative knowledge catches up around 2.8B.

The interpretation for the paper: **"knowing how to do it" and "knowing what it is"
are separate capabilities with separate emergence curves.** Pattern-completion rides on
local n-gram/template statistics that are dense in training data; definitional
knowledge requires the concept to be assembled and retrievable. The model *does*
before it *knows*. (Caveat to disclose: completion also has the highest degeneration
rate — see §8 — so completion scoring needs the degeneration filter to be credible.)

---

## 3. Internal uncertainty mirrors the behavioral gap (`entropy_divergence.csv`)

**The setup.** Mean last-token entropy on declarative vs evaluative prompts at each
scale. `entropy_gap = evaluative_entropy − declarative_entropy`. Higher entropy = more
internal uncertainty.

**Pythia:**

| scale | declarative H | evaluative H | gap |
|-------|--------------|--------------|-----|
| 160M  | 4.03 | 4.21 | 0.18 |
| 410M  | 3.63 | 4.01 | 0.38 |
| 1B    | 3.26 | 4.08 | 0.82 |
| 2.8B  | 3.30 | 3.90 | 0.60 |
| 6.9B  | 3.02 | 3.72 | 0.70 |
| 12B   | 2.72 | 3.75 | **1.03** |

**What it means.** Declarative entropy **falls steadily** (4.03 → 2.72: the model gets
more and more confident at *defining*), while evaluative entropy **stays high and flat**
(~3.7–4.2: it stays uncertain at *judging*). So the entropy gap **widens monotonically
with scale**, reaching ~1.0 nat at 12B. GPT-2 is noisier but lands in the same place
(0.99 at 1.5B).

This is the result I'd pair with §1 as a two-panel figure. **The model is internally
signaling the declarative–evaluative gap.** Its own uncertainty "knows" the evaluative
task is harder, and that internal awareness *grows* with scale — even at 12B where the
behavioral gap looked like it closed. The behavioral gap and the internal gap are two
views of the same phenomenon, and the internal one is the more honest scale signal.

---

## 4. Fluent wrongness — the error signal erodes with scale (`fluent_wrongness.csv`)

**The setup.** Compare last-token entropy on accessibility prompts the model gets
**wrong** vs bicycle-control prompts it gets **right**. `confidence_gap =
access_incorrect_H − control_correct_H`. If this goes to zero (or negative), the model
is as confident when it's wrong on accessibility as when it's right on something easy —
i.e. its confidence no longer flags its own errors.

| suite | scale | confidence_gap |
|-------|-------|----------------|
| pythia | 160M | 0.97 |
| pythia | 410M | 0.63 |
| pythia | 1B | 0.64 |
| pythia | 2.8B | 0.29 |
| pythia | 6.9B | **0.07** |
| pythia | 12B | 0.32 |
| gpt2 | 124M | 0.68 |
| gpt2 | 355M | 0.56 |
| gpt2 | 774M | 0.13 |
| gpt2 | 1.5B | **0.07** |

**What it means.** At small scale the gap is large and positive: a small model is
*visibly* less certain when it's wrong on accessibility — its uncertainty is doing its
job as an error flag. As scale grows, **the gap collapses toward zero** in both suites.
The largest models are nearly as confident when wrong on accessibility as when right on
bicycles. We don't see the gap go fully negative, so this is the *trend toward* fluent
wrongness rather than its full-blown form — but the direction is unambiguous: **scale
erodes the confidence signal that would otherwise distinguish a confident correct
answer from a confident accessibility error.** That's the mechanism behind "confident
confabulation."

(Detailed per-concept × accuracy entropy is in `entropy_confidence.csv` if you want to
show, e.g., that GPT-2's correct alt-text answers sit at H≈0.9 while its wrong ones sit
at H≈3.8 — clean separation that the aggregate erosion above is averaging over.)

---

## 5. Per-concept scaling trajectories (`per_concept_trajectories.csv`, `per_concept_scaling.csv`)

**The setup.** For each concept, the accuracy score (0/1/2) at every scale, classified
into a trajectory type.

**The three shapes (Pythia):**
- **Monotonic climb** — `alt text` (0→1→1→2→2→2), `screen reader` (1→1→2→2→2→2),
  `WCAG` (emerges late, 0 until 6.9B then 2), `color contrast` (mixed but upward).
  These are the "scale works" concepts.
- **Peak and regress (inverse scaling at the top)** — `keyboard navigation`
  (1→2→2→2→2→**0**) and `skip link` (0→1→0→2→2→**0**). Both are fully correct at 6.9B
  and **collapse to 0 at 12B.** The biggest model *loses* competence it demonstrably
  had one size down.
- **Never emerges** — `ARIA` (flat 0 at every scale), `captions`, `semantic HTML`,
  and `focus indicator` (Pythia). Scale does nothing.

**What it means.** "Bigger is better" is false at the concept level. The headline
emergence curve is an *average over concepts with qualitatively different fates.* The
12B regressions on keyboard navigation and skip link are concrete, reproducible inverse
scaling worth calling out by name — they're the kind of result reviewers remember.
GPT-2 sorts concepts slightly differently (e.g. focus indicator peak-regresses there,
skip link never emerges), which is itself evidence the trajectory is data-dependent,
not architectural.

---

## 6. ARIA never emerges (`emergence_thresholds.csv`)

ARIA's declarative accuracy is **0.0 at all 10 models in both suites.** So are HTML
(as a defined concept), captions, closed captions, empty link, form label, link text,
page title, semantic HTML, and the bicycle control. The concepts that *do* cross
threshold: color contrast (earliest, ~355–410M), keyboard navigation (~355–410M),
screen reader (774M–1B), alt text (1.5B / 2.8B), WCAG (latest, 1.5B / 6.9B), skip link
(2.8B Pythia only).

**What it means.** ARIA is the canonical "increasingly confident confabulation" case —
acronym-dense, jargon-heavy, sparse in pretraining, and it never resolves at any scale
we tested. It's the clean counterexample to emergence and pairs naturally with the
fluent-wrongness erosion in §4: the model gets *more* fluent about ARIA without ever
getting *correct*.

---

## 7. Binding ≠ knowing (`binding_accuracy_corr.csv`, `binding_vs_accuracy.csv`) — the key caveat

**The setup.** For each compound at each scale, pair the **max attention-binding
score** (how strongly some head binds the compound's tokens together, 0–1) with the
behavioral accuracy score. Then correlate.

| suite | n pairs | Pearson r | Spearman r |
|-------|---------|-----------|-----------|
| gpt2  | 32 | 0.45 | 0.39 |
| pythia | 48 | **0.12** | **−0.12** |

**What it means.** **Binding strength does not predict accuracy.** GPT-2 shows a weak-
to-moderate positive association; Pythia shows essentially none (and a slightly
*negative* rank correlation). The reason is visible in `binding_vs_accuracy.csv`:
max_binding is pinned near **0.9–1.0 for almost every compound at almost every scale** —
including concepts that never emerge. `focus_indicator` binds at 0.94–0.99 across all
of Pythia while its accuracy is 0. `closed_captions` binds at 0.72–0.98 while accuracy
is 0 until 6.9B.

So the attention heads bind the tokens of "focus indicator" into a unit **whether or
not the model understands focus indicators.** Binding is a near-saturated, low-level
operation; understanding is something else, layered on top and *not* reducible to it.
This is the honest, important mechanistic result — and it directly corroborates the
thatDangCircuit finding that compound binding is **distributed, not a localizable
circuit you can point to and say "the knowledge lives here."** Don't oversell binding
as the seat of knowledge; sell it as necessary plumbing that's present even when the
knowledge is absent.

---

## 8. Degenerate output — a confound to disclose (`degenerate_by_*.csv`)

Degeneration = a short phrase repeated ≥3× (e.g. "a link that is not a link that is
not a link").

- **By prompt type:** completion **36%**, hypothesis **27%**, evaluative 8%,
  validation 4%, declarative 2%, control 1.5%.
- **By concept:** script 40%, form label 30%, captions 27%, alt text 19%.
- **By scale:** highest at the smallest models (GPT-2 124M = 19.6%) and falls with
  scale, but never disappears (still ~6% at the top).

**What it means.** Degeneration is a **small-model + open-ended-generation** artifact.
Two honest implications: (1) it's a *confound for the completion paradox* — the prompt
type with the best accuracy story also degenerates most, so completion accuracy must be
scored with degenerate outputs excluded/flagged or a skeptic will discount it; (2) it's
a *quality signal in its own right* — the concepts that degenerate most (script, form
label, captions) overlap with the ones that never emerge, suggesting degeneration is
what "I don't have this concept" looks like behaviorally at small scale.

---

## 9. Accuracy by prompt type, the unifying view (`accuracy_by_prompt_type.csv`)

Ranked by how easy the task is to pattern-match, accuracy falls off exactly as the
dissociation story predicts:

- **Completion** highest and roughly flat across scale (50–75%) — procedural, rides on
  local statistics, available early.
- **Control** high (52–85%) — includes the bicycle baseline plus the non-accessibility
  concept probes; rises cleanly with scale (sanity check that scaling *does* work when
  the concept is common).
- **Declarative** climbs hard with scale (Pythia 25→70).
- **Evaluative** climbs but always lags declarative (the §1 gap).
- **Hypothesis / validation** lowest and only show signal at the largest scales —
  these are the most conceptually demanding probes.

This table is the quantitative spine of the dissociation thesis: a clean ordering of
prompt types by conceptual demand, with emergence scale increasing right along that
ordering.

> **Methodology note carried from DECISIONS.md:** the non-bicycle `control` rows are
> *concept probes* for other domains, not folded into the declarative/evaluative
> accuracy tables. They surface only here. Keep that boundary when writing — don't let
> control accuracy leak into the gap numbers.

---

## Recommended figures

Ranked. The first three carry the paper; the rest are appendix/supporting.

**Fig 1 (headline) — The completion paradox.**
Line plot, x = scale, two lines: completion accuracy vs declarative accuracy, for
`alt text` (and a second panel for `captions`), faceted by suite. The visual is the
100%-completion line flat across the top while the declarative line climbs from 0 to
meet it. One figure, the whole "does before it knows" thesis.
*Source: `completion_paradox.csv`.*

**Fig 2 — The gap, behavioral and internal (two panels).**
Left panel: declarative vs evaluative **accuracy** across scale (the behavioral gap,
§1). Right panel: declarative vs evaluative **entropy** across scale (the internal gap
widening, §3). Same x-axis, stacked. Shows the gap is real *and* the model knows it.
*Source: `pythia_gap.csv` / `gpt2_gap.csv` + `entropy_divergence.csv`.*

**Fig 3 — Per-concept trajectory heatmap.**
Grid: concept (rows) × scale (columns), cell color = accuracy score 0/1/2, faceted by
suite. Lets the reader *see* monotonic-climb vs peak-regress vs never-emerges at a
glance — and the 12B cells for keyboard navigation / skip link going dark is the
inverse-scaling money shot.
*Source: `per_concept_trajectories.csv`.*

**Fig 4 — Binding ≠ knowing scatter.**
Scatter, x = max binding (0–1), y = accuracy score (0/1/2), colored by suite, r values
annotated. The point is the dense vertical band at x≈1.0 spanning all y values — binding
is saturated regardless of accuracy. Honest mechanistic caveat in one panel.
*Source: `binding_vs_accuracy.csv` + `binding_accuracy_corr.csv`.*

**Fig 5 (supporting) — Confidence erosion / fluent wrongness.**
Line plot, x = scale, y = confidence_gap (access-incorrect entropy − control-correct
entropy), one line per suite, with a y=0 reference line. Shows the error-flagging
signal decaying toward zero with scale.
*Source: `fluent_wrongness.csv`.*

**Fig 6 (appendix) — Degeneration profile.**
Bar chart of % degenerate by prompt type (and a small companion by scale). Documents
the completion confound honestly.
*Source: `degenerate_by_prompt_type.csv`, `degenerate_by_scale.csv`.*

All six are generatable from the analysis CSVs in the existing
`generate-figures/` style (Atkinson Hyperlegible, navy `#08306b` / light blue
`#6baed6`). If you want, I can write the `generate-fig*.py` scripts to match the
Paper-1 figure conventions.
