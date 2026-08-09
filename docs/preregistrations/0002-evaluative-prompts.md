# 0002 — Evaluative prompt battery expansion

- **Status:** draft — NOT YET FROZEN
- **Drafted:** 2026-08-09
- **Frozen (commit):** *(fill in — this commit must precede any run)*
- **Related decisions:** 0010 (source flag), 0011 (gap estimand), 0015 (key
  normalization)

> **Freeze statement.** This file is complete and committed before any of the new
> evaluative prompts are run against any model. Items are not revised after results
> are seen. If an item turns out to be badly constructed, it is reported as-is and the
> problem is discussed in limitations — it is not silently replaced. Revision after
> seeing which items produced the effect would fit the instrument to the hypothesis.

---

## 1. Motivation

The declarative–evaluative gap is currently measured by comparing a declarative
battery (10 original concepts) against an evaluative battery of 5 code-review prompts
that do not correspond to those concepts. Alt text pairs directly; "Click here" tests
link text, which is not among the ten; unlabeled input has no declarative counterpart
at all. Any pairing of the existing batteries is therefore forced.

This expansion authors evaluative items that correspond one-to-one with declarative
concepts, so the gap can be stated as a within-concept claim — *for this concept, at
this scale, the model defines it and cannot apply it* — rather than as a difference
between two means over non-overlapping concept sets.

Cost is low: evaluative prompts touch elicitation only. No binding rerun, no frequency
rerun, no infini-gram queries.

## 2. Concept mapping

Eight of the ten Paper 1 declarative concepts take a natural evaluative form. Two do
not, and are excluded deliberately rather than by omission.

| # | Concept | Declarative prompt (existing) | Evaluative item |
|---|---------|-------------------------------|-----------------|
| 1 | screen reader | "A screen reader is" | *(to author)* |
| 2 | skip link | "A skip link is" | *(to author)* |
| 3 | alt text | "The purpose of alt text is" | *(to author)* |
| 4 | focus indicator | "A focus indicator is" | *(to author)* |
| 5 | keyboard navigation | "Keyboard navigation allows" | *(to author)* |
| 6 | color contrast | "Color contrast is important because" | *(to author)* |
| 7 | semantic HTML | "Semantic HTML helps" | *(to author)* |
| 8 | closed captions | "Closed captions are used for" | *(to author)* |

**Excluded, with reason:**

- **WCAG** — an acronym expansion task. An evaluative item ("which WCAG criterion does
  this violate") tests criterion-number recall, not application of the concept. The
  declarative item tests whether the model can expand the acronym; there is no
  matching evaluative capability to test.
- **ARIA** — same reason. ARIA additionally serves as the fluent-confabulation control
  in the existing battery, a role that a paired evaluative item would confuse.

The paper reports **eight pairs**, and states the exclusion explicitly rather than
letting a reader wonder where the other two went.

## 3. Item authoring rules

Frozen before authoring. Each evaluative item must:

1. **Have unambiguous ground truth.** A single correct answer that any practising
   accessibility specialist would give. If two specialists could reasonably disagree,
   the item is out.
2. **Require application, not recall.** The correct answer must not be derivable from
   restating the definition. An item answerable by pattern-completion from the
   declarative prompt is testing the wrong thing.
3. **Match the existing evaluative style.** Zero-shot, completion-framed, consistent
   with Experiment 2a's `code_review` template type so results are comparable to the
   original five.
4. **Not name the concept in the prompt.** "What is this `<img>` missing?" not "What
   alt text is missing?" Naming the concept converts the item into a recall task.
5. **Be authored without reference to model outputs.** Items are written from the
   concept list and the WCAG success criteria, not by looking at what models already
   get right or wrong.

The existing five Experiment 2a items are **retained unchanged** and reported
alongside. They are not replaced, and their results are not re-coded.

## 4. Run configuration

Frozen:

- **Models (13):** Pythia 160M / 410M / 1B / 2.8B / 6.9B / 12B; GPT-2 small / medium /
  large / XL; OLMo-2 1B / 7B / 13B. Base (non-instruction-tuned) checkpoints.
- **Decoding:** greedy, `do_sample=False`, `temperature=0`. *(Explicitly stated
  because a prior `do_sample=True` defect invalidated an earlier elicitation run.)*
- **`max_tokens`:** 100, matching the standardization already applied in
  `data/accessibility.yaml`.
- **Battery file:** items added to `data/accessibility.yaml` with
  `prompt_type: evaluative`, `template_type: code_review`, and
  `source: original` *(pending 0010)*.
- **Coding rubric:** identical to the existing evaluative coding — correct = identifies
  the specific violation; partial = identifies some issue but not the core violation;
  incorrect = wrong, off-topic, or loops. No new rubric is introduced.

## 5. Analysis plan

Frozen:

- **Primary.** Paired within-concept comparison across all 13 models: for each
  concept × model, declarative outcome vs evaluative outcome. Reported as the count of
  model × concept cells where declarative is correct and evaluative is not.
- **Secondary.** Gap in percentage points per scale, per family, restricted to the
  eight paired concepts. Compared against
  `_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv` as a sanity check on
  the concept restriction.
- **Uniformity is the claim.** The floor claim is carried by "no evaluative emergence
  at any scale in any family," not by an average difference. Report the full
  8 × 13 grid, not only the aggregate.
- **No significance test on the aggregate gap.** Per-cell outcomes are categorical and
  the interesting statement is uniformity, not a mean difference.

## 6. Predictions

Recorded in advance:

1. The gap holds at every scale in every family, on the paired items.
2. Pythia 6.9B is the strongest evaluative performer and still shows the gap.
3. Declarative accuracy rises with scale on the paired concepts; evaluative accuracy
   stays near floor with occasional isolated successes.
4. Isolated evaluative successes cluster on concepts that appear in training data as
   named anti-patterns (the "Click here" pattern) rather than on concepts requiring
   inference from the code.

## 7. Branches — all ship

- **Gap replicates on all eight pairs.** Reported as the primary result; the paired
  framing replaces the pooled-means framing throughout Section I.
- **Gap replicates on some pairs and not others.** Reported per concept. Which
  concepts break the pattern is itself a finding and is discussed rather than
  averaged away.
- **Gap does not replicate.** Reported. The pooled-means result is then attributed to
  the concept-population mismatch documented in decision 0010, and Section I is
  rewritten around whatever the paired data actually shows.
- **New items produce degenerate output** (looping, prompt echo) at a rate materially
  different from the original five. Instrumentation problem; reported as such, and the
  original five remain the primary evidence.

## 8. Outputs

- `data/accessibility.yaml` — eight new entries, `prompt_type: evaluative`
- `results/elicitation/{suite}/{model}/{model}-accessibility.csv` — regenerated
- `results/analysis/paired_gap.csv` — the 8 × 13 grid *(new)*

---

## Authoring worksheet

*Not part of the frozen protocol. Delete or move below the freeze line before
committing.*

For each concept: what does a violation look like in code, and what is the single
correct identification of it?

| Concept | Violation in code | Correct answer |
|---------|-------------------|----------------|
| screen reader | | |
| skip link | | |
| alt text | | |
| focus indicator | | |
| keyboard navigation | | |
| color contrast | | |
| semantic HTML | | |
| closed captions | | |
