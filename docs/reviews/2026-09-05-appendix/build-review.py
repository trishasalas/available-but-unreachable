"""The appendix preview has been integrated into the canonical manuscript.

This compatibility entry point builds paper/build-out/tmlr-submission.pdf.
It no longer generates alternate Markdown sections or a separate review PDF.
"""
from pathlib import Path
import subprocess

paper = Path(__file__).resolve().parents[3] / "paper"
subprocess.run(["bash", "build-paper.sh"], cwd=paper, check=True)
