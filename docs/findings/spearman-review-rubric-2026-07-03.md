# Spearman Review Rubric — authored blind 2026-07-03

> Written by Claude (Fable 5, claude.ai) with CC's pipeline PAUSED and no
> expansion-derived output viewed by anyone reviewing. Companion to the
> DECISIONS 2026-07-03 pre-registration entry (Spearman unit-of-analysis).
> This rubric is the review protocol for CC's packaged results, whoever
> conducts the review (Fable before 2026-07-07; Opus 4.6 unchanged if the
> clock loses). Commit BEFORE results are viewed — the rubric's value is
> that it provably predates the numbers.

## How to use

Work the sections in order. Each item gets a written verdict, not a
checkbox — one to three sentences. Where an item fails, the verdict names
what ships instead (per the pre-registered branches), not just "failed."

---

## 1. Conformance to pre-registration (gate — do this first)

1.1 Confirm the primary analysis unit is compound × suite (one row per
compound per suite), not response-level or compound × scale.

1.2 Confirm x = log10 bigram count from the frozen frequency table and
y = mean across scales of STRICT binary accuracy (correct=1, partial or
incorrect=0), per Trisha's ratification in DECISIONS 2026-07-03. Lenient
binarization or weighted partial appearing as the PRIMARY is a
conformance failure.

1.3 Confirm no naive row-level p-value appears anywhere in the deliverable.
Row-level Spearman, if present, must carry a clustered-bootstrap CI and be
labeled descriptive.

1.4 Confirm the dual sense split was computed at compound level (y rebuilt
from sense-filtered rows), not by filtering a row-level table.

Any 1.x failure: return to CC for correction before interpreting anything.
Numbers from a nonconforming analysis are not partially usable.

## 2. The headline numbers

2.1 Record ρ (Pythia) and ρ (GPT-2), with n per suite (how many of the 49
compounds coded cleanly and carry a frequency value). Apply the
pre-registered thresholds mechanically first (≥0.4 support / 0.2–0.4 weak /
<0.2 or wrong sign not supported), THEN discuss. The thresholds speak
before the reviewer does.

2.2 Pythia is confirmatory (Pile = training corpus); GPT-2 is
replication-under-proxy. If they disagree, the finding is Pythia's, and the
GPT-2 divergence is discussed as proxy-corpus limitation — not averaged
away, not silently dropped.

2.3 Dual sense split: does a11y-sense-only strengthen or weaken ρ relative
to all-rows? Strengthening is consistent with the wrong-domain-capture
story (generic-sense answers dilute the signal). Weakening needs its own
paragraph — do not paper over it.

2.4 Zero-inflation check: report how many compounds sit at exactly y=0
under the strict-binary primary. Then compare against the weighted
sensitivity run (handoff item 5b): if flat-zero compounds become ordered
under partial weighting AND that ordering tracks frequency, the partial
codes are carrying signal — that is a reportable finding about WHERE in
the correct/partial/incorrect ladder the frequency effect lives, and it
feeds the never_emerges discussion. If the zeros stay unordered, one
sentence and move on.

## 3. The word1 / tokenization interrogation (the review anchor)

3.1 Partial Spearman controlling word1 unigram frequency: does the bigram
effect survive? Record the attenuation, not just significance.

3.2 Partial controlling compound token count: same question.

3.3 If frequency does NOT survive the partials: the pre-registered branch
is that this ships as tokenization/word1 capture — a different, sharper
mechanistic claim. The review's job in that branch is to check the
alternative is stated as the finding, not as a caveat to a dead thesis.

3.4 S4 PMI robustness read: does PMI (association strength) tell the same
story as raw bigram frequency? If PMI and raw count diverge, which one
tracks accuracy — exposure or association?

## 4. Pre-registered prediction scoring (from DECISIONS 2026-07-03)

4.1 Token-competition / wrong-domain candidates (sensory_characteristics,
redundant_entry, status_message, error_identification,
pointer_cancellation, landmark_region, focus_management): which fired?
Score each: fired / partial / did not fire. Report the hit rate against
the base rate across all 41 (a 7/7 hit rate means little if 35/41 of all
compounds failed the same way).

4.2 tree_grid: did it land never_emerges as predicted?

4.3 Ceiling anchors (sign_language, text_formatting, form_field,
responsive_design): did they actually ceiling? An anchor that failed is
evidence AGAINST the frequency thesis and must be reported as such.

4.4 AD↔captions adjacent-substitution signature: observed?

4.5 B4 blank: record the count — how many of 49 regress from
correct/partial at intermediate scale to incorrect at maximum scale, and
in which suite(s). If ~1, the pre-registered collapse branch applies:
claim reverts to skip_link-only and ships that way.

## 5. Audit checks

5.1 Criteria-strictness vs predicted class: record the correlation. If
strictness tracks predictions, flag for discussion in Limitations — do not
bury it. If it doesn't, one footnote and done.

5.2 Trajectory-class stability: record count stable / total under the
single-flip test. Below ~45/49, the taxonomy section's confidence language
gets revised downward before any prose is written around it.

5.3 Regression guard: confirm CC's report shows the original 8 concepts'
coding outputs byte-identical pre/post translation.

5.4 Untranslated rows: list any rows CC returned to Trisha. These compounds
are excluded from n, and the exclusion is stated, not silent.

## 6. Exit questions (write the answers down)

6.1 Does the evidence as delivered support A3's wording ("frequency is the
distal cause"), or does it support only "frequency predicts trajectory"?
Causal language must be earned by the partials surviving plus the A2
trace — correlation alone gets "predicts."

6.2 What is the single weakest link in the A6 chain
(distribution → distributed representation → decision-point competition)
after these results? Name it. That is what blind study 2 or D7 targets.

6.3 Did anything in the deliverable surprise the reviewer in a way the
pre-registration did not anticipate? Log it in CAPTURE.md as a follow-up,
not as a mid-review scope change.

---

*Semantics owed to Trisha's ratification where marked in DECISIONS; the
rubric's questions are review machinery and carry no result-contingent
content. If any question turns out to be unanswerable from the deliverable,
that is a deliverable gap — return to CC, do not improvise.*
