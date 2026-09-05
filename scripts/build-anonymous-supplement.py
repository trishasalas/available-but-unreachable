"""Package saved evidence and anonymous source derivatives; never edit originals.

Run from the repository root. The ZIP is a review artifact, not an upload.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "build-out" / "tmlr-anonymous-supplement.zip"
paths = set()

def include(pattern):
    paths.update(p for p in ROOT.glob(pattern) if p.is_file() and "__pycache__" not in p.parts)

for pattern in [
    "src/*.py", "data/*.yaml", "data/binding/*.yaml", "requirements.txt",
    "data/infini_gram_calibration_counts.csv", "results/adhoc/d8_frequency_prior/*",
    "results/logits/pythia/*", "docs/audits/measurement-pathway-evidence/*",
    "results/analysis/*.csv", "results/frequency/**/*.csv", "results/frequency/**/*.md",
    "results/effective_binding/**/*.csv", "results/effective_binding/**/*.md",
    "results/evaluative_paired/**/*", "results/ablation/frequency_heads/pythia-2.8b/*registered-*",
    "results/elicitation/**/*accessibility.csv", "results/elicitation/**/*control.csv",
    "results/elicitation/**/*.md", "results/entropy/**/*accessibility.csv",
    "results/entropy/**/*control.csv", "results/entropy/**/*.md",
    "results/binding/**/*accessibility.csv", "results/binding/**/*.md",
    "docs/preregistrations/0002*", "docs/preregistrations/0003*",
    "docs/audits/2026-09-05-head-localization-reconciled*",
    "docs/audits/2026-09-05-registered-ablation*",
    "docs/audits/2026-09-05-condition-integration.md",
    "docs/audits/paired-results-audit.md", "paper/generate-figures/*.py",
]:
    include(pattern)
for stem in [
    "effective-binding-pythia", "effective-binding-gpt2", "effective-binding-olmo",
    "effective-binding-analysis", "frequency-head-ablation-pythia", "paired-evaluative-colab",
    "binding-pythia", "binding-gpt2", "binding-olmo",
    "elicitation-pythia", "elicitation-gpt2", "elicitation-olmo",
]:
    include(f"notebooks/{stem}.ipynb")

identity = re.compile(r"trisha|salas|/Users/|/home/[^/]+/", re.I)
manifest = []
files = {}
for path in sorted(paths):
    rel = path.relative_to(ROOT).as_posix()
    original = path.read_bytes()
    text = original.decode("utf-8")
    changes = []
    if path.suffix == ".ipynb":
        nb = json.loads(text)
        nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
        for cell in nb["cells"]:
            cell["metadata"] = {}
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
            source = "".join(cell.get("source", []))
            if "repo_owner" in source or "git', 'clone" in source or "GH_TMLR" in source:
                source = (
                    "# Anonymous supplement: open this notebook from the unpacked notebooks directory.\n"
                    "from pathlib import Path\nimport os, sys, subprocess, hashlib\n"
                    "PROJECT_ROOT = Path.cwd().parent\n"
                    "assert (PROJECT_ROOT / 'src').is_dir(), 'Open from the unpacked notebooks directory'\n"
                    "sys.path.insert(0, str(PROJECT_ROOT))\nos.chdir(PROJECT_ROOT)\n"
                )
                changes.append("replaced personal repository setup with unpacked-directory setup")
            elif re.search(r"git.{0,20}config|git push|git.{0,8}push", source):
                source = "# Repository publishing cell omitted from the anonymous supplement.\n"
                changes.append("removed repository publishing cell")
            cell["source"] = source.splitlines(keepends=True)
        text = json.dumps(nb, indent=1, ensure_ascii=False) + "\n"
        changes.append("cleared notebook outputs and metadata")
    if identity.search(text):
        text = re.sub(r"Trisha Salas|trishasalas|Trisha|Salas", "Author", text, flags=re.I)
        text = re.sub(r"/Users/[^/\s]+/", "/anonymous/", text)
        text = re.sub(r"/home/[^/\s]+/", "/anonymous/", text)
        changes.append("anonymized identity text or local home path")
    assert not identity.search(text), rel
    content = text.encode("utf-8")
    files[rel] = content
    manifest.append({
        "path": rel, "original_sha256": hashlib.sha256(original).hexdigest(),
        "packaged_sha256": hashlib.sha256(content).hexdigest(), "changes": changes,
    })

files["prompt-inventory.md"] = (ROOT / "docs/reviews/2026-09-05-appendix/prompt-inventory.md").read_bytes()
files["README.md"] = b"""# Anonymous reproducibility supplement

This package accompanies the manuscript. It contains frozen stimuli, saved results,
analysis code, inference notebooks, and provenance records. The manuscript appendix
is the guide to the reported estimands. Other domains in the shared inventories are
not evidence for cross-domain generalization; older result tables are not substitutes
for the canonical tables named below. No model weights are included.

