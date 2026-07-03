# Criteria Handoff — 2026-07-03

> Written by Claude (Fable 5) at Trisha's request after completing 41/41
> criteria authoring in `docs/findings/criteria_authoring.csv` (moved from
> gitignored `_analysis/` 2026-07-03 — load-bearing artifacts don't live in scratch).
> Companion to DECISIONS.md entry 2026-07-03. Frequency table remains CLOSED.
> Expansion raws remain UNVIEWED until coding runs.

---

## TRISHA — your checklist (in order)

1. **Ratify or veto the three flagged placements** (5-minute skim of the
   worksheet rows; each is marked "Fable placement, Trisha may veto"):
   - `informative_image`: conveys-info-but-never-mentions-alt-text → PARTIAL
   - `accessible_description`: "it's the aria-describedby attribute" → PARTIAL
   - `cognitive_disabilities`: mental-illness conflation as whole answer → PARTIAL
   Any veto: change the cell, note it in DECISIONS (one line, dated).

2. **Git commit — this is the freeze that makes the predictions predictions.**
   Files: `docs/findings/criteria_authoring.csv`,
   `docs/findings/coding_coverage.csv`,
   `docs/findings/coding-criteria-draft.md`, `DECISIONS.md`,
   `docs/findings/criteria-handoff-2026-07-03.md`.
   Suggested message:
   `author n=49 coding criteria blind (41 rows; frequency table closed; doctrine + predictions pre-registered)`

3. ~~S8 — the `attention/` git mv~~ **DONE — verified 2026-07-03 (Fable):**
   `results/` inspected directly; no `attention/` directory exists (suite-first
   layout confirmed: gpt2/, pythia/, analysis/, frequency/, logits/,
   mlp_investigation/, _archive/). Gate reduces to the criteria commit alone.

4. **Unleash CC** (brief below — copy/paste or point CC at this file).

5. After CC delivers: the Spearman + trajectories come to **Fable for review
   before 2026-07-07** (word1 confound question + S4 robustness read are the
   review anchors). If the clock loses, the review rubric falls to Opus 4.6 —
   Fable will leave the interrogation list on disk if the 6th arrives without
   numbers.

---

## CC — the brief (paste this or point CC here)

**Context:** 41 new coding criteria are authored in
`docs/findings/criteria_authoring.csv` (status column = AUTHORED for all 41;
coverage map at `docs/findings/coding_coverage.csv` — both moved out of
gitignored `_analysis/` on 2026-07-03).
Trisha authored blind; your job is faithful mechanical translation. Where a
row's markers are untranslatable or ambiguous, STOP and return the row to
Trisha — do not improvise semantics. Traceability is sacred.

**Tasks, in order:**

1. **Translate** the 41 worksheet rows into the new-criteria section of
   `src/accuracy_coding.py`. Column mapping: `correct_criteria` +
   `correct_markers` → correct rules; `partial_criteria` → partial rules;
   `incorrect_markers` → incorrect rules (includes wrong-domain senses,
   trench-coat patterns, circular, degenerate — reuse the existing
   circular/degenerate detectors from the original 8).

2. **Encode the coding doctrine as a comment block** at the top of the new
   section (verbatim from DECISIONS 2026-07-03): lateral→incorrect,
   vertical→partial, synonym→nods, mechanism-for-concept→partial (except
   where mechanism constitutes concept), trench-coat→incorrect.

3. **Implement sense recording** (Option A + dual analysis, per DECISIONS
   2026-07-02/03): per-response `sense_observed` ∈ {a11y, generic} computed
   from a GLOBAL a11y marker list (screen reader; assistive; WCAG; announce;
   blind; low vision; keyboard-only; ARIA; alt text) UNION the per-row
   `a11y_sense_markers` column. Hoist common markers into the global list;
   per-row column supplies the compound-specific additions.

4. **Regression guard:** the original 8 concepts' coding logic is UNTOUCHED.
   Verify by re-running coding on the pre-expansion results and diffing —
   original-8 outputs must be byte-identical before and after your changes.

5. **S5 — captions rename fix** (coverage CSV MUTANT rows): resolve the
   three-way captions/closed-captions naming split, including the DANGEROUS
   CELL — the closed-captions declarative row must not fall through to
   `incorrect` on a name-miss. Document the resolution in DECISIONS.

6. **Resolve the two VERIFY rows** (link text, form label): confirm which
   evaluative branch in `accuracy_coding.py` catches their prompts; report
   findings, update coverage CSV status.

7. **Gate check before running anything downstream:** confirm Trisha's
   criteria-freeze commit exists. (S8 verified DONE 2026-07-03 — no
   `attention/` in results/, suite-first layout confirmed by direct
   inspection.) Then:

8. **Run the pipeline:** coding over the frozen expansion raws
   (tag=expansion, both suites, all scales) → `gap_analysis` rerun →
   `per_concept_trajectories.csv` → **dual Spearman** (frequency vs accuracy:
   all rows AND a11y-sense-only), per the S4 PMI robustness column trigger.

9. **Deliver:** translation diff summary; regression-check result;
   trajectories CSV; both Spearman values with n's; a table scoring the
   DECISIONS 2026-07-03 pre-registered predictions (which token-competition
   candidates fired, tree_grid trajectory class, ceiling-anchor accuracy);
   and a list of any rows returned to Trisha untranslated.

**Do not:** modify criteria semantics, view/report frequency-table contents
to Trisha before the Spearman lands packaged, or run gap_analysis before
both gate conditions are met.

---

## ADDENDUM 2026-07-03 (post-freeze, pre-results) — Spearman spec amended

> Added by Fable 5 while CC was PAUSED; no expansion output viewed by
> anyone. Authoritative spec: DECISIONS 2026-07-03 "Spearman
> unit-of-analysis + interpretation thresholds pre-registered." This
> addendum amends Task 8 and adds two deliverables; everything else in the
> brief stands.

**Task 8 amendment — the dual Spearman runs at compound level, not row
level:**

1. PRIMARY: one observation per compound per suite. x = log10 bigram count
   (frozen frequency table). y = mean across scales of STRICT binary
   accuracy (correct=1, partial or incorrect=0) — ratified by Trisha
   2026-07-03, see DECISIONS. Do NOT use lenient binarization or weighted
   partial in the primary.
   Report ρ + n per suite, separately for Pythia and GPT-2, for BOTH sense
   splits (all rows / a11y-sense-only, with y rebuilt from filtered rows).
2. Also report Kendall's tau-b for each primary cell.
3. Partial Spearman (per suite, all-rows split): controlling (a) compound
   token count, (b) word1 unigram frequency from the PMI/S4 columns.
   Report raw ρ alongside each partial so attenuation is visible.
4. Row-level Spearman: DESCRIPTIVE ONLY, clustered bootstrap over
   compounds (≥1000 resamples) for the CI. No naive row-level p-value in
   any deliverable.
5. SECONDARY: repeat primary with y = accuracy at maximum scale.
5b. SENSITIVITY (descriptive only): repeat primary with weighted y
    (correct=1 / partial=0.5 / incorrect=0). Report alongside, clearly
    labeled; thresholds apply to the strict-binary primary only.

**New deliverables (pre-declared audit checks):**

6. Criteria-strictness check: per worksheet row, count incorrect_markers;
   correlate with predicted trajectory class (from the DECISIONS
   2026-07-03 predictions). Report the value either way.
7. Trajectory-class stability: per compound, flip the single most
   influential response code one adjacent level and re-derive the class;
   report count stable / total, and list the unstable compounds.

**Deliverable routing unchanged:** everything packages to Fable for review
per `docs/findings/spearman-review-rubric-2026-07-03.md`. The frequency
table stays closed to Trisha until the review lands.
