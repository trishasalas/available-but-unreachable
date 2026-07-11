# Tangent regeneration — divergence report

Comparison of regenerated `generation_text` (continuation-only, 50
greedy steps, `src/logit_export.export_because_tables`) against the
hand-transcribed *1. Generation* blocks in `docs/tangent.md`.

Whitespace is normalized (runs collapsed to single spaces) before
comparison — the transcription carries hand-entered indentation and
blank lines that are not model output. A **match** means the
regenerated continuation reproduces the transcribed text over their
common span; a **divergence** reports the first differing character.

| scale | prompt | verdict | detail |
|---|---|---|---|
| pythia-2.8b | skip_link | ✅ exact match (normalized) | 236 chars |
| pythia-2.8b | screen_reader | ✅ exact match (normalized) | 254 chars |
| pythia-2.8b | alt_text | ✅ exact match (normalized) | 191 chars |
| gpt2-medium | skip_link | ✅ exact match (normalized) | 220 chars |
| gpt2-medium | screen_reader | ✅ exact match (normalized) | 223 chars |
| gpt2-medium | alt_text | ✅ exact match (normalized) | 215 chars |
| gpt2-large | skip_link | ✅ exact match (normalized) | 202 chars |
| gpt2-large | screen_reader | ✅ exact match (normalized) | 228 chars |
| gpt2-large | alt_text | ✅ exact match (normalized) | 201 chars |
| gpt2-xl | skip_link | ✅ exact match (normalized) | 214 chars |
| gpt2-xl | screen_reader | ✅ exact match (normalized) | 185 chars |
| gpt2-xl | alt_text | ✅ exact match (normalized) | 218 chars |
| pythia-6.9b | skip_link | ⏳ pending | Trisha's Colab run (6.9b/12b) |
| pythia-6.9b | screen_reader | ⏳ pending | Trisha's Colab run (6.9b/12b) |
| pythia-6.9b | alt_text | ⏳ pending | Trisha's Colab run (6.9b/12b) |
| pythia-12b | skip_link | ⏳ pending | Trisha's Colab run (6.9b/12b) |
| pythia-12b | screen_reader | ⏳ pending | Trisha's Colab run (6.9b/12b) |
| pythia-12b | alt_text | ⏳ pending | Trisha's Colab run (6.9b/12b) |

## Determinism

12/12 local (scale × prompt) comparisons are exact matches after whitespace normalization. Greedy (argmax) decoding is deterministic, and the transcription's 2.8B/GPT-2 runs were themselves MPS-local, so the regeneration reproduces them bit-for-bit — no thin-margin flips to document at these scales. The cross-hardware determinism caveat (MPS float vs Colab CUDA flipping near-tie elections) stays live only for the Colab-origin 6.9B/12B; check it when those regens land.

## Known findings — confirmation

**12B cross-contamination (transcription, to be confirmed by Trisha's Colab regen):**
- screen_reader → `it does not have a text alternative. The text alternative is a text version of the content…`
- alt_text → `it has no text alternative. The alt text is a short description of the image. The alt text…`
- matches handoff description: screen_reader=True, alt_text=True
- The intro currently attributes the *screen-reader* answer to the *alt-text* question. Fix is Trisha's (placeholder flagged in `_rebuild/01-introduction.md`).

**GPT-2 XL corrupted block (transcription):** the XL screen_reader *2. Where the correct token ranks* section is a verbatim paste of a decision-point top-15 table (keeps the `rank` header and is identical to the XL skip-link *3. Top-15* block) — a copy-paste wound. The regenerated `gpt2-xl_screen_reader_because_steps.csv` supersedes it. Note: this wound is in the *step-trace* section, not the generation text, so it does not surface in the generation compare above.