## Main evidence

- Behavioral means: results/analysis/{pythia,gpt2,olmo}_gap.csv.
- Paired test: results/analysis/paired_gap_{cells,summary}.csv and paired_item_coded.csv.
- Raw binding versus accuracy: results/analysis/binding_accuracy_corr.csv.
- Value-weighted binding: results/analysis/effective_binding_correlations_{natural,uniform}.csv
  and effective_binding_aggregate_permutation_{natural,uniform}.csv.
- Declarative frequency: results/frequency/spearman_summary.csv, all_rows only;
  spearman_partial.csv for declarative sensitivity. spearman_accuracy.csv is historical.
- Registered intervention: results/ablation/frequency_heads/pythia-2.8b/*registered-*.

Read src/effective_binding_inputs.py before loading effective-binding inputs: it
resolves the saved GPT-2-large natural/uniform label reversal. GPT-2-medium uniform
is the verified rerun. Do not silently treat filenames alone as condition truth.
The shared Pile binding predictor differs from family-matched declarative predictors.
There is no new statistical token-count control for value-weighted binding.

## Running analyses

Use Python with numpy, pandas, scipy, PyYAML and matplotlib for saved-data analyses.
Inference additionally requires the model libraries; requirements.txt is a broad
development dependency list, not an exact reconstruction of every historical run.
Run manifests record available versions, checkpoints and hardware. Missing revisions
are not retrospectively filled. Inference notebooks may incur substantial compute.
Open notebooks from the unpacked notebooks directory. Personal clone and publishing
cells were replaced or omitted. Do not run the effective-binding analysis notebook's
head-selection cells over the registered frozen selection artifacts: those artifacts
are part of the intervention's provenance, not outputs to refresh for publication.

## Anonymization and hash provenance

Original repository files were not modified. Notebook outputs and metadata were
cleared; personal repository setup/publishing cells were removed or replaced. Identity
comments and personal local paths were anonymized. Scientific result CSVs are copied
unchanged. ANONYMIZATION.json maps original and packaged SHA-256 values and records
each transformation. SHA256SUMS.json verifies the contents of this package.

The registered saved-artifact audit passed all eleven original hashes in the source
repository. Its historical manifest retains those original hashes. The anonymous
frequency-head-ablation notebook has a different hash because its personal setup and
publishing cells were removed; running the original checker unchanged will stop at
that notebook hash. This package does not claim that its anonymous notebook bytes
reproduce the original notebook hash. Result statistics and frozen splits are intact.
Full baseline/intervened vocabulary distributions were not saved, so KL cannot be
independently reconstructed from CSVs alone.

The ZIP contains no Git history, credentials, manuscript author metadata, or links to
a named copy of this manuscript. The exact prompt inventory is prompt-inventory.md.
"""
files["ANONYMIZATION.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
# Keep the historical checker intact and supply an explicitly named derivative.
audit = files["docs/audits/2026-09-05-registered-ablation-check.py"].decode()
old_assert = " assert actual==digest,(path,actual,digest)"
assert audit.count(old_assert) == 1
audit = audit.replace(old_assert, ''' if actual != digest and path == 'notebooks/frequency-head-ablation-pythia.ipynb':
  entry = next(e for e in json.loads(Path('ANONYMIZATION.json').read_text()) if e['path'] == path)
  assert entry['original_sha256'] == digest and entry['packaged_sha256'] == actual
  print('ANONYMIZATION EXCEPTION: packaged notebook hash verified; original notebook hash is recorded, not independently reproduced.')
 else:
  assert actual == digest, (path, actual, digest)''')
audit = audit.replace(" print('Hash matches:',path)", " print('Original hash matches:',path) if actual == digest else None")
files["verify-registered-anonymous.py"] = audit.encode()
files["README.md"] += b"""

For a complete saved-data check in this anonymous package, run
`python verify-registered-anonymous.py` from the unpacked root. This separately
named derivative checks the ten unchanged original hashes and the anonymous
notebook's packaged hash. It explicitly reports the notebook exception before
recomputing selection, random controls and statistical tests. It does not claim
independent reproduction of the original notebook hash. The historical checker
under docs/audits/ is retained unchanged.
"""
for name, content in files.items():
    assert not identity.search(content.decode("utf-8")), name
files["SHA256SUMS.json"] = (json.dumps({k: hashlib.sha256(v).hexdigest() for k, v in files.items()}, indent=2) + "\n").encode()
OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, content in sorted(files.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 9, 5, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, content, compresslevel=9)
assert OUT.stat().st_size < 100_000_000, "Supplement exceeds TMLR's 100 MB limit"
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    for name, digest in json.loads(z.read("SHA256SUMS.json")).items():
        assert hashlib.sha256(z.read(name)).hexdigest() == digest, name
print(f"Verified {len(files)} files; ZIP {OUT.stat().st_size / 1e6:.2f} MB: {OUT}")
