"""
Gap analysis — produces coded accuracy tables and summary statistics.

Run from project root:
    python -m src.gap_analysis

Or import in notebook:
    from src.gap_analysis import run_gap_analysis
    tables = run_gap_analysis(PROJECT_ROOT)

Depends on:
    src.analysis.load_all_results — loads raw CSVs
    src.accuracy_coding.code_response — applies coding rules
"""

from pathlib import Path
import pandas as pd

from src.analysis import load_all_results, scale_label
from src.accuracy_coding import code_response


PYTHIA_SCALE_ORDER = ['160M', '410M', '1B', '2.8B', '6.9B', '12B']
GPT2_SCALE_ORDER = ['124M', '355M', '774M', '1.5B']
SCORE_MAP = {'correct': 2, 'partial': 1, 'incorrect': 0}


def run_gap_analysis(project_root):
    """
    Run full gap analysis and return dict of DataFrames.
    Optionally saves to results/analysis/.
    """
    project_root = Path(project_root)
    elicitation, entropy, binding = load_all_results(project_root)

    # Add scale labels
    elicitation['scale_label'] = elicitation['scale'].apply(scale_label)
    if not entropy.empty:
        entropy['scale_label'] = entropy['scale'].apply(scale_label)
    if not binding.empty:
        binding['scale_label'] = binding['scale'].apply(scale_label)

    # Apply accuracy coding
    elicitation['accuracy'] = elicitation.apply(
        lambda r: code_response(
            r['prompt_type'], r['concept'], r['prompt'], r['output']
        ),
        axis=1
    )

    tables = {}

    for suite_name, suite_filter, col_order in [
        ('pythia', 'pythia', PYTHIA_SCALE_ORDER),
        ('gpt2', 'gpt2', GPT2_SCALE_ORDER),
    ]:
        subset = elicitation[elicitation['suite'] == suite_filter]

        # Declarative accuracy pivot
        decl = subset[subset['prompt_type'] == 'declarative']
        decl_pivot = decl.pivot_table(
            index='concept', columns='scale_label',
            values='accuracy', aggfunc='first'
        )
        decl_pivot = decl_pivot[[c for c in col_order if c in decl_pivot.columns]]
        tables[f'{suite_name}_declarative'] = decl_pivot

        # Evaluative accuracy pivot
        evalu = subset[subset['prompt_type'] == 'evaluative']
        eval_pivot = evalu.pivot_table(
            index='concept', columns='scale_label',
            values='accuracy', aggfunc='first'
        )
        eval_pivot = eval_pivot[[c for c in col_order if c in eval_pivot.columns]]
        tables[f'{suite_name}_evaluative'] = eval_pivot

        # Gap scores per scale
        gap_rows = []
        for scale in col_order:
            if scale in decl_pivot.columns and scale in eval_pivot.columns:
                d_score = decl_pivot[scale].map(SCORE_MAP).mean()
                e_score = eval_pivot[scale].map(SCORE_MAP).mean()
                gap_rows.append({
                    'scale': scale,
                    'declarative_score': round(d_score, 4),
                    'evaluative_score': round(e_score, 4),
                    'gap': round(d_score - e_score, 4),
                    'declarative_pct': round(d_score / 2 * 100, 1),
                    'evaluative_pct': round(e_score / 2 * 100, 1),
                    'gap_pct_pts': round((d_score - e_score) / 2 * 100, 1),
                })
        tables[f'{suite_name}_gap'] = pd.DataFrame(gap_rows)

    # Emergence thresholds (cross-architecture)
    emergence_rows = []
    for concept in sorted(elicitation['concept'].unique()):
        row = {'concept': concept}
        for suite_name, suite_filter, col_order in [
            ('pythia', 'pythia', PYTHIA_SCALE_ORDER),
            ('gpt2', 'gpt2', GPT2_SCALE_ORDER),
        ]:
            emerged = 'never'
            for scale in col_order:
                matches = elicitation[
                    (elicitation['suite'] == suite_filter) &
                    (elicitation['scale_label'] == scale) &
                    (elicitation['concept'] == concept) &
                    (elicitation['prompt_type'] == 'declarative')
                ]
                if len(matches) > 0:
                    coded = code_response(
                        'declarative', concept,
                        matches.iloc[0]['prompt'],
                        matches.iloc[0]['output']
                    )
                    if coded == 'correct':
                        emerged = scale
                        break
            row[f'{suite_name}_emergence'] = emerged
        emergence_rows.append(row)
    tables['emergence_thresholds'] = pd.DataFrame(emergence_rows)

    # Full coded elicitation (for traceability)
    tables['elicitation_coded'] = elicitation

    # Extended analyses (read existing entropy/binding CSVs, no new experiments)
    tables.update(run_extended_analysis(elicitation, entropy, binding))

    return tables


