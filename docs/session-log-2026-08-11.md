# Session log — 2026-08-11

Continuation of the audit response. Three pieces of work landed; two claims were cut
on the basis of data examined tonight.

---

## 1. Decision 0015 implemented — concept key normalization

Commit `1e489c2`. `concept` is normalized to canonical form (lowercase, underscores)
on every frame that carries it; the on-disk spelling is preserved as `concept_raw`;
every consumer that *dispatches* on the concept reads `concept_raw` rather than
`concept`.

Verified a no-op on every number: gap tables byte-identical, `elicitation_coded`
joined before/after on `(model, prompt_id)` gives 3458/3458 rows with accuracy
changed on zero, `dual_spearman` reproduces the frozen `compound_accuracy_table.csv`
with zero differing cells.

**Found during implementation, not in the brief:** `src/dual_spearman.py` is a second
dispatching consumer (`code_response` and `observe_sense`, two call sites). Left
alone it would have coded every declarative row incorrect and flipped every sense to
generic — silently, since both miss without raising. The brief named only
`gap_analysis`. `gap_analysis` also turned out to have two call sites, not one; the
second is inside the emergence-threshold loop and was passing the normalized loop
variable.

Vocabulary 233 → 232. Exactly one many-to-one collapse:
`['captions', 'closed captions'] → 'closed_captions'`. Note this is a **2 → 1**
collapse in-frame, not the three-way collapse 0015 describes — the third spelling
(`closed_captions`) lives in the frequency tables, which the canonical key now
*matches* rather than merges.

**Also corrected:** the `captions` → `closed captions` rename was cited as commit
`7f84365` in CLAUDE.md, `src/analysis.py`, and 0015. It is actually `ca01b59`
(2026-08-05, "rearrange results directory structure") — the same commit that moved
the results layout and stranded the paper's frequency numbers. `7f84365` is "add
missing compounds + make suite iteration dynamic," which took `COMPOUNDS` from 49 to
53. Verified with `git log -S` in both directions.

---

## 2. Decision 0014 implemented — `pythia-13b` → `pythia-12b`

All three layers together: directory, five CSVs plus manifest, and the `model` column
in-file across 326,880 rows. The column rewrite was byte-level with asserted per-file
counts (76320/63360/63360/63360/60480) matching the manifest exactly, and
`pythia-13b` was verified to appear only in the `model` column and never in prompt
text before any edit. Alias retired at `src/analysis.py:267`.

Total binding rows unchanged at 2,150,144. Skip list and gpt2 collision report
byte-identical to baseline.

`OLMo-2-1124-13B` is a genuinely different model and was matched at every step.

Two corrections to the ADR, recorded as an amendment: the stated failure mode was
wrong (a stray `pythia-13b` parses as 13B and sorts *last*, not scale 0 sorting
first), and the "Depends on" line was not satisfiable in code — the notebook has no
model list, only a hand-typed `model_name`, so the guard is wetware.

---

## 3. Decision 0016 — OLMo checkpoint pinning

Supersedes 0012, which described the wrong problem. Full write-up in
`docs/decisions/0016-olmo-checkpoint-pinning.md`.

Short version: all three OLMo models pinned to explicit revisions in
`src/olmo_config.py` and rerun. **Elicitation output came back byte-identical** —
`git diff` on `results/elicitation/olmo/` shows no change to any CSV, only the
manifests differ, and only because they now carry revision fields the old ones
lacked.

ρ = 0.5823 unchanged, τ = 0.4610 unchanged, partials 0.5810 / 0.5969 unchanged.

So the checkpoint difference does not affect these prompts. The 0.4819 / 0.3288
divergence between the two old 1B result sets is not the corpus and not the
checkpoint; it most likely originates in a Colab session whose code exists nowhere in
this repo (commit `ebb4d2b`). Both are superseded by pinned runs, so the question is
academic.

Manifest now records the revision twice — model config and HuggingFace resolve —
plus the commit SHA. Run metadata: 2026-08-12T00:03 UTC, commit `2c2e926`,
A100-SXM4-80GB, `do_sample=False`, TL 2.18.0.

---

## 4. Two claims cut

Both were examined against the full three-family data tonight and neither survives.
Recording the data rather than the decision — the cuts follow obviously from the
numbers, and nobody is going to re-propose them.

### Fluent wrongness — entropy does not support it

Mean output entropy when incorrect on accessibility, minus entropy when correct on
control. Positive means *more* uncertain when wrong, which is the ordinary case. The
claim required the gap to go negative — confidently wrong — at scale.

| suite | scale | a11y-wrong H | ctrl-right H | gap |
|---|---|---|---|---|
| pythia | 160M | 4.3233 | 3.1541 | +1.1691 |
| pythia | 410M | 3.9213 | 3.2012 | +0.7200 |
| pythia | 1B | 3.7176 | 3.0190 | +0.6986 |
| pythia | 2.8B | 3.6732 | 3.2593 | +0.4139 |
| pythia | 6.9B | 3.6182 | 3.2919 | +0.3263 |
| pythia | 12B | 3.5972 | 3.0655 | +0.5316 |
| gpt2 | 124M | 4.7010 | 3.9656 | +0.7354 |
| gpt2 | 355M | 4.5171 | 3.9990 | +0.5180 |
| gpt2 | 774M | 3.9531 | 3.6654 | +0.2877 |
| gpt2 | 1.5B | 3.5251 | 3.4310 | +0.0941 |
| olmo | 1B | 4.3774 | 3.5690 | +0.8084 |
| olmo | 7B | 3.7022 | 4.2741 | **−0.5719** |
| olmo | 13B | 3.8735 | 5.1069 | **−1.2333** |

