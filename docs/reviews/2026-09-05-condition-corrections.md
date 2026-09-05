# Proposed condition and tokenization corrections

Status: manuscript prose approved and applied. Reconciled canonical results and figures integrated with an explicit hash-bound GPT-2-large input mapping.

## Results

Replace “The direction repeats under uniform prompts and after controlling for compound token count.” with:

The direction repeats under uniform prompts at all thirteen model-scale points.

## Discussion

Replace “The direction survives a uniform prompt and token-count controls.” with:

The direction repeats under uniform prompts.

## Methods: corpus frequency

Replace “OLMo uses counts from OLMo-Mix-1124, matching its training data.” with:

For declarative accuracy, OLMo uses counts from OLMo-Mix-1124, matching its training data. The registered value-weighted binding analysis uses the same frozen Pile-frequency table for all thirteen models, treating it as a cross-corpus reference for GPT-2 and OLMo.

## Numerical correction

GPT-2 774M natural-prompt rho in Table 5 (and its appendix copy) changes from -0.362 to -0.350. Its 95% bootstrap interval is [-0.596, -0.043]. Figure 5 must use the reconciled natural-prompt table. The corrected thirteen-model aggregate p remains 0.0003.

## Verified uniform replication

The GPT-2-medium uniform rerun is verified (780f639). Its rho is -0.430, with 95% bootstrap interval [-0.648, -0.153]. The complete uniform aggregate p is 0.0004; natural remains 0.0003. Update the appendix draft accordingly. The original duplicate remains archived, and GPT-2-large conditions are reconciled using actual prompt text.

## Tokenization account

Retain the existing Methods last-subtoken description. The appendix will describe deliberate span matching and the existing exclusions. No statistical binding token-count control is claimed, and no new token-count sensitivity has been run.