# ---------------------------------------------------------------------------
# Extended analyses
#
# These read the existing entropy/binding/results CSVs (no new experiments).
# Each produces a self-describing, figure-ready table saved to results/analysis/.
# Outputs are intentionally interpretation-free (raw numbers, explicit n) so
# the structure is recoverable from the data alone.
# ---------------------------------------------------------------------------

SCALE_ORDERS = {'pythia': PYTHIA_SCALE_ORDER, 'gpt2': GPT2_SCALE_ORDER}


def _concept_to_compound(concept):
    """Map an accuracy-coding concept (space form) to a binding compound
    (snake_case). Single-token concepts (ARIA, WCAG, HTML) have no binding
    compound and simply won't join."""
    special = {'captions': 'closed_captions', 'closed captions': 'closed_captions'}
    c = str(concept).strip().lower()
    return special.get(c, c.replace(' ', '_'))


def _is_degenerate(text):
    """Flag degenerate repetition: the same 1-4 word phrase repeated three or
    more times consecutively (e.g. 'a link that is not a link that is not a
    link', or 'logo.png logo.png logo.png')."""
    words = str(text).split()
    for n in (1, 2, 3, 4):
        for i in range(len(words) - 3 * n + 1):
            seg = words[i:i + n]
            if words[i + n:i + 2 * n] == seg and words[i + 2 * n:i + 3 * n] == seg:
                return True
    return False


def run_extended_analysis(elicitation, entropy_df, binding_df):
    """Run all six extended analyses and return a dict of tables."""
    tables = {}
    by, fw = entropy_confidence_tables(elicitation, entropy_df)
    tables['entropy_confidence'] = by                 # ext 1
    tables['fluent_wrongness'] = fw                   # ext 1 (focused)

    pairs, corr = binding_accuracy_tables(elicitation, binding_df)
    tables['binding_vs_accuracy'] = pairs             # ext 2
    tables['binding_accuracy_corr'] = corr            # ext 2 (correlation)

    scaling, traj = per_concept_scaling_tables(elicitation)
    tables['per_concept_scaling'] = scaling           # ext 3 (figure-ready)
    tables['per_concept_trajectories'] = traj         # ext 3 (classified)

    tables['entropy_divergence'] = entropy_divergence_table(entropy_df)  # ext 4

    deg_scale, deg_concept, deg_ptype = degenerate_tables(elicitation)
    tables['degenerate_by_scale'] = deg_scale         # ext 5
    tables['degenerate_by_concept'] = deg_concept     # ext 5
    tables['degenerate_by_prompt_type'] = deg_ptype   # ext 5

    tables['completion_paradox'] = completion_paradox_table(elicitation)  # ext 6

    tables['accuracy_by_prompt_type'] = accuracy_by_prompt_type_table(elicitation)
    return tables


