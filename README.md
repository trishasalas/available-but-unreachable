# How Models Think
## A research series on accessibility knowledge in language models

**Author:** Trisha Salas  
**Series question:** How do language models acquire, represent, and store
domain-specific accessibility knowledge — and what does that tell us about
the limits and possibilities of AI-powered accessibility tooling?

---

## The Papers

### [Paper 1: Accessibility Knowledge Emergence: Behavioral and Mechanistic Evidence from the Pythia and GPT-2 Model Suites](./paper-1-emergence/)
*Published January 2026*

Behavioral emergence study. When do accessibility concepts (screen reader,
alt text, WCAG, ARIA) become accessible to model outputs? Answer: 2.8B
parameters for most concepts, never for ARIA. Recognition precedes generation.
Code: [mech-interp-research](https://github.com/trishasalas/mech-interp-research)

### Papers 2 and 3
*In progress*

---

## Repository Structure

```
how-models-think/
├── src/                    ← shared analysis library
│   ├── models.py           ← model loading, ModelInfo, memory management
│   ├── logit_lens.py       ← logit lens analysis
│   ├── decompose.py        ← MLP vs attention decomposition
│   ├── heads.py            ← attention head analysis
│   ├── viz.py              ← visualization utilities
│   ├── perplexity.py       ← perplexity / recognition probing
│   └── probe.py            ← linear probing (in progress)
├── paper-1-emergence/      ← published, code in mech-interp-research
├── paper-2-probing/        ← in progress
├── paper-3-mechanistic/    ← in progress
└── notes/
    ├── DECISIONS.md        ← architectural decisions with rationale
    └── OBSERVATIONS.md     ← experimental findings and hypotheses
```

---

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt with attribution.

---

## Note on repo history

*February 2026: Restructured as multi-paper series. Shared `src/` library extracted from notebook code.*
