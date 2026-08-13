"""Provenance manifest for the norm-aware effective-binding notebooks.

This module is intentionally separate from ``src/manifest.py``.  The original
manifest writer remains untouched; these experiments have different measures,
prompt conditions, output paths, and interpretation caveats.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import platform
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import torch


MEASURE_DEFINITIONS = {
    "binding_score": "Raw attention from the later compound token to the earlier token (compatibility alias).",
    "attention_weight": "Raw attention from the later compound token to the earlier token.",
    "ov_write_norm": "L2 norm of the earlier token's head-specific value vector after W_O.",
    "weighted_ov_norm": "attention_weight multiplied by ov_write_norm.",
    "relative_weighted_ov_norm": "weighted_ov_norm divided by the later token's resid_pre L2 norm.",
    "target_residual_norm": "L2 norm of resid_pre at the later compound token.",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _package_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not installed"


def _git_state(project_root: Path) -> tuple[str, bool]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        dirty = bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=project_root,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        return commit, dirty
    except (OSError, subprocess.SubprocessError):
        return "unknown", False


def _relative(path: Path, project_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _device_description(model) -> str:
    parameter = next(model.parameters())
    if parameter.device.type == "cuda":
        try:
            return f"{parameter.device} ({torch.cuda.get_device_name(parameter.device)})"
        except Exception:
            return str(parameter.device)
    if parameter.device.type == "mps":
        return "mps (Apple Metal)"
    return str(parameter.device)


def write_effective_binding_manifest(
    project_root,
    output_dir,
    model_name: str,
    model,
    prompt_condition: str,
    family: str,
    domain_counts: Mapping[str, Mapping[str, object]],
    results_df,
    prompt_files: Iterable,
    unresolved: Sequence[Sequence[object]] = (),
    revision: str | None = None,
    hf_commit_sha: str | None = None,
) -> Path:
    """Write one Markdown manifest after an effective-binding model run.

    Parameters mirror the objects already present in the new notebooks.  The
    function does not mutate results, infer missing rows, or rewrite any CSV.
    It records exactly what the completed notebook run produced.
    """
    project_root = Path(project_root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if prompt_condition not in {"natural", "uniform"}:
        raise ValueError(
            "prompt_condition must be either 'natural' or 'uniform'; "
            f"received {prompt_condition!r}"
        )

    prompt_paths = [Path(path) for path in prompt_files]
    commit, dirty = _git_state(project_root)
    parameter = next(model.parameters())

    expected_total = sum(int(item["expected"]) for item in domain_counts.values())
    written_total = sum(int(item["written"]) for item in domain_counts.values())

    manifest_path = output_dir / (
        f"{model_name}-{prompt_condition}-effective-binding.md"
    )

    lines = [
        "# Effective-binding run manifest",
        "",
        f"- Run time (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Git commit: `{commit}`",
        f"- Working tree dirty at manifest time: `{dirty}`",
        "",
        "## Experiment",
        "",
        f"- Model family: `{family}`",
        f"- Model name: `{model_name}`",
        f"- Prompt condition: `{prompt_condition}`",
        "- Constituent direction: later compound token attends to earlier compound token",
        "- Multi-token constituent rule: last subtoken represents the constituent",
        "- Default scope: accessibility compounds with frozen frequency measurements",
        "",
        "## Model",
        "",
        f"- Layers: {model.cfg.n_layers}",
        f"- Attention heads: {model.cfg.n_heads}",
        f"- Hidden size: {model.cfg.d_model}",
        f"- Vocabulary size: {model.cfg.d_vocab}",
        f"- Parameter count: {sum(p.numel() for p in model.parameters()):,}",
        f"- Parameter dtype: `{parameter.dtype}`",
        f"- Device: `{_device_description(model)}`",
    ]

    if revision:
        lines.append(f"- Requested model revision: `{revision}`")
    if hf_commit_sha:
        lines.append(f"- Resolved Hugging Face commit: `{hf_commit_sha}`")

    lines.extend([
        "",
        "## Measurements",
        "",
        "| column | definition |",
        "|---|---|",
    ])
    for column, definition in MEASURE_DEFINITIONS.items():
        lines.append(f"| `{column}` | {definition} |")

    lines.extend([
        "",
        "The norm-aware measures are source-specific, head-specific writes. They are not a complete ALTI decomposition through all residual and normalization paths.",
    ])
    if family.lower() == "olmo":
        lines.append(
            "For OLMo, the source-specific write is measured immediately before the attention-branch RMS normalization."
        )

    lines.extend([
        "",
        "## Completeness",
        "",
        f"- Expected rows: {expected_total:,}",
        f"- Written rows: {written_total:,}",
        f"- Difference: {expected_total - written_total:,}",
        f"- Rows in concatenated result frame: {len(results_df):,}",
        f"- Unresolved compounds: {len(unresolved)}",
        "",
        "| domain | expected | written | output file | SHA-256 |",
        "|---|---:|---:|---|---|",
    ])

    for domain, item in domain_counts.items():
        output_path = output_dir / str(item["file"])
        checksum = _sha256(output_path) if output_path.exists() else "missing"
        flag = "" if int(item["expected"]) == int(item["written"]) else " ⚠️"
        lines.append(
            f"| {domain} | {int(item['expected']):,} | "
            f"{int(item['written']):,}{flag} | `{item['file']}` | `{checksum}` |"
        )

    lines.extend([
        "",
        "## Inputs",
        "",
        "| prompt file | SHA-256 |",
        "|---|---|",
    ])
    for path in prompt_paths:
        checksum = _sha256(path) if path.exists() else "missing"
        lines.append(f"| `{_relative(path, project_root)}` | `{checksum}` |")

    if unresolved:
        lines.extend([
            "",
            "## Unresolved token matches",
            "",
            "| domain | compound | word 1 | word 2 |",
            "|---|---|---|---|",
        ])
        for item in unresolved:
            domain, compound, word1, word2 = item[:4]
            lines.append(f"| {domain} | {compound} | `{word1}` | `{word2}` |")

    lines.extend([
        "",
        "## Output schema",
        "",
        ", ".join(f"`{column}`" for column in results_df.columns),
        "",
        "## Environment",
        "",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.platform()}`",
        f"- torch: `{_package_version('torch')}`",
        f"- transformer-lens: `{_package_version('transformer-lens')}`",
        f"- transformers: `{_package_version('transformers')}`",
        f"- pandas: `{_package_version('pandas')}`",
        f"- numpy: `{_package_version('numpy')}`",
        f"- PyYAML: `{_package_version('PyYAML')}`",
        "",
    ])

    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Manifest: {manifest_path}")
    return manifest_path
