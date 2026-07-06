"""
D6 — multi-head joint ablation (the distributed-ensemble test).

Spec: docs/superpowers/specs/2026-06-29-multihead-lexical-ablation-design.md
Pre-registration: DECISIONS.md (D6 entry — commit before first forward pass).

Claim the run licenses (scoped, per spec): even the strongest lexical lead
(screen reader) is DISTRIBUTED across heads, not a localized circuit. Screen
reader is the hardest case for the null to survive; the robustness panel is
support, not the claim.

The load-bearing design decision (spec §"which head set"): raw top-binding
heads are early structural plumbing (L1/H12 et al.). Stage A therefore EARNS
the ablation set — deep (min_layer) ∧ selective (own-compound collocation beats
every other domain under a UNIFORM template, per the C1 metric caveat) ∧ not
(sink ∨ structural). The excluded heads are not discarded: they become the
labeled contrast / positive-control tail of the cumulative curve.

One compound per visit (D8 pattern). Model loads once per session, passed in.

Usage (from notebook):
    from src.d6_multihead_ablation import run_d6, sanity_check, COMPOUNDS
    sanity_check(model)                       # once per session
    run_d6(model, PROJECT_ROOT, "screen_reader")

Outputs (repo convention — results are CSVs, ledgers accumulate):
    results/pythia/pythia-2.8b-candidate-heads.csv     (Stage A, per compound)
    results/pythia/pythia-2.8b-multihead-ablation.csv  (Stage B curves)
"""

from pathlib import Path

import pandas as pd

try:  # package import (repo) — flat import (Colab upload) fallback
    from .binding import run_single_compound
    from .head_characterization import (
        DOMAIN_COMPOUNDS, SINK_THRESHOLD, STRUCTURAL_THRESHOLD,
        characterize_heads, collocation_scan,
    )
    from .qk_ov import ablate_head_at_position, ablate_heads_at_position, \
        cumulative_ablation, find_token_index
except ImportError:
    from binding import run_single_compound
    from head_characterization import (
        DOMAIN_COMPOUNDS, SINK_THRESHOLD, STRUCTURAL_THRESHOLD,
        characterize_heads, collocation_scan,
    )
    from qk_ov import ablate_head_at_position, ablate_heads_at_position, \
        cumulative_ablation, find_token_index


MODEL_NAME = "pythia-2.8b"          # single model under test, per spec

# compound: (word1, word2, natural_prompt, dest_word, role, domain)
# dest_word = the compound's second word — the position whose composed
# representation the earned heads write into; ablation lands there.
COMPOUNDS = {
    "screen_reader": ("screen", "reader", "A screen reader is",
                      "reader", "primary", "a11y"),
    "alt_text":      ("alt", "text", "The purpose of alt text is",
                      "text", "robustness", "a11y"),
    "stock_market":  ("stock", "market", "A stock market is",
                      "market", "robustness", "finance"),
    "semantic_html": ("semantic", "HTML", "Semantic HTML helps",
                      "HTML", "robustness", "a11y"),
}

# Negative (specificity) control: the earned screen-reader set ablated on the
# weak-collocation control compound — expect flat (these heads don't bind here).
NEG_CONTROL = ("bicycle", "wheel", "A bicycle wheel is", "wheel")

# Uniform frame for the selectivity scan (C1: cross-domain binding comparisons
# require a uniform template — natural prompts confound position with content).
UNIFORM_TEMPLATE = "A {w1} {w2} is"

# ---- Stage A knobs (surfaced, not buried; freeze in the pre-reg entry) ---- #
MIN_LAYER = 10          # spec default; refine from the Stage A table if needed
N_CANDIDATES = 18       # spec: N ≈ 15–20 so the deep tail is captured
SELECTIVITY_FLOOR = 0.3   # own-compound uniform-template attention must clear this
SELECTIVITY_RATIO = 1.5   # ...and exceed max other-domain score by this factor
TAIL_LEN = 5            # structural/sink heads appended as positive-control tail


