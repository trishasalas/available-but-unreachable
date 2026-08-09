# Anonymization checklist — ADDENDUM (audit 2026-08-07)

Merge into `docs/anonymization-checklist.md`. The existing checklist is correct and
matches current TMLR/ICLR/ICML practice; these are gaps found by sweeping the repos.

## Policy confirmations (re-verified against current guides)

- TMLR: double-blind, submissions must be anonymized. Preprints permitted at any time,
  anonymously OR under your identity — the obligation is **not linking** the submission
  to a named version.
- Third-person self-citation is the standard and sufficient remedy (ICLR author guide).
- **Inference is not a breach.** ICML states explicitly that reviewers deducing identity
  from external resources does not constitute a violation of double-blind. Reviewers are
  instructed not to search. A narrow field does not create an obligation to be unguessable.
- Corollary: omitting Salas (2026) / thatDangCircuit to reduce guessability would be the
  larger error — incomplete related work, plus an uncited load-bearing claim in section 4.

## New sweep items (not in the current checklist)

- [ ] **Abstract, final sentence** — "All artifacts, criteria, and decision logs are public."
      Class-B leak in the most-read paragraph. Change to "available at [anonymized]" for
      the review build; restore at camera-ready.
- [ ] **`paper/build/metadata.yaml`** carries `author: "Trisha Salas"` and there is no
      separate anonymized build target. Create one (or a build-time override) rather than
      hand-editing at submission.
- [ ] **thatDangCircuit has no reference entry** despite section 4 relying on it for the
      population-ablation layer. Add as Class A, third person, with the concept DOI
      10.5281/zenodo.21604592. Reciprocally, thatDangCircuit's README says the citation
      "will be completed here upon publication" — both sides currently point at each other.
- [ ] **`paper/sections/10-references.md`** still contains
      "TODO: Get full citation details (volume, pages, DOIs) for arxiv papers".

## Mirror scope — larger than a copy

Identity strings (`trisha` / `salas`) by repo:

| repo | files affected | notes |
|---|---|---|
| `tmlr/` | 60 | DECISIONS.md, several `src/*.py`, findings docs, metadata.yaml |
| `blind-study/` | 97 | PROTOCOL.md ("Authors: Trisha Salas + Claude"), MANIFEST.md, ~90 session files under `runs/` |

Note `blind-study/MANIFEST.md` lists "Salas, Trisha" **inside the banned-strings list** the
corpus verifier enforces — the anonymity apparatus itself leaks. The existing
`verify_corpus.py` could be repointed at the mirror to check the scrub.

If C5 ships as a Methods subsection with a mirror behind it, budget real time for this;
it is not a same-day task.

## Blog posts (planned)

Permitted, and no need to delay. TMLR allows preprints under your own identity, so blog
posts are strictly weaker. Two rules:
- the submission must not link to them;
- no post should identify a specific manuscript as the one under review at TMLR.

Writing about thatDangCircuit and the blind study under your name during review is fine.
