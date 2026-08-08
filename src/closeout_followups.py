"""Post-review closeout computations (cc-followups-2026-07-04).

FOUR closeout items from the ratified Spearman review verdicts
(docs/findings/spearman-review-verdicts-2026-07-03.md). These are
CLOSEOUT COMPUTATIONS over already-frozen artifacts, NOT new experiments:
every input is a committed CSV from the n=49 pipeline (commit ca0319e) or
the frozen worksheet (commit 42695be). The primary pipeline
(src/dual_spearman.py) is deliberately NOT touched.

  1. Strictness audit, FULL worksheet -> results/analysis/
     criteria_strictness_audit_full.csv  (all 41 authored rows; the frozen
     12-row criteria_strictness_audit.csv is reproduced exactly as a guard)
  2. Scorecard base rate -> results/frequency/scorecard_base_rate.csv
     (chance-firing denominator for the 4/7 attractor hit rate)
  3. Failed ceiling anchors -> prose (docs/findings/); numbers emitted here
  4. S4 PMI robustness -> results/frequency/spearman_pmi_robustness.csv

Run:  PYTHONPATH=. python -m src.closeout_followups
"""
from pathlib import Path
import csv
import math

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

CONCEPT_TO_COMPOUND = {
    "screen reader": "screen_reader", "alt text": "alt_text",
    "skip link": "skip_link", "color contrast": "color_contrast",
    "keyboard navigation": "keyboard_navigation",
    "focus indicator": "focus_indicator", "semantic HTML": "semantic_html",
    "captions": "closed_captions", "closed captions": "closed_captions",
    "WCAG": "WCAG", "ARIA": "ARIA",
}

# --- Pre-registered scaffolding (DECISIONS 2026-07-03) ---------------------
# The 7 token-competition / wrong-domain candidates and their scorecard
# "fired" adjudication (DECISIONS 2026-07-03 scorecard, commit ca0319e).
# fired = the *predicted wrong-domain attractor* surfaced in the outputs.
TOKEN_COMPETITION_CANDIDATES = [
    'sensory_characteristics', 'redundant_entry', 'status_message',
    'error_identification', 'pointer_cancellation', 'landmark_region',
    'focus_management',
]
SCORECARD_FIRED = {  # frozen output-level judgment (attractor appeared)
    'sensory_characteristics': True, 'redundant_entry': True,
    'pointer_cancellation': True, 'landmark_region': True,
    'status_message': False, 'error_identification': False,
    'focus_management': False,
}
# Predicted trajectory class per DECISIONS 2026-07-03 (the failure signature
# the candidates were predicted to show is never_emerges).
PREDICTED_CLASS = {
    'sensory_characteristics': 'never_emerges', 'redundant_entry': 'never_emerges',
    'status_message': 'never_emerges', 'error_identification': 'never_emerges',
    'pointer_cancellation': 'never_emerges', 'landmark_region': 'never_emerges',
    'focus_management': 'never_emerges', 'tree_grid': 'never_emerges',
    'sign_language': 'monotonic_climb', 'text_formatting': 'monotonic_climb',
    'form_field': 'monotonic_climb', 'responsive_design': 'monotonic_climb',
}
CEILING_ANCHORS = ['sign_language', 'text_formatting', 'form_field',
                   'responsive_design']

# Frozen 12-row strictness counts (src/dual_spearman.py, hand-transcribed).
# Used ONLY as a regression check that the programmatic semicolon-count
# reproduces the authored values before we extend to all 41.
FROZEN_12_MARKERS = {
    'sensory_characteristics': 3, 'redundant_entry': 4, 'status_message': 6,
    'error_identification': 4, 'pointer_cancellation': 4, 'landmark_region': 4,
    'focus_management': 4, 'tree_grid': 4,
    'sign_language': 3, 'text_formatting': 4, 'form_field': 4,
    'responsive_design': 3,
}