# --------------------------------------------------------------------------- #
# Stage A — earn the candidate set                                             #
# --------------------------------------------------------------------------- #
def _binding_rows(model, project_root, compound_name):
    """Per-head binding scores for the compound at 2.8B. Reads the frozen
    binding CSV when the compound is in the sweep; otherwise runs a fresh
    in-memory single-compound pass (same math — binding.run_single_compound,
    one forward pass) for out-of-sweep compounds like stock_market."""
    csv = Path(project_root) / "results/pythia" / f"{MODEL_NAME}-binding.csv"
    if csv.exists():
        df = pd.read_csv(csv)
        sub = df[df["compound"] == compound_name]
        if len(sub):
            return sub[["compound", "layer", "head", "binding_score"]].copy(), "frozen CSV"
    w1, w2, prompt = COMPOUNDS[compound_name][:3]
    rows = run_single_compound(model, compound_name, w1, w2, prompt)
    if not rows:
        raise ValueError(f"binding pass found no tokens for '{compound_name}'")
    return (pd.DataFrame(rows)[["compound", "layer", "head", "binding_score"]],
            "fresh in-memory pass (compound not in the frozen sweep)")


def _domain_dict_with(compound_name):
    """DOMAIN_COMPOUNDS extended (not mutated) so the compound under test is
    guaranteed present in its own domain for the selectivity scan."""
    w1, w2, prompt, _dest, _role, domain = COMPOUNDS[compound_name]
    dc = {k: list(v) for k, v in DOMAIN_COMPOUNDS.items()}
    dc.setdefault(domain, [])
    if not any(a == w1 and b == w2 for a, b, _p in dc[domain]):
        dc[domain].append((w1, w2, prompt))
    return dc


def _on_target_attention(model, prompt, heads, dest_word):
    """BOS and position-1 attention measured FROM the compound's word2 position
    ON the compound's own prompt (AMENDED 2026-07-06).

    The unconditional metric (generic prompts) conflates structural sinks with
    selective heads at idle: a selective head has nothing to do off-target and
    parks its mass on BOS — the parking is the selectivity's shadow, not
    evidence against it (first run: 16/18 candidates flagged sink, including
    both selective heads; L29/H7 generic BOS 0.91 vs on-target ~0.0001 to
    pos-1, 0.90 to word1). A TRUE structural sink parks on BOS even when a
    bindable target is present. This restores the April characterization's
    operationalization ('not BOS' was measured at the reader position).
    """
    str_tokens = model.to_str_tokens(prompt)
    di = find_token_index(str_tokens, dest_word)
    if di is None:
        raise ValueError(
            f"dest_word '{dest_word}' not found in prompt tokens: {str_tokens}")
    _, cache = model.run_with_cache(
        prompt, names_filter=lambda n: n.endswith("pattern"))
    rows = []
    for layer, head in heads:
        pat = cache["pattern", int(layer)][0, int(head)]  # [dest, src]
        rows.append({"layer": int(layer), "head": int(head),
                     "bos_attention": round(float(pat[di, 0]), 4),
                     "attn_to_pos1": round(float(pat[di, 1]), 4)})
    return pd.DataFrame(rows)


