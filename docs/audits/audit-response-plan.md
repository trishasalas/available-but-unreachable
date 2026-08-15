# Audit response plan

- **Created:** 2026-08-08
- **Last updated:** 2026-08-10
- **Audit:** `docs/claude-science/tmlr_audit_2026-08-09.md`, run at commit `6786d13`
- **Findings CSV:** `docs/claude-science/tmlr_audit_findings_2026-08-09.csv`
- **Pending decisions:** `docs/decisions/` (0010–0015)

> **Scope.** Paper prose findings are deliberately **out of scope**. The old prose is knowingly stale and is being rewritten under a new framing (see below). Findings A5, A13, and most of A14 are therefore deferred, not fixed.

---

## Changelog

**2026-08-15** — Restored four mechanistic evidence CSVs flagged by Sol audit (Section 5): d6_multihead_ablation/{multihead-ablation,candidate-heads}.csv, head_characterization/{head-characterization,collocation}.csv. Packaging fix, no science change.

**2026-08-10** — Decision 0014 implemented (`pythia-13b` → `pythia-12b`, all three layers, alias retired) and amended with two factual corrections found during implementation. **The accuracy line is down to one code change.** See its revised status below.

**2026-08-09 (evening)** — Frequency work landed. `frequency-analysis.ipynb` split into `frequency-{pythia,gpt2,olmo}.ipynb` matching the repo convention; index named as a literal in each, no `SUITE_INDEX` dict, no loop over suites. A18's sentinel and truthiness bugs fixed. A1 retired structurally — `dual_spearman.run` is now the sole writer of all six outputs and `frequency.py` writes no global file. A22's p-value formatting and index caching both closed. Frozen `frequency_table.csv` repaired in place (blank rows and phantom columns stripped, verified no-op on the 49 real rows). **A4 turned out not to be a corpus finding** — see below. Session log: `docs/session-log-2026-08-09-frequency-split.md`.

**2026-08-09 (afternoon)** — Steps 1 and 2 complete. `src/analysis.py` fixed and merged (`aa7e1bb`); decision 0010 accepted. Pass condition met: pythia-160M declarative = 0.5, declarative pivot n=10 (the ten originals, `closed captions` included), evaluative pivot unchanged at n=5. **The 12B declarative regression is now visible** — see Results below. Four new open items surfaced that were not in the audit.

**2026-08-09** — Substantially revised. Phase 0 is complete; the tree is clean and pushed. Archive reorganized into `_Archive/{_notebooks,_results,_src}` and tracked. Stale `.claude/worktrees/entropy-manifest-update` removed (branch was already merged; it held a pre-OLMo, pre-binding snapshot). Two pre-expansion reference tables rescued from it before deletion. `data/accessibility.yaml` inspected: the original/expansion split is explicit in section comments, and elicitation CSVs confirmed to have no `source` column. Decisions migrated to ADR format in `docs/decisions/`. New work added at the end: evaluative battery expansion and logit-lens follow-up.

**2026-08-08** — Created from the audit.

---

## Status: what is already done

- [x] Working tree clean, committed, pushed to private origin
- [x] `results/frequency/frequency_table.csv` restored — SpreadJS had rewritten it with full-field quoting, CRLF line endings, and ~15 phantom trailing columns. The frozen Pile table is intact (`screen_reader = 32100`)
- [x] Archive reorganized and **tracked** — the five previously-untracked `results/_archive/*.csv` are now in git under `_Archive/_results/`
- [x] Stale worktree removed
- [x] Pre-expansion reference tables preserved: `_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv`, `gpt2_gap_PRE_EXPANSION_REFERENCE.csv`, `completion_paradox_PRE_RENAME_REFERENCE.csv`

**Still worth doing:** set VS Code `workbench.editorAssociations` so `*.csv` opens in the plain text editor by default. SpreadJS rewrites the entire file on save, including columns never touched. This will happen again otherwise.

---

## The accuracy line

> **Added 2026-08-09.** The plan below is a complete cleanup. Accuracy does not require  
> a complete cleanup. This section separates the two, because the list otherwise reads  
> as one long undifferentiated obligation.

