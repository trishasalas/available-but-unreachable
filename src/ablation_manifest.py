"""Manifest support for frequency-sensitive held-out head ablations.

This module is separate from both ``src/manifest.py`` and
``src/effective_binding_manifest.py``.  It supports:

1. contemporaneous manifests written at the end of a future model run; and
2. explicitly labelled post-run reconstructions for CSVs produced before this
   manifest writer existed.
"""

from __future__ import annotations

import ast
import csv
import datetime as dt
import hashlib
import math
import platform
import statistics
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Iterable, Sequence


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not installed"


def _git_state(project_root: Path) -> tuple[str, bool]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=project_root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=project_root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip())
        return commit, dirty
    except (OSError, subprocess.SubprocessError):
        return "unknown", False


def _relative(path: Path | None, project_root: Path) -> str:
    if path is None:
        return "not recorded"
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _file_row(label: str, path: Path | None, project_root: Path) -> str:
    if path is None:
        return f"| {label} | not recorded | not recorded |"
    if not path.exists():
        return f"| {label} | `{_relative(path, project_root)}` | missing |"
    return (
        f"| {label} | `{_relative(path, project_root)}` | `{_sha256(path)}` |"
    )


def _load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _unique_literal(rows: list[dict[str, str]], column: str):
    values = {row[column] for row in rows}
    if len(values) != 1:
        raise ValueError(
            f"Expected one {column!r} value in {len(rows)} rows; found {len(values)}"
        )
    value = values.pop()
    if column.endswith("heads"):
        return [tuple(map(int, pair)) for pair in ast.literal_eval(value)]
    return value


def _summary(rows: list[dict[str, str]]) -> dict[str, object]:
    selected = [float(row["selected_kl"]) for row in rows]
    control = [float(row["control_kl"]) for row in rows]
    difference = [float(row["selected_minus_control_kl"]) for row in rows]
    return {
        "n_rows": len(rows),
        "selected_mean": statistics.mean(selected),
        "selected_median": statistics.median(selected),
        "selected_min": min(selected),
        "selected_max": max(selected),
        "control_mean": statistics.mean(control),
        "control_median": statistics.median(control),
        "control_min": min(control),
        "control_max": max(control),
        "difference_mean": statistics.mean(difference),
        "difference_median": statistics.median(difference),
        "selected_gt_control": sum(a > b for a, b in zip(selected, control)),
        "selected_eq_control": sum(a == b for a, b in zip(selected, control)),
        "selected_lt_control": sum(a < b for a, b in zip(selected, control)),
        "selected_top_changed": sum(
            row["selected_top_changed"].strip().lower() == "true" for row in rows
        ),
        "control_top_changed": sum(
            row["control_top_changed"].strip().lower() == "true" for row in rows
        ),
    }


def _model_lines(model, revision: str | None) -> list[str]:
    if model is None:
        lines = [
            "- Live model object: not available during reconstruction",
            "- Runtime device and dtype: not contemporaneously recorded by the ablation notebook",
        ]
    else:
        parameter = next(model.parameters())
        lines = [
            f"- Layers: {model.cfg.n_layers}",
            f"- Attention heads: {model.cfg.n_heads}",
            f"- Hidden size: {model.cfg.d_model}",
            f"- Parameter count: {sum(p.numel() for p in model.parameters()):,}",
            f"- Parameter dtype: `{parameter.dtype}`",
            f"- Device: `{parameter.device}`",
        ]
    if revision:
        lines.append(f"- Requested revision: `{revision}`")
    return lines