def earn_candidate_set(model, project_root, compound_name,
                       min_layer=MIN_LAYER, n_candidates=N_CANDIDATES):
    """
    Stage A: derive + characterize the deep candidate heads for one compound.

    Returns DataFrame[compound, layer, head, binding_score, induction,
    prev_token, dup_token, type, bos_attention, attn_to_pos1, own_score,
    max_other_score, max_other_domain, selective, sink, structural,
    in_lexical_set, binding_source].
    """
    binding, source = _binding_rows(model, project_root, compound_name)
    deep = (binding[binding["layer"] >= min_layer]
            .sort_values("binding_score", ascending=False)
            .head(n_candidates))
    heads = list(zip(deep["layer"].astype(int), deep["head"].astype(int)))
    print(f"Stage A [{compound_name}]: {len(heads)} deep candidates "
          f"(min_layer={min_layer}, source: {source})")

    char = characterize_heads(model, heads)
    # AMENDED 2026-07-06: sink/structural measured on-target (from the word2
    # position on the compound's own prompt), not on generic prompts.
    _w1c, _w2c, nat_prompt, dest_c = COMPOUNDS[compound_name][:4]
    onpos = _on_target_attention(model, nat_prompt, heads, dest_c)

    # Selectivity under the uniform template (C1 caveat): own-compound score
    # vs the strongest score from any OTHER domain.
    w1, w2 = COMPOUNDS[compound_name][:2]
    own_label = f"{w1} {w2}"
    own_domain = COMPOUNDS[compound_name][5]
    colloc = collocation_scan(model, heads,
                              domain_compounds=_domain_dict_with(compound_name),
                              template=UNIFORM_TEMPLATE)
    sel_rows = []
    for layer, head in heads:
        hc = colloc[(colloc["layer"] == layer) & (colloc["head"] == head)]
        own = hc[hc["compound"] == own_label]["score"]
        own_score = float(own.iloc[0]) if len(own) else float("nan")
        others = hc[hc["domain"] != own_domain]
        if len(others):
            top_other = others.loc[others["score"].idxmax()]
            max_other, max_dom = float(top_other["score"]), top_other["domain"]
        else:
            max_other, max_dom = float("nan"), "—"
        sel_rows.append({
            "layer": layer, "head": head,
            "own_score": round(own_score, 4),
            "max_other_score": round(max_other, 4),
            "max_other_domain": max_dom,
            "selective": bool(own_score >= SELECTIVITY_FLOOR
                              and own_score >= SELECTIVITY_RATIO * max_other),
        })
    sel = pd.DataFrame(sel_rows)

    out = (deep.merge(char, on=["layer", "head"])
               .merge(onpos, on=["layer", "head"])
               .merge(sel, on=["layer", "head"]))
    out["sink"] = out["bos_attention"] >= SINK_THRESHOLD
    out["structural"] = out["attn_to_pos1"] >= STRUCTURAL_THRESHOLD
    # Spec definition, verbatim: deep ∧ selective ∧ not (sink ∨ structural).
    out["in_lexical_set"] = out["selective"] & ~out["sink"] & ~out["structural"]
    out["binding_source"] = source
    out = out.sort_values("binding_score", ascending=False).reset_index(drop=True)

    n_lex = int(out["in_lexical_set"].sum())
    print(f"  earned lexical set: {n_lex} heads — "
          + (", ".join(f"L{r.layer}H{r.head}" for r in
                       out[out["in_lexical_set"]].itertuples()) or "(empty!)"))
    return out


# --------------------------------------------------------------------------- #
# Stage B — joint ablation with controls                                       #
# --------------------------------------------------------------------------- #
def _ordered_with_tail(cand):
    """Ablation order: earned lexical set (binding desc), then up to TAIL_LEN
    excluded sink/structural heads (binding desc) as the labeled positive-
    control tail. Returns (ordered_heads, segments)."""
    lex = cand[cand["in_lexical_set"]]
    tail = cand[~cand["in_lexical_set"] & (cand["sink"] | cand["structural"])]
    tail = tail.head(TAIL_LEN)
    heads = ([(int(r.layer), int(r.head)) for r in lex.itertuples()]
             + [(int(r.layer), int(r.head)) for r in tail.itertuples()])
    segments = ["lexical"] * len(lex) + ["structural_tail"] * len(tail)
    return heads, segments


def run_joint_ablation(model, cand, compound_name):
    """Stage B for one compound: cumulative curve over the earned set + tail,
    plus (for the primary) the bicycle-wheel negative control on the SAME set."""
    _w1, _w2, prompt, dest, role, _domain = COMPOUNDS[compound_name]
    heads, segments = _ordered_with_tail(cand)
    if not heads:
        raise ValueError(f"no heads to ablate for '{compound_name}' — "
                         "Stage A earned an empty set and no tail")

    print(f"Stage B [{compound_name}]: cumulative ablation over {len(heads)} "
          f"heads ({segments.count('lexical')} lexical + "
          f"{segments.count('structural_tail')} tail)")
    curve = cumulative_ablation(model, prompt, heads, dest, segments=segments)
    curve.insert(0, "compound", compound_name)
    curve["role"] = role
    frames = [curve]

    if role == "primary":
        nw1, nw2, nprompt, ndest = NEG_CONTROL
        print(f"  negative control: same set on '{nprompt}' at '{ndest}'")
        neg = cumulative_ablation(model, nprompt, heads, ndest,
                                  segments=segments)
        neg.insert(0, "compound", f"{nw1}_{nw2}")
        neg["role"] = "neg_control"
        frames.append(neg)

    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- #
