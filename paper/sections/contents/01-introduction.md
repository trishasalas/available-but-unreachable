## Introduction

Rewrite the intro

### New sections

01-introduction.md
02-the-gap.md
03-ruling-out-binding.md
04-the-trajectory-taxonomy.md
05-what-predicts-trajectory.md
06-entropy-fluent-wrongness.md
07-related-work.md
08-discussion.md
09-limitations.md
10-references.md
11-colophon.md

### Notes

Results are in the named sections. Each section is "here's what we did and here's what we found." That's a legitimate structure for interpretability papers — interleaved method and result per investigation rather than all methods then all results.

---

What's NOT accounted for yet:

- `docs/cc-extended-gap-analysis.md` — haven't read it, might fit in the gap or discussion
- `docs/results-significance.md` — probably discussion or limitations
- `docs/binding-reframe-draft.md` — probably folds into the binding section
- `_analysis/Pythia.xlsx` and the visual analysis xlsx — your working spreadsheets
- `results/analysis/emergence_thresholds.csv` — could go in the gap section or trajectory taxonomy


### New work needed before you can write:

- Infini-gram runs (Section 5)
- Token competition traces beyond skip_link (Section 5)
- Figures for everything


### SUGGESTION: Opening example from tangent.ipynb

Three evaluative prompts, same structure, same model (Pythia 12B), three completely different failure modes:

- screen_reader (32,100 bigrams): "it does not have a text alternative" — correct
- skip_link (662 bigrams): 404 error page — confidently wrong
- div/onclick (no compound): "not in the same document" — fluently wrong from a different domain

This is the hook. Reader immediately sees the phenomenon and wants to know why. Then: "The answer turns out to be a single number — how often the compound appears in the training corpus."

Could also use the logit ranking at the decision point as a second beat: the correct answer (' users') was right there at rank 12. It didn't win.
