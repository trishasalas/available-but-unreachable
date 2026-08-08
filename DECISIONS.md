# DECISIONS.md

Research and methodology decisions with rationale. Pre-registrations are committed to git before any results are seen — timestamps are the evidence.

---

## D7 — Binding battery consolidated across domains (2026-08-08)

Merged accessibility, medical, legal, finance, and control compounds into a single 227-compound binding battery. Binding is a structural property of compound representation, not domain-specific. Cross-domain set enables direct comparison.

## D6 — Multi-head joint ablation (distributed-ensemble test)

### 2026-07-06 — Pre-registration (committed before any weights loaded)

**Why:** A5's null (L29/H7 causally inert, KL ≈ 1e-5) cannot distinguish "the  
mechanism is elsewhere" from "the mechanism is distributed across a set of  
heads." D6 jointly ablates an EARNED set of deep lexical heads.

**Setup (frozen):** Pythia 2.8B only, TL 2.17.0 pinned, no generation.  
Compounds: screen_reader (primary), alt_text / stock_market / semantic_html  
(robustness), bicycle wheel (negative control, screen_reader's earned set).  
Ablation = zero hook_z at the compound's word2 position; effect = KL(base ||  
ablated) at the final position.

**Set-earning rules (frozen):**

- Deep: `min_layer = 10`, top `N = 18` candidates by binding score.
- Selective: own-compound attention ≥ 0.3 AND ≥ 1.5× max other-domain score,  
under uniform template "A {w1} {w2} is".
- Sink/structural: BOS ≥ 0.5; pos-1 ≥ 0.5.

**Frozen interpretation thresholds (primary = screen_reader):**

- Full earned-lexical-set joint KL < 0.01 nats → "flat": earned set jointly  
unnecessary; A5 hardens.
- Lexical-set KL ≥ 0.1 nats → a joint lexical circuit exists.
- 0.01 ≤ KL < 0.1 → gray zone; reported as-is.
- Instrument validity gate: structural tail peak KL must exceed 10× the  
lexical-segment peak.

**Predictions:** four near-flat lexical segments (all < 0.01), rising tails,  
flat bicycle control.

**Branches (all ship):** (1) flat → distributed confirmed, scoped prose.  
(2) primary rises ≥ 0.1 → joint circuit found; reframe. (3) robustness  
compounds diverge → reported per compound. (4) tail flat → instrumentation stop.

**Outputs:** `results/pythia/pythia-2.8b-candidate-heads.csv`,  
`results/pythia/pythia-2.8b-multihead-ablation.csv`.

### 2026-07-06 — Amendment (before rerun)

First run returned an EMPTY earned set — 16/18 deep candidates flagged sink.  
Diagnosis: the unconditional sink/structural metrics conflate structural sinks  
with selective heads AT IDLE — a selective head off-target parks mass on BOS.  
**Amendment:** sink and structural measured from the compound's word2 position on  
the compound's own prompt; thresholds unchanged; all other rules unchanged.

### 2026-07-06 — Instrument-validity gate resolution

Earned lexical set {L29/H7, L27/H10} for screen_reader. Joint ablation:  
KL 0.000022 nats (< 0.01 → flat). Negative control (same duet, bicycle wheel):  
0.000032 → flat. However, instrument-validity gate fails as scoped: tail peak  
3.4× vs frozen 10×.

Resolution: same tail heads on the control prompt rose to 29× — the gate's  
spirit satisfied. The hooks demonstrably zero heads and move outputs. The  
primary's flat tail is a property of the PROMPT, not the instrument.

**Design lesson:** the 10× gate assumed structural ablations perturb ANY prompt;  
that assumption is prompt-sensitive. Future gates should evaluate on the control  
prompt by design.

### 2026-07-06 — Verdict: branch 1

**Results by compound:**

