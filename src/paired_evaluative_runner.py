"""Model runner for the frozen paired evaluative battery.

The runner writes to ``results/evaluative_paired`` only. It deliberately
preserves the raw continuation, including leading newlines and whitespace,
because answer-position behavior is part of the instrument audit.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import platform
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pandas as pd

from src.paired_evaluative import MODEL_META, _model_key, load_battery, validate_battery


GENERATION = {
    "do_sample": False,
    "max_new_tokens": 100,
    "verbose": False,
}


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


def run_paired_model(
    model,
    model_name: str,
    project_root: str | Path,
    battery_path: str | Path | None = None,
    revision: str | None = None,
    hf_commit_sha: str | None = None,
) -> pd.DataFrame:
    """Run all 16 frozen prompts for one model and save CSV plus manifest."""
    project_root = Path(project_root)
    if battery_path is None:
        battery_path = project_root / "data" / "evaluative_paired.yaml"
    battery_path = Path(battery_path)
    battery = load_battery(battery_path)
    validate_battery(battery, project_root / "data" / "accessibility.yaml")

    model_key = _model_key(model_name)
    if model_key not in MODEL_META:
        raise ValueError(f"model {model_name!r} is not in the frozen 13-model set")
    suite, scale = MODEL_META[model_key]

    rows = []
    for item in battery["prompts"]:
        prompt = item["prompt"]
        full_output = model.generate(prompt, **GENERATION)
        if not isinstance(full_output, str) or not full_output.startswith(prompt):
            raise ValueError(
                f"{model_key}/{item['prompt_id']}: generation did not return "
                "the original prompt followed by a string continuation"
            )
        continuation = full_output[len(prompt) :]
        rows.append({
            "suite": suite,
            "scale": scale,
            "model": model_name,
            "prompt_id": item["prompt_id"],
            "pair_id": item["pair_id"],
            "concept": item["concept"],
            "polarity": item["polarity"],
            "paired_with": item["paired_with"],
            "prompt_type": item["prompt_type"],
            "template_type": item["template_type"],
            "prompt": prompt,
            "output": continuation,
            "max_tokens": item["max_tokens"],
        })

    results = pd.DataFrame(rows)
    if len(results) != 16 or results["prompt_id"].nunique() != 16:
        raise RuntimeError(f"{model_key}: paired runner did not produce 16 unique rows")

    output_dir = project_root / "results" / "evaluative_paired" / suite / model_key
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{model_key}-evaluative-paired.csv"
    results.to_csv(csv_path, index=False)
    _write_manifest(
        project_root=project_root,
        output_dir=output_dir,
        model=model,
        model_name=model_name,
        model_key=model_key,
        suite=suite,
        scale=scale,
        battery_path=battery_path,
        csv_path=csv_path,
        revision=revision,
        hf_commit_sha=hf_commit_sha,
    )
    return results


def _write_manifest(
    *,
    project_root: Path,
    output_dir: Path,
    model,
    model_name: str,
    model_key: str,
    suite: str,
    scale: str,
    battery_path: Path,
    csv_path: Path,
    revision: str | None,
    hf_commit_sha: str | None,
) -> Path:
    commit, dirty = _git_state(project_root)
    parameter = next(model.parameters())
    manifest_path = output_dir / f"{model_key}-evaluative-paired.md"
    lines = [
        "# Paired evaluative run manifest",
        "",
        f"- Run time (UTC): {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Git commit: `{commit}`",
        f"- Working tree dirty at run time: `{dirty}`",
        f"- Battery: `{battery_path.relative_to(project_root)}`",
        f"- Battery SHA-256: `{_sha256(battery_path)}`",
        f"- Result CSV: `{csv_path.relative_to(project_root)}`",
        f"- Result SHA-256: `{_sha256(csv_path)}`",
        "",
        "## Model",
        "",
        f"- Requested model: `{model_name}`",
        f"- Frozen model key: `{model_key}`",
        f"- Suite: `{suite}`",
        f"- Scale: `{scale}`",
        f"- Parameter dtype: `{parameter.dtype}`",
        f"- Device: `{parameter.device}`",
        f"- Layers: {model.cfg.n_layers}",
        f"- Heads: {model.cfg.n_heads}",
        f"- Hidden size: {model.cfg.d_model}",
        f"- Vocabulary size: {model.cfg.d_vocab}",
    ]
    if revision:
        lines.append(f"- Requested revision: `{revision}`")
    if hf_commit_sha:
        lines.append(f"- Resolved Hugging Face commit: `{hf_commit_sha}`")
    lines.extend([
        "",
        "## Generation",
        "",
        "- `do_sample=False`",
        "- `max_new_tokens=100`",
        "- Raw continuation preserved without stripping leading whitespace",
        "- Expected rows: 16",
        "- Written rows: 16",
        "",
        "## Environment",
        "",
        f"- Python: `{platform.python_version()}`",
        f"- torch: `{_package_version('torch')}`",
        f"- transformers: `{_package_version('transformers')}`",
        f"- transformer-lens: `{_package_version('transformer-lens')}`",
        "",
    ])
    manifest_path.write_text("\n".join(lines), encoding="utf-8")
    return manifest_path
