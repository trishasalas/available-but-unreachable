"""Compound-level frequency<->accuracy Spearman (amended spec).

Authoritative spec: DECISIONS 2026-07-03 "Spearman unit-of-analysis +
interpretation thresholds pre-registered" + criteria-handoff ADDENDUM. This
SUPERSEDES the earlier trajectory-ordinal / row-level construction.

PRIMARY (per suite; Pythia = confirmatory [Pile = training corpus],
GPT-2 = replication-under-proxy):
  one observation per COMPOUND per suite.
    x = log10(frozen Infini-gram bigram_count)   [ranks used; log10 monotone]
    y = mean across scales of STRICT binary accuracy (correct=1;
        partial OR incorrect=0)                  [Trisha 2026-07-03]
  Report Spearman rho + n for BOTH sense splits (all_rows / a11y_sense_only,
  y rebuilt from sense-filtered rows). Compound-level p is legitimate (49
  independent compounds, not pseudo-replicated).
  Thresholds (strict-binary primary): rho>=0.4 support; 0.2<=rho<0.4 weak;
  rho<0.2 or wrong sign -> not supported.

ROBUSTNESS (all pre-declared):
  - Kendall tau-b alongside each primary cell.
  - Partial Spearman (all_rows) controlling (a) compound token count
    (GPT-2 BPE subword pieces, uniform proxy) and (b) word1 unigram count.
  - Row-level Spearman: DESCRIPTIVE ONLY; clustered bootstrap over compounds
    (>=1000 resamples) for CI. NO naive row-level p anywhere.
  - Secondary y: strict accuracy at maximum scale.
  - Sensitivity y: weighted (correct=1/partial=0.5/incorrect=0), descriptive.

AUDITS (pre-declared):
  - Criteria-strictness (count incorrect_markers per row) vs predicted class.
  - Trajectory-class stability under a single adjacent code flip.

Reads the PER-SUITE frequency tables written by notebooks/frequency-*.ipynb
(no Infini-gram call). Each suite's x comes from the corpus that suite was
trained on, and every output row carries the `corpus_index` it used. Before
2026-08-09 this read one global frequency_table.csv and gave every suite the
same x — audit finding A4. Run:
    python -m src.dual_spearman
"""
from pathlib import Path
import math

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau

from src.analysis import load_all_results, scale_label
from src.accuracy_coding import code_response, observe_sense
from src.frequency import load_suite_frequency_table
from src.gap_analysis import SCALE_ORDERS, _classify_trajectory
CONCEPT_TO_COMPOUND = {
    "screen reader": "screen_reader", "alt text": "alt_text",
    "skip link": "skip_link", "color contrast": "color_contrast",
    "keyboard navigation": "keyboard_navigation",
    "focus indicator": "focus_indicator", "semantic HTML": "semantic_html",
    "captions": "closed_captions", "closed captions": "closed_captions",
    "WCAG": "WCAG", "ARIA": "ARIA",
}

STRICT = {'correct': 1, 'partial': 0, 'incorrect': 0}
WEIGHTED = {'correct': 1.0, 'partial': 0.5, 'incorrect': 0.0}
ORDINAL = {'incorrect': 0, 'partial': 1, 'correct': 2}   # for trajectory scoring
TRAJ_ORDINAL = {'never_emerges': 0, 'mixed': 1, 'peak_regress': 2,
                'monotonic_climb': 3}

# Pre-registered predictions (DECISIONS 2026-07-03), predicted trajectory-class
# ordinal for the audit-6 strictness check. Token-competition candidates were
# predicted to be captured by a wrong-domain attractor (fail -> never_emerges);
# tree_grid never_emerges; ceiling anchors monotonic_climb.
PREDICTED_CLASS = {
    'sensory_characteristics': 'never_emerges', 'redundant_entry': 'never_emerges',
    'status_message': 'never_emerges', 'error_identification': 'never_emerges',
    'pointer_cancellation': 'never_emerges', 'landmark_region': 'never_emerges',
    'focus_management': 'never_emerges', 'tree_grid': 'never_emerges',
    'sign_language': 'monotonic_climb', 'text_formatting': 'monotonic_climb',
    'form_field': 'monotonic_climb', 'responsive_design': 'monotonic_climb',
}


def _tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained('gpt2')


