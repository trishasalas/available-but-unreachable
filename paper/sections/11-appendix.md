## Appendix A: Binding Audit Detail

### A.1 Per-head diagnostics

This table backs the sink-and-structure findings of Section 3: for each top binding head, its layer, binding score, induction score, previous-token score, beginning-of-sequence attention mass, and resulting classification.

<!-- TABLE PLACEHOLDER — populate from the head-audit results at promotion. Columns: head · layer · binding score · induction · prev-token · BOS mass · classification. -->

One reclassification deserves prose: L27/H10 shows 0.82 generic attention mass on the beginning-of-sequence token at idle, which would disqualify it as an attention sink under off-target measurement; measured at the compound's own binding position, that mass proves to be idle-parking, and the head is selective on target. This case motivates the on-target measurement rule of A.2.

### A.2 Joint-ablation set-earning criteria and gate accounting

Sink and positional status are measured at the compound's own binding position, because a selective head at idle parks its attention mass on the beginning-of-sequence token, and off-target measurement would disqualify exactly the heads under test.

Earned sets by compound: screen reader earns two heads (L29/H7, L27/H10); alt text and stock market each earn bespoke three-head sets with zero overlap with each other or with screen reader's; the complete per-compound set composition, protocol, and disclosed amendment are in the public decision log's gate accounting.

One panel compound, semantic HTML, degenerated at the set-earning stage: its natural prompt fragments the sentence-initial first word under tokenization, so its candidate pool was nominated largely by fragment-merging attention rather than pairing selectivity; its over-inclusive thirteen-head set nonetheless ablates to 0.0015, and Section 3 reports it per-compound with that caveat.