def accuracy_by_prompt_type_table(elicitation):
    """Coverage + accuracy across ALL prompt types and scales.

    With validation/hypothesis/control now coded, this surfaces every coded
    response (not just declarative/evaluative) without redefining the
    concept-level tables. Note: non-bicycle 'control' rows are accessibility-
    concept probes; bicycle 'control' is the reasoning baseline.
    """
    df = elicitation.copy()
    df['score'] = df['accuracy'].map(SCORE_MAP)

    rows = []
    for suite, order in SCALE_ORDERS.items():
        s = df[df['suite'] == suite]
        for scale in order:
            for ptype in sorted(s['prompt_type'].dropna().unique()):
                cell = s[(s['scale_label'] == scale) & (s['prompt_type'] == ptype)]
                if len(cell) == 0:
                    continue
                coded = cell[cell['accuracy'] != 'uncoded']
                rows.append({
                    'suite': suite, 'scale': scale, 'prompt_type': ptype,
                    'n': len(cell),
                    'n_coded': len(coded),
                    'n_uncoded': int((cell['accuracy'] == 'uncoded').sum()),
                    'accuracy_pct': round(coded['score'].mean() / 2 * 100, 1)
                    if len(coded) else None,
                })
    return pd.DataFrame(rows)


def entropy_confidence_tables(elicitation, entropy_df):
    """Ext 1 — entropy as a confidence metric ('fluent wrongness').

    Joins last-token entropy onto coded responses, then reports mean entropy
    by concept x scale x accuracy. The focused table compares the model's
    confidence when WRONG on accessibility vs when RIGHT on the bicycle
    control — lower entropy on accessibility errors is fluent wrongness.
    """
    if entropy_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    e = entropy_df[['model', 'prompt_id', 'last_token_entropy', 'mean_entropy']]
    e = e.drop_duplicates(['model', 'prompt_id'])
    merged = elicitation.merge(e, on=['model', 'prompt_id'], how='left')

    by = merged.groupby(
        ['suite', 'concept', 'scale_label', 'accuracy'], as_index=False
    ).agg(
        n=('last_token_entropy', 'size'),
        mean_last_token_entropy=('last_token_entropy', 'mean'),
        mean_entropy=('mean_entropy', 'mean'),
    )
    by['mean_last_token_entropy'] = by['mean_last_token_entropy'].round(4)
    by['mean_entropy'] = by['mean_entropy'].round(4)

    fw_rows = []
    for suite, order in SCALE_ORDERS.items():
        s = merged[merged['suite'] == suite]
        for scale in order:
            ss = s[s['scale_label'] == scale]
            wrong = ss[(ss['concept'] != 'bicycle') &
                       (ss['accuracy'] == 'incorrect')]['last_token_entropy'].dropna()
            ctrl = ss[(ss['concept'] == 'bicycle') &
                      (ss['accuracy'] == 'correct')]['last_token_entropy'].dropna()
            if len(wrong) == 0 and len(ctrl) == 0:
                continue
            w_mean = wrong.mean() if len(wrong) else None
            c_mean = ctrl.mean() if len(ctrl) else None
            fw_rows.append({
                'suite': suite, 'scale': scale,
                'n_access_incorrect': len(wrong),
                'access_incorrect_entropy': round(w_mean, 4) if w_mean is not None else None,
                'n_control_correct': len(ctrl),
                'control_correct_entropy': round(c_mean, 4) if c_mean is not None else None,
                # negative => model is MORE confident (lower entropy) when wrong
                'confidence_gap': round(w_mean - c_mean, 4)
                if (w_mean is not None and c_mean is not None) else None,
            })
    return by, pd.DataFrame(fw_rows)


