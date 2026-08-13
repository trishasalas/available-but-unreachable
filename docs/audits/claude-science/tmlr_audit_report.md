# TMLR repo audit — things the claims layer doesn't currently see

Scope: `results/`, `notebooks/`, `src/`, `paper/sections/`, `docs/findings/CLAIMS.md`, `DECISIONS.md`,
plus git history. Every number below was recomputed from the frozen CSVs on disk, not read from prose.

The claims discipline here is unusually good — 51 evidence pointers, pre-registered thresholds, a
documented retraction (A2), a self-caught measurement artifact (C6). The findings below are the
places where that discipline has a blind spot, not places where it is absent.

---

## BLOCKERS

### F1 — The completion-paradox sign test does not reproduce

`paper/sections/02-the-behavioral-gap.md` states it twice:

> "completion accuracy exceeds declarative accuracy at all ten suite-by-scale points (sign test, p ~ .001)"

Recomputed from `results/analysis/completion_paradox.csv`:

| level | strictly greater | p (one-sided sign test) |
|---|---|---|
| suite x scale (n=10) | **6 / 10** | 0.377 |
| concept x scale (n=40) | **10 / 40** | 0.9997 |

At the suite-scale level the ten points break down as **6 strictly greater, 3 exact ties**
(gpt2-1.5B 75=75, gpt2-774M 50=50, pythia-12B 75=75), **and 1 reversal** — pythia-6.9B, where
completion 50.0% falls below declarative 75.0%.

At the finer concept-scale level, two rows reverse, both on the same concept:

| suite | scale | concept | completion | declarative |
|---|---|---|---|---|
| pythia | 6.9B | captions | 0.0% | 50.0% |
| gpt2 | 774M | captions | 0.0% | 50.0% |

Note gpt2-774M is a concept-level reversal but an aggregate **tie** (its other concept, alt text,
offsets it) — the two levels must not be conflated.

The claim is only true as "completion >= declarative at 9 of 10 points" (ties included), which
is not a p ~ .001 result. B6's narrower exemplar — Pythia-160M alt text, completion 100% vs
declarative 0% — **does** verify exactly. The exemplar survives; the generalized sign test does not.
Note the battery is 4 concepts but only 2 (alt text, captions) have declarative counterparts, so
n is effectively 20 concept-scale pairs, not 40.

### F2 — The evidence for A4, A5 and D6 is not in the working tree

Commit `ca01b59` ("rearrange results directory structure", 2026-08-05) deleted 45 result files that
were never re-added. Among them, the four CSVs that A4/A5/D6 cite as NAILED:

- `pythia-2.8b-head-characterization.csv`
- `pythia-2.8b-collocation.csv`
- `pythia-2.8b-candidate-heads.csv`
- `pythia-2.8b-multihead-ablation.csv`

