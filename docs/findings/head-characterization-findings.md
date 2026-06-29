# What are the top binding heads *doing*? — Pythia-2.8B head characterization

Session findings, 2026-06-28. Companion to
`notebooks/what-are-they-doing.ipynb` and `src/head_characterization.py`.
Results CSVs: `results/pythia/pythia-2.8b-head-characterization.csv`,
`results/pythia/pythia-2.8b-collocation.csv`.

Framing note: this is a claim about **model internals** — what kind of attention
computation the compound-"binding" metric actually measures. Accessibility
compounds are the test set, not the subject.

## Question

The blind-study analysts hypothesized the top compound-binding heads were
**induction heads**. The 2026-06-14 Colab session reported an induction test that
appeared to falsify this — but on re-examination it was run on the **wrong heads**
(see below). This session re-tests the hypothesis properly on the `tmlr` data,
with the head set **derived from the binding CSV** rather than hardcoded.

## Method

`src/head_characterization.py`:
- `get_top_binding_heads(csv)` — derives top heads per compound from the binding
  sweep (never hardcoded; indices are architecture-specific).
- `characterize_heads(model, heads)` — induction / previous-token / duplicate-token
  scores from a single repeated-random-sequence forward pass.
- `attention_to_bos(model, heads)` — mean attention to position 0 (BOS), the
  attention-sink diagnostic.
- `collocation_scan(model, heads, template=...)` — word2→word1 attention across
  five domains; `template` forces a uniform frame to remove prompt-position confounds.

## Results

### 1. The 2026-06-14 Pythia numbers were measured on GPT-2's heads (corrected)

`CAPTURE.md` recorded a Pythia-2.8B induction test on `L15/H19, L12/H21, L13/H20`.
Those are **GPT-2 XL's** top binding heads, carried over by mistake. In Pythia-2.8B
they have ~zero binding (below the 0.1 floor; absent from the binding CSV). Pythia's
actual top binders are different and must be derived per model. The "not induction"
conclusion survives, but the recorded cross-architecture evidence did not.

### 2. Not induction heads (this time on the right heads)

Max induction score across all derived Pythia-2.8B top heads = **0.0201** (induction
heads score ≥ 0.5). Confirmed, cross-architecture, on correctly-derived heads.

### 3. The dominant "binder" is a previous-token head

`L1/H12` is the top binder for **7 of 11 compounds** (mean binding 0.96) — and scores
**previous-token = 0.886**. Its high binding score is a **positional artifact**: in a
two-token compound, word2 is always adjacent to word1, so any previous-token head
"binds" every compound. This is the Pythia analog of the GPT-2 XL finding.

### 4. The late-layer "uncharacterized" heads are mostly attention sinks + structure

The five late heads that scored near-zero on induction/prev/dup were **not** a novel
type. The raw attention dump shows:

| Head | What it actually attends to |
|------|------------------------------|
| L29/H7  | BOS sink by default — **except a genuine `reader`→`screen` binding (0.90)** |
| L30/H29 | BOS sink; sparse high scores track word position, not concept |
| L10/H16 | BOS sink; `focus indicator` is the one strong hit |
| L28/H15 | BOS sink; finance-leaning sparse hits (hedge fund, stock market) |
| L27/H24 | **position-1 head** — attends to the `A`/`The` token, not a binder at all |

"Uncharacterized" was a label for *not-yet-tested*, not *novel*. The BOS-sink and
position-1 tests named most of them.

### 5. The binding metric is contaminated at late layers (methodological — CONFIRMED)

Two artifacts inflate late-layer binding scores, both now confirmed quantitatively:

- **Attention sinks**: `attention_to_bos` shows **5 of 6** late heads park most of
  their mass on BOS — L29/H7 0.91, L28/H15 0.81, L10/H16 0.74, L30/H29 0.72,
  L10/H14 0.55. A sink head reads near-zero on every content metric yet leaks signal
  into the binding score. (L27/H24 is the lone non-sink at 0.004 — it's the
  position-1 head instead.)
- **Prompt position**: under the natural template `L27/H24` scored `due process`
  0.98, `color contrast` 0.87, `case law` 0.63. Under a **uniform template**
  ("A {w1} {w2} is") those collapse to **0.006 / 0.14 / 0.016** — the head attends to
  **position 1** (the `A`/`The`), so it only scored high when word1 landed there.
  Lesson: cross-domain binding comparisons must hold the template fixed.

Each sink head also carries a sparse set of **lexical carve-outs** — specific
compounds it binds despite the sink default (L29/H7→"screen reader", L28/H15→"hedge
fund"/"stock market", L30/H29→"skip link"/"bicycle wheel"). These are idiosyncratic,
cut across domains, and are **not** collocation-strength-based (L30/H29's #2 hit is
the weak-collocation control "bicycle wheel" at 0.78). So they are sink heads with
memorized token-pair exceptions, not collocation detectors and not a11y-specific.

### 6. The one genuine lead — RESOLVED: representation without function

`L29/H7`'s `reader`→`screen` = 0.90 is real and highly selective: it attends to the
actual content token (not BOS, not position 1), only for "screen reader" (next
compound 0.21, rest <0.08), and the weight-based QK is ~0 (the lock is built through
the layers, not in the embeddings). So the QK circuit genuinely locks onto this pair.

**But the head is causally inert.** Zero-ablating its output at the `reader` position
changes the model's next-token prediction for "A screen reader is ___" by
`KL = 1e-05` — distributions identical to 4 decimals, including the screen-reader-
relevant ` software` at rank 3. The OV write (proper DLA) suppresses "screen" and
promotes a "fire/shoot/photographers" cluster — a "screen" word-sense direction, not
accessibility semantics, and functionally dead given the null ablation.

**Conclusion:** the single most "screen reader–specific" head in the network is a
*redundant representation*, not a retrieval mechanism — the single-head echo of
thatDangCircuit's distributed/redundant result. Representation ≠ necessity, even here.
(Investigated in `notebooks/lexical-head-l29h7.ipynb` via `src/qk_ov.py`;
raw numbers in `results/lexical-head-results.md`.)

## Implications

- The compound-"binding" signal at the top heads is largely **mundane**:
  previous-token adjacency (early), attention-sink + positional structure (late).
  It is **not** induction and **not** a concept-specific circuit.
- This *strengthens* the program's thesis ("the mechanism is domain-general;
  accessibility is the lens"): no head owns accessibility; a11y compounds are handled
  by the same machinery as finance/legal/medical compounds — and much of the apparent
  binding is metric artifact, not representation.
- For the paper: report the binding metric's late-layer artifacts as a limitation,
  and separate the early-layer positional contribution from any genuine lexical heads.

## Next steps

- [x] Rerun collocation with `template="A {w1} {w2} is"` (uniform) + the
      `attention_to_bos` column → **done; both artifacts confirmed** (see §5).
- [x] QK/OV decomposition of `L29/H7` → **done; resolved as inert representation**
      (selective QK, null ablation KL=1e-05). See §6.
- [x] Update `docs/CAPTURE.md` with the GPT-2-head carryover correction.
- [ ] Optional: head-type battery across the Pythia family (160M–12B) for the
      cross-scale picture.
- [ ] Optional rigor on L29/H7: mean-ablation (vs zero) and effect at the `reader`
      position (vs final) — both expected to confirm the null result.
- [ ] Optional (bigger): Pile co-occurrence frequency vs carve-out strength.

Full raw session transcript (noisy, all tool calls):
`~/.claude/projects/-Users-trishasalas-Repos-Research/9405e8f6-c03a-4b2d-8553-a8b8eda5fce3.jsonl`
