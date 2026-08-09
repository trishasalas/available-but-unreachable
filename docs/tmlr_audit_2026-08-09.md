# TMLR repo audit — 2026-08-09

Scope: `~/Repos/Research/tmlr` at commit `6786d13` (dirty working tree), excluding `_archive`, `.claude/`, archives and caches. Three parallel audit tracks (code, data, claims/paper); every number below was recomputed from files on disk (or `git show` for before/after comparison), never read from prose. Per instruction, the earlier audit document was disregarded; all findings are stated on their own evidence.

## Summary

This week's reruns are **internally excellent at the raw-data layer**: all 13 binding model trees (row counts, YAML compound sets, 12-column schema, manifests expected==written==actual), all 13 elicitation manifests, and all new-style entropy manifests verify exactly; the manifest per-battery-writers migration, the binding notebook migration (227/227 compounds round-trip), and the frequency.py refactor were all implemented as specified. The problems are concentrated in two places: **(1) the frequency pipeline's fixed output filenames**, which let the suite loop destroy two canonical artifacts in the working tree, and **(2) the prose layer** — paper sections and CLAIMS.md still carry pre-regeneration numbers almost everywhere, and several no longer reproduce even directionally.

| ID  | Severity | Area                 | Finding                                                                                                                                                                                               |
| --- | -------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1  | BLOCKER  | frequency pipeline   | Frozen Pile frequency table and primary Spearman summary clobbered by last-suite-wins overwrite                                                                                                       |
| A4  | MAJOR    | frequency pipeline   | OLMo robustness battery mixes corpora: partial/Kendall/bootstrap use Pile x-values while the primary uses Dolma; four contradictory OLMo-1B rhos on disk                                              |
| A6  | MAJOR    | analysis code        | Documented exclusion of the 41 expansion compounds from the gap tables is a silent no-op                                                                                                              |
| A7  | MAJOR    | claims vs data       | CLAIMS B7 binding–accuracy correlation is destroyed by the regenerated 49-compound data but still marked NAILED                                                                                       |
| A8  | MAJOR    | claims vs data       | 'Never-emerges' concept list and B4 regression counts no longer reproduce after the closed-captions re-coding                                                                                         |
| A10 | MAJOR    | claims integrity     | Evidence for NAILED claims A4/A5/D6 (and B4's expansion CSVs) exists only in results/_archive; CLAIMS' own gate says such claims do not ship                                                          |
| A11 | MODERATE | pipeline hygiene     | The five tables just archived out of results/analysis are still written by the pipeline, read by a figure script, and cited by findings docs                                                          |
| A12 | MODERATE | working tree hygiene | Three regenerated analysis CSVs are spreadsheet-mangled in the working tree                                                                                                                           |
| A15 | MODERATE | naming/consistency   | Binding battery names the largest Pythia checkpoint 'pythia-13b'; elicitation/entropy call the same checkpoint 'pythia-12b'                                                                           |
| A16 | MODERATE | results completeness | Entropy battery gaps: pythia-1b has 1 of 5 domains and no new-style manifest; gpt2-small duplicates the rerun gpt2 dir; 13 legacy schema-drifted CSVs coexist                                         |
| A17 | MODERATE | provenance           | OLMo provenance is misfiled and incomplete: 1B commit-sha files inside the 7B elicitation dir; no binding or elicitation manifest records a checkpoint revision                                       |
| A18 | MODERATE | code robustness      | Latent frequency-pipeline bugs: Infini-gram failure sentinel (-1) would flow into Spearman as a real value; cond_prob==0.0 becomes None; partial-correlation controls dropped from the per-suite path |
| A19 | MINOR    | stale artifacts      | Superseded frequency-era artifacts leave four different 'pythia primary rho' values on disk                                                                                                           |
| A20 | MINOR    | src hygiene          | Obsolete src/ modules (precise list) plus stale **pycache** and a redundant data/backup.py                                                                                                            |
| A21 | MINOR    | docs integrity       | ~14 documentation pointers in CLAIMS.md/DECISIONS.md resolve to nothing; DECISIONS has two entries labeled D7; appendix table placeholder still unpopulated                                           |
| A22 | MINOR    | presentation         | p-values print as 0.0 in spearman_summary; pythia and gpt2 redundantly re-query the identical Pile index                                                                                              |

## BLOCKERS

### A1 — Frozen Pile frequency table and primary Spearman summary clobbered by last-suite-wins overwrite

run_frequency_analysis() writes results/frequency/frequency_table.csv and spearman_summary.csv with fixed filenames; frequency-analysis.ipynb loops it over suites (pythia → gpt2 → olmo), so each pass overwrites the last. After this week's run, frequency_table.csv holds OLMo-Mix/Dolma counts (53 rows; screen_reader = 987,882) instead of the frozen Pile counts (49 rows; screen_reader = 32,100 — survives only at git HEAD), and spearman_summary.csv contains ONLY the 3 olmo rows (0.5823 / 0.5757 / -0.0073) — the pythia and gpt2 primary rows written by dual_spearman at 17:20 were destroyed at 17:31. dual_spearman.py and closeout_followups.py read frequency_table.csv as 'the FROZEN frequency table'; any rerun now silently correlates pythia/gpt2 accuracy against Dolma counts. The file carries no corpus/index column, so provenance is unrecoverable from the file itself.

**Evidence:** Disk frequency_table.csv screen_reader=987882 (matches olmo_frequency_accuracy.csv on all rows); git show HEAD: 49 rows, screen_reader=32100; log10(32100)=4.5065 == compound_accuracy_table x_log10_bigram in all three suites. spearman_summary.csv = 3 olmo-only rows, mtime 17:31; sibling dual_spearman outputs mtime 17:20 with all suites. src/frequency.py fixed paths; src/dual_spearman.py:311 writes the same spearman_summary.csv path as PRIMARY.

**Suggested fix:** Restore both files from HEAD (git checkout -- results/frequency/frequency_table.csv results/frequency/spearman_summary.csv), then give run_frequency_analysis per-suite filenames (e.g. {suite}_frequency_table.csv / {suite}_spearman_summary.csv) and add a corpus/index column.

## MAJORS

### A5 — Every statistic in paper §3 is stale against the regenerated frequency battery

§3 inks Pythia ρ=0.5715 / GPT-2 ρ=0.5052 with partials 0.5913/0.4857 (word1) and 0.5603/0.4896 (token count). The regenerated battery consistently gives Pythia 0.5875 / GPT-2 0.5194 (recomputed independently from three artifacts), partials word1 0.6059/0.4988, token count 0.5807/0.5092. The pre-registered ρ≥0.4 threshold still clears, so the conclusion survives — but every number needs re-inking, and the estimand changed (trajectory ordinal → mean accuracy per docs/frequency-refactor.md) without the paper saying so. CLAIMS A3 carries the same stale values.

**Evidence:** Recomputed spearman(log10 bigram, mean_accuracy) from pythia/gpt2_frequency_accuracy.csv = 0.5875 / 0.5194 (n=49), matching spearman_partial.raw_rho and compound_accuracy_table. Old values now exist only in stale spearman_pmi_robustness.csv (mtime 07-04) and git HEAD.

**Suggested fix:** Re-ink §3 and CLAIMS A3 from the current artifacts and state the mean-accuracy estimand explicitly.

### A6 — Documented exclusion of the 41 expansion compounds from the gap tables is a silent no-op

gap_analysis.py:76-78 filters source=='original' with a comment saying the frequency-stratified expansion compounds must NOT be pooled into the declarative/evaluative paradigm means. But analysis.py:66 hardcodes source='original' for every loaded row, and in the new per-domain layout the expansion compounds share the same CSVs as the original 10. The filter keeps everything: declarative pivots and gap scores are computed over 51 concepts, and the headline gap compares a 51-concept declarative mean against a 5-concept evaluative mean. This directly shapes the gap tables that A2's paper rewrite would be based on.

**Evidence:** elicitation_coded.csv source value_counts == {'original': 3458}. Pythia declarative pivot: 51 concepts. Recomputed pythia-160M declarative over all 51 = 0.7059 == pythia_gap.csv; restricted to the 10 original concepts = 0.5.

**Suggested fix:** Propagate a real source flag in load_all_results (e.g. from a compound→source map) or drop the dead filter and re-derive the gap tables deliberately; then re-check A2.

### A7 — CLAIMS B7 binding–accuracy correlation is destroyed by the regenerated 49-compound data but still marked NAILED

B7 inks 'GPT-2 Pearson r = 0.448; Pythia r = 0.116' on 8 compounds (n_pairs 32/48). Current binding_accuracy_corr.csv: gpt2 r=0.087 (n=196), pythia r=-0.003 (Spearman -0.126, n=294), olmo r=0.115 (n=147). The architecture-dependence contrast collapses to ~zero everywhere. B7 feeds A4's 'correlate' framing and paper §4; paper/figures/binding-vs-accuracy.png is Jun 27 vintage (old data).

**Evidence:** results/analysis/binding_accuracy_corr.csv rows recomputed exactly from binding_vs_accuracy.csv (637 rows, 49 compounds/suite, all three families present).

**Suggested fix:** Downgrade/retract B7, update §4 and the figure, or adjudicate why the 8-compound subset was the right test.

### A8 — 'Never-emerges' concept list and B4 regression counts no longer reproduce after the closed-captions re-coding

§3 (echoed in §2): 'ARIA, captions, and semantic HTML never arrive across ten models and two model-families'. Current per_concept_trajectories.csv codes closed captions CORRECT at Pythia 2.8B (peak_regress) and CORRECT at GPT-2 1.5B (monotonic_climb) — captions now emerges in both families. B4's inked counts (4 Pythia / 2 GPT-2 / 1 both strict) recompute to 5 / 2 / 1 (closed captions joins the Pythia regressors); by peak_regress label 8 / 4 / 1. GPT-2 skip link is now labeled never_emerges (0/1/1/0), weakening the §3 'degrades at maximum scale in both families' exemplar.

**Evidence:** per_concept_trajectories.csv rows for closed captions and skip link; elicitation_coded.csv confirms gpt2 closed captions declarative correct at 1.5B, pythia at 2.8B. Recomputed strict pythia regressor set = {accessible name, closed captions, keyboard navigation, reading order, skip link}.

**Suggested fix:** Re-derive the never-emerges list and B4 counts from the current table; update §2/§3 and CLAIMS B4.

### A10 — Evidence for NAILED claims A4/A5/D6 (and B4's expansion CSVs) exists only in results/_archive; CLAIMS' own gate says such claims do not ship

CLAIMS A4/A5/D6 cite results/pythia/pythia-2.8b-{head-characterization,collocation,candidate-heads,multihead-ablation}.csv and notebooks/lexical-head-l29h7.ipynb; DECISIONS D6/D8 name the same outputs. results/pythia/ does not exist; the four CSVs live only in results/_archive/ and the notebook is gone entirely (binding-lexical-head.ipynb may be its successor, but nothing says so). B4's *-expansion-results.csv paths also resolve only to _archive. D7's sealed d7_step5_ranks_preban.csv exists only inside .claude/worktrees/, not under results/logits/.

**Evidence:** find results -name 'pythia-2.8b-*' → _archive only; notebooks/lexical-head-l29h7.ipynb absent; find -name '*preban*' → .claude/worktrees/... only. CLAIMS.md: 'A claim with an unverifiable Evidence pointer does not ship.'

**Suggested fix:** Un-archive (or re-home) the evidence CSVs to a canonical results/ path and update every pointer; copy the preban CSV into results/logits/.

## MODERATES

### A11 — The five tables just archived out of results/analysis are still written by the pipeline, read by a figure script, and cited by findings docs

completion_paradox, emergence_thresholds, criteria_strictness_audit(_full), trajectory_stability_audit were deleted from results/analysis (moved untracked to _archive). But gap_analysis.py still emits completion_paradox and emergence_thresholds (saved by analysis.ipynb's save_tables), dual_spearman.py writes criteria_strictness_audit + trajectory_stability_audit, closeout_followups writes the _full variant, generate-fig-completion-paradox.py reads one, and results-significance.md + CLAIMS B3/B6 cite them. The next pipeline run silently undoes the archival — it has already cycled once (archived copies carry post-archival regeneration mtimes).

**Evidence:** git status 5 D + 5 ?? pairs; gap_analysis.py:139,210; dual_spearman.py:315-316; generate-fig-completion-paradox.py:51; results-significance.md:70,201,304.

**Suggested fix:** Pick one: retire the writers (and update the citing docs/claims), or keep the tables canonical and revert the archival.

### A12 — Three regenerated analysis CSVs are spreadsheet-mangled in the working tree

accuracy_by_prompt_type.csv, binding_accuracy_corr.csv, binding_vs_accuracy.csv (mtime 18:17, uncommitted) were re-saved by a spreadsheet app after the 14:10 pipeline run: every field quoted, CRLF, padded to 20 columns with 12-16 empty trailing columns, and blank-row padding to a ~200-row grid (binding_accuracy_corr.csv is 199 lines for a 3-row table). Numeric content is identical to HEAD (verified cell-by-cell, max diff 0.0), but pandas now returns 'Unnamed' columns and NaN rows, ints parse as floats, and the git diff is pure noise.

**Evidence:** head of binding_accuracy_corr.csv shows quoted empty-column padding; wc -l 199 vs 4 at HEAD; merged current-vs-HEAD on keys: all shared values identical.

**Suggested fix:** git checkout -- the three files (or re-run save_tables); avoid saving from the spreadsheet app.

### A15 — Binding battery names the largest Pythia checkpoint 'pythia-13b'; elicitation/entropy call the same checkpoint 'pythia-12b'

results/binding/pythia/pythia-13b/ (directory, filenames, manifest 'Model name: pythia-13b', CSV model column) uses a name that does not exist in the Pythia suite; the manifest's own parameter count (11845.4M) identifies pythia-12b. Cross-battery joins survive only because analysis.py hardcodes a special case mapping pythia-13b → scale 12e9 and joins on (suite, scale, compound), never on model. Any model-column join, per-model listing, or paper model table will treat them as different models. docs/directory-structure.md inks the pythia-13b path.

**Evidence:** pythia-13b-binding.md 'Params: 11845.4M'; CSV model column ['pythia-13b']; analysis.py:118-119.

**Suggested fix:** Rename the directory/files/manifest/model column to pythia-12b and drop the analysis.py special case.

### A16 — Entropy battery gaps: pythia-1b has 1 of 5 domains and no new-style manifest; gpt2-small duplicates the rerun gpt2 dir; 13 legacy schema-drifted CSVs coexist

results/entropy/pythia/pythia-1b/ has only the accessibility domain from the new run (plus a legacy 92-row entropy.csv and a legacy stub .md); every other model has all 5 domains with expected==written==actual manifests. results/entropy/gpt2/gpt2-small/ holds only legacy files for the same 124M checkpoint whose complete new run lives in results/entropy/gpt2/gpt2/. The 13 legacy *-entropy.csv files lack the 'domain' column; analysis.py skips them only because 'entropy' fails domain extraction — a load-bearing accident, undocumented.

**Evidence:** Directory listings; per-domain pivot shows NaN for pythia-1b control/finance/legal/medical; schema scan: 2 distinct column tuples, domain-less one exactly in the 13 legacy files.

**Suggested fix:** Run the 4 missing pythia-1b domains (or document the gap); delete/archive gpt2-small and the legacy CSVs, or add an explicit skip rule.

### A17 — OLMo provenance is misfiled and incomplete: 1B commit-sha files inside the 7B elicitation dir; no binding or elicitation manifest records a checkpoint revision

results/elicitation/olmo/OLMo-2-1124-7B/ contains OLMo-2-0425-1B-commit-sha.md and commit-sha-OLMo-2-0425-1B.md (both recording the 1B pin, stage1-step1907359) plus a truncated commit-sha-OLMo-2-1124-7B.md with no Revision/SHA lines. The CSVs themselves are clean (model column verified). Meanwhile none of the three binding or three elicitation OLMo manifests contains a Revision line — although manifest.py supports revision= and the entropy manifests record it — so the binding runs' checkpoints are recorded nowhere. For a revision-pinned scale series this is essential provenance. (The notebooks are now fixed; the stale files predate the fix and the batteries have not been re-run.)

**Evidence:** File contents printed; grep -i revision: 0 hits in binding/elicitation manifests, 2 each in entropy manifests. OLMo-2-0425-1B/ also carries a redundant legacy .md.

**Suggested fix:** Delete the misfiled/truncated sidecar files; backfill Revision into the six manifests from the notebook pins (or re-emit manifests).

### A18 — Latent frequency-pipeline bugs: Infini-gram failure sentinel (-1) would flow into Spearman as a real value; cond_prob==0.0 becomes None; partial-correlation controls dropped from the per-suite path

query_infinigram returns count=-1 after exhausted retries; build_frequency_table does not screen it — a -1 would produce a negative conditional probability and enter the Spearman ranking as the minimum rank (dropna doesn't catch it). 'round(cond_prob,6) if cond_prob else None' maps a legitimate 0.0 to None. Latent this run (0 negatives on disk; the notebook log shows 4 consecutive rate-limit waits — one more 403 would have written -1). Also, frequency_accuracy_correlation computes only raw Spearmans but its docstring calls word1_spearman a 'partial-correlation control', and the refactor spec's 'keep partial correlations for constituent frequency and tokenization length' is implemented only in dual_spearman, not in the per-suite path. Separately, run_binding_sweep's default arg is a guaranteed crash (unpacks five domain-name strings as 4-tuples) and its suite inference would file OLMo under results/gpt2/ — dead code advertised by the module docstring.

**Evidence:** frequency.py:625-650, 693-716, 745-768; notebook stdout rate-limit lines; binding.py:340-379 + docstring line 8 (importers verified: only find_token_index/run_single_compound are consumed).

**Suggested fix:** Screen count<0 to NaN before writing; use 'is not None' for the cond_prob guard; fix or delete run_binding_sweep and its docstring advertisement.

## MINOR

### A19 — Superseded frequency-era artifacts leave four different 'pythia primary rho' values on disk

results/frequency/ simultaneously offers pythia rho = 0.5289 (spearman_accuracy.csv, 07-29, only file using suite label 'olmo2-1b'), 0.5715 (spearman_pmi_robustness.csv, 07-04 — the value the paper still cites), 0.5785 (git-HEAD summary) and 0.5875 (current battery), plus the demoted trajectory-era merges (gpt2/pythia_frequency_trajectory.csv) the refactor doc said to archive. Each stale file is one confused citation away from a wrong number.

**Evidence:** mtimes and values read from each file.

**Suggested fix:** Archive spearman_accuracy.csv, the trajectory CSVs, and (after re-inking §3) regenerate or retire spearman_pmi_robustness.csv.

### A20 — Obsolete src/ modules (precise list) plus stale **pycache** and a redundant data/backup.py

Dead code with zero live consumers, superseded: elicitation.py and entropy.py (load nonexistent data/all_prompts.yml; entropy.py writes the pre-reorg layout and can't route OLMo), decompose.py, heads.py, logit_lens.py, perplexity.py, probe.py + models.py (probe is models' only importer), viz.py, tangent_byte_compare.py, logit_export.py. KEEP despite zero imports: dual_spearman.py and closeout_followups.py (run-as-script entry points; dual_spearman actively regenerated this week's battery), d6_multihead_ablation.py / d7_token_ban.py / d8_frequency_prior.py (cited as evidence in CLAIMS/DECISIONS — reproducibility). Stale bytecode: **pycache**/tl2_olmo2_adapter.cpython-311.pyc has no matching .py (renamed to tl217_olmo2_adapter). data/backup.py duplicates four src/binding.py arrays byte-identically — redundant now that data/binding/*.yaml is canonical. NOT duplicates: top-level data/*.yaml are the elicitation/entropy PROMPT files (key 'prompts'), a different artifact from data/binding/*.yaml (key 'compounds') — do not delete.

**Evidence:** Import graph over all main-tree notebooks + src cross-imports + paper scripts; ast comparison backup.py vs binding.py (44/44/42/44 tuple-identical); pycache stem diff.

**Suggested fix:** Delete the dead modules (git history preserves them), the orphan .pyc, and data/backup.py; add a comment to dual_spearman/closeout_followups noting they are **main** entry points.

### A21 — ~14 documentation pointers in CLAIMS.md/DECISIONS.md resolve to nothing; DECISIONS has two entries labeled D7; appendix table placeholder still unpopulated

Unresolvable in the canonical tree: binding-reframe-draft.md, coding-criteria-draft.md, lexical-head-l29h7.ipynb, 2026-06-29-multihead-lexical-ablation-design.md, results/paper1-replication/, blind-study/, data/all_prompts.yml, results/lexical-head-results.md (actually at docs/findings/), results/pythia/*-entropy.csv, expansion-results paths, completion_paradox.csv and trajectory_stability_audit.csv (deleted this week while B3/B6 and §3/§9 still cite their results), notebooks/mlp.ipynb, D6/D8 output CSVs. '## D7 — Binding battery consolidated across domains (2026-08-08)' collides with the pre-existing '## D7 — Single-token-ban counterfactual' (CLAIMS A2/C6/D7 mean the token-ban one). paper/sections/11-appendix.md still carries the '' whose source CSV is archived (see A10).

**Evidence:** Existence test on every backtick path in both docs (28 tested, 14 unresolvable); grep '^## ' DECISIONS.md lines 7 and 156.

**Suggested fix:** Renumber the new DECISIONS entry (e.g. D9), fix or annotate each dangling pointer, populate or remove the appendix placeholder.

### A22 — p-values print as 0.0 in spearman_summary; pythia and gpt2 redundantly re-query the identical Pile index

frequency_accuracy_correlation rounds p to 4 decimals, so a true p≈1e-6 ships as '0.0' — reviewer bait. The notebook's SUITE_INDEX maps pythia and gpt2 to the same v4_piletrain_llama index and re-runs the full Infini-gram query loop for each (verified byte-identical counts, 49/49), doubling runtime and API load for no information.

**Evidence:** spearman_summary.csv 'olmo,bigram_spearman,0.5823,0.0'; frequency.py:768; 0/49 count mismatches between the pythia and gpt2 merge files.

**Suggested fix:** Format p scientifically; cache per index.

## Verified clean (checked, no finding)

- **Manifest migration** complete per the 2026-08-08 spec: `_write_manifest` + three per-battery writers with the planned signatures; `create_manifest_file` gone from every main-tree `.py`/`.ipynb`; all 9 battery notebooks call the correct writer exactly once.
- **elicitation-gpt2.ipynb** now writes to `results/elicitation/gpt2/...`; no misfiled gpt2 dirs remain under `pythia/`. **elicitation-olmo.ipynb** no longer hardcodes 13B provenance; commit-sha is computed inline against the real `model_name` and folded into the manifest.
- **Binding migration**: `data/binding/*.yaml` round-trips tuple-for-tuple against `src/binding.py` (44/53/42/44/44 = 227); `binding-gpt2/pythia/olmo.ipynb` are distinct, family-correct, and emit the exact planned 12-column order; all 65 binding CSVs match schema and compound sets; manifests expected==written==actual everywhere.
- **Regenerated frequency battery is internally consistent** (given its corpus choices): per-family rho recompute exactly (pythia 0.5875, gpt2 0.5194, olmo-vs-Dolma 0.5823, n=49); the 49-compound denominator is correct (4 of 53 compounds have no declarative rows by design); Kendall/partial/bootstrap/secondary tables all reproduce to 4 dp; the closed-captions accuracy edits in the working tree were independently recomputed and the NEW values are correct.
- **binding_accuracy_corr reproduces exactly** from binding_vs_accuracy (all three families present); `analysis.py` scale handling correct for OLMo and for the pythia-13b alias.
- No empty files under `results/` (excluding `_archive`); no model-column contamination in any elicitation CSV; commit 7f84365's four added compounds match the binding YAML word pairs exactly.

## Suggested triage order

1. `git checkout --` the five clobbered/mangled CSVs (A1, A12) — one command, stops the bleeding.
2. Fix `run_frequency_analysis` output naming + corpus column (A1), decide the OLMo x-corpus (A4), regenerate the battery once, cleanly.
3. Decide the archival question (A11) and the pythia-13b rename (A15) before any pipeline rerun, since both get silently undone/entrenched by the next run.
4. Then the prose pass: §2 (A2, A3), §3 (A5), §4 (A14), §5 (A13), CLAIMS B4/B7/A3 (A7, A8), OLMo scoping (A9), evidence re-homing (A10).
