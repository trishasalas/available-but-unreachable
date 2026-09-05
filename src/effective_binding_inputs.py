"""Resolve effective-binding condition inputs while preserving original run records.

GPT-2-large's original files have reversed condition labels. The documented
correction is hash-bound and validated against actual prompt strings at load time.
"""
from pathlib import Path
import hashlib
import pandas as pd
import yaml
from src.effective_binding_validation import validate_binding_output

GPT2_LARGE_SOURCES = {'uniform': ('results/effective_binding/gpt2/gpt2-large/natural/gpt2-large-natural-accessibility.csv', '97a15e6130a5fb1c3660152dcb6e297b4e104f14bfcce8f891814c6c67686752'), 'natural': ('results/effective_binding/gpt2/gpt2-large/uniform/gpt2-large-uniform-accessibility.csv', 'c952fbe49fedb19afcf777c2f29071396ffbef861f9df6c90adcb357028c6f6c')}


def condition_files(project_root, condition):
    if condition not in {"natural", "uniform"}:
        raise ValueError(f"Unknown condition: {condition}")
    root = Path(project_root)
    files = sorted((root / "results/effective_binding").glob(f"*/*/{condition}/*-{condition}-accessibility.csv"))
    files = [p for p in files if p.parts[-3] != "gpt2-large"]
    relative, digest = GPT2_LARGE_SOURCES[condition]
    corrected = root / relative
    if hashlib.sha256(corrected.read_bytes()).hexdigest() != digest:
        raise ValueError("GPT-2-large source changed; review its condition mapping before analysis")
    files.append(corrected)
    return sorted(files)


def load_condition_frame(path, project_root, condition):
    frame = pd.read_csv(path)
    # Relabel the analysis view only; never rewrite the original run CSV.
    frame["prompt_condition"] = condition
    cases = yaml.safe_load((Path(project_root) / "data/binding/accessibility.yaml").read_text())["compounds"]
    model = Path(path).parts[-3]
    validate_binding_output(frame, cases, model, condition,
                            int(frame.layer.max()) + 1, int(frame["head"].max()) + 1)
    return frame