# criteria_authoring.csv has irregular quoting: 10 rows carry an UNQUOTED
# comma inside a prose/marker field, so csv splits those rows into 12-14
# physical fields and positional field[6] no longer isolates
# incorrect_markers. A row parses to exactly 11 fields IFF its quoting is
# balanced, so the other 31 rows are safe programmatically. For these 10 the
# incorrect_markers cell is reassembled from the split fields and its
# semicolon-separated items counted by hand (house style, per dual_spearman's
# 12). Authored text quoted for audit; redundant_entry & error_identification
# also appear in FROZEN_12 and must agree.
MALFORMED_MARKERS = {
    # inverted sense(...); CAPTIONS CONFUSION(...); circular; degenerate
    'audio_description': 4,
    # archery/shooting/marketing sense(...); circular; degenerate
    'target_size': 3,
    # non-UI touch senses(...); circular; degenerate
    'touch_target': 3,
    # non-UI drag senses(...); circular; degenerate
    'drag_movement': 3,
    # vague consistency restatement(...); helpful-support-staff sense; degenerate
    'consistent_help': 3,
    # database/dedup(...); trench-coat(...); circular; degenerate
    'redundant_entry': 4,
    # security-hardening(...); trench-coat(...); circular; degenerate
    'accessible_authentication': 4,
    # software-debugging(...); trench-coat(...); circular; degenerate
    'error_identification': 4,
    # generic tree-data(...); file-system tree; trench-coat; circular; degenerate
    'accessibility_tree': 5,
    # broadcast-radio sense(...); trench-coat; circular; degenerate
    'radio_group': 4,
}


def _r(v, nd=4):
    return round(float(v), nd) if v is not None and not pd.isna(v) else np.nan


def _comp(concept):
    return CONCEPT_TO_COMPOUND.get(concept, str(concept).replace(' ', '_'))


# --- item 1: strictness audit, full worksheet ------------------------------
def strictness_full(root):
    """Count semicolon-separated items in each row's incorrect_markers cell
    for ALL 41 authored compounds. Rows that parse to exactly 11 fields are
    well-formed -> programmatic count; the 10 irregularly-quoted rows use the
    hand-verified MALFORMED_MARKERS. Regression-checked against the frozen 12."""
    raw = list(csv.reader(open(root / 'docs' / 'findings' /
                               'criteria_authoring.csv')))
    header, data = raw[0], raw[1:]
    ic = header.index('incorrect_markers')
    rows = []
    for r in data:
        comp = r[1]
        if len(r) == len(header):
            cell = (r[ic] or '').strip()
            n = len([p for p in cell.split(';') if p.strip()])
        elif comp in MALFORMED_MARKERS:
            n = MALFORMED_MARKERS[comp]
        else:
            raise AssertionError(
                f"{comp}: {len(r)} fields but no MALFORMED_MARKERS entry")
        rows.append({'freq_compound': comp, 'n_incorrect_markers': n,
                     'pred_class': PREDICTED_CLASS.get(comp, '')})
    df = pd.DataFrame(rows)
    if len(df) != 41:
        raise AssertionError(f"expected 41 authored rows, got {len(df)}")

    # REGRESSION GUARD: extended count must reproduce the frozen 12 exactly.
    got = df.set_index('freq_compound')['n_incorrect_markers']
    mism = {c: (int(got.loc[c]), exp) for c, exp in FROZEN_12_MARKERS.items()
            if int(got.loc[c]) != exp}
    if mism:
        raise AssertionError(f"strictness count regression: {mism}")
    return df


