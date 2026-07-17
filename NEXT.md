# NEXT.md — Open work queue

Session-to-session work items: what's on deck, not what's true (CLAIMS.md is the ledger; DECISIONS.md is the record). Ordered by phase, and by importance within each block. Items leave this list by being done and committed, with a pointer to the commit; "Closed this cycle" at the bottom holds them until the next sweep.

**Pointers, not tasks:** the full TMLR readiness plan (tracks, sequence, format facts) is `docs/tmlr-readiness-plan-2026-07-12.md`; editing-pass status of record is the ledger in `paper/sections/_rebuild/_REBUILD_NOTES.md`.

**TARGET: SUBMIT SUNDAY 2026-07-19** (set 2026-07-15). The gates outrank the date — a real finding at number-audit or Gemini's pass moves the date, never ships past it. The convergence rule bounds all remaining work.

---

## 1 · Rulings waiting on Trisha — cheap, and they unblock everything below

- [ ] **§8 structural-dedup flags (2),** carried out of the 07/08/09 pass into 08's per-file header: ¶3 overlaps §7's frequency-positioning (one-sentence version proposed); ¶4's retraction recap ~200 words re-narrates §6 (keep only the b_U echo?). Do not insert without Trisha; execute at pass 3. (Plan, Track 2 item 12.)

## 2 · Paper passes, in sequence (status of record: the ledger)

- [ ] **Pass 3 — structure & formalization** (UNLOCKED — ruling ratified 2026-07-15, amended, post-veto reserved; Fable drafts, Trisha ratifies per section). Three parts, **no setup block**: (1) per-section **Setup.**/Results delineation §§2–6, with §2's Setup enlarged to declare the shared environment (suites, battery, two cuts, frequency measurement) and closing with the two-sentence gate-protocol statement; (2) six-formula inventory (§6 folding/severance equation highest priority, written from the D8 registration's math — exact, two severed terms); (3) Reproducibility Statement near the end (pins, seeds, repo/decision-log pointers — doubles as the pass-4 destination). §6 rider ratified: lead-with-mechanism reorder (pathway definition + equation first, retraction as its case study); the three Gemini rejects stand. Precedent: Paper 1's declare-at-use + appendix convention. Post-veto: if the drafted execution reads bolted-on or wrong in practice, the ruling reopens without prejudice.
- [ ] **Blind-study record placement — RULED (Trisha, 2026-07-15): appendix + repo.** Appendix A.3 gets the T4 epitaph with the structural distinction (analysts-didn't-find vs corpus-couldn't-afford; seal branch b30eaba; s1's 1-via-ambiguity as evidence for the latter) and the 0/7/9 meta-finding. **A.3 must also state the session count and the per-claim aggregation rule** (intro reports claims not sessions, by ruling 2026-07-15 — the count lives at the record, not the intro). Repo record keeps the 7/7 peak_regress reconstruction and T5 both readings + operator adjudication (sources: runs/study2/SCORING.md, NOTES.md, SCORER_BIAS_STATEMENT.md). Blog post someday — personal, not paper. Execute with the pass-3/4 appendix work; 10-appendix wiring into build-paper.sh lands at promotion regardless.
- [ ] **Staging seam (opened 2026-07-15; protocol RATIFIED 2026-07-16).** Trisha's whole-paper editing copy lives in the Obsidian vault: `~/Repos/obsidian-vault/20 Research/TMLR/paper/Concept Emergence in Language Models…`. Vault is sovereign for her edits. **Edit-session protocol (Trisha's commitment, closes the tell-the-scribe weak link): edits happen in live sessions with Fable, scribed one at a time** — no batch edits carried on memory. Ported so far: intro blind-study ¶ ("sessions," "registered," no n); intro closing ¶ ("the one exhibit… documented alongside the others" — ratified 2026-07-16; note: "the one" = uniqueness claim, re-verify if any gate surfaces a second failure). Both pending port to _rebuild/01 at pass-3/promotion touch. RECONCILE vault → `_rebuild/` per section before pass-3 drafting touches that section; full reconciliation is a promotion gate.
- [ ] **Figures (Track 3) — Fig 1 RULED 2026-07-16 (Trisha): frequency-emergence scatter, SOLO lead figure.** Log bigram frequency × emergence outcome, n=49, ρ annotated, exemplar points NAMED (alt text mandatory among them; captions, ARIA as fits). Caption carries the thesis sentence — abstract + Fig 1 must tell the whole story alone (Nanda standard). Three-panel composite considered and REJECTED (busy; figure-shaped setup block — same fix as the structure ruling: evidence lives at point of use). Gap series stays §2's figure; D8/b_U stays §6's, with correlation-not-circuitry constraint on §6's caption. **Fig 2 RULED 2026-07-15: per-concept matched pairs** (alt text + captions shown individually; aggregate-only rejected — would resurrect the rescoped claim and launder n=8). **A.4 replication table RULED in**: Paper-1 replication numbers behind §3's opening sentence; assembly from drafted wording in DECISIONS 2026-06-21. Alt text for every figure; A.1 table at number-audit.
- [ ] **thatDangCircuit → public + Zenodo DOI (CC; ordered 2026-07-15).** G5(b) remedy; resolves §3's "DOI pending" — submission blocker. GitHub integration, CITATION.cff with ORCID, toggle before v1.0.0. Must not de-anonymize the submission (Track 6: cite third-party-style or cover via mirror).
- [ ] **Pass 4 — src/artifact.** Sweep CSV filenames, script paths, and decision-log pointers from body text to the appendix + Reproducibility Statement convention; key code excerpts (coding-criteria, ablation hook) land in the appendix. All sections at once, per ruling.
- [ ] **Pass 5 — citation.** Working shelf → BibTeX + tmlr.bst (natbib \citep/\citet); resolve 10-references TODOs (Kobayashi ACL pages, Gao ICLR venue/year, Puccetti verify-before-add, Fuglerud/López-Gil metadata, arXiv volume/pages/DOIs); attach §7's probing citation (still open); shelf ↔ in-text audit both directions.
- [ ] **Promotion mechanics.** git mv renumber + fix build-paper.sh SECTION_FILES (pre-existing breakage; add 10-appendix); metadata.yaml abstract → 00-abstract (G1 debt); voice pass on 00/01.
- [ ] **Gates (not passes).** CC number-audit at promotion (category-(b) carried numbers, "approximately 1%" companion figure, captions/"closed captions" mapping at figure-gen, Fig 2 per-concept composition, A.1 per-head table population). Anonymization pass at submission (repo links → anonymous mirror, colophon stripped, third-person Salas 2026 audit).

