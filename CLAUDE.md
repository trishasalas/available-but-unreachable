# CLAUDE.md — tmlr

Project context for Claude Code sessions in this repo. Read this before changing
anything.

## What this is

A mechanistic interpretability study for TMLR submission: the **declarative–evaluative
gap** in language models, using accessibility concepts as the test domain. Models
define a concept correctly and cannot apply it — and the paper asks what explains
that.

Cross-architecture: Pythia (6 scales), GPT-2 (4), OLMo-2 (3) = **13 models**.
Base checkpoints only, greedy decoding, TransformerLens 2.17.0 pinned.

Current framing — *"It's not attention and it's not frequency"*:

- **I. The gap exists** — fluent wrongness, entropy
- **II. It's not attention (or a circuit)** — binding; the three-tier architecture is
  statistically real and causally inert
- **III. It's not corpus frequency alone** — frequency is the floor, not the ceiling

Author is an accessibility specialist by profession. **Ground truth on accessibility
is hers, not yours.** Do not author or revise accessibility criteria, coding rules, or
evaluative items.

## Ground rules

**Show the diff before committing.** Always. Small, reviewable changesets.

**Do not use subagents.** Work in one session with a readable transcript. Summaries of
work are not work, and this repo has an active problem with things that report success
while being wrong.

**Surface anything written to project memory.** If you create or modify a file under
`~/.claude/projects/-Users-trishasalas-Repos-Research-tmlr/memory/`, say so in the
session and quote what you wrote. A record the user cannot see is not a record, it is
an assumption with a filename. Two memory entries were found on 2026-08-09 that were
sincerely written and materially wrong — one asserting TransformerLens falls back to
CPU on Apple Silicon (it does not; it warns and honors `mps`), one recording a
preference with the wrong reason attached. Both had been silently shaping sessions for
days.

**Do not create worktrees under `.claude/`.** A stale one shadowed the entire results
tree and cost an hour to diagnose. If isolation is genuinely needed, ask first.

**State on disk, never in wetware.** Any decision gets written down. See below.

**Scope: this repo by default.** Everything needed for work in this repo is under
`/Users/trishasalas/Repos/Research/tmlr/` or in the conda environment (below).

- **Default scope** is the repo. Start here and stay here unless there is a reason not
  to.
- **`/Users/trishasalas/Repos/Research/` is available** when the task genuinely spans
  projects — sibling repos are `how-models-think`, `blind-study`, `maybe-neurons`,
  `OlmoSpelunking`, `thatDangCircuit`. Say why before going there.
- **The home directory is a hard no.** Do not search, list, or read outside
  `~/Repos/Research/`. If something appears to be missing — an environment, a config, a
  file — **ask** rather than going looking for it. There is no `.venv`; see Environment
  below.

**Moving or archiving a file under `results/` is a decision, not tidying.** Results
files are cited by name in `docs/findings/CLAIMS.md`, and a claim whose evidence lives
only in an archive does not ship — that is CLAIMS' own gate. Before moving anything
under `results/`, check whether CLAIMS references it, and record what moved and why.
On 2026-08-09 the author could not reconstruct, one day later, why five files had been
archived; one was a NAILED claim's only evidence and a figure script had broken
silently. Default to leaving files where they are.

**If a task has a verifiable pass condition, run it and report the number.** If it does
not match, stop and report — do not adjust until it does.

**There is no test suite.** No `tests/`, no `test_*.py` anywhere outside `_Archive/`.
The pass conditions written into the task briefs are the regression harness, and they
run only when a human types them. Nothing in this repo fails on its own — which is why
the failure mode below is the shape it is. Treat a brief's pass conditions as the
tests for that change: run every one, report every number, and snapshot a baseline
before editing when the condition is "this should not move."

## The recurring failure mode — read this one

Every significant bug in this repo has the same shape: **a record that was true when
written, silently stopped being true, and nothing failed.**

Usually because the scope moved underneath correct code. Scope moved four times:
compounds 11 → 53, results layout flat → per-domain, suites two → three, batteries one
→ five domains.

Concrete instances currently open:

- `analysis.py` hardcodes `source = 'original'`, so a documented filter in
  `gap_analysis.py` has never filtered anything — and a DECISIONS entry from 2026-07-03
  states the rationale correctly and names `load_all_results` as the implementing
  function. The record, the code comment, and the code all disagreed for a month.
- `tokenization_comparison` hardcodes 11 compounds against a 53-compound battery
- The frequency pipeline writes fixed filenames inside a loop over suites
- One concept has three spellings across three batteries
- Two project-memory files were found sincerely written and materially wrong
- Five results files were archived with no recorded reason; the reason was
  unrecoverable a day later

**Therefore: when you change something, state what it depends on.** Not "this now
works" — "this works as long as X remains true." That sentence is the whole point. A
decision was recorded on 2026-07-03 that named the exact function implementing it; the
function never did, and nothing failed for a month.

Prefer making scope *visible* over documenting it: row counts, skip counts,
collision warnings at load time.

## Environment

**Conda, not venv.** There is no `.venv` anywhere — do not look for one.

- **Primary env:** `mechinterp`
  Interpreter: `/opt/homebrew/Caskroom/miniconda/base/envs/mechinterp/bin/python`
- **Secondary env:** `Research`
  Interpreter: `/opt/homebrew/Caskroom/miniconda/base/envs/Research/bin/python`
- Use the full interpreter path rather than relying on an activated shell.
- Run modules with `PYTHONPATH=.` from the repo root.

**TransformerLens is 2.18.** `DECISIONS.md` pins 2.17.0; that entry is stale. Results
were regenerated on Colab under 2.18. The drift is undocumented and is an open item in
`docs/audit-response-plan.md` — do not "fix" it by downgrading without asking.

**MPS works.** TransformerLens emits `utils.warn_if_mps()` on Apple Silicon but honors
`device="mps"`. Verified: `next(model.parameters()).device` returns `mps:0`. A project
memory file claiming a CPU fallback was wrong and has been removed. Do not add device
workarounds.

**Frequency work needs no GPU.** No models load; the infini-gram queries are the slow
part, roughly an hour for two suites. That is expected, not a hang.

## Layout

```
data/            *.yaml prompt batteries (key: prompts) — accessibility, control,
                 medical, legal, finance
data/binding/    *.yaml compound batteries (key: compounds) — 227 compounds
                 ⚠ DIFFERENT ARTIFACT from data/*.yaml. Do not conflate or delete.
src/             analysis modules (see below)
results/         {elicitation,entropy,binding,frequency,analysis,logits,mlp,adhoc}/
notebooks/       experiment notebooks
paper/           manuscript + generate-figures/
docs/            decisions/, preregistrations/, findings/, claude-science/
_Archive/        {_notebooks,_results,_src,_docs} — tracked, do not run from
```

### `src/` orientation

- `analysis.py` — **the loader everything reads.** `load_all_results` returns
  elicitation / entropy / binding frames. Currently the highest-risk file in the repo.
- `gap_analysis.py` — applies accuracy coding, produces the gap tables
- `accuracy_coding.py` — **any change here requires a DECISIONS entry.** The coding
  rules determine what counts as correct; changing one retroactively changes every
  table and figure.
- `elicitation.py`, `entropy.py`, `binding.py`, `frequency.py` — battery runners
- `manifest.py` — expected == written == actual. This layer audits clean; keep it that
  way.
- `logit_lens.py`, `logit_export.py`, `decompose.py`, `qk_ov.py`,
  `head_characterization.py`, `heads.py`, `probe.py` — mechanistic tooling
- `d6_multihead_ablation.py`, `d7_token_ban.py`, `d8_frequency_prior.py` — registered
  experiments. **Keep**, do not tidy as dead code.
- `dual_spearman.py`, `closeout_followups.py`, `tangent_byte_compare.py` — **keep**
- `tl217_olmo2_adapter.py`, `olmo_config.py` — OLMo-2 support for pinned TL

## Traps