- **screen_reader:** earned set {L29/H7, L27/H10}. Joint KL **0.000022** → FLAT.
- **alt_text:** earned set {L21/H6, L10/H26, L12/H21}. Joint KL **0.000267** → FLAT.
- **stock_market:** earned set {L27/H24, L18/H14, L21/H24}. Joint KL **0.000285** → FLAT. L27/H24 ablates solo at 0.000000.
- **semantic_html:** 13-head "earned" set, joint KL **0.001471** → numerically FLAT but earned-set construct degenerated (tokenization caveat below).

**semantic_html caveat:** sentence-initial "Semantic" fragments as  
['Sem', 'antic', ' HTML', ' helps']. The binding sweep measured  
word2→FRAGMENT attention; the candidate pool was nominated by  
detokenization-flavored behavior, not pairing selectivity. Joint-ablation  
number is unaffected.

**Cross-compound observations:** zero overlap between compounds' earned sets —  
selectivity is bespoke, per-compound. No general "lexical head" role at 2.8B.

**Verdict:** branch 1. For the strongest lexical lead and three robustness  
compounds, the earned deep selective sets are jointly unnecessary (all joint  
KLs ≤ 0.00147, bar 0.01). A5 hardens from "single-head inert" to "earned set  
jointly unnecessary."

---

## D8 — Is the lens artifact frequency-shaped? (b_U-as-frequency-prior)

### 2026-07-05 — Pre-registration (committed before any weights loaded)

**Motivation (viewed data, disclosed):** in all six frozen lens-vs-truth flips  
(skip_link declarative, one per scale), the TRUE pathway elected the  
higher-frequency token. 6/6 directional, observed BEFORE this registration.

**Prior art (disclosed before weights loaded):** Kobayashi et al. (Findings of  
ACL 2023) — LM-head BIAS correlates with output token frequency in models with  
explicit head biases. Cho et al. (arXiv 2406.01468) — log-linear frequency  
encoding in output embeddings. H1's geometric half is therefore REPLICATION; D8's  
residual novelty is: (a) RELOCATION — Pythia/GPT-NeoX has no head bias; the  
prior lives in ln_final β, becoming b_U only under TL folding; (b) SEVERANCE  
CONSEQUENCE — the resid @ W_U shortcut removes exactly this term.

**Frozen predictions:**

- H1 (primary, confirmatory): Spearman ρ(b_U_i, log unigram frequency_i)  
≥ +0.3, one-sided positive, at Pythia-12B; same sign at all six scales.
- H2 (exploratory, no threshold): ρ(colsum(W_U)_i, log frequency_i) per scale.

**Frequency measurement (frozen):** primary proxy = GPT-NeoX token ID. Calibration  
= Infini-gram Pile-train string counts, n=500 single-word tokens. If proxy and  
calibration disagree in sign, report both, conclude nothing, stop.

**Branches (all ship):** (1) H1 holds → C6 gains a mechanism. (2) H1 fails →  
logged as honest negative. (3) Mixed signs → report, no story.

### 2026-07-05 — Verdict: H1 CONFIRMED

ρ(b_U, freq proxy), trimmed: 160M +0.322 · 410M +0.512 · 1B +0.543 ·  
2.8B +0.533 · 6.9B +0.535 · **12B +0.591** (frozen bar ≥ +0.3, met at every  
scale). ρ(colsum, freq proxy): |ρ| < 0.01 at all six scales — frequency-dead.

Calibration (same day, Infini-gram Pile-train, n=500, zero failures):  
ρ(b_U, log Pile count): 160M 0.664 · 410M 0.737 · 1B 0.767 · 2.8B 0.722 ·  
6.9B 0.689 · **12B 0.779** (p ≤ 6e-65 throughout). Signs agree with proxy  
everywhere — the paper says "log unigram frequency in the Pile."

The frequency prior lives in b_U specifically — the exact term the resid @ W_U  
shortcut severs — while the retained centering coefficient (colsum) is  
frequency-neutral.

### 2026-07-05 — Frozen-artifact audit: lens-rollout divergence is systematic

Whitespace-normalized diff of frozen lens-rollout chosen-token sequences  
against frozen true-pathway elicitation outputs. The lens rollout departs the  
true greedy path at EVERY scale — divergence at ~step 2–7. The 12B artifact  
(D7 verdict) was not a near-tie fluke. C6 upgrades from single-artifact caution  
to systematic finding.

