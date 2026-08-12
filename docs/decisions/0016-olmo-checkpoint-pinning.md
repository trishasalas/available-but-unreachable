# 0016 — OLMo checkpoint pinning

- **Status:** accepted
- **Date:** 2026-08-11
- **Supersedes:** [0012](0012-olmo-frequency-corpus.md), which described the problem incorrectly
- **Audit finding:** A4, restated

## Context

0012 was written as a corpus decision: it claimed OLMo's robustness statistics used Pile x-values while the primary used Dolma, and that four contradictory OLMo-1B rho values existed because of corpus mixing.

**That diagnosis was wrong.** Established 2026-08-09 during the frequency notebook split:

- `SUITE_INDEX` had always mapped OLMo to `v4_olmo-mix-1124_llama` correctly. The corpus was never mixed at the index level.
- The corpus columns in both contradictory OLMo-1B result sets are **byte-identical**. The divergence is entirely in `mean_accuracy`, on 18 of 49 rows.
- The real defect was in `rowlevel_bootstrap`, which built its x-vector via `tab.drop_duplicates('compound')` **across all suites**, so whichever suite sorted first supplied x for every other suite. Fixed in the same pass.

What remained after that was a genuine reproducibility gap, of a different kind. Two OLMo-1B result sets existed with different accuracy codings. One recorded `Revision: stage1-step990000-tokens2077B`; the other recorded no revision at all. Raw elicitation confirmed different generations for the same prompt under greedy decoding. Neither revision matched any deliberate choice — the checkpoint was whatever HuggingFace served at the time of the run.

A model without a pinned revision is not a reproducible input.

## Decision

Pin every OLMo model to an explicit revision, recorded as constants in
`src/olmo_config.py` and imported by every OLMo notebook:

```python
OLMO_REVISIONS = {
    "OLMo-2-0425-1B":  "stage1-step1907359-tokens4001B",
    "OLMo-2-1124-7B":  "stage1-step928646-tokens3896B",
    "OLMo-2-1124-13B": "stage1-step596057-tokens5001B",
}
```

Each is the final stage-1 checkpoint for its model, derived by taking the
highest `step` among `stage1` branches rather than transcribed by hand.

The elicitation manifest records the revision twice — once from the model config
and once from the HuggingFace resolve, alongside the commit SHA. Provenance is
recoverable from the artifact, not from memory of how a run was launched.

Rather than adjudicating between the two existing 1B result sets, **all three OLMo
models were rerun** at the pinned revisions.

## Verification — 2026-08-11

The rerun produced **byte-identical elicitation output**. `git diff` on
`results/elicitation/olmo/` shows no change to any CSV; only the manifests differ,
and only because they now carry revision fields the old ones lacked.

Downstream, everything reproduces exactly:

| | value |
|---|---|
| Primary ρ (all rows) | **0.5823**, p = 1.1e-05, n = 49 |
| Kendall τ-b | 0.4610, p = 2.7e-05 |
| Partial ρ (compound token count) | 0.5810 |
| Partial ρ (word1 unigram count) | 0.5969 |
| a11y sense only | ρ = 0.0804, p = 0.776, n = 15 |
| Corpus index | `v4_olmo-mix-1124_llama` |
| Compounds | 49 in table, 49 with elicitation rows, 0 skipped |
| Sentinels screened | 0 |

Run metadata: 2026-08-12T00:03 UTC, commit `2c2e926`, A100-SXM4-80GB,
`do_sample=False`, TransformerLens 2.18.0, torch 2.11.0+cu128. Manifest
reconciles expected == written on all five domains, 266 rows, 5/5 complete.

**Interpretation.** The checkpoint difference does not affect these prompts. Had it
been the cause of the 0.4819 / 0.3288 divergence, repinning would have moved
something. It moved nothing. The OLMo numbers are stable under repinning, and the
question 0012 was written to resolve is closed — not by choosing a winner, but by
establishing that the choice does not matter for this battery.

**What remains unexplained**, and is deliberately left so: the origin of the
0.4819 / 0.3288 difference. It is not the corpus and not the checkpoint. It most
likely originates in how one of those older runs was produced — both predate the
manifest carrying a revision, and one of them arrived via commit `ebb4d2b`
("update olmo files and results after colab run") from a Colab session whose code
exists nowhere in this repo. Both are superseded by pinned runs, so the question is
academic. Recorded here so nobody re-opens it expecting a live problem.

## Consequences

OLMo results are reproducible from the artifact alone. A future rerun that produces
different numbers indicates a real change rather than an unpinned checkpoint, which
is the property that was missing.

The frequency battery gains a stability result it did not have: the primary ρ is
invariant across at least two OLMo-1B checkpoints. That is worth a sentence in
Section III's robustness discussion — not as a headline, but because "we pinned the
checkpoint and the number did not move" is a stronger statement than "we pinned the
checkpoint."

Harder: `OLMO_REVISIONS` is a hand-maintained constant that must track any future
model addition. The commented derivation helper in `olmo_config.py` mitigates this
but does not enforce it.

**Depends on:** every OLMo notebook importing `OLMO_REVISIONS` rather than passing a
revision inline, and on `from_pretrained` actually honoring the revision argument
for each model. Both verified 2026-08-11 via the manifest's HuggingFace commit SHA,
which resolves to the pinned branch rather than to `main`.

**Who else reads this:** `src/olmo_config.py` is imported by the OLMo elicitation,
entropy, binding, and frequency notebooks. A change to a revision constant
invalidates every OLMo result downstream and requires a full rerun of that model,
not a partial one.
