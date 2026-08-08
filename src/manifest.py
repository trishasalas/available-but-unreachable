import platform, subprocess, datetime
import torch
from importlib.metadata import version


def _write_manifest(PROJECT_ROOT, output_dir, model_name, model, battery_name, domain_counts, results_df, prompt_files, gen_kwargs=None, hf_commit_sha=None, revision=None):
    """Shared manifest writer. Call one of the per-battery wrappers below."""
    try:
        commit = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'], cwd=PROJECT_ROOT, text=True).strip()
        dirty = subprocess.check_output(
            ['git', 'status', '--porcelain'], cwd=PROJECT_ROOT, text=True).strip() != ''
    except Exception:
        commit, dirty = 'unknown', False

    with open(output_dir / f'{model_name}-{battery_name}.md', 'w') as f:
        f.write(f"# Model data captured during {battery_name.title()} Battery\n\n")
        f.write(f"- Run (UTC): {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
        f.write(f"- Git commit: {commit}{' (DIRTY)' if dirty else ''}\n\n")

        f.write(f"## Model\n\n")
        f.write(f"- Model name: {model_name}\n")
        f.write(f"- Model dtype: {next(model.parameters()).dtype}\n")
        f.write(f"- Device: {next(model.parameters()).device}\n")
        f.write(f"- Layers: {model.cfg.n_layers}\n")
        f.write(f"- Heads: {model.cfg.n_heads}\n")
        f.write(f"- Hidden size: {model.cfg.d_model}\n")
        f.write(f"- Vocab size: {model.cfg.d_vocab}\n")
        f.write(f"- Params: {sum(p.numel() for p in model.parameters())/1e6:.1f}M\n")
        if revision:
            f.write(f"- Revision: {revision}\n")
        f.write(f"\n")

        f.write(f"## Server\n\n")
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            f.write(f"- GPU: {gpu_name}\n")
        elif torch.backends.mps.is_available():
            f.write(f"- GPU: Apple MPS\n")
        else:
            f.write(f"- GPU: CPU\n")
        f.write(f"\n")

        if gen_kwargs:
            f.write(f"## Generation\n\n")
            for k, v in gen_kwargs.items():
                f.write(f"- {k}: {v}\n")
            f.write(f"\n")

        f.write(f"## Environment\n\n")
        f.write(f"- transformer_lens: {version('transformer_lens')}\n")
        f.write(f"- transformers: {version('transformers')}\n")
        f.write(f"- torch: {version('torch')}\n")
        f.write(f"- python: {platform.python_version()}\n")
        f.write(f"- platform: {platform.platform()}\n\n")

        if hf_commit_sha:
            f.write(f"## Hugging Face\n\n")
            f.write(f"- Commit SHA: {hf_commit_sha}\n")
            if revision:
                f.write(f"- Revision: {revision}\n")
            f.write(f"\n")

        f.write(f"## Domains\n\n")
        f.write(f"| domain | expected | written | file |\n")
        f.write(f"|---|---|---|---|\n")
        for d, c in domain_counts.items():
            flag = '' if c['expected'] == c['written'] else ' ⚠️'
            f.write(f"| {d} | {c['expected']} | {c['written']}{flag} | `{c['file']}` |\n")
        f.write(f"\n**Total rows:** {len(results_df)}\n")
        f.write(f"**Domains completed:** {len(domain_counts)} / {len(prompt_files)}\n")


def write_elicitation_manifest(PROJECT_ROOT, output_dir, model_name, model,
                               domain_counts, results_df, prompt_files,
                               gen_kwargs, revision=None, hf_commit_sha=None):
    """Elicitation generates text, so gen_kwargs is required."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "elicitation",
        domain_counts, results_df, prompt_files,
        gen_kwargs=gen_kwargs, hf_commit_sha=hf_commit_sha, revision=revision)


def write_entropy_manifest(PROJECT_ROOT, output_dir, model_name, model,
                           domain_counts, results_df, prompt_files,
                           revision=None, hf_commit_sha=None):
    """Entropy is forward-pass only — no generation settings to record."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "entropy",
        domain_counts, results_df, prompt_files,
        hf_commit_sha=hf_commit_sha, revision=revision)


def write_binding_manifest(PROJECT_ROOT, output_dir, model_name, model,
                           domain_counts, results_df, prompt_files,
                           revision=None, hf_commit_sha=None):
    """Binding is forward-pass only — no generation settings to record."""
    return _write_manifest(
        PROJECT_ROOT, output_dir, model_name, model, "binding",
        domain_counts, results_df, prompt_files,
        hf_commit_sha=hf_commit_sha, revision=revision)