# Ledger persistence (replace-by-compound semantics; reruns don't duplicate)   #
# --------------------------------------------------------------------------- #
def _upsert(path, df, key_col="compound"):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = pd.read_csv(path)
        old = old[~old[key_col].isin(df[key_col].unique())]
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(path, index=False)
    return path


# --------------------------------------------------------------------------- #
# Session sanity (spec §Testing) — run once before the first real ablation     #
# --------------------------------------------------------------------------- #
SR_PROMPT = COMPOUNDS["screen_reader"][2]


def sanity_check(model):
    """Three in-notebook asserts from the spec. Loud on pass, fatal on fail."""
    # 1. Empty set => identity => KL == 0 (hook machinery adds nothing).
    r0 = ablate_heads_at_position(model, SR_PROMPT, [], "reader")
    assert r0["kl_base_to_ablated"] == 0.0, \
        f"empty-set ablation should be identity; got KL={r0['kl_base_to_ablated']}"

    # 2. Plural [(29,7)] reproduces the singular (regression on the refactor).
    rs = ablate_head_at_position(model, SR_PROMPT, 29, 7, "reader")
    rp = ablate_heads_at_position(model, SR_PROMPT, [(29, 7)], "reader")
    assert abs(rs["kl_base_to_ablated"] - rp["kl_base_to_ablated"]) < 1e-4, \
        f"singular {rs['kl_base_to_ablated']} vs plural {rp['kl_base_to_ablated']}"

    # 3. A large late-layer set => KL > 0 (the instrument is not silently inert).
    late = model.cfg.n_layers - 2
    big = [(late, h) for h in range(min(8, model.cfg.n_heads))]
    r3 = ablate_heads_at_position(model, SR_PROMPT, big, "reader")
    assert r3["kl_base_to_ablated"] > 0.0, \
        "late-layer joint ablation moved nothing — positive control failed"

    print(f"sanity_check PASSED — identity KL 0.0; L29/H7 singular==plural "
          f"({rs['kl_base_to_ablated']}); late-layer set (L{late}, 8 heads) "
          f"KL={r3['kl_base_to_ablated']}")


# --------------------------------------------------------------------------- #
# Orchestrator — one compound per visit                                        #
# --------------------------------------------------------------------------- #
def run_d6(model, project_root, compound_name,
           min_layer=MIN_LAYER, n_candidates=N_CANDIDATES):
    """Stage A + Stage B for one compound; upserts both ledgers; prints the
    verdict-relevant summary (peak lexical KL vs peak tail KL)."""
    if compound_name not in COMPOUNDS:
        raise ValueError(f"unknown compound '{compound_name}'; "
                         f"choose from {list(COMPOUNDS)}")
    root = Path(project_root)

    cand = earn_candidate_set(model, root, compound_name,
                              min_layer=min_layer, n_candidates=n_candidates)
    cand_path = _upsert(root / "results/pythia" /
                        f"{MODEL_NAME}-candidate-heads.csv", cand)
    print(f"  Stage A table → {cand_path}")

    curves = run_joint_ablation(model, cand, compound_name)
    curve_path = _upsert(root / "results/pythia" /
                         f"{MODEL_NAME}-multihead-ablation.csv", curves)
    print(f"  Stage B curves → {curve_path}")

    own = curves[curves["compound"] == compound_name]
    lex = own[own["segment"] == "lexical"]["kl"]
    tail = own[own["segment"] == "structural_tail"]["kl"]
    print(f"\n[{compound_name}] peak KL — lexical set: "
          f"{lex.max() if len(lex) else float('nan')}"
          f" | with structural tail: {tail.max() if len(tail) else '(no tail)'}")
    print("Flat lexical segment + rising tail = distributed result "
          "+ working instrument, in one curve.")
    return curves