def binding_accuracy_tables(elicitation, binding_df):
    """Ext 2 — binding depth vs accuracy.

    Pairs the max binding score per concept x scale with the declarative
    accuracy score, and reports Pearson/Spearman correlation per suite.
    Only the 11 multi-word compounds have binding data (single-token
    concepts like ARIA/WCAG cannot have cross-token binding).
    """
    if binding_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    idx = binding_df.groupby(['suite', 'scale', 'compound'])['binding_score'].idxmax()
    maxb = binding_df.loc[idx][
        ['suite', 'scale', 'compound', 'layer', 'head', 'binding_score']
    ].rename(columns={'layer': 'binding_layer', 'head': 'binding_head',
                      'binding_score': 'max_binding'})

    decl = elicitation[elicitation['prompt_type'] == 'declarative'].copy()
    decl['score'] = decl['accuracy'].map(SCORE_MAP)
    decl['compound'] = decl['concept'].apply(_concept_to_compound)
    acc = decl.groupby(['suite', 'scale', 'scale_label', 'compound'], as_index=False).agg(
        accuracy_score=('score', 'mean')
    )

    pairs = acc.merge(maxb, on=['suite', 'scale', 'compound'], how='inner')
    pairs['accuracy_score'] = pairs['accuracy_score'].round(3)
    pairs['max_binding'] = pairs['max_binding'].round(4)
    pairs = pairs.sort_values(['suite', 'compound', 'scale']).reset_index(drop=True)

    corr_rows = []
    for suite in sorted(pairs['suite'].unique()):
        sub = pairs[pairs['suite'] == suite]
        pear = sub['max_binding'].corr(sub['accuracy_score']) if len(sub) >= 3 else None
        spear = (sub['max_binding'].corr(sub['accuracy_score'], method='spearman')
                 if len(sub) >= 3 else None)
        corr_rows.append({
            'suite': suite, 'n_pairs': len(sub),
            'pearson_r': round(pear, 3) if pd.notna(pear) else None,
            'spearman_r': round(spear, 3) if pd.notna(spear) else None,
        })
    return pairs, pd.DataFrame(corr_rows)


def _classify_trajectory(values):
    """Classify a per-scale score sequence into a trajectory type."""
    vals = [v for v in values if pd.notna(v)]
    if not vals:
        return 'no_data'
    mx = max(vals)
    if mx < 2:                                   # never reaches 'correct'
        return 'never_emerges'
    non_decreasing = all(b >= a - 1e-9 for a, b in zip(vals, vals[1:]))
    if non_decreasing and vals[-1] >= mx - 1e-9:
        return 'monotonic_climb'
    peak_idx = vals.index(mx)
    if peak_idx < len(vals) - 1 and vals[-1] < mx - 1e-9:
        return 'peak_regress'
    return 'mixed'


def per_concept_scaling_tables(elicitation):
    """Ext 3 — per-concept scaling curves + trajectory classification.

    Long figure-ready table (suite x concept x scale -> declarative score),
    plus a wide table classifying each concept's trajectory as
    monotonic_climb / peak_regress / never_emerges / mixed.
    """
    decl = elicitation[elicitation['prompt_type'] == 'declarative'].copy()
    decl['score'] = decl['accuracy'].map(SCORE_MAP)

    long_rows, traj_rows = [], []
    for suite, order in SCALE_ORDERS.items():
        s = decl[decl['suite'] == suite]
        for concept in sorted(s['concept'].unique()):
            series = {}
            for scale in order:
                cell = s[(s['scale_label'] == scale) & (s['concept'] == concept)]['score']
                val = cell.mean() if len(cell) else None
                series[scale] = round(val, 3) if val is not None else None
                long_rows.append({
                    'suite': suite, 'concept': concept, 'scale': scale,
                    'declarative_score': series[scale],
                    'declarative_pct': round(val / 2 * 100, 1) if val is not None else None,
                })
            row = {'suite': suite, 'concept': concept,
                   'trajectory': _classify_trajectory([series[s_] for s_ in order])}
            row.update(series)
            traj_rows.append(row)
    return pd.DataFrame(long_rows), pd.DataFrame(traj_rows)


def entropy_divergence_table(entropy_df):
    """Ext 4 — declarative vs evaluative entropy divergence per scale.

    If evaluative entropy rises (or stays high) relative to declarative as
    scale grows, the model is internally signaling uncertainty on the task
    it behaviorally fails — the declarative-evaluative gap, seen internally.
    """
    if entropy_df.empty:
        return pd.DataFrame()

    rows = []
    for suite, order in SCALE_ORDERS.items():
        s = entropy_df[entropy_df['suite'] == suite]
        for scale in order:
            ss = s[s['scale_label'] == scale]
            d = ss[ss['prompt_type'] == 'declarative']['last_token_entropy'].dropna()
            ev = ss[ss['prompt_type'] == 'evaluative']['last_token_entropy'].dropna()
            if len(d) == 0 and len(ev) == 0:
                continue
            d_mean = d.mean() if len(d) else None
            e_mean = ev.mean() if len(ev) else None
            rows.append({
                'suite': suite, 'scale': scale,
                'declarative_entropy': round(d_mean, 4) if d_mean is not None else None,
                'evaluative_entropy': round(e_mean, 4) if e_mean is not None else None,
                'entropy_gap': round(e_mean - d_mean, 4)
                if (d_mean is not None and e_mean is not None) else None,
            })
    return pd.DataFrame(rows)


