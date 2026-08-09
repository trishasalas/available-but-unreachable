---
name: transformerlens-refuses-mps
description: "TransformerLens 2.18 silently falls back to CPU on Apple Silicon; notebooks print \"Using device: mps\" but run on CPU"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 35a30dac-d2d9-49c8-a191-050032d5453e
  modified: 2026-08-08T16:14:30.811Z
---

TransformerLens 2.18's `utils.get_device()` **deliberately refuses to
auto-select MPS**. Its `_MPS_MIN_SAFE_TORCH_VERSION` is `None`, meaning no torch
version is currently considered safe, because of known correctness issues
(TransformerLens issue #1178). It falls back to CPU unless
`TRANSFORMERLENS_ALLOW_MPS=1` is set.

The tmlr notebooks compute a `device` variable and print `Using device: mps`,
but never pass it to `HookedTransformer.from_pretrained(...)` — so local runs
execute on CPU. The manifest is correct and self-consistent: `Server: GPU: Apple
MPS` reports hardware present, `Device: cpu` reports where the model actually
is. The **printed message** is the wrong part, not the manifest.

**Why:** Worth leaving on CPU. TL is guarding against silently-wrong numbers on
exactly the attention tensors the binding battery measures; forcing MPS trades
correctness for speed.
**How to apply:** Don't "fix" this by setting `TRANSFORMERLENS_ALLOW_MPS=1` or
passing `device=device`. If local runs are too slow, use Colab GPU. Verified
2026-08-08 on torch 2.10.0 / transformer_lens 2.18.0.
