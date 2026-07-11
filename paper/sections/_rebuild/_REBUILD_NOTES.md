# Rebuild notes — Fable, 2026-07-10

Ten files in `_rebuild/`, drafted against `notes/Rebuild Skeleton.md` after your ratification pass. Canonical sections untouched. Review each, then promote with `git mv` (or cherry-pick prose) — the renumbering commit and this promotion are naturally the same commit, and it also fixes `build-paper.sh` SECTION_FILES (pre-existing breakage, per CC).

## What each file is

| File | Nature | Word count vs budget |
|---|---|---|
| 00-abstract | fresh construction (fixes metadata.yaml G1 debt — old thesis) | ~230 / 200 |
| 01-introduction | current intro + hook fixes + **Table 1 (new)** + **blind-study paragraph (new)** + renumbered roadmap | over budget — Table 1 earns it |
| 02-behavioral-gap | current 02 + 124M fix + **two-cuts disclosure (new)** + **completion paradox adopted (new ¶)** | ~on budget |
| 03-binding-not-causal | preserved; headline reframed to lead with cross-domain generality; [→ APPENDIX] markers added | over budget — cuts are your call, markers show where |
| 04-frequency-predicts | **merge** of old 04 + old 05; taxonomy absorbed as vocabulary; failure-character ¶ repositioned as bridge to 05 | ~on budget |
| 05-fluent-wrongness | rewritten center — see ⚠️ below | ~on budget |
| 06-measurement-pathways | old 06a nearly verbatim + blind-study origin sentence + §4 tie-back close | on budget |
| 07 / 08 / 09 | reference renumbering + small dependent edits only | unchanged |

## ⚠️ Adjudications required before promotion (in priority order)

1. **T2: sign flip vs. non-negative collapse.** The old 06 prose claimed the confidence gap crosses zero (+0.37 → −0.37, "sign flip"). `fluent_wrongness.csv` shows a **non-negative penalty shrinking toward zero** (Pythia 0.97 → 0.07 at 6.9B, rebound 0.32 at 12B; GPT-2 0.68 → 0.07), which matches **T2 as registered and blind-recovered** ("shrinks toward zero, non-negative throughout"). The draft follows the CSV + registration. If the sign-flip came from a different cell definition (per-concept aggregation in `entropy_confidence.csv`?), decide which analysis is canonical. This touches 05, 08 (one phrase), 09 (one phrase), Table 1, and the Figure 5 design.
2. **Intro hook, third example.** Needs the verbatim div/onclick 12B quote from the committed responses (placeholder marked). Also verify "twenty-five years" framing.
3. **03 appendix cuts.** Markers placed at the per-head diagnostic table and the joint-ablation gate accounting. Budget says cut; blessed prose says you decide.
4. **metadata.yaml abstract** must be replaced with 00-abstract at promotion (G1 debt).

## Numbers provenance

Every number in these drafts is either (a) verified today against a CSV/MD I read (`pythia_gap`, `gpt2_gap`, `accuracy_by_prompt_type`, `fluent_wrongness`, `spearman_summary`, `pythia_frequency_trajectory`, `d7_summary`, gate CSVs), or (b) carried unchanged from the current blessed sections (binding KLs, b_U ρ range, partial correlations, stability 20/102, rank arcs). Nothing was recalled from memory. CC's number-audit pass should still run at promotion — especially the (b) category.

## Style contract

One line per paragraph throughout. Provenance header on every file.

## Figure slots as drafted

Fig 1 gap (behavioral only) → §2 · Fig 2 completion-paradox → §2 · Fig 3 concept-trajectories (caption repair) → §4 · Fig 4 frequency scatter (jitter + domain color, n=49) → §4 · Fig 5 confidence-penalty collapse → §5 · Fig 6 step-5 audit exhibit → §6. Decision-point ranks stay in §4 prose. Blue=declarative/green=evaluative grammar per figure policy; red reserved for §5's wrong-answer line.
