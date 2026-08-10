# `frequency_table.csv` — frozen Pile frequency table

**Do not open this file in a spreadsheet editor.** See the incident below.

## What it is

Infini-gram corpus counts for the 49 accessibility compounds, queried once and
then frozen. It is the `x` side of every Section III correlation: consumers take
`log10(bigram_count)` as the independent variable.

| | |
|---|---|
| Corpus index | `v4_piletrain_llama` (Pile-train, Llama-2 tokenizer, 380B tokens) |
| Rows | 49 (all `domain == accessibility`) |
| Frozen | 2026-07-02, commit `dd141cb` |
| Columns | `compound, domain, word1, word2, bigram_count, word1_count, word2_count, conditional_prob` |

`conditional_prob` is `bigram_count / word1_count`.

## Why it is frozen

The numbers the paper reports reproduce from this file exactly:

```
pythia  rho = 0.5715  p = 1.798e-05  n = 49
gpt2    rho = 0.5052  p = 2.137e-04  n = 49
```

Re-querying Infini-gram would change the counts and move both. Regeneration is
therefore a decision with its own ADR, not a maintenance action.

## The 2026-08-09 spreadsheet incident

Between 2026-07-02 (`dd141cb`) and 2026-08-09 (`af6074f`) this file was opened
and saved in a spreadsheet editor. The saved file carried:

- 150 entirely blank rows appended after the 49 real ones
- 12 phantom empty columns (header widened from 8 fields to 20)
- every field force-quoted
- CRLF line endings throughout
- small floats textually reformatted (`6.3e-05` → `6.30E-05`)

**No value changed.** All 49 compounds were verified numerically identical
across all seven data columns. Pandas absorbed the damage silently — blank rows
became NaN, `Unnamed:` columns were ignored — so nothing failed and no statistic
moved. That silence is the reason this note exists.

Repaired 2026-08-09 by restoring the exact `dd141cb` bytes. Verified after
restore: 49 rows, 8 columns, 0 CRLF, and both rho values above reproduce with
`max |Δx| = 8.9e-16`.

## Depends on

- **This file is `v4_piletrain_llama` only.** It is valid as `x` for Pythia
  (Pile is the training corpus, confirmatory) and GPT-2 (replication under
  proxy). It is **not** valid for OLMo-2, whose corpus is OLMo-Mix-1124. OLMo
  counts live in per-suite tables under `results/frequency/olmo/` and must never
  be sourced from here.
- **Consumers assume 49 accessibility rows.** A row count other than 49 means
  something rewrote this file; stop and check git rather than proceeding.
- **`bigram_count` must be positive.** Consumers call `log10` on it directly, so
  a `-1` Infini-gram failure sentinel or a `0` raises rather than corrupting
  silently. Do not "fix" that by coercing to NaN upstream of the freeze.
