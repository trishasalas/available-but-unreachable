"""Validate effective-binding rows against the intended prompt condition before saving."""
import numpy as np


def validate_binding_output(frame, compounds, model_name, condition, n_layers, n_heads):
    if condition not in {'natural', 'uniform'}:
        raise ValueError(f'Unknown prompt condition: {condition}')
    cases = {c['name']: c for c in compounds}
    if len(cases) != len(compounds) or set(frame.compound) != set(cases):
        raise ValueError('Compound inventory is incomplete or duplicated')
    if len(frame) != len(cases) * n_layers * n_heads:
        raise ValueError('Incomplete layer/head coverage')
    if frame.duplicated(['compound', 'layer', 'head']).any():
        raise ValueError('Duplicate compound/layer/head rows')
    if not frame.model.eq(model_name).all() or not frame.prompt_condition.eq(condition).all():
        raise ValueError('Model or condition labels disagree with the requested run')
    for name, group in frame.groupby('compound'):
        c = cases[name]
        expected = c['prompt'] if condition == 'natural' else f"A {c['word1']} {c['word2']} is"
        if not group.prompt.eq(expected).all():
            raise ValueError(f'{name}: saved prompt does not match {condition}')
        if not group.word1.eq(c['word1']).all() or not group.word2.eq(c['word2']).all():
            raise ValueError(f'{name}: constituent names do not match inventory')
        if set(zip(group['layer'], group['head'])) != {(l, h) for l in range(n_layers) for h in range(n_heads)}:
            raise ValueError(f'{name}: invalid layer/head coverage')
    columns = ['attention_weight', 'ov_write_norm', 'weighted_ov_norm',
               'relative_weighted_ov_norm', 'target_residual_norm']
    values = frame[columns].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError('Binding measurements must be finite and nonnegative')
