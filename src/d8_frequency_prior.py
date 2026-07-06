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

    # b_U vector saved per scale (200KB) so calibration is a fully
    # OFFLINE join later — see calibrate(). Counts are tokenizer-property
    # (shared across scales); b_U is model-property. Decoupled 2026-07-05
    # after the 403s exposed the 6x-duplicate-query design waste.
    with open(out_dir / f"d8_bU_{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["token_id", "b_U"])
        for i in range(model.cfg.d_vocab):
            w.writerow([i, float(b_U[i])])
    row["bU_vector_saved"] = True
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return row


def run_d8(project_root, models=None):
    out_dir = Path(project_root) / "results" / "d8_frequency_prior"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for m in (models or MODELS):
        try:
            rows.append(run_model(m, out_dir))
        except Exception as e:
            # A model's failure is data, not a batch-killer. Record it.
            rows.append({"model": m, "error": repr(e)})
            print(f"{m}: FAILED and recorded -- {e!r}")

    # Union of keys across rows so error rows and result rows coexist.
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    path = out_dir / "d8_per_scale.csv"
    exists = path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerows(rows)

    lines = ["# D8 summary", "",
             f"- timestamp: {datetime.datetime.now().isoformat(timespec='seconds')}",
             f"- H1 frozen: rho(b_U, freq) >= +{H1_THRESHOLD} at 12B, "
             f"same sign all scales (proxy direction: rho vs -token_id)", ""]
    for r in rows:
        if "error" in r:
            lines.append(f"- {r['model']}: FAILED — {r['error']}")
            continue
        verdict = ("H1-consistent" if r["rho_bU_freqproxy_trimmed"]
                   >= H1_THRESHOLD else "below threshold")
        lines.append(
            f"- {r['model']}: rho(b_U, freq_proxy) full="
            f"{r['rho_bU_freqproxy_full']:.3f}, trimmed="
            f"{r['rho_bU_freqproxy_trimmed']:.3f} [{verdict}]; "
            f"colsum trimmed={r['rho_colsum_freqproxy_trimmed']:.3f}; "
            f"b_U vector saved={r.get('bU_vector_saved', False)}")
    lines += ["", "Sign-disagreement rule (frozen): if proxy and "
              "calibration disagree in sign, report both, conclude "
              "nothing, stop.",
              "", "Verdict paragraph is authored in DECISIONS, same "
              "session, whichever branch fires. Seal status: untouched.",
              json.dumps({"seed": CAL_SEED, "trim_min_id": TRIM_MIN_ID,
                          "infini_index": INFINI_INDEX})]
    (out_dir / "d8_summary.md").write_text("\n".join(lines))
    print(f"D8 complete -> {out_dir}/d8_summary.md")


# ---------------------------------------------------------------------------
# Offline-first calibration (added 2026-07-05 after API 403s)
# ---------------------------------------------------------------------------

CAL_CACHE = Path("data") / "infini_gram_calibration_counts.csv"


def _write_cache(path, cache, strs):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["token_id", "token", "count"])
        for i in sorted(cache):
            w.writerow([i, strs[i], cache[i]])


def calibrate(project_root, models=None, qps=1.0, max_retries=5):
    """Fully decoupled calibration pass. Counts are tokenizer-property:
    fetched ONCE into a shared, resumable, crash-safe cache (checkpointed
    every 25 calls) with polite pacing and exponential backoff + jitter
    (the infini-gram docs' own guidance: wrap requests in retry loops).
    b_U is model-property: joined from the d8_bU_<model>.csv vectors
    saved by run_model. Rerun freely; never re-asks a cached question.

    Tokenizer note: sampling here rebuilds vocab strings from the shared
    GPT-NeoX tokenizer (no model load); same regex, same seed => same
    sample ids as the in-run path."""
    import math
    import random
    import time
    from transformers import AutoTokenizer

    root = Path(project_root)
    out_dir = root / "results" / "d8_frequency_prior"
    cache_path = root / CAL_CACHE
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    tok = AutoTokenizer.from_pretrained("EleutherAI/pythia-160m")
    strs = [tok.decode([i]) for i in range(len(tok))]
    sample = calibration_sample(strs)

    cache = {}
    if cache_path.exists():
        with open(cache_path) as f:
            for r in csv.DictReader(f):
                cache[int(r["token_id"])] = int(r["count"])
    todo = [i for i in sample if i not in cache]
    print(f"calibrate: {len(sample)} sampled, {len(cache)} cached, "
          f"{len(todo)} to fetch at {qps} qps")

    for n, i in enumerate(todo):
        for attempt in range(max_retries):
            try:
                cache[i] = infini_count(strs[i])
                break
            except Exception:
                time.sleep((2 ** attempt) + random.random())
        time.sleep(1.0 / qps)
        if (n + 1) % 25 == 0:
            _write_cache(cache_path, cache, strs)   # crash-safe
    _write_cache(cache_path, cache, strs)

    lines = ["# D8 calibration (offline join vs shared Pile-count cache)",
             f"- counts cached: {len(cache)}/{len(sample)} "
             f"(index {INFINI_INDEX}; Llama-2 tokenizer string counts —"
             f" caveat per pre-reg)", ""]
    for m in (models or MODELS):
        bu_path = out_dir / f"d8_bU_{m}.csv"
        if not bu_path.exists():
            lines.append(f"- {m}: no saved b_U vector — rerun run_model "
                         f"once for this scale")
            continue
        bu = {}
        with open(bu_path) as f:
            for r in csv.DictReader(f):
                bu[int(r["token_id"])] = float(r["b_U"])
        pairs = [(bu[i], math.log(cache[i] + 1))
                 for i in sample if i in cache and i in bu]
        rho, p = _spearman([a for a, _ in pairs], [b for _, b in pairs])
        lines.append(f"- {m}: rho(b_U, log Pile count) = {rho:.3f} "
                     f"(n={len(pairs)}, p={p:.2g})")
    lines += ["", "Sign-disagreement rule (frozen): if this disagrees in "
              "sign with the token-ID proxy, report both, conclude "
              "nothing, stop."]
    (out_dir / "d8_calibration_summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
