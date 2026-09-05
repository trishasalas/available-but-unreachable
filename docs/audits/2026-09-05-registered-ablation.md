# Registered Pythia-2.8B ablation: saved-artifact audit

Date: 2026-09-05. Result commit: `38e07f5`.
Scope: preregistration 0003 section 12 and the 2026-09-04 controls amendment.
Status: saved-artifact, selection, statistical, and code-path checks pass. Model inference was not rerun.

## Checks

- All 11 SHA-256 entries in the contemporaneous ablation manifest match current files. This includes the producing notebook, intervention helper, amendment, split, candidate table, five output CSVs, and upstream model manifest.
- The split reproduces exactly from sorted compound names and NumPy seed 20260813: first 25 selection, remaining 24 held out, with no overlap. Primary output order matches the held-out order.
- Recomputed selection correlations from the raw natural-condition value-weighted binding data, restricted to the 25 selection compounds and layers 22–31, recover L28/H5, L30/H6, L28/H13, L22/H25, L30/H11 in that order (zero-based indices).
- All 100 random sets match the first 100 seeded draws from 315 eligible heads. Each contains five distinct late-layer heads and excludes selected heads. No duplicate sets occurred, so the notebook’s duplicate-set rejection did not change the draws.
- All 2,400 random compound/set rows are present and unique. Head identities and frequencies match their frozen sources. Every saved KL is finite.
- The empty control has maximum absolute KL 0, passing the 1e-8 threshold. All 24 positive-control KLs exceed 1e-6; maximum 0.0018376098014414, median 0.0001181839907076.
- All 100 random-set correlation, mean-KL, median-KL, and top-change summaries reproduce. The selected-set aggregate summaries reproduce.
- The selected frequency–KL correlation is 0.03652173913043478. Exactly 5,626 of 10,000 seeded permutations are at least as negative, giving (5626+1)/10001 = 0.5626437356264373.
- All 100 random correlations are finite; 24 are at least as negative as the selected result. The empirical one-sided tail is (24+1)/101 = 0.24752475247524752.
- Selected-set mean KL is 0.0000212664344872, median 0.0000162282740348, range 0.00000244832335738–0.000102933961898. No selected-set or positive-control top tokens change; all 2,400 random-control top-change flags are also false. Primary top-change flags agree with saved top-token lists.
- All 24 held-out YAML prompts and later-constituent indices match the saved natural-condition binding artifacts, using the current `find_token_index` implementation.

## Producing code and chronology

The notebook saves the head sets before intervention, evaluates the primary and gate controls, checks both gates before random runs, then saves statistics and invokes the manifest writer. The helper zeros `hook_z` at the later constituent’s last subtoken and computes KL(base || ablated) from float32 log-softmax distributions at the final prompt position, without CSV rounding of KL.

The split and candidate tables were committed on September 2 (`86a53d7`). The controls amendment was committed at September 5 00:04:48 UTC (`ca4e014`), followed by the saved-split-label fix at 00:34:49 (`ead4e0b`). Manifest creation is recorded at 00:41:37; results were committed at 00:41:57 (`38e07f5`). These records support the documented order; Git timestamps are not an independent execution log.

## Boundaries and manuscript action

This audit recomputes statistics from saved KL values; full-vocabulary baseline/ablated distributions were not saved, so KL itself was checked by inspecting the producing code rather than independently recomputing from logits. The model revision is not explicitly pinned in the ablation loading cell. Retain that provenance limitation in the reproducibility inventory rather than inventing an exact revision. The manifest explicitly records a dirty working tree, while its listed artifact and code hashes match.

The registered prediction of greater perturbation for rarer compounds was not supported under this five-head, single-position intervention. This does not establish equivalence to zero effect, causal irrelevance of all binding, or unchanged application accuracy. Earlier six-scale exploratory ablation files remain in place but their numerical results are excluded from the manuscript, as agreed with the author.

Author approved the methods, results, discussion, and appendix wording on 2026-09-05; these changes are applied, including removal of the stale statement that the registered causal test was not completed. Detailed appendix expansion and inclusion in the PDF remain pending.

Reproducible numerical audit: `docs/audits/2026-09-05-registered-ablation-check.py`, run from the repository root in the mechinterp environment. The separate prompt/token-index check and code/chronology inspection are documented above.
