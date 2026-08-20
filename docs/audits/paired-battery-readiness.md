# Paired evaluative battery readiness review

## Freeze status

The reviewed 16-item battery, preregistration, deterministic coding, tests, runner,
and analyzer were frozen together on 2026-08-20 before any new model output was
generated. The initial draft described below remains superseded and must not be run.

The frozen instrument is `data/evaluative_paired.yaml`. Any post-freeze change requires
a dated protocol amendment and a complete rerun.

- Frozen battery SHA-256: `e495f5ce0af138484b7d7f34ecf4f467d5fbe6e918f2a165a78b52eddd7e75de`
- Synthetic verification: 13 tests passed in the `mechinterp` environment.

## What exists now

- `data/evaluative_paired_draft.yaml` contains 10 items covering 3 of the intended 8 concepts: alt text, closed captions, and color contrast.
- Five concepts are missing: focus indicator, keyboard navigation, semantic HTML, skip link, and screen reader.
- The draft contains 3 or 4 items per concept, but preregistration 0002 describes one evaluative item per concept and the audit plan describes two framings per concept.
- Pythia-2.8B output influenced at least the prompt wrapper and one conformant-item comment. The notebook also contains a partial attempted run of the 10-item draft. No paired result CSV is saved under `results/`.
- `docs/audits/audit-response-plan.md` marks the 13-model run and coding complete, but no saved paired battery results support those checkboxes.

## Four blockers before a freeze

### 1. The conformant frame presupposes failure

Several conformant items end with `The accessibility problem ... is`. A base model is being asked to continue a clause that asserts a problem exists. Hallucinating a fault under that frame is not a clean false-positive measure.

The proposal uses the neutral completion `an accessibility reviewer should mark this example as` for both polarities. A model can continue with either `accessible` or `inaccessible because ...`.

### 2. The current analysis cannot aggregate multiple items

`src/gap_analysis.py` builds the evaluative table with `pivot_table(..., aggfunc='first')`. If several paired items are appended to `data/accessibility.yaml`, only one response per concept and scale survives. Which item survives is an implementation detail, not a declared estimand.

The paired battery should remain a separate file and output family. It needs a dedicated analyzer.

### 3. The evaluator has no rules for the new items

`src/accuracy_coding.py::code_evaluative` recognizes only the five original prompt patterns. Every proposed item currently falls through to `incorrect`.

The prompt-specific rubrics must be authored and committed before any frozen run. Coding cannot be adapted after seeing model language.

### 4. The preregistration is no longer accurate

Preregistration 0002 says the instrument is one item per concept, uses `prompt_type: evaluative`, is added to `data/accessibility.yaml`, and can be analyzed as an 8 by 13 grid. The current draft already moved to multiple polarities and frames. The preregistration must describe the instrument that will actually run.

## Recommended primary design

- Eight declarative concepts, excluding WCAG and ARIA as already planned.
- Two evaluative items per concept: one violation and one conformant minimal pair.
- Identical neutral answer frame across polarities.
- **Primary evaluative pass:** both items correct. This prevents a model that always declares a problem, or never declares one, from passing the concept.
- **Primary paired gap cell:** declarative response is correct and evaluative pair does not pass.
- Report the complete cell states, not only the gap count:
  - declarative correct / evaluative pass
  - declarative correct / evaluative fail
  - declarative fail / evaluative pass
  - declarative fail / evaluative fail
- Partial-credit item means are secondary and cannot replace the pair-pass outcome.
- Keep the original five evaluative items as a historical battery. Do not pool them into the paired estimator.

## Pilot handling

Pythia-2.8B has seen an earlier version of the instrument. The cleanest rule is:

- label Pythia-2.8B as pilot;
- exclude it from the confirmatory aggregate;
- freeze prompts, rubrics, analysis code, and all outcome branches;
- use the other 12 models as the untouched test set;
- run the frozen battery on Pythia-2.8B unchanged and report it descriptively alongside the confirmatory models.

This is not a failure of preregistration. It is an explicit development/test split created before the remaining outputs are seen.

## Decisions requiring the author's judgment

1. **Screen reader — APPROVED:** The `aria-hidden='true'` pair is a valid application test. Understanding the consequence of `aria-hidden` requires understanding how a screen reader obtains content through the accessibility tree.
2. **Keyboard navigation — APPROVED AFTER REVISION:** The original proposal used `div onclick` versus a native `button`. Author review rejected that distinction as too dependent on specialist knowledge of native control semantics and identified tab order as the practical center of keyboard navigation. The approved violation uses positive `tabindex` values to override document order; the conformant pair omits `tabindex` because native interactive elements already participate in the tab sequence in source order. Author also identified `tabindex="0"` for adding an element to natural tab order and `tabindex="-1"` for removing it from sequential navigation while retaining programmatic focus as adjacent cases.
3. **Skip link — APPROVED:** The no-bypass versus jump-to-main scenario is unambiguous enough without full page code because the scenario removes alternative bypass mechanisms by construction.
4. **Primary scoring — APPROVED:** Both polarity items must be correct for an evaluative concept to pass. Item-level partial credit is retained only for secondary analysis.

Additional item review:

- **Semantic HTML — APPROVED:** A visually styled `div` heading versus a native `h2` fairly tests whether the model understands that heading structure must be programmatically exposed.
- **Focus indicator — APPROVED WITH CAVEAT:** `outline: none` without a replacement removes the browser's native visible focus indicator. The conformant item uses an explicit visible outline, but custom styling is not required for basic conformance because the browser supplies focus visibility unless author CSS suppresses it.
- **Color contrast — APPROVED:** `#999999` on white (approximately 2.85:1) is the violation; `#767676` on white (approximately 4.54:1) is the conformant minimal pair for normal-size text.
- **Closed captions — APPROVED:** A lecture video without a captions track is paired with the same video containing an English `<track kind="captions">` element.
- **Alt text — APPROVED:** A product-context image without `alt` is paired with the same image using `alt="Sink filled with dirty dishes"`; the supplied text alternative is appropriate to the surrounding context.

All eight concept pairs and the pair-level scoring rule completed author review on 2026-08-20.

## Freeze sequence

1. Author reviews the 16 proposed items for ground truth only. **COMPLETE**
2. Revise preregistration 0002 to match the final item count, pilot handling, pair-pass estimand, and outcome branches. **COMPLETE**
3. Add deterministic prompt-specific coding rules and unit tests before any model output is generated. **COMPLETE**
4. Add a dedicated paired-battery validator and analyzer; verify them on synthetic responses only. **COMPLETE**
5. Commit the battery, rubric, tests, analyzer, and preregistration together as the freeze commit. **COMPLETE**
6. Run the 12 untouched models first. Run Pythia-2.8B last and label it pilot.
7. Save per-model manifests and an 8 by 13 cell table. All branches ship.
