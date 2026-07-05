"""D7: single-token-ban counterfactual at the Step 5 decision point.

Pre-registration: DECISIONS.md 2026-07-04 ("D7 pre-registered"), as AMENDED
2026-07-04: the prompt is the DECLARATIVE "A skip link is", per mlp.ipynb
cell 22 and results/mlp_investigation/pythia/pythia-12b_skip_link_steps.csv.
("evaluative" in the original entry was a drafting slip by its author;
tangent.md confirms the evaluative prompt has no Step-5 election.)

Ceremony order (enforced by run_d7 — no gate pass, no intervention):

  Gate 1 — LENS-PATHWAY REGRESSION. Reproduce the frozen trace via the
      ORIGINAL pathway (resid_post @ W_U, no ln_final — cell 22's exact
      computation). Requirement: the CHOSEN token sequence matches the
      frozen CSV for all 15 steps AND 'click' wins Step 5. Top-5 cell
      mismatches are recorded as discrepancies (dtype / numerics note)
      but do not fail the gate unless a chosen token diverges.

  Gate 2 — STANDARD-FORWARD AGREEMENT. Greedy via model() logits (the
      model's true output distribution, ln_final included) must also
      choose 'click' at Step 5. Lens/forward disagreement at Step 5 is
      an instrumentation question (pre-reg branch 3) -> hard abort.
      If Gate 2 passes, the A6 exhibit is retroactively strengthened:
      robust across unembedding pathways (see A6 provenance caveat,
      DECISIONS 2026-07-04).

  Intervention — conditions A and B, on the STANDARD forward pass:
      A (single-step ban):  banned ids floored to -inf at Step 5 only
      B (persistent ban):   banned ids floored to -inf at Step 5 and
                            every subsequent step

Ban list (frozen): "click", " click", "Click", " Click" — enumerated
from the tokenizer at runtime, single-token-ness ASSERTED, ids recorded
verbatim to d7_ban_list.csv before any generation (BPE side-door rule).

Success criterion: the frozen coding criteria (src/accuracy_coding.py,
concept 'skip link', declarative) applied to the full 50-token
continuation. Same practitioner bar as the elicitation experiment.
Note the frozen partial branch: "...not displayed..." alone codes
PARTIAL — branch 1 requires the completion to reach the skip-to-content
function (skip/jump + navigation/main content/section/specific location).

Pre-registered outcome branches (all ship; mechanical suggestion only —
the verdict paragraph is authored in DECISIONS, not by this script):
  1. correct continuation wins the banned election AND full completion
     codes correct  -> token competition causally demonstrated
  2. another incorrect token wins, completion incorrect -> competitor
     NEIGHBORHOOD finding
  3. degenerate/incoherent output -> instrumentation check first

Colab usage:
    !pip install transformer_lens==2.17.0
    # clone the repo (or upload src/ + this file), cd to repo root
    from transformer_lens import HookedTransformer
    model = HookedTransformer.from_pretrained("pythia-12b")
    # ^ DEFAULTS ON PURPOSE — no dtype, no device override. This mirrors
    #   mlp.ipynb cell 4 (`from_pretrained(model_name)`), the load that
    #   produced the frozen trace. Gate 1 reproduces the original run's
    #   numerics; changing precision here would be self-inflicted pathway
    #   drift. Actual dtype/device are recorded in d7_summary.md.
    from src.d7_token_ban import run_d7
    run_d7(model, ".")
    # then files.download() everything in results/logits/
    # (loss class: ephemeral /content — DECISIONS 2026-07-02)

Outputs -> results/logits/ :
    d7_ban_list.csv
    d7_gate1_lens_regression.csv
    d7_gate2_forward_trace.csv
    d7_step5_ranks_preban.csv
    d7_conditionA_steps.csv, d7_conditionA_step5_postban_ranks.csv
    d7_conditionB_steps.csv, d7_conditionB_step5_postban_ranks.csv
    d7_summary.md
"""

import csv
import datetime
from pathlib import Path

import torch

try:
    from .accuracy_coding import code_response
except ImportError:  # running with src/ on sys.path (Colab upload pattern)
    from accuracy_coding import code_response


# --------------------------------------------------------------------------
# Frozen constants — do not edit without a new pre-registration.
# --------------------------------------------------------------------------