**6.9B validation:** pathways agree through step 6 — 'displayed' wins Step 5 on  
the true pathway. Rank-1 claim validated by frozen artifacts alone.

---

## D7 — Single-token-ban counterfactual at Step 5

### 2026-07-04 — Pre-registration (committed before first forward pass)

**Why:** Review verdict 6.2 named the weakest link in A6: "competition at the  
decision point is the operative failure" rests on ONE trace of ONE compound. D7  
is the cheapest counterfactual that can harden it.

**Setup (frozen):** Pythia 12B, TL 2.17.0, greedy decoding. Prompt: "A skip link  
is" (declarative). Regression check FIRST: reproduce the unmodified trace before  
any intervention.

**Intervention (frozen):** logit floor to −inf for "click" and tokenization  
variants at the decision step. Two conditions: (A) ban at Step 5 only;  
(B) persistent ban.

**Pre-registered outcome branches:**

1. Correct continuation wins → token competition causally demonstrated.
2. Another incorrect token wins → the failure is a competitor NEIGHBORHOOD.
3. Degenerate output → instrumentation check before interpretation.

**Amendment (before first forward pass):** "evaluative" in the original entry  
was a drafting error; the referent was always the declarative prompt "A skip  
link is" per the step-trace cell in notebooks/mlp.ipynb.

### 2026-07-04 — Verdict: Gate 2 failed — lens-pathway artifact

- **Gate 1 PASSED:** lens pathway reproduces the frozen trace, all 15 tokens  
byte-identical; 'click' wins Step 5 under the lens.
- **Gate 2 FAILED:** true forward pass (ln_final included) elects ' a'  
(logit 16.27) at Step 5, not 'click'. 'displayed' at rank 5. Full  
continuation: "a link that is not a link. It is a link that is not" —  
byte-identical to frozen elicitation raws.
- **No intervention was run.** Gates prevented banning a competitor that  
doesn't win on the true pathway.

**Interpretation:** The A6 exhibit is a measurement artifact of the lens pathway  
(skipping ln_final flips near-tie margins). All behavioral results are  
unaffected (generated through the true pathway). 'displayed' present-but-losing  
(rank 5) survives. The named competitor ('click', frequency story at token  
level) does not.

---

## D1 — BOS diagnostic on 12B late-layer binding resurgence

### 2026-07-27 — Pre-registration

See `docs/d1-preregistration.md`.

---

## Tangent Battery Regeneration

### 2026-07-10

The intro's opening triad quoted 12B generations whose only surviving record was  
hand-transcribed prose. That transcription carried confirmed paste-wounds (12B  
screen-reader/alt-text cross-contamination). `src/logit_export.py` is now the  
authoritative source. Per (model, compound) it exports a greedy step trace and a  
decision-point top-15, plus one joined `{model}_because_generations.csv`.

Run 2026-07-10, local MPS, TL 2.17.0 pinned, float32, greedy argmax. Three  
VERIFIED prompts only (skip_link, screen_reader, alt_text). Local scales:  
pythia-160m/410m/1b/2.8b, gpt2-medium/large/xl. Pending (Colab GPU):  
pythia-6.9b, pythia-12b. Artifacts in `results/logits/{model}_*`.

Verification: `src/tangent_byte_compare.py` — 12/12 local comparisons are exact  
matches after whitespace normalization.

---

## Spearman Analysis Specification

### 2026-07-03 — Unit-of-analysis + interpretation thresholds (blind)

Authored with the coding/Spearman pipeline PAUSED. No expansion-derived output  
viewed. Frequency table remains CLOSED.

**Primary analysis:** One observation per compound per suite.

- x = log10(Infini-gram bigram count)
- y = binary accuracy, STRICT: correct=1, partial or incorrect=0. Mean across  
scales within the suite.
- Spearman ρ per suite. Pythia is confirmatory; GPT-2 is replication-under-proxy.

