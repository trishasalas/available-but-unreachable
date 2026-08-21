# Paired evaluative results audit

**Run completed:** 2026-08-20  
**Frozen battery:** `data/evaluative_paired.yaml`  
**Battery SHA-256:** `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`  
**Freeze commit:** `91a2c3a79b62322465daffa0a9fec0bee92016d0`

## Completeness

The saved result set contains all 13 preregistered models, all 16 items per
model, and 208 unique model-item responses. The frozen analyzer produced 104
model-by-concept cells and 13 model summaries without missing declarative joins.

## Preregistered primary result

The 12 untouched confirmatory models produced **0 strict evaluative pair passes
in 96 model-by-concept cells**. A pair passes only when both its violation and
conformant items are coded correct.

Among confirmatory cells:

- 85 passed neither polarity;
- 7 passed only the conformant item;
- 4 passed only the violation item;
- 0 passed both.

The confirmatory models contained 35 cells in which the same concept's
declarative response was correct. All 35 failed the evaluative pair, so the
preregistered conditional gap is 35/35. Pythia-160M had no declarative passes
among the eight paired concepts and therefore has no conditional denominator.

The development-exposed Pythia-2.8B pilot produced one strict pair pass: skip
link. It had five declarative passes, with four declarative-pass/evaluative-fail
cells and one declarative-and-evaluative pass.

## Item-level distribution

Across the 192 confirmatory item responses, the frozen coder assigned:

- 11 correct;
- 84 partial;
- 97 incorrect.

This distribution shows why the pair-level zero must not be presented as a
complete description of behavior. Most model-concept cells fail both items, but
11 cells show one-sided success.

## Prompt echo and classification sensitivity

Twenty-one of 192 confirmatory continuations contain an exact copy of their
prompt. Removing exact prompt copies and rerunning the frozen coder leaves every
confirmatory model at zero pair passes. It changes no confirmatory item label.

Pythia-2.8B begins the skip-link violation with `inaccessible` and the conformant
item with `accessible`. It then repeats much of each prose prompt. Its two-polarity
classification is unambiguous, but the repeated violation prompt supplies the
reason-bearing language used by the frozen rule. The defensible description is
therefore that it classified both examples correctly; an independent generated
explanation is not established.

A first-segment stance-only sensitivity produces two apparent classification
pair passes: Pythia-2.8B skip link and OLMo-2-1B closed captions. The OLMo
continuation immediately reverses its initial `accessible` token and calls the
conformant example inaccessible. This demonstrates why first-token stance is not
a suitable replacement for the frozen full-continuation score.

## Mechanical coding flags

Manual inspection identified two conformant items labeled correct by incidental
keyword matches:

1. OLMo-2-1B's focus-indicator response contains `accessible` inside a URL while
   saying the example has an accessibility error.
2. GPT-2's alt-text response says `accessible` and `not 'accessible'`; quotation
   marks prevent the frozen `not accessible` string match.

Neither item has a correct paired violation, so correcting either false positive
cannot create a confirmatory pair pass. The preregistered primary result is
therefore robust to these coding failures. Item-level correct counts should be
reported as frozen mechanical labels unless a separately identified adjudicated
sensitivity is added.

## Framing limitation

Skip link is the battery's only prose-described concept. The other seven pairs
require interpreting HTML or CSS. The pilot's sole success is therefore
consistent with framing-dependent reachability, but concept and representation
format are confounded in this one cell. It is not evidence of general evaluative
mastery or uniquely strong skip-link knowledge.

## Claim boundary

Supported:

> No confirmatory model passed any same-concept violation/conformant pair under
> the frozen coding protocol. Every confirmatory declarative-pass cell failed its
> evaluative pair.

Not supported:

- that the models possess no evaluative capability;
- that every possible application prompt would fail;
- that Pythia-2.8B independently explained the skip-link violation;
- that the skip-link result separates concept knowledge from prose framing.

The paired result must remain separate from the historical pooled gap tables.
All four declarative/evaluative cell states and item-level polarity outcomes ship
with the paper.
