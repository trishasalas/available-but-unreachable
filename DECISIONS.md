# DECISIONS.md
Research and figure decisions with rationale.

---

## Replication Verification Against Paper 1

### 2026-07-03 — n=49 coding criteria authored blind (Gate 1 judgment work complete)

**Decision:** All 41 expansion-compound criteria authored in
`docs/findings/criteria_authoring.csv` across two sessions (2026-07-02 evening,
2026-07-03 morning). **Path note 2026-07-03:** worksheet + coding_coverage.csv
moved from `_analysis/` to `docs/findings/` after the first freeze attempt
revealed `_analysis/*` is gitignored — git reported "working tree clean" while
the instrument sat invisible. Load-bearing artifacts don't live in scratch;
caught by `git log -1 --stat` audit. Authored conversationally — Trisha dictated the
practitioner bar per compound, Fable 5 scribed into the worksheet; semantics
are Trisha's throughout, transcription is the model's. Original 8 criteria
UNTOUCHED (regression guard applies at translation).

**Blind state:** frequency table CLOSED for the entire authoring window;
expansion raws exist (tag=expansion, run 2026-07-02) and remain UNVIEWED and
UNCODED. Criteria precede data, per house rule and B4 precedent.

**Sense policy:** Option A + per-response sense recording (decided
2026-07-02, logged in coding-criteria-draft.md) — implemented as the
`a11y_sense_markers` worksheet column; analysis reports Spearman both ways
(all rows / a11y-sense-only).

**Coding doctrine accreted during authoring (CC: encode as comment block):**
1. LATERAL confusion (wrong mirror: AD↔captions, decorative↔informative,
   semantic-web-for-semantic-markup) → INCORRECT.
2. VERTICAL confusion (instance-for-umbrella: alt-text-for-text-alternative;
   tab-for-tabpanel; name-collapse on description) → PARTIAL.
3. SYNONYM pairs (target_size↔touch_target) → cross-definition NODS.
4. MECHANISM-FOR-CONCEPT (attribute-as-the-thing) — severity is PER-ROW:
   where the mechanism constitutes the concept (aria-live for live region)
   → nods; where the mechanism is categorically different plumbing
   (aria-describedby for accessible description, per 2026-07-03 veto)
   → INCORRECT.
