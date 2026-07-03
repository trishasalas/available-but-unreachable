# CLAIMS.md — Canonical claims inventory (TMLR paper)

> **Status: DRAFT** — first pass drafted 2026-07-01 by Claude (Fable 5, claude.ai)
> from: DECISIONS.md, docs/findings/*, blind-study STAGE2_SCORING.md +
> runs/stage2/SCORES_TRISHA.md + runs/stage2/NOTES.md. Trisha reviews every row.
>
> **Purpose:** one row per claim the paper makes (or deliberately declines to
> make). Every section draft pulls from here; blind-study-2 targets are drawn
> from here; a claim with an unverifiable Evidence pointer does not ship.
>
> **Status codes:**
> - `NAILED` — claim matches artifact; pointer verified on disk
> - `NEEDS-POINTER` — claim is right but the evidence path needs verification (⚠️ = Claude has not opened the artifact, pointer taken from DECISIONS/findings docs)
> - `OPEN` — experiment or check still pending
> - `FALSIFIED` — documented negative result (these ship too, as negatives)
> - `PRELIM` — real signal, not yet claim-strength; paper mentions with hedge or omits
> - `OUT` — out of scope for this paper (logged for the series)
>
> **Blind column:** status against the blind study (Stage 1 + Stage 2 verdicts,
> per pre-registered thresholds). `S2-target` = candidate recovery target for
> the scoped (TMLR-directory) blind study 2.

---

## A. Core mechanism claims (the paper's spine)

| # | Claim | Evidence | Blind | Paper home | Status |
|---|-------|----------|-------|-----------|--------|
| A1 | The declarative–evaluative gap is real, persists across scale in Pythia (all scales except 12B, which closes via declarative regression), and **widens** with scale in GPT-2 (50 pt at 1.5B) | `results/analysis/` gap tables via deterministic coding (`src/accuracy_coding.py`, `src/gap_analysis.py`); DECISIONS 2026-06-28 (gap analysis framework) | **M3 recovered 2/3** (S8 "declarative-procedural-normative gap"; S9 "knowing-vs-doing") | Results (Exp 1) + Discussion | NEEDS-POINTER ⚠️ (CSVs not opened) |
| A2 | **Token competition is the proximate mechanism** of skip_link inverse scaling: at generation Step 5, "displayed" (correct) is rank 1 at 6.9B and rank 4 at 12B, where it loses to higher-frequency "click" (rank 1). Knowledge is present and outcompeted, not absent | `results/mlp_investigation/` (6 models × 5 CSVs incl. `skip_link_steps`); DECISIONS 2026-06-28 (MLP investigation) | **M1 universal partial (1/1/1)** at Stage 2 — registered shape now directly demonstrated. **Prime S2-target** | Results + Section 05 | NEEDS-POINTER ⚠️ |
| A3 | **Frequency is the distal cause**: corpus token-frequency imbalance gates which continuation wins (skip_link 662 vs screen_reader 32,100 Infini-gram bigram occurrences) | `src/frequency.py` (compound inventory, Infini-gram wrapper, Spearman trajectory correlation); `results/frequency/` | **M2 recovered 2/3** (S8 independently pulled corpus counts; S9 §4F) | Section 05 (first-class) | NEEDS-POINTER ⚠️ (module + results dir exist; contents not opened this session) |
| A4 | **Binding is a correlate, not a mechanism.** Top binding heads are not induction heads (max induction 0.0201 vs ≥0.5 bar, correctly-derived heads); dominant binder L1/H12 is a previous-token head (0.886) scoring high by positional adjacency; 5/6 late-layer top binders are BOS attention sinks (0.55–0.91 mass on BOS); L27/H24 is a position-1 head (0.98 → 0.006 under uniform template) | `results/pythia/pythia-2.8b-head-characterization.csv`, `results/pythia/pythia-2.8b-collocation.csv`; `docs/findings/head-characterization-findings.md`; paste-ready prose in `docs/findings/binding-reframe-draft.md` | **N1 refined**: analysts' "generic mechanism, not knowledge" confirmed in spirit; induction hypothesis **falsified** on right heads | New Results subsection ("What the Late-Binding Heads Are") + Discussion + Limitations | NAILED (findings docs read; CSVs listed in findings doc) |
| A5 | **L29/H7: representation without function.** Genuinely selective QK lock on "screen reader" (reader→screen 0.90; next compound 0.21; weight-level QK ≈ 0 ⇒ built through the layers) — yet causally inert: zero-ablation at `reader` position, KL = 1e-05; control (bicycle wheel) KL = 0.0; OV writes a wrong-sense "screen" direction (fire/shooter/photographers), functionally dead | `notebooks/lexical-head-l29h7.ipynb`; `src/qk_ov.py`; `docs/findings/The one genuine lexical head.md`; `results/lexical-head-results.md` (note: findings doc says results/, file currently at docs/findings/lexical-head-results.md — reconcile path) | Not a registered target; single-head echo of thatDangCircuit population null | Results (same subsection as A4) — the closing exhibit | NAILED, two optional rigor items OPEN (mean-ablation vs zero; effect at final position) |
| A6 | The three levels compose into one causal story: **distribution (A3) → distributed/redundant representation (A4, thatDangCircuit) → decision-point competition (A2)**. Attention binding *marks* emergence; it does not *implement* it | Synthesis of A2–A5; hinge sentence drafted in `binding-reframe-draft.md` Edit 3 | M2+M3 both recovered = pre-registered mechanism criterion **met** (STAGE2_SCORING.md) | Discussion (thesis paragraph) + Abstract | OPEN (prose exists; integration not done — abstract/title still assert old thesis, see G1) |

## B. Behavioral / emergence claims (Paper 1 lineage, re-run on TL2)

| # | Claim | Evidence | Blind | Paper home | Status |
|---|-------|----------|-------|-----------|--------|
| B1 | 2.8B threshold for most accessibility concepts (Pythia); binding replication confirms Paper 1 on 5/6 models (deepest-strong-layer Δ ≤ 1); GPT-2 main table replicates exactly (12/12 zero deltas) | DECISIONS 2026-06-21 (two replication entries, incl. 410M outlier explanation + "Deepest Strong Layer" relabel) | Stage 1 lineage (R1 partials) | Results (Exp 3/4) + Methods wording (drafted in DECISIONS) | NEEDS-POINTER ⚠️ (binding CSVs) |
| B2 | ARIA never emerges: 10 models, zero correct, both architectures; confabulation grows more confident with scale | `results/analysis/` (gap tables; degenerate/trajectory CSVs) | **R2 recovered 2/3 at Stage 2** (anomalous set; S8 F2, S9 §4A) — also Stage 1 recovered | Results | NEEDS-POINTER ⚠️ |
| B3 | Trajectory taxonomy is a core empirical contribution: monotonic_climb (screen reader, alt text, WCAG), peak_regress (skip link, Pythia), never_emerges (ARIA, captions, focus indicator, semantic HTML — 4 concepts, both families), mixed | `results/analysis/per_concept_scaling.csv`, `per_concept_trajectories.csv` | Not directly targeted; **S2-target candidate** (can strangers re-derive the classes from raw curves?) | Results + a figure | NEEDS-POINTER ⚠️ |
| B4 | **Pre-registered blind 2026-07-02** (expansion raws exist, unviewed, uncoded — shape committed before coding): inverse scaling (peak_regress) is not skip_link-specific — __ of 49 compounds regress from correct/partial at an intermediate scale to incorrect at maximum scale, in [Pythia / GPT-2 / both]. If the blank fills with ~1, the claim collapses back to skip_link-only and ships that way. **Established exemplar (pre-expansion, already-viewed data):** skip_link regression is cross-architectural — Pythia 12B and GPT-2 1.5B both produce degenerate "a link that is not a link" loops; A2's Step-5 token-competition trace is the mechanism exhibit | Established: DECISIONS 2026-06-28 (gap analysis findings table). Pending: `results/{suite}/{model}-expansion-results.csv` (frozen, tag=expansion) → blind-authored criteria (`docs/findings/coding-criteria-draft.md` + `docs/findings/criteria_authoring.csv`) → `src/accuracy_coding.py` → `gap_analysis` rerun → `per_concept_trajectories.csv` | R5 scored 0/0/1 at Stage 2 — **drowned-not-absent hypothesis; prime S2-target** (requires cross-scale assembly to be visible; see DECISIONS note verbatim) | Results | OPEN — expansion shape pre-registered, numbers pending blind coding; exemplar portion NEEDS-POINTER ⚠️ (skip_link CSVs) |
| B5 | **Fluent wrongness has a sign flip at 2.8B**: confidence_gap +0.37 (160M) → −0.37 (12B) — larger models are *more confident when wrong* on a11y than when right on control | `results/analysis/entropy_confidence.csv`, `fluent_wrongness.csv` — **caveat carried in output: n_control_correct ≈ 2 per scale** | S8 recovered the qualitative shape ("fluency carries no uncertainty signal") under M3 | Results (Exp 2) — with the small-n caveat stated | NEEDS-POINTER ⚠️ + caveat mandatory |
| B6 | **Completion paradox**: syntactic competence precedes declarative knowledge (Pythia 160M: alt-text completion 100%, declarative 0%) | `results/analysis/completion_paradox.csv`; coding criteria documented in DECISIONS 2026-06-27 (`code_completion()` — syntactic, not conceptual, by design) | Not targeted; S2-target candidate | Results | NEEDS-POINTER ⚠️ |
| B7 | Binding↔accuracy correlation is architecture-dependent (GPT-2 r = 0.45; Pythia r = 0.12; 11 compounds only — single-token concepts excluded by construction) | `results/analysis/binding_vs_accuracy.csv`, `binding_accuracy_corr.csv` | — | Results, one paragraph; feeds A4's "correlate" framing | NEEDS-POINTER ⚠️ |

## C. Methodological claims (they ARE findings; TMLR audience cares)

| # | Claim | Evidence | Blind | Paper home | Status |
|---|-------|----------|-------|-----------|--------|
| C1 | **The binding metric is contaminated at late layers** (BOS sinks + prompt-position); cross-domain binding comparisons require a uniform template. This is an artifact class that generalizes to other attention-pairing metrics | head-characterization findings §5; collocation CSV (natural vs uniform template) | Discovered post-blind | Methods + Limitations (and it quietly implicates unaudited metrics elsewhere in the literature — no need to name anyone) | NAILED |
| C2 | Deterministic, version-controlled accuracy coding; 0 uncoded of 510; any criteria change requires a DECISIONS entry | `src/accuracy_coding.py`; DECISIONS 2026-06-27 (×2) + policy entry 2026-06-28 | Enables blind-study verifiability by design | Methods | NAILED (policy + counts read; script not opened) |
| C3 | TL3 generation collapse; **all TMLR data on TL2**, validated as faithful vs raw HF (same behavioral basin, surface-token drift from LayerNorm folding) | DECISIONS 2026-06-28 (three entries: TL3 collapse, TL2 validation, full rerun) | Operational | Methods (version note) + a GitHub issue owed to TransformerLens | NAILED |
| C4 | Perplexity demoted to supplementary (entropy replicates r ≈ 0.96; perplexity r ≈ 0.18); recognition-precedes-generation preserved as suggestive | DECISIONS 2026-06-20 (restructuring); blind: 5/6 Stage 1 analysts independently flagged the entropy-perplexity split | Stage 1 evidence used in the decision | Supplementary | NAILED |
| C5 | Blind-study protocol itself: pre-registered scoring (STAGE2_SCORING.md, effective-on-commit, authored 2026-06-12), independent double scoring, keys closed, deviations logged (incl. Fable→Opus 4.8 model swap 2026-06-13) | `blind-study/` repo: PROTOCOL.md, STAGE2_SCORING.md, runs/stage2/* | It IS the blind study | Methods or Appendix; consider a short "external validation" subsection | NAILED |

## D. Open predictions / pending checks (pre-registerable before running)

| # | Item | What would settle it | Status |
|---|------|----------------------|--------|
| D1 | 12B late-layer "resurgence" may be partly an attention-sink phenomenon, not re-engaged binding | BOS-attention diagnostic on the 12B resurgence heads (`attention_to_bos` already in `src/head_characterization.py`) — one notebook | OPEN (cheap; do before submission) |
| D2 | L29/H7 rigor: mean-ablation (vs zero); ablation effect at final position (vs `reader`) | Both expected to confirm null; closes the obvious reviewer question on A5 | OPEN (cheap) |
| D3 | Subword-split compounds bind *higher* than clean compounds at 2.8B+ (0.329 vs 0.278) — unexpected; composition-step hypothesis vs measurement-point artifact | Further analysis before any claim (DECISIONS 2026-06-21 says so explicitly) | PRELIM — paragraph + hedge, or omit |
| D4 | Head-type battery across Pythia family (160M–12B) for the cross-scale head-characterization picture | Optional; extends A4 across scale | OPEN (optional) |
| D5 | Pile co-occurrence frequency vs sink-head carve-out strength (are the memorized exceptions frequency-driven?) | Optional; would connect A4's carve-outs to A3's frequency story | OPEN (optional) |
| D6 | **Multi-head joint ablation** (earned deep-lexical set for screen_reader; structural heads as labeled contrast; cumulative-KL curve with positive control in the tail; 3-compound robustness panel) — closes the "distributed ensemble" loophole conceded in the Limitations draft; if flat, A5 hardens from "single-head inert" to "earned set jointly unnecessary" and the Limitations paragraph shrinks to the metric caveat only | Spec approved 2026-06-29: `docs/superpowers/specs/2026-06-29-multihead-lexical-ablation-design.md`; targets `notebooks/lexical-head.ipynb` + `src/qk_ov.py` extensions | OPEN — **designed, pending run**; highest-value pending experiment for Section 03 |

## E. Blind study 2 (scoped to TMLR evidence base) — design decisions pending

| # | Item | Note |
|---|------|------|
| E1 | **Corpus definition**: likely `results/` + `data/` + `_analysis/` + selected `src/`, masked. **Must exclude**: README.md, CLAUDE.md, DECISIONS.md, `docs/findings/*`, `paper/` — all contain findings in plaintext (front-door answer key otherwise) | Blocking: decide before any file is copied |
| E2 | Pre-registered targets drawn from this file: A2 (M1 shape, now demonstrated — does the evidence base make it legible?), B4 (R5 drowned-vs-absent — THE scoped-study question), B3 (taxonomy re-derivation: given vs recovered — decide which study this is), B5, B6 | Success criteria claim-shaped, committed to git first (Stage-1/2 precedent) |
| E3 | Analyst pool model-diverse (accidental Stage 2 robustness → deliberate design); web tools off; exit question re: domain/program recognition (contamination has increased since Stage 1: TechRxiv, essay, CAPTURE.md) | Budget: analysts don't need Fable; synthesis does |
| E4 | Distinctive values may fingerprint findings through masking (662; KL = 1e-05; 0.90/0.21). Decide: bin/jitter with documented transform, or accept and log | Same class as Stage 1's `acc`-tag gap — decide, don't discover |

## F. Out of scope (logged for the series, not this paper)

| # | Item | Why out |
|---|------|---------|
| F1 | OLMo checkpoint work (active unlearning; alt="photo.jpg" regression by step 30K); Zhang et al. (2026) mixed-format vocabulary; INTERCEPT intervention study | Load-bearing for the OLMo paper; deliberately withheld from Paper 1/TMLR (standing decision) |
| F2 | Stage 2 novelty follow-ups not resolved by A4: N2 (Pythia-1B dip), N3 (early convergence ~0.5% of training), N4 (steering null at L33), N5 (arch-b duplication bug fix) | CAPTURE.md follow-up queue; N1 resolved by head characterization (see A4) |
| F3 | ~~Multi-head joint ablation — deferred~~ **Un-deferred 2026-06-29**: approved design spec exists (`docs/superpowers/specs/2026-06-29-multihead-lexical-ablation-design.md`). Moved to D6 | See D6 |

## G. Integration debts (claims the repo currently makes that the findings no longer support)

| # | Debt | Fix |
|---|------|-----|
| G1 | **Title + abstract still assert the March thesis** ("Sustained Deep-Network Binding Is a Correlate…" title survives, but abstract per DECISIONS 2026-03-03 asserts *necessary structural condition* — contradicted by A4/A5/A6) | Apply `binding-reframe-draft.md` Edit 1 (abstract) + reconsider title framing; Edits 2–3 place the new subsection + discussion/limitations blocks |
| G2 | README.md + CLAUDE.md stale (describe how-models-think layout, `paper-1-emergence/` / `accessibility-knowledge-emergence/` paths, GitHub pointer) — and both contain findings plaintext (see E1) | CC task (Trisha, queued 2026-07-01) |
| G3 | Path inconsistency: head-characterization findings doc cites `results/lexical-head-results.md`; file appears to live at `docs/findings/lexical-head-results.md` | Reconcile pointer or move file |
| G4 | CAPTURE.md correction for the 2026-06-14 GPT-2-heads-on-Pythia carryover is marked done in findings doc — verify the CAPTURE.md entry exists and states that the conclusion survived but the recorded cross-architecture evidence did not | Verify (5 min) |
| G5 | **Unpublished dependency debt**: thatDangCircuit experiments (three-tier population ablations, N4 steering null, extended compound list) are cited in Section 03 prose but live in a private repo — nothing citable, nothing verifiable. Blind-study repo has the same status (C5 depends on it) | Split remedy, decided 2026-07-02: (a) load-bearing claims get reproduced inside tmlr — D6 covers the population question; port or soften anything else Section 03 leans on; (b) thatDangCircuit goes public + Zenodo DOI (GitHub integration, CITATION.cff with ORCID, toggle before v1.0.0 release) — paper cites the DOI; (c) essay "Why I'm Not Writing the Ablation Paper" narrates it on trishasalas.com; (d) blind-study repo publishes only AFTER study 2 to avoid contaminating the masked corpus |

---

*Rows are cheap. Add the new tangent(s) here before they become directories.*
