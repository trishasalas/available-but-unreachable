# Audit response plan — 2026-08-08

Working plan against `docs/tmlr_audit_2026-08-09.md` (audit run at `6786d13`).

**Scope decision:** paper prose findings are **out of scope** for this pass. The old
prose is knowingly stale and is being rewritten under the new framing (see
"Paper framing" below). Findings A5, A13, and most of A14 are therefore deferred,
not fixed.

**State as of writing:** working tree clean apart from `results/frequency/frequency_table.csv`
(SpreadJS mangling — quoting, CRLF, phantom trailing columns). Local is 2 commits
ahead of origin. The frozen Pile table is intact (`screen_reader = 32100`); it was
never clobbered in committed history.

---

## Phase 0 — Make the tree safe

- [ ] `git add` the untracked `results/_archive/*.csv` files. Five files, currently
      backed up by nothing. Two of them (`completion_paradox.csv`,
      `trajectory_stability_audit.csv`) are cited evidence for claims marked NAILED
      (finding A10). Tracked-and-maybe-wrong beats untracked-and-gone.
- [ ] `git checkout -- results/frequency/frequency_table.csv`
- [ ] Verify: `wc -l` → 50 (49 rows + header); `head -1` → unquoted, no trailing commas
- [ ] Set VS Code `workbench.editorAssociations` so `*.csv` opens in the plain text
      editor by default. SpreadJS rewrites the entire file on save, including columns
      never touched.
- [ ] Optional: `.gitattributes` entry marking `results/**/*.csv` as `text eol=lf`

## Phase 1 — Fix the loader (`src/analysis.py`)

This is the file everything downstream reads. All four issues live here.

- [ ] **A6 — the source flag.** `load_all_results` hardcodes `df['source'] = 'original'`
      on every row, unguarded. Confirmed: elicitation CSVs have no `source` column, so
      the filter in `gap_analysis.py:76-78` has never filtered anything. It has been
      decorative since the per-domain reorg.

      *Interim fix:* hardcode the 10 original concepts as a set in `analysis.py` and
      derive `source` from membership. Not elegant, but true and auditable at a glance.

      *Watch out:* commit `7f84365` renamed `captions` → `closed captions`. The
      membership set must account for this or it silently drops to 9 concepts.

      *Durable fix (defer to Phase 4):* add a `source` field to `data/binding/*.yaml`
      and propagate through the battery writers.

- [ ] **gpt2 double-count.** `_extract_scale` maps both `'gpt2'` and `'gpt2-small'` to
      124M, and per finding A16 both directories exist. Nothing dedupes. Every
      gpt2-small row is counted twice in any groupby over scale — and if the two dirs
      hold pre- and post-rerun data, old and new are being averaged together.

- [ ] **Silent skips.** `_extract_domain` strips `model_name + '-'` from the stem;
      anything not in `KNOWN_DOMAINS` is `continue`d with no warning. A file in a
      directory whose name doesn't prefix it vanishes without trace. Add a skip counter
      to the load printout.

- [ ] **Concept key normalization.** Three spellings of one concept currently exist
      across batteries: `closed_captions` (frequency), `closed captions` (declarative),
      `captions` (completion). Normalize at load time — one function, applied
      everywhere. This is the real fix for A3; the rename didn't break the join, it
      exposed a normalization that was never there.

- [ ] **Stale compound lists.** `tokenization_comparison` hardcodes 11 compounds across
      its `clean`/`split` lists. The battery is 53 compounds now; the other 42 all land
      in an `'unknown'` bucket. Refresh or retire.

**Known good in this file, per audit:** `_extract_scale` handles the OLMo case correctly
(`'olmo'` ends in `'m'`, `float('olm')` raises, loop continues), and the `pythia-13b`
alias is handled. `binding_summary` and `max_binding_layer` are straightforward.

## Phase 2 — Re-derive the gap tables

- [ ] Re-derive with the source flag actually working.
- [ ] **Pair the comparison.** Restrict declarative to the concepts that have evaluative
      counterparts. The current tables compare a 51-concept declarative mean against a
      5-concept evaluative mean — two incomparable populations.
- [ ] Confirm the negative gap at Pythia-6.9B disappears.

      *Prediction on record:* it will. The gap stays positive at all scale points,
      probably widens overall, and the monotonic declarative rise (35.3 → 55.9) stays
      because that part is real. 6.9B is the strongest evaluative performer but still
      has the gap. If the negative *survives* the fix, stop and look at the 6.9B
      declarative responses directly.

- [ ] Once positive everywhere: the sentence worth having is
      "gap positive at all 6 Pythia scales, all 4 GPT-2 scales, all 3 OLMo models."
      Uniformity is what carries the floor claim.

## Phase 3 — Decisions before any rerun

See `docs/decisions-pending.md`. These get silently undone or entrenched by the next
pipeline run, so they come first.

