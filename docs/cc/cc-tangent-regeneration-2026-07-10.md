# CC Handoff: Tangent Battery Regeneration

**Date:** 2026-07-10
**Prepared by:** Fable (claude.ai) with Trisha
**Why:** The intro's opening triad quotes 12B generations whose only surviving record is hand-transcribed prose (`notes/tangent.md` in the vault / `results/tangent.md` lineage). The transcription has at least one confirmed cross-contamination (see Known Findings). `src/logit_export.py` was built to replace exactly this pipeline and was never run at scale. This blocks promotion of `_rebuild/01-introduction.md`.
**Execution split:** CC preps everything and runs the local scales. Trisha runs 6.9B and 12B herself via the VS Code Colab extension. Do not attempt the big scales locally.

## 1 · Extend `src/logit_export.py` (small, surgical)

- `n_steps` default (or the call sites) → **50**. Ten steps is too short to capture the quoted generations.
- Add a **joined-generation export** so byte-compare is a string check, not token archaeology: one `results/logits/{model_name}_because_generations.csv` per model with columns `model, compound, prompt, n_steps, generation_text` where `generation_text` is the detokenized greedy continuation (continuation only, not the prompt).
- **Do NOT change rank indexing.** Exports stay 0-indexed for consistency with the existing D7 artifacts. The prose convention (0- vs 1-indexed ranks in the paper) is a separate Trisha decision — flagged, not yours.
- Only the **three verified prompts** run: `skip_link`, `screen_reader`, `alt_text`. The five DRAFT prompts in `EVAL_PROMPTS` are review-before-use and are **out of scope**.

## 2 · Modify `notebooks/tangent.ipynb` in place

- Add a `MODEL_NAME` variable at the top so a per-scale run is: edit one string → Restart & Run All. No other manual steps.
- Add the export cell at the end (the docstring's own prescription): import from `src.logit_export`, pass the three verified prompts, output to `results/logits/`.
- The notebook must run **unmodified under both the local kernel and a Colab kernel**. Investigate the existing Cell 00/Cell 0 Colab-detection pattern and follow it — if `src/` isn't importable under the Colab kernel, solve it the way the repo already solves file access in Colab. Don't invent a new pattern.
- Leave the exploratory cells intact; this is an addition, not a rewrite.

## 3 · Run matrix

| Scale | Who runs it |
|---|---|
| pythia-160m, 410m, 1b, 2.8b | CC, locally (MPS; caches exist for 2.8b at minimum) |
| pythia-6.9b, 12b | **Trisha, Colab** (VS Code Colab extension) |
| gpt2-medium, gpt2-large, gpt2-xl | CC, locally if memory allows; else flag for Colab |

Each run: Restart & Run All, confirm exports landed, move on. GPT-2 small isn't in the historical record; skip unless Trisha says otherwise.

## 4 · Byte-compare against the transcription

Compare each exported `generation_text` against the corresponding quote blocks in the tangent transcription document. Report a divergence table (scale × prompt × match/divergence + first differing text). Do not edit the transcription to make it match.

**Known findings the compare should confirm, not discover:**
- **12B quote cross-contamination:** screen_reader generation is "it does not have a text alternative…"; alt_text generation is "it has no text alternative. The alt text is a short description of the image…". The intro currently attributes the screen-reader answer to the alt-text question. Confirm both strings; the intro fix itself is Trisha's (placeholder already flagged in `_rebuild/01-introduction.md`).
- **GPT-2 XL corrupted block:** the transcription's XL screen-reader "step trace" is a duplicate of a decision-point table (copy-paste wound). Regeneration supersedes it; note it in the divergence report.

**Determinism caveat (important):** greedy decoding is deterministic on fixed hardware, but MPS vs CUDA float differences can flip near-tie elections — the exact regime D7 showed divergences concentrate in. Where the original ran on Colab GPU (12B certainly), the authoritative rerun is also Colab GPU. Cross-hardware mismatches at thin margins are *explainable divergences to document*, not failures — report the margin at the flip step if one occurs.

## 5 · Closeout

- **DECISIONS.md entry** when the first full export lands (the module docstring has been asking for this since it was written).
- Annotate the tangent transcription document with a superseded banner at top pointing to `results/logits/` — no other edits to it; it stays as the historical record of the paste-wound.
- One commit for the code/notebook changes, separate commit(s) for results artifacts as they land. Trisha's Colab results commit is hers.

## Out of scope

- The five DRAFT evaluative prompts
- Rank-indexing convention (Trisha rules separately)
- Any edits to `_rebuild/` prose
- Fixing tangent.md content