def write_ablation_manifest(
    *,
    project_root,
    csv_path,
    candidate_path=None,
    notebook_path=None,
    intervention_code_path=None,
    model_metadata_manifest=None,
    model=None,
    revision: str | None = None,
    random_seed: int = 42,
    split_description: str = "Sorted compound names, shuffled once; first half selection, second half held out",
    reconstructed: bool = False,
    manifest_path=None,
) -> Path:
    """Write a manifest for one held-out ablation CSV.

    Set ``reconstructed=True`` when the writer is invoked after the original
    runtime has ended.  The manifest will distinguish recovered provenance from
    contemporaneously observed runtime state.
    """
    project_root = Path(project_root)
    csv_path = Path(csv_path)
    candidate_path = Path(candidate_path) if candidate_path else None
    notebook_path = Path(notebook_path) if notebook_path else None
    intervention_code_path = (
        Path(intervention_code_path) if intervention_code_path else None
    )
    model_metadata_manifest = (
        Path(model_metadata_manifest) if model_metadata_manifest else None
    )
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    rows = _load_rows(csv_path)
    if not rows:
        raise ValueError(f"Ablation CSV is empty: {csv_path}")

    model_name = str(_unique_literal(rows, "model"))
    condition = str(_unique_literal(rows, "condition"))
    selected_heads = _unique_literal(rows, "selected_heads")
    control_heads = _unique_literal(rows, "control_heads")
    summary = _summary(rows)
    commit, dirty = _git_state(project_root)

    if manifest_path is None:
        manifest_path = csv_path.with_suffix(".md")
    manifest_path = Path(manifest_path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    status = "POST-RUN RECONSTRUCTION" if reconstructed else "CONTEMPORANEOUS RUN RECORD"
    lines = [
        "# Held-out frequency-head ablation manifest",
        "",
        f"**Record status: {status}**",
        "",
    ]
    if reconstructed:
        lines.extend([
            "This manifest was created after the ablation completed because the original notebook wrote only the CSV.",
            "File hashes, saved interventions, split rules, and result summaries are recovered exactly from surviving artifacts.",
            "Runtime-only facts not preserved by those artifacts are explicitly marked as unavailable rather than inferred.",
            "",
        ])

    lines.extend([
        f"- Manifest creation time (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Repository commit at manifest creation: `{commit}`",
        f"- Working tree dirty at manifest creation: `{dirty}`",
        "",
        "## Design",
        "",
        f"- Model: `{model_name}`",
        f"- Prompt condition: `{condition}`",
        f"- Random seed: `{random_seed}`",
        f"- Split: {split_description}",
        f"- Held-out compounds: {summary['n_rows']}",
        f"- Selected heads: `{selected_heads}`",
        f"- Layer-matched random control heads: `{control_heads}`",
        "- Intervention: zero each listed head's `hook_z` output at the later constituent position",
        "- Outcome: KL(base || ablated) at the final prompt position; top-token change also recorded",
        "",
        "## Model/runtime",
        "",
        *_model_lines(model, revision),
        "",
        "## Recovered artifacts",
        "",
        "| artifact | path | SHA-256 |",
        "|---|---|---|",
        _file_row("Ablation CSV", csv_path, project_root),
        _file_row("Candidate-head table", candidate_path, project_root),
        _file_row("Ablation notebook", notebook_path, project_root),
        _file_row("Intervention implementation", intervention_code_path, project_root),
        _file_row("Corresponding model manifest", model_metadata_manifest, project_root),
        "",
        "## Saved-result audit",
        "",
        f"- Rows: {summary['n_rows']}",
        f"- Selected KL mean / median: {summary['selected_mean']:.10g} / {summary['selected_median']:.10g}",
        f"- Selected KL range: [{summary['selected_min']:.10g}, {summary['selected_max']:.10g}]",
        f"- Control KL mean / median: {summary['control_mean']:.10g} / {summary['control_median']:.10g}",
        f"- Control KL range: [{summary['control_min']:.10g}, {summary['control_max']:.10g}]",
        f"- Selected-minus-control mean / median: {summary['difference_mean']:.10g} / {summary['difference_median']:.10g}",
        f"- Selected > control / equal / selected < control: {summary['selected_gt_control']} / {summary['selected_eq_control']} / {summary['selected_lt_control']}",
        f"- Selected top-token changes: {summary['selected_top_changed']} / {summary['n_rows']}",
        f"- Control top-token changes: {summary['control_top_changed']} / {summary['n_rows']}",
        "",
        "## Output schema",
        "",
        ", ".join(f"`{column}`" for column in rows[0].keys()),
        "",
        "## Manifest-generation environment",
        "",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.platform()}`",
        f"- torch: `{_package_version('torch')}`",
        f"- transformer-lens: `{_package_version('transformer-lens')}`",
        f"- pandas: `{_package_version('pandas')}`",
        f"- numpy: `{_package_version('numpy')}`",
        "",
    ])

    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Ablation manifest: {manifest_path}")
    return manifest_path


def write_reconstructed_ablation_manifest(**kwargs) -> Path:
    """Convenience wrapper that cannot accidentally omit the reconstruction label."""
    kwargs["reconstructed"] = True
    kwargs["model"] = None
    return write_ablation_manifest(**kwargs)
