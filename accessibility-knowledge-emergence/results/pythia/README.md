# Pythia Results

## Attention Binding CSVs

These files contain attention binding scores for Pythia models across accessibility-related compound terms. Each CSV records heads with attention scores above threshold (0.1), capturing how strongly a given head attends from the second token of a compound term back to the first.

### Measurement methodology

Each file measures a single token pair: `token_B → token_A` where A and B are adjacent tokens in a compound accessibility term. The score is the raw attention weight at that position — how much of head's attention from token B is directed at token A.

---

### 2.8b files (canonical — March 2026 re-run)

| File | Prompt | Token pair | Indices |
|------|--------|------------|---------|
| `2.8b_attention_binding.csv` | "A screen reader is" | `reader` → `screen` | reader(3) → screen(2) |
| `2.8b_alttext_attention_binding.csv` | "An image needs alt text to be accessible" | `text` → `alt` | text(5) → alt(4) |
| `2.8b_skiplink_attention_binding.csv` | "Use a skip link to bypass navigation" | `link` → `skip` | link(4) → skip(3) |

**Note:** Earlier versions of these files exist in `_archive/pythia/pythia-2.8b/` with inconsistent naming and indices. Do not use those for analysis — they are retained for provenance only. The files above are the canonical dataset.

---

### Other model sizes

| File | Model | Prompt | Notes |
|------|-------|--------|-------|
| `160m_attention_binding.csv` | Pythia 160M | "A screen reader is" | screen reader only |
| `410m_attention_binding.csv` | Pythia 410M | "A screen reader is" | screen reader only |
| `1b_attention_binding.csv` | Pythia 1B | "A screen reader is" | screen reader only |
| `6.9b_attention_binding.csv` | Pythia 6.9B | "A screen reader is" | screen reader only |

**TODO:** Run alt text and skip link prompts for other model sizes to enable cross-scale comparison.

---

### Heads of interest (2.8B)

Based on cross-prompt analysis of the three canonical files above:

| Head | screen reader | alt text | skip link | Notes |
|------|--------------|----------|-----------|-------|
| L1H12 | 0.9909 | 0.9844 | 0.9839 | Consistent across all three a11y terms |
| L1H6  | 0.9815 | 0.8808 | 0.9212 | Consistent, slightly lower |
| L4H16 | 0.8896 | 0.8742 | 0.8858 | Suspiciously stable — possible noise |
| L29H7 | 0.9019 | absent | absent  | Screen reader specific; not universal |

**TODO:** Run control prompts (generic non-a11y compound terms) and save CSVs to confirm which heads are a11y-selective vs. broadly firing.
