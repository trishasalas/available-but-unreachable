# Task brief — fix `src/analysis.py`

> Paste this into Claude Code as the task. Written 2026-08-09.  
> Full context: `docs/audit-response-plan.md` step 1; decisions  
> `docs/decisions/0010-source-flag-expansion-compounds.md` and  
> `docs/decisions/0015-concept-key-normalization.md`.

> **Superseded 2026-08-10.** The alias was retired under decision 0014.
> This brief is a historical record; do not follow its guidance.

---

## Read first

Before changing anything, read these. They contain the reasoning, not just the  
instruction, and the reasoning is the part that matters:

- `docs/decisions/0010-source-flag-expansion-compounds.md`
- `docs/decisions/0015-concept-key-normalization.md`
- `src/analysis.py` (the file being changed)
- `src/gap_analysis.py` lines 60–90 (the consumer of the `source` column)
- `data/accessibility.yaml` (the source of truth for the concept split)

## Why this task exists

An audit found that a documented exclusion has never been enforced.  
`gap_analysis.py:76-78` filters `source == 'original'` to keep 41 frequency-stratified  
expansion compounds out of the declarative/evaluative paradigm means.  
`analysis.py:66` hardcodes `df['source'] = 'original'` on every loaded row, so the  
filter has never removed anything. Elicitation CSVs have no `source` column at all.

The consequence: declarative pivots are computed over 51 concepts, and the headline  
gap compares a 51-concept declarative mean against a 5-concept evaluative mean. The  
error is large enough to produce an impossible negative gap at Pythia-6.9B.

This was not an undocumented decision. `DECISIONS.md` ("Gap-table sampling-frame  
partition", 2026-07-03) records the rationale correctly and names `load_all_results`  
as the implementing function. The record and the implementation diverged silently.

## Pass condition — verify before reporting done

After the change, re-derive the gap tables and check:

```
pythia-160M declarative == 0.5
```

Reference artifact: `_Archive/_results/pythia_gap_PRE_EXPANSION_REFERENCE.csv`, a  
pre-expansion gap table preserved from a stale git worktree. Current (wrong) value is  
`0.7059`.

Do not report the task complete without running this check and stating the number you  
got. If it does not come back 0.5, stop and report rather than adjusting until it  
does.

---

## Change 1 — Derive `source` instead of hardcoding it

In `load_all_results`, replace the unguarded `df['source'] = 'original'` with a value  
derived from concept membership.

The ten original concepts, from `data/accessibility.yaml` under the section comment  
"DECLARATIVE — Original Paper 1 Experiment 1 prompts":

```
screen reader
WCAG
skip link
alt text
ARIA
focus indicator
keyboard navigation
color contrast
semantic HTML
closed captions
```

**Trap — read this twice.** The tenth concept is `closed captions`, **not**  
`captions`. It was renamed in commit `7f84365`. Using `captions` silently yields nine  
concepts and a wrong gap table with no error. Verify the ten strings against  
`data/accessibility.yaml` rather than trusting this list.

Everything not in the set is `'expansion'`.

Implementation notes:

- Define the set as a module-level frozenset with a comment marking it **interim** and  
pointing at decision 0010 (the durable fix is a `source:` field in the YAML, deferred  
to the frequency regeneration).
- Apply normalization (change 2) before membership testing.
- Guard the assignment the way the adjacent `domain` line is guarded: if a loaded CSV  
already has a real `source` column, do not overwrite it. The unguarded write is the  
original defect and should not be reproduced in the fix.
- Emit a count at load: how many rows resolved to `original` vs `expansion`. A silent  
`{'original': N}` is what hid this for a month.

## Change 2 — Normalize concept keys at load time

One function, applied to every frame in `load_all_results`. Canonical form:  
lowercase, underscores (`closed_captions`), matching the frequency battery and file  
naming.

Three spellings of one concept currently exist:

| Battery     | Key               |
| ----------- | ----------------- |
| Frequency   | `closed_captions` |
| Declarative | `closed captions` |
| Completion  | `captions`        |

This is the root cause of a broken join elsewhere in the codebase — only `alt text`  
currently survives the completion/declarative concept join. Normalize in exactly one  
place, name it obviously, and make it idempotent.

`captions` → `closed_captions` is a genuine alias and needs an explicit mapping, not  
just whitespace handling.

## Change 3 — Fix the gpt2 double-count

`_extract_scale` maps both `'gpt2'` and `'gpt2-small'` to `124_000_000`, and both  
directories exist on disk. Nothing dedupes, so every gpt2-small row is counted twice  
in any groupby over scale — and if the two directories hold pre- and post-rerun data,  
old and new are being averaged together.

Detect and handle the collision. Report which directories collided and how many rows  
were affected rather than silently resolving it.

## Change 4 — Make silent skips visible

`_extract_domain` strips `model_name + '-'` from the CSV stem; anything not in  
`KNOWN_DOMAINS` is `continue`d with no warning. A file in a directory whose name does  
not prefix it vanishes without trace — the load printout reports rows loaded, never  
rows skipped.

Add to the existing printout: files skipped, with paths, and the domain string that  
failed the membership test.

---

## Constraints

- **Do not change** `_extract_scale`'s OLMo handling. It is correct and subtle:  
`'olmo'` ends in `'m'`, `float('olm')` raises, the loop continues to the right part.  
Audit-verified.
- **Do not change** the `pythia-13b` alias yet. It is the subject of decision 0014 and  
is being handled separately.
- **Do not refactor** `tokenization_comparison`. It is stale (hardcodes 11 compounds  
against a 53-compound battery) but is not on the critical path and is a separate  
task.
- **Do not touch** anything in `results/` or `_Archive/`.
- Keep the diff small enough to review by eye. Four changes, one file.

## When done

Report:

1. The diff.
2. The pythia-160M declarative value you got.
3. The original/expansion row counts.
4. Any files the new skip counter revealed, and any directory collision it found.

Items 3 and 4 are not decoration — they are the first time this pipeline has reported  
its own scope, and the numbers may be surprising.
