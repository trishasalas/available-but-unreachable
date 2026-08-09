# TODO

Here's the plan. Ordered so each step unblocks the next, and nothing gets undone by a later rerun.

**0 — Snapshot.** `git stash push -m "pre-audit snapshot"`, then `git status` and read it yourself. Ten minutes, and it makes everything after it reversible.

**1 — Stop the bleeding.** `git checkout --` the two clobbered frequency files. Then find A12's three mangled CSVs and do the same. One command each.

**2 — Answer the one question that shapes everything.** Grep an elicitation CSV header for `source`. If it's there, the A6 fix is deleting one line in `analysis.py`. If it isn't, you need a compound→source map. Don't write anything until you know which.

**3 — Loader repairs, all in `analysis.py`.** The source line. The gpt2/gpt2-small double-count. A skip counter so silent drops become visible. That's one sitting, and it's the file everything downstream reads.

**4 — Re-derive the gap tables, paired.** Declarative restricted to the 5 concepts with evaluative counterparts. This is where you find out if 6.9B behaves — and you already told me it will.

**5 — Pre-rerun decisions.** The OLMo x-corpus (A4), the archived-tables question (A11), the pythia-13b/12b rename (A15). Decide before regenerating, because the next run entrenches whatever you don't decide.

**6 — Frequency pipeline.** Per-suite filenames, corpus column, the A18 sentinel and `is not None` fixes. Then regenerate once, cleanly.

**7 — The join.** `closed captions` vs `closed_captions` — check whether the underscore/space split is what's actually breaking A3, then see what the paradox does with all four concepts.

Steps 0–4 are the ones that get you a gap table you trust. That's the emotional milestone, not the technical one, and it's genuinely reachable in a day.

Everything else — CLAIMS, DECISIONS, dead `src/` modules, dangling pointers, p-value formatting — is after. None of it blocks the science.

Want this as a markdown file you can check off, or is having said it out loud enough?