# --- item 2: scorecard base rate -------------------------------------------
def scorecard_base_rate(root):
    """Chance-firing denominator for the 4/7 attractor hit rate.

    The scorecard's 'fired' = the *specific predicted wrong-domain attractor*
    surfaced in the outputs (an output-level read). That event is NOT
    reproducible from the frozen CSVs and is NOT any trajectory/accuracy
    threshold: landmark_region (fired) and focus_management (did-not-fire)
    have identical strict accuracy. So the mechanically-computable base rate
    is built on the pre-registered FAILURE SIGNATURE the candidates were
    predicted to show -> never_emerges trajectory class."""
    tr = list(csv.DictReader(open(root / 'results' / 'analysis' /
                                  'per_concept_trajectories.csv')))
    traj = {}
    for r in tr:
        traj.setdefault(_comp(r['concept']), {})[r['suite']] = r['trajectory']

    auth = [r['freq_compound'] for r in csv.DictReader(
        open(root / 'docs' / 'findings' / 'criteria_authoring.csv'))]

    def ne(c, s):
        return traj.get(c, {}).get(s) == 'never_emerges'

    rows = []
    for c in auth:
        p, g = ne(c, 'pythia'), ne(c, 'gpt2')
        rows.append({
            'compound': c,
            'traj_pythia': traj.get(c, {}).get('pythia', ''),
            'traj_gpt2': traj.get(c, {}).get('gpt2', ''),
            'never_emerges_pythia': int(p),
            'never_emerges_gpt2': int(g),
            'fired_signature_both': int(p and g),
            'fired_signature_either': int(p or g),
            'predicted_candidate': int(c in TOKEN_COMPETITION_CANDIDATES),
        })
    df = pd.DataFrame(rows)
    n = len(df)
    summary = {
        'n_compounds': n,
        'base_rate_ne_pythia': f"{int(df.never_emerges_pythia.sum())}/{n}",
        'base_rate_ne_gpt2': f"{int(df.never_emerges_gpt2.sum())}/{n}",
        'base_rate_ne_both': f"{int(df.fired_signature_both.sum())}/{n}",
        'base_rate_ne_either': f"{int(df.fired_signature_either.sum())}/{n}",
        'candidates_ne_both':
            f"{int(df[df.predicted_candidate==1].fired_signature_both.sum())}/7",
        'candidates_ne_either':
            f"{int(df[df.predicted_candidate==1].fired_signature_either.sum())}/7",
        'scorecard_fired_attractor_level': "4/7 (output-level; not mechanical)",
    }
    return df, summary


# --- item 3: ceiling anchor read -------------------------------------------
def ceiling_anchor_read(root):
    tab = pd.read_csv(root / 'results' / 'frequency' /
                      'compound_accuracy_table.csv')
    rows = []
    for c in CEILING_ANCHORS:
        for suite in ['pythia', 'gpt2']:
            r = tab[(tab.compound == c) & (tab.suite == suite)].iloc[0]
            rows.append({'compound': c, 'suite': suite,
                         'x_log10_bigram': _r(r.x_log10_bigram, 3),
                         'y_all': _r(r.y_all, 3),
                         'y_maxscale': _r(r.y_maxscale, 3)})
    return pd.DataFrame(rows)


# --- item 4: S4 PMI robustness ---------------------------------------------
def pmi_robustness(root):
    """Spearman using PMI (association strength) in place of raw log10 bigram
    count. Compound level, both suites, all-rows y (strict binary).

    PMI = log2( P(w1,w2) / (P(w1) P(w2)) )
        = log2( bigram_count * N / (word1_count * word2_count) ).
    For Spearman the additive log2(N) corpus-size constant is identical
    across compounds and rank-invariant, so it does not affect rho. We report
    the rank-invariant PMI kernel  log2( bigram / (w1*w2) )  and label it."""
    freq = pd.read_csv(root / 'results' / 'frequency' / 'frequency_table.csv')
    freq = freq[freq.domain == 'accessibility'].copy()
    freq['pmi'] = np.log2(freq.bigram_count /
                          (freq.word1_count.astype(float) * freq.word2_count))
    pmi = freq.set_index('compound')['pmi']

    tab = pd.read_csv(root / 'results' / 'frequency' /
                      'compound_accuracy_table.csv')
    rows = []
    for suite in ['pythia', 'gpt2']:
        s = tab[tab.suite == suite].copy()
        s['pmi'] = s.compound.map(pmi)
        d = s.dropna(subset=['pmi', 'y_all', 'x_log10_bigram'])
        rho_pmi, p_pmi = spearmanr(d.pmi, d.y_all)
        rho_raw, p_raw = spearmanr(d.x_log10_bigram, d.y_all)      # reproduce primary
        rho_xx, _ = spearmanr(d.pmi, d.x_log10_bigram)             # how different is PMI ordering
        rows.append({'suite': suite,
                     'spearman_rho_pmi': _r(rho_pmi), 'p_pmi': _r(p_pmi),
                     'spearman_rho_rawbigram': _r(rho_raw), 'p_rawbigram': _r(p_raw),
                     'rho_pmi_vs_rawbigram': _r(rho_xx),
                     'n_compounds': int(len(d))})
    return pd.DataFrame(rows)