- [ ] OLMo x-corpus (A4)
- [ ] Archival question (A11)
- [ ] `pythia-13b` / `pythia-12b` naming (A15)

## Phase 4 — Frequency pipeline

- [ ] **A1 — per-suite filenames.** `run_frequency_analysis()` writes
      `frequency_table.csv` and `spearman_summary.csv` with fixed names; the notebook
      loops it over suites, so each pass overwrites the last. Note that
      `{suite}_frequency_accuracy.csv` files *are* already per-suite — the fix is
      narrower than it first appears.
- [ ] Add a corpus/index column so provenance is recoverable from the file itself.
- [ ] **A18 — latent bugs.** Infini-gram's `-1` failure sentinel flows into Spearman as
      a real value (screen `count < 0` to NaN before writing). `cond_prob == 0.0`
      becomes `None` via a truthiness check (use `is not None`). Partial-correlation
      controls are dropped from the per-suite path.
- [ ] **A22.** p-values round to 4dp so a true p≈1e-6 ships as `0.0`. Format
      scientifically. Also: pythia and gpt2 map to the same Pile index and re-run the
      full query loop for each — cache per index.
- [ ] Regenerate the battery once, cleanly.

## Phase 5 — The completion paradox (A3)

- [ ] With key normalization in place, re-run the completion/declarative join.
- [ ] Check what the paradox does with all four concepts back. Currently alt-text-only:
      7 greater / 6 ties / 0 less, p=0.0078 — significant *through a broken join*.
- [ ] Fix `paper/generate-figures/generate-fig-completion-paradox.py:51`, which reads
      the archived path and can no longer run.
- [ ] **Free win worth checking:** grep the domain batteries (legal/medical/finance) for
      any concept with both a cloze item and a declarative item. If the completion
      paradox extends beyond accessibility, that's a substantially bigger result than
      the accessibility-only version.

## Phase 6 — Housekeeping (nothing here blocks the science)

- [ ] A10 — re-home evidence for NAILED claims A4/A5/D6 out of `results/_archive`
- [ ] A7 / A8 — update CLAIMS B7 and B4 against regenerated data
- [ ] A16 — entropy battery gaps (pythia-1b has 1 of 5 domains, no new-style manifest;
      gpt2-small duplicates the rerun gpt2 dir; 13 legacy schema-drifted CSVs)
- [ ] A17 — OLMo provenance: 1B commit-sha files sitting in the 7B elicitation dir
- [ ] A19 — archive superseded frequency-era artifacts (four different "pythia primary
      rho" values currently on disk)
- [ ] A20 — delete dead `src/` modules, orphan `.pyc`, `data/backup.py`.
      **Do not delete** top-level `data/*.yaml` (elicitation/entropy prompt files, key
      `prompts`) — a different artifact from `data/binding/*.yaml` (key `compounds`).
      **Keep** `dual_spearman.py`, `closeout_followups.py`, `d6/d7/d8_*.py`.
- [ ] A21 — ~14 dangling doc pointers; two DECISIONS entries both labeled D7;
      appendix table placeholder

---

## Paper framing (current)

**"It's not attention and it's not frequency"** — two negatives braced by a positive.

- **I. The gap exists.** Fluent wrongness lives here (not its own section). Entropy
  here. Perplexity status TBD.
- **II. It's not attention (or a circuit).** Binding experiments. A7's collapsed
  binding–accuracy correlation (gpt2 r=0.087, pythia r=-0.003, olmo r=0.115) is
  *evidence for this section*, not damage — a clean null across three families.
- **III. It's not corpus frequency alone.** All the frequency work.

**Only Section I depends on A6.** II and III are untouched by the source flag.

### Notes carried from discussion

- **Evaluative evidence is accessibility-only**, 5 items × 13 models. The domain
  batteries are cloze, which measures production under structural constraint — it
  cannot test evaluative capability. Scope to this honestly rather than reframing
  around it. Five evaluative items per domain is Paper 3, and the real cost isn't the
  rerun, it's asserting ground truth in domains where the author isn't the authority.
- **The floor claim doesn't need many items, it needs uniformity.** "Never, anywhere,
  across three families" is stronger at n=5 than "sometimes, on average" at n=50.
- **Self-citation of Paper 1** is a judgment call either way, but note that Section II
  refutes Paper 1's headline claim (sustained late-layer binding as a necessary
  structural condition). Cited in third person it reads as self-correction, which is a
  strength. Omitted, it risks looking like a quiet walk-back.
- **The expansion wasn't the mistake.** The data layer verifies clean throughout —
  227/227 compounds round-trip, all 65 binding CSVs match schema, manifests
  expected == written == actual everywhere. What broke is that the *analysis* layer
  didn't expand with the data: code that was correct for the old scope and silently
  became wrong for the new one, without ever throwing. That's the normal cost of scope
  change, and it's why audits exist. The expansion is what caught the binding claim.
