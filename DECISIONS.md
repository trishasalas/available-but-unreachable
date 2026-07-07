# DECISIONS.md
Research and figure decisions with rationale.

---

## Replication Verification Against Paper 1

### 2026-07-07 — D9 graduation condition RATIFIED: independent pre-registration required; no inheritance from B5's lineage

**Rule:** if D9 (Socratic failure-state flip, +0.74 @ 1B → −0.38 @ 2.8B,
last-token − mean entropy under Socratic elicitation) is ever promoted
from PRELIM to claim-strength — in this paper or a successor — it
requires its **own pre-registration from scratch**. It may not ride in
on B5's lineage or cite B5's audit trail as its provenance.

**Rationale:** D9 and B5 are different constructs. B5 measures
wrongness-confidence (entropy of incorrect-on-a11y vs
correct-on-control); D9 measures elicitation-format failure states
(Paper 1's "internal structure"). The B5 provenance hunt (2026-07-06)
established that D9's numbers had drifted INTO B5's row in memory
transit — the corrected B5 row and D9's re-homing are the record of
that separation. Letting D9 later graduate on B5's paperwork would
re-merge what the audit just disentangled.

**Path to claim-strength (already sketched in D9's CLAIMS row, restated
here as the minimum bar):** new pre-registration; extension to six
scales on TL2 entropy CSVs under deterministic coding; frozen
thresholds before any run. Post-submission errand, D1-sized.

**Provenance:** flagged by CC at session close 2026-07-06 (sectioning
pass, commits 103bf81 / 27decdf / e4b325c); entry drafted by Fable
(claude.ai); RATIFIED by Trisha in-thread 2026-07-07 ("approval here
is sufficient").

---

### 2026-07-06 — D6 VERDICT: distributed-ensemble loophole CLOSED — earned deep selective sets are jointly unnecessary at all four compounds (branch 1, with per-compound gate accounting and one earned-set-construct caveat)

**Mechanical record (run 2026-07-06, local MPS, TL 2.17.0 pinned, float32,
no generation, amended on-target operationalization, outputs
results/pythia/pythia-2.8b-candidate-heads.csv +
pythia-2.8b-multihead-ablation.csv):**

- **screen_reader (primary):** earned set **{L29/H7, L27/H10}** — L27/H10's
  first on-target measurement clears both filters (generic BOS 0.82 was
  idle-parking). Joint KL **0.000022** (< 0.01 → FLAT). Negative control
  (same duet, bicycle wheel): 0.000032, flat. Gate fired (tail 3.4× vs
  frozen 10×); resolved same day via control-prompt evidence (29×) +
  session sanity asserts — instrument VALID (ratified resolution above).
- **alt_text:** earned set **{L21/H6, L10/H26, L12/H21}**. Joint KL
  **0.000267** → FLAT. Gate fired (~1×, tail below lexical peak); resolved
  per-compound under the ratified clause (same instrument evidence).
- **stock_market:** earned set **{L27/H24, L18/H14, L21/H24}**. Joint KL
  **0.000285** → FLAT. Tail rose to 0.001665 (5.8× — fired, resolved;
  liveliest tail of the panel, largely self-evidencing). Notable: L27/H24,
  the strongest selective binder for this compound, ablates solo at
  **0.000000** — the sharpest representation-without-necessity datum in the
  program. Cross-validation of the amendment: screen_reader's L27/H10
  appears in THIS compound's candidates and is correctly refiled as sink
  on-target (no screen-reader work here → BOS parking) — same head, two
  prompts, two correct filings.
- **semantic_html (branch-3 divergence; reported per-compound, no
  smoothing):** 13-head "earned" set, joint KL **0.001471** → numerically
  FLAT (7× under bar) but the earned-set construct degenerated here — see
  caveat. No excluded sink/structural candidates → empty tail → gate
  VACUOUS (instrument aliveness self-evidenced: the curve rises 300×
  across its own segment).

**semantic_html caveat (cause identified — tokenization):** the natural
prompt "Semantic HTML helps" fragments sentence-initial word1:
['Sem', 'antic', ' HTML', ' helps']. The frozen binding sweep therefore
measured word2→FRAGMENT attention; the candidate pool was nominated
largely by detokenization-flavored behavior (fragment-mending recruits
broadly), not pairing selectivity — explaining the anomalous 13-head
"lexical" set and the binding_score/own_score column spread (uniform
template "A semantic HTML is" tokenizes CLEAN; the two columns measured
different token geometries). RESIDUAL, logged not interpreted:
own_scores on the clean template are also near-universally high
(0.99/0.96/0.91…) — ' HTML' token-register peculiarity and genuine
corpus breadth of the bigram both remain candidates; saved question.
The joint-ablation NUMBER is unaffected (whatever these 13 heads are,
deleting them jointly costs 0.00147 nats). Downstream flag: the frozen
binding CSV's semantic_html rows inherit the fragment-geometry caveat;
claims pass to confirm nothing shipped leans on them (expected: nothing
does — A-claims are screen_reader/L29H7-scoped).

**Cross-compound observations (descriptive, not pre-registered):** zero
overlap between compounds' earned lexical sets — selectivity is bespoke,
per-compound; no general "lexical head" role exists at 2.8B. Tail/sink
personnel ARE shared across prompts (e.g., L25/H2 in two tails):
general-purpose plumbing, compound-specific representation.

**Verdict:** branch 1. The distributed-ensemble loophole in Limitations
is closed in scoped form: for the strongest lexical lead in the program
(screen reader) and three robustness compounds, the earned deep
selective sets — the only deep heads exhibiting pairing-selective
attention — are **jointly unnecessary** (all joint KLs ≤ 0.00147,
frozen bar 0.01). A5 hardens from "single-head inert" to "earned set
jointly unnecessary." The Limitations paragraph shrinks to the metric
caveat plus the semantic_html construct caveat. Paper language stays
scoped: "the strongest lexical lead is distributed" — never the
unscoped claim.

**Design lessons (named, for future specs):** (1) validity gates of the
10× form must be evaluated on the control prompt by design — the
structural-ablations-perturb-any-prompt assumption is prompt-sensitive
(per the ratified gate resolution). (2) Natural prompts must not open
with the compound: sentence-initial word1 changes token identity; Stage 0
of any future compound design includes a tokenization assert. (3) Ratio
selectivity tests assume sparse own-score distributions; add an
absolute-crowding check (e.g., flag when > half the candidate pool passes)
so degeneracy announces itself.

**RATIFY/VETO: Trisha, 2026-07-06: RATIFY**

---

### 2026-07-06 — D6 PRE-REGISTERED: multi-head joint ablation (the distributed-ensemble test; commit before any weights are loaded)

**GATE-4 RESOLUTION 2026-07-06 (instrument-validity gate fired on the
primary; check performed; instrument ruled VALID; result stands with
caveat):** amended rerun (local, MPS) earned lexical set {L29/H7, L27/H10}
for screen_reader — L27/H10's first on-target measurement clears both
filters; its generic BOS 0.82 was idle-parking, same as L29/H7's. Joint
ablation of the full earned set: **KL 0.000022 nats** (< 0.01 frozen bar →
flat). Negative control (same duet on bicycle wheel): 0.000032 → flat.
BOTH frozen result criteria pass. However the instrument-validity gate
FAILS AS SCOPED on the primary: tail peak 0.000074 vs lexical peak
0.000022 = **3.4×** (frozen: ≥ 10×). Branch-4 stop declared; panel paused
before alt_text.

**Instrumentation check (evidence, all from the same session):** (1)
sanity asserts passed — empty-set identity KL == 0, plural == singular on
L29/H7, late-layer 8-head set moved KL; (2) the IDENTICAL tail heads,
same hooks, same code path, on the control prompt rose 0.000041 →
0.000940 peak = **29×** its lexical peak — the gate's spirit satisfied on
the adjacent prompt. Conclusion: the hooks demonstrably zero heads and
demonstrably move outputs. The primary's flat tail is a property of the
PROMPT, not the instrument: on "A screen reader is ___" (baseline top
token ' a', p = 0.51) the next-token prediction is insensitive to the
entire deep attention neighborhood at the `reader` position — selective
duet AND true sinks alike.

**Verdict under the resolution:** primary result STANDS — the earned deep
selective set is exactly {L29/H7, L27/H10} and it is jointly unnecessary
(0.000022). A5 hardens as pre-registered. Caveat travels with the claim:
the validity gate was satisfied via the control prompt, not the primary.
**Lesson (design debt, named):** the 10× gate silently assumed structural
ablations perturb ANY prompt; that assumption is prompt-sensitive. Future
gates of this shape should be evaluated on the control prompt by design.
Panel continuation: remaining compounds run under the same gate,
resolved per-compound by the same check if it fires again.

**Observation, logged NOT interpreted (speculation, explicitly outside
the registration):** the immovable prediction is a maximally
high-frequency token; possible connection to D8's b_U frequency prior
(the anchor lives in the unembedding, not in these heads). Parked as a
saved question; no claim ships from this line.

**GATE-RESOLUTION RATIFY/VETO + commit before panel resumes: Trisha,
2026-07-06: RATIFIED**

**AMENDED 2026-07-06 (instrumentation stop; before any lexical-segment data
exists):** first screen_reader run returned an EMPTY earned set — 16/18 deep
candidates flagged sink, including BOTH selectivity-passing heads (L29/H7,
BOS 0.9117; L27/H10, BOS 0.8186). Branch-4 stop declared before
interpretation. Diagnosis: the unconditional sink/structural metrics
(generic-prompt BOS ≥ 0.5, pos-1 ≥ 0.5) conflate structural sinks with
selective heads AT IDLE — a selective head off-target has nowhere to put its
mass and parks on BOS; the parking is the selectivity's shadow. The frozen
April characterization (docs/findings/The one genuine lexical head.md)
measured ON-TARGET: at the `reader` position L29/H7 routes 0.90 to "screen",
0.0001 to pos-1 — "not BOS, not position-1." **Amendment restores that
original operationalization rather than inventing a new rule:** sink and
structural are measured from the compound's word2 position on the compound's
own prompt; thresholds (0.5 / 0.5) unchanged; all other rules, thresholds,
predictions, and branches unchanged.
**Viewed-data disclosure:** the aborted run exposed structural-TAIL cumulative
curves only — screen_reader tail peak 0.000587, bicycle control tail peak
0.000728 (superseded rows; upsert replaces on rerun). No lexical-segment KL
exists anywhere; the lexical-segment predictions remain blind. Tail
membership changes under the amendment (L29/H7 exits the tail), so viewed
tail values do not leak the gate outcome.
**AMENDMENT RATIFY/VETO + commit before rerun: Trisha, 2026-07-06: RATIFIED**

**Why:** A5's null (L29/H7 causally inert, KL ≈ 1e-5) cannot distinguish "the
mechanism is elsewhere" from "the mechanism is distributed across a set of
heads" — the loophole conceded in the Limitations draft. D6 jointly ablates an
EARNED set of deep lexical heads. If even screen reader — the strongest
single-head binding of the 11 compounds — is distributed, weaker compounds are
distributed a fortiori. Design approved 2026-06-29
(`docs/superpowers/specs/2026-06-29-multihead-lexical-ablation-design.md`);
instrument committed e7a5e4b (`src/qk_ov.py` plural ablation + cumulative
curve; `src/d6_multihead_ablation.py`; `notebooks/d6-multihead-ablation.ipynb`)
BEFORE this entry and before any run — gates in history before any result
existed.

**Setup (frozen):** Pythia 2.8B only, TL 2.17.0 pinned, no generation.
Compounds: screen_reader (primary), alt_text / stock_market / semantic_html
(robustness), bicycle wheel (negative control, screen_reader's earned set).
Ablation = zero hook_z at the compound's word2 position; effect = KL(base ||
ablated) at the final position.

**Stage A set-earning rules (frozen; spec definition verbatim — deep ∧
selective ∧ ¬(sink ∨ structural)):**
- Deep: `min_layer = 10`, top `N = 18` candidates by binding score.
- Selective: own-compound attention ≥ **0.3** AND ≥ **1.5×** the max
  other-domain score, under the UNIFORM template "A {w1} {w2} is" (C1: natural
  prompts confound position with content). Calibration point: L29/H7 = 0.90 vs
  0.21 clears this easily.
- Sink/structural: existing thresholds (BOS ≥ 0.5; pos-1 ≥ 0.5). Head-type
  battery columns recorded but NOT a membership filter.
- stock_market is not in the frozen 11-compound sweep: its Stage A runs a fresh
  in-memory `run_single_compound` pass (same math, one forward pass);
  `binding_source` column records provenance per compound.
- Excluded sink/structural candidates (≤ 5, binding desc) are appended as the
  labeled **positive-control tail** of the cumulative curve.

**Frozen interpretation thresholds (primary = screen_reader):**
- Full earned-lexical-set joint KL **< 0.01 nats** → "flat": the set is
  jointly unnecessary; A5 hardens from "single-head inert" to "earned set
  jointly unnecessary"; the Limitations paragraph shrinks to the metric caveat.
- Lexical-set KL **≥ 0.1 nats** → a joint lexical circuit exists; A4/A5
  reframe; ships as a positive finding, not a failure.
- **0.01 ≤ KL < 0.1** → gray zone; reported as-is, no story.
- **Instrument validity gate:** the structural tail's peak KL must exceed
  **10×** the lexical-segment peak. If the tail does not rise, instrumentation
  check BEFORE any interpretation (branch-3 discipline, per D7). The empty-set
  identity (KL == 0) and plural==singular regression asserts must pass first
  (`sanity_check`).
- Negative control: screen_reader's earned set on "A bicycle wheel is" at
  `wheel` expected < 0.01 nats (flat).

**Predictions (falsifiable, made blind):** four near-flat lexical segments
(all < 0.01), rising tails, flat bicycle control. [Fable placement; Trisha may
re-weight before ratifying.]

**Branches (all ship):** (1) flat everywhere → distributed confirmed, scoped
prose only ("the strongest lexical lead is distributed," never the unscoped
claim). (2) primary rises ≥ 0.1 → joint circuit found; A4/A5 reframe. (3)
robustness compounds diverge from the primary → reported per compound, no
smoothing. (4) tail flat → instrumentation stop.

**Outputs:** `results/pythia/pythia-2.8b-candidate-heads.csv`,
`results/pythia/pythia-2.8b-multihead-ablation.csv` (upsert-by-compound; reruns
replace, never duplicate). Figure from CSV via `generate-figures/` per repo
convention.

**RATIFY/VETO + commit before loading weights: Trisha, 2026-07-06: RATIFY**

---

### 2026-07-05 — D8 VERDICT: H1 CONFIRMED under the frozen proxy — b_U is frequency-ordered at all six scales; colsum is NOT — the prior localizes to exactly the severed term; calibration pending (API 403)

**Mechanical record (run 2026-07-05, TL 2.17.0, float32, weights-only,
seed-42 protocol, outputs results/d8_frequency_prior/):**
ρ(b_U, freq proxy), trimmed: 160M +0.322 · 410M +0.512 · 1B +0.543 ·
2.8B +0.533 · 6.9B +0.535 · **12B +0.591** (frozen bar: ≥ +0.3 at 12B,
same sign all scales — met at every scale individually; full-vocab and
trimmed variants agree to ~0.01). ρ(colsum, freq proxy): |ρ| < 0.01 at
all six scales — frequency-dead.

**Verdict:** H1 CONFIRMED under the frozen token-ID proxy. H2's null is
the dissociation that sharpens the mechanism: the frequency prior lives
in b_U specifically — the exact term the resid @ W_U shortcut severs —
while the retained centering coefficient (colsum) is frequency-neutral.
End-to-end chain now measured: bias-free GPT-NeoX parks the unigram prior
in ln_final β → TL folding relocates it into b_U → the shortcut amputates
exactly that term → thin-margin elections lose their frequency voter →
the 6/6 anti-frequency flip direction (2026-07-05 audit). Kobayashi et
al. (2023) replicated and RELOCATED into an architecture with no explicit
head bias; severance casualty documented. C6 gains its mechanism.

**Calibration incomplete (honesty clause):** Infini-gram returned 403
after ~80 calls/scale (rate-limit signature); partial count CSVs on disk
lack b_U values (instrument flaw — patched same day: per-row b_U
recorded, inter-call sleep, per-call backoff-and-continue). The frozen
sign-disagreement rule COULD NOT FIRE. H1 therefore stands as
PROXY-CONFIRMED; the paper does not say "log unigram frequency" until an
independent calibration lands (small scales suffice; local-machine
retry).

**Observations (not pre-registered, logged not interpreted):** ρ rises
with scale (0.32 → 0.59); 160M b_U norm anomalously large (5,647 vs
18–65 at all other scales) and weakest correlation — 160M/410M oddity
file grows. d_vocab padding differs by scale (50304/50432/50688),
expected.

**CALIBRATION COMPLETE (same day, ~13:00 CDT):** Infini-gram Pile-train
counts, n=500/500 (fresh cache, 1 qps, zero failures, offline-first
instrument). ρ(b_U, log Pile count): 160M 0.664 · 410M 0.737 · 1B 0.767 ·
2.8B 0.722 · 6.9B 0.689 · **12B 0.779** (p ≤ 6e-65 throughout; 12B
p = 4e-103). **Signs agree with the proxy at all six scales — the frozen
sign-disagreement rule does NOT fire.** H1 upgrades from proxy-confirmed
to CONFIRMED: the paper may say "log unigram frequency in the Pile."
Calibration ρ exceeds proxy ρ everywhere (proxy was the conservative
floor — full-vocab noise). Observation, logged not interpreted: 160M
jumps 0.32→0.66 proxy→calibration, suggesting its disorder (and giant
norm) concentrates in non-word vocab regions. Artifacts:
results/d8_frequency_prior/d8_calibration_summary.md +
data/infini_gram_calibration_counts.csv (committed cache — no one
re-asks these questions).

**RATIFY/VETO + calibration-retry decision: Trisha, 2026-07-06: RATIFY**

---

### 2026-07-05 — D8 PRE-REGISTERED: is the lens artifact frequency-shaped? (b_U-as-frequency-prior hypothesis; commit before any weights are loaded)

**AMENDED 2026-07-05, before any weights loaded (prior-art disclosure;
predictions unchanged):** post-registration literature search found
Kobayashi et al. (Findings of ACL 2023, "Transformer language models
handle word frequency in prediction head") — LM-head BIAS correlates with
output token frequency in models with explicit head biases — and Cho et
al. (arXiv 2406.01468) — log-linear frequency encoding in a common sparse
direction of output embeddings, causally steerable, emerges very early in
Pythia training. H1's geometric half is therefore REPLICATION, not
discovery, and its prior rises accordingly. D8's residual novelty
narrows to: (a) RELOCATION — Pythia/GPT-NeoX has no head bias; if H1
holds, the prior lives in ln_final β, becoming b_U only under TL folding;
(b) SEVERANCE CONSEQUENCE — the resid @ W_U shortcut removes exactly this
term, connecting Kobayashi/Cho's geometry to Belrose et al.'s
"systematically biased toward some vocabulary items" and to our six-scale
rollout divergence (2026-07-05 audit, below). Full citation shelf added to
paper/sections/contents/10-references.md same morning. Gates, thresholds,
frequency protocol, and seal status unchanged.

**Motivation (viewed data, disclosed):** in all six frozen lens-vs-truth
flips (skip_link declarative, one per scale), the TRUE pathway elected the
higher-frequency token and the naked lens elected the rarer one — 6/6
directional, observed 2026-07-05 morning BEFORE this registration. That
observation motivated this entry and is NOT part of the confirmatory test.

**Mechanism under test:** with TL2 fold_ln, the naked lens (resid @ W_U)
omits two argmax-relevant terms: (1) the centering nudge, mean(resid) ×
colsum(W_U) per token; (2) the folded unembed bias b_U = β_ln_final · W_U —
a context-independent per-token logit offset, the only architectural home
for a static unigram prior. Hypothesis: the model parks (part of) its
frequency prior in b_U; the naked lens therefore systematically under-ranks
frequent tokens at thin margins.

**Frozen predictions:**
- H1 (primary, confirmatory): Spearman ρ(b_U_i, log unigram frequency_i)
  ≥ +0.3, one-sided positive, at Pythia-12B; same sign at all six scales.
- H2 (exploratory, no threshold): sign and magnitude of
  ρ(colsum(W_U)_i, log frequency_i) reported per scale; no prediction.
- H3 (held observational): the 6/6 flip direction stands as motivating
  observation only; any confirmatory flip-direction test requires NEW
  lens rollouts on new prompts under a further registration.

**Frequency measurement (frozen):** primary proxy = GPT-NeoX token ID
(BPE merge order ≈ frequency rank), full vocab, free. Calibration subset =
Infini-gram Pile-train string counts on a sample of n=500 single tokens
that are standalone words (alphabetic, leading space), stratified by
token-ID decile; Llama-2 tokenizer caveat logged (string-level counts,
not NeoX-token-level). If proxy and calibration disagree in sign, report
both, conclude nothing, stop.

**Compute & scope:** weights-only — extract b_U and colsum(W_U) per scale
(all six), no generation, no forward passes; Colab or local. The sealed
`d7_step5_ranks_preban.csv` is NOT opened (H1/H2 do not require margins).

**Branches (all ship):** (1) H1 holds → the C6 methods finding gains a
mechanism: the naked lens amputates the frequency prior; the lens artifact
and the paper's phenomenon share a channel (Discussion, clearly bounded —
this strengthens C6, NOT A3; corpus-level causality unmoved). (2) H1 fails
→ the 6/6 direction seeks another explanation (centering term, or
coincidence at n=6); logged as honest negative. (3) Mixed signs across
scales → report, no story.

**RATIFY/VETO + commit before loading weights: Trisha, 2026-07-05: RATIFY**

---

### 2026-07-05 — Frozen-artifact audit: lens-rollout divergence is SYSTEMATIC across all six scales; 6.9B Step-5 'displayed' VALIDATED without GPU

**Method (no new data generated):** whitespace-normalized diff of the frozen
lens-rollout chosen-token sequences
(`results/mlp_investigation/pythia/*_skip_link_steps.csv`, autoregressive
resid_post @ W_U) against the frozen true-pathway elicitation outputs
(`results/pythia/*-results.csv`, skip_link declarative). Both artifact sets
from the 2026-06-28 TL2 rerun; pathway is the differing variable.

**Result:** the lens rollout departs the true greedy path at EVERY scale —
divergence at ~step 2 (160M), 4 (410M), 7 (1B), 4 (2.8B), 7 (6.9B), 5 (12B).
The 12B artifact (D7 verdict, below) was not a near-tie fluke: autoregressive
lens rollouts exit the true trajectory within ≤7 steps, presumably at the
first thin margin, after which every downstream token describes a fictional
sentence (the rollout compounds its own artifact). Notable: the lens rollout
made 2.8B look WORSE than reality (lens: tree-traversal fiction; truth:
"used to skip a section of a web page" — nearly correct), and 410M's true
output is a proto-loop ("not part of the main page. A skip link is a link
that is not part...") — the degenerate attractor has a developmental
trajectory the lens traces obscured.

**6.9B validation:** pathways AGREE through step 6 ("a link that is not
displayed in") — 'displayed' wins Step 5 on the true pathway at 6.9B.
Rank-1 claim validated by frozen artifacts alone; no forward-check run
needed. Honest cross-scale decision-point contrast: 6.9B elects 'displayed'
(validated 2026-07-05) vs 12B elects ' a' / degenerate loop, 'displayed'
rank 5 (D7 Gate 2).

**Consequences:** C6 upgrades from single-artifact caution to systematic
finding. Distinction preserved: autoregressive lens ROLLOUTS fabricate
trajectories; single-step lens readouts at true-pathway-generated contexts
carry a lesser, distinct caveat. All multi-step content in the
mlp_investigation steps CSVs inherits the generation-claim caveat.
CLAIMS A2/C6 rows updated same morning.

**RATIFY/VETO: Trisha, 2026-07-05: RATIFY**

---

### 2026-07-04 — D7 VERDICT: Gate 2 failed — the Step-5 click-vs-displayed election is a lens-pathway artifact; no intervention run; A6 exhibit requires reframing

**Mechanical record (run 2026-07-05T00:25 UTC = 2026-07-04 19:25 CDT, Colab A100, TL 2.17.0,
float32, `src/d7_token_ban.py`; artifacts in results/logits/ pending
download from the session):**
- Ban list enumerated and recorded before any generation:
  'click'=9738, ' click'=5532, 'Click'=7146, ' Click'=15682 (all
  single-token, asserted).
- **Gate 1 PASSED:** the lens pathway (resid_post @ W_U, no ln_final —
  the original cell's exact computation) reproduces the frozen trace,
  all 15 chosen tokens byte-identical, 'click' wins Step 5 under the lens.
  The artifact is reproducible.
- **Gate 2 FAILED:** the true forward pass (ln_final included) elects
  ' a' (logit 16.27) at Step 5, not ' click'. 'displayed' sits at rank 5
  pre-ban on the true pathway. Full true-pathway continuation: "a link
  that is not a link. It is a link that is not" — verified byte-identical
  (first 15 steps) against the frozen elicitation raw
  (results/pythia/pythia-12b-results.csv, skip_link declarative).
  Two independent harnesses agree; instrumentation EXONERATED per
  branch 3 before any interpretation.
- **No intervention was run.** The gates prevented banning a competitor
  that does not win on the true pathway.

**Interpretation (RATIFY/VETO — Trisha, morning of 2026-07-05):**
1. The A6 exhibit (click rank 1 / displayed rank 4 at 12B Step 5) is a
   measurement artifact of the lens pathway: skipping ln_final's
   centering flips near-tie margins. The A6 provenance caveat
   (2026-07-04, below) anticipated exactly this fork; Gate 2 resolved it
   to the disagreement branch.
2. UNAFFECTED: all behavioral results (elicitation coding, inverse
   scaling, gap tables, both Spearman analyses) — generated through the
   true pathway throughout; Gate 2 independently re-derived the 12B
   degenerate output.
3. "Present but outcompeted" survives in modified form: 'displayed' is
   rank 5 at the true decision point. What wins is not a high-frequency
   web token but the degenerate self-reference continuation (' a' →
   "a link"). The exhibit's mechanism sentence ("'click', a
   higher-frequency web token, overtakes") does NOT survive and must not
   ship; the step-by-step table (2026-06-28 entry) must not become a
   figure as-is. CLAIMS.md B4's pointer to "A2's Step-5 trace as the
   mechanism exhibit" needs corresponding correction.
4. D7 as pre-registered is MOOT on the true pathway (its premise — ban
   the Step-5 winner 'click' — dissolved). Verdict 6.1 stands: A3 keeps
   "predicts"; no causal language is earned. Any follow-up (true-pathway
   competitor characterization; whether 6.9B's lens trace agrees with
   its true pathway, which its elicitation output suggests it does; a
   ban experiment targeting the actual degenerate attractor) is a NEW
   pre-registration, not an extension.
5. Shippable as a finding: the correction itself — the paper catches its
   own exhibit via a pre-registered gate before a reviewer could. Candidate
   framing: measurement-pathway sensitivity at near-tie decision points as
   a caution for logit-lens-adjacent generation claims.

---

### 2026-07-04 — A6 exhibit provenance caveat (disclosure; no semantics changed) + tangent.md paste artifact

**Disclosure:** the frozen Step-5 trace was computed via `resid_post @ W_U`,
skipping `ln_final` — a logit-lens-flavored pathway, not the model's true
output distribution (skip_link step-trace cell, notebooks/mlp.ipynb). The
behavioral basin matches elicitation results; ranks and margins could shift
under the standard forward pass. D7's Gate 2 tests exactly this: agreement
retroactively strengthens the exhibit (robust across unembedding pathways —
free sentence for the paper); disagreement is a branch-3 instrumentation stop.
This caveat attaches to the A6 exhibit regardless of D7's outcome.

**Related disclosure (tangent.md):** the GPT-2 XL screen_reader step-trace
block in tangent.md is a paste-duplicate of the skip_link top-15 table
(hand-paste artifact; header reads "rank" where every other step table reads
"step"). tangent.md was recovered from trash 2026-07-04 and restored to the
vault (`20 Research/tmlr/results`); preserved as-is with this note. Any
promotion of its data to paper evidence requires mechanical regeneration via
`src/logit_export.py` — which would also, at last, populate `results/logits/`
alongside D7's outputs.

---

### 2026-07-04 — Post-review closeout computations (cc-followups items 1–4); scorecard "fired" found non-mechanical

**What:** Ran the four ratified closeout items over frozen artifacts
(`src/closeout_followups.py`; pipeline commit ca0319e, worksheet 42695be) —
NOT new experiments, no criteria touched, primary pipeline untouched. Frozen
12-row strictness counts and the primary ρ (Pythia 0.5715 / GPT-2 0.5052)
reproduced exactly as guards. Deliverables: `criteria_strictness_audit_full.csv`
(41 rows), `scorecard_base_rate.csv`, `spearman_pmi_robustness.csv`, and
`docs/findings/closeout-followups-2026-07-04.md`.

**Results:** (1) Strictness across the full worksheet: markers 3–6, mean 3.80;
predicted-fail 4.1 vs anchors 3.5 vs an unflagged field also spanning 3–5 — no
gradient by predicted class; footnote may say "across the full worksheet."
(3) Ceiling anchors: sign_language + form_field held; **text_formatting and
responsive_design failed to ceiling** despite top-of-range frequency — reported
as evidence against a pure-frequency account (rubric 4.3), same font as the
hits. (4) PMI robustness: association tells the same story as raw exposure in
Pythia (0.51 vs 0.57) but attenuates below the 0.4 line in GPT-2 (PMI 0.36 vs
raw 0.51) — raw corpus exposure is the more robust predictor; divergence
reportable, not a problem.

**Surprising surface (why this entry exists):** Item 2's base rate cannot use
the scorecard's own "fired" definition. The scorecard scored "fired" as an
OUTPUT-LEVEL content event — the compound's *specific predicted foreign domain*
surfaced (food, database, C/C++, geographic) — which is not reproducible from
any frozen CSV and is not any accuracy/trajectory threshold: landmark_region
(fired) and focus_management (not-fired) have identical strict accuracy. So the
mechanical base rate is built on the pre-registered SHAPE signature
(never_emerges): 18/41 both-suites, 28/41 either. The 7 candidates never-emerge
at 3/7 both (≈ base rate) and 6/7 either (modestly above). Reading: the SHAPE
signature is at the field base rate for these compounds; the CONTENT signature
(predicted attractor) is what discriminates but is establishable only by output
inspection. never_emerges is therefore a conservative CEILING on chance-firing,
so the attractor-level 4/7 is more informative than this denominator implies.
Reported two-tiered in the findings doc. **Trisha's call** whether the paper
reports the never_emerges base rate, commissions output-level attractor coding
for a true content-signature null, or cites 4/7 with the ceiling caveat. No
criteria semantics changed.

**RATIFIED (Trisha, 2026-07-04): option (c).** The paper cites 4/7 with the
ceiling caveat, both axes named — "fired" is an output-level content judgment
(predicted foreign domain surfaced); no mechanical base rate exists for it;
never_emerges (18/41) reported as a conservative ceiling on chance-firing.
Option (b) — output-level attractor coding across all 41 — is RETAINED as an
optional census, energy permitting this weekend: it doubles as the two-tier
headcount (lexicalized-but-outcompeted vs compositional-fallback, per the
6.3 framing) and D7's extension shortlist. If run: coding rule written down
BEFORE reading outputs, labeled post-hoc-operationalized. If not run, the
paper is complete on (c) alone.

---

### 2026-07-04 — D7 pre-registered: single-token-ban counterfactual at the Step 5 decision point (BLIND to outcome; commit before first forward pass)

**AMENDED 2026-07-04, before first forward pass (RATIFIED: Trisha, 2026-07-04):**
"evaluative" below was a drafting error by the entry's author (Fable 5,
original thread — confirmed by same, 2026-07-04); the referent was always the
frozen Step-5 trace, prompt **"A skip link is"** (declarative), per the
skip_link step-trace cell in notebooks/mlp.ipynb (the cell writing
`{model}_skip_link_steps.csv`) and
`results/mlp_investigation/pythia/pythia-12b_skip_link_steps.csv`. The
recovered tangent.md (evaluative "because" traces, six models; restored from
trash 2026-07-04 to vault `20 Research/tmlr/results`) confirms the evaluative
prompt has no Step-5 election and lands in a different attractor at 12B
(error-page frame) — the two prompts probe different failure surfaces. All
gates, conditions, branches, and scope unchanged. Original wording below left
intact per amend-don't-reinterpret. Execution: `src/d7_token_ban.py`
(gates enforced in code; ban list recorded before any generation).

**Why:** Review verdict 6.2 (spearman-review-verdicts-2026-07-03.md) named the
weakest link in the A6 chain: "competition at the decision point is the
operative failure" rests on ONE observational trace of ONE compound. D7 is the
cheapest counterfactual that can harden it: remove the competitor, watch
whether the knowledge surfaces. Verdict 6.1 stands regardless — A3 keeps
"predicts" in the abstract; a positive D7 earns CAUSAL language scoped to the
token level only ("token competition is causally decisive at this decision
point"), not corpus level (that remains OLMo/Paper-2 territory).

**Setup (frozen):**
- Model: Pythia 12B, TransformerLens 2.17.0 (pinned), greedy decoding
- Prompt: the original skip_link evaluative prompt from the Step 5 trace
  (exact prompt per logit_export provenance — same string, byte-identical)
- Regression check FIRST: reproduce the unmodified trace; confirm "click"
  still wins Step 5 under TL2 before any intervention. No reproduction,
  no experiment.

**Intervention (frozen):**
- Mechanism: logit floor to −inf for banned tokens at the decision step
- Ban list: "click" AND tokenization variants: " click", "Click", " Click"
  (BPE side-door rule — competitor must not re-enter via casing/whitespace).
  Variants enumerated from the tokenizer BEFORE running; list recorded in
  the results entry verbatim.
- Two pre-declared conditions:
  - **A (single-step ban):** ban applies at Step 5 only; generation
    continues unconstrained after
  - **B (persistent ban):** ban applies at Step 5 and all subsequent steps
  - Rationale: A tests whether the competitor's win is decisive once;
    B tests whether it re-wins later. Divergence between A and B is itself
    reportable (competitor persistence).

**Scope (frozen — the anti-scope-creep fence):**
- PRIMARY: skip_link only. This is the causal demonstration.
- PRE-DECLARED EXTENSIONS (run only if the session has room; not required
  for the primary claim): 2–3 compounds from the fired token-competition
  candidates per the prediction scorecard, same protocol, competitor
  token(s) identified from each compound's own Step-trace before banning.
  Extensions are generalization evidence, labeled as such.
- Anything beyond this list is a NEW pre-registration, not an extension.

**Pre-registered outcome branches (all ship):**
1. A correct continuation ("displayed" or practitioner-equivalent) wins the
   banned election AND the full completion codes correct under the frozen
   criteria → token competition causally demonstrated at the decision
   point. A6's final arrow hardens; Discussion gains the scoped causal
   paragraph. [PREDICTED BRANCH — Fable placement; Trisha may re-weight]
2. Another incorrect token wins (next gate-crasher in line) and the
   completion remains incorrect → the failure is a competitor
   NEIGHBORHOOD, not a single token — the prior swamps the signal in
   depth. Ships as its own finding; arguably strengthens the
   frequency-swamping account while weakening single-token framing.
3. Degenerate or incoherent output → instrumentation check (harness, hook
   placement, TL version confirm) BEFORE any interpretation. Not a
   finding until instrumentation is exonerated.

**Success criterion for "correct completion":** the frozen coding criteria
(criteria_authoring.csv, commit 42695be) applied to the generated text —
same practitioner bar as the elicitation experiment, no ad-hoc judging.

**Ceremony:** this entry commits BEFORE the first forward pass
(`pre-register D7 token-ban counterfactual`). Results + verdict paragraph
land in DECISIONS the same session, whichever branch fires.

---

### 2026-07-03 — CC execution: n=49 criteria translated, coded, dual Spearman (amended spec) run

**Decision:** Executed the CC brief (criteria-handoff-2026-07-03.md) after the
criteria-freeze commit (42695be) and the amended Spearman spec. Gate conditions
met before any downstream run: freeze commit present; S8 verified (no
`attention/` in results/).

**Translation (41 rows → `code_declarative`):** faithful mechanical translation
of `criteria_authoring.csv`. `correct` requires the worksheet's *distinguishing*
markers (so circular / trench-coat restatements fall through to `incorrect`
exactly as the original 8 do — doctrine plank 5 without a separate detector);
worksheet `incorrect_markers` traps became negative guards. Doctrine block
(5 planks, verbatim) encoded at the top of the expansion section.
**Two self-caught translation bugs fixed** (both were compound-token leakage,
caught via the prediction scorecard, not the worksheet):
  1. `tree_grid` counted the echoed token `tree` as a hierarchy marker →
     "a grid of trees" passed as correct. Fixed: correct now requires the
     table-half (`table`/`columns`, not the echoed `grid`) AND real hierarchy
     (`expand`/`collapse`/`hierarch`). Now 0/10 correct — matches its
     never_emerges prediction.
  2. `responsive_design` used `respond`, which does not substring-match the
     echoed `responsive`, wrongly rejecting "responsive to the screen" /
     "any device". Fixed to key on the screen/device content. 3/10 → 5/10.
No rows were returned to Trisha untranslated — every worksheet row had concrete
marker tokens.

**Sense recording (Option A + dual analysis):** `observe_sense(concept, output)`
→ {a11y, generic}, a11y iff any GLOBAL marker (screen reader; assistive; WCAG;
announce; blind; low vision; keyboard-only; ARIA; alt text) OR any per-compound
`a11y_sense_markers` appears.

**S5 (captions naming) RESOLVED:** the coverage map's worst case did not
materialize — actual data has 0 declarative `closed captions` rows (only 50
control, handled by `code_control`); the declarative captions data lives under
concept `captions` (handled). Closed the DANGEROUS CELL defensively with a
`closed captions` declarative alias (no-op on current data). Coverage CSV
corrected (n_declarative 1→0 for closed captions) and the two MUTANT rows +
two VERIFY rows (link text → 'click here' branch; form label → input type=text
branch) marked OK.

**Regression guard (non-negotiable) PASSED:** original coded outputs
byte-identical before/after (510 rows, correct 186 / partial 147 / incorrect
177 unchanged); all 20 original `per_concept_trajectories.csv` rows byte-
identical (0 diffs) after the n=49 rerun (82 new rows added). By construction
the translation only *adds* dict keys and empties the PENDING guard.

**Dual Spearman — AMENDED SPEC (compound-level; frozen freq table, no
Infini-gram re-query).** Primary = one obs/compound/suite, x=log10(bigram),
y=mean-across-scales STRICT binary accuracy (correct=1; partial|incorrect=0).
Results (packaged to `results/frequency/` for Fable review per the rubric;
raw bigram counts NOT surfaced):
  - PRIMARY all-rows: Pythia ρ=0.57 (n=49), GPT-2 ρ=0.51 (n=49) → both clear
    SUPPORT (≥0.4). Kendall τ-b 0.43 / 0.40.
  - a11y-sense-only: Pythia ρ=0.86 (n=9), GPT-2 ρ=−0.21 (n=6, ns).
    **CAVEAT (flagged for review):** the sense filter collapses n hard because
    declarative cloze answers rarely emit explicit a11y tokens; survivors are
    lexically biased toward concepts whose names contain a11y terms, and GPT-2
    is degenerate (near-constant class). Not a robust headline; the all-rows
    primary is the confirmatory read.
  - Partial Spearman (word1-confound review anchor): controlling word1 unigram
    freq, Pythia ρ 0.57→0.59, GPT-2 0.51→0.49; controlling token count,
    0.57→0.56 / 0.51→0.49. The correlation SURVIVES both controls — not a
    word1 / tokenization artifact.
  - Secondary (max-scale) and weighted-y sensitivity both ≥0.45, consistent.
  - Row-level (descriptive only; clustered bootstrap, no naive p): Pythia
    ρ=0.42 CI[0.24,0.57], GPT-2 ρ=0.39 CI[0.20,0.54].

**Audits:** (6) criteria-strictness vs predicted class ρ=−0.43 (p=0.16, n=12) —
predicted-fail compounds carry marginally more incorrect_markers (4.1 vs 3.5),
non-significant and plausibly innocent (attractor-rich compounds naturally
document more traps); reported for disclosure. (7) trajectory-class stability:
only **20/102** classes survive a single one-level flip of the most influential
response — trajectory classes are fragile, which VINDICATES the amended spec's
move to compound-level continuous accuracy as the primary unit.

**Prediction scorecard (blind pre-registration, scored):** token-competition
candidates that FIRED via their predicted attractor: sensory_characteristics
(food 4/10), redundant_entry (database 4/10), pointer_cancellation (C/C++ 4/10),
landmark_region (geographic 7/10) — all 0–1/10 correct. Did NOT fire:
status_message (0/10 HTTP/social), focus_management (0/10 attention/self-help),
error_identification (1/10 debugging). tree_grid never_emerges both suites
(0/10) — HELD. Ceiling anchors: sign_language 9/10 + form_field 10/10 (monotonic
both) HELD; responsive_design 5/10 (monotonic both) moderate; text_formatting
3/10 (mixed/never) NOT held — vague filler answers. AD↔captions substitution:
weak (2/10). Full scorecard packaged to Fable.

**New code:** `src/dual_spearman.py` (amended-spec pipeline). `load_trajectories`
in `src/frequency.py` gained a concept→compound fallback (the 41 new concepts
mapped to NaN and silently dropped the merge to n=8). Deliverables routed to
Fable per `docs/findings/spearman-review-rubric-2026-07-03.md`; frequency table
stays closed to Trisha until the review lands.

### 2026-07-03 — Gap-table sampling-frame partition (methodology rule, pre-results)

**Decision (Trisha ratified 2026-07-03):** the declarative-evaluative GAP is a
paradigm-level mean over the elicitation-experiment concept set (declarative
over 10 concepts, evaluative over 5 — never a matched per-concept pair). The 41
n=49 expansion compounds are frequency-stratified probes carrying only the
declarative arm and deliberately spanning rare never-emerges compounds; pooling
them into the declarative paradigm mean would depress the baseline BY
CONSTRUCTION of the sampling frame and shrink the gap — a sampling-frame
artifact, independent of Paper 1.

**Rule:** `load_all_results` tags each row `source` in {original, expansion} (by
filename); `gap_analysis` restricts ONLY the declarative/evaluative/gap pivots
to `source=='original'`, while the trajectory, per-concept scaling, emergence,
completion, and frequency analyses read the full n=49. The elicitation-
experiment gap stays on its own sampling frame; the frequency probes stay in the
frequency analysis where their sampling purpose fits. Decided on the STRUCTURE
of the problem (one-armed probes in a two-arm mean), not on any correlation
result. Byte-identical-pivot verification is logged with the execution commit.

---

### 2026-07-03 — Spearman unit-of-analysis + interpretation thresholds pre-registered (blind; CC pipeline paused)

**Blind state:** Authored with CC's coding/Spearman pipeline PAUSED mid-flight.
No expansion-derived output (coded rows, trajectories, correlations) has been
viewed by Trisha or by Fable 5. Frequency table remains CLOSED to Trisha.
This entry freezes the analysis unit and interpretation rules before any
result is seen. Honest-timestamp note: authored after pipeline start but
prior to any viewing — weaker than before-execution, stronger than post hoc.
Commit before CC resumes.

**Problem:** The handoff spec said "dual Spearman (frequency vs accuracy:
all rows AND a11y-sense-only)" without declaring the unit of analysis.
Row-level observations (compound × scale × suite) are pseudo-replicates:
each compound carries ONE frequency value repeated across ~6–10 rows,
inflating effective n and invalidating naive p-values even where ρ is real.

**Decision (primary analysis):** One observation per compound per suite.
- x = log10(Infini-gram bigram count), from the existing frequency table —
  no new lookups, no unblinding.
- y = binary accuracy, STRICT: correct=1, partial or incorrect=0. Mean of
  the binary across scales within the suite. RATIFIED by Trisha 2026-07-03
  (superseding Fable's initial 0.5-weighted placement): the practitioner
  bar is binary — a vertical-confusion answer does not half-work in
  practice — and strict binary carries no arbitrary weight parameter.
  Explicitly rejected now, not post hoc: lenient binarization
  (correct-or-partial=1).
- Spearman ρ reported separately per suite. Pythia (Pile = actual training
  corpus) is the confirmatory test; GPT-2 (WebText unindexed; Pile counts
  are a proxy corpus) is replication-under-proxy and the paper labels it so.
- The dual sense split (all responses / a11y-sense-only) applies at this
  compound level: recompute y from sense-filtered rows.

**Pre-registered direction and thresholds (primary analysis, per suite):**
- Predicted direction: POSITIVE (higher compound corpus frequency → higher
  accuracy).
- ρ ≥ 0.4 → support for the frequency thesis. 0.2 ≤ ρ < 0.4 → weak/
  suggestive; paper hedges. ρ < 0.2 or wrong sign → thesis not supported at
  compound-frequency level; ships as a negative, with the token-competition
  trace (A2) standing on its own evidence.

**Robustness set (supplementary, all pre-declared):**
1. Kendall's tau-b alongside ρ (tie-robust).
2. Partial Spearman controlling (a) compound token count and (b) word1
   unigram frequency [unigram counts already exist in the frequency table
   via the PMI/S4 column — no new collection]. If frequency does not
   survive the partials, report as tokenization/word1 capture — a shippable
   alternative finding, not a failure.
3. Row-level Spearman retained as DESCRIPTIVE ONLY; CI via clustered
   bootstrap over compounds (≥1000 resamples). No naive row-level p-value
   is reported anywhere.
4. Secondary y: accuracy at maximum scale (the "where it ends up" reading).
5. Weighted-accuracy sensitivity check: recompute the primary with
   y = mean of correct=1 / partial=0.5 / incorrect=0. DESCRIPTIVE ONLY —
   thresholds gate on the strict-binary primary alone. Pre-declared
   rationale: strict binary can zero-inflate y if many expansion compounds
   are never_emerges (tied zeros weaken ρ; tau-b partially covers this).
   If compounds flat at zero under strict binary are ordered under partial
   weighting, the partial codes carry the frequency signal — reported as a
   finding, not smoothed over.

**Two audit checks added to CC's deliverables (cheap, pre-declared):**
- Criteria-strictness vs prediction check: correlate a crude strictness
  proxy (count of incorrect_markers per row in criteria_authoring.csv)
  with predicted trajectory class; report the value either way. Defuses the
  "criteria tuned to fulfill predictions" objection.
- Trajectory-class stability: per compound, does the assigned class survive
  flipping the single most influential response code one level (adjacent
  code only)? Report count stable / total.

**Review gate:** Packaged results go to Fable for review per the rubric
committed blind at `docs/findings/spearman-review-rubric-2026-07-03.md`
before 2026-07-07; the rubric falls to Opus 4.6 unchanged if the clock
loses.

**Provenance:** unit-of-analysis issue raised by Fable 5 (claude.ai) in
program review 2026-07-03; semantics pending Trisha's ratification/veto
before the freeze commit. CC's handoff amended by addendum in
`docs/findings/criteria-handoff-2026-07-03.md`.

---

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