def _partial_spearman(x, y, z):
    """Spearman partial correlation of (x, y) controlling z: Pearson on ranks
    plugged into the first-order partial-correlation formula."""
    rx, ry, rz = (pd.Series(v).rank() for v in (x, y, z))
    rxy = np.corrcoef(rx, ry)[0, 1]
    rxz = np.corrcoef(rx, rz)[0, 1]
    ryz = np.corrcoef(ry, rz)[0, 1]
    denom = math.sqrt(max((1 - rxz**2) * (1 - ryz**2), 1e-12))
    return (rxy - rxz * ryz) / denom, rxy


def build_compound_table(project_root, suite):
    """Per compound, for ONE suite: x=log10(bigram), y variants, controls.

    Reads that suite's own frequency table, so `x` comes from the corpus the
    suite was actually trained on. Until 2026-08-09 this read a single global
    frequency_table.csv and assigned the same x to every suite, which is audit
    finding A4.

    Returns:
        (tab, elic, corpus_index) — the compound table, the coded elicitation
        frame for this suite, and the corpus index the x-values came from.

    Raises:
        FileNotFoundError: if the suite has no per-suite frequency table.
    """
    project_root = Path(project_root)
    freq, corpus_index = load_suite_frequency_table(project_root, suite)
    freq = freq[freq['domain'] == 'accessibility'].copy()

    elic, _, _ = load_all_results(project_root)
    elic['scale_label'] = elic['scale'].apply(scale_label)
    elic = elic[elic['prompt_type'] == 'declarative'].copy()
    elic['accuracy'] = elic.apply(
        lambda r: code_response('declarative', r['concept'], r['prompt'],
                                r['output']), axis=1)
    elic['sense'] = elic.apply(
        lambda r: observe_sense(r['concept'], r['output']), axis=1)
    # Faithful concept->compound (handles captions->closed_captions and
    # semantic HTML->semantic_html; falls back to space->underscore).
    elic['compound'] = elic['concept'].map(
        lambda c: CONCEPT_TO_COMPOUND.get(c, str(c).replace(' ', '_')))
    elic = elic[elic['suite'] == suite].copy()

    tok = _tokenizer()
    tok_count = {c: len(tok.tokenize(c.replace('_', ' '))) for c in freq['compound']}

    order = SCALE_ORDERS[suite]
    rows, skipped = [], []
    for _, fr in freq.iterrows():
        comp = fr['compound']
        sub = elic[elic['compound'] == comp]
        if sub.empty:
            # No elicitation rows for this compound in this suite. Record it —
            # a silent `continue` here is why OLMo produced zero rows and no
            # output file ever said so.
            skipped.append(comp)
            continue
        # order rows by scale
        sub = sub.assign(_ord=sub['scale_label'].apply(
            lambda sl: order.index(sl) if sl in order else -1))
        sub = sub[sub['_ord'] >= 0].sort_values('_ord')
        strict = sub['accuracy'].map(STRICT)
        weighted = sub['accuracy'].map(WEIGHTED)
        a11y_strict = sub[sub['sense'] == 'a11y']['accuracy'].map(STRICT)
        rows.append({
            'suite': suite, 'compound': comp,
            'corpus_index': corpus_index,
            'x_log10_bigram': math.log10(fr['bigram_count']),
            'y_all': strict.mean(),
            'y_a11y': a11y_strict.mean() if len(a11y_strict) else np.nan,
            'n_a11y_rows': int(len(a11y_strict)),
            'y_maxscale': strict.iloc[-1],
            'y_weighted': weighted.mean(),
            'n_rows': int(len(sub)),
            'token_count': tok_count.get(comp, np.nan),
            'word1_count': fr['word1_count'],
        })

    print(f'{suite}: {len(freq)} compounds in frequency table, '
          f'{len(rows)} with elicitation rows, {len(skipped)} skipped')
    if skipped:
        print(f'{suite}: SKIPPED (no elicitation rows) -> {skipped}')
    if not rows:
        print(f'{suite}: WARNING — no compound rows built. Every statistic for '
              f'this suite will be absent, not wrong. Check that elicitation '
              f'results exist for {suite}.')
    return pd.DataFrame(rows), elic, corpus_index