**The bar is: every number in the paper is correct.** Not tidy, not fully documented — correct.

### Trustworthy now

- **The gap tables.** Concept population verified against the ten Experiment 1 originals, `source` derived rather than hardcoded, the impossible 6.9B negative resolved, the 12B declarative regression real and reproducing a finding recorded 2026-06-28. Section I's core numbers are sound as of `aa7e1bb`.
- **The binding data.** 227/227 compounds round-trip, all 65 CSVs match schema, manifests reconcile. Section II's null (A7: gpt2 r=0.087, pythia r=−0.003, olmo r=0.115) is computed from clean data.

### NOT trustworthy — these change numbers

> **Revised 2026-08-11.** All four of the original four are done. No code change that moves a number remains open.

**✓ DONE 2026-08-11 — 0015's code.** `concept_raw` for the coding layer, normalized `concept` for joins. Landed in *three* files, not two — `src/dual_spearman.py` is a second dispatching consumer the brief did not name. Verified a no-op on every number: gap tables byte-identical, and `elicitation_coded` joined before/after on `(model, prompt_id)` shows accuracy changed on 0 of 3458 rows. Brief: `docs/tasks/task-0015-concept-normalization.md`. See 0015's Implementation section.

**✗ STILL OPEN — the completion join (A3).** Unblocked as of 2026-08-11; 0015's keys now normalize. Currently resolves on `alt text` alone: 7 greater / 6 ties / 0 less, p = 0.0078 — significant *through a broken join*. What it does with **two** paired concepts is an open empirical question — `alt_text` and `closed_captions`. Not four: `page_title` and `script` are syntactic controls with no declarative arm by design, so normalization takes the paired set from 1 to 2. See 0015's amendment.

**✓ DONE 2026-08-11 — the two OLMo-1B runs.** Now an accuracy item, because OLMo entered the pre-registered battery on 2026-08-09. Two result sets exist: ρ = 0.4819 and ρ = 0.3288, **identical corpus counts**, differing on 18 of 49 `mean_accuracy` rows. One records `Revision: stage1-step990000-tokens2077B`; the other records no revision. Raw elicitation confirms different generations for the same prompt under greedy decoding. This is a checkpoint adjudication, not a corpus one.

**✓ RESOLVED — the paper will be rewritten from a different copy.** The paper cites ρ = 0.5715 (pythia) and 0.5052 (gpt2). Correct values are **0.5875 / 0.5194 / 0.5823**. The old numbers were computed at `ca0319e` against a `compound_accuracy_table.csv` built when `results/elicitation/pythia/pythia-2.8b/` did not yet exist — an incomplete input, not an alternative coding. Ruled 2026-08-09: re-ink. CLAIMS A3's cited values need the same update.

**✓ DONE — A18, frequency pipeline bugs.** Sentinel screening and `is not None` landed in the new per-suite notebooks. 49 queried / 49 returned / 0 screened, all three suites.

**✓ DONE — A1, filename clobbering.** Retired structurally rather than patched. `dual_spearman.run` is the sole writer of all six outputs; `frequency.py` writes no global file; `query_infinigram`'s index argument is now required, so a robustness path cannot silently inherit a default.

**✓ RESOLVED, NOT AS STATED — 0012, the OLMo corpus.** **A4 was never a corpus finding.** The corpus columns are byte-identical across both OLMo result sets; the divergence is entirely in `mean_accuracy`. `SUITE_INDEX` had always mapped OLMo to `v4_olmo-mix-1124_llama` correctly. The real defect was in `rowlevel_bootstrap`, which built its x-vector via `tab.drop_duplicates('compound')` **across all suites** — so whichever suite sorted first supplied x for every other suite. Fixed. OLMo's corpus-matched ρ = 0.5823 and τ = 0.4610 now reproduce the audit's hand-computed figures exactly. `docs/decisions/0012` still describes the wrong problem and **needs superseding as a checkpoint-pinning decision.**

**That is the accuracy list now: land 0015, fix the join, adjudicate the OLMo checkpoints, re-ink Section III.**

### Below the line — does not change a number

Everything else. Recorded so it is visible, not so it blocks:

