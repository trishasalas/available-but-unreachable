# Spearman Review — Written Verdicts (2026-07-03)

> Review conducted by Claude (Fable 5, claude.ai) per the blind-committed
> rubric (`spearman-review-rubric-2026-07-03.md`, commit 3ca257c).
> Deliverables reviewed from commit ca0319e. Reviewer's headline judgment
> (6.1: "predicts, not cause") was stated blind, in-conversation, before
> any CSV was read. One paragraph per rubric item. Verdicts ratified by
> Trisha in review conversation 2026-07-03.

**1. Conformance — PASS.** Unit is compound × suite (n=49 per suite);
x = log10 frozen bigram count; y = strict-binary mean per ratified spec;
partials, tau-b, sensitivity, and secondary runs all present; row-level
appears only with clustered-bootstrap CI, no naive p-value anywhere;
sense split computed at compound level. The numbers below were produced
by the promised analysis.

**2.1 Headline — SUPPORTED, both suites.** Pythia ρ=0.5715, GPT-2
ρ=0.5052, n=49 each, direction positive as predicted. Both clear the
pre-registered ρ≥0.4 support threshold; thresholds applied mechanically
before interpretation.

**2.2 Confirmatory vs proxy — CONSISTENT.** Pythia (exact training
corpus) and GPT-2 (Pile counts as proxy for unindexed WebText) agree in
direction and magnitude; no divergence to explain. Paper labels the
asymmetry but claims cross-architecture replication.

**2.3 Sense split — UNUSABLE AS STATISTICS, VALUABLE AS DESCRIPTION.**
a11y-sense-only collapses to n=9 (Pythia, ρ=0.86) and n=6 (GPT-2,
ρ=−0.21, p=0.69); neither is interpretable. The collapse itself is the
finding: for >80% of compounds, correct-domain responses were too rare
to analyze — wrong-domain capture appearing as a missing-data pattern.
Report as limitation plus one descriptive paragraph; all-rows primary
carries the evidence.

**2.4 Zero-inflation — NO DISTORTION.** Weighted sensitivity (ρ=0.5876 /
0.4835) and secondary max-scale (0.4531 / 0.5416) bracket the primary;
tau-b (0.4348 / 0.3975) confirms ties are not manufacturing the effect.
Every pre-declared y tells the same story.

**3. Word1/tokenization interrogation — CONFOUND FAILED, FLAT.** Partial
ρ controlling compound token count: 0.5603 / 0.4896. Controlling word1
unigram frequency: 0.5913 (up from raw) / 0.4857. Attenuation is
negligible; word1 was mild noise, not the puppeteer. The signal is the
compound's own corpus life — the unit of learning is the bound compound.
S4 PMI robustness read: OPEN (not in staged set; request from CC or
fold into supplementary).

**4. Prediction scorecard — PARTIALLY OPEN.** CC reports 4/7
token-competition candidates fired, tree_grid never_emerges held, 2/4
ceiling anchors clean. Verdict deferred until (a) base-rate computation
— hit rates mean nothing without the chance-firing rate across all 41 —
and (b) the two failed ceiling anchors are named from
compound_accuracy_table.csv and reported as evidence against the thesis
per rubric 4.3, in the same font as the hits.

**5.1 Criteria strictness — CLEAN, EXTEND.** Incorrect-marker counts run
3–6 with no gradient across predicted classes (never_emerges ≈4.1,
ceiling anchors ≈3.5; lone outlier status_message=6). No evidence the
author's bar tracked her predictions. ASK: CC emits the same columns for
all 41 authored rows so the footnote reads "across the full worksheet."

**5.2 Trajectory stability — FAILED; TAXONOMY DEMOTED.** 20/102 class
assignments survive a one-level flip, far below the ~45 bar. Stable set
is dominated by never_emerges (floor effect); fragility concentrates in
shape-defined classes (mixed, peak_regress). Verdict: four-way
classification exceeds instrument resolution. B3 demotes from finding to
descriptive vocabulary — shapes may be narrated per compound, never
counted or computed on. Headline unharmed: the pre-registered primary
reads continuous accuracy, which single flips cannot move.

**5.3 Regression guard — PASS.** Original-8 coding byte-identical
pre/post translation per CC's verified report.

**5.4 Untranslated rows — NONE.** 0 rows returned; n=49 carries no
silent exclusions.

**6.1 Exit: A3 wording — "PREDICTS," NOT "CAUSE."** Prediction of
unusual quality (two suites, proxy replication, confounds flat, every
alternative y agreeing) but no intervention anywhere in the design, and
frequency's entourage (abstractness, terminology age, polysemy) remains
uncontrolled. Causal account appears as stated hypothesis with the
Step-5 trace as exhibit. Matches reviewer's blind pre-commitment.

**6.2 Exit: weakest link in A6 — THE FINAL ARROW.** "Competition at the
decision point is the operative failure" rests on one observational
trace of one compound. RECOMMENDATION: D7 (single-token-ban
counterfactual at Step 5) jumps the queue to pre-submission priority —
an afternoon on existing logit_export plumbing, and the cheapest
experiment in the program that can upgrade a word in the abstract.
Corpus-level causation remains Paper 2's mandate.

**6.3 Exit: surprises — ONE, LOGGED AND CURATED.** The sense-split n-collapse was
not anticipated by the pre-registration; its interpretation (absence as
evidence of domain capture) is post hoc and labeled as such. Follow-up
question (does per-compound sense-rate correlate with frequency?) was
DECLINED by Trisha 2026-07-04 as near-degenerate with the primary finding
— not queued. Her framing, recorded as the sharper account: rare compounds
are not "captured by the wrong domain" so much as never lexicalized as
units at all — the model falls back to reading them as ordinary
compositional compounds (focus + indicator, live + region), landing in the
parts' dominant senses by default. This splits failures into two tiers:
lexicalized-but-outcompeted (skip_link — correct token present in the
Step-5 candidate set, loses the election) vs never-lexicalized
(compositional fallback; nothing formed to capture). D7's branches
adjudicate the tiers per compound: competitor-ban recovery ⇒ tier one;
next-compositional-reading promotion ⇒ tier two. Framing candidate for
the Discussion; no new experiment required.

**Deviations log.** Pre-registration committed after pipeline start but
before any viewing (timing inversion, logged in DECISIONS). Aggregate
gap-shift values incidentally viewed by Trisha 2026-07-03 (logged).
Reviewer read staged results 2026-07-03 per review gate; frequency table
now open to Trisha — the blind window is closed.

**Open items.** (1) CC: strictness columns for all 41. (2) CC: scorecard
base rates. (3) Name the two failed ceiling anchors in Section 4 prose.
(4) S4 PMI read. (5) D7 scheduling decision — Trisha's call.