**Thresholds:** Predicted direction POSITIVE. ρ ≥ 0.4 → support. 0.2 ≤ ρ < 0.4  
→ weak/suggestive. ρ < 0.2 or wrong sign → thesis not supported.

**Robustness set:** Kendall's tau-b; partial Spearman controlling token count and  
word1 frequency; row-level Spearman (DESCRIPTIVE ONLY, clustered bootstrap);  
secondary y at max scale; weighted-accuracy sensitivity check.

### 2026-07-03 — CC execution: n=49 criteria coded, dual Spearman run

Gate conditions met (freeze commit 42695be; no `attention/` in results/).

Translation: 41 rows from `criteria_authoring.csv` → `code_declarative`.  
Two self-caught translation bugs fixed (tree_grid compound-token leakage;  
responsive_design substring-match error).

**Regression guard PASSED:** original coded outputs byte-identical (510 rows  
unchanged); all 20 original trajectory rows byte-identical.

**Results:**

- PRIMARY: Pythia ρ=0.57 (n=49), GPT-2 ρ=0.51 (n=49) → both SUPPORT.  
Kendall τ-b 0.43 / 0.40.
- Partial Spearman controlling word1 freq: Pythia 0.59, GPT-2 0.49. Controlling  
token count: 0.56 / 0.49. Correlation SURVIVES both controls.
- a11y-sense-only: Pythia ρ=0.86 (n=9), GPT-2 ρ=−0.21 (n=6, ns). CAVEAT:  
sense filter collapses n hard; not a robust headline.
- Row-level (descriptive): Pythia ρ=0.42 CI[0.24,0.57], GPT-2 ρ=0.39  
CI[0.20,0.54].

**Prediction scorecard (blind, scored):** Fired via predicted attractor:  
sensory_characteristics (food 4/10), redundant_entry (database 4/10),  
pointer_cancellation (C/C++ 4/10), landmark_region (geographic 7/10). Did NOT  
fire: status_message, focus_management, error_identification. tree_grid  
never_emerges both suites (0/10) — HELD. Ceiling anchors: sign_language 9/10 +  
form_field 10/10 — HELD; text_formatting 3/10 NOT held.

### 2026-07-03 — Gap-table sampling-frame partition

The declarative-evaluative GAP is a paradigm-level mean over the  
elicitation-experiment concept set (declarative over 10 concepts, evaluative  
over 5 — never a matched per-concept pair). The 41 expansion compounds are  
frequency-stratified probes carrying only the declarative arm; pooling them  
would depress the baseline BY CONSTRUCTION. `load_all_results` tags each row  
`source` in {original, expansion}; `gap_analysis` restricts only the gap pivots  
to `source=='original'`.

---

## n=49 Coding Criteria

### 2026-07-03 — Criteria authored blind

All 41 expansion-compound criteria authored in `docs/findings/criteria_authoring.csv`.  
Authored conversationally — Trisha dictated the practitioner bar per compound.  
Original 8 criteria UNTOUCHED (regression guard applies at translation).

**Blind state:** frequency table CLOSED for entire authoring window; expansion  
raws exist (tag=expansion) and remain UNVIEWED and UNCODED. Criteria precede  
data.

**Coding doctrine:**

1. LATERAL confusion (wrong mirror: AD↔captions) → INCORRECT.
2. VERTICAL confusion (instance-for-umbrella) → PARTIAL.
3. SYNONYM pairs → cross-definition nods.
4. MECHANISM-FOR-CONCEPT — severity per-row.
5. TRENCH COAT (compound restated with a modal verb) → circular → INCORRECT.

**Pre-registered predictions:** Token-competition candidates:  
sensory_characteristics (food), redundant_entry (database), status_message  
(HTTP), error_identification (debugging), pointer_cancellation (C/C++),  
landmark_region (geographic), focus_management (attention/self-help).  
never_emerges: tree_grid. Ceiling anchors: sign_language, text_formatting,  
form_field, responsive_design.

---

## B4 — Inverse scaling pre-registration

### 2026-07-02

