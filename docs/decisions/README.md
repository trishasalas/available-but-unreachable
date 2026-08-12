# Decisions

Research and methodology decisions, one file per decision, in [ADR ](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)style.

## How this works

- **One decision per file.** Named `NNNN-slug.md`, zero-padded, so the directory  
sorts correctly and the highest number is the last line of `ls`.
- **Files are immutable once accepted.** If a decision changes, write a new one that  
supersedes it. Edit the old file only to update its Status line. The history of the  
thinking is the point.
- **Status is required.** `proposed` means written down but not chosen. `accepted`  
means chosen. `superseded by NNNN` means replaced. `deprecated` means abandoned  
without replacement.
- **Consequences is not optional.** State what gets harder as well as what gets  
easier — and state what the decision *depends on* in order to keep being true.  
A6 happened because "expansion compounds are excluded from paradigm means" was  
recorded without recording that it depended on a `source` column existing in the  
loaded data. When the column stopped existing, nothing failed and nothing warned.

New decision: copy `TEMPLATE.md`, take the next number, fill it in.

## Legacy decisions (D1–D7)

D1 through D7 live in the repo-root `DECISIONS.md` and are **not** being backfilled  
here. CLAIMS.md cites several of them by number; breaking those citations to gain  
tidiness is a bad trade. The old file remains the record for everything up to D7.

One known problem inherited from that file: **D7 is assigned twice** — to  
"Single-token-ban counterfactual" and to "Binding battery consolidated across domains  
(2026-08-08)". CLAIMS A2/C6/D7 refer to the single-token-ban entry, so that one keeps  
the number. The binding-battery entry is re-recorded here as 0009.

## Index

| ID                                              | Decision                                          | Status     |
| ----------------------------------------------- | ------------------------------------------------- | ---------- |
| [0009](0009-binding-battery-consolidated.md)    | Binding battery consolidated across domains       | accepted   |
| [0010](0010-source-flag-expansion-compounds.md) | Source flag for expansion compounds               | accepted   |
| [0011](0011-gap-estimand-paired-concepts.md)    | Gap estimand: pooled means or paired concepts     | accepted   |
| [0012](0012-olmo-frequency-corpus.md)           | OLMo x-corpus for the frequency battery           | superseded |
| [0013](0013-analysis-tables-archival-status.md) | Archival status of five `results/analysis` tables | proposed   |
| [0014](0014-pythia-12b-naming.md)               | `pythia-13b` vs `pythia-12b` naming               | accepted   |
| [0015](0015-concept-key-normalization.md)       | Concept key normalization across batteries        | accepted   |

Numbering continues from D8, which is the highest number in the legacy file — the  
b_U-as-frequency-prior pre-registration and verdict (2026-07-05, H1 confirmed at all  
six scales). Note that several legacy entries carry titles but no D-number at all  
("Gap-table sampling-frame partition", "Spearman Analysis Specification", "Results  
layout", and others). Those are real decisions and are cited as such; they simply  
predate any numbering discipline. Do not renumber them.

## Related

- `docs/preregistrations/` — pre-registrations, committed before results are seen.  
Timestamps are the evidence. Separate number space from decisions.
- `docs/audit-response-plan.md` — the working plan that 0010–0015 block.