- p-values printing as `0.0` (A22) — **DONE 2026-08-09**, now scientific notation
- file locations, `adhoc/` moves, archive tidying (0013)
- `pythia-13b` / `pythia-12b` naming (0014) — **DONE 2026-08-10**
- figure scripts and dangling doc pointers — **these come last**, after the data  
settles; repairing a figure path before the data is final is the same error as  
updating prose before the numbers stabilised
- CLAIMS pointer updates, dead `src/` modules, the entropy coverage gap
- the latent gpt2/gpt2-small collision — currently 0 rows, harmless until the skipped  
CSV is fixed
- TransformerLens 2.17 → 2.18 drift — undocumented, but the results reproduce

### Not required for the paper at all

- **The evaluative battery expansion** (preregistration 0002, step 7) and the  
**two-framing design**. These are a new experiment. They make a stronger paper and  
they are not a prerequisite for the one that exists.
- **The logit lens work** (step 9). Same — a revision or Paper 3, not a blocker.

---

## The ordered plan

Each step unblocks the next. The "why" is the dependency, not the motivation.

### 1. Fix `src/analysis.py`

**DONE 2026-08-09** — commit `aa7e1bb`, merged to main. Decision 0010 accepted.

One editing session, four changes:

- [x] **Source flag (A6).** `load_all_results` hardcodes `df['source'] = 'original'`, unguarded — while the adjacent `domain` assignment two lines above *is* guarded. Elicitation CSVs have no `source` column, so the filter in `gap_analysis.py:76-78` has never removed a row. Derive `source` from membership in the ten original concepts. See decision 0010. The ten, from `data/accessibility.yaml` (section comment: "Original Paper 1 Experiment 1 prompts"): screen reader, WCAG, skip link, alt text, ARIA, focus indicator, keyboard navigation, color contrast, semantic HTML, **closed captions** (renamed from `captions` in `ca01b59` — getting this wrong silently drops to nine). *(Commit corrected 2026-08-11: `7f84365` widens `COMPOUNDS` 49→53 and does not touch the concept name; verified with `git log -S`.)*

- [x] **Concept key normalization (A3 root cause, decision 0015).** **DONE 2026-08-11.** Landed in `src/analysis.py`, `src/gap_analysis.py` (2 call sites), and `src/dual_spearman.py` (2 call sites — a dispatching consumer the brief did not name). Pass conditions all met: 160M declarative 0.5, pivot n=10, evaluative n=5, gap tables byte-identical, source counts unchanged, 0 of 3458 per-row accuracy codes changed. Vocabulary 233 → 232, one collapse (`captions` + `closed captions` → `closed_captions`). Shape: preserve the on-disk spelling as `concept_raw`, normalize `concept` in place at load, have `gap_analysis` pass `concept_raw` to `code_response`. It cannot land as a plain in-place normalization, because `src/accuracy_coding.py` dispatches on a 52-key rules dict in space form, case-sensitively (`'WCAG'`, `'semantic HTML'`), and returns `'incorrect'` on a miss rather than raising. **Zero of those 52 keys survive canonicalization**, so normalizing the column without the `concept_raw` split would silently code every declarative row incorrect — declarative mean 0.0, not 0.5. Three spellings exist across batteries: `closed_captions` (frequency), `closed captions` (declarative), `captions` (completion). Pass condition when it lands: 160M declarative stays 0.5, pivot stays n=10, evaluative stays n=5.

- [x] **gpt2 double-count (A16).** **REPORTED, NOT RESOLVED** — and it turns out to be *latent*, not active. `_extract_scale` maps both `'gpt2'` and `'gpt2-small'` to 124M and both directories exist. Nothing dedupes, so every gpt2-small row is counted twice in any groupby over scale.

- [x] **Skip counter.** `_extract_domain` silently `continue`s any file whose stem doesn't match `KNOWN_DOMAINS`. Add skipped-file counts to the load printout so scope changes announce themselves instead of hiding.

*Why first: everything downstream reads this file. Nothing computed is trustworthy until it is.*