5. TRENCH COAT (compound restated with a modal verb: "help should be
   consistent") → circular → INCORRECT. tc always loses.

**Pre-registered predictions (falsifiable at coding time, made blind):**
- Token-competition / wrong-domain capture candidates: sensory_characteristics
  (food science), redundant_entry (database dedup), status_message
  (HTTP/social/server), error_identification (debugging), pointer_cancellation
  (C/C++ pointers), landmark_region (geographic), focus_management
  (attention/self-help).
- Adjacent-technique substitution signature: AD↔captions confusion marker.
- never_emerges candidate: tree_grid (rarest widget compound).
- Deliberate ceiling anchors (high-freq, low discrimination, SHOULD be easy
  if the frequency thesis holds): sign_language, text_formatting, form_field,
  responsive_design.

**Vetoes RESOLVED 2026-07-03 (Trisha):**
1. informative_image: VETOED — alt-text mention is the GATE; no alt text (or
   literal "text alternative") → INCORRECT. Partial zone eliminated; binary row.
2. accessible_description: VETOED — aria-describedby evicted from the row
   entirely (programmatic thing, categorically different); naming it as the
   answer → INCORRECT, not partial. Doctrine plank 4 amended accordingly.
3. cognitive_disabilities: RATIFIED as-is — mental-illness conflation stays
   PARTIAL ("tough one — leave as is").

**Next:** ~~Trisha reviews vetoes~~ DONE 2026-07-03 → git commit (freezes
predictions) → CC translation per handoff
(docs/findings/criteria-handoff-2026-07-03.md) → ~~S5/S8~~ S8 verified done
(no attention/ in results/), S5 remains CC's → gap_analysis → dual Spearman
→ Fable review before 2026-07-07.

---

### 2026-07-02 — B4 rewritten as blind pre-registration (expansion scope)

**Decision:** CLAIMS.md row B4 rewritten from a skip_link-specific claim to a two-part row: (1) a **pre-registered blind template** for the n=49 expansion — "inverse scaling (peak_regress) is not skip_link-specific: __ of 49 compounds regress from correct/partial at an intermediate scale to incorrect at maximum scale" — with the count and family blanks left open; (2) the **established exemplar** (skip_link cross-architectural degeneration, DECISIONS 2026-06-28) preserved verbatim as already-viewed evidence, with A2's Step-5 trace as the mechanism exhibit.

**Blind state at time of writing:** expansion raws exist (`tag=expansion`, run 2026-07-02, both suites, all scales) but are **unviewed and uncoded** — operator ran the batteries and moved files only. Coding criteria not yet authored. Frequency table closed. This entry timestamps the claim shape BEFORE any expansion result is seen, extending the criteria-before-data rule to claims rows.

**Falsification path written into the row:** if the blank fills with ~1, the claim collapses back to skip_link-only and ships that way — the collapse is a shippable negative, not a failure.

**Status change:** NEEDS-POINTER → OPEN (expansion portion) + NEEDS-POINTER retained for the exemplar's skip_link CSVs.

**Enforcement note:** this pre-registration has teeth only once committed to git. Commit CLAIMS.md + this entry before criteria authoring resumes.

---

### 2026-07-02 — Results layout restored; expansion elicitation protocol

**Decision:** Canonical layout declared: raw per-model outputs live at results/{suite}/ (pythia, gpt2); experiment-specific outputs live in named dirs (frequency/, mlp_investigation/, logits/, analysis/). The attention/ grouping (introduced in 26c6a8d reorg) is dissolved — it held raw elicitation/entropy/binding triplets and was never attention-specific. load_all_results() now allowlists suite dirs explicitly.

**Resurrection:** pythia-2.8b-head-characterization.csv and pythia-2.8b-collocation.csv restored from d50441f (committed there,
deleted by a later reorg commit). A4/A5 evidence pointers valid again.

**Expansion protocol:** run_all_prompts() gains concepts= and tag= params. The 41 new compounds run with concepts=PENDING_CRITERIA, tag='expansion', writing {model}-expansion-results.csv — original {model}-results.csv raws are frozen and never overwritten. Colab sessions end with files.download(); loss class (ephemeral /content) closed.

**Rationale for suite-first over experiment-first (added same day):** The experiment-first scheme from the 26c6a8d reorg (frequency/, mlp_investigation/, etc.) is arguably the better abstract design, and it is retained for targeted experiment outputs. Raw per-model batteries return to results/{suite}/ for three reasons: 

1. the elicitation/entropy/binding triplets are substrate, not an experiment — every downstream analysis consumes them, so "core
characterization vs. targeted follow-up" is the distinction the layout nowencodes;
2. every existing contract already points at results/{suite}/ — elicitation.py writes it, analysis.py reads it, the head-characterization
findings and CLAIMS.md cite it, and the resurrected CSVs' git history lives
there — so restoration cost one two-line loader patch versus edits to two
writers, one reader, and four docs mid-campaign; 
3. provenance continuity: resurrected files return to the paths their commit history records.

### Defensible-over-ideal, chosen knowingly.

**Parked (post-TMLR):** Layout v3 — full experiment-first migration (results/elicitation/{suite}/ etc.) as a single contained commit. Precondition: consolidate all results-path constants into one module (src/paths.py or similar) so the next philosophy change is a five-line diff, not archaeology. One layout at a time; this file is where layouts are declared.

### 2026-06-28 — MLP investigation results: magnitude hypothesis disconfirmed, token competition mechanism discovered

**Decision:** The MLP magnitude interference hypothesis is disconfirmed. The actual mechanism for skip_link inverse scaling is a single-token competition at generation Step 5, where "displayed" (correct) is outranked by "click" (incorrect) at 12B but wins at 6.9B. Document both the negative result and the positive finding.

**Original hypothesis:** MLP layers at 12B actively interfere with compound binding more than at 6.9B, suppressing domain-specific signal with stronger general-language priors. This would manifest as elevated MLP/attention ratios for skip_link vs a control compound (color_contrast) at 12B.

**Disconfirmation:** Residual stream decomposition across 1B, 6.9B, and 12B showed:
- Final-layer MLP spike is architectural, not compound-specific. All models show massive MLP norm at the last layer (1B: 64, 6.9B: 234, 12B: 324) regardless of prompt.
- Cross-prompt comparison: MLP/attention ratios are nearly identical between skip_link and color_contrast at both 6.9B (4.437 vs 4.444, delta -0.007) and 12B (4.365 vs 4.888, delta -0.523). Color_contrast actually receives MORE MLP rewriting, not less.
- The MLPs are doing the same amount of work for compounds the model gets right and compounds it gets wrong.

**Logit lens finding:** Vocabulary projection at the final MLP layer shows identical generic tokens for both prompts ("earthqu", "researc", "tradem", "counc"). The final-layer MLP is doing output calibration, not semantic work. This is consistent with the logit lens literature (nostalgebraist) on GPT-2 architecture, now confirmed on Pythia.

**Logit lens on skip_link:** Zero topic-relevant tokens at ANY scale (160M through 12B). "Skip", "navigation", "jump" never appear in top-5 predictions at any layer. This is true even at 6.9B where generation is correct. Low-frequency domain knowledge is encoded distributedly — present in the residual stream (generation proves it) but invisible to direct vocabulary projection.

**The actual mechanism — step-by-step token competition:**

Autoregressive generation traced step-by-step across all six Pythia scales reveals the inverse scaling operates at a single decision point. All models that reach Step 4 choose "not" (6.9B and 12B). The divergence occurs at Step 5:

| Scale | Step 4 | Step 5 chosen | "displayed" rank | "click" rank | Generation path |
|-------|--------|--------------|-----------------|-------------|----------------|
| 160M  | links  | that         | absent          | absent      | graph theory    |
| 410M  | skipped | when        | absent          | absent      | web-bypassing   |
| 1B    | link   | used         | absent          | absent      | CS networking   |
| 2.8B  | skipped | when        | absent          | absent      | tree traversal  |
| 6.9B  | not    | **displayed** | **rank 1**     | absent      | ✓ correct       |
| 12B   | not    | **click**    | **rank 4**     | **rank 1**  | ✗ degenerate    |

"Displayed" is present as a candidate at both 6.9B (rank 1, wins) and 12B (rank 4, loses to "click"). The concept is not absent at 12B — it is outcompeted. "Click" is a higher-frequency web token that becomes strong enough at 12B to overtake the correct but lower-frequency "displayed."

**Conceptual trajectory across scale:** The compound "skip link" develops through distinct conceptual neighborhoods:
- 160M: physical/graph theory ("link between two links")
- 410M: web-adjacent ("skipped when clicked")
- 1B: CS networking ("data link used in computer networks")
- 2.8B: data structures ("skipped when traversing a tree structure") — notably, "navigating" and "browsing" appear in Step 6 top-5
- 6.9B: correct web accessibility meaning ("not displayed in a browser")
- 12B: correct domain but wrong conclusion ("not clickable" → degenerate loop)

**Significance for the paper:**
1. The inverse scaling is not about knowledge disappearing. The correct token is present in 12B's candidate set. It loses a competition it won one scale down.
2. This is a different mechanism from absence (1B) or wrong domain (160M). Scaling creates stronger general-language priors ("click" for web contexts) that outcompete lower-frequency domain-specific tokens ("displayed" in the accessibility sense).
3. The MLP magnitude negative result is itself significant: it rules out gross interference and points to directional (content-level) competition rather than structural suppression.
4. The step-by-step table is a potential figure showing inverse scaling captured at the exact token where it occurs.

**Data:** All results saved to `results/mlp_investigation/` — six models × five CSVs each (decomposition, late_layer_summary, logit_lens, vocab_projection, skip_link_steps).

### 2026-06-28 — OLMo 2 1B methodology: raw HuggingFace for generation/entropy, TL3 for binding only

**Decision:** OLMo 2 1B experiments use a split-tool methodology. Generation (elicitation prompts) and entropy are run through raw HuggingFace `transformers`. Binding analysis uses TransformerLens 3 (TransformerBridge). TL3 is not used for generation.

**Rationale:** TL3 is the only TransformerLens version that supports OLMo — TL2 does not. However, TL3's generation pathway produces degenerate repetition on Pythia (confirmed 2026-06-28, see earlier entry). The binding/attention data from TL3 was validated as faithful: Pythia binding scores between TL2 and TL3 showed near-identical topology with only small magnitude shifts (e.g., L0H3 screen_reader: 0.9656 → 0.9687). The failure is isolated to the `generate()` pathway, not the activation caching or hook infrastructure.

Raw HuggingFace generation was validated against TL2 on Pythia 2.8B (see 2026-06-28 TL2 validation entry). Same behavioral trajectories, same failure modes, different surface tokens due to LayerNorm folding. Raw HF is a faithful representation of the model's actual generation capabilities.

**Implication for cross-model comparisons:** Pythia results use TL2 for all three data types (generation, entropy, binding). OLMo results use raw HF for generation/entropy and TL3 for binding. The generation pathway difference (TL2 with LayerNorm folding vs raw HF without) is documented but not expected to affect behavioral accuracy coding, since the TL2-vs-HF validation showed identical coding outcomes on matched prompts.

**OLMo checkpoint trajectory:** Six stage-1 checkpoints are available in `OlmoSpelunking/results/OLMo-2-0425-1B/` (step 10K through step 930K). Prior gap-analysis probes on these checkpoints confirmed the active unlearning phenomenon: evaluative alt text generation degrades from descriptive (`alt="A man in a white shirt"`) at step 10K to filename-based (`alt="photo.jpg"`) by step 30K, while declarative knowledge of alt text simultaneously improves. The split-tool methodology will be applied consistently across all checkpoint reruns.

**Files affected:** New OLMo experiment notebook (TBD). Results to a new subdirectory in `results/` (naming TBD — likely `results/olmo-2-1b/`).

### 2026-06-28 — Gap analysis framework: accuracy coding and replicable pipeline

**Decision:** Accuracy coding for elicitation responses is implemented as a deterministic Python module (`src/accuracy_coding.py`). Every coding criterion is documented inline. The gap analysis (`src/gap_analysis.py`) imports the coding module, applies it to all results, and saves output to `results/analysis/`. Reproducible via `python -m src.gap_analysis` or from `notebooks/analysis.ipynb`.

**Rationale:** The coding rules ARE the methodology. They must be version-controlled, reviewable, and reproducible. A reviewer clones the repo, runs the command, and gets identical CSVs. No manual coding, no subjective interpretation, no hidden state.

**Coding scheme:**
- `correct`: captures the core accessibility-relevant meaning a practitioner would recognize
- `partial`: touches the right domain but misses the key point
- `incorrect`: wrong domain, circular, degenerate, or nonsensical

Criteria are concept-specific. See `src/accuracy_coding.py` for full documentation.

**Key findings from initial run (Pythia + GPT-2, all scales):**

| Finding | Detail |
|---------|--------|
| Gap persists at all Pythia scales | Declarative accuracy outpaces evaluative at every scale except 12B |
| 12B gap closes via declarative regression | 12B declarative drops from 70% (6.9B) to 50% — skip_link and keyboard_navigation regress from correct to incorrect |
| GPT-2 gap widens with scale | At 1.5B: declarative 60%, evaluative 10% — a 50 pct pt gap, the largest in either suite |
| skip_link inverse scaling is cross-architectural | Both Pythia 12B and GPT-2 1.5B produce degenerate "a link that is not a link" loops |
| ARIA: 10 models, zero correct | Universal failure across both architectures, all scales |
| 4 concepts never emerge in either family | ARIA, captions, focus indicator, semantic HTML — all coded incorrect or partial at maximum scale |

**Output directory:** `results/analysis/` (no underscore — included in reproducibility scope, excluded from blind study by content type, not naming convention).

**Next steps:** Six extended analyses planned (entropy confidence, binding-accuracy correlation, per-concept scaling curves, entropy divergence, degenerate detection, completion paradox). Documented in CC instructions. Implementation by CC in `src/gap_analysis.py`.

---

### 2026-06-28 — Accuracy coding changes require DECISIONS.md entry

**Decision:** Any change to the coding criteria in `src/accuracy_coding.py` must be accompanied by a DECISIONS.md entry documenting what changed and why.

**Rationale:** The coding rules determine what counts as "correct." Changing a rule retroactively changes every table and figure downstream. The decision record ensures that coding evolution is traceable and that blind study analysts can verify the rules weren't tuned to produce favorable results.

---

### 2026-06-27 — `code_completion()` added; six extended analyses implemented

**Decision:** Added `code_completion(concept, prompt, output)` to `src/accuracy_coding.py` and routed `prompt_type == 'completion'` through it in `code_response()`. Implemented the six extended analyses (planned in the gap-analysis framework entry above) in `src/gap_analysis.py`. All outputs save to `results/analysis/` and reproduce via `python -m src.gap_analysis`.

**Why this is a coding-criteria change (per the policy entry above):** `completion` responses were previously `uncoded`. They are now graded, so `elicitation_coded.csv` changes. No other coding function was modified — `hypothesis`, `validation`, and non-bicycle `control` rows remain `uncoded` (not required by these analyses; coding them is deferred to avoid expanding blind-study scope).

**`code_completion()` criteria (syntactic, not conceptual):** grades whether the model emitted the structurally-correct continuation, independent of whether it can *define* the concept. This is deliberate — it isolates pattern-matching competence for the completion-paradox analysis.
- `alt text`: `correct` if output contains `alt="<non-empty>"`; `partial` if `alt=""`/bare `alt=`; else `incorrect`.
- `captions`: `correct` if output contains `track` AND `caption`; `partial` if one; else `incorrect`.
- `page title`: `correct` if non-empty `<title>…`; `partial` if empty `<title>`; else `incorrect`.
- `script`: `correct` if `src="…"`; `partial` if bare `src=`/`</script>`; else `incorrect`. (`page title` and `script` are syntactic controls — no declarative counterpart.)

**Six extended analyses (all read existing `results/{pythia,gpt2}/*.csv` — no new experiments):**

| # | Output CSV(s) | What it measures |
|---|---------------|------------------|
| 1 | `entropy_confidence.csv`, `fluent_wrongness.csv` | last-token entropy by concept×scale×accuracy; "fluent wrongness" = confidence when wrong on a11y vs right on bicycle control |
| 2 | `binding_vs_accuracy.csv`, `binding_accuracy_corr.csv` | max binding score paired with declarative accuracy; Pearson/Spearman per suite (11 compounds only) |
| 3 | `per_concept_scaling.csv`, `per_concept_trajectories.csv` | per-concept accuracy across scale; trajectory class (monotonic_climb / peak_regress / never_emerges / mixed) |
| 4 | `entropy_divergence.csv` | declarative vs evaluative mean entropy per scale |
| 5 | `degenerate_by_scale.csv`, `degenerate_by_concept.csv`, `degenerate_by_prompt_type.csv` | rate of degenerate repetition (1–4 word phrase repeated ≥3×) |
| 6 | `completion_paradox.csv` | few-shot completion accuracy vs declarative accuracy per concept×scale |

**Key findings from first run (consistent with Paper 1):**

| Finding | Detail |
|---------|--------|
| Fluent wrongness emerges at the 2.8B threshold | Pythia `confidence_gap` flips from +0.37 (160M, more uncertain when wrong) to −0.37 (12B, *more confident* when wrong on a11y than right on control). Sign flip at 2.8B. |
| Completion paradox is strongest at small scale | Pythia 160M: alt-text completion 100% correct while declarative 0%. Model emits `alt="…"` syntactically before it can define alt text. |
| Trajectories replicate Paper 1 | ARIA `never_emerges` (both families); screen reader / alt text / WCAG `monotonic_climb`; skip link `peak_regress` (Pythia). |
| Binding↔accuracy correlation is architecture-dependent | GPT-2 Pearson r=0.45; Pythia r=0.12 — binding depth predicts accuracy more in GPT-2. |

**Caveats recorded in the outputs (transparency for blind study):**
- `fluent_wrongness.csv` carries `n_control_correct` (≈2 per scale — the bicycle baseline is small because `code_control()` only grades 3 subtasks; 20 bicycle rows remain `uncoded`).
- `binding_vs_accuracy.csv` covers only the 11 multi-word compounds; single-token concepts (ARIA, WCAG, HTML) have no cross-token binding by construction.

---

### 2026-06-27 — Coded the remaining prompt types (validation, hypothesis, control); 0 uncoded

**Decision:** Added graders so every elicitation response is coded. Previously `validation`, `hypothesis`, and non-bicycle `control` rows (330 total) returned `'uncoded'`; now `elicitation_coded.csv` has **0 uncoded of 510**.

**Why:** Gradeable data shouldn't sit out of the analysis. These rows contain real, scoreable responses; leaving them `uncoded` silently dropped them from every accuracy-based table.

**New / extended coding functions** (in `src/accuracy_coding.py`):
- `code_validation(concept, prompt, output)` — routes by prompt content: acronym expansion (`ARIA`→"accessible rich internet", `HTML`→"hypertext markup"), missing-attribute diagnosis on `<img>`, and screen-reader-failure reasoning.
- `code_hypothesis(concept, prompt, output)` — diagnostic alt-text probes: names/adds the missing `alt` attribute (`alt=` for "correct this code"), or explains the screen-reader failure.
- `code_control()` extended — non-bicycle control concepts (`closed captions`, `color contrast`, `page title`) graded for conceptual correctness; added definitional bicycle probes ("What is a bicycle?", "Explain bicycles…").

**Methodological boundary (important for the blind study):** the 150 non-bicycle `control` rows are **accessibility-concept probes**, not reasoning baselines. The bicycle `control` remains the reasoning baseline. To avoid conflating roles, the newly-coded rows are **not** folded into the existing declarative/evaluative concept tables. Instead they surface through a new coverage table, `accuracy_by_prompt_type.csv` (suite × scale × prompt_type → n, n_coded, n_uncoded, accuracy_pct), so all coded data is represented without redefining the Paper-1-aligned tables.

**Coding distribution after change:** correct 186 / partial 147 / incorrect 177 (of 510). The existing declarative/evaluative/gap/emergence tables are **unchanged** (they filter by prompt_type and never included these rows).

---

### 2026-06-28 — TL3 generation collapse confirmed; reverted to TL2 for TMLR

**Decision:** All TMLR experiments rerun on TransformerLens 2.x (HookedTransformer). TL3 (TransformerBridge) produces degenerate generation and is unsuitable for the TMLR submission. TL3 reserved for future OLMo work pending bug resolution.

**Evidence:** Three-way comparison on Pythia 2.8B, same prompts, same greedy decoding:
- Raw HuggingFace: Varied, topically relevant, wrong but coherent ("I have a photo in my website. I want to make it accessible to people with disabilities")
- TL2 (HookedTransformer): Slightly different surface tokens, same behavioral trajectory ("I have a photo gallery on my website. I want to add an accessibility attribute to the")
- TL3 (TransformerBridge): Degenerate collapse across all evaluative prompts ("the same time the same time the same time")

Binding scores between TL2 and TL3 show small magnitude shifts (e.g., L0H3 screen_reader: 0.9656 → 0.9687) but the attention topology is preserved. The failure is downstream of attention — generation pathway only.

**Rationale for reverting:** The 2026-06-21 decision to use TL3 was based on it being the current version and the expectation that reviewers would reproduce on current tooling. The generation collapse invalidates that rationale. TL2 produces outputs consistent with raw HuggingFace inference, confirming it is a faithful wrapper. Correct results on a stable tool outweigh version currency.

**Update to 2026-06-21 entry:** The "Rationale for not pinning TL 2" in that entry is superseded by this decision. TL3's generation collapse is not a minor token-level shift — it is a fundamental failure that breaks the elicitation experiment entirely.

**Action:** File a GitHub issue on TransformerLens with the three-way comparison as a reproduction case.

---

### 2026-06-28 — TL2 validated as faithful wrapper via raw HuggingFace comparison

**Decision:** TL2's HookedTransformer produces behaviorally equivalent outputs to raw HuggingFace inference. LayerNorm folding causes numerical drift that compounds over autoregressive generation, producing different surface tokens but identical failure modes. The paper's elicitation findings reflect the model's actual capabilities, not a measurement artifact.

**Evidence:** Pythia 2.8B, prompt "What accessibility attribute is missing from this HTML: <img src='photo.jpg'>?", greedy decoding (temp=0):
- Raw HF: "I have a photo in my website. I want to make it accessible to people with disabilities"
- TL2: "I have a photo gallery on my website. I want to add an accessibility attribute to the"

Same attractor (StackOverflow-style help request frame). Neither identifies the missing alt attribute. Different surface tokens, identical behavioral conclusion.

**Mechanism:** HookedTransformer pre-folds LayerNorm parameters into attention and MLP weight matrices. The computation is mathematically equivalent but floating-point non-commutativity introduces tiny numerical differences that compound token-by-token over autoregressive generation. After 20+ tokens the models diverge at the surface level while staying in the same behavioral basin.

---

### 2026-06-28 — Full scaling suite rerun complete (Pythia 160M–12B, GPT-2 small–XL)

**Decision:** All experiments rerun on TL2 via Google Colab A100. Results stored in `results/pythia/` and `results/gpt2/`. Three CSVs per model: binding, entropy, results.

**Environment:** Colab Pro+ with A100 GPU. TransformerLens pinned to match local MacBook version. NumPy and torchaudio version conflicts resolved via pinned installs (Colab's pre-installed packages conflict with TL2 dependencies due to a recent Hugging Face `transformers` change that introduced a transitive `torchaudio` dependency for Parakeet audio model support).

**Runtime:** ~5 minutes per model on A100 vs ~15 minutes on local M5 MacBook Pro.

---

### 2026-06-28 — skip_link inverse scaling: generation regression at 12B with preserved binding

**Decision:** Document and investigate the skip_link inverse scaling as a key finding for the TMLR paper. The compound "skip link" shows correct generation at 6.9B but degenerate looping at 12B, despite near-identical binding scores. This dissociation between binding and generation is direct evidence that the declarative-evaluative gap operates downstream of attention.

**Generation comparison:**
- 6.9B: "a link that is not displayed in the browser. It is used to jump to a specific location in the page." (near-correct)
- 12B: "a link that is not a link. It is a link that is not a link." (degenerate loop)

**Binding comparison (max per layer for skip_link):**

| Metric | 6.9B | 12B |
|--------|------|-----|
| Peak binding | 0.989 (L3) | 0.978 (L3) |
| Late-layer mean | 0.677 | 0.620 |
| Late-layer pattern | Sustained (L25–L30 all >0.68) | Oscillating (spikes at L30, L34 interspersed with drops at L27, L29, L32) |
| Final layer | 0.260 (L31) | 0.251 (L35) |

**Interpretation:** The attention mechanism binds "skip" and "link" as a compound at both scales. The failure at 12B is not a binding failure — it is a generation-pathway failure. The oscillation pattern in 12B's late layers suggests interference: something is disrupting the binding signal between attention layers. The most likely candidate is MLP interference, where stronger general-language priors at 12B override the domain-specific compound binding.

**Connection to the blind study:** The skip_link inverse scaling was one of the findings not recovered by the blind study analysts. The focused rerun makes the scaling trajectory visible (160M circular → 410M warmer → 2.8B correct → 6.9B correct with detail → 12B degenerate), which requires cross-scale comparison to interpret as regression rather than standalone failure.

---

### 2026-06-28 — Next investigation: MLP interference at late layers

**Decision:** Run residual stream decomposition on 6.9B and 12B to determine whether MLP layers are the source of late-layer binding oscillation at 12B.

**Method:**
- Cache activations for the skip_link prompt on both models
- Extract attention output norm and MLP output norm at each late layer (last token position)
- Compare MLP/attention ratio across layers, focusing on oscillation points
- Control comparison: run the same analysis on a compound that does NOT show inverse scaling (e.g., color_contrast or link_text) to verify the effect is compound-specific

**What confirmation would mean:** The declarative-evaluative gap is not passive absence of knowledge. The model's attention correctly binds the compound, but MLP layers — where factual/associative knowledge is stored — actively compete with domain-specific binding at larger scales. Scaling amplifies general-language priors, which makes them better at overriding low-frequency domain compounds. The gap widens with scale because scale amplifies the wrong signal.

**What confirmation would mean for CPT:** Mixed-format training at an early checkpoint is not just adding knowledge — it is establishing domain-specific MLP representations before general-language priors become strong enough to suppress them.

**Files needed:** New notebook or addition to existing binding notebook. Results to `results/pythia/` with naming convention TBD.

### 2026-06-21 — TransformerLens version change: TL 2 → 3.3.0

**Decision:** All TMLR data was generated on TransformerLens 3.3.0. Paper 1 used TransformerLens 2.x. The version difference produces different token-level outputs for declarative prompts (e.g., 2.8B "A screen reader is" → "reads aloud the text" on TL 2 vs degenerate output on TL 3.3.0). All TMLR data is internally consistent.

**Implications:**
- Elicitation response coding must be done fresh against TL 3.3.0 outputs — Paper 1's correct/partial/incorrect table cannot be carried forward
- The qualitative findings (threshold, gap, binding patterns) should hold across versions; exact token-level completions shift
- Entropy values may also differ (systematic ~1.5 point offset observed, pending investigation)
- Methodology section must note the TL version explicitly

**Rationale for not pinning TL 2:** TL 3.3.0 is the current version. Reviewers reproducing the work will use a current version. Running on TL 2 would produce Paper 1-matching outputs but would not be what anyone reproduces going forward. Internal consistency across the TMLR dataset matters more than exact replication of Paper 1's token-level outputs.

**Approach:** Present TMLR results on their own terms. Note the version in methodology. Where findings differ from Paper 1 at the token level, acknowledge the version change as the likely cause. The binding replication (which is numerical, not token-level) already confirms the core mechanistic findings hold across versions.

---

### 2026-06-21 — Pythia binding replication: late-layer resurgence confirmed

**Decision:** The new 11-compound binding data corroborates Paper 1's late-layer resurgence finding on 5 of 6 Pythia models.

**Results:**

| Model | Paper Deepest Strong Layer | Workbook Deepest Strong Layer | Δ |
|-------|---------------------------|-------------------------------|----|
| 160M  | 11                        | 11                            | 0  |
| 410M  | 9                         | 23                            | +14 |
| 1B    | 6                         | 6                             | 0  |
| 2.8B  | 29                        | 30                            | +1 |
| 6.9B  | 30                        | 29                            | −1 |
| 12B   | 34                        | 34                            | 0  |

**410M outlier explained:** Paper 1 measured only screen_reader at 410M (deepest strong layer = 9). The expanded 11-compound set finds strong binding at deeper layers for closed_captions (L23), skip_link (L23), page_title (L22), and others. Screen_reader alone at 410M still behaves consistently with Paper 1. The expanded compound set reveals binding persistence not visible in the original three-compound scope.

**Strong head counts:** Track Paper 1 closely — exact at 160M (10) and 410M (22), within 1–3 at 6.9B and 12B. 2.8B shows 40 vs 25, consistent with more compounds producing more strong heads.

**Investigation note:** Initial analysis misread Paper 1's "Last Layer" column as a head count rather than a layer depth index. This was caught by comparing against the paper's methodology section (p.8), which defines the metric as attention weights. Column label changed to "Deepest Strong Layer" for TMLR to prevent this misinterpretation.

---

### 2026-06-21 — GPT-2 binding replication: main table exact, per-compound variation at XL

**Decision:** GPT-2 main binding table (screen_reader across all four sizes) replicates Paper 1 exactly — all 12 deltas are zero. Per-compound data at XL (alt_text, skip_link) shows minor quantitative variation from Paper 1 while maintaining the same qualitative pattern.

**Per-compound XL discrepancies:**
- alt_text: Strong heads 45 vs 34 (+11), Deepest Strong Layer 40 vs 19 (+21)
- skip_link: Total >0.1 274 vs 253 (+21), Strong heads 44 vs 49 (−5), Deepest Strong Layer 43 = 43
- screen_reader: exact match on all metrics

**Explanation:** Paper 1 tested alt_text and skip_link at select scales only (2.8B Pythia, XL GPT-2) with less thorough verification than the primary screen_reader analysis. The new pipeline runs all compounds uniformly across all sizes. The prompts are identical (verified against original notebook). The variation is consistent with the broader, uniform methodology used here and does not affect the qualitative findings.

**TMLR approach:** Present the new data as the primary analysis. Note in methodology that the expanded compound set uses a uniform pipeline across all sizes (vs. Paper 1's approach of testing additional compounds at select scales). Screen_reader replicates exactly. Minor quantitative differences in alt_text and skip_link at XL are consistent with the expanded scope. One sentence, not a paragraph.

**Suggested wording (methodology):** "We replicated the original binding analysis with an expanded compound set of eleven accessibility terms, run uniformly across all model sizes in both families. Screen reader binding replicates the original findings exactly across all four GPT-2 sizes and five of six Pythia models (within ±1 layer). The expanded compound set reveals additional binding depth at 410M not visible in the original three-compound scope."

**Suggested wording (410M):** "The expanded compound set reveals binding persistence at 410M not visible in the original three-compound analysis. Screen reader binding at 410M replicates the original finding; additional compounds — particularly closed captions and skip link — show strong binding at deeper layers, indicating compound-specific variation in binding depth that the original scope did not capture."

---

### 2026-06-21 — Column label fix: "Last Layer" → "Deepest Strong Layer"

**Decision:** Rename the binding summary table column from "Last Layer" (Paper 1) to "Deepest Strong Layer" in the TMLR submission.

**Rationale:** "Last Layer" is ambiguous — it was misread as a head count during the replication verification when it is actually a layer depth index (the deepest layer containing a head with binding ≥ 0.5). "Deepest Strong Layer" is self-documenting. Paper 1's GPT-2 table already used "Last Strong Layer" (p.24); the Pythia table (p.19) used "Last Layer." TMLR should be consistent.

---

### 2026-06-21 — GPT-2 promoted to co-equal cross-architecture analysis

**Decision:** Present GPT-2 results alongside Pythia as co-equal evidence organized by finding, not as "Replication: GPT-2" footnotes after each Pythia section.

**Rationale:** Paper 1 treated GPT-2 as a replication check — each experiment had a Pythia section followed by a brief GPT-2 confirmation. For TMLR, both model families have full data (all experiments, all sizes, all compounds). Organizing by finding rather than by architecture is more sophisticated, reduces redundancy, and naturally elevates GPT-2 from footnote to co-equal evidence. Divergences between families (e.g., GPT-2's shallower binding depth, GPT-2 small showing declarative knowledge Pythia 160M lacks) become discussion points about training data effects rather than separate sections.

---

### 2026-06-21 — Subword tokenization natural experiment

**Decision:** Document and analyze the binding difference between cleanly-tokenized compounds (8: screen_reader, alt_text, skip_link, color_contrast, page_title, form_label, link_text, focus_indicator) and subword-split compounds (3: keyboard_navigation, closed_captions, semantic_html).

**Finding:** Subword-split compounds show consistently *higher* mean binding than clean compounds at scales 2.8B+ (e.g., 0.329 vs 0.278 at 2.8B, 0.334 vs 0.282 at 6.9B). This was unexpected — the hypothesis was that subword splits would weaken binding due to the additional composition step.

**Interpretation (preliminary):** The subword composition step may force more attention work, strengthening the binding signal. Or the measurement point (last subtoken) may capture composition attention in addition to compound binding. Worth a paragraph and possibly a figure in the TMLR submission. Further analysis needed before making a claim.

**Methodological note:** The `find_token_index` function in `src/binding.py` was updated to handle multi-token words by concatenating adjacent subtokens and returning the last subtoken index (where the composed representation lives). Three compounds required this fix: keyboard → [Key, board], captions → [capt, ions], semantic → [Sem, antic].

---

## TMLR Submission Restructuring

### 2026-06-20 — Compound binding set aligned to prompt concepts

**Decision:** Expand the Experiment 4 binding sweep from 3 compounds (screen reader, alt text, skip link) to all two-token compound concepts tested in the elicitation experiment. Target set: screen reader, skip link, alt text, color contrast, keyboard navigation, closed captions, page title, form label, link text, focus indicator, semantic HTML (~11 compounds).

**Rationale:** The original paper tested behavioral knowledge on one set of concepts and binding on a different, smaller set. Aligning them means every concept is measured at two levels — behavioral (does the model know this?) and mechanistic (does the model structurally connect these tokens?). This is triangulation, not scope creep. It strengthens the central claim that binding is a correlate of emergence by demonstrating the relationship holds across a broader concept set, not just the three original pairs.

**Constraint:** Compounds must be two-token pairs that map cleanly to token indices in the model's vocabulary. Single-token concepts (WCAG, ARIA) and multi-word concepts need separate handling or exclusion from binding analysis.

**Source:** The 44-compound battery from thatDangCircuit is available but exceeds Paper 1's scope. The prompt-aligned set is the right middle ground — broader than the original, constrained to what the paper already tests behaviorally.

---

### 2026-06-20 — Experiment restructuring for TMLR

**Decision:** Consolidate the experiment numbering from five experiments (1, 2a, 2b, 2c, 3) to three experiments plus supplementary:

- **Experiment 1: Declarative & Evaluative Elicitation** — all prompt strategies in one experiment. Declarative completions, evaluative code review, completion (few-shot/bare), hypothesis-driven, validation, and elicitation controls (expanded concepts + bicycle). The declarative-evaluative gap emerges from the results, not from the experiment numbering.
- **Experiment 2: Entropy Analysis** — mean and last-token entropy on hypothesis prompts. Measures internal state during elicitation.
- **Experiment 3: Attention Binding** — compound binding sweep across all scales with the expanded concept set.
- **Supplementary: Perplexity** — demoted with reliability caveat (entropy replicates at r≈0.96; perplexity does not at r≈0.18). Recognition-precedes-generation finding preserved as suggestive, not central.

**Rationale:** The original numbering (1, 2a, 2b, 2c, 3) treated elicitation robustness as a sub-experiment bolted onto the evaluative finding. It's not — it's evidence that the gap is real. Consolidating all prompts into one experiment makes the gap emerge naturally from the data. The elicitation robustness results strengthen the finding instead of looking like an afterthought.

Perplexity demotion is based on blind study evidence: five of six analysts independently flagged the entropy-perplexity reliability split. The paper's core findings (threshold, gap, ARIA inverse scaling, binding) all stand on entropy and behavioral measures.

---

### 2026-06-20 — Prompt consolidation into single YAML file

**Decision:** Consolidated all prompts from four source files (declarative_prompts.yml, elicitation-robustness-prompts_completion.yml, elicitation-robustness-prompts_hypothesis.yml, elicitation-robustness-prompts_validation.yml, elicitation_control_prompts.jsonl) into one file: `data/all_prompts.yml`. Original files archived to `data/_archive/`.

**Schema:** Each prompt has: prompt_id, concept, prompt_type (declarative | evaluative | completion | hypothesis | validation | control), template_type, prompt, max_tokens.

**Rationale:** The original files used inconsistent formats (three YAML files with different schemas, one JSONL). Consolidation gives one source of truth, one schema, one file to verify. YAML chosen over JSONL for human readability — at 46 prompts, readability outweighs pipeline ergonomics.

**max_tokens standardized to 100** across all prompts (original paper used 10 for declarative, 20 for evaluative). Models that know the answer stop early; extra room captures full confabulation patterns for analysis.

**Duplicates noted:** `valid_alt_text_direct_001` duplicates `eval_alt_text_001` prompt text; `valid_aria_confab_001` duplicates `decl_aria_001`. Intentional — validation prompts confirm the pattern independently.

**Files:**
- `data/all_prompts.yml` — 46 prompts, 6 sections
- `data/_archive/` — 5 original files preserved

---

### 2026-06-20 — Runner module: src/elicitation.py

**Decision:** Created `src/elicitation.py` module with `run_all_prompts()` and `load_prompts()` functions. Follows the same pattern as other src modules (models.py, heads.py, etc.).

**Rationale:** Moves experiment execution from inline notebook cells to a reusable module. Each model run is now three lines in the notebook: import, call, display. Auto-saves per-model CSV to `results/pythia/` or `results/gpt2/` based on model name. Consistent output schema across all runs enables cross-scale analysis.

**Output schema:** prompt_id, concept, prompt_type, template_type, prompt, output, max_tokens, model

---

## Elicitation Robustness Experiment

### 2026-03-10 — Elicitation control prompts: design, execution, results

**Decision:** Added elicitation robustness check using 3 new accessibility concepts (closed captions, color contrast, page title) across 5 template types (cloze, direct_question, instruction, evaluative, scenario) with bicycle as non-accessibility control. Run on Pythia 2.8B, Pythia 1B, GPT-2-large.

**Rationale:** Pre-empts reviewer critique ("did you ask it right?"). If the declarative-evaluative gap holds across meaningfully different elicitation strategies, it rules out prompting artifacts as a confounder. Different concepts than original paper (screen reader, alt text, skip link) so this also demonstrates the gap isn't concept-specific.

**Why bicycle control:** One non-accessibility prompt per template type, same structure, neutral domain the model definitely knows. If the model can do evaluative reasoning on bicycles but not accessibility using the same template, the failure is domain knowledge depth, not template format.

**Key Results:**

Pythia 2.8B:
- Cloze/direct: ✅ Strong declarative knowledge across all concepts
- Instruction: ❌ Breaks into forum-post roleplay ("I'm a web developer and I'm trying to explain...")
- Evaluative (accessibility): ⚠️ Wrong reasons ("video not in English", "not in the same color range")
- Evaluative (bicycle): ✅ Correct ("not designed to stop")
- Scenario: ⚠️ Misses negative premises ("no title" → describes normal browsing)

Pythia 1B (predicted dead zone — confirmed):
- Evaluative (accessibility): ❌ Circular ("because of the low color contrast", "because the title is not available")
- Evaluative (bicycle): ❌ Also circular ("not safe because it is not safe to ride")
- Scenario (closed captions): ❌ Contradicts premise — says deaf user "can hear the audio"
- 1B failure is NOT domain-specific — can't do evaluative reasoning on anything

GPT-2-large (surprise finding):
- Evaluative: ❌ Nonsensical across all concepts including bicycle ("not safe because it is not a vehicle")
- Scenario: ✅ Correct for accessibility ("can't understand what is being said", "unable to distinguish between text and background")
- Likely explanation: WebText training data rich in narrative accessibility content. Scenario template pattern-matches on blog/explainer structure, not genuine evaluative reasoning
- IMPORTANT: This is a training data artifact, not evidence of understanding. Note as limitation in paper.

**Interpretation:** The declarative-evaluative gap holds across new concepts, new template types, and two architectures. Bicycle control isolates domain knowledge as the variable. 1B dead zone confirmed with convergent evidence (linear probe, fine-tuning, now elicitation all underwhelming). GPT-2-large scenario results require discussion of training data confound.

**Files:**
- `data/elicitation_control_prompts.jsonl` — 20 prompts (15 accessibility + 5 bicycle control)
- `notebooks/elicitation-robustness.ipynb` — runner notebook
- `results/elicitation_robustness_raw.csv` — raw completions

**Next steps (target: Mon-Tue 2026-03-16/17):**
- Add methods paragraph on elicitation robustness design
- Add results table to paper
- Add discussion of GPT-2-large training data artifact
- Update paper revision on Authorea/TechRxiv

---

## Figure Decisions

### 2026-03-04 — PDF/UA-2 Figure Tagging & Caption Styling Session

#### Problem
Figures completely absent from PDF tag tree. Acrobat accessibility panel skipped images entirely. No `<Figure>` elements despite `\DocumentMetadata{tagging=on}`.

#### Root Cause
Two issues:
1. Figures were in `paper/figures/` but path was unresolvable from the build context — CC discovered this by actually running the build with shell access and reading logs
2. LaTeX float machinery (`htbp` placement + `\begin{figure}` wrapping) is fundamentally incompatible with PDF/UA-2 tag tree ordering

#### Fix
1. Figures moved to `paper/sections/figures/` so paths resolve correctly
2. Added `--from markdown-implicit_figures` to build script — disables Pandoc's automatic float wrapping, images become inline `\includegraphics` only
3. Removed `\usepackage{float}` from template
4. Pandoc 3.9 automatically wires `alt=` from bracketed markdown text `![alt](path)` — no Lua filter needed for alt text

#### Caption Styling
- Captions written as plain paragraphs in markdown using `::: {.caption}` divs
- `caption-style.lua` filter converts divs to styled LaTeX
- Font: `\figurecaptionfont` (`\newfontfamily`) — named to avoid collision with `caption` package's reserved `\captionfont`
- Style: footnotesize, Atkinson Hyperlegible Mono, #767676 gray, italic
- Line height fixed by adding `\\par` inside the Lua filter block — `\linespread` and `\setlength{\baselineskip}` don't apply without a paragraph terminator

#### What We Tried That Didn't Work
- Lua filter with `\tagpdfsetup{alttext=}` — wrong key
- `alt=` on `\includegraphics` directly — graphicx not loaded when filter ran
- `\tagstructbegin/\tagstructend` wrapping — built successfully but images still untagged
- Raw LaTeX figure blocks — correct positioning but broke tagging entirely
- MacTeX update — not the issue
- `\linespread` and `\setlength{\baselineskip}` for line height — no effect without `\par`

#### Agents / Tools
- Created `lualatex-pandoc-debugger` agent in CC (Opus, all tools, project memory) — found the path issue and float fix by reading actual build logs
- Gemini assisted with the `\par` line height fix
- Key lesson: shell access + logs found in 20 minutes what we couldn't see in hours of template archaeology

#### Files Modified
- `build-paper.sh` — added `--from markdown-implicit_figures`, `--lua-filter=paper/filters/caption-style.lua`
- `paper/template.tex` — removed float package, added `\figurecaptionfont`
- `paper/filters/caption-style.lua` — created
- All five section markdown files — figures use plain `![alt](path)` syntax, captions in `::: {.caption}` divs

### 2026-03-03 — Exclude Pythia 160M from summary figure (fig-01-summary)

**Decision:** Pythia 160M is excluded from the Figure 1 summary line graph. The emergence trajectory figure runs from 410M to 6.9B.

**Rationale:** 160M's binding depth ratio (11/12 = 0.92) is visually misleading in both the normalized and z-scored versions. Layer 11 in a 12-layer model does not represent the same representational depth as layer 29 in a 32-layer model, even though the ratio looks similar. The high starting point dominates the figure and obscures the V-shape + cliff that is the actual finding. 160M is effectively a control condition — it demonstrates that very small models do not achieve emergence — and this is covered clearly in the results text. The emergence story lives in the 410M–6.9B range.

**160M is retained in:** all results tables, Experiment 4 binding persistence bar chart (fig-binding-persistence.png), and all discussion of the full Pythia suite. It is not omitted from the paper, only from this specific summary figure.

---

## Abstract Decisions

### 2026-03-03 — Rewrite abstract to lead with finding

**Decision:** Abstract rewritten to open with the north star finding rather than domain setup.

**Rationale:** Original abstract opened with "WCAG represents a specialized domain..." — context-first framing that buried the thesis. Neel Nanda's BLUF framework informed the revision. New abstract opens with sustained deep-network binding as necessary structural condition, introduces WCAG as the test domain in sentence two with explicit rationale ("we use X because Y"), and names both coined terms ("fluent wrongness", "declarative-evaluative gap") explicitly.

---

## Title Decisions

### 2026-03-03 — Final title

**Decision:** "Sustained Deep-Network Binding Is a Correlate of Accessibility Concept Emergence: Evidence from the Pythia and GPT-2 Model Suites"

**Rationale:** Finding-first structure per BLUF principle. "Is a correlate of" chosen over "predicts" (overclaims causation) and "suggests/hints at" (undersells the finding). "Correlate" is precise, defensible, and already used in the paper body. Model families named for discoverability.
