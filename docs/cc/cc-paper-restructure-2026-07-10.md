# CC Handoff: Paper Directory Restructure — Reconciliation

**Date:** 2026-07-10 (updated same day)
**Prepared by:** Fable (claude.ai) with Trisha
**Status:** Trisha has ALREADY PERFORMED the file moves manually (VS Code
explorer, i.e. filesystem moves, not `git mv`). CC's job is reconciliation
and fallout, not moving files.
**Scope:** Verify reality against the target tree, chase broken references,
stage correctly, one commit. Zero prose changes.

## CC task list

1. **Enumerate the delta.** `git status` shows everything that moved (as
   deletes + untracked adds, since moves were done outside git).
2. **Reconcile against the target tree below.** If reality diverges from the
   target, FLAG it to Trisha — do not "correct" her placement decisions.
3. **Stage deletes and adds together** so git's rename detection pairs them.
   Before committing, confirm renames were detected (staged status shows
   `renamed:` entries, or check `git diff --cached -M --summary`). File
   history must stay continuous — not twelve deaths and twelve strangers.
4. **Chase the fallout** (Path updates section below).
5. **Apply .gitignore additions**, untrack `build-debug/` if tracked.
6. **Run the verification gate.**
7. **One commit.**

## Target tree (Trisha's intent — reality should match this)

```
paper/
├── README.md
├── build-paper.sh
├── build/
│   ├── header.tex
│   ├── template.tex
│   ├── metadata.yaml
│   └── filters/
│       ├── caption-style.lua
│       └── figure-alt.lua
├── build-debug/          (gitignored)
├── figures/
│   ├── binding-vs-accuracy.png
│   ├── completion-paradox.png
│   ├── concept-trajectories.png
│   └── gap-behavioral-internal.png
├── generate-figures/
│   ├── generate-fig-binding-vs-accuracy.py
│   ├── generate-fig-completion-paradox.py
│   ├── generate-fig-concept-trajectories.py
│   └── generate-fig-gap-behavioral-internal.py
└── sections/
    ├── 01-introduction.md … 11-colophon.md   (12 files, moved AS-IS)
```

Section filenames stay AS-IS including `06a-measurement-pathways.md`. The
skeleton renumbering is a separate future commit. Do not renumber here.

## Ratified rulings (Trisha, 2026-07-10)

- `paper/figures/_bk/` (three perplexity figures): **delete.** If Trisha
  already deleted it, verify it's gone from the index too.
- `build-debug/`: **gitignore.** If currently tracked, that was accidental —
  `git rm -r --cached paper/build-debug/` (keep local files).
- Root `figures/L1H12-induction-test.png`: audit-then-delete. Suspected
  exploratory artifact of `notebooks/induction-head-test.ipynb`, no generator
  script. If unreferenced and reproducible: delete, and remove the then-empty
  root `figures/` directory. (If Trisha already handled this, just verify.)
- Generator scripts: confirm all four map 1:1 to the four PNGs in
  `paper/figures/`. Flag anything that doesn't.

## Path updates required (CC's real work)

- `paper/build-paper.sh` — sections path (`sections/contents/` → `sections/`),
  template/header/metadata/filters paths (→ `build/`), output paths.
- All four `generate-fig-*.py` — figure output paths must resolve to
  `paper/figures/` from the new location; input paths into `results/` must
  still resolve.
- `paper/README.md` — update layout descriptions.
- `paper/build/metadata.yaml` and `template.tex` — check relative references
  to filters/resources that assume the old layout.

## .gitignore additions

```
paper/build-debug/
paper/**/*.aux
paper/**/*.log
paper/**/*.fls
paper/**/*.fdb_latexmk
.DS_Store
```

## Verification gate (path integrity, not output identity)

1. **Stale-reference sweep:** repo-wide grep for `sections/contents`,
   root-relative `generate-figures` references, `_bk`, and
   `L1H12-induction-test`. Must come back empty (excluding this doc and git
   history).
2. **Conditional smoke test:** run `build-paper.sh` after path updates.
   Green exit = pass. If it fails for a reason that predates the restructure,
   note it in the commit message and stop — fixing the build is a second
   reason to change and belongs in a different commit.
3. Every path in "Path updates required" checked as resolving.

## Commit discipline

One commit. Message states: structural relocation (moves performed manually
by author, rename detection verified), path updates, gitignore additions;
no prose changes; sweep + smoke test results cited.

## Out of scope

- Section renumbering / skeleton rebuild
- Any prose edits
- Fixing a pre-existing build breakage
- `results/` reorganization