Three families, three behaviours. Pythia stays positive throughout. GPT-2 shrinks
monotonically toward zero. OLMo crosses and goes strongly negative at 7B and 13B.
There is no cross-family pattern to report.

Note also OLMo-13B's `ctrl-right` entropy of 5.1069 — the model is *more* uncertain
on correct control answers than on wrong accessibility ones. The control cell is
small (2–5 responses per scale, per the earlier external review), so that figure
should not be leaned on either.

The underlying *phenomenon* is still real and still visible in outputs — the 404-style
template, the first-person narrative about failing to add an alt attribute, ARIA's
confident wrong expansions. What is not supported is the quantitative claim that
models are measurably more confident when wrong. Cut. "Confidently wrong at scale"
was a quip that got dressed as a hypothesis.

### Completion paradox — one concept, two items per cell

Re-run after 0015 landed, which was expected to add concepts to the join. It added
one, not three: post-normalization the completion battery has `alt_text`,
`closed_captions`, `page_title`, `script`; the declarative battery has the first two.
`page_title` and `script` are syntactic controls with no declarative arm **by design**
(`code_completion`'s own docstring says so), not a normalization gap.

So the paired set went 1 → 2, and the effect does not survive the second concept:

| suite | scale | concept | compl | decl | gap |
|---|---|---|---|---|---|
| pythia | 160M | alt_text | 100.0% | 0.0% | +100.0 |
| pythia | 410M | alt_text | 100.0% | 50.0% | +50.0 |
| gpt2 | 355M | alt_text | 100.0% | 50.0% | +50.0 |
| gpt2 | 774M | alt_text | 100.0% | 50.0% | +50.0 |
| olmo | 13B | alt_text | 100.0% | 50.0% | +50.0 |
| pythia | 1B | closed_captions | 50.0% | 0.0% | +50.0 |
| pythia | 12B | closed_captions | 50.0% | 0.0% | +50.0 |
| gpt2 | 355M | closed_captions | 50.0% | 0.0% | +50.0 |
| olmo | 1B | closed_captions | 50.0% | 0.0% | +50.0 |
| pythia | 2.8B | closed_captions | 50.0% | 100.0% | **−50.0** |
| gpt2 | 1.5B | closed_captions | 50.0% | 100.0% | **−50.0** |
| olmo | 7B | closed_captions | 50.0% | 100.0% | **−50.0** |

`alt_text` remains clean and positive everywhere. `closed_captions` goes both ways —
three negatives where there were previously zero. The effect is alt-text-specific.

The cell values are also only ever 0 / 50 / 100, because completion is n=2 per cell.
A single item flipping moves a cell by fifty points. The earlier
7 greater / 6 ties / 0 less, p = 0.0078 was one concept at two items per model.

Cut. It would need a purpose-built completion battery to be a claim, and that is a
new experiment, not a fix.

---

## Where this leaves the paper

Section I is now: **the gap exists, measured across 13 models, and it closes from
above at 12B.** Behavioural, uniform, one surprise at maximum scale.

The paring is consistent across everything cut so far — trajectory taxonomy demoted
(CLAIMS B3, 20/102 assignments survive perturbation), perplexity demoted (blind study
scored it fragile, 5/6 sessions), fluent wrongness cut, completion paradox cut. Every
one was a named sub-phenomenon that failed to generalize once the data got broader.

Which is the argument, not a consolation: **the gap is more than one thing.** Each
named sub-phenomenon was one facet — fluent wrongness is what it looks like on
acronyms, the completion paradox is what it looks like on alt text, peak-regress is
what it looks like at 12B on three concepts. None held across the whole because none
*was* the whole. That is why no single mechanism explains it, and why the eliminative
structure is the right shape.

What survived contact with more data: the gap itself, the binding null, and the
frequency correlation with its ceiling.

---

## State

**Accuracy line: closed.** Every number on disk is correct.

- 0010, 0011, 0014, 0015, 0016 accepted; 0012 superseded by 0016; **0013 is the only
  open decision** and it blocks nothing (file locations)
- Current frequency figures: pythia **0.5875**, gpt2 **0.5194**, olmo **0.5823**
- The paper still cites 0.5715 / 0.5052, computed at `ca0319e` against a
  `compound_accuracy_table.csv` built before `results/elicitation/pythia/pythia-2.8b/`
  existed — an incomplete input, not an alternative coding

**Not a re-ink.** Section III of the current manuscript is being substantially
rewritten rather than corrected in place; the current numbers go into whatever
replaces it. Noted because the old section reports three per-scale OLMo correlations
(ρ = 0.33 / 0.45 / 0.51, "strengthening monotonically with scale") that the current
pipeline does not produce — it produces one pooled figure, ρ = 0.5823, n = 49. That
discrepancy needs resolving in the rewrite, not before it.

**Known and unfixed, deliberately:** `pmi` in the frequency tables is computed as
`log2(bigram / (word1 · word2))` with no corpus-size term, so values sit around −38
rather than in the usual PMI range. Rank-invariant, so Spearman and Kendall are
unaffected and the robustness checks are valid. Worth either renaming the column or
adding `log2(N)` before any PMI value is reported in prose.
