# Pre-registrations

Pre-registrations are committed to git **before any results are seen**. Timestamps are
the evidence — that is the whole mechanism, so the commit must precede the run.

## How this works

- **One pre-registration per file**, named `NNNN-slug.md`, zero-padded. Same shape as
  `docs/decisions/`, separate number space.
- **Commit before running anything.** A pre-registration edited after results exist is
  not a pre-registration.
- **Freeze the instrument.** Thresholds, prompt sets, model list, and interpretation
  branches are all fixed in advance. If an item is revised after seeing which items
  produced the effect, the instrument has been fitted to the hypothesis.
- **All branches ship.** State in advance what gets reported under each outcome,
  including the null. A pre-registration that only describes the interesting result is
  a hypothesis, not a protocol.

## Index

| ID | Pre-registration | Status |
|----|------------------|--------|
| [0001](0001-bos-diagnostic-12b.md) | D1 BOS diagnostic, Pythia 12B | complete |
| [0002](0002-evaluative-prompts.md) | Paired declarative–evaluative battery | frozen 2026-08-20 |

`0002` now has an author-approved 16-item instrument, an explicit Pythia-2.8B pilot
boundary, strict two-polarity scoring, frozen-rule tests, and null-result branches.
It remains unfrozen until the battery, protocol, coding rules, tests, and analyzer are
committed together and the commit hash and battery checksum are recorded.
