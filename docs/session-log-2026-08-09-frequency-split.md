# Session log — frequency notebook split (2026-08-09)

Record of what was found, not a summary of what was done. Task brief:
`docs/task-frequency-notebook-split.md`. Audit: `docs/claude-science/tmlr_audit_2026-08-09.md`.

Commits, in order:

| commit | what |
|---|---|
| `d9baae7` | repair spreadsheet damage to frozen `frequency_table.csv` |
| `0395202` | split notebooks per suite; one corpus per suite, one writer per file |
| `27ee289` | regenerate frequency battery per suite; OLMo included for the first time |

---

## 1. What landed

**Three notebooks** — `frequency-{pythia,gpt2,olmo}.ipynb`, 16 cells each, matching
the `elicitation-*.ipynb` pattern. Each names its Infini-gram index as a literal in
cell 2 and prints it. No `SUITE_INDEX` dict, no lookup, no loop over suites. The
mechanism is in cells: scope derivation, the query loop, the `-1` sentinel screen,
conditional probability, PMI, the write.

Two deliberate departures from the reference pattern:

- No model-loading or memory-cleanup cells — nothing loads, frequency needs no GPU.
- The correlation is **called, not implemented**. Cell 15 calls
  `dual_spearman.run_suite`. Three notebooks each computing their own Spearman is
  how the number carrying Section III ended up in three places.

Counts are reused, not re-queried (`REQUERY = False`). Re-querying moves `x` and
every Section III number with it; that is its own decision. pythia/gpt2 reuse the
frozen Pile table — which also closes A22's index-caching item, since one query set
serves both. olmo reuses the OLMo-Mix counts from `ebb4d2b`.

**`src/frequency.py` reduced to plumbing** — compound inventory, the Infini-gram
call with its retry/backoff, per-suite table I/O with schema validation and
`corpus_index` stamping.

Removed, all with zero external consumers:

| removed | why |
|---|---|
| `build_frequency_table` | mechanism; now inline in the notebooks |
| `frequency_accuracy_correlation` | duplicate estimator; `dual_spearman` is canonical |
| `run_frequency_analysis` | wrote both colliding global filenames |
| `save_frequency_results` | unused, stale output path |

**`query_infinigram`'s `index` is now required.** It previously defaulted to
`PILE_INDEX`. A default is exactly how a robustness path silently gets Pile counts
for OLMo; without one, forgetting it raises a `TypeError` at the call site. This is
a structural guard, not a check that has to be remembered.

**`spearman_summary.csv` now has one writer.** `dual_spearman.run` is the only
writer of all six output files. The name was deliberately **not** changed: CLAIMS A3
(`NAILED`) already cites `spearman_summary.csv` for the primary rho, so keeping the
name and removing the second writer restores that claim's pointer to truth with no
documentation churn.

**`dual_spearman` reads per-suite tables.** `build_compound_table(project_root, suite)`
loads `results/frequency/{suite}/{suite}_frequency_table.csv`, so each suite's `x`
comes from its own corpus. Every output row carries `corpus_index`. Compounds with
no elicitation rows are counted and named rather than silently skipped. p-values are
no longer rounded to 4dp (A22) — a true `p = 1.8e-05` had been shipping as `0.0`.

**Depends on:** per-suite tables existing at
`results/frequency/{suite}/{suite}_frequency_table.csv`. A suite without one is
reported and skipped, never computed against another corpus's counts.

---

## 2. Pass conditions

| # | Condition | Result |
|---|---|---|
| 1 | Row counts | 49 queried / 49 returned / **0 screened as −1**, all three suites |
| 2 | Pythia rho | **0.5875** — matches the brief's ≈0.587 anchor |
| 3 | OLMo corpus | every statistic `v4_olmo-mix-1124_llama`, recorded in each file |
| 4 | Corpus column | present in all 9 outputs |
| 5 | p-values | `9.084344091588645e-06`, not `0.0` |

