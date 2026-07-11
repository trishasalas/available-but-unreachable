"""Byte-compare regenerated generation_text against docs/tangent.md quotes.

Parses the historical transcription's "1. Generation" blocks per (scale,
prompt), strips the echoed prompt, and compares against the continuation-only
generation_text in results/logits/{scale}_because_generations.csv.

Emits results/logits/REGEN_DIVERGENCE.md. Reproducible: regenerate the report
with `python -m src.tangent_byte_compare` (or run this file) after the exports
land. Do not hand-edit the report.
"""
import csv, re
from pathlib import Path

TMLR = Path("/Users/trishasalas/Repos/Research/tmlr")
TRANS = TMLR / "docs" / "tangent.md"
LOGITS = TMLR / "results" / "logits"

PROMPTS = {
    "skip_link": "A long navigation menu without a skip link is not accessible because",
    "screen_reader": "A website without screen reader support is not accessible because",
    "alt_text": "An image without alt text is not accessible because",
}
# transcription "## " model header -> our scale filename stem
MODEL_HEADERS = {
    "Pythia 2.8B": "pythia-2.8b",
    "Pythia 6.9B": "pythia-6.9b",
    "Pythia 12B": "pythia-12b",
    "GPT2 Medium": "gpt2-medium",
    "GPT2 Large": "gpt2-large",
    "GPT2 XL": "gpt2-xl",
}


def norm(s):
    """Collapse all whitespace to single spaces, strip."""
    return re.sub(r"\s+", " ", s).strip()


def which_prompt(line):
    for k, v in PROMPTS.items():
        if v in line:
            return k
    return None


def parse_transcription():
    """-> {(scale, compound): raw_generation_block_str}"""
    lines = TRANS.read_text().splitlines()
    out = {}
    scale = None
    compound = None
    capturing = False
    buf = []

    def flush():
        nonlocal buf, scale, compound
        if scale and compound and buf:
            out[(scale, compound)] = "\n".join(buf).strip()
        buf = []

    for ln in lines:
        m = re.match(r"^##\s+(.*?)\s*$", ln)
        if m and m.group(1) in MODEL_HEADERS:
            flush()
            scale = MODEL_HEADERS[m.group(1)]
            compound = None
            capturing = False
            continue
        # prompt line (either "### prompt = ..." or a bare prompt= line)
        p = which_prompt(ln)
        if p and ("prompt" in ln.lower() or ln.strip().startswith("###")):
            flush()
            compound = p
            capturing = False
            continue
        if re.match(r"^\s*1\.\s*Generation", ln):
            capturing = True
            buf = []
            continue
        if re.match(r"^\s*2\.\s*Where the correct token", ln):
            flush()
            capturing = False
            continue
        if re.match(r"^\s*3\.\s*Top-15", ln):
            capturing = False
            continue
        if capturing:
            buf.append(ln)
    flush()
    return out


def strip_prompt(gen_block, compound):
    """Remove the echoed prompt prefix from a transcription generation block."""
    n = norm(gen_block)
    p = norm(PROMPTS[compound])
    if n.startswith(p):
        return n[len(p):].strip()
    # some blocks echo the prompt after leading whitespace/markers; find it
    idx = n.find(p)
    if idx != -1:
        return n[idx + len(p):].strip()
    return n  # prompt not found; return as-is (flag later)


def first_diff(a, b):
    """Return (index, a_ctx, b_ctx) of first differing char over common prefix."""
    m = min(len(a), len(b))
    for i in range(m):
        if a[i] != b[i]:
            lo = max(0, i - 15)
            return i, a[lo:i + 20], b[lo:i + 20]
    if len(a) != len(b):
        return m, a[max(0, m - 20):], b[max(0, m - 20):]
    return None


def load_generations(scale):
    f = LOGITS / f"{scale}_because_generations.csv"
    if not f.exists():
        return None
    return {r["compound"]: r["generation_text"]
            for r in csv.DictReader(f.open())}


trans = parse_transcription()
report = ["# Tangent regeneration — divergence report",
          "",
          "Comparison of regenerated `generation_text` (continuation-only, 50",
          "greedy steps, `src/logit_export.export_because_tables`) against the",
          "hand-transcribed *1. Generation* blocks in `docs/tangent.md`.",
          "",
          "Whitespace is normalized (runs collapsed to single spaces) before",
          "comparison — the transcription carries hand-entered indentation and",
          "blank lines that are not model output. A **match** means the",
          "regenerated continuation reproduces the transcribed text over their",
          "common span; a **divergence** reports the first differing character.",
          "",
          "| scale | prompt | verdict | detail |",
          "|---|---|---|---|"]

# All scales the transcription covers, in report order. Whether each is
# compared or still pending is auto-detected from the presence of its
# generations CSV — so when 6.9B/12B land, no code change is needed.
TRANS_SCALES = ["pythia-2.8b", "pythia-6.9b", "pythia-12b",
                "gpt2-medium", "gpt2-large", "gpt2-xl"]
