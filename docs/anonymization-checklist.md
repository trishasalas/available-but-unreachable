# Anonymization checklist — TMLR submission gate

The short answer to "how do I cite myself?": **in the third person, like anyone
else's work.** This is standard double-blind procedure, TMLR expects it, and it is
not deception — reviewers know authors have prior work; they just shouldn't be told
which citations are yours.

## The rule that resolves almost everything

Cite Salas (2026) exactly as you'd cite Kandpal or Belrose: "Salas (2026)
established the correlation; this paper's expanded sweep replicates it." That
sentence — already in §3 — is ALREADY COMPLIANT. What's forbidden is first-person
linkage: "our prior work," "we previously showed," "the author's earlier paper."
The audit is a search for those patterns, not a rewrite.

## Two classes of artifact — handled differently

**Class A — PRIOR work (Paper 1, thatDangCircuit).** Cite third-person with real
DOIs, in the references, under Salas. Allowed, normal, no mirror needed. The
thatDangCircuit Zenodo DOI goes in as: Salas, T. (2026). thatDangCircuit
[software/data]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX — resolving §3's
"DOI pending."

**Class B — THIS paper's artifacts (elicitation battery, decision logs, coding
criteria, the paper repo, SCORING.md).** These cannot be third-personed — they are
this paper's own supplementary material, and linking your named GitHub identifies
you. For review: anonymous mirror (anonymous.4open.science, or an anonymized
GitHub org) — "all artifacts, criteria, and decision logs are available at
[anonymized]." Real links + archival DOI swap in at camera-ready.

## The sweep list (run at submission, in order)

- [ ] Grep the paper for: "our prior", "our earlier", "we previously", "my ",
      "the author's" — fix any first-person linkage to prior work.
- [ ] "One author's professional practice"-type sentences: generalize or cut
      (profession + Salas citation adjacent = triangulation).
- [ ] Class-B links → anonymous mirror; verify every repo/decision-log pointer
      in the text resolves to the mirror, not trishasalas anything.
- [ ] Colophon: stripped from the submission build.
- [ ] Acknowledgments: omitted until camera-ready.
- [ ] PDF metadata: author fields blank in the anonymized build target
      (check pandoc metadata.yaml → anonymized target).
- [ ] References: Paper 1 + thatDangCircuit present, third-person, real DOIs.
- [ ] LLM-assistance disclosure footnote present (TMLR FAQ requirement) — the
      footnote itself is anonymity-safe; verify current required wording at
      submission.

## What you do NOT need to do

- You do not need to hide that Paper 1 exists, unpublish anything, or scrub your
  public preprints/repos from the internet. Double-blind is best-effort on the
  submission's contents; your public research life continues as normal.
- You do not need to anonymize the thatDangCircuit repo itself — it's Class A,
  cited like anyone's artifact.

## Verify-at-submission note

The above is the standard TMLR double-blind pattern and matches the plan's
"third-person Salas audit." One item to re-verify against the current TMLR author
guide + FAQ on submission day: exact anonymous-mirror expectations and the LLM
footnote wording. Ten minutes, day-of.