```
suite   corpus_index             rho      p          n    Kendall tau-b
pythia  v4_piletrain_llama       0.5875   9.08e-06   49   0.4490
gpt2    v4_piletrain_llama       0.5194   1.31e-04   49   0.4108
olmo    v4_olmo-mix-1124_llama   0.5823   1.14e-05   49   0.4610
```

Partial correlations:

```
pythia  compound_token_count 0.5807   word1_unigram_count 0.6059
gpt2    compound_token_count 0.5092   word1_unigram_count 0.4988
olmo    compound_token_count 0.5810   word1_unigram_count 0.5969
```

**Independent confirmation of pass condition 3.** OLMo's corpus-matched
ρ = 0.5823 and τ = 0.4610 reproduce the audit's hand-computed A4 figures exactly.
The Pile-contaminated τ = 0.4490 that A4 reported for OLMo is gone.

---

## 3. Why the paper's numbers were stale — ruling: **re-ink**

The paper cites Pythia ρ = 0.5715 and GPT-2 ρ = 0.5052
(`paper/sections/03-frequency-predicts-failure-structure.md:11,13`). The pipeline
now produces 0.5875 and 0.5194.

`x` is **provably identical**: max |Δx| = 8.9e-16 against the frozen table. The
entire difference is **one compound** — `closed_captions`, `y_all` 0.0 → 0.1667,
with the same 6 rows in both. That single compound moves Pythia's rho by 0.016.

Cause: `compound_accuracy_table.csv` was built at `ca0319e` (2026-07-03), when
`results/elicitation/pythia/pythia-2.8b/` **did not exist**. The results layout moved
flat → per-domain afterwards (36 files added) and `load_all_results` changed twice
(`3e60191` 2026-08-08, `aa7e1bb` 2026-08-09). The 2.8B row that now codes `correct`
lives in `pythia-2.8b-accessibility.csv`, a file that postdates the table.

**A hypothesis was raised and discarded.** The first suspicion was the three-spellings
trap — `accuracy_coding.py:295` documents `'closed captions'` as control-only, and
the declarative data uses exactly that spelling. Tested directly: `code_response`
returns identical codes for `'captions'` and `'closed captions'` on all 6 rows
(`y_all = 0.166667` either way). The spelling is **not** implicated. Recording this
so the hypothesis is not re-run.

**Ruling (Trisha, 2026-08-09): re-ink, not a vintage decision.** 0.5715 was computed
against a table missing a scale's elicitation data. That is an incomplete input, not
an alternative coding, so there is no choice to make. The numbers are
**0.5875 / 0.5194 / 0.5823**. Section III needs re-inking to match.

---

## 4. The `rowlevel_bootstrap` bug — A4's mechanism in an unaudited function

The most important finding of the session.

```python
# before
freq_x = tab.drop_duplicates('compound').set_index('compound')['x_log10_bigram']
rows = []
for suite in sorted(tab['suite'].unique()):
    s = elic[elic['suite'] == suite].copy()
    s['x'] = s['compound'].map(freq_x)
```

`freq_x` was built **once, outside the suite loop**, from a table-wide
`drop_duplicates('compound')`. Since suites were iterated in sorted order, whichever
suite sorted first (`gpt2`) supplied the `x` vector for **every** suite. Each suite's
own x-values were computed, written into `tab`, and then discarded.

This is exactly the defect A4 describes — robustness statistics silently using
another corpus's x — living in a function the audit never named, because the audit
reached A4 through `compound_accuracy_table.csv` and stopped there. Nothing failed:
the bootstrap produced plausible rho values and a plausible CI for every suite.

Fixed by moving the `freq_x` construction inside the loop and building it from that
suite's rows only.

**Depends on:** `tab` carrying one `corpus_index` per suite. If a future change ever
merges two corpora into one suite's rows, `load_suite_frequency_table` raises rather
than letting the ambiguity through.

