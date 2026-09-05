"""Exploratory within-model localization from saved natural-prompt measurements.

Run from repository root. Writes only named audit outputs beside this script.
Uses all 49 compounds, not the 25-compound intervention-selection split.
Bootstrap resamples compounds jointly for all heads within each model.
No head identities are aligned across models; no causal inference is made.
"""
from pathlib import Path
import hashlib
import math
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr, false_discovery_control

ROOT = Path.cwd()
OUT = ROOT / 'docs/audits'
PREFIX = '2026-09-05-head-localization-reconciled'
N_BOOT = 2000
SEED = 20260905
frequency = pd.read_csv(ROOT / 'results/frequency/frequency_table.csv')[
    ['compound', 'bigram_count']].drop_duplicates()
saved = pd.read_csv(ROOT / 'results/analysis/effective_binding_compound_summary_natural.csv')

def correlations(x, y):
    xr = rankdata(x).astype(float)
    yr = rankdata(y, axis=0).astype(float)
    xr -= xr.mean()
    yr -= yr.mean(axis=0)
    denom = np.sqrt((xr*xr).sum() * (yr*yr).sum(axis=0))
    return np.divide(xr @ yr, denom, out=np.full(y.shape[1], np.nan), where=denom > 0)

import sys
sys.path.insert(0, str(ROOT))
from src.effective_binding_inputs import condition_files, load_condition_frame
models, heads, depths, hashes = [], [], [], []
for path in condition_files(ROOT, 'natural'):
    hashes.append((str(path.relative_to(ROOT)), hashlib.sha256(path.read_bytes()).hexdigest()))
    d = load_condition_frame(path, ROOT, 'natural')
    family, model = d.family.iloc[0], d.model.iloc[0]
    n_layers = int(d.layer.max()) + 1
    # Match the primary analysis's inner join to available corpus frequencies.
    late = d[(d.layer >= math.ceil(2*n_layers/3)) & d.compound.isin(frequency.compound)]
    matrix = late.pivot(index='compound', columns=['layer', 'head'], values='relative_weighted_ov_norm').sort_index()
    y = matrix.to_numpy()
    assert len(matrix) == 49 and np.isfinite(y).all()
    x = np.log1p(frequency.set_index('compound').loc[matrix.index, 'bigram_count'].to_numpy())
    p95 = np.quantile(y, .95, axis=1)
    reference = saved[saved.model.eq(model)].set_index('compound').loc[matrix.index, 'p95_relative']
    np.testing.assert_allclose(p95, reference, rtol=1e-12, atol=1e-14)
    rho = correlations(x, y)
    p = np.full(len(rho), np.nan)
    for j in np.flatnonzero(np.isfinite(rho)):
        result = spearmanr(x, y[:, j])
        np.testing.assert_allclose(rho[j], result.statistic, atol=1e-14)
        p[j] = result.pvalue
    valid = np.isfinite(p)
    q = np.full(len(p), np.nan)
    q[valid] = false_discovery_control(p[valid], method='bh')
    rng = np.random.default_rng(SEED)
    boot = np.empty((N_BOOT, len(rho)))
    for b in range(N_BOOT):
        index = rng.integers(0, len(x), len(x))
        boot[b] = correlations(x[index], y[index])
    # Constant heads have no correlation or interval; preserve them as missing.
    low, high = np.full(len(rho), np.nan), np.full(len(rho), np.nan)
    low[valid], high[valid] = np.nanquantile(boot[:, valid], [.025, .975], axis=0)
    finite_boot = np.isfinite(boot).sum(axis=0)
    neg_boot = np.divide((boot < 0).sum(axis=0), finite_boot,
                         out=np.full(len(rho), np.nan), where=finite_boot > 0)
    tail = y >= p95[:, None]
    per_head = pd.DataFrame({
        'family': family, 'model': model, 'layer': matrix.columns.get_level_values(0),
        'head': matrix.columns.get_level_values(1), 'n_compounds': len(x),
        'relative_layer_depth': (matrix.columns.get_level_values(0)+1)/n_layers,
        'rho': rho, 'p_two_sided': p, 'q_bh_within_model': q,
        'bootstrap_ci_low': low, 'bootstrap_ci_high': high,
        'bootstrap_negative_fraction': neg_boot, 'bootstrap_valid_resamples': finite_boot,
        'upper_tail_compound_count': tail.sum(axis=0)})
    heads.append(per_head)
    for layer, g in per_head.groupby('layer'):
        depths.append(dict(family=family, model=model, layer=layer,
            relative_layer_depth=g.relative_layer_depth.iloc[0], n_heads=len(g),
            n_finite=int(g.rho.notna().sum()), n_negative=int((g.rho<0).sum()),
            median_rho=g.rho.median(), q25_rho=g.rho.quantile(.25), q75_rho=g.rho.quantile(.75)))
    row = dict(family=family, model=model, n_late_heads=len(rho),
        n_finite=int(valid.sum()), n_negative=int((rho<0).sum()),
        n_negative_q_lt_05=int(((rho<0)&(q<.05)).sum()),
        n_negative_bootstrap_ci=int((high<0).sum()),
        median_head_rho=float(np.nanmedian(rho)),
        p95_rho=float(spearmanr(x,p95).statistic),
        upper_tail_unique_heads=int(tail.any(axis=0).sum()),
        upper_tail_heads_per_compound_min=int(tail.sum(axis=1).min()),
        upper_tail_heads_per_compound_max=int(tail.sum(axis=1).max()))
    models.append(row)
    print(row, flush=True)

assert len(models) == 13
pd.DataFrame(models).to_csv(OUT / f'{PREFIX}-models.csv', index=False)
pd.concat(heads, ignore_index=True).to_csv(OUT / f'{PREFIX}-heads.csv', index=False)
pd.DataFrame(depths).to_csv(OUT / f'{PREFIX}-depths.csv', index=False)
hashes.append(('results/frequency/frequency_table.csv', hashlib.sha256((ROOT/'results/frequency/frequency_table.csv').read_bytes()).hexdigest()))
pd.DataFrame(hashes, columns=['path','sha256']).to_csv(OUT / f'{PREFIX}-inputs.csv', index=False)
print(f'Wrote exploratory audit tables; {N_BOOT} bootstrap resamples, seed {SEED}.')
