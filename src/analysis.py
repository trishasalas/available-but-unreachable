"""
Analysis module — loads and combines results across all models.

Usage (from notebook):
    from src.analysis import load_all_results
    elicitation, entropy, binding = load_all_results(PROJECT_ROOT)

Directory layout (post-reorganisation):
    results/{elicitation,entropy,binding}/{suite}/{model}/{model}-{domain}.csv
    Suites: pythia, gpt2, olmo
    Domains: accessibility, control, medical, legal, finance

What this module now guarantees, and what it still does not
-----------------------------------------------------------
DONE 2026-08-09 (audit findings A6, A9, A10; decision 0010 option A):
  - `source` is DERIVED from concept membership, not hardcoded 'original'.
  - Every load reports its own scope: source counts, skipped CSVs, and any
    (suite, scale) claimed by more than one model directory.

DONE 2026-08-11 (audit finding A3; decision 0015):
  - `concept` is NORMALIZED to canonical form (lowercase, underscores) on
    every frame that carries it. The on-disk spelling is preserved verbatim
    as `concept_raw`, and every load prints the vocabulary collapse.
  - `compound` (binding) is deliberately NOT normalized. Verified 2026-08-11:
    all 227 binding compounds are already canonical, so normalizing there
    would be a no-op dressed up as a safeguard. If that ever stops being
    true it shows up as a failed join, not as silently merged rows.

DEFERRED — not an omission:
  - The gpt2 / gpt2-small collision is REPORTED, not resolved. Deduping it is
    a decision about which run is authoritative, not a loader concern.

DEPENDS ON — read before changing either column:
  - Every consumer that DISPATCHES on the concept (rather than joining on it)
    must read `concept_raw`, not `concept`. src/accuracy_coding.py routes on a
    52-key rules dict in space form, case-sensitively ('WCAG', 'semantic
    HTML'), and `rules.get(concept, {})` returns 'incorrect' on a miss rather
    than raising. Zero of those 52 keys survive canonicalization, so a
    consumer that passes the normalized `concept` to code_response codes every
    declarative row incorrect — declarative mean 0.0 — with no error anywhere.
    Current dispatching consumers: src/gap_analysis.py (2 call sites),
    src/dual_spearman.py (2 call sites). Both pass `concept_raw`.
"""

from pathlib import Path
import pandas as pd


KNOWN_DOMAINS = {'accessibility', 'control', 'medical', 'legal', 'finance'}

# --- INTERIM (decision 0010, option A) --------------------------------------
# The ten original Paper 1 Experiment 1 declarative concepts, in canonical form.
# Verified 2026-08-09 against the section boundary in data/accessibility.yaml
# ("Original Paper 1 Experiment 1 prompts" .. "DECLARATIVE (expansion)") rather
# than transcribed by hand.
#
# This list lives in code and must be kept in sync with the YAML BY HAND — which
# is the exact failure mode 0010 exists to fix. The durable fix is an explicit
# `source:` field in data/accessibility.yaml, deferred to the Phase 4 frequency
# regeneration; this frozenset is superseded at that point.
#
# Trap: the tenth is `closed captions`, NOT `captions` (renamed in ca01b59).
# Getting it wrong silently yields nine concepts and no error.
ORIGINAL_CONCEPTS = frozenset({
    'screen_reader',
    'wcag',
    'skip_link',
    'alt_text',
    'aria',
    'focus_indicator',
    'keyboard_navigation',
    'color_contrast',
    'semantic_html',
    'closed_captions',
})

# Genuine cross-battery aliases — not whitespace/case variants. The completion
# battery says `captions` where the declarative battery says `closed captions`.
CONCEPT_ALIASES = {
    'captions': 'closed_captions',
}