def primary_and_robustness(tab):
    """Primary + all pre-declared robustness cells.

    Every output row carries `corpus_index`, taken from the compound table, so
    a reader can tell which corpus produced a number without consulting the
    notebook that produced it. All cells for a suite read the same `tab`, so
    the primary and the robustness paths cannot disagree about the corpus.
    """
    prim, kend, part, sec, sens = [], [], [], [], []
    for suite in sorted(tab['suite'].unique()):
        s = tab[tab['suite'] == suite]
        idx = s['corpus_index'].iloc[0] if len(s) else np.nan
        for split, ycol in [('all_rows', 'y_all'), ('a11y_sense_only', 'y_a11y')]:
            d = s.dropna(subset=[ycol, 'x_log10_bigram'])
            n = len(d)
            if n >= 3 and d[ycol].nunique() > 1 and d['x_log10_bigram'].nunique() > 1:
                rho, p = spearmanr(d['x_log10_bigram'], d[ycol])
                tau, tp = kendalltau(d['x_log10_bigram'], d[ycol])
            else:
                rho = p = tau = tp = np.nan
            prim.append({'suite': suite, 'corpus_index': idx,
                         'sense_split': split,
                         'spearman_rho': _r(rho), 'spearman_p': _p(p),
                         'n_compounds': n})
            kend.append({'suite': suite, 'corpus_index': idx,
                         'sense_split': split,
                         'kendall_tau_b': _r(tau), 'kendall_p': _p(tp),
                         'n_compounds': n})
        # partial spearman (all_rows only)
        d = s.dropna(subset=['y_all', 'x_log10_bigram', 'token_count',
                             'word1_count'])
        for zcol, zlabel in [('token_count', 'compound_token_count'),
                             ('word1_count', 'word1_unigram_count')]:
            if len(d) >= 4 and d[zcol].nunique() > 1:
                pr, raw = _partial_spearman(d['x_log10_bigram'], d['y_all'],
                                            d[zcol])
            else:
                pr = raw = np.nan
            part.append({'suite': suite, 'corpus_index': idx,
                         'control': zlabel,
                         'partial_rho': _r(pr), 'raw_rho': _r(raw),
                         'n_compounds': len(d)})
        # secondary (max scale) + sensitivity (weighted)
        for name, ycol, bucket in [('secondary_maxscale', 'y_maxscale', sec),
                                   ('sensitivity_weighted', 'y_weighted', sens)]:
            d = s.dropna(subset=[ycol, 'x_log10_bigram'])
            if len(d) >= 3 and d[ycol].nunique() > 1:
                rho, p = spearmanr(d['x_log10_bigram'], d[ycol])
            else:
                rho = p = np.nan
            bucket.append({'suite': suite, 'corpus_index': idx,
                           'y_definition': name,
                           'spearman_rho': _r(rho), 'spearman_p': _p(p),
                           'n_compounds': len(d)})
    return (pd.DataFrame(prim), pd.DataFrame(kend), pd.DataFrame(part),
            pd.DataFrame(sec + sens))


def rowlevel_bootstrap(elic, tab, n_boot=2000, seed=0):
    """DESCRIPTIVE ONLY. Row-level Spearman with clustered bootstrap over
    compounds for the CI. No p-value."""
    rng = np.random.default_rng(seed)
    rows = []
    for suite in sorted(tab['suite'].unique()):
        st = tab[tab['suite'] == suite]
        idx = st['corpus_index'].iloc[0] if len(st) else np.nan
        # x must come from THIS suite's rows. Taking it from a table-wide
        # drop_duplicates('compound') silently reused the first suite's
        # x-vector for every other suite (audit finding A4).
        freq_x = st.drop_duplicates('compound').set_index('compound')['x_log10_bigram']
        s = elic[elic['suite'] == suite].copy()
        s['x'] = s['compound'].map(freq_x)
        s['y'] = s['accuracy'].map(STRICT)
        s = s.dropna(subset=['x', 'y'])
        comps = s['compound'].unique()
        point, _ = spearmanr(s['x'], s['y'])
        boots = []
        for _ in range(n_boot):
            pick = rng.choice(comps, size=len(comps), replace=True)
            frames = [s[s['compound'] == c] for c in pick]
            bs = pd.concat(frames, ignore_index=True)
            if bs['x'].nunique() > 1 and bs['y'].nunique() > 1:
                r, _ = spearmanr(bs['x'], bs['y'])
                boots.append(r)
        lo, hi = np.percentile(boots, [2.5, 97.5]) if boots else (np.nan, np.nan)
        rows.append({'suite': suite, 'corpus_index': idx,
                     'rowlevel_spearman_rho': _r(point),
                     'ci95_low': _r(lo), 'ci95_high': _r(hi),
                     'n_rows': int(len(s)), 'n_compounds': int(len(comps)),
                     'n_boot': len(boots)})
    return pd.DataFrame(rows)