# Scales whose regen was produced on Colab GPU (Trisha), not local MPS (CC).
# The transcription's per-scale hardware is not fully recorded — only 12B is
# known to have run on Colab GPU — so these are flagged, not asserted to be a
# clean MPS-vs-CUDA cross-check.
COLAB_REGEN = {"pythia-6.9b", "pythia-12b"}

compared = 0        # (scale, compound) rows actually compared
exact = 0           # of those, exact matches
diverged = []       # (scale, compound, detail) for any divergence

for scale in TRANS_SCALES:
    gens = load_generations(scale)
    for compound in PROMPTS:
        key = (scale, compound)
        have_trans = key in trans
        mine = gens.get(compound) if gens else None
        if mine is None:
            report.append(f"| {scale} | {compound} | ⏳ pending | "
                          f"generations CSV not yet in results/logits/ |")
            continue
        if not have_trans:
            report.append(f"| {scale} | {compound} | ⚠ no transcription | "
                          f"regen present, no quote block to compare |")
            continue
        t = strip_prompt(trans[key], compound)
        m = norm(mine)
        d = first_diff(t, m)
        compared += 1
        hw = " (Colab-GPU regen)" if scale in COLAB_REGEN else ""
        if d is None:
            exact += 1
            report.append(f"| {scale} | {compound} | ✅ exact match "
                          f"(normalized){hw} | {len(m)} chars |")
        else:
            i, tctx, mctx = d
            det = (f"first diff @char {i}; "
                   f"trans=`…{tctx}…` vs regen=`…{mctx}…`")
            det = det.replace("|", "\\|").replace("\n", " ")
            diverged.append((scale, compound, det))
            report.append(f"| {scale} | {compound} | ⚠ divergence{hw} | "
                          f"{det} |")

# --- determinism summary (auto-counted over compared rows) ---
colab_done = sorted(s for s in COLAB_REGEN
                    if load_generations(s) is not None)
report += ["",
           "## Determinism",
           "",
           f"{exact}/{compared} compared (scale × prompt) comparisons are "
           "exact matches after whitespace normalization. Greedy (argmax) "
           "decoding is deterministic; where the transcription and the regen "
           "share hardware (MPS-local for 2.8B/GPT-2, CC) reproduction is "
           "bit-for-bit. Colab-GPU regens (Trisha) so far: "
           + (", ".join(colab_done) if colab_done else "none yet") +
           (". These reproduce the transcription exactly too — no near-tie "
            "flips have surfaced. Note the transcription's per-scale hardware "
            "is not fully recorded (only 12B is known to be Colab GPU), so an "
            "exact match here is reassurance, not a controlled MPS-vs-CUDA "
            "experiment."
            if not diverged else
            f". {len(diverged)} divergence(s) found overall — see rows above; "
            "report the logit margin at the flip step."),
           ""]

report += ["## Known findings — confirmation", ""]

# 12B cross-contamination: compare the two transcribed 12B strings directly.
sr = trans.get(("pythia-12b", "screen_reader"), "")
at = trans.get(("pythia-12b", "alt_text"), "")
sr_c = strip_prompt(sr, "screen_reader") if sr else ""
at_c = strip_prompt(at, "alt_text") if at else ""
report.append("**12B cross-contamination (transcription, to be confirmed by "
              "Trisha's Colab regen):**")
report.append(f"- screen_reader → `{sr_c[:90]}…`")
report.append(f"- alt_text → `{at_c[:90]}…`")
sr_ok = sr_c.startswith("it does not have a text alternative")
at_ok = at_c.startswith("it has no text alternative")
report.append(f"- matches handoff description: screen_reader={sr_ok}, "
              f"alt_text={at_ok}")
report.append("- The intro currently attributes the *screen-reader* answer to "
              "the *alt-text* question. Fix is Trisha's (placeholder flagged in "
              "`_rebuild/01-introduction.md`).")
report.append("")

# GPT-2 XL corrupted block: transcription's XL screen_reader "2. Where the
# correct token ranks" is a paste of a decision-point (rank-headed) table.
report.append("**GPT-2 XL corrupted block (transcription):** the XL "
              "screen_reader *2. Where the correct token ranks* section is a "
              "verbatim paste of a decision-point top-15 table (keeps the "
              "`rank` header and is identical to the XL skip-link *3. Top-15* "
              "block) — a copy-paste wound. The regenerated "
              "`gpt2-xl_screen_reader_because_steps.csv` supersedes it. Note: "
              "this wound is in the *step-trace* section, not the generation "
              "text, so it does not surface in the generation compare above.")

out = LOGITS / "REGEN_DIVERGENCE.md"
out.write_text("\n".join(report) + "\n")
print("\n".join(report))
print(f"\n>>> wrote {out}")