---

## 5. OLMo self-resolved

OLMo previously had **zero** rows in `compound_accuracy_table.csv`, and therefore
zero rows in primary, Kendall, partial, secondary/sensitivity and bootstrap.
`SCALE_ORDERS` did include `olmo`, so `build_compound_table` hit `if sub.empty:
continue` 49 times and wrote nothing. No output file recorded the absence.

This was scoped as separate work and was not attempted. It resolved as a
consequence: once OLMo had a per-suite frequency table, `build_compound_table` found
all **49 compounds with elicitation rows, 0 skipped**. OLMo is now present in every
statistic, with `corpus_index = v4_olmo-mix-1124_llama` on every row.

The skip is now visible either way — `build_compound_table` prints the counted and
skipped compounds by name, and warns explicitly when a suite yields no rows at all.

---

## 6. The restore demonstration — one filename, one writer, made concrete

The audit's A1 recommended `git checkout` to restore `frequency_table.csv` and
`spearman_summary.csv` after a last-suite-wins clobber. That restore had already been
applied before this session started, which is why the audit's disk description no
longer matched reality.

It restored the **wrong estimator**. `spearman_summary.csv` had two writers —
`frequency.py`'s naive correlation and `dual_spearman`'s pre-registered primary — so
`git checkout` restored whichever writer wrote it at that commit. The file came back
holding `frequency.py`'s schema (`suite,metric,r,p,n`) with ρ = 0.5785 / 0.5021,
while CLAIMS A3 cites that same filename for ρ = 0.5715 / 0.5052.

**With two writers on one path, even the repair picks a winner arbitrarily.** One
filename, one writer is not tidiness; it is what makes a restore meaningful.

---

## 7. Still open

**Two contradictory OLMo-1B runs.** `results/olmo/OLMo-2-0425-1B_spearman_result.md`
gives ρ = 0.4819; `results/frequency/olmo/OLMo-2-0425-1B_spearman_result.md` gives
ρ = 0.3288. The corpus columns are **byte-identical** (49/49 compounds, same
bigram/word1/word2 counts) and both name `v4_olmo-mix-1124_llama`. The divergence is
entirely in `mean_accuracy`, which differs on **18/49** compounds. The newer file
records `Revision: stage1-step990000-tokens2077B` and `dtype torch.float32`; the
older records no revision. The raw elicitation CSVs confirm it — the same prompt
under greedy decoding returns *"a software program that reads aloud the text on a
computer screen"* in one and *"a device that is used to access the internet"* in the
other. **This is checkpoint pinning, not corpora.** Unadjudicated.

**Duplicate OLMo trees.** `results/olmo/` and `results/frequency/olmo/` hold
overlapping artifacts, including a browser-download duplicate
`OLMo-2-0425-1B-results (1).csv` (218 lines vs 176 for the non-`(1)` file). Neither
tree has a producer in the repo — both arrived via `ebb4d2b`, *"update olmo files and
results after colab run"*. The code that made them exists only in a Colab session.

**`spearman_accuracy.csv` has no writer anywhere in the repo.** Carries ρ = 0.5289
for pythia and is the only file using the suite label `olmo2-1b` and the corpus name
`dolma` — neither string appears anywhere in `src/`, `notebooks/`, or `paper/`.
A19 recommends archiving it. Still on disk.

**`accuracy_coding.py:295` documents a condition that has reversed.** The comment
states the declarative captions data uses concept `'captions'` and that
`'closed captions'` appears "only as control", describing the alias below it as a
defensive no-op closing a DANGEROUS CELL. The data now has 6 declarative
`'closed captions'` rows and zero `'captions'` rows, so the defensive branch is the
live path. Harmless today — both branches code identically, verified — but the
comment is false and the file is under the "any change requires a DECISIONS entry"
rule, so this is flagged, not touched.

