# The one genuine lexical head — Pythia-2.8B L29/H7

Head characterization (`what-are-they-doing.ipynb`) resolved the top binding heads as
previous-token / position-1 / attention-sink artifacts — **except** L29/H7, which has
a real `reader`→`screen` carve-out (attention 0.90) that is not BOS, not position-1,
and specific to "screen reader" (on "bicycle wheel" it attends to self instead).

This notebook dissects that head via its two circuits (Elhage et al. 2021):
- **QK** — *where* it attends: is the routing selective to "screen reader"?
- **OV** — *what* it writes: does moving "screen" into "reader" promote relevant tokens?
- **Causal** — is the head necessary, or compensated (the distributed-redundancy story)?

Logic lives in `src/qk_ov.py`. Two outcomes are both informative: a genuine single-head
lexical mechanism, or another confirmation that representation ≠ necessity.

## 1. QK circuit — is the routing selective to "screen reader"?

The trustworthy QK signal on Pythia is the **realized** post-softmax attention (the raw
q·k is swamped by massive-activation outlier dimensions). If L29/H7 routes word2→word1
*only* for "screen reader" and not other compounds, the QK circuit is lexically selective.

### Realized word2->word1 attention across compounds (uniform template).

**Code**

```python
colloc = collocation_scan(model, [(LAYER, HEAD)], template="A {w1} {w2} is")
print(colloc.sort_values("score", ascending=False).to_string(index=False))
```

**Results**

layer  head  domain        compound  score
    29     7    a11y   screen reader 0.9019
    29     7 general    coffee table 0.2104
    29     7    a11y       skip link 0.0725
    29     7 medical     side effect 0.0479
    29     7   legal        case law 0.0465
    29     7 finance    stock market 0.0301
    29     7 finance      hedge fund 0.0209
    29     7 general   bicycle wheel 0.0178
    29     7 finance    credit score 0.0112
    29     7    a11y  color contrast 0.0080
    29     7 medical      heart rate 0.0058
    29     7   legal     due process 0.0057
    29     7 general      phone call 0.0029
    29     7    a11y        alt text 0.0029
    29     7    a11y focus indicator 0.0028
    29     7 medical  blood pressure 0.0011
    29     7   legal     court order 0.0008


### Within the screen-reader prompt, where does "reader" actually look?    

**Code**

```python
for key in ["screen", "A", "reader"]:
print(realized_attention(model, LAYER, HEAD, SR_PROMPT, "reader", key))
```

**Results**

{'query': 'reader', 'key': 'screen', 'attention': 0.9019}
{'query': 'reader', 'key': 'A', 'attention': 0.0001}
{'query': 'reader', 'key': 'reader', 'attention': 0.0121}

### Intrinsic (weight-based) QK preference, E[q] W_Q . E[k] W_K.

**Code**

```python
# NOTE: at layer 29 the residual has evolved far from the token embeddings, so this
# embedding-level view is a WEAK proxy. Near-zero here is itself informative: it means
# the lock is built up THROUGH the layers, not present in the raw embeddings.
second = ["reader", "wheel", "text", "market", "process"]
first  = ["screen", "bicycle", "alt", "stock", "due"]
print(qk_token_matrix(model, LAYER, HEAD, second, first).to_string())
```

**Results**

screen  bicycle    alt  stock    due
reader   -0.002   -0.001 -0.000  0.002  0.000
wheel     0.005    0.004  0.000  0.000  0.002
text     -0.003   -0.002  0.000  0.003  0.000
market   -0.001   -0.004  0.000  0.004 -0.001
process  -0.007   -0.003 -0.003  0.004 -0.002

## 2. OV circuit — what does it write when attending to "screen"?

Push "screen"'s value through the OV circuit (W_V then W_O), scaled by the realized attention, and logit-lens the result (direct logit attribution). If the write promotes screen-reader / accessibility-relevant tokens, the head is moving *content*, not noise.

**Code**

