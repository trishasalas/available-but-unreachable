# D7 run summary

- timestamp: 2026-07-05T00:25:57
- model: pythia-12b  |  TL: 2.17.0  |  dtype: torch.float32  |  device: cuda:0
- prompt (frozen, amended referent): 'A skip link is'

- ban list: [("'click'", 9738), ("' click'", 5532), ("'Click'", 7146), ("' Click'", 15682)]

## Gate 1 — lens-pathway regression
- chosen sequence matches frozen CSV, 15 steps: YES
- 'click' wins Step 5 (lens): True
- PASSED: True

## Gate 2 — standard-forward agreement
- 'click' wins Step 5 (true forward pass): False
- 'displayed' rank at Step 5 (pre-ban): 5

**ABORT: lens and forward pass disagree at Step 5. Instrumentation question (branch 3) — stop, exonerate the harness before interpreting.**