**`CLAUDE.md`'s trap note misattributes that rename.** It states *"`closed captions`,
not `captions`. Renamed in `7f84365`."* `7f84365` (2026-08-08) does not touch
captions at all — it is *"add missing compounds + make suite iteration dynamic"*,
the commit that took `COMPOUNDS` from 49 to 53 and replaced the hardcoded
`['pythia', 'gpt2']` loop in `dual_spearman` with `tab['suite'].unique()`. The
rename actually happened in **`ca01b59`** (2026-08-05, *"rearrange results directory
structure"*), which is the same commit that moved the results layout. Verified with
`git log -S` on `data/accessibility.yaml` in both directions. The trap itself is
real and the guidance is correct; only the commit pointer is wrong. Worth fixing in
`CLAUDE.md` — a record naming a specific commit that does something else is the
documented failure mode operating on the file that documents the failure mode.

**`docs/decisions/0012-olmo-frequency-corpus.md` describes the wrong problem.** It is
written as a corpus-selection decision. The evidence says the OLMo discrepancy is
checkpoint pinning (see above). It needs rewriting as a checkpoint-pinning decision;
per the immutability rule, supersede rather than edit.

**No `python3` kernelspec is registered in the `mechinterp` env,** so the notebooks
ship without cell outputs. The only registered kernel is `olmo`, pointing at a
different env (`/opt/homebrew/Caskroom/miniconda/base/envs/olmo/bin/python`).
Verification this session ran the cell sources in-process via IPython's
`TransformerManager` — same interpreter, real numbers, but no stored outputs.
Registering a kernelspec writes to `~/Library/Jupyter/` and was not done unasked.

---

## 8. The 53 vs 49 arithmetic

`src.frequency.COMPOUNDS` holds **53** entries. The frequency analysis uses **49**.

The four extras — `empty_link`, `form_label`, `link_text`, `page_title` — are all
`accessibility` domain but have **no declarative prompt**, so they have no accuracy
to correlate against. They appear in the battery only under other prompt types.

They were added in `7f84365` (2026-08-08) to make `frequency.py` match the binding
YAML inventory at 227/227 — a legitimate change for binding, which silently widened
the frequency inventory past what the frequency analysis can use. The same commit
made `dual_spearman`'s suite iteration dynamic, which is what allowed OLMo to begin
flowing through the loop and then be silently dropped by the `if sub.empty: continue`
described in §5.

The paper's stated arithmetic is exactly right: 51 declarative concepts − 2
single-token concepts (ARIA, WCAG, which have no bigram) = 49. Verified — the
battery-derived set and the frozen table's compound set are identical, with zero
difference in either direction.

The notebooks now **derive** this set from `data/accessibility.yaml` rather than
hardcoding it or taking `COMPOUNDS` wholesale, print the three counts, and assert
`len(compounds) == 49` with a message saying that a change here is a scope change
that moves `n` and every Section III number with it.

**Depends on:** `data/accessibility.yaml` remaining the source of the declarative
battery. If the battery grows, the assertion fires and the count changes visibly —
rather than the scope moving underneath correct code, which is how compounds went
11 → 53, results flat → per-domain, suites two → three, and batteries one → five
without anything failing.

---

## Verification notes

- The frozen `frequency_table.csv` was repaired by restoring the exact `dd141cb`
  (2026-07-02) bytes, not by re-serializing. Spreadsheet damage introduced in
  `af6074f`: 150 blank rows, 12 phantom columns, force-quoting, CRLF, and small
  floats reformatted (`6.3e-05` → `6.30E-05`). All 49 compounds verified numerically
  identical across all seven data columns before and after. A first attempt that
  rewrote the file from parsed strings preserved the spreadsheet's float formatting;
  restoring from git was strictly better and is what shipped.
- The frozen table was confirmed **unchanged** after the full pipeline run — nothing
  writes it any more.
- A sibling `results/frequency/frequency_table.README.md` records the freeze date,
  the index, the incident, and the invariants consumers depend on.
