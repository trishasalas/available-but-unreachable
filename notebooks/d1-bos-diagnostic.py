# %% [markdown]
# # D1 — BOS-attention diagnostic: Pythia-12B late-layer binding resurgence
#
# Pre-registration: docs/d1-preregistration.md (COMMIT BEFORE RUNNING).
# Prediction P1: ≥ half of late-layer (layer ≥ 27) top-binding heads at 12B are
# sink-dominated (mean BOS attention ≥ 0.5) or structural (mean attention to
# position 1 ≥ 0.5). All branches ship.
#
# Colab: Runtime → A100 / high-RAM GPU. Run cells top to bottom.

# %% Setup — Colab
# If running in Colab, clone/mount the repo first so src/ and results/ resolve.
# Example (adjust to your flow):
#   from google.colab import drive; drive.mount('/content/drive')
#   %cd /content/drive/MyDrive/Repos/Research/tmlr        # or your path
# Then:
#   !pip -q install transformer-lens==2.17.0 pandas

# %% Imports and paths
from pathlib import Path
import pandas as pd
import torch

PROJECT_ROOT = Path.cwd()  # run from the tmlr repo root; adjust if needed
assert (PROJECT_ROOT / "src").exists(), f"Run from repo root; cwd={PROJECT_ROOT}"

from src.head_characterization import (
    get_top_binding_heads,
    characterize_heads,
    SINK_THRESHOLD,
    STRUCTURAL_THRESHOLD,
)

BINDING_CSV = PROJECT_ROOT / "results/pythia/pythia-12b-binding.csv"
OUT_DIR = PROJECT_ROOT / "results/d1_bos_diagnostic"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LATE_LAYER_MIN = 27  # frozen: final quarter of 36 layers (see pre-registration)

# %% Derive the head set from the frozen binding record (never hardcoded)
heads = get_top_binding_heads(BINDING_CSV)
print(f"Top binding heads from frozen CSV: {heads}")

late_heads = [(l, h) for (l, h) in heads if l >= LATE_LAYER_MIN]
print(f"Late-layer (≥{LATE_LAYER_MIN}) resurgence set under test: {late_heads}")
assert late_heads, "No late-layer heads in top set — record this outcome; it is itself reportable."

# %% Load Pythia-12B (bf16; A100-class GPU)
from transformer_lens import HookedTransformer

model = HookedTransformer.from_pretrained(
    "pythia-12b",
    torch_dtype=torch.bfloat16,
    device="cuda",
)
model.eval()
print(model.cfg.n_layers, "layers,", model.cfg.n_heads, "heads")

# %% Characterize — one forward pass; sink/structural/induction/prev from the same cache
table = characterize_heads(model, late_heads)
print(table)

# NOTE (defensive): the assertions below expect columns for BOS attention and
# position-1 attention. If characterize_heads names them differently in this
# version (e.g. 'bos_attn' vs 'attention_to_bos'), adjust COL_BOS / COL_POS1 —
# and record the adjustment in DECISIONS.md. Thresholds do NOT change.
COL_BOS = next(c for c in table.columns if "bos" in c.lower())
COL_POS1 = next((c for c in table.columns if "pos" in c.lower() or "struct" in c.lower()), None)
print(f"Using columns: BOS={COL_BOS}, POS1={COL_POS1}")

# %% Apply the frozen rule
table["sink_dominated"] = table[COL_BOS] >= SINK_THRESHOLD
table["structural"] = (table[COL_POS1] >= STRUCTURAL_THRESHOLD) if COL_POS1 else False
table["qualifies"] = table["sink_dominated"] | table["structural"]

n_late = len(table)
n_qual = int(table["qualifies"].sum())
frac = n_qual / n_late

if n_qual == 0:
    verdict = "NOT CONFIRMED"
elif frac >= 0.5:
    verdict = "CONFIRMED"
else:
    verdict = "PARTIAL"

print(f"\nD1 VERDICT: {verdict} — {n_qual}/{n_late} late-layer binders sink-or-structural (frozen bar: ≥ 50%)")

# %% Persist — per-head table + verdict record
table.to_csv(OUT_DIR / "d1_late_head_characterization.csv", index=True)

verdict_md = f"""# D1 VERDICT — {verdict}

Pre-registration: docs/d1-preregistration.md (frozen before run).
Head set (derived from results/pythia/pythia-12b-binding.csv, layer ≥ {LATE_LAYER_MIN}): {late_heads}
Result: {n_qual}/{n_late} late-layer top binders sink-dominated (BOS ≥ {SINK_THRESHOLD}) or structural (pos-1 ≥ {STRUCTURAL_THRESHOLD}).
Frozen bar: ≥ 50% ⇒ CONFIRMED; >0 <50% ⇒ PARTIAL; 0 ⇒ NOT CONFIRMED.

Per-head table: d1_late_head_characterization.csv
Paper consequences per outcome mapping in the pre-registration. All branches ship.
Instrument: transformer-lens==2.17.0, one characterization forward pass.
"""
(OUT_DIR / "VERDICT.md").write_text(verdict_md)
print(f"\nWritten: {OUT_DIR / 'd1_late_head_characterization.csv'}")
print(f"Written: {OUT_DIR / 'VERDICT.md'}")

# %% [markdown]
# ## After the run
# 1. Commit results/d1_bos_diagnostic/ (CSV + VERDICT.md).
# 2. Bring the verdict to the thread — text consequences execute per the
#    pre-registration's outcome mapping, Trisha ratifying as always.