def degenerate_tables(elicitation):
    """Ext 5 — degenerate (repetitive) output detection.

    Flags repeated-phrase collapse and reports the rate by scale, concept,
    and prompt type.
    """
    df = elicitation.copy()
    df['degenerate'] = df['output'].apply(_is_degenerate)

    def _rate(group_cols):
        g = df.groupby(group_cols, as_index=False).agg(
            n=('degenerate', 'size'),
            n_degenerate=('degenerate', 'sum'),
        )
        g['pct_degenerate'] = (g['n_degenerate'] / g['n'] * 100).round(1)
        return g

    return (_rate(['suite', 'scale_label']),
            _rate(['concept']),
            _rate(['prompt_type']))


def completion_paradox_table(elicitation):
    """Ext 6 — the completion paradox.

    Per concept x scale, compares few-shot completion accuracy (syntactic
    pattern-matching) against declarative accuracy (conceptual knowledge).
    A positive paradox_gap means the model completes the syntax correctly at
    scales where it cannot define the concept.
    """
    df = elicitation.copy()
    df['score'] = df['accuracy'].map(SCORE_MAP)

    rows = []
    for suite, order in SCALE_ORDERS.items():
        s = df[df['suite'] == suite]
        concepts = sorted(
            set(s[s['prompt_type'] == 'completion']['concept']) |
            set(s[s['prompt_type'] == 'declarative']['concept'])
        )
        for concept in concepts:
            for scale in order:
                cell = s[(s['scale_label'] == scale) & (s['concept'] == concept)]
                comp = cell[cell['prompt_type'] == 'completion']['score']
                decl = cell[cell['prompt_type'] == 'declarative']['score']
                if len(comp) == 0 and len(decl) == 0:
                    continue
                c_mean = comp.mean() if len(comp) else None
                d_mean = decl.mean() if len(decl) else None
                rows.append({
                    'suite': suite, 'concept': concept, 'scale': scale,
                    'completion_pct': round(c_mean / 2 * 100, 1) if c_mean is not None else None,
                    'declarative_pct': round(d_mean / 2 * 100, 1) if d_mean is not None else None,
                    'paradox_gap_pct_pts': round((c_mean - d_mean) / 2 * 100, 1)
                    if (c_mean is not None and d_mean is not None) else None,
                })
    return pd.DataFrame(rows)


