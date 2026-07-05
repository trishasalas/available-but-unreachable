"""D8: is the lens artifact frequency-shaped? (b_U-as-frequency-prior)

Pre-registration: DECISIONS.md 2026-07-05 (D8), as AMENDED same day with
prior-art disclosure (Kobayashi et al. 2023; Cho et al. 2024) BEFORE any
weights were loaded. Predictions unchanged by the amendment:

  H1 (confirmatory): Spearman rho(b_U, log unigram frequency) >= +0.3 at
      Pythia-12B, same sign at all six scales. Under the frozen token-ID
      proxy (BPE merge order: LOWER id ~ MORE frequent), H1-consistent
      means rho(b_U, -token_id) >= +0.3.
  H2 (exploratory): sign/magnitude of rho(colsum(W_U), frequency) per
      scale; no prediction, report only.
  H3: held observational (6/6 flip direction was viewed data; disclosed
      as motivation, not tested here).

Weights-only. No generation, no forward passes. The sealed
results/logits/d7_step5_ranks_preban.csv is NOT touched.

Frozen frequency protocol:
  - Primary proxy: GPT-NeoX token ID over the full vocab, plus a trimmed
    robustness variant excluding ids < 512 and non-printable/special
    tokens (byte-region ids are not frequency-ordered).
  - Calibration: Infini-gram Pile-train (index v4_piletrain_llama,
    Llama-2 tokenizer -- STRING-level counts, caveat logged) on n=500
    single tokens that are alphabetic with a leading space, stratified
    50 per token-ID decile, seed=42. If proxy and calibration disagree
    in sign: report both, conclude nothing, stop (per pre-reg).

Colab usage (small scales also run locally on Apple Silicon):
    !pip install transformer_lens==2.17.0 scipy requests
    # upload this file (and nothing else needed), then:
    from d8_frequency_prior import run_d8
    run_d8(".")                      # all six scales
    run_d8(".", models=["pythia-12b"])   # or one at a time

Outputs -> results/d8_frequency_prior/ :
    d8_per_scale.csv       (rho values, b_U norms, environment)
    d8_calibration_<model>.csv  (sampled tokens, counts, per-scale)
    d8_summary.md          (H1 verdict per scale, H2 report)
"""

import csv
import datetime
import json
import re
from pathlib import Path

import torch

MODELS = ["pythia-160m", "pythia-410m", "pythia-1b",
          "pythia-2.8b", "pythia-6.9b", "pythia-12b"]
REQUIRED_TL_VERSION = "2.17.0"
H1_THRESHOLD = 0.3          # frozen
CAL_N = 500                 # frozen
CAL_SEED = 42               # frozen
TRIM_MIN_ID = 512           # byte/special region guard (robustness variant)
INFINI_INDEX = "v4_piletrain_llama"
INFINI_URL = "https://api.infini-gram.io/"


def _tl_version():
    try:
        from importlib.metadata import version, PackageNotFoundError
        for dist in ("transformer_lens", "transformer-lens"):
            try:
                return version(dist)
            except PackageNotFoundError:
                continue
    except Exception:
        pass
    return "unknown"


def _spearman(x, y):
    from scipy.stats import spearmanr
    rho, p = spearmanr(x, y)
    return float(rho), float(p)


def extract_vectors(model):
    """b_U and colsum(W_U) from a loaded HookedTransformer (fold_ln
    defaults). Guards: b_U must be nonzero (else folding didn't happen
    and the experiment premise is void -- stop, don't improvise)."""
    b_U = model.b_U.detach().float().cpu()
    W_U = model.W_U.detach().float().cpu()
    colsum = W_U.sum(dim=0)
    if float(b_U.abs().max()) == 0.0:
        raise RuntimeError(
            "b_U is exactly zero -- ln_final beta not folded? Premise "
            "void under this load; record and stop (pre-reg branch: "
            "report, no story).")
    return b_U, colsum


def token_strings(model):
    return [model.to_string(torch.tensor([i]))
            for i in range(model.cfg.d_vocab)]


def trimmed_mask(strs):
    mask = []
    for i, s in enumerate(strs):
        ok = i >= TRIM_MIN_ID and s.isprintable() and "<|" not in s
        mask.append(ok)
    return mask


def calibration_sample(strs):
    """n=500 alphabetic leading-space single tokens, 50 per token-ID
    decile, seed frozen."""
    import random
    rng = random.Random(CAL_SEED)
    eligible = [i for i, s in enumerate(strs)
                if re.fullmatch(r" [A-Za-z]+", s)]
    if not eligible:
        return []
    per = CAL_N // 10
    lo, hi = min(eligible), max(eligible)
    span = (hi - lo + 1) / 10.0
    sample = []
    for d in range(10):
        bucket = [i for i in eligible
                  if lo + d * span <= i < lo + (d + 1) * span]
        rng.shuffle(bucket)
        sample += bucket[:per]
    return sorted(sample)