CLAIMS.md row B4 rewritten as a blind pre-registration for the n=49 expansion:  
"inverse scaling (peak_regress) is not skip_link-specific: __ of 49 compounds  
regress from correct/partial at an intermediate scale to incorrect at maximum  
scale." Count blank left open. Established exemplar (skip_link cross-architectural  
degeneration) preserved as already-viewed evidence.

**Blind state:** expansion raws exist but are unviewed and uncoded.

---

## Results layout

### 2026-07-02

Canonical layout: raw per-model outputs at results/{suite}/ (pythia, gpt2);  
experiment-specific outputs in named dirs (frequency/, mlp_investigation/,  
logits/, analysis/). The attention/ grouping (26c6a8d) dissolved. Suite-first  
for the substrate data; experiment-first for targeted outputs.

---

## MLP Investigation and Token Competition

### 2026-06-28 — MLP magnitude hypothesis disconfirmed; token competition discovered

The MLP magnitude interference hypothesis is disconfirmed.

**Disconfirmation:** Residual stream decomposition across 1B, 6.9B, and 12B:

- Final-layer MLP spike is architectural, not compound-specific.
- MLP/attention ratios nearly identical between skip_link and color_contrast  
at both 6.9B (4.437 vs 4.444) and 12B (4.365 vs 4.888).

**Logit lens:** Zero topic-relevant tokens at ANY scale. Low-frequency domain  
knowledge is encoded distributedly — present in the residual stream but  
invisible to direct vocabulary projection.

**Token competition mechanism:**

| Scale | Step 5 chosen | "displayed" rank | Generation path |
| ----- | ------------- | ---------------- | --------------- |
| 160M  | that          | absent           | graph theory    |
| 410M  | when          | absent           | web-bypassing   |
| 1B    | used          | absent           | CS networking   |
| 2.8B  | when          | absent           | tree traversal  |
| 6.9B  | **displayed** | **rank 1**       | correct         |
| 12B   | **click**     | **rank 4**       | degenerate      |

The concept is not absent at 12B — it is outcompeted. Data in  
`results/mlp_investigation/`.

---

## TransformerLens Validation

### 2026-06-28 — TL3 generation collapse; reverted to TL2