...plus all ten `*-binding.csv` (B1's replication evidence) and all `*-expansion-results.csv`
(B4's stated evidence path). `results/pythia/` now contains exactly one file, `pythia-160m-entropy.csv`.

They survive in git at `ca01b59^` and I have recovered them (`recovered_evidence.zip`). The claims
still verify against the recovered copies:

- max induction **0.0201** across the 8 characterized heads (bar >= 0.5) — A4 holds
- L1/H12 prev_token **0.8860** — A4 holds
- **5 of 6** heads with BOS values are >= 0.5 (range 0.549–0.912) — A4's "5/6 late-layer sinks" holds
- L29/H7 collocation on screen reader **0.9019**, next compound **0.2104** — A5 holds
- joint KL screen_reader n=2 **0.000022** vs bar 0.01 — D6 holds

One caveat worth logging: A4 says "max induction 0.0201". That is the max within the 8-row
*characterization* table. In `candidate-heads.csv` the max induction is **0.2449** (L17/H26 on
stock_market, a non-lexical-set head). Still an order of magnitude under the 0.5 bar, but the
claim should say which table it refers to.

**Action:** restore these four files (plus binding + expansion) to `results/pythia/`, or amend
every pointer. A reviewer running the repo as-is cannot verify A4, A5, D6 or B1.

---

## MAJOR

### F3 — OLMo 2 exists on disk but nowhere in the claims layer

The word "olmo" appears **0 times** in `CLAIMS.md`, **0 times** in `DECISIONS.md`, and **0 times**
in the body of all twelve paper sections. Yet the repo holds, for three OLMo-2 models:

- 92 elicitation prompts each (`results/frequency/olmo/*-results.csv`)
- full entropy tables (`results/entropy/olmo/*/`)
- completed Spearman merges + partial-correlation controls

The project brief names OLMo 2 as one of three studied families. Right now it is a fourth,
undeclared experiment. I ran the existing deterministic coder (`src/accuracy_coding.py`) over the
OLMo elicitation data — **276 rows, 0 uncoded** — and got results that matter:

| model | declarative % | evaluative % | gap (pts) | ρ freq | conf. penalty |
|---|---|---|---|---|---|
| OLMo-2-0425-1B | 61.1 | 40.0 | **+21.1** | 0.329 | +0.003 |
| OLMo-2-1124-7B | 66.7 | 50.0 | **+16.7** | 0.455 | −0.043 |
| OLMo-2-1124-13B | 55.6 | 70.0 | **−14.4** | 0.509 | −0.067 |

(matched to Pythia's concept set: 9 declarative, 5 evaluative concepts)

Two things fall out:

1. **The frequency finding (A3) replicates in a third family, on a third corpus.** OLMo-2-13B
   reaches ρ = 0.509 against Dolma/OLMo-Mix — nearly identical to Pythia's 0.5715 against the
   Pile. This is the strongest available answer to "is this a Pile artifact?" and it is
   currently sitting unused. This is the biggest thing being missed.
2. **The gap claim (A1) inverts at OLMo-2-13B.** Evaluative accuracy exceeds declarative by
   14.4 points. Pythia-12B "closes the gap by declarative regression"; OLMo-13B goes further and
   crosses. A1 as written ("the gap is real and persists across scale") does not survive contact
   with the third family. Either A1 needs a scope qualifier (two families, named), or the
   OLMo inversion becomes a finding in its own right.

Also: the confidence penalty (B5) goes **negative at two of the three** OLMo scales (7B −0.043,
13B −0.067), whereas B5 claims "no sign flip — non-negative at all 10 models." OLMo-1B is
+0.003 — effectively zero, but non-negative, so it is consistent with B5 as written. Adding OLMo
would therefore break B5's non-negativity at the two larger scales, in the same direction the
trend predicts.

Caveats on all of this: 5 evaluative concepts is thin, and see F9.

### F4 — Two contradictory Spearman ρ for the same OLMo model

- `results/olmo/OLMo-2-0425-1B_spearman_result.md` → **ρ = 0.4819**, p = 0.0005
- `results/frequency/olmo/OLMo-2-0425-1B_spearman_result.md` → **ρ = 0.3288**, p = 0.0211

Both reproduce exactly when recomputed from their own adjacent merged CSV, so neither is a typo.
The two `_spearman_merged.csv` files differ on `mean_accuracy` for **18 of 49** compounds
(e.g. `menu_bar` 1.0 vs 0.0; `responsive_design` 0.0 vs 1.0) — a coding or run difference, not
rounding. Only the `results/frequency/` copy records a revision
(`stage1-step990000-tokens2077B`). No DECISIONS entry adjudicates. Pick the canonical one and
delete or clearly quarantine the other before either number reaches a draft.

### F5 — `spearman_summary.csv` disagrees with every other frequency artifact

| source | Pythia | GPT-2 |
|---|---|---|
| `spearman_summary.csv` (bigram_spearman) | **0.5785** | **0.5021** |
| `spearman_partial.csv` (raw_rho) | 0.5715 | 0.5052 |
| `spearman_pmi_robustness.csv` (rawbigram) | 0.5715 | 0.5052 |
| CLAIMS A3 / paper §3 | 0.5715 | 0.5052 |

The summary file is the outlier — and it is the one whose name invites citation. Either it was
computed on a different row filter or it predates a coding change. Regenerate or annotate it.

### F6 — B4's regression count doesn't match B4's own definition

B4 defines the count as concepts that "regress from **correct/partial** at an intermediate scale
to incorrect at maximum scale" and inks 4 Pythia / 2 GPT-2 / 1 both.

Recomputed from `per_concept_trajectories.csv`:

| definition | Pythia | GPT-2 | both |
|---|---|---|---|
| peak >= partial (as written) | **7** | **6** | **4** |
| peak == correct (as inked) | 4 | 2 | 1 |

The inked numbers correspond to correct-only. The prose is what's wrong, not the count — but as
written a reader recomputing B4 gets 7/6/4 and concludes the claim is overstated. Note the
looser definition strengthens the claim ("not skip-link-specific" is the point), so it may be
worth reporting both.

Also worth noting: the "1 in both" concept is `accessible name`, not `skip link` — and the
established cross-architectural exemplar in the same row is skip link. Under correct-only,
skip link regresses in Pythia but not GPT-2.

---

## MODERATE

### F7 — Three "different" binding notebooks are the same file

`binding-gpt2.ipynb`, `binding-pythia.ipynb` and `binding-olmo.ipynb` are **byte-identical**
(sha256 `efc31e53...`). All three load `pythia-160m` only; the strings `gpt2` and `olmo` do not
appear in any of them. Same pattern: `frequency-gpt2.ipynb` and `frequency-pythia.ipynb` are
byte-identical (`c1890972...`) and both reference OLMo, GPT-2 and Pythia model ids.

The filenames promise per-family analyses that the notebooks don't contain. Either the
parameterization was never committed, or three copies were made as templates and never filled in.

### F8 — Stale duplicates with no canonical marker

- `results/olmo/` duplicates four files from `results/frequency/olmo/` with **differing** content
  (the `output` column differs on 91–92 of 92 rows — different generation runs, not a copy)
- `OLMo-2-0425-1B-results (1).csv` — a browser-download duplicate, differs from its sibling
- `results/frequency/pythia/pythia-{160m,410m}_skip_link_competition.csv` are byte-identical to
  their `results/mlp/pythia/` twins

### F9 — The OLMo scale series is confounded with training budget

| model | revision | tokens seen |
|---|---|---|
| OLMo-2-0425-1B | stage1-step990000 | 2077B |
| OLMo-2-1124-7B | stage1-step99000 | **416B** |
| OLMo-2-1124-13B | stage1-step99000 | **831B** |

Parameters rise 1B → 7B → 13B while tokens seen move **inversely** (2077B → 416B → 831B). Any
"OLMo scaling" statement mixes two variables. Notably ρ still rises monotonically with parameters
(0.33 → 0.45 → 0.51) *against* the token gradient, which arguably strengthens the frequency
reading — but it must be stated. Pythia and GPT-2 are clean here; OLMo is not. If final-revision
checkpoints are available, re-running the 7B/13B at matched steps would remove this.

---

## MINOR

### F10 — Nine documentation pointers resolve to nothing

`binding-reframe-draft.md`, `coding-criteria-draft.md`, `notebooks/lexical-head-l29h7.ipynb`,
`docs/superpowers/specs/2026-06-29-multihead-lexical-ablation-design.md`, `blind-study/`,
`data/all_prompts.yml`, `paper/sections/figures/`, plus two that merely moved:
`results/paper1-replication/` → `results/adhoc/gap-paper-replication/` and
`results/d8_frequency_prior/` → `results/adhoc/d8_frequency_prior/`.

CLAIMS.md's own rule is "a claim with an unverifiable Evidence pointer does not ship." A5 already
flags one of these ("reconcile path") — the other eight are unflagged.

### F11 — Appendix A.1 ships a placeholder

`paper/sections/11-appendix.md` contains
`<!-- TABLE PLACEHOLDER — populate from the head-audit results at promotion. -->`
The CSV that would populate it is one of the four deleted in F2.

---

## What verified cleanly

Worth recording, since most of this repo holds up:

- A1 gap series: `pythia_gap.csv` 15/20/20/20/20/0, `gpt2_gap.csv` 15/25/25/50 — exact
- A3 frequency: skip_link 662, screen_reader 32,100, alt_text 23,306 — exact
- A3 robustness battery (partial, PMI, Kendall, bootstrap, secondary) all present and internally consistent
- B2: ARIA incorrect at all 10 models, declarative 0.0 everywhere — exact. ARIA is also
  incorrect at all three OLMo scales, so B2 extends to 13 models
- B3: stability audit **20/102** stable — exact
- B5: penalty series 0.97/0.63/0.64/0.29/0.07/0.32 and 0.68/0.56/0.13/0.07 — exact
- B6 exemplar: Pythia-160M alt text completion 100.0 / declarative 0.0 — exact
- B7: GPT-2 Pearson 0.448, Pythia 0.116, Spearman −0.117, n_pairs 32/48 — exact
- D7/C6: gate CSVs, `d7_summary.md` and `REGEN_DIVERGENCE.md` all present and mutually consistent;
  the 18/18 regeneration match is real
- D1 verdict, D8 six-scale b_U tables — present and consistent

---

## Suggested order of work

1. **F2** — restore the deleted evidence (unzip `recovered_evidence.zip` into `results/pythia/`
   and `results/elicitation/`). Nothing else can be verified by a reviewer until this is done.
2. **F1** — re-derive or retract the sign test in §2. This is the only place where paper prose
   asserts something the frozen data contradicts.
3. **F3** — decide whether OLMo 2 is in or out. If in, it is a genuine third-corpus replication
   of A3 and it forces a scope revision of A1 and B5. If out, say so in Limitations and move
   `results/*/olmo` to an archive directory.
4. **F5, F4, F6** — one canonical number each; a DECISIONS entry for each adjudication.
5. **F7–F11** — hygiene.
