# Task brief — split `frequency-analysis.ipynb` to match the convention

> Paste into Claude Code. Written 2026-08-09.
> Related: audit findings A1, A4, A18, A22; decision `docs/decisions/0012-olmo-frequency-corpus.md`.
> Plan: `docs/audit-response-plan.md` — this is the whole "accuracy line" for Section III.

---

## Read first

- `notebooks/frequency-analysis.ipynb` — the notebook being split
- `notebooks/elicitation-pythia.ipynb` and `notebooks/elicitation-olmo.ipynb` — **the
  reference pattern.** Read both. The target is for the new frequency notebooks to look
  like these.
- `src/frequency.py` — the module being reduced
- `docs/frequency-refactor.md` — the 2026-08-05 brief that produced the current
  structure. Useful context for what was deliberate.
- `docs/decisions/0012-olmo-frequency-corpus.md`

## The problem

`frequency-analysis.ipynb` is the only task notebook that has not been split by suite.
Every other task follows `{task}-{suite}.ipynb`:

```
elicitation-pythia.ipynb   entropy-pythia.ipynb   binding-pythia.ipynb
elicitation-gpt2.ipynb     entropy-gpt2.ipynb     binding-gpt2.ipynb
elicitation-olmo.ipynb     entropy-olmo.ipynb     binding-olmo.ipynb
```

Frequency instead loops over all three suites inside one notebook. That single
structural difference is the direct cause of three separate audit findings:

- **A1** — `run_frequency_analysis()` writes `frequency_table.csv` and
  `spearman_summary.csv` with fixed filenames. Inside a loop over suites, each pass
  overwrites the last. Whichever suite ran last is what is on disk.
- **A4** — the corpus index is indirected through a `SUITE_INDEX` dict. The primary
  correlation path consults it correctly; the robustness paths (partial correlation,
  Kendall, bootstrap) do not, and use Pile x-values for OLMo. Four contradictory
  OLMo-1B rho values currently exist on disk.
- **A18** — the mechanism that would have made these visible is buried in
  `src/frequency.py` instead of being in readable cells.

The second structural difference is over-abstraction. In every other notebook the
*mechanism* — what was actually computed — lives in cells you can read, and only
plumbing is imported from `src/`. Frequency inverted that. A cell reading
`run_frequency_analysis(suite)` records that something happened, not what.

## Target

Three notebooks, matching the convention exactly:

```
notebooks/frequency-pythia.ipynb
notebooks/frequency-gpt2.ipynb
notebooks/frequency-olmo.ipynb
```

Each one:

1. **Names its own infini-gram index at the top, as a literal.** No `SUITE_INDEX` dict,
   no lookup. `frequency-pythia` and `frequency-gpt2` use `v4_piletrain_llama`;
   `frequency-olmo` uses `v4_olmo-mix-1124_llama`. The index must be visible in the
   first cells, so a robustness path cannot silently use a different one — that is
   exactly how A4 happened.
2. **No loop over suites.** One notebook, one suite. This retires A1 without needing
   per-suite filenames: outputs go to `results/frequency/{suite}/` following whatever
   the current per-suite files already do (`{suite}_frequency_accuracy.csv` etc.).
3. **Mechanism in cells.** The infini-gram query, count extraction, sentinel handling,
   PMI / conditional-probability computation, and the Spearman call are all *what
   happened* and belong in readable cells. Match how `elicitation-pythia.ipynb`
   structures this — read it rather than inventing a layout.
4. **Plumbing stays imported.** File I/O, manifest writing, retry logic, schema
   validation stay in `src/frequency.py`.

The test for where a line belongs: **if a reviewer asked "how did you compute this,"
would you point at the notebook or open a module?** Anything requiring a module to
answer should be in the notebook.

## Fix while moving

Read the code as you move it. These three are in the path and are the reason Section
III's numbers are currently untrustworthy:

- **The `-1` sentinel.** Infini-gram returns `-1` to signal a failed lookup. It
  currently flows into the Spearman calculation as though it were a real count. Screen
  `count < 0` to NaN before it reaches any statistic, and **report how many rows were
  screened** — a silent drop here is the same failure class as everything else in this
  repo.
- **`cond_prob == 0.0` becoming `None`.** A truthiness check (`if cond_prob:`) treats a
  legitimate zero as missing. Use `is not None`.
- **Partial-correlation controls dropped from the per-suite path.** Verify the controls
  are applied on every path, not just the primary.

Also, while in there:

- **A22 — p-value formatting.** Values round to 4dp, so a true p≈1e-6 ships as `0.0`.
  Format scientifically.
- **A22 — index caching.** `pythia` and `gpt2` both map to `v4_piletrain_llama` and
  currently re-run the full query loop each. With separate notebooks this is now a
  question of whether the second notebook can reuse the first's cached counts. If that
  is not straightforward, leave it and note it — correctness first.

## Pass conditions

Run and report all of these. **Do not adjust code to make a number match — report the
mismatch instead.**

1. **Row counts.** Each notebook covers the full compound battery for its suite. Report
   compounds queried, compounds returned, and rows screened as `-1`.
2. **Pythia rho.** The current on-disk pythia value is unreliable because of A1's
   clobbering, so this is a sanity check rather than an oracle: recomputed pythia rho
   should land near the previously reported ρ≈0.587 (n=49, p<0.001). A large divergence
   means stop and report, not adjust.
3. **OLMo corpus.** Confirm every OLMo statistic — primary, partial, Kendall, bootstrap
   — used `v4_olmo-mix-1124_llama`. State this explicitly in the output.
4. **Corpus column.** Every output file carries a column naming the index used, so
   provenance is recoverable from the artifact rather than from the notebook that
   produced it.
5. **p-values** print in scientific notation, not as `0.0`.

## Constraints

- **Do not delete `frequency-analysis.ipynb`.** Move it to `_Archive/_notebooks/` when
  the three replacements verify. Deletion is the only irreversible action here.
- **Do not touch** `src/accuracy_coding.py`. Any change there requires its own DECISIONS
  entry and retroactively changes every table and figure.
- **Do not touch** `src/analysis.py`. Decision 0015's `concept_raw` work is a separate
  changeset.
- **Do not regenerate** anything under `results/` until the three notebooks are written
  and reviewed. Write first, run second, and say before running.
- Work inline. No subagents, no worktrees under `.claude/`.

## Report

1. The three notebooks, and how they differ from `elicitation-*.ipynb` if at all.
2. What stayed in `src/frequency.py` and why.
3. The pass-condition numbers, including screened-row counts.
4. Anything found while reading the code that is not in this brief. The last two briefs
   both surfaced a real bug that way, and it was more valuable than the assigned work.