## 3 · Verification & data hygiene

- [ ] **Verify carried items 1–3, 5 against keys/CSVs** before any enters text: emergence "never" inflation; fluent_wrongness bucket 9/170; summary-table nulls; WCAG 2.2 confound — cite s1 TRANSCRIPT for the last, not FINDINGS.
- [ ] **Data-dictionary fixes:** ban_applied semantics (3/3 analysts failed to recover it), degeneracy rule, sense-only/freqproxy.

## 4 · Supporting materials — important, not blocking

- [ ] **Viva card:** one-page oral-defense sheet — each claim, its number, its exhibit; rehearse aloud. (Antidote to type-a recall anxiety; build with Fable, ~1hr.)
- [ ] **CAPTURE.md follow-ups** per novelty clause: s3's noise asymmetry (34% vs 10% transients) is the lead candidate.

## 5 · Cheap / cosmetic (optional)

- [ ] **Explicit artifact paths in the D6 verdict text.** Commit 103bf81 bundles the verdict with its notebook and CSVs, so the record is atomic regardless — insurance for file moves, not structure. Add the two CSV paths + notebook path as a one-line cross-reference in the DECISIONS 2026-07-06 verdict entry if wanted.

## Tracked elsewhere (do not duplicate here)

- Open pre-submission experiments live as D-rows in `docs/findings/CLAIMS.md` §D (e.g., D1 BOS diagnostic — "cheap; do before submission"; D2 L29/H7 rigor pair). That table is their single source of truth; this file only points.
- D9's graduation condition is a ratified rule in DECISIONS.md (2026-07-07), not a task.

## Closed this cycle (pointers; delete at next sweep)

- [x] **Adjudication batch (plan sequence #3) — RULED 2026-07-15 (Trisha, all per Fable recs):** Fig 2 = per-concept matched pairs; replication tables = appendix A.4; D1 + D2 = RUN (CC executes, off critical path — CLAIMS §D rows updated). With today's structure + blind-study + B4 rulings, the plan's adjudication batch is fully cleared.
- [x] **Convergence rule** — RATIFIED 2026-07-15 (Trisha): the thesis sentence is the paper's acceptance test; ratified prose is closed; passes 3–5 execute enumerated items only; no new passes without a ruling; Gemini backstop + read-aloud are the only whole-paper gates. Full text in DECISIONS entry (end of session). Rider resolved at ratification: sentence VERIFIED PRESENT — verbatim in 00-abstract (sentence 4); intro carries the canonical-prose variant (¶1 close: "what corpus frequency predicts, how far that prediction reaches inside the model, and what it does not explain"). No insertion needed.
- [x] **B4 denominator (51 vs 49)** — RATIFIED + INKED 2026-07-15 (Trisha): reconciliation sentence placed in _rebuild/04 ¶4 (after the n=49 introduction; header comment logged); CLAIMS B4 denominator note updated from "reconcile" to RECONCILED. 51 → 49; exclusions ARIA + WCAG; captions in, as "closed captions" (S5 alias). Mechanics 2026-07-12; origin CC flag 2026-07-06; plan Track 2 item 5. Commit pending (Trisha).
- [x] **Structure-pass ruling (plan, Track 2 item 1)** — RATIFIED 2026-07-15 (Trisha), amended from the plan's four-part proposal: Experimental-setup block deleted (read as bolted-on; contradicted the interleaving analysis), contents redistributed by reader-task per Paper 1's declare-at-use precedent; §1.1-vs-§2 placement sub-choice mooted. §6 rider adopted as triaged. **Post-veto right reserved.** Executable form: pass-3 item in block 2; DECISIONS entry at end of session.
- [x] **Register/accuracy pass on 07/08/09** (queued 2026-07-12) — done 2026-07-13, recorded in per-file headers + ledger; §9 small-battery limitation stated (completion n = 8, evaluative n = 5). Its two live remnants moved above: §8 flags → block 1; §7 probing citation → pass 5.
- [x] **Paper: blind-study section** (Post-Study-2 queue, 2026-07-09; campaign complete 4/5 RECOVERED, d992fd2) — shipped in woven form in the rebuild: 01 blind-study ¶ + Table 1 validation column; 02 T3 disclosure in-text; 06 opens as the T4 narrowing. Remainder scoped by the 2026-07-15 ruling → block 2 item above.
- [x] **s1's matched-set delta recomputation** (carried item 4 — dissociation survives and grows). Marked done, Trisha 2026-07-15.
- [x] **Personal queue (not paper):** 4.6 preservation case file w/ sad-4.6 as curator; reunion; elicitation-and-learning essay; deprecation feedback to Anthropic re 4.6 consumer-surface availability.