# incorrect_markers item counts, transcribed manually from
# docs/findings/criteria_authoring.csv for the predicted-class compounds.
# NOTE: that worksheet has malformed CSV quoting (nested un-doubled quotes),
# so per-field programmatic parsing is unreliable; counts below are read
# directly from the authored text (semicolon-separated items in the
# incorrect_markers cell). Scope = the 12 compounds carrying a DECISIONS
# 2026-07-03 prediction (audit-6 only correlates those).
N_INCORRECT_MARKERS = {
    'sensory_characteristics': 3, 'redundant_entry': 4, 'status_message': 6,
    'error_identification': 4, 'pointer_cancellation': 4, 'landmark_region': 4,
    'focus_management': 4, 'tree_grid': 4,
    'sign_language': 3, 'text_formatting': 4, 'form_field': 4,
    'responsive_design': 3,
}


def audit_criteria_strictness(project_root, tab):
    """Audit 6: incorrect_markers count per row vs predicted trajectory class.
    Defuses the 'criteria tuned to fulfill predictions' objection — a near-zero
    correlation means strictness does not track the predicted outcome."""
    rows = []
    for comp, pred in PREDICTED_CLASS.items():
        rows.append({'freq_compound': comp,
                     'n_incorrect_markers': N_INCORRECT_MARKERS[comp],
                     'pred_class': pred,
                     'pred_ordinal': TRAJ_ORDINAL[pred]})
    aw = pd.DataFrame(rows)
    if len(aw) >= 4 and aw['n_incorrect_markers'].nunique() > 1:
        rho, p = spearmanr(aw['n_incorrect_markers'], aw['pred_ordinal'])
    else:
        rho = p = np.nan
    return (aw[['freq_compound', 'n_incorrect_markers', 'pred_class']],
            {'spearman_rho': _r(rho), 'p': _r(p), 'n': int(len(aw)),
             'mean_markers_predicted_fail': round(
                 aw[aw.pred_ordinal == 0]['n_incorrect_markers'].mean(), 2),
             'mean_markers_predicted_climb': round(
                 aw[aw.pred_ordinal == 3]['n_incorrect_markers'].mean(), 2)})


def audit_trajectory_stability(elic):
    """Audit 7: does each compound's trajectory class survive flipping the
    single most influential response one adjacent code level?"""
    rows = []
    for suite, order in SCALE_ORDERS.items():
        s = elic[elic['suite'] == suite]
        for comp in sorted(s['compound'].unique()):
            sub = s[s['compound'] == comp]
            series = []
            codes = []
            for scale in order:
                cell = sub[sub['scale_label'] == scale]
                if len(cell):
                    code = cell.iloc[0]['accuracy']
                    series.append(ORDINAL.get(code, np.nan))
                    codes.append((len(series) - 1, ORDINAL.get(code, np.nan)))
                else:
                    series.append(np.nan)
            base = _classify_trajectory(series)
            stable = True
            for idx, val in codes:
                if pd.isna(val):
                    continue
                for nv in (val + 1, val - 1):
                    if 0 <= nv <= 2:
                        pert = list(series)
                        pert[idx] = nv
                        if _classify_trajectory(pert) != base:
                            stable = False
                            break
                if not stable:
                    break
            rows.append({'suite': suite, 'compound': comp,
                         'trajectory': base, 'stable': stable})
    return pd.DataFrame(rows)


def _r(v):
    """Round a correlation coefficient to 4dp. Coefficients only."""
    return round(float(v), 4) if v is not None and not pd.isna(v) else np.nan


def _p(v):
    """Keep a p-value at full precision.

    Never round a p-value to 4dp: a true p = 1.8e-05 rounds to 0.0 and ships as
    'p = 0.0', which is both wrong and unpublishable (audit finding A22). CSVs
    carry the full float; format at the point of display.
    """
    return float(v) if v is not None and not pd.isna(v) else np.nan


SUITES = ('pythia', 'gpt2', 'olmo')