```python
ov = ov_logit_lens(model, LAYER, HEAD, SR_PROMPT, "screen", "reader", top_k=20)
print(f"attention screen->reader: {ov['attention']}")
print("\nPROMOTED tokens:")
for tok, val in ov["promoted"]:
    print(f"  {tok!r:>16}  {val}")
print("\nSUPPRESSED tokens:")
for tok, val in ov["suppressed"]:
    print(f"  {tok!r:>16}  {val}")
```

**Results**

attention screen->reader: 0.9019

PROMOTED tokens:
            'fire'  0.515
        ' shooter'  0.455
           ' fire'  0.443
       ' shooting'  0.436
           'fires'  0.432
          ' shoot'  0.419
            'camp'  0.385
          ' fires'  0.383
            'Fire'  0.383
          'loader'  0.374
       ' firearms'  0.37
            'chin'  0.366
          'reload'  0.366
          'logger'  0.362
  ' photographers'  0.361
          ' firef'  0.361
            ' ear'  0.36
            'LAND'  0.355
           'lands'  0.353
         ' losing'  0.353

SUPPRESSED tokens:
         ' screen'  -1.409
        ' screens'  -1.291
          'screen'  -1.23
         ' Screen'  -1.158
          'Screen'  -1.114
      ' screening'  -1.014
       ' screened'  -0.972
            'scre'  -0.892
            'Scre'  -0.879
           ' Scre'  -0.866
           'creen'  -0.749
          ' Wings'  -0.57
           'clean'  -0.536
            ' air'  -0.52
       ' aviation'  -0.515
          ' clean'  -0.508
          ' plane'  -0.487
          ' wings'  -0.482
          ' airst'  -0.48
         ' filter'  -0.48

## 3. Causal check — is the head necessary?

Zero L29/H7's output at the `reader` position and measure the change in the model's next-token prediction for "A screen reader is ___". Large KL → a genuine, necessary single-head mechanism. Small KL → compensated downstream (the distributed-redundancy story from thatDangCircuit). The "bicycle wheel" control should barely move.

**Code**

```python
res = ablate_head_at_position(model, SR_PROMPT, LAYER, HEAD, "reader", top_k=10)
print(f"KL(base || ablated): {res['kl_base_to_ablated']}")
print("baseline top:", res["baseline_top"])
print("ablated  top:", res["ablated_top"])
```

**Results**

KL(base || ablated): 1e-05
baseline top: [(' a', 0.5137), (' an', 0.1712), (' software', 0.0329), (' used', 0.0288), (' not', 0.015), (' the', 0.0149), (' available', 0.0122), (' designed', 0.0105), (' often', 0.0103), (' typically', 0.0084)]
ablated  top: [(' a', 0.5136), (' an', 0.171), (' software', 0.0331), (' used', 0.0288), (' not', 0.0149), (' the', 0.0149), (' available', 0.0124), (' designed', 0.0106), (' often', 0.0103), (' typically', 0.0084)]

**Code**

```python
# Control: ablate the same head where it does NOT bind (on "bicycle wheel" it attends to self, not to "bicycle"). Expect a much smaller KL than the screen-reader case.
ctrl = ablate_head_at_position(model, "A bicycle wheel is", LAYER, HEAD, "wheel", top_k=10)
print(f"control KL (bicycle wheel): {ctrl['kl_base_to_ablated']}")
print(f"screen-reader KL:           {res['kl_base_to_ablated']}")
```

**Results**

control KL (bicycle wheel): 0.0
screen-reader KL:           1e-05

## Reading the results

- **QK selective + OV writes relevant tokens + ablation moves the output** → a genuine
  single-head lexical retrieval mechanism for "screen reader." Small but real positive
  result; worth a figure.
- **QK selective + OV relevant + ablation inert** → the head *represents* the pairing
  but isn't *necessary* — consistent with thatDangCircuit's distributed/redundant
  finding. Representation ≠ retrieval, at the single-head level.
- **OV writes noise / no relevant tokens** → the carve-out is an attention curiosity
  without a clear computational role; downgrade the lead.

Whichever way it lands, record it in `docs/head-characterization-findings.md` §6.