TL3 (TransformerBridge) produces degenerate generation ("the same time the same  
time the same time"). Binding scores between TL2 and TL3 show preserved  
topology. The failure is in the generation pathway only. All TMLR experiments  
rerun on TL2.

### 2026-06-28 — TL2 validated as faithful wrapper

TL2's HookedTransformer produces behaviorally equivalent outputs to raw  
HuggingFace inference. LayerNorm folding causes numerical drift that produces  
different surface tokens but identical failure modes. Same attractor, same  
behavioral conclusion.

### 2026-06-28 — Full scaling suite rerun complete

All experiments rerun on TL2 via Colab A100. Results in `results/pythia/` and  
`results/gpt2/`. Three CSVs per model: binding, entropy, results. TL pinned.

---

## Gap Analysis Framework

### 2026-06-28 — Accuracy coding and replicable pipeline

Accuracy coding implemented as deterministic Python (`src/accuracy_coding.py`).  
Every criterion documented inline. Gap analysis (`src/gap_analysis.py`) applies  
coding to all results. Reproducible via `python -m src.gap_analysis`.

**Coding scheme:** correct (core accessibility-relevant meaning) / partial  
(right domain, misses key point) / incorrect (wrong domain, circular,  
degenerate).

**Key findings:**

| Finding                                       | Detail                                                                 |
| --------------------------------------------- | ---------------------------------------------------------------------- |
| Gap persists at all Pythia scales             | Except 12B, which closes via declarative regression                    |
| 12B gap closes via regression                 | Declarative drops 70% → 50%; skip_link and keyboard_navigation regress |
| GPT-2 gap widens with scale                   | 50 pt gap at 1.5B                                                      |
| skip_link inverse scaling cross-architectural | Both 12B Pythia and 1.5B GPT-2 produce degenerate loops                |
| ARIA: 10 models, zero correct                 | Universal failure, both architectures                                  |

### 2026-06-28 — Accuracy coding changes require a DECISIONS.md entry

Any change to `src/accuracy_coding.py` must be accompanied by an entry here  
documenting what changed and why. The coding rules determine what counts as  
"correct"; changing a rule retroactively changes every table and figure.

### 2026-06-27 — `code_completion()` added; six extended analyses

Added completion coding to `src/accuracy_coding.py`. Completion criteria are  
syntactic, not conceptual — isolates pattern-matching competence for the  
completion-paradox analysis.

Six extended analyses implemented (all read existing CSVs — no new experiments):  
entropy confidence/fluent wrongness, binding-accuracy correlation, per-concept  
scaling/trajectories, entropy divergence, degenerate detection, completion paradox.

### 2026-06-27 — All prompt types coded; 0 uncoded of 510

Added graders for validation, hypothesis, and non-bicycle control rows (330  
total). Distribution: correct 186 / partial 147 / incorrect 177. Existing  
declarative/evaluative/gap/emergence tables are unchanged (filtered by  
prompt_type).

---

## Binding Replication

### 2026-06-21 — Pythia binding: late-layer resurgence confirmed

11-compound binding data corroborates Paper 1's late-layer resurgence on 5/6  
models (Δ ≤ 1 layer). 410M outlier explained: Paper 1 measured only  
screen_reader (deepest strong = 9); expanded set finds binding at L22-23.

### 2026-06-21 — GPT-2 binding: main table exact

Screen_reader across all four GPT-2 sizes: all 12 deltas are zero. Per-compound  
variation at XL consistent with expanded uniform methodology.

### 2026-06-21 — Column label fix

"Last Layer" → "Deepest Strong Layer" to prevent misinterpretation (layer depth  
index, not head count).

---

## Experiment Structure

### 2026-06-21 — GPT-2 promoted to co-equal cross-architecture analysis

Present both families organized by finding, not as "Replication: GPT-2"  
footnotes. Divergences become discussion points about training data effects.

### 2026-06-21 — Subword tokenization natural experiment

Subword-split compounds show consistently higher mean binding than clean  
compounds at 2.8B+ (0.329 vs 0.278). Unexpected. Preliminary — further analysis  
needed before any claim.

### 2026-06-20 — Compound binding set expanded

Expanded from 3 compounds (screen reader, alt text, skip link) to all two-token  
compound concepts tested in elicitation (~11 compounds). Aligns behavioral and  
mechanistic measurement.

### 2026-06-20 — Experiment restructuring for TMLR

Consolidated from five experiments (1, 2a, 2b, 2c, 3) to three plus  
supplementary. Perplexity demoted (entropy replicates r ≈ 0.96; perplexity  
r ≈ 0.18).

### 2026-06-20 — Prompt consolidation

All prompts consolidated into `data/all_prompts.yml` (46 prompts, 6 sections).  
Originals archived to `data/_archive/`.

### 2026-06-20 — Runner module: src/elicitation.py

Experiment execution moved from inline notebook cells to `src/elicitation.py`.  
Auto-saves per-model CSV to `results/{suite}/`.

---

## Elicitation Robustness

### 2026-03-10 — Design, execution, results

Elicitation robustness check: 3 new concepts × 5 template types + bicycle  
control. Run on Pythia 2.8B, 1B, GPT-2-large.

Key results: declarative-evaluative gap holds across new concepts, templates,  
and architectures. Bicycle control isolates domain knowledge as the variable.  
1B dead zone confirmed. GPT-2-large scenario results show a training data  
confound (WebText narrative content, not evaluative reasoning).

---

## Figure Decisions

### 2026-03-04 — PDF/UA-2 figure tagging

Figures moved to `paper/sections/figures/`; `--from markdown-implicit_figures`  
disables float wrapping; Pandoc 3.9 wires alt text from `![alt](path)`  
automatically. Caption styling via `caption-style.lua`.

### 2026-03-03 — Exclude Pythia 160M from summary figure

160M excluded from the emergence trajectory figure (runs 410M to 6.9B). 160M's  
binding depth ratio (11/12 = 0.92) is misleading — effectively a control  
condition. Retained in all tables and other analyses.