def run(root):
    root = Path(root)
    out_f = root / 'results' / 'frequency'
    out_a = root / 'results' / 'analysis'

    s_full = strictness_full(root)
    base_df, base_summary = scorecard_base_rate(root)
    ceil = ceiling_anchor_read(root)
    pmi = pmi_robustness(root)

    s_full.to_csv(out_a / 'criteria_strictness_audit_full.csv', index=False)

    # scorecard base rate: state the 'fired' operationalization in the header
    # (cc-followups item 2). Comment-prefixed so pandas(comment='#') skips it.
    base_header = (
        "# scorecard base rate (cc-followups item 2). FIRED := the pre-registered\n"
        "# FAILURE SIGNATURE the 7 token-competition candidates were predicted to\n"
        "# show = never_emerges trajectory class (per_concept_trajectories.csv,\n"
        "# commit ca0319e), computed per suite over all 41 expansion compounds.\n"
        "# NOTE: this is NOT the scorecard's output-level 'fired' (= the specific\n"
        "# predicted wrong-domain attractor surfaced), which is not reproducible\n"
        "# from frozen CSVs: landmark_region (scorecard-fired) and focus_management\n"
        "# (scorecard-not-fired) have identical strict accuracy. never_emerges is a\n"
        "# CONSERVATIVE (broader) proxy -> a ceiling on the chance-firing rate.\n"
        f"# base rate never_emerges: pythia {int(base_df.never_emerges_pythia.sum())}/41, "
        f"gpt2 {int(base_df.never_emerges_gpt2.sum())}/41, "
        f"both {int(base_df.fired_signature_both.sum())}/41, "
        f"either {int(base_df.fired_signature_either.sum())}/41.\n"
        f"# predicted candidates: both {int(base_df[base_df.predicted_candidate==1].fired_signature_both.sum())}/7, "
        f"either {int(base_df[base_df.predicted_candidate==1].fired_signature_either.sum())}/7; "
        "scorecard attractor-level 4/7.\n")
    path = out_f / 'scorecard_base_rate.csv'
    path.write_text(base_header + base_df.to_csv(index=False))

    pmi.to_csv(out_f / 'spearman_pmi_robustness.csv', index=False)
    return dict(strictness_full=s_full, base_df=base_df,
                base_summary=base_summary, ceiling=ceil, pmi=pmi)


if __name__ == '__main__':
    root = Path(__file__).parent.parent
    R = run(root)
    pd.set_option('display.width', 200)
    print('=== ITEM 1: strictness, full worksheet (41 rows; frozen-12 guard PASSED) ===')
    print(R['strictness_full'].to_string(index=False))
    print(f"\n  markers range {R['strictness_full'].n_incorrect_markers.min()}"
          f"-{R['strictness_full'].n_incorrect_markers.max()}, "
          f"mean {R['strictness_full'].n_incorrect_markers.mean():.2f}")
    print('\n=== ITEM 2: scorecard base rate ===')
    for k, v in R['base_summary'].items():
        print(f'  {k}: {v}')
    print('\n=== ITEM 3: ceiling anchors ===')
    print(R['ceiling'].to_string(index=False))
    print('\n=== ITEM 4: PMI robustness ===')
    print(R['pmi'].to_string(index=False))
