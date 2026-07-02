"""Export evaluative decision-point logit data to results/logits/.

Replaces the print -> eyeball -> hand-paste-into-markdown pipeline in
notebooks/tangent.ipynb with mechanical CSV export. Two artifacts per
(model, compound):

  results/logits/{model}_{compound}_because_steps.csv
      greedy generation trace: step, token_id, token, logit
  results/logits/{model}_{compound}_because_ranks.csv
      decision-point candidates: rank, token_id, token, logit

Usage (paste as a cell in tangent.ipynb, after the model is loaded):

    from src.logit_export import export_because_tables, EVAL_PROMPTS
    export_because_tables(model, "pythia-2.8b", EVAL_PROMPTS,
                          PROJECT_ROOT / "results" / "logits")

Run once per loaded model; filenames key on the model_name you pass.
Remember the DECISIONS.md entry when the first full export lands.
"""

import csv
from pathlib import Path

import torch

# Verified prompts (the three used in tangent.ipynb / tangent.md).
# The remaining five are TEMPLATE-UNIFORM DRAFTS — Trisha reviews/edits
# before first use; framing choices are authorship, not plumbing.
# (Uniform template matters: see collocation/position-artifact lesson.)
EVAL_PROMPTS = {
    "skip_link": "A long navigation menu without a skip link is not accessible because",
    "screen_reader": "A website without screen reader support is not accessible because",
    "alt_text": "An image without alt text is not accessible because",
    # --- DRAFTS below: review before use ---
    "keyboard_navigation": "A web application without keyboard navigation is not accessible because",
    "color_contrast": "A page without sufficient color contrast is not accessible because",
    "focus_indicator": "A form without a visible focus indicator is not accessible because",
    "semantic_html": "A page built without semantic HTML is not accessible because",
    "closed_captions": "A video without closed captions is not accessible because",
}


def export_because_tables(model, model_name, prompts, out_dir,
                          n_steps=10, top_k=15):
    """Greedy step trace + decision-point top-k for each prompt, to CSV."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = next(model.parameters()).device

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

        # --- greedy step trace ---
        steps_path = out_dir / f"{model_name}_{compound}_because_steps.csv"
        current_ids = input_ids.clone()
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
                    current_ids = torch.cat(
                        [current_ids,
                         torch.tensor([[nt]], device=device)], dim=1)

        print(f"exported: {ranks_path.name}, {steps_path.name}")
