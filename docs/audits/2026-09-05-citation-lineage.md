# Citation and lineage audit — 2026-09-05

Status: proposed changes prepared; no authoritative paper files changed in this pass. Author approval required for prose and citation conversion package.

## Verified corrections

- The live blog displays January 2026 and includes definitions, evaluative code prompts, recognition-versus-generation, and a “Looking Inside: Attention Patterns” section. It is not behavioral-only. Source: https://trishasalas.com/writing/notes/testing-accessibility-knowledge-pythia/ . The old `/blog/research/` route redirects to this canonical URL. The live date is not an independent archival verification of every revision.
- Zenodo parent DOI 10.5281/zenodo.20360787 resolves through its API to version 10.5281/zenodo.20360788, published 2026-05-23. Title: Accessibility Concept Emergence in the Pythia Suite: Thresholds, Binding, and the Declarative-Evaluative Gap. Metadata describes both attention binding across depth and the behavioral gap, including Pythia and GPT-2. The current parent DOI is retained as requested, with version DOI in the proposed reference note. Source: https://zenodo.org/api/records/20360787 . PDF content was not fetched; the scope statement is supported by the author's public record description.
- Khanh-Dung Tran is the correct name. OpenReview's indexed published PDF title page and the author's public repository agree. The full OpenReview page/PDF fetch was challenged, so metric details were checked against the author's accepted LaTeX source: https://github.com/RayoHQ/attention-binding-a11y/blob/main/main.tex , lines 257–285. EB* is the maximum across layers of the strongest within-term attention head minus the layer's mean within-term attention. It does not include value-write norms or residual normalization. The source also reports checkpoint dynamics, few-shot experiments, and ablations. Do not imply that cross-architecture attention analysis or ablation in this domain begins with this manuscript.
- Dai author given names: Lu Dai, Ziyang Rao, Yili Wang, Hanqing Wang, Hao Liu, Hui Xiong. Five entries were incorrect in references.bib. Source: https://arxiv.org/abs/2607.08393 . Existing summary of the Knowing-Using Gap is consistent with its abstract.
- Basu author corrections: Namrata Elamaran, Aakriti Kinra, John Morgan. Source: https://arxiv.org/abs/2603.18353 . Existing summary of the four interventions is consistent with its abstract.

## Methodological support to add

- Jain and Wallace (2019): https://aclanthology.org/N19-1357/ — attention weights and importance need not agree.
- Serrano and Smith (2019): https://aclanthology.org/P19-1282/ — magnitude is an imperfect indicator of effect under intervention.
- Ferrando, Gállego, and Costa-jussà (2022): https://aclanthology.org/2022.emnlp-main.595/ — ALTI includes multi-head attention, residual connections, and layer normalization in its attention-block attribution.
- Michel, Levy, and Neubig (2019): https://papers.neurips.cc/paper_files/paper/2019/hash/2c601ad9d2ff9bc8b282670cdd54f69f-Abstract.html — head removal/pruning can preserve performance in the tested systems.

## Citation-system preparation

`docs/reviews/2026-09-05-citations/` contains the proposed prose, a proposed full bibliography, and the existing-citation replacement map. These are review artifacts, not a competing canonical manuscript.

All 24 proposed BibTeX entries compile with the repository's tmlr.bst without warnings in a temporary standalone bibliography check. This checks syntax and style compatibility, not every bibliographic field or in-text reference. It used all entries only for validation. The final paper must not retain nocite-all.

After approval: apply approved prose; replace typed citations with @keys; add missing references; remove nocite-all; let BibTeX assign Salas year suffixes; verify that only cited references appear; inspect the rebuilt reference pages. References.md is excluded from the build and should be synchronized as a human-readable source list or explicitly marked as such. Do not mark the citation-system TODO complete before that end-to-end check.

The proposed narrative reports the specific combination of paired validation, cross-family frequency analysis, value-weighted late-layer measurement, and the registered frequency-selected held-out test. It does not claim a new exhaustive priority search or inherit earlier papers' stronger causal interpretations.

## Revised proposal

The pending proposal now concentrates attribution in Related Work, gives the blog and preprint third-person credit for behavioral and attention analyses, and limits Tran to one factual sentence identifying EB* and the scope of that study. Introduction and Frequency proposals state the present contribution without repeating the lineage. Official TMLR author guidance and FAQ were checked for anonymous submission/supplement and named-version link requirements. Paper files remain unchanged pending approval.

## Application and validation

Author approved the revised proposal on 2026-09-05. Applied to the authoritative manuscript. The final compiled bibliography has exactly the 23 unique keys cited in the document; no nocite wildcard, missing entry, or extra printed entry remains. Salas preprint and blog resolve to 2026a and 2026b respectively; Tran is cited once in main text. Final build has no citation warnings or overfull boxes. PDF Author metadata is empty. The 24-entry source bibliography retains the uncited thatDangCircuit reference without printing it. The reference Markdown is regenerated as an inventory of the 23 cited entries. Full source-content, novelty, and submission-package anonymity checks remain pending.

Rendered inspection: reviewed the 14-page overview and the Related Work and reference pages at page scale. Citation labels, accents, links, and reference wrapping render legibly. Existing table splitting and figure/caption pagination remain part of the separate appendix/layout work; this is not final submission-layout signoff.
