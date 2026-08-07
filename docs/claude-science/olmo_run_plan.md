# OLMo 2 full-battery run plan (v2 — revisions verified against HF)

Prepared 2026-08-07. v2 supersedes v1: the revision strategy is YOURS (last checkpoint
before stage-2 mid-training) and is correct — v1's `main` recommendation was wrong and is
withdrawn. What changed is the three revision STRINGS, which do not currently match that
intent.

---

## 1. Revision correction (do this first)

Intent: last stage-1 checkpoint before stage-2 mid-training, all three models.
The pinned strings do not implement it.

| model | last stage1 (verified on HF) | currently pinned | fraction of stage 1 |
|---|---|---|---|
| OLMo-2-0425-1B | `stage1-step1907359-tokens4001B` | `stage1-step990000-tokens2077B` | ~52% |
| OLMo-2-1124-7B | `stage1-step928646-tokens3896B` | `stage1-step99000-tokens416B` | ~11% |
| OLMo-2-1124-13B | `stage1-step596057-tokens5001B` | `stage1-step99000-tokens831B` | ~17% |

**Cause (verified, reproducible):** all three pins are exactly the *alphabetically last*
stage-1 branch — the order HuggingFace lists them in. Step numbers are not zero-padded, so
string sort puts `step99000` after `step928646` (`9` > `2` at the third character) and
`step990000` after `step1907359`. The 7B's sorted tail reads
`…step96000, step97000, step98000, step99000`, which looks exactly like the end of a
training run. The true final checkpoints sort back near the top of the list.

This is a systematic UI artifact, not a one-off, and it will recur on any hand re-pin.
Resolve the branch numerically instead:

```python
import re
LAST_STAGE1 = lambda names: max(
    (b for b in names if b.startswith("stage1")),
    key=lambda b: int(re.search(r"step(\d+)", b).group(1)),
)
```

All three corrected revisions verified present with config + weights:

| model | sha | safetensors shards |
|---|---|---|
| OLMo-2-0425-1B | 9d3e43659f | 3 |
| OLMo-2-1124-7B | c0371f4281 | 7 |
| OLMo-2-1124-13B | 08d2aca2e2 | 13 |

**Token-budget confound (audit finding F9) is largely resolved by the fix:** spread goes
from 5.0x (2077 / 416 / 831 B) to 1.28x (4001 / 3896 / 5001 B). Worth one Methods sentence,
no longer a structural problem.

Action: replace the hand-edited `revision = "..."` string in frequency-olmo / entropy-olmo /
elicitation-olmo with one shared module-level mapping so the three notebooks cannot drift.

### Why end-of-stage-1 beats `main` (record this in DECISIONS)

Stage-2 mid-training mixes in curated high-quality data. `main` would confound corpus
frequency with a deliberate data-quality intervention — precisely the variable A3 measures.
End-of-stage-1 gives three models on the same pretraining distribution, and the Infini-gram
index already in use (`v4_olmo-mix-1124_llama`) is the stage-1 mix: index and checkpoint
match. Stage-2 OLMo is a natural follow-up experiment (does curation move the frequency
correlation?), not the base condition.

---

## 2. D8 cannot run on OLMo — pre-register it as an architectural control

`src/tl217_olmo2_adapter.py` sets `unembed.b_U` to zeros: OLMo 2 uses RMSNorm (no beta to
fold) and carries no unembedding bias. `src/d8_frequency_prior.py` guards on exactly this
and raises "b_U is exactly zero -- ln_final beta not folded? Premise violated."

Not a porting bug. C6/D8 claims the lens artifact is frequency-shaped BECAUSE ln_final's
beta folds into b_U, which holds a corpus-frequency prior, and the resid @ W_U shortcut
severs that term. OLMo 2 architecturally lacks the term.

- **Predicted:** no frequency-shaped lens artifact in OLMo 2, or one by a different route.
  Confirms C6's mechanism by its absence where the architecture removes it.
- **Falsifier:** artifact appears anyway → b_U is not the whole story; C6 needs a second route.

Both branches ship. Commit the prediction before running.

---

## 3. Portability — verified where possible

Elicitation battery is ALREADY aligned: 59 concepts, identical prompt_type distribution to
Pythia (declarative 51, control 20, completion 8, evaluative 5, validation 5, hypothesis 3).

Adapter KV-head gate (`num_key_value_heads == num_attention_heads`) — **all three PASS**,
checked against the corrected revisions:

| model | layers | heads | kv_heads | d_model |
|---|---|---|---|---|
| OLMo-2-0425-1B | 16 | 16 | 16 | 2048 |
| OLMo-2-1124-7B | 32 | 32 | 32 | 4096 |
| OLMo-2-1124-13B | 40 | 40 | 40 | 5120 |

Binding is therefore in scope for all three, 13B included (the adapter docstring names only
1B and 7B — it is out of date, not restrictive).

| test | status |
|---|---|
| elicitation + deterministic coding | ready (`code_response` coded 276/276, 0 uncoded) |
| gap (A1) | ready |
| entropy / fluent wrongness (B5) | ready |
| frequency (A3) | ready — Dolma index matches the stage-1 checkpoint |
| trajectories (B3/B4) | ready — needs >= 3 scales, you have exactly 3 |
| binding (A4/B1/B7) | ready — KV gate passes on all three |
| logit lens / MLP (C6) | port + verify: `qk_ov.ov_logit_lens` does centering + real ln_final scale; check on a known OLMo prompt before trusting rollouts |
| D8 (b_U prior) | cannot run — becomes the architectural control (section 2) |

---

## 4. Run order

1. Commit to DECISIONS: corrected revisions, the end-of-stage-1 rationale, the D8 prediction.
2. Fix the three revision strings; centralize as one constant.
3. Elicitation -> deterministic coding -> gap + trajectories.
4. Entropy -> fluent wrongness.
5. Frequency -> Spearman + full robustness battery (partial, PMI, Kendall, bootstrap,
   secondary), so OLMo matches Pythia/GPT-2 in rigor rather than shipping a bare rho.
6. Binding (all three).
7. C6 lens port — single-step readouts first, rollouts only after verification.
8. D8 architectural control.

---

## 5. All prior OLMo numbers are superseded

Everything currently in `results/{frequency,entropy,olmo}/olmo` was produced at the wrong
checkpoints and must be regenerated or archived. Specifically retired:

- rho = 0.3288 / 0.4546 / 0.5088 (stage1 partial checkpoints)
- the contradictory 1B pair (0.4819 in `results/olmo/` vs 0.3288 in `results/frequency/olmo/`,
  audit finding F4) — the correction moots the adjudication
- the gap inversion at 13B (-14.4 pts) and the negative B5 penalties: real at 17% of stage-1
  training, unknown at end-of-stage-1

Do not mix old and new in any table. Archive the stage1-partial run rather than deleting it —
with the corrected run alongside, it becomes a training-budget comparison, which is adjacent
to the blind study's unanimous training-dynamics novelty items (S1a/S1b/S1c/N3).
