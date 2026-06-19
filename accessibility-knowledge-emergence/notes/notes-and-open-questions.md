# Open Questions & Notes

## Attention Binding

### 160M Layer 11 Head 8 — perfect score of 1.0
"reader" attends to "screen" exclusively at this head, but 160M cannot correctly define screen reader. Two competing interpretations:
1. **Proximity hypothesis** — the head is responding to token adjacency, not concept recognition. The model has no higher-level context to distribute attention to so it collapses onto the nearest token.
2. **Binding precedes semantics** — mechanistic binding of the compound term exists before semantic understanding of the concept emerges.

**Potential probe:** Test whether the same head shows strong binding for other adjacent compound terms that 160M also fails to define. If yes, supports proximity hypothesis. If selective to "screen reader," more interesting.

**For paper:** Lead with the conservative interpretation (proximity effects cannot be ruled out) rather than overclaiming.

---

### Full five-model binding comparison — RESOLVED
All five models analyzed. Key findings now in results.md:
- Early layers (0-3) dominate across all models (70-91% of strong binding)
- Strong head count scales with model size: 10, 22, 11, 25, 37
- Last strong layer tracks behavioral emergence: drops off at L6-11 below threshold, persists to L29-30 at 2.8B and 6.9B
- 2.8B inflection point: 3.6x jump in total heads above threshold vs 1B
- 1B is architectural outlier (8 heads, 16 layers) — counts not directly comparable

**Remaining open question:** Whether early-layer binding at small scales (especially 160M L11H8 score=1.0) reflects genuine compound representation or proximity effects. Cannot be resolved from attention weights alone — noted as limitation in results.

---

### CSV threshold notes
- 0.1 = noise floor, above background but not meaningful on its own
- 0.2-0.5 = moderate, worth noting in context
- 0.5+ = strong, meaningful binding
- 1.0 = exclusive attention, "reader" attending to "screen" only

When analyzing CSVs, count of heads above 0.5 is more meaningful than total count above 0.1 threshold.

---

## Declarative Results

### Newline as data point
"Semantic HTML helps" and "Captions are used for" trigger newline mid-completion across model sizes. Suggests document template pattern-matching rather than semantic knowledge — the model knows the document shape these terms appear in (lists, definitions) without knowing the accessibility meaning. Clean illustration of the declarative/evaluative gap showing up in generation behavior itself.

### ARIA hallucination trajectory
Each model wrong in a completely different way, getting more elaborately wrong with scale:
- 160M: "the first time in the history of the country" (gibberish)
- 410M: "the acronym for the acronym for" (loops)
- 1B: "Artificial Replacement of a Human Being" (wrong expansion)
- 2.8B: "A Rational Approach to Information and Automation" (wrong expansion)
- 6.9B: "Association of Research Libraries in Africa" (wrong expansion, confident)

Confidence increases with scale, accuracy does not. More fluent confabulation, not correct recall. Distinct phenomenon from "doesn't know" — worth its own sentence in results.

### Non-monotonic behavior
Screen reader: 2.8B says "reads aloud" (correct), 6.9B drops "aloud" (regresses).
Skip link: correct at 2.8B, wrong at 6.9B.
Perplexity: 2.8B prefers correct by 4x, 6.9B by 3x — larger model slightly less certain.
Capability near emergence thresholds is unstable, not strictly linear with scale.

---

## Evaluative Results

### img prompt fails across all models
Every model fails to identify missing alt attribute even when question explicitly asks what is missing. Model that can define alt text cannot identify a missing one. Strongest illustration of declarative/evaluative gap.

### "Click here" is the only evaluative success
Works at 2.8B and 6.9B. Ambiguous link text may be more common as a named anti-pattern in training data than missing alt attributes.

### div onclick trajectory
Responses become more specific with scale without arriving at correct answer:
- 160M: loops
- 410M: "not a valid HTML element"
- 1B: "not a `<span>` element"
- 2.8B: "not in the same document"
- 6.9B: "not a form control"

Trajectory toward correct answer (keyboard inaccessibility, missing role/tabindex) without arriving.

---

## Future Writing Ideas

- Visual explainer: vectors vs tensors vs embeddings — 1D vs 2D vs 3D with actual pictures. Target audience: accessibility/web folks coming to ML from outside. Good blog post angle.

---

## Reproducibility
160M results confirmed consistent across two runs. Perplexity values match to 4 decimal places.