def load_all_results(project_root):
    """
    Load and concatenate all result CSVs across all model families.

    Returns three DataFrames:
        elicitation_df — all prompt responses across all models
        entropy_df     — all entropy measurements across all models
        binding_df     — all binding scores across all models

    Each DataFrame has 'model', 'suite', 'scale', 'domain', and 'source'
    columns.
    """
    project_root = Path(project_root)
    results_dir = project_root / 'results'

    frames = {'elicitation': [], 'entropy': [], 'binding': []}
    skipped = []                                   # (path, failed domain string)
    dir_rows = {}                                  # (data_type, suite, scale) -> {model_dir: rows}

    for data_type in frames:
        type_dir = results_dir / data_type
        if not type_dir.exists():
            continue

        for suite_dir in sorted(type_dir.iterdir()):
            if not suite_dir.is_dir():
                continue
            dir_suite = suite_dir.name

            for model_dir in sorted(suite_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                model_name = model_dir.name
                suite = _infer_suite(model_name, dir_suite)
                scale = _extract_scale(model_name, suite)

                # Registered before the per-file loop so a directory that
                # contributes ZERO rows still shows up in the collision report.
                dir_rows.setdefault((data_type, suite, scale), {}).setdefault(model_name, 0)

                for csv_file in sorted(model_dir.glob('*.csv')):
                    domain = _extract_domain(csv_file.stem, model_name)
                    if domain not in KNOWN_DOMAINS:
                        skipped.append((csv_file.relative_to(project_root), domain))
                        continue

                    df = pd.read_csv(csv_file)
                    if 'domain' not in df.columns:
                        df['domain'] = domain
                    df['suite'] = suite
                    df['scale'] = scale
                    # Guarded like 'domain' above: never clobber a real column.
                    # The unguarded write here was the original defect (0010).
                    if 'source' not in df.columns:
                        df['source'] = _derive_source(df)
                    frames[data_type].append(df)
                    dir_rows[(data_type, suite, scale)][model_name] += len(df)

    elicitation_df = pd.concat(frames['elicitation'], ignore_index=True) if frames['elicitation'] else pd.DataFrame()
    entropy_df = pd.concat(frames['entropy'], ignore_index=True) if frames['entropy'] else pd.DataFrame()
    binding_df = pd.concat(frames['binding'], ignore_index=True) if frames['binding'] else pd.DataFrame()

    for df in [elicitation_df, entropy_df, binding_df]:
        if 'scale' in df.columns:
            df.sort_values('scale', inplace=True)

    # Concept-key normalization (decision 0015). Exactly one place, on purpose.
    vocab = {}
    for name, df in [('elicitation', elicitation_df), ('entropy', entropy_df),
                     ('binding', binding_df)]:
        vocab[name] = _normalize_concept_column(df)

    print("Loaded:")
    for name, df in [('Elicitation', elicitation_df), ('Entropy', entropy_df), ('Binding', binding_df)]:
        if not df.empty and 'model' in df.columns:
            counts = df['source'].value_counts().to_dict() if 'source' in df.columns else {}
            print(f"  {name}: {len(df)} rows across {df['model'].nunique()} models "
                  f"({sorted(df['suite'].unique())})  source={counts}")
        else:
            print(f"  {name}: {len(df)} rows")

    # Scope reporting. These three blocks exist because silence is what let the
    # source filter, the gpt2 collision, and a dropped CSV hide for a month.
    if skipped:
        print(f"\nSkipped {len(skipped)} CSV(s) — stem did not resolve to a KNOWN_DOMAIN:")
        for path, domain in skipped:
            print(f"  {path}  ->  domain={domain!r}")

    collisions = {k: v for k, v in dir_rows.items() if len(v) > 1}
    if collisions:
        print(f"\nScale collisions — one (suite, scale) claimed by >1 model directory.")
        print("  NOT deduped: reported so the resolution is a decision, not a side effect.")
        for (data_type, suite, scale), dirs in sorted(collisions.items()):
            listed = ', '.join(f"{d} ({n} rows)" for d, n in sorted(dirs.items()))
            print(f"  {data_type}/{suite} @ {scale_label(scale)}: {listed}")

    # Vocabulary scope. Printed every load rather than documented once, because
    # a collapse that appears later (a new battery, a re-spelled concept) is
    # exactly the kind of change that otherwise lands silently.
    for name, v in vocab.items():
        if not v:
            continue
        print(f"\n{name}: concept vocabulary {v['n_before']} -> {v['n_after']} "
              f"distinct after normalization "
              f"({len(v['collapsed'])} many-to-one collapse(s))")
        for canonical, raws in sorted(v['collapsed'].items()):
            print(f"  {raws} -> {canonical!r}")

    return elicitation_df, entropy_df, binding_df


def _normalize_concept_column(df):
    """Canonicalize `concept` in place, preserving the on-disk spelling.

    Decision 0015. Sets `concept_raw` to the value as written on disk, then
    rewrites `concept` to canonical form via `_canonical_concept`.

    Returns a vocabulary report: distinct counts before/after, and the
    many-to-one collapses keyed by canonical form. Returns {} for frames with
    no `concept` column (binding, which carries `compound` and is already
    canonical — see the module docstring).

    Depends on: no consumer dispatching on `concept`. Anything that routes on
    the concept — code_response, observe_sense, any dict keyed in space form —
    must read `concept_raw`.
    """
    if df.empty or 'concept' not in df.columns:
        return {}

    df['concept_raw'] = df['concept']
    df['concept'] = df['concept'].map(_canonical_concept)

    groups = {}
    for raw, canonical in zip(df['concept_raw'], df['concept']):
        groups.setdefault(canonical, set()).add(raw)
    return {
        'n_before': int(df['concept_raw'].nunique()),
        'n_after': int(df['concept'].nunique()),
        'collapsed': {k: sorted(v) for k, v in groups.items() if len(v) > 1},
    }


def _canonical_concept(value):
    """Canonical concept key: lowercase, underscores ('closed_captions').

    Matches the frequency battery and file-naming conventions. Idempotent.
    Handles genuine cross-battery aliases (CONCEPT_ALIASES), not just
    whitespace and case.

    Applied (decision 0015, landed 2026-08-11) by `_normalize_concept_column`
    to the `concept` column of every loaded frame, and by `_derive_source`
    below for the ORIGINAL_CONCEPTS membership test. NOT applied to binding's
    `compound` column, which is already canonical.
    """
    c = str(value).strip().lower().replace(' ', '_')
    return CONCEPT_ALIASES.get(c, c)


def _derive_source(df):
    """Tag each row 'original' or 'expansion' (decision 0010).

    'expansion' means one of the 41 frequency-stratified expansion compounds,
    which carry only the declarative arm and must stay out of the paradigm
    means in gap_analysis. The discriminator is the YAML section those prompts
    live in, which is exactly: accessibility domain, declarative prompt type,
    concept outside the ten originals.

    Scoped to declarative on purpose. The evaluative arm's five concepts are
    Paper 1 originals, but only two of them ('alt text', 'semantic HTML') are
    in ORIGINAL_CONCEPTS — a bare concept-membership test would silently cut
    the evaluative pivot from five concepts to two, and the declarative pass
    condition would not catch it. Verified against
    _Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv, whose evaluative
    column must stay unchanged.

    Frames with no prompt_type (binding) are tagged on concept membership
    alone, which is the intended meaning there — every non-original compound
    in the binding battery IS an expansion compound.

    Limit worth naming: rows outside the accessibility domain (control,
    medical, legal, finance) are tagged 'original' because the original/
    expansion axis is not defined for them. Every consumer filters on domain
    first. Do not read 'original' on a medical row as a claim about Paper 1.
    """
    concept_col = 'concept' if 'concept' in df.columns else (
        'compound' if 'compound' in df.columns else None)
    if concept_col is None:
        return 'original'

    is_expansion = (
        (df['domain'] == 'accessibility') &
        ~df[concept_col].map(_canonical_concept).isin(ORIGINAL_CONCEPTS)
    )
    if 'prompt_type' in df.columns:
        is_expansion &= (df['prompt_type'] == 'declarative')

    return is_expansion.map({True: 'expansion', False: 'original'})


def _infer_suite(model_name, dir_suite):
    """Correct suite when model dirs are misplaced (e.g. OLMo under gpt2/)."""
    if model_name.startswith('OLMo'):
        return 'olmo'
    return dir_suite


def _extract_domain(csv_stem, model_name):
    """Extract domain from filename: 'pythia-160m-accessibility' -> 'accessibility'."""
    prefix = model_name + '-'
    if csv_stem.startswith(prefix):
        return csv_stem[len(prefix):]
    return csv_stem


def _extract_scale(model_name, suite):
    """
    Extract parameter count as integer for sorting.
    'pythia-160m'        -> 160_000_000
    'gpt2-xl'           -> 1_500_000_000
    'OLMo-2-1124-7B'    -> 7_000_000_000
    """
    gpt2_scales = {
        'gpt2': 124_000_000,
        'gpt2-small': 124_000_000,
        'gpt2-medium': 355_000_000,
        'gpt2-large': 774_000_000,
        'gpt2-xl': 1_500_000_000,
    }
    if suite == 'gpt2':
        return gpt2_scales.get(model_name, 0)

    # No pythia-13b alias here on purpose (decision 0014). The binding outputs
    # were renamed to pythia-12b, the upstream name. A stray 'pythia-13b'
    # directory now falls through to the generic parse, which reads 13b as
    # 13_000_000_000 and separates it from pythia-12b in every groupby —
    # visibly wrong instead of silently absorbed. Depends on: results/binding/
    # pythia/ containing pythia-12b and no pythia-13b.
    multipliers = {'m': 1_000_000, 'b': 1_000_000_000}
    parts = model_name.split('-')
    for part in parts:
        p = part.lower()
        for suffix, mult in multipliers.items():
            if p.endswith(suffix):
                try:
                    return int(float(p[:-1]) * mult)
                except ValueError:
                    continue
    return 0


def scale_label(scale_int):
    """Convert scale integer to readable label: 160000000 -> '160M'"""
    if scale_int >= 1_000_000_000:
        return f"{scale_int / 1_000_000_000:.1f}B".replace('.0B', 'B')
    elif scale_int >= 1_000_000:
        return f"{scale_int / 1_000_000:.0f}M"
    return str(scale_int)


def binding_summary(binding_df, threshold=0.1):
    """
    Summarize binding data: count of heads above threshold per compound per model.
    Returns a pivot table suitable for heatmaps.
    """
    above = binding_df[binding_df['binding_score'] > threshold]
    summary = above.groupby(['model', 'compound', 'scale']).size().reset_index(name='n_heads_above')
    return summary


def max_binding_layer(binding_df):
    """
    For each compound x model, find the layer with the strongest binding head.
    Useful for tracking binding depth across scales.
    """
    idx = binding_df.groupby(['model', 'compound'])['binding_score'].idxmax()
    return binding_df.loc[idx][['model', 'compound', 'layer', 'head', 'binding_score', 'scale']].reset_index(drop=True)


def tokenization_comparison(binding_df):
    """
    Compare binding scores between cleanly-tokenized and subword-split compounds.
    Returns summary statistics for each group.
    """
    clean = ['screen_reader', 'alt_text', 'skip_link', 'color_contrast',
             'page_title', 'form_label', 'link_text', 'focus_indicator']
    split = ['keyboard_navigation', 'closed_captions', 'semantic_html']

    binding_df = binding_df.copy()
    binding_df['tokenization'] = binding_df['compound'].apply(
        lambda x: 'clean' if x in clean else 'subword_split' if x in split else 'unknown'
    )

    summary = binding_df.groupby(['tokenization', 'model', 'scale']).agg(
        mean_binding=('binding_score', 'mean'),
        max_binding=('binding_score', 'max'),
        heads_above_01=('binding_score', lambda x: (x > 0.1).sum()),
    ).reset_index()

    return summary
