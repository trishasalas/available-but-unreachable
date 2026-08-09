# 0009 — Binding battery consolidated across domains

- **Status:** accepted
- **Date:** 2026-08-08
- **Note:** originally recorded in `DECISIONS.md` as a second "D7", colliding with
  "Single-token-ban counterfactual". CLAIMS A2/C6/D7 cite the single-token-ban entry,
  so that one keeps D7 and this one is renumbered here. Content unchanged.

## Context

Binding had been measured per-domain, which meant accessibility compounds could only
be compared against other accessibility compounds. The question the binding work
actually asks — whether sustained deep-layer binding is a structural property of
compound representation — is not a domain-specific question.

## Decision

Merge accessibility, medical, legal, finance, and control compounds into a single
227-compound binding battery. Binding is treated as a structural property of compound
representation, not a domain-specific one. The cross-domain set enables direct
comparison.

## Consequences

Direct cross-domain comparison becomes possible, and the binding claim can be tested
against a much larger compound set — which is what surfaced the collapse of the
binding–accuracy correlation (audit A7: gpt2 r=0.087, pythia r=-0.003, olmo r=0.115).

Harder: any analysis that assumed a domain-homogeneous battery needs a domain filter
added. `tokenization_comparison` in `src/analysis.py` still hardcodes 11 compounds
from the pre-consolidation era and buckets the other 42 as `'unknown'`.

**Depends on:** every compound carrying a usable `domain` value through to analysis.
The battery writers emit one; `load_all_results` preserves it only when the CSV
already has the column (`if 'domain' not in df.columns`). That guard is correct and
should stay correct.