**`closed captions`, not `captions`.** Renamed in `ca01b59` (2026-08-05, "rearrange
results directory structure") — the same commit that moved the results layout, which is
also what stranded the paper's frequency numbers. Using the old form silently yields
nine concepts instead of ten, with no error.

*(Corrected 2026-08-09: this note originally cited `7f84365`, taken from the audit and
not verified. That commit is "add missing compounds + make suite iteration dynamic" —
it widened `COMPOUNDS` from 49 to 53 and replaced `dual_spearman`'s hardcoded
`['pythia', 'gpt2']` with `tab['suite'].unique()`. Verified with `git log -S` on
`data/accessibility.yaml` in both directions. A record naming a commit that does
something else, in the file documenting that failure mode.)*

**Three spellings of one concept exist:** `closed_captions` (frequency),
`closed captions` (declarative), `captions` (completion). Canonical form is lowercase
with underscores. Normalization belongs at load time, in one place.

**`_extract_scale`'s OLMo path is correct despite looking wrong.** `'olmo'` ends in
`'m'`, `float('olm')` raises, the loop continues to the right part. Audit-verified.
Do not "fix" it.

**`pythia-12b` is the one name for that checkpoint.** The binding battery used to call
it `pythia-13b` and `_extract_scale` carried an alias. Decision 0014 was ruled and
executed 2026-08-10: binding outputs renamed (directory, filenames, and the `model`
column in all five CSVs), alias removed. A stray `pythia-13b` now parses as 13B and
splits from `pythia-12b` in every groupby, which is the intended loud failure. **The
run-time name is typed by hand** in `notebooks/binding-pythia.ipynb` cell 8
(`model_name = "..."`) — a rerun that types `pythia-13b` re-creates the split.

**`gpt2` and `gpt2-small` are both on disk and both map to 124M.** Nothing dedupes;
rows are double-counted in any groupby over scale.

**Infini-gram returns `-1` as a failure sentinel.** It must not reach a correlation as
if it were a count.

**Do not open CSVs in a spreadsheet editor.** SpreadJS rewrites the whole file on save
— quoting, CRLF, phantom trailing columns.

**Beware `do_sample`.** A prior `do_sample=True` defect invalidated an entire
elicitation run. All experiments are greedy, `temperature=0`, `do_sample=False`.

## Conventions

**`DECISIONS.md`** (repo root) — the historical ledger through D8. Entries are cited by
number from CLAIMS.md. Do not renumber, do not backfill.

**`docs/decisions/`** — new decisions, ADR format, one file per decision,
`NNNN-slug.md`. Immutable once accepted; supersede rather than edit. Every entry has a
**Depends on** line. See that directory's README.

**`docs/preregistrations/`** — `NNNN-slug.md`. Committed to git **before any results
are seen**; timestamps are the evidence. Predictions, thresholds, and interpretation
branches frozen in advance. All branches ship, including the null. Never edit a prereg
after a run.

**`docs/findings/CLAIMS.md`** — claim ledger. A claim whose evidence lives only in an
archive does not ship. Check this before moving any results file. Note that some
decisions are recorded *only* here rather than in DECISIONS.md — the trajectory
taxonomy demotion (B3, 2026-07-06: descriptive vocabulary, not an empirical
contribution, per a stability audit showing 20/102 class assignments survive a
one-level coding perturbation) is an example. If a methodological question seems
undocumented, search CLAIMS before concluding it is.

## Current state (2026-08-09)

Responding to a repo audit — `docs/claude-science/tmlr_audit_2026-08-09.md`, 22
findings. The working plan with the ordered steps and their dependencies is
`docs/audit-response-plan.md`. Paper prose is deliberately out of scope; it is being
rewritten under the new framing.

**The data layer verifies clean** — 227/227 compounds round-trip, all 65 binding CSVs
match schema, manifests reconcile everywhere. What broke is the analysis layer above
it. Do not go looking for problems in the batteries.

Six decisions are `proposed` and unruled (`docs/decisions/0010`–`0015`). Several block
the next pipeline run. Do not regenerate anything that depends on an unruled decision.

**Open and unwritten:** the frequency correlation estimand changed from trajectory
ordinal to mean accuracy (see `docs/frequency-refactor.md`, the task brief that
implemented it). That change is downstream of the B3 taxonomy demotion but is not the
same decision, and it has no ADR. The author wants to discuss it before it is written
up — do not draft it unprompted.