**Known good here, per audit:** `_extract_scale` handles OLMo correctly (`'olmo'` ends in `'m'`, `float('olm')` raises, loop continues) and the `pythia-13b` alias works. `binding_summary` and `max_binding_layer` are fine. `tokenization_comparison` is stale — hardcodes 11 compounds against a 53-compound battery — but is not on the critical path.

### 2. Re-derive the gap tables and check pythia-160M declarative

**DONE 2026-08-09.** Pass condition met.

- [x] Re-derive with the source flag actually working
- [x] Confirm pythia-160M declarative == 0.5
- [x] Confirm the negative gap at Pythia-6.9B is gone (−0.0392 → +0.3)

See **Results — the corrected gap** below. The prediction recorded here on 2026-08-08 was half right: the negative at 6.9B resolved, but a negative appears at 12B, and it is real.

Expect **0.5**, matching `_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv`. Currently 0.7059 (51-concept pooled).

*Why: this is the regression test. It confirms step 1 against a preserved artifact rather than against reasoning. It is also where the impossible negative gap at Pythia-6.9B should disappear — the -2.0 was the pooling bug announcing itself, since a negative gap is impossible under the theory.*

**Prediction on record (2026-08-08, scored):** the negative disappears ✓, the gap stays positive at all six Pythia scales ✗ — it does not; a real negative appears at 12B. The monotonic declarative rise does *not* survive, and that is the finding. 6.9B is the strongest evaluative performer and still has the gap ✓.

### 3. Rule on decision 0011 — the estimand

- [x] Ruled

Paired within-concept, or difference of pooled means.

*Why here: it needs the corrected numbers to judge, and everything after depends on knowing what "the gap" means.*

### 4. Rule on decisions 0012, 0013, 0014

- [x] 0012 — OLMo x-corpus
- [x] 0013 — archival status of the five `results/analysis` tables
- [x] 0014 — `pythia-13b` vs `pythia-12b` — accepted and executed 2026-08-10

OLMo x-corpus; archival status of the five `results/analysis` tables; `pythia-13b` vs  `pythia-12b`.

*Why before any regeneration: the next pipeline run either entrenches or silently*  *undoes each of these.*

### 5. Fix the frequency pipeline, then regenerate once

- [ ] **Per-suite filenames (A1).** `frequency_table.csv` and `spearman_summary.csv` use  fixed names inside a loop over suites. Note the fix is narrower than it looks — the    `{suite}_frequency_accuracy.csv` files are already per-suite.
- [ ] **Corpus column.** Required by whichever way 0012 goes; without it provenance is  unrecoverable from the artifact.
- [ ] **A18 latent bugs.** Infini-gram's `-1` failure sentinel flows into Spearman as a  real value — screen `count < 0` to NaN before writing. `cond_prob == 0.0` becomes    `None` via a truthiness check; use `is not None`. Partial-correlation controls are    dropped from the per-suite path.
- [ ] **A22.** p-values round to 4dp, so a true p≈1e-6 ships as `0.0`. Format  scientifically. Also cache per index — pythia and gpt2 both map to the Pile and    currently re-run the full query loop each.

- [ ] Regenerate the battery once, cleanly

*Why after 4: run this once, with the decisions already baked in.*

### 6. Fix the completion-paradox join

- [ ] Re-run the join with normalized keys
- [ ] Fix `paper/generate-figures/generate-fig-completion-paradox.py:51`
- [ ] Grep domain batteries for concepts with both cloze and declarative items