def run_suite(project_root, suite):
    """Primary + robustness for ONE suite, from that suite's frequency table.

    Writes nothing. `run` is the only writer; this is what the frequency
    notebooks call to see their suite's numbers.

    Returns:
        dict with compound_table, primary, kendall, partial,
        secondary_sensitivity, rowlevel, corpus_index, elic.
    """
    tab, elic, corpus_index = build_compound_table(project_root, suite)
    prim, kend, part, secsens = primary_and_robustness(tab)
    boot = rowlevel_bootstrap(elic, tab) if len(tab) else pd.DataFrame()
    return dict(compound_table=tab, primary=prim, kendall=kend, partial=part,
                secondary_sensitivity=secsens, rowlevel=boot,
                corpus_index=corpus_index, elic=elic)


def run(project_root, suites=SUITES):
    """Run every suite that has a frequency table and write the outputs.

    One filename, one writer: this function is the only writer of every file
    below. A second Spearman implementation in src/frequency.py wrote to
    spearman_summary.csv until 2026-08-09, so the file under the authoritative
    name held whichever estimator ran last. CLAIMS A3 cites spearman_summary.csv
    for rho = 0.5715 / 0.5052 — this function's numbers.

    Suites without a per-suite frequency table are reported and skipped, not
    silently omitted.
    """
    project_root = Path(project_root)
    out_f = project_root / 'results' / 'frequency'
    out_a = project_root / 'results' / 'analysis'

    per_suite, missing = {}, []
    for suite in suites:
        try:
            per_suite[suite] = run_suite(project_root, suite)
        except FileNotFoundError as e:
            missing.append(suite)
            print(f'{suite}: SKIPPED — {e}')

    if not per_suite:
        raise RuntimeError('no suite had a frequency table; nothing to compute')

    def cat(key):
        frames = [r[key] for r in per_suite.values() if len(r[key])]
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    tab = cat('compound_table')
    prim, kend = cat('primary'), cat('kendall')
    part, secsens, boot = cat('partial'), cat('secondary_sensitivity'), cat('rowlevel')

    elic_all = pd.concat([r['elic'] for r in per_suite.values()],
                         ignore_index=True)
    strict_tab, strict_summary = audit_criteria_strictness(project_root, tab)
    stab = audit_trajectory_stability(elic_all)

    # Save (bigram raw stays out of chat; x is log10 in the substrate)
    tab.to_csv(out_f / 'compound_accuracy_table.csv', index=False)
    prim.to_csv(out_f / 'spearman_summary.csv', index=False)     # PRIMARY
    kend.to_csv(out_f / 'spearman_kendall.csv', index=False)
    part.to_csv(out_f / 'spearman_partial.csv', index=False)
    secsens.to_csv(out_f / 'spearman_secondary_sensitivity.csv', index=False)
    boot.to_csv(out_f / 'spearman_rowlevel_bootstrap.csv', index=False)
    strict_tab.to_csv(out_a / 'criteria_strictness_audit.csv', index=False)
    stab.to_csv(out_a / 'trajectory_stability_audit.csv', index=False)

    print(f'\nsuites computed: {sorted(per_suite)}')
    if missing:
        print(f'suites MISSING a frequency table (no statistic written): {missing}')
    print('corpus index per suite: ' +
          ', '.join(f'{s}={r["corpus_index"]}' for s, r in per_suite.items()))

    return dict(compound_table=tab, primary=prim, kendall=kend, partial=part,
                secondary_sensitivity=secsens, rowlevel=boot,
                strictness=strict_summary, strictness_tab=strict_tab,
                stability=stab, per_suite=per_suite, missing=missing)


if __name__ == '__main__':
    root = Path(__file__).parent.parent
    R = run(root)
    pd.set_option('display.width', 200)
    print('\n=== PRIMARY: compound-level Spearman (strict binary y) ===')
    print(R['primary'].to_string(index=False))
    print('\n=== Kendall tau-b ===')
    print(R['kendall'].to_string(index=False))
    print('\n=== Partial Spearman (all_rows) ===')
    print(R['partial'].to_string(index=False))
    print('\n=== Secondary (max-scale) + Sensitivity (weighted) ===')
    print(R['secondary_sensitivity'].to_string(index=False))
    print('\n=== Row-level (DESCRIPTIVE ONLY; clustered bootstrap CI; no p) ===')
    print(R['rowlevel'].to_string(index=False))
    print('\n=== Audit 6 — criteria strictness vs predicted class ===')
    print(R['strictness'])
    print('\n=== Audit 7 — trajectory-class stability ===')
    st = R['stability']
    print(f"stable {int(st['stable'].sum())}/{len(st)}; unstable:",
          list(st[~st['stable']].apply(lambda r: f"{r['suite']}:{r['compound']}", axis=1)))
