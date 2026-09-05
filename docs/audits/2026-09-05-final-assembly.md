# Final assembly and verification — 2026-09-05

## Canonical manuscript

`paper/sections/` is the only active prose source. `paper/build-paper.sh` renders the main sections, then the bibliography, then `10-appendix.md`. The former preview builder delegates to that build. Historical review Markdown is not an input. Generated alternate main sections and the obsolete review PDF were retired to local temporary backups.

The main-section integration comparison passed: all ten existing main/reference sections retained their prose, allowing only the approved table removals, one table caption, and table-reference substitutions. Fable's restored metaphors remain. The author subsequently approved the Conclusion and first-page disclosure, the authorship clarification in that disclosure, and the appendix's eighth-token counting correction. Abstract and Limitations were not edited in this pass. The existing title and deliberate three-part Results numbering are retained.

The disclosure is voluntary: the author-supplied current TMLR LLM policy permits assistance and assigns responsibility, without prescribing a disclosure footnote. Earlier TODO wording calling it required was unsupported. The author approved keeping a title-linked first-page footnote.

## Verification performed

- Canonical PDF: 20 pages, including references on 13–14 and appendix on 15–20. Every page was visually inspected; first page and appendix pages 17 and 19 were rechecked after final local changes. No final LaTeX warnings, overflow, or unresolved references. One main table and eight appendix tables have formal captions and distinct hyperlink targets.
- All 23 cited keys match the 23 printed references. Author metadata is blank. Personal names occur only in scholarly references; the personal-domain URL is the cited earlier blog post, not a named version of this manuscript.
- All three relocated pooled tables preserve every cell. Pooled gap arithmetic matches the saved family CSVs. The paired summaries reproduce 96 confirmatory cells, 35 correct definitions, zero pair passes, 85/7/4 item breakdown, and one separate pilot pass.
- Raw-binding Spearman correlations reproduce at sample sizes 196/294/147: −.059/−.126/.108 (GPT-2/Pythia/OLMo). GPT-2 saturation at .99 is 192/196, rounding to 98%.
- Declarative-frequency Spearman correlations recomputed from 147 saved compound rows reproduce .5875/.5194/.5823; each family has 49 compounds and p<.001. Declarative token-count partial correlations remain explicitly separate from binding measurement validity.
- All 26 primary binding correlations and 52 bootstrap endpoints in appendix A3 match the canonical condition tables. Both shared-label aggregate probabilities match the archived extreme counts and one-count correction.
- The registered ablation checker reproduces the frozen split, selected heads, all random sets, control gates, statistics and all eleven original artifact hashes. No model inference or new sensitivity analysis ran.
- The six OLMo-only 7B emergence entries match the saved threshold table. The six older bias-frequency correlations reproduce .664/.737/.767/.722/.689/.779 by joining the 500-token count cache to saved bias vectors. Whitespace-normalized shortcut/forward comparisons first diverge at zero-indexed steps 2–7; the approved appendix correction reports the eighth generated token.
- The current claims ledger supersedes historical active markers while retaining old IDs and evidence pointers. No original result or preregistration was changed.

## Anonymous supplement

The reproducible package builder is `scripts/build-anonymous-supplement.py`. The ZIP contains 494 files (55.34 MB), under the 100 MB limit stated at https://jmlr.org/tmlr/author-guide.html. It includes the exact prompt inventory, raw and summarized evidence, scientific code, anonymous notebook derivatives, measurement-validation evidence copies, and provenance records. All archived measurement-validation originals remain intact; copied bytes and hashes agree.

Checksums verify every packaged file; ZIP integrity passes. Personal identity strings and home paths are absent under the recorded scanner. Notebook outputs and metadata are cleared, personal clone/setup cells are replaced with local unpacked-directory setup, and publishing cells are omitted. CSV evidence is unchanged. The package contains no manuscript source metadata or Git history.

Smoke test from an independently extracted ZIP: all five data-driven figure generators run successfully. Paired collapse, raw binding, and binding-frequency forest reproduce pixel-identically; the pooled gap and frequency-floor figures reproduce the same plotted results with small typography/layout differences. Figure 1 remains the author's approved illustrative raster; its source completions and corpus counts are preserved rather than replacing it with a different design.

Limits: inference notebooks were not executed on models. Clearing and anonymizing the registered notebook changes its bytes, so its original historical notebook hash cannot be reproduced from the anonymous derivative. The historical checker remains unchanged. A separately named anonymous checker verifies ten unchanged original hashes plus the anonymous notebook hash, explicitly reports that exception, then reproduces the selection, controls and statistical tests. The package records original and packaged hashes. Full vocabulary distributions were not saved, so the original KL values cannot be reconstructed from CSVs alone. These are disclosed provenance limits, not a failed inference rerun.

## Author submission actions

The local manuscript/package preparation is separate from actually submitting. OpenReview profile, affiliations/conflicts, funding, competing-interest and human-subject reporting fields require author completion. No upload or submission was performed. Use the canonical PDF and anonymous ZIP, not historical review files.