def save_tables(tables, output_dir):
    """Save all analysis tables to CSV.

    Pivot tables carry a meaningful (named) index, so it is written; the
    long/figure-ready tables use a default RangeIndex, which is dropped to
    keep the CSVs clean for downstream (and blind-study) consumption.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, df in tables.items():
        path = output_dir / f'{name}.csv'
        write_index = not isinstance(df.index, pd.RangeIndex)
        df.to_csv(path, index=write_index)
        print(f"  {path.name}: {len(df)} rows")


def print_summary(tables):
    """Print a human-readable summary of the gap analysis."""

    for suite in ['pythia', 'gpt2']:
        suite_upper = suite.upper()

        # Declarative
        print(f"\n{'='*70}")
        print(f"{suite_upper} DECLARATIVE ACCURACY")
        print(f"{'='*70}")
        print(tables[f'{suite}_declarative'].to_string())

        # Evaluative
        print(f"\n{'='*70}")
        print(f"{suite_upper} EVALUATIVE ACCURACY")
        print(f"{'='*70}")
        print(tables[f'{suite}_evaluative'].to_string())

        # Gap
        print(f"\n{'='*70}")
        print(f"{suite_upper} DECLARATIVE-EVALUATIVE GAP")
        print(f"{'='*70}")
        gap = tables[f'{suite}_gap']
        for _, row in gap.iterrows():
            bar_d = '█' * int(row['declarative_pct'] / 3)
            bar_e = '█' * int(row['evaluative_pct'] / 3)
            print(f"  {row['scale']:>5s}  DECL: {row['declarative_pct']:5.1f}% {bar_d}")
            print(f"         EVAL: {row['evaluative_pct']:5.1f}% {bar_e}")
            print(f"         GAP:  {row['gap']:+.2f} ({row['gap_pct_pts']:+.1f} pct pts)")
            print()

    # Emergence
    print(f"{'='*70}")
    print("DECLARATIVE EMERGENCE THRESHOLDS")
    print(f"{'='*70}")
    em = tables['emergence_thresholds']
    print(f"  {'Concept':30s} {'Pythia':>10s} {'GPT-2':>10s}")
    print(f"  {'─'*30} {'─'*10} {'─'*10}")
    for _, row in em.iterrows():
        print(f"  {row['concept']:30s} {row['pythia_emergence']:>10s} {row['gpt2_emergence']:>10s}")

    print_extended_summary(tables)


def print_extended_summary(tables):
    """Print highlights from the six extended analyses."""
    if 'binding_accuracy_corr' in tables and not tables['binding_accuracy_corr'].empty:
        print(f"\n{'='*70}")
        print("BINDING DEPTH vs ACCURACY (ext 2)")
        print(f"{'='*70}")
        for _, r in tables['binding_accuracy_corr'].iterrows():
            print(f"  {r['suite']:>7s}: pearson r={r['pearson_r']}  "
                  f"spearman r={r['spearman_r']}  (n={r['n_pairs']} compound-scale pairs)")

    if 'fluent_wrongness' in tables and not tables['fluent_wrongness'].empty:
        print(f"\n{'='*70}")
        print("FLUENT WRONGNESS (ext 1) — entropy when wrong on a11y vs right on control")
        print(f"{'='*70}")
        print("  (negative confidence_gap = MORE confident when wrong on accessibility)")
        for _, r in tables['fluent_wrongness'].iterrows():
            print(f"  {r['suite']:>7s} {r['scale']:>5s}  a11y-wrong H={r['access_incorrect_entropy']}  "
                  f"ctrl-right H={r['control_correct_entropy']}  gap={r['confidence_gap']}")

    if 'per_concept_trajectories' in tables and not tables['per_concept_trajectories'].empty:
        print(f"\n{'='*70}")
        print("PER-CONCEPT TRAJECTORIES (ext 3)")
        print(f"{'='*70}")
        traj = tables['per_concept_trajectories']
        for suite in ['pythia', 'gpt2']:
            sub = traj[traj['suite'] == suite]
            if sub.empty:
                continue
            print(f"  [{suite}]")
            for _, r in sub.iterrows():
                print(f"    {r['concept']:25s} {r['trajectory']}")

    if 'completion_paradox' in tables and not tables['completion_paradox'].empty:
        print(f"\n{'='*70}")
        print("COMPLETION PARADOX (ext 6) — completion% vs declarative% (largest gaps)")
        print(f"{'='*70}")
        cp = tables['completion_paradox'].dropna(subset=['paradox_gap_pct_pts'])
        cp = cp.reindex(cp['paradox_gap_pct_pts'].abs().sort_values(ascending=False).index)
        for _, r in cp.head(12).iterrows():
            print(f"  {r['suite']:>7s} {r['scale']:>5s} {r['concept']:20s}  "
                  f"compl={r['completion_pct']}%  decl={r['declarative_pct']}%  "
                  f"gap={r['paradox_gap_pct_pts']:+.1f} pts")


if __name__ == '__main__':
    import sys
    project_root = Path(__file__).parent.parent
    tables = run_gap_analysis(project_root)

    output_dir = project_root / 'results' / 'analysis'
    print(f"\nSaving to {output_dir}/")
    save_tables(tables, output_dir)

    print("\n")
    print_summary(tables)
