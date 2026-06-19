# Paper 1: Testing Accessibility Knowledge Across Pythia Model Sizes

**Status:** Published  
**Published:** January 18, 2026  
**Post:** https://trishasalas.com/posts/testing-accessibility-knowledge-across-pythia-model-sizes/  
**Code:** https://github.com/trishasalas/mech-interp-research  
**Cited by:** Dung et al. (2026) — extends the 2.8B threshold finding using attention binding as a predictive signal

## Summary

Behavioral emergence study using the Pythia model suite (160M–6.9B) and
TransformerLens. Mapped when accessibility concepts (screen reader, alt text,
skip link, WCAG, ARIA) become accessible to model outputs across scale.

**Key findings:**
- Screen reader, skip link, alt text emerge at 2.8B
- WCAG emerges at 6.9B; ARIA never emerges
- Recognition precedes generation (perplexity flip at 410M→1B)
- Emergence is non-monotonic — skip link regressed at 6.9B
- Attention binding of "screen reader" as compound concept appears across multiple layers

## What this paper leaves open

- *Why* 2.8B? Behavioral threshold established but not mechanistically explained.
- Is accessibility knowledge geometrically present in smaller models before
  the behavioral flip? (→ Paper 2)
- How is the knowledge actually stored in models that succeed? (→ Paper 3)