PROMPT = "A skip link is"          # AMENDED referent: declarative trace prompt
MODEL_NAME = "pythia-12b"
REQUIRED_TL_VERSION = "2.17.0"     # pinned in the pre-registration
DECISION_STEP = 5                  # the Step 5 election
N_TRACE_STEPS = 15                 # matches the frozen CSV (steps 0-14)
N_GEN_TOKENS = 50                  # long enough for coding (see docstring)
TOP_K_RECORD = 15                  # decision-point ranks table depth
BAN_SURFACE_FORMS = ("click", " click", "Click", " Click")
CORRECT_TOKEN_STRIPPED = "displayed"   # branch-1 watch token (rank 4 frozen)
COMPETITOR_STRIPPED = "click"          # the frozen Step-5 winner

# Frozen expected trace, embedded verbatim from
# results/mlp_investigation/pythia/pythia-12b_skip_link_steps.csv
# (generated by mlp.ipynb cell 22; provenance: DECISIONS 2026-06-28 MLP
# investigation entry). Embedded so the gate works in an ephemeral Colab
# session even without a repo checkout — and so what we compared against
# is itself in version control.
FROZEN_TRACE = [
    # step, chosen, top1, top2, top3, top4, top5
    (0,  "a",       "a",       "an",       "used",      "generally", "typically"),
    (1,  "link",    "link",    "type",     "special",   "component", "web"),
    (2,  "that",    "that",    "to",       "between",   "which",     "in"),
    (3,  "is",      "is",      "allows",   "can",       "points",    "links"),
    (4,  "not",     "not",     "used",     "embedded",  "displayed", "placed"),
    (5,  "click",   "click",   "visible",  "followed",  "displayed", "a"),
    (6,  "able",    "able",    "-",        "able",      "b",         "ba"),
    (7,  ".",       ".",       ",",        "by",        "and",       "or"),
    (8,  "It",      "It",      "A",        "Skip",      "The",       "This"),
    (9,  "is",      "is",      "can",      "'s",        "may",       "appears"),
    (10, "used",    "used",    "usually",  "a",         "often",     "typically"),
    (11, "to",      "to",      "in",       "for",       "as",        "when"),
    (12, "link",    "link",    "navigate", "create",    "connect",   "indicate"),
    (13, "to",      "to",      "a",        "from",      "other",     "pages"),
    (14, "another", "another", "a",        "other",     "content",   "an"),
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _get_tl_version():
    """TransformerLens does not expose __version__ as a module attribute
    (true throughout 2.x) — the installed version lives in package
    metadata. Try both distribution-name spellings, then fall back."""
    try:
        from importlib.metadata import version, PackageNotFoundError
        for dist in ("transformer_lens", "transformer-lens"):
            try:
                return version(dist)
            except PackageNotFoundError:
                continue
    except Exception:
        pass
    import transformer_lens
    return getattr(transformer_lens, "__version__", "unknown")


def _check_tl_version(allow_mismatch=False):
    v = _get_tl_version()
    if v != REQUIRED_TL_VERSION:
        msg = (f"TransformerLens {v} != pinned {REQUIRED_TL_VERSION} "
               f"(pre-reg frozen). pip install "
               f"transformer_lens=={REQUIRED_TL_VERSION}")
        if not allow_mismatch:
            raise RuntimeError(msg)
        print(f"WARNING (override active): {msg}")
    return v


def enumerate_ban_list(model, out_dir):
    """Enumerate ban-list token ids from the tokenizer BEFORE any
    generation; assert single-token-ness; record verbatim (BPE side-door
    rule). Returns list of (surface_form, token_id)."""
    ban = []
    for surface in BAN_SURFACE_FORMS:
        ids = model.to_tokens(surface, prepend_bos=False)[0]
        assert ids.shape[0] == 1, (
            f"Ban surface form {surface!r} tokenizes to {ids.shape[0]} "
            f"tokens ({ids.tolist()}) — not single-token; pre-reg ban "
            f"mechanism (logit floor on one id) cannot apply. Record and "
            f"stop; this is a pre-registration amendment situation, not a "
            f"workaround situation.")
        ban.append((surface, int(ids[0].item())))

    path = out_dir / "d7_ban_list.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["surface_form_repr", "token_id"])
        for surface, tid in ban:
            w.writerow([repr(surface), tid])
    print(f"ban list recorded: {path.name} -> "
          f"{[(repr(s), t) for s, t in ban]}")
    return ban


def lens_trace(model, n_steps=N_TRACE_STEPS):
    """Cell 22's exact computation: resid_post at the final block,
    unembedded via W_U directly (no ln_final). Reproduced verbatim for
    the regression gate — this is deliberately NOT the model's true
    output pathway (see A6 provenance caveat)."""
    device = next(model.parameters()).device
    tokens = model.to_tokens(PROMPT)
    last_block = model.cfg.n_layers - 1
    hook_name = f"blocks.{last_block}.hook_resid_post"
    rows = []
    for step in range(n_steps):
        _, cache = model.run_with_cache(
            tokens, names_filter=lambda name: name == hook_name)
        last_pos = tokens.shape[1] - 1
        final_resid = cache[hook_name][0, last_pos]
        logits = final_resid @ model.W_U
        top5 = logits.topk(5)
        top_tokens = [model.to_string(t.unsqueeze(0)).strip()
                      for t in top5.indices]
        next_token = logits.argmax().unsqueeze(0).unsqueeze(0)
        chosen = model.to_string(next_token[0]).strip()
        rows.append({"step": step, "chosen": chosen,
                     "top1": top_tokens[0], "top2": top_tokens[1],
                     "top3": top_tokens[2], "top4": top_tokens[3],
                     "top5": top_tokens[4]})
        tokens = torch.cat([tokens, next_token.to(device)], dim=1)
        del cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    return rows


def forward_trace(model, n_steps, banned_ids=None, ban_mode=None,
                  record_step5_topk=True):
    """Greedy generation via the model's TRUE forward pass (ln_final
    included). ban_mode: None | 'A' (step == DECISION_STEP only) |
    'B' (step >= DECISION_STEP). Returns (rows, step5_ranks, gen_ids)
    where step5_ranks is the post-ban top-k at the decision step (or
    pre-ban when no ban applies)."""
    device = next(model.parameters()).device
    input_ids = model.to_tokens(PROMPT)
    current_ids = input_ids.clone()
    banned = torch.tensor([tid for _, tid in banned_ids],
                          device=device) if banned_ids else None
    rows, step5_ranks = [], []
    with torch.no_grad():
        for step in range(n_steps):
            logits = model(current_ids)[0, -1, :]
            ban_applies = (
                banned is not None and (
                    (ban_mode == "A" and step == DECISION_STEP) or
                    (ban_mode == "B" and step >= DECISION_STEP)))
            if ban_applies:
                logits[banned] = float("-inf")
            if step == DECISION_STEP and record_step5_topk:
                vals, idxs = torch.topk(logits, TOP_K_RECORD)
                for rank, (v, i) in enumerate(zip(vals, idxs)):
                    tok = model.to_string(torch.tensor([i.item()]))
                    step5_ranks.append({
                        "rank": rank, "token_id": int(i.item()),
                        "token_repr": repr(tok),
                        "token_stripped": tok.strip(),
                        "logit": float(v.item()),
                        "ban_applied_this_step": ban_applies})
            nt = int(torch.argmax(logits).item())
            tok = model.to_string(torch.tensor([nt]))
            rows.append({"step": step, "token_id": nt,
                         "token_repr": repr(tok),
                         "token_stripped": tok.strip(),
                         "logit": float(logits[nt].item()),
                         "ban_applied": ban_applies})
            current_ids = torch.cat(
                [current_ids, torch.tensor([[nt]], device=device)], dim=1)
    gen_ids = current_ids[0, input_ids.shape[1]:]
    return rows, step5_ranks, gen_ids


def _write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.name} ({len(rows)} rows)")


