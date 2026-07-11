"""Export evaluative decision-point logit data to results/logits/.

Replaces the print -> eyeball -> hand-paste-into-markdown pipeline in
notebooks/tangent.ipynb with mechanical CSV export. Per (model, compound):

  results/logits/{model}_{compound}_because_steps.csv
      greedy generation trace: step, token_id, token, logit
  results/logits/{model}_{compound}_because_ranks.csv
      decision-point candidates: rank, token_id, token, logit

Plus one joined-generation file per model, so a byte-compare against the
historical transcription (docs/tangent.md) is a string check, not token
archaeology:

  results/logits/{model}_because_generations.csv
      one row per compound: model, compound, prompt, n_steps, generation_text
      where generation_text is the detokenized greedy CONTINUATION only
      (the prompt is not included).

Usage (paste as a cell in tangent.ipynb, after the model is loaded):

    from src.logit_export import export_because_tables, VERIFIED_PROMPTS
    export_because_tables(model, "pythia-2.8b", VERIFIED_PROMPTS,
                          PROJECT_ROOT / "results" / "logits")

Run once per loaded model; filenames key on the model_name you pass — pass
the short name (e.g. "pythia-2.8b", not "EleutherAI/pythia-2.8b").
Remember the DECISIONS.md entry when the first full export lands.

Rank/step indexing stays 0-indexed for consistency with the D7 artifacts.
The prose 0- vs 1-indexed convention is a separate (Trisha) decision.
"""

import csv
from pathlib import Path

import torch

# Verified prompts (the three used in tangent.ipynb / tangent.md).
VERIFIED_PROMPTS = {
    "skip_link": "A long navigation menu without a skip link is not accessible because",
    "screen_reader": "A website without screen reader support is not accessible because",
    "alt_text": "An image without alt text is not accessible because",
}

# The remaining five are TEMPLATE-UNIFORM DRAFTS — Trisha reviews/edits
# before first use; framing choices are authorship, not plumbing.
# (Uniform template matters: see collocation/position-artifact lesson.)
# Out of scope for the tangent regeneration; kept here for later review.
DRAFT_PROMPTS = {
    "keyboard_navigation": "A web application without keyboard navigation is not accessible because",
    "color_contrast": "A page without sufficient color contrast is not accessible because",
    "focus_indicator": "A form without a visible focus indicator is not accessible because",
    "semantic_html": "A page built without semantic HTML is not accessible because",
    "closed_captions": "A video without closed captions is not accessible because",
}

# Back-compat alias: the full set (verified + drafts). Prefer VERIFIED_PROMPTS.
EVAL_PROMPTS = {**VERIFIED_PROMPTS, **DRAFT_PROMPTS}


def export_because_tables(model, model_name, prompts, out_dir,
                          n_steps=50, top_k=15):
    """Greedy step trace + decision-point top-k for each prompt, to CSV.

    Also writes one joined {model_name}_because_generations.csv for the
    whole set. The step trace and the joined generation come from the SAME
    greedy loop, so the two artifacts can never disagree the way two
    hand-copied runs did in the original transcription.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = next(model.parameters()).device

    generation_rows = []

    for compound, prompt in prompts.items():
        # --- decision-point ranks (top_k right after the prompt) ---
        input_ids = model.to_tokens(prompt)
        with torch.no_grad():
            logits = model(input_ids)
            dp_logits = logits[0, -1, :]
        top_values, top_indices = torch.topk(dp_logits, top_k)

        ranks_path = out_dir / f"{model_name}_{compound}_because_ranks.csv"
        with open(ranks_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["model", "compound", "prompt", "rank",
                        "token_id", "token", "logit"])
            for rank, (val, idx) in enumerate(zip(top_values, top_indices)):
                tok = model.to_string(torch.tensor([idx.item()]))
                w.writerow([model_name, compound, prompt, rank,
                            idx.item(), tok, f"{val.item():.4f}"])

        # --- greedy step trace (also feeds the joined generation) ---
        steps_path = out_dir / f"{model_name}_{compound}_because_steps.csv"
        current_ids = input_ids.clone()
        gen_token_ids = []
        with open(steps_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["model", "compound", "prompt", "step",
                        "token_id", "token", "logit"])
            with torch.no_grad():
                for step in range(n_steps):
                    logits = model(current_ids)
                    nt_logits = logits[0, -1, :]
                    nt = torch.argmax(nt_logits).item()
                    tok = model.to_string(torch.tensor([nt]))
                    w.writerow([model_name, compound, prompt, step,
                                nt, tok, f"{nt_logits[nt].item():.4f}"])
                    gen_token_ids.append(nt)
                    current_ids = torch.cat(
                        [current_ids,
                         torch.tensor([[nt]], device=device)], dim=1)

        # Detokenize the whole continuation at once (byte-level BPE can split
        # a character across tokens; whole-sequence decode reassembles it).
        generation_text = model.to_string(torch.tensor(gen_token_ids))
        generation_rows.append(
            [model_name, compound, prompt, n_steps, generation_text])

        print(f"exported: {ranks_path.name}, {steps_path.name}")

    # --- one joined-generation file per model ---
    gens_path = out_dir / f"{model_name}_because_generations.csv"
    with open(gens_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "compound", "prompt", "n_steps",
                    "generation_text"])
        w.writerows(generation_rows)
    print(f"exported: {gens_path.name}")
