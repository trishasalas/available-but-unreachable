"""Synthetic smoke tests for the dedicated paired-battery runner."""

from pathlib import Path
import shutil
import tempfile
import unittest

import pandas as pd

from src.paired_evaluative_runner import GENERATION, run_paired_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class _FakeParameter:
    dtype = "float32"
    device = "cpu"


class _FakeConfig:
    n_layers = 1
    n_heads = 1
    d_model = 8
    d_vocab = 32


class _FakeModel:
    cfg = _FakeConfig()

    def parameters(self):
        return iter([_FakeParameter()])

    def generate(self, prompt, **kwargs):
        if kwargs != GENERATION:
            raise AssertionError(f"unexpected generation settings: {kwargs}")
        return prompt + "\n accessible based on the code shown"


class PairedRunnerTests(unittest.TestCase):
    def test_runner_preserves_raw_continuation_and_writes_only_paired_tree(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_dir = root / "data"
            data_dir.mkdir()
            battery = data_dir / "evaluative_paired.yaml"
            shutil.copyfile(
                PROJECT_ROOT / "data" / "evaluative_paired.yaml",
                battery,
            )
            shutil.copyfile(
                PROJECT_ROOT / "data" / "accessibility.yaml",
                data_dir / "accessibility.yaml",
            )

            result = run_paired_model(
                _FakeModel(),
                model_name="pythia-160m",
                project_root=root,
                battery_path=battery,
                revision="synthetic-test",
                hf_commit_sha="synthetic-sha",
            )

            self.assertEqual(len(result), 16)
            self.assertTrue(result["output"].str.startswith("\n ").all())
            output_dir = (
                root
                / "results"
                / "evaluative_paired"
                / "pythia"
                / "pythia-160m"
            )
            csv_path = output_dir / "pythia-160m-evaluative-paired.csv"
            manifest_path = output_dir / "pythia-160m-evaluative-paired.md"
            self.assertTrue(csv_path.exists())
            self.assertTrue(manifest_path.exists())
            saved = pd.read_csv(csv_path, keep_default_na=False)
            self.assertTrue(saved["output"].str.startswith("\n ").all())
            self.assertFalse((root / "results" / "analysis").exists())
            manifest = manifest_path.read_text(encoding="utf-8")
            self.assertIn("Raw continuation preserved", manifest)
            self.assertIn("synthetic-sha", manifest)


if __name__ == "__main__":
    unittest.main()