def infini_count(term):
    import requests
    r = requests.post(INFINI_URL, json={
        "index": INFINI_INDEX, "query_type": "count", "query": term},
        timeout=30)
    r.raise_for_status()
    return int(r.json().get("count", 0))


def run_model(name, out_dir):
    from transformer_lens import HookedTransformer
    model = HookedTransformer.from_pretrained(name)   # defaults, house rule
    b_U, colsum = extract_vectors(model)
    strs = token_strings(model)
    ids = torch.arange(model.cfg.d_vocab).float()
    freq_proxy = -ids                                  # lower id ~ more frequent

    row = {"model": name, "d_vocab": model.cfg.d_vocab,
           "b_U_norm": float(b_U.norm()),
           "tl_version": _tl_version(),
           "dtype": str(model.b_U.dtype)}

    rho, p = _spearman(b_U.numpy(), freq_proxy.numpy())
    row["rho_bU_freqproxy_full"], row["p_full"] = rho, p

    mask = torch.tensor(trimmed_mask(strs))
    rho_t, p_t = _spearman(b_U[mask].numpy(), freq_proxy[mask].numpy())
    row["rho_bU_freqproxy_trimmed"], row["p_trimmed"] = rho_t, p_t
    row["n_trimmed"] = int(mask.sum())

    rho_c, _ = _spearman(colsum.numpy(), freq_proxy.numpy())
    rho_ct, _ = _spearman(colsum[mask].numpy(), freq_proxy[mask].numpy())
    row["rho_colsum_freqproxy_full"] = rho_c
    row["rho_colsum_freqproxy_trimmed"] = rho_ct

    # Calibration (network; graceful failure per pre-reg honesty)
    cal_rows, cal_rho = [], None
    try:
        import math
        sample = calibration_sample(strs)
        for i in sample:
            c = infini_count(strs[i])
            cal_rows.append({"token_id": i, "token": strs[i], "count": c,
                             "log_count": math.log(c + 1)})
        if cal_rows:
            cal_rho, _ = _spearman(
                [b_U[r["token_id"]].item() for r in cal_rows],
                [r["log_count"] for r in cal_rows])
    except Exception as e:
        row["calibration_error"] = repr(e)
    row["rho_bU_infinigram_calibration"] = cal_rho
    row["cal_n"] = len(cal_rows)

    if cal_rows:
        with open(out_dir / f"d8_calibration_{name}.csv", "w",
                  newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(cal_rows[0].keys()))
            w.writeheader(); w.writerows(cal_rows)

    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return row


def run_d8(project_root, models=None):
    out_dir = Path(project_root) / "results" / "d8_frequency_prior"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [run_model(m, out_dir) for m in (models or MODELS)]

    path = out_dir / "d8_per_scale.csv"
    exists = path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if not exists:
            w.writeheader()
        w.writerows(rows)

    lines = ["# D8 summary", "",
             f"- timestamp: {datetime.datetime.now().isoformat(timespec='seconds')}",
             f"- H1 frozen: rho(b_U, freq) >= +{H1_THRESHOLD} at 12B, "
             f"same sign all scales (proxy direction: rho vs -token_id)", ""]
    for r in rows:
        verdict = ("H1-consistent" if r["rho_bU_freqproxy_trimmed"]
                   >= H1_THRESHOLD else "below threshold")
        lines.append(
            f"- {r['model']}: rho(b_U, freq_proxy) full="
            f"{r['rho_bU_freqproxy_full']:.3f}, trimmed="
            f"{r['rho_bU_freqproxy_trimmed']:.3f} [{verdict}]; "
            f"colsum trimmed={r['rho_colsum_freqproxy_trimmed']:.3f}; "
            f"infini-gram cal={r['rho_bU_infinigram_calibration']}")
    lines += ["", "Sign-disagreement rule (frozen): if proxy and "
              "calibration disagree in sign, report both, conclude "
              "nothing, stop.",
              "", "Verdict paragraph is authored in DECISIONS, same "
              "session, whichever branch fires. Seal status: untouched.",
              json.dumps({"seed": CAL_SEED, "trim_min_id": TRIM_MIN_ID,
                          "infini_index": INFINI_INDEX})]
    (out_dir / "d8_summary.md").write_text("\n".join(lines))
    print(f"D8 complete -> {out_dir}/d8_summary.md")