*Why after 1: it needs key normalization to exist.* Key normalization landed 2026-08-11, so this is unblocked. Then re-run and see what the paradox does with **two** paired concepts instead of alt-text-only — `alt_text` and `closed_captions`. Not four: post-normalization the completion battery carries `alt_text`, `closed_captions`, `page_title`, `script`, but the last two are syntactic controls with no declarative arm by design (`code_completion`'s docstring says so). Current state: 7 greater / 6 ties / 0 less, p = 0.0078 — significant *through a broken join*.

Also fix `paper/generate-figures/generate-fig-completion-paradox.py:51`, which reads a  path that no longer exists.

**Free win worth checking:** grep the domain batteries (legal/medical/finance) for any  concept with both a cloze item and a declarative item. If the completion paradox  extends beyond accessibility, that is a substantially larger result.

### 7. Author the evaluative items and freeze preregistration 0002

- [ ] Author framing A (question) items
- [ ] Author framing B (cloze) items
- [ ] Verify every target is a single token in NeoX **and** GPT-2 BPE
- [ ] Fill the concept mapping table; confirm the exclusion list
- [ ] Delete the authoring worksheet
- [ ] **Commit the freeze** — must precede any run

Two framings per concept (see below). `docs/preregistrations/0002-evaluative-prompts.md`.

*Why now and not earlier: authoring is slow, and it is yours alone — ground truth in*  *accessibility is the one thing that cannot be delegated. Nothing above depends on it.*  *The freeze commit must precede any run; that is the entire mechanism.*

### 8. Run the evaluative battery

- [x] Run, 13 models
- [x] Code the results

Elicitation only, 13 models. *Why cheap: no binding, no frequency, no infini-gram.*

### 9. Write preregistration 0003 and run the logit lens

- [ ] Draft 0003 (answer position + target token, per item)- [ ] Commit the freeze- [ ] Run

*Why last: it needs 0002's items frozen, because answer position and target token are*  *per-item.*

### Then housekeeping — none of it blocks the science

- [ ] A10 — re-home evidence for NAILED claims A4/A5/D6
- [ ] A7 / A8 — update CLAIMS B7 and B4 against regenerated data
- [ ] A16 — entropy battery gaps (pythia-1b has 1 of 5 domains; 13 legacy schema-drifted CSVs)
- [ ] A17 — OLMo provenance: 1B commit-sha files in the 7B elicitation dir
- [ ] A19 — archive superseded frequency-era artifacts (four different "pythia primary rho" values on disk)
- [ ] A20 — delete dead `src/` modules, orphan `.pyc`, `data/backup.py`. **Do not delete** top-level `data/*.yaml` (prompt files, key `prompts`) — a different artifact from `data/binding/*.yaml` (key `compounds`). **Keep** `dual_spearman.py`, `closeout_followups.py`, `d6/d7/d8_*.py`.

- [ ] A21 — ~14 dangling doc pointers; the duplicate D7 (now noted in `docs/decisions/README.md`); appendix table placeholder. Set VS Code `workbench.editorAssociations` for `*.csv`

---

## Results — the corrected gap (2026-08-09)

With `source` derived correctly, restricted to the ten original concepts:

| scale | declarative | evaluative | gap      |
| ----- | ----------- | ---------- | -------- |
| 160M  | 0.5         | 0.2        | +0.3     |
| 410M  | 0.8         | 0.4        | +0.4     |
| 1B    | 0.6         | 0.2        | +0.4     |
| 2.8B  | 1.2         | 0.6        | +0.6     |
| 6.9B  | 1.3         | 1.0        | +0.3     |
| 12B   | 0.9         | 1.0        | **−0.1** |

### The 12B declarative regression

The impossible negative at 6.9B is gone. A negative appears at **12B**, and unlike the previous one it is not an artifact. Per-concept declarative codings, Pythia, ten originals:

| concept             | 160M | 410M | 1B   | 2.8B    | 6.9B    | 12B     |
| ------------------- | ---- | ---- | ---- | ------- | ------- | ------- |
| ARIA                | inc  | inc  | inc  | inc     | inc     | inc     |
| WCAG                | inc  | inc  | inc  | inc     | **cor** | **cor** |
| alt text            | inc  | part | part | **cor** | **cor** | **cor** |
| closed captions     | inc  | inc  | inc  | **cor** | inc     | **inc** |
| color contrast      | part | cor  | part | part    | cor     | cor     |
| focus indicator     | part | inc  | inc  | inc     | inc     | inc     |
| keyboard navigation | part | cor  | cor  | cor     | cor     | **inc** |
| screen reader       | part | part | cor  | cor     | cor     | cor     |
| semantic HTML       | part | part | inc  | part    | part    | part    |
| skip link           | inc  | part | inc  | cor     | cor     | **inc** |

Column sums: **160M 5 · 410M 8 · 1B 6 · 2.8B 12 · 6.9B 13 · 12B 9**

Declarative capability peaks at 6.9B and **drops at 12B**. Three concepts regress: `keyboard navigation` (correct → incorrect), `skip link` (correct → incorrect), and `closed captions` (already regressed at 6.9B, stays incorrect).

**This restores a finding the pooled data was hiding.** DECISIONS.md, 2026-06-28, gap analysis findings table: *"12B gap closes via declarative regression; declarative drops 70% → 50%; skip_link and keyboard_navigation regress."* Same phenomenon, same two named concepts. The 41 frequency-stratified expansion compounds had been papering over it — the polluted table showed declarative rising monotonically 35.3 → 55.9 with no 12B regression at all.

**Consequence for Section I.** The story is not "the gap is positive at every scale." It is: the gap opens early, widens to a maximum at 2.8B, then **closes from above** at maximum scale as declarative capability regresses. Inverse scaling at the paradigm level, not merely for `skip link`. This also connects directly to CLAIMS B4 (peak_regress is not skip_link-specific) and to the ARIA fluent-confabulation pattern: scale produces different failure modes for different concepts rather than uniform improvement.

Worth noting `semantic HTML` never reaches correct at any scale, and `ARIA` and `focus indicator` never emerge at all — four of ten concepts are at or near floor throughout.

### What the reference table does and does not validate

`_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv` is byte-identical to `results/analysis/pythia_gap.csv` at commit `0f116a5` (2026-06-27). It matches the new output exactly at 160M, 410M, and 1B, and diverges at 2.8B (+0.2), 6.9B (−0.1), and 12B (−0.1). The evaluative column matches at every scale.

The divergence is **upstream, not the filter**. A source filter selects a concept population identically at every scale; three scales match exactly and the population verifies correct. `0f116a5` predates both `ca0319e` (2026-07-03 — 41 expansion criteria and the coding doctrine) and `ca01b59` (2026-08-05 — `max_tokens` standardized from 10/20 to 100). Both the coding rules and the generations changed underneath it.

**So the reference validates the concept population, not the scores.** It should be labelled as such before anyone uses it as an oracle again. Which of the two is authoritative for scores is an open decision — see below.

---

## Open items surfaced 2026-08-09 (not in the audit)

- [ ] **Reference authority.** Is the 2026-06-27 table or the current pipeline authoritative for gap *scores*? The concept population is settled; the scores differ because coding rules and generation length both changed. This bears directly on Section I's numbers and wants its own decision.
- [ ] **Latent gpt2 collision.** `gpt2-small` collides with `gpt2` at 124M but contributes **0 rows**, because its only CSV (`results/entropy/gpt2/gpt2-small/gpt2-entropy.csv`) is one of the 13 files the new skip counter reports. Fixing the skip *activates* the double-count. The two findings are coupled and neither is dangerous alone — do not fix one in isolation.
- [ ] **13 CSVs skipped on every load.** Twelve are per-model `{model}-entropy.csv` summaries, benign but previously invisible. The thirteenth is `gpt2-small/gpt2-entropy.csv`, which resolves to `domain='gpt2-entropy'`.
- [ ] **Entropy coverage gap.** Entropy covers 61 (model, domain) pairs against elicitation's 65. Missing: `pythia-1b` × {control, finance, legal, medical}. This localizes part of A16.
- [ ] **TransformerLens version drift.** DECISIONS pins 2.17.0; the local `mechinterp` env runs **2.18**, and results were regenerated on Colab under 2.18. Either pin back or ratify 2.18 with a byte-comparison against a frozen artifact (`src/tangent_byte_compare.py` exists for this). Currently undocumented drift.
- [ ] **Label the reference table** with what it validates (population, not scores) and its provenance commit `0f116a5`.

---

## Paper framing (current)

**"It's not attention and it's not frequency"** — two negatives braced by a positive.

- **I. The gap exists.** Fluent wrongness lives here, not in its own section. Entropy here. Perplexity status TBD.
- **II. It's not attention (or a circuit).** Binding experiments. A7's collapsed binding–accuracy correlation (gpt2 r=0.087, pythia r=-0.003, olmo r=0.115) is *evidence for this section*, not damage — a clean null across three families.
- **III. It's not corpus frequency alone.** All the frequency work.

**Only Section I depends on A6.** II and III are untouched by the source flag.

### Two-framing design (new, 2026-08-09)

Each evaluative concept gets two items testing the same violation, differing only in whether the answer position permits termination:

- **A — question.** Ends at `?`. The model may legitimately close the unit.
- **B — cloze.** Grammatically incomplete; terminating is not a licensed continuation.

Demonstrated at Pythia-2.8B: the question form (`What accessibility attribute is missing from this HTML: <img src='photo.jpg'>?`) produces `\n\n` and a fresh paragraph. The cloze form (`<img src='photo.jpg'> is missing the attribute`) produces `"alt"` — correct, first try, same model.

**Cloze is primary** for the headline gap number: it is the conservative choice, since  it gives the model its best shot. A gap surviving the friendliest framing is a stronger  claim than one measured under the format most likely to produce artifacts.

**This is also a within-concept test of the frequency hypothesis.** Corpus frequency is  a property of the concept — `alt` has the same Pile count regardless of framing. If  frequency were doing the explanatory work, framing should not move the outcome. It  does. That is Section III's argument arriving by a method orthogonal to the Spearman  correlations: frequency sets availability, framing determines reachability.

Note that four of the five original Experiment 2a items were *already* cloze, and they  still fail. That is the evidence against "the gap is entirely a prompt artifact."

### Logit lens (new, 2026-08-09)

Exploratory work in `~/Repos/Research/maybe-neurons/`. At Pythia-2.8B, tracking `" alt"` rank by layer at the final prompt position of the question-framed item:

- L15–16: top1 is `Answer` — the model enters an answering frame
- L18–19: top1 is `attribute`, `alt` reaches rank **21**
- L20–31: top1 becomes `\n`, `alt` falls away to **325**

Contrast with the declarative `skip link` item, which the model answers correctly: the target surfaces around L16–17 and *holds to the output* (rank 0 at L31).

Same mid-network emergence, opposite late-layer fate. This suggests the gap is in part  created in the final third of the network — retrieval succeeds and is then displaced by  a structural prior.

**Caveats before this becomes a claim:** the two traces differ in framing *and* in  declarative-vs-evaluative, so the contrast is confounded until matched pairs exist  (step 7). Rank 21 is a closest approach, not a retrieval. There is no null distribution  for what an unrelated token's rank trajectory looks like.

---

## Notes carried from discussion

- **Evaluative evidence is accessibility-only**, 5 items × 13 models. The domain batteries are cloze, which measures production under structural constraint and cannot test evaluative capability. Scope to this honestly. Extending to other domains is Paper 3, and the real cost is not the rerun — it is asserting ground truth in domains where the author is not the authority.
- **The floor claim needs uniformity, not sample size.** "Never, anywhere, across three families" is stronger at n=5 than "sometimes, on average" at n=50.
- **Not self-citing Paper 1.** Decided 2026-08-09. Note that Section II refutes Paper 1's headline claim (sustained late-layer binding as a necessary structural condition); without the citation there is no prior claim in play, and the paper states what the data shows once, correctly.
- **Screen reader may not take an evaluative form.** It is a tool, not a page property — every screen-reader violation is really another concept's violation. Likely joins WCAG and ARIA as a stated exclusion, leaving seven paired concepts.
- **The expansion was not the mistake.** The data layer verifies clean throughout: 227/227 compounds round-trip, all 65 binding CSVs match schema, manifests expected == written == actual everywhere. What broke is that the *analysis* layer did not expand with the data — code correct for the old scope that silently became wrong for the new one, without ever throwing. That is the normal cost of scope change, and it is why audits exist. The expansion is what caught the binding claim.
- **Audit trigger, for next time.** Not "audit more often" — that returns findings on work in progress. Audit *after the scope moves and the dust settles*. Every finding here clusters at one of four scope changes: compounds 11 → 53, layout flat → per-domain, suites two → three, batteries one → five domains. The cheaper version is making scope visible at load time, which step 1's skip counter starts.