# --------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------

def gate1_regression(model, out_dir):
    """Lens-pathway reproduction of the frozen trace."""
    rows = lens_trace(model)
    out, discrepancies, chosen_diverged = [], [], False
    for row, frozen in zip(rows, FROZEN_TRACE):
        step, f_chosen, *f_top = frozen
        rec = dict(row)
        rec.update({"expected_chosen": f_chosen,
                    "chosen_match": row["chosen"] == f_chosen})
        for k, expected in zip(("top1", "top2", "top3", "top4", "top5"),
                               f_top):
            match = row[k] == expected
            rec[f"{k}_match"] = match
            if not match:
                discrepancies.append(
                    f"step {step} {k}: got {row[k]!r} expected {expected!r}")
        if not rec["chosen_match"]:
            chosen_diverged = True
            discrepancies.append(
                f"step {step} CHOSEN: got {row['chosen']!r} "
                f"expected {f_chosen!r}")
        out.append(rec)
    _write_csv(out_dir / "d7_gate1_lens_regression.csv", out)

    step5 = rows[DECISION_STEP]
    click_wins = step5["chosen"] == COMPETITOR_STRIPPED
    passed = (not chosen_diverged) and click_wins
    return passed, discrepancies, click_wins


def gate2_agreement(model, out_dir):
    """Standard forward pass must also elect 'click' at Step 5."""
    rows, step5_ranks, _ = forward_trace(model, N_TRACE_STEPS)
    _write_csv(out_dir / "d7_gate2_forward_trace.csv", rows)
    _write_csv(out_dir / "d7_step5_ranks_preban.csv", step5_ranks)
    click_wins = rows[DECISION_STEP]["token_stripped"] == COMPETITOR_STRIPPED
    displayed_rank = next(
        (r["rank"] for r in step5_ranks
         if r["token_stripped"] == CORRECT_TOKEN_STRIPPED), None)
    return click_wins, displayed_rank


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def run_d7(model, project_root, allow_tl_version_mismatch=False):
    project_root = Path(project_root)
    out_dir = project_root / "results" / "logits"
    out_dir.mkdir(parents=True, exist_ok=True)

    tl_version = _check_tl_version(allow_tl_version_mismatch)
    dtype = str(next(model.parameters()).dtype)
    device = str(next(model.parameters()).device)
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    summary = [
        "# D7 run summary", "",
        f"- timestamp: {stamp}",
        f"- model: {MODEL_NAME}  |  TL: {tl_version}  |  "
        f"dtype: {dtype}  |  device: {device}",
        f"- prompt (frozen, amended referent): {PROMPT!r}", ""]

    # Ban list first — enumerated and recorded before any generation.
    ban = enumerate_ban_list(model, out_dir)
    summary.append(f"- ban list: {[(repr(s), t) for s, t in ban]}")

    # ---- Gate 1 ----
    g1_pass, discrepancies, g1_click = gate1_regression(model, out_dir)
    summary += ["", "## Gate 1 — lens-pathway regression",
                f"- chosen sequence matches frozen CSV, 15 steps: "
                f"{'YES' if g1_pass or not discrepancies else 'see below'}",
                f"- 'click' wins Step 5 (lens): {g1_click}",
                f"- PASSED: {g1_pass}"]
    if discrepancies:
        summary.append("- discrepancies (recorded, dtype/numerics note):")
        summary += [f"    - {d}" for d in discrepancies]
    if not g1_pass:
        summary += ["", "**ABORT: Gate 1 failed. No reproduction, no "
                        "experiment (pre-reg). Instrumentation check "
                        "before any interpretation (branch 3).**"]
        (out_dir / "d7_summary.md").write_text("\n".join(summary))
        raise RuntimeError("D7 Gate 1 failed — see d7_summary.md")

    # ---- Gate 2 ----
    g2_click, displayed_rank = gate2_agreement(model, out_dir)
    summary += ["", "## Gate 2 — standard-forward agreement",
                f"- 'click' wins Step 5 (true forward pass): {g2_click}",
                f"- 'displayed' rank at Step 5 (pre-ban): {displayed_rank}"]
    if not g2_click:
        summary += ["", "**ABORT: lens and forward pass disagree at Step 5. "
                        "Instrumentation question (branch 3) — stop, "
                        "exonerate the harness before interpreting.**"]
        (out_dir / "d7_summary.md").write_text("\n".join(summary))
        raise RuntimeError("D7 Gate 2 failed — see d7_summary.md")
    summary.append("- NOTE: forward-pass agreement retroactively "
                   "strengthens the A6 exhibit (robust across unembedding "
                   "pathways).")

    # ---- Intervention ----
    for mode in ("A", "B"):
        rows, step5_ranks, gen_ids = forward_trace(
            model, N_GEN_TOKENS, banned_ids=ban, ban_mode=mode)
        _write_csv(out_dir / f"d7_condition{mode}_steps.csv", rows)
        _write_csv(out_dir / f"d7_condition{mode}_step5_postban_ranks.csv",
                   step5_ranks)
        continuation = model.to_string(gen_ids)
        coding = code_response("declarative", "skip link",
                               PROMPT, continuation)
        winner = rows[DECISION_STEP]
        summary += [
            "", f"## Condition {mode} "
                f"({'single-step ban' if mode == 'A' else 'persistent ban'})",
            f"- Step 5 winner under ban: {winner['token_repr']} "
            f"(id {winner['token_id']}, logit {winner['logit']:.3f})",
            f"- full continuation ({N_GEN_TOKENS} tokens): "
            f"{continuation!r}",
            f"- frozen-criteria coding: **{coding}**"]

    summary += [
        "", "## Branch suggestion (mechanical — verdict paragraph is "
            "authored in DECISIONS, same session, whichever branch fired)",
        "- branch 1 requires: correct-continuation token wins the banned "
        "election AND full completion codes correct",
        "- branch 2: another incorrect token wins, completion incorrect "
        "(competitor neighborhood)",
        "- branch 3: degenerate/incoherent -> instrumentation first",
        "- A-vs-B divergence is itself reportable (competitor persistence)."]
    (out_dir / "d7_summary.md").write_text("\n".join(summary))
    print(f"\nD7 complete. Read {out_dir / 'd7_summary.md'} and come home "
          f"to DECISIONS.md.")
