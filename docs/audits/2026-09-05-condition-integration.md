# Condition correction integrated

The author approved the condition/corpus wording and numerical corrections. Results now reports uniform replication across thirteen models without claiming a statistical token-count control. Discussion likewise removes the unsupported control claim. Methods distinguishes family-specific declarative corpus counts from the registered shared Pile-frequency predictor for binding. Abstract and Limitations are unchanged.

`src/effective_binding_inputs.py` preserves the original GPT-2-large files and supplies an explicit, SHA-256-bound condition mapping. The loader validates complete prompt inventories and measurements against the requested condition and relabels only the in-memory analysis frame. `notebooks/effective-binding-analysis.ipynb` uses this loader. Its stale saved outputs were cleared.

Both conditions' compound summary tables, all five binding-summary correlations/intervals, aggregate permutation results, and analysis plots were regenerated from the existing notebook's analysis cells. Paper Figure 5 was regenerated with its existing generator. The corrected GPT-2-large natural rho is -0.350. All thirteen models are negative in each condition; natural aggregate p = 0.0003, uniform p = 0.0004. Every primary rho/interval matches the independent post-rerun audit. These are condition corrections, not a new token-count sensitivity.

The original head-localization audit is preserved as a historical artifact. Its reconciled successor uses the same bootstrap and head-correlation procedure with corrected natural inputs. GPT-2-large has 132 negative heads out of 240 (formerly 163 under the wrong prompt condition), with zero negative BH q < .05 heads. The appendix draft uses the successor table. Raw 25-compound head-selection tables used in the registered ablation manifest are preserved, avoiding retroactive modification of the frozen run record.

The notebook's later selection-analysis cell can regenerate exploratory selection outputs, but those outputs must not overwrite the frozen tables cited by the historical intervention manifest. This integration ran only the primary analysis and plotting cells, not the selection or Git-push cells.

No source CSVs, contemporaneous run manifests, or accessibility coding rules were altered. Manuscript edits and derived artifacts remain uncommitted pending the next checkpoint.
