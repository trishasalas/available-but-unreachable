"""Render the canonical appendix for inclusion after the bibliography."""
from pathlib import Path
import subprocess

paper = Path(__file__).resolve().parents[1]
target = paper / "build-out" / "appendix.tex"
target.parent.mkdir(exist_ok=True)
subprocess.run([
    "pandoc", "--from", "markdown+tex_math_single_backslash", "--to", "latex",
    "--shift-heading-level-by=-1", "--wrap=none", "--natbib",
    str(paper / "sections" / "10-appendix.md"), "-o", str(target),
], check=True, cwd=paper)
text = target.read_text()
text = text.replace(
    "\\begin{longtable}",
    "\\Needspace{22\\baselineskip}\n\\begingroup\\small\n\\begin{longtable}",
).replace("\\end{longtable}", "\\end{longtable}\n\\endgroup")
target.write_text(text)
