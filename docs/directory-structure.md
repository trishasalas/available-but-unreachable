# Directory Structure

👉  tree
├── DECISIONS.md
├── README.md
├── data
│   ├── accessibility.yaml
│   ├── backup.py
│   ├── binding
│   │   ├── accessibility.yaml
│   │   ├── control.yaml
│   │   ├── finance.yaml
│   │   ├── legal.yaml
│   │   └── medical.yaml
│   ├── control.yaml
│   ├── finance.yaml
│   ├── infini_gram_calibration_counts.csv
│   ├── legal.yaml
│   └── medical.yaml
├── docs
│   ├── claude-science
│   │   ├── anonymization-addendum.md
│   │   ├── anonymization-checklist.md
│   │   ├── olmo_run_plan.md
│   │   ├── tmlr_audit_findings.csv
│   │   └── tmlr_audit_report.md
│   ├── d1-preregistration.md
│   ├── findings
│   │   ├── CLAIMS.md
│   │   ├── The one genuine lexical head.md
│   │   ├── coding_coverage.csv
│   │   ├── criteria_authoring.csv
│   │   ├── head-characterization-findings.md
│   │   ├── lexical-head-results.md
│   │   └── results-significance.md
│   └── superpowers
│       ├── plans
│       │   ├── 2026-08-07-entropy-manifest-update.md
│       │   ├── 2026-08-08-binding-notebook-migration.md
│       │   └── 2026-08-08-manifest-per-battery-writers.md
│       └── specs
│           ├── 2026-08-07-entropy-manifest-update-design.md
│           ├── 2026-08-08-binding-notebook-migration-design.md
│           └── 2026-08-08-manifest-per-battery-writers-design.md
├── notebooks
│   ├── analysis.ipynb
│   ├── archive
│   │   ├── mlp.ipynb
│   │   └── tangent.ipynb
│   ├── binding-gpt2.ipynb
│   ├── binding-induction-head-test.ipynb
│   ├── binding-lexical-head.ipynb
│   ├── binding-olmo.ipynb
│   ├── binding-pythia.ipynb
│   ├── d1-bos-diagnostic.ipynb
│   ├── d6-multihead-ablation.ipynb
│   ├── d8-frequency-prior.ipynb
│   ├── elicitation-gpt2.ipynb
│   ├── elicitation-olmo.ipynb
│   ├── elicitation-pythia.ipynb
│   ├── entropy-gpt2.ipynb
│   ├── entropy-olmo.ipynb
│   ├── entropy-pythia.ipynb
│   ├── frequency-gpt2.ipynb
│   ├── frequency-olmo.ipynb
│   ├── frequency-pythia.ipynb
│   └── logit-lens-analysis.ipynb
├── paper
│   ├── README.md
│   ├── build
│   │   ├── filters
│   │   │   ├── caption-style.lua
│   │   │   └── figure-alt.lua
│   │   ├── header.tex
│   │   ├── metadata.yaml
│   │   └── template.tex
│   ├── build-debug
│   │   ├── paper-intermediate-luamml-mathml.html
│   │   ├── paper-intermediate.aux
│   │   ├── paper-intermediate.log
│   │   ├── paper-intermediate.pdf
│   │   ├── paper-intermediate.tex
│   │   ├── template.aux
│   │   ├── template.fdb_latexmk
│   │   ├── template.fls
│   │   └── template.log
│   ├── build-paper.sh
│   ├── figures
│   │   ├── binding-vs-accuracy.png
│   │   ├── completion-paradox.png
│   │   ├── concept-trajectories.png
│   │   └── gap-behavioral-internal.png
│   ├── generate-figures
│   │   ├── generate-fig-binding-vs-accuracy.py
│   │   ├── generate-fig-completion-paradox.py
│   │   ├── generate-fig-concept-trajectories.py
│   │   └── generate-fig-gap-behavioral-internal.py
│   └── sections
│       ├── 01-introduction.md
│       ├── 02-the-behavioral-gap.md
│       ├── 03-frequency-predicts-failure-structure.md
│       ├── 04-binding-generalizes-but-is-not-causal.md
│       ├── 05-fluent-wrongness.md
│       ├── 06-measurement-pathways.md
│       ├── 07-related-work.md
│       ├── 08-discussion.md
│       ├── 09-limitations.md
│       ├── 10-references.md
│       ├── 11-appendix.md
│       └── 12-colophon.md
├── requirements.txt
├── results
│   ├── _archive
│   │   ├── d7_ban_list.csv
│   │   ├── d7_gate1_lens_regression.csv
│   │   ├── d7_gate2_forward_trace.csv
│   │   ├── d7_step5_ranks_preban.csv
│   │   ├── d7_summary.md
│   │   ├── gpt2-binding.csv
│   │   ├── gpt2-expansion-results.csv
│   │   ├── gpt2-large-binding.csv
│   │   ├── gpt2-large-expansion-results.csv
│   │   ├── gpt2-medium-binding.csv
│   │   ├── gpt2-medium-expansion-results.csv
│   │   ├── gpt2-xl-binding.csv
│   │   ├── gpt2-xl-expansion-results.csv
│   │   ├── mlp
│   │   │   ├── gpt2
│   │   │   │   ├── gpt2-large_decomposition.csv
│   │   │   │   ├── gpt2-large_late_layer_summary.csv
│   │   │   │   ├── gpt2-large_logit_lens.csv
│   │   │   │   ├── gpt2-large_skip_link_steps.csv
│   │   │   │   ├── gpt2-large_vocab_projection.csv
│   │   │   │   ├── gpt2-medium_decomposition.csv
│   │   │   │   ├── gpt2-medium_late_layer_summary.csv
│   │   │   │   ├── gpt2-medium_logit_lens.csv
│   │   │   │   ├── gpt2-medium_skip_link_steps.csv
│   │   │   │   ├── gpt2-medium_vocab_projection.csv
│   │   │   │   ├── gpt2-xl_decomposition.csv
│   │   │   │   ├── gpt2-xl_late_layer_summary.csv
│   │   │   │   ├── gpt2-xl_logit_lens.csv
│   │   │   │   ├── gpt2-xl_skip_link_steps.csv
│   │   │   │   ├── gpt2-xl_vocab_projection.csv
│   │   │   │   ├── gpt2_decomposition.csv
│   │   │   │   ├── gpt2_late_layer_summary.csv
│   │   │   │   ├── gpt2_logit_lens.csv
│   │   │   │   ├── gpt2_skip_link_steps.csv
│   │   │   │   └── gpt2_vocab_projection.csv
│   │   │   └── pythia
│   │   │       ├── pythia-12b_decomposition.csv
│   │   │       ├── pythia-12b_late_layer_summary.csv
│   │   │       ├── pythia-12b_logit_lens.csv
│   │   │       ├── pythia-12b_skip_link_steps.csv
│   │   │       ├── pythia-12b_vocab_projection.csv
│   │   │       ├── pythia-160m_decomposition.csv
│   │   │       ├── pythia-160m_late_layer_summary.csv
│   │   │       ├── pythia-160m_logit_lens.csv
│   │   │       ├── pythia-160m_skip_link_competition.csv
│   │   │       ├── pythia-160m_skip_link_steps.csv
│   │   │       ├── pythia-160m_vocab_projection.csv
│   │   │       ├── pythia-1b_decomposition.csv
│   │   │       ├── pythia-1b_late_layer_summary.csv
│   │   │       ├── pythia-1b_logit_lens.csv
│   │   │       ├── pythia-1b_skip_link_steps.csv
│   │   │       ├── pythia-1b_vocab_projection.csv
│   │   │       ├── pythia-2.8b_decomposition.csv
│   │   │       ├── pythia-2.8b_late_layer_summary.csv
│   │   │       ├── pythia-2.8b_logit_lens.csv
│   │   │       ├── pythia-2.8b_skip_link_steps.csv
│   │   │       ├── pythia-2.8b_vocab_projection.csv
│   │   │       ├── pythia-410m_decomposition.csv
│   │   │       ├── pythia-410m_late_layer_summary.csv
│   │   │       ├── pythia-410m_logit_lens.csv
│   │   │       ├── pythia-410m_skip_link_competition.csv
│   │   │       ├── pythia-410m_skip_link_steps.csv
│   │   │       ├── pythia-410m_vocab_projection.csv
│   │   │       ├── pythia-6.9b_decomposition.csv
│   │   │       ├── pythia-6.9b_late_layer_summary.csv
│   │   │       ├── pythia-6.9b_logit_lens.csv
│   │   │       ├── pythia-6.9b_skip_link_steps.csv
│   │   │       └── pythia-6.9b_vocab_projection.csv
│   │   ├── pythia-12B-expansion-results.csv
│   │   ├── pythia-12b-binding.csv
│   │   ├── pythia-160m-binding.csv
│   │   ├── pythia-160m-expansion-results.csv
│   │   ├── pythia-1B-expansion-results.csv
│   │   ├── pythia-1b-binding.csv
│   │   ├── pythia-2.8B-expansion-results.csv
│   │   ├── pythia-2.8b-binding.csv
│   │   ├── pythia-2.8b-candidate-heads.csv
│   │   ├── pythia-2.8b-collocation.csv
│   │   ├── pythia-2.8b-head-characterization.csv
│   │   ├── pythia-2.8b-multihead-ablation.csv
│   │   ├── pythia-410m-binding.csv
│   │   ├── pythia-410m-expansion-results.csv
│   │   ├── pythia-6.9B-expansion-results.csv
│   │   └── pythia-6.9b-binding.csv
│   ├── adhoc
│   │   ├── d1_bos_diagnostic
│   │   │   ├── VERDICT.md
│   │   │   └── d1_late_head_characterization.csv
│   │   ├── d8_frequency_prior
│   │   │   ├── d8_bU_pythia-12b.csv
│   │   │   ├── d8_bU_pythia-160m.csv
│   │   │   ├── d8_bU_pythia-1b.csv
│   │   │   ├── d8_bU_pythia-2.8b.csv
│   │   │   ├── d8_bU_pythia-410m.csv
│   │   │   ├── d8_bU_pythia-6.9b.csv
│   │   │   ├── d8_calibration_summary.md
│   │   │   ├── d8_per_scale.csv
│   │   │   └── d8_summary.md
│   │   └── gap-paper-replication
│   │       ├── README.md
│   │       ├── elicitation-robustness-v2-checkpoint-frozen.ipynb
│   │       ├── exp2b-socratic-flip-summary.csv
│   │       ├── pythia-1b-exp2b-entropy.csv
│   │       └── pythia-2.8b-exp2b-entropy.csv
│   ├── analysis
│   │   ├── accuracy_by_prompt_type.csv
│   │   ├── binding_accuracy_corr.csv
│   │   ├── binding_vs_accuracy.csv
│   │   ├── completion_paradox.csv
│   │   ├── criteria_strictness_audit.csv
│   │   ├── criteria_strictness_audit_full.csv
│   │   ├── degenerate_by_concept.csv
│   │   ├── degenerate_by_prompt_type.csv
│   │   ├── degenerate_by_scale.csv
│   │   ├── elicitation_coded.csv
│   │   ├── emergence_thresholds.csv
│   │   ├── entropy_confidence.csv
│   │   ├── entropy_divergence.csv
│   │   ├── fluent_wrongness.csv
│   │   ├── gpt2_declarative.csv
│   │   ├── gpt2_evaluative.csv
│   │   ├── gpt2_gap.csv
│   │   ├── olmo_declarative.csv
│   │   ├── olmo_evaluative.csv
│   │   ├── olmo_gap.csv
│   │   ├── per_concept_scaling.csv
│   │   ├── per_concept_trajectories.csv
│   │   ├── pythia_declarative.csv
│   │   ├── pythia_evaluative.csv
│   │   ├── pythia_gap.csv
│   │   └── trajectory_stability_audit.csv
│   ├── binding
│   │   ├── gpt2
│   │   │   ├── gpt2
│   │   │   │   ├── gpt2-accessibility.csv
│   │   │   │   ├── gpt2-binding.md
│   │   │   │   ├── gpt2-control.csv
│   │   │   │   ├── gpt2-finance.csv
│   │   │   │   ├── gpt2-legal.csv
│   │   │   │   └── gpt2-medical.csv
│   │   │   ├── gpt2-large
│   │   │   │   ├── gpt2-large-accessibility.csv
│   │   │   │   ├── gpt2-large-binding.md
│   │   │   │   ├── gpt2-large-control.csv
│   │   │   │   ├── gpt2-large-finance.csv
│   │   │   │   ├── gpt2-large-legal.csv
│   │   │   │   └── gpt2-large-medical.csv
│   │   │   ├── gpt2-medium
│   │   │   │   ├── gpt2-medium-accessibility.csv
│   │   │   │   ├── gpt2-medium-binding.md
│   │   │   │   ├── gpt2-medium-control.csv
│   │   │   │   ├── gpt2-medium-finance.csv
│   │   │   │   ├── gpt2-medium-legal.csv
│   │   │   │   └── gpt2-medium-medical.csv
│   │   │   └── gpt2-xl
│   │   │       ├── gpt2-xl-accessibility.csv
│   │   │       ├── gpt2-xl-binding.md
│   │   │       ├── gpt2-xl-control.csv
│   │   │       ├── gpt2-xl-finance.csv
│   │   │       ├── gpt2-xl-legal.csv
│   │   │       └── gpt2-xl-medical.csv
│   │   ├── olmo
│   │   │   ├── OLMo-2-0425-1B
│   │   │   │   ├── OLMo-2-0425-1B-accessibility.csv
│   │   │   │   ├── OLMo-2-0425-1B-binding.md
│   │   │   │   ├── OLMo-2-0425-1B-control.csv
│   │   │   │   ├── OLMo-2-0425-1B-finance.csv
│   │   │   │   ├── OLMo-2-0425-1B-legal.csv
│   │   │   │   └── OLMo-2-0425-1B-medical.csv
│   │   │   ├── OLMo-2-1124-13B
│   │   │   │   ├── OLMo-2-1124-13B-accessibility.csv
│   │   │   │   ├── OLMo-2-1124-13B-binding.md
│   │   │   │   ├── OLMo-2-1124-13B-control.csv
│   │   │   │   ├── OLMo-2-1124-13B-finance.csv
│   │   │   │   ├── OLMo-2-1124-13B-legal.csv
│   │   │   │   └── OLMo-2-1124-13B-medical.csv
│   │   │   └── OLMo-2-1124-7B
│   │   │       ├── OLMo-2-1124-7B-accessibility.csv
│   │   │       ├── OLMo-2-1124-7B-binding.md
│   │   │       ├── OLMo-2-1124-7B-control.csv
│   │   │       ├── OLMo-2-1124-7B-finance.csv
│   │   │       ├── OLMo-2-1124-7B-legal.csv
│   │   │       └── OLMo-2-1124-7B-medical.csv
│   │   └── pythia
│   │       ├── pythia-13b
│   │       │   ├── pythia-13b-accessibility.csv
│   │       │   ├── pythia-13b-binding.md
│   │       │   ├── pythia-13b-control.csv
│   │       │   ├── pythia-13b-finance.csv
│   │       │   ├── pythia-13b-legal.csv
│   │       │   └── pythia-13b-medical.csv
│   │       ├── pythia-160m
│   │       │   ├── pythia-160m-accessibility.csv
│   │       │   ├── pythia-160m-binding.md
│   │       │   ├── pythia-160m-control.csv
│   │       │   ├── pythia-160m-finance.csv
│   │       │   ├── pythia-160m-legal.csv
│   │       │   └── pythia-160m-medical.csv
│   │       ├── pythia-1b
│   │       │   ├── pythia-1b-accessibility.csv
│   │       │   ├── pythia-1b-binding.md
│   │       │   ├── pythia-1b-control.csv
│   │       │   ├── pythia-1b-finance.csv
│   │       │   ├── pythia-1b-legal.csv
│   │       │   └── pythia-1b-medical.csv
│   │       ├── pythia-2.8b
│   │       │   ├── pythia-2.8b-accessibility.csv
│   │       │   ├── pythia-2.8b-binding.md
│   │       │   ├── pythia-2.8b-control.csv
│   │       │   ├── pythia-2.8b-finance.csv
│   │       │   ├── pythia-2.8b-legal.csv
│   │       │   └── pythia-2.8b-medical.csv
│   │       ├── pythia-410m
│   │       │   ├── pythia-410m-accessibility.csv
│   │       │   ├── pythia-410m-binding.md
│   │       │   ├── pythia-410m-control.csv
│   │       │   ├── pythia-410m-finance.csv
│   │       │   ├── pythia-410m-legal.csv
│   │       │   └── pythia-410m-medical.csv
│   │       └── pythia-6.9b
│   │           ├── pythia-6.9b-accessibility.csv
│   │           ├── pythia-6.9b-binding.md
│   │           ├── pythia-6.9b-control.csv
│   │           ├── pythia-6.9b-finance.csv
│   │           ├── pythia-6.9b-legal.csv
│   │           └── pythia-6.9b-medical.csv
│   ├── elicitation
│   │   ├── gpt2
│   │   │   ├── gpt2
│   │   │   │   ├── gpt2-accessibility.csv
│   │   │   │   ├── gpt2-control.csv
│   │   │   │   ├── gpt2-elicitation.md
│   │   │   │   ├── gpt2-finance.csv
│   │   │   │   ├── gpt2-legal.csv
│   │   │   │   └── gpt2-medical.csv
│   │   │   ├── gpt2-large
│   │   │   │   ├── gpt2-large-accessibility.csv
│   │   │   │   ├── gpt2-large-control.csv
│   │   │   │   ├── gpt2-large-elicitation.md
│   │   │   │   ├── gpt2-large-finance.csv
│   │   │   │   ├── gpt2-large-legal.csv
│   │   │   │   └── gpt2-large-medical.csv
│   │   │   ├── gpt2-medium
│   │   │   │   ├── gpt2-medium-accessibility.csv
│   │   │   │   ├── gpt2-medium-control.csv
│   │   │   │   ├── gpt2-medium-elicitation.md
│   │   │   │   ├── gpt2-medium-finance.csv
│   │   │   │   ├── gpt2-medium-legal.csv
│   │   │   │   └── gpt2-medium-medical.csv
│   │   │   └── gpt2-xl
│   │   │       ├── gpt2-xl-accessibility.csv
│   │   │       ├── gpt2-xl-control.csv
│   │   │       ├── gpt2-xl-elicitation.md
│   │   │       ├── gpt2-xl-finance.csv
│   │   │       ├── gpt2-xl-legal.csv
│   │   │       └── gpt2-xl-medical.csv
│   │   ├── olmo
│   │   │   ├── OLMo-2-0425-1B
│   │   │   │   ├── OLMo-2-0425-1B-accessibility.csv
│   │   │   │   ├── OLMo-2-0425-1B-commit-sha.md
│   │   │   │   ├── OLMo-2-0425-1B-control.csv
│   │   │   │   ├── OLMo-2-0425-1B-elicitation.md
│   │   │   │   ├── OLMo-2-0425-1B-finance.csv
│   │   │   │   ├── OLMo-2-0425-1B-legal.csv
│   │   │   │   ├── OLMo-2-0425-1B-medical.csv
│   │   │   │   └── OLMo-2-0425-1B.md
│   │   │   ├── OLMo-2-1124-13B
│   │   │   │   ├── OLMo-2-1124-13B-accessibility.csv
│   │   │   │   ├── OLMo-2-1124-13B-commit-sha.md
│   │   │   │   ├── OLMo-2-1124-13B-control.csv
│   │   │   │   ├── OLMo-2-1124-13B-elicitation.md
│   │   │   │   ├── OLMo-2-1124-13B-finance.csv
│   │   │   │   ├── OLMo-2-1124-13B-legal.csv
│   │   │   │   └── OLMo-2-1124-13B-medical.csv
│   │   │   └── OLMo-2-1124-7B
│   │   │       ├── OLMo-2-0425-1B-commit-sha.md
│   │   │       ├── OLMo-2-1124-7B-accessibility.csv
│   │   │       ├── OLMo-2-1124-7B-commit-sha.md
│   │   │       ├── OLMo-2-1124-7B-control.csv
│   │   │       ├── OLMo-2-1124-7B-elicitation.md
│   │   │       ├── OLMo-2-1124-7B-finance.csv
│   │   │       ├── OLMo-2-1124-7B-legal.csv
│   │   │       ├── OLMo-2-1124-7B-medical.csv
│   │   │       ├── commit-sha-OLMo-2-0425-1B.md
│   │   │       └── commit-sha-OLMo-2-1124-7B.md
│   │   └── pythia
│   │       ├── pythia-12b
│   │       │   ├── pythia-12b-accessibility.csv
│   │       │   ├── pythia-12b-control.csv
│   │       │   ├── pythia-12b-elicitation.md
│   │       │   ├── pythia-12b-finance.csv
│   │       │   ├── pythia-12b-legal.csv
│   │       │   └── pythia-12b-medical.csv
│   │       ├── pythia-160m
│   │       │   ├── pythia-160m-accessibility.csv
│   │       │   ├── pythia-160m-control.csv
│   │       │   ├── pythia-160m-elicitation.md
│   │       │   ├── pythia-160m-finance.csv
│   │       │   ├── pythia-160m-legal.csv
│   │       │   └── pythia-160m-medical.csv
│   │       ├── pythia-1b
│   │       │   ├── pythia-1b-accessibility.csv
│   │       │   ├── pythia-1b-control.csv
│   │       │   ├── pythia-1b-elicitation.md
│   │       │   ├── pythia-1b-finance.csv
│   │       │   ├── pythia-1b-legal.csv
│   │       │   └── pythia-1b-medical.csv
│   │       ├── pythia-2.8b
│   │       │   ├── pythia-2.8b-accessibility.csv
│   │       │   ├── pythia-2.8b-control.csv
│   │       │   ├── pythia-2.8b-elicitation.md
│   │       │   ├── pythia-2.8b-finance.csv
│   │       │   ├── pythia-2.8b-legal.csv
│   │       │   └── pythia-2.8b-medical.csv
│   │       ├── pythia-410m
│   │       │   ├── pythia-410m-accessibility.csv
│   │       │   ├── pythia-410m-control.csv
│   │       │   ├── pythia-410m-elicitation.md
│   │       │   ├── pythia-410m-finance.csv
│   │       │   ├── pythia-410m-legal.csv
│   │       │   └── pythia-410m-medical.csv
│   │       └── pythia-6.9b
│   │           ├── pythia-6.9b-accessibility.csv
│   │           ├── pythia-6.9b-control.csv
│   │           ├── pythia-6.9b-elicitation.md
│   │           ├── pythia-6.9b-finance.csv
│   │           ├── pythia-6.9b-legal.csv
│   │           └── pythia-6.9b-medical.csv
│   ├── entropy
│   │   ├── gpt2
│   │   │   ├── gpt2
│   │   │   │   ├── gpt2-accessibility.csv
│   │   │   │   ├── gpt2-control.csv
│   │   │   │   ├── gpt2-entropy.md
│   │   │   │   ├── gpt2-finance.csv
│   │   │   │   ├── gpt2-legal.csv
│   │   │   │   └── gpt2-medical.csv
│   │   │   ├── gpt2-large
│   │   │   │   ├── gpt2-large-accessibility.csv
│   │   │   │   ├── gpt2-large-control.csv
│   │   │   │   ├── gpt2-large-entropy.csv
│   │   │   │   ├── gpt2-large-entropy.md
│   │   │   │   ├── gpt2-large-finance.csv
│   │   │   │   ├── gpt2-large-legal.csv
│   │   │   │   └── gpt2-large-medical.csv
│   │   │   ├── gpt2-medium
│   │   │   │   ├── gpt2-medium-accessibility.csv
│   │   │   │   ├── gpt2-medium-control.csv
│   │   │   │   ├── gpt2-medium-entropy.csv
│   │   │   │   ├── gpt2-medium-entropy.md
│   │   │   │   ├── gpt2-medium-finance.csv
│   │   │   │   ├── gpt2-medium-legal.csv
│   │   │   │   └── gpt2-medium-medical.csv
│   │   │   ├── gpt2-small
│   │   │   │   ├── gpt2-entropy.csv
│   │   │   │   └── gpt2-entropy.md
│   │   │   └── gpt2-xl
│   │   │       ├── gpt2-xl-accessibility.csv
│   │   │       ├── gpt2-xl-control.csv
│   │   │       ├── gpt2-xl-entropy.csv
│   │   │       ├── gpt2-xl-entropy.md
│   │   │       ├── gpt2-xl-finance.csv
│   │   │       ├── gpt2-xl-legal.csv
│   │   │       └── gpt2-xl-medical.csv
│   │   ├── olmo
│   │   │   ├── OLMo-2-0425-1B
│   │   │   │   ├── OLMo-2-0425-1B-accessibility.csv
│   │   │   │   ├── OLMo-2-0425-1B-control.csv
│   │   │   │   ├── OLMo-2-0425-1B-entropy.csv
│   │   │   │   ├── OLMo-2-0425-1B-entropy.md
│   │   │   │   ├── OLMo-2-0425-1B-finance.csv
│   │   │   │   ├── OLMo-2-0425-1B-legal.csv
│   │   │   │   └── OLMo-2-0425-1B-medical.csv
│   │   │   ├── OLMo-2-1124-13B
│   │   │   │   ├── OLMo-2-1124-13B-accessibility.csv
│   │   │   │   ├── OLMo-2-1124-13B-control.csv
│   │   │   │   ├── OLMo-2-1124-13B-entropy.csv
│   │   │   │   ├── OLMo-2-1124-13B-entropy.md
│   │   │   │   ├── OLMo-2-1124-13B-finance.csv
│   │   │   │   ├── OLMo-2-1124-13B-legal.csv
│   │   │   │   └── OLMo-2-1124-13B-medical.csv
│   │   │   └── OLMo-2-1124-7B
│   │   │       ├── OLMo-2-1124-7B-accessibility.csv
│   │   │       ├── OLMo-2-1124-7B-control.csv
│   │   │       ├── OLMo-2-1124-7B-entropy.csv
│   │   │       ├── OLMo-2-1124-7B-entropy.md
│   │   │       ├── OLMo-2-1124-7B-finance.csv
│   │   │       ├── OLMo-2-1124-7B-legal.csv
│   │   │       └── OLMo-2-1124-7B-medical.csv
│   │   └── pythia
│   │       ├── pythia-12b
│   │       │   ├── pythia-12b-accessibility.csv
│   │       │   ├── pythia-12b-control.csv
│   │       │   ├── pythia-12b-elicitation-entropy-binding.md
│   │       │   ├── pythia-12b-entropy.csv
│   │       │   ├── pythia-12b-entropy.md
│   │       │   ├── pythia-12b-finance.csv
│   │       │   ├── pythia-12b-legal.csv
│   │       │   └── pythia-12b-medical.csv
│   │       ├── pythia-160m
│   │       │   ├── pythia-160m-accessibility.csv
│   │       │   ├── pythia-160m-control.csv
│   │       │   ├── pythia-160m-elicitation-entropy-binding.md
│   │       │   ├── pythia-160m-entropy.csv
│   │       │   ├── pythia-160m-entropy.md
│   │       │   ├── pythia-160m-finance.csv
│   │       │   ├── pythia-160m-legal.csv
│   │       │   └── pythia-160m-medical.csv
│   │       ├── pythia-1b
│   │       │   ├── pythia-1b-accessibility.csv
│   │       │   ├── pythia-1b-entropy.csv
│   │       │   └── pythia-1b-entropy.md
│   │       ├── pythia-2.8b
│   │       │   ├── pythia-2.8b-accessibility.csv
│   │       │   ├── pythia-2.8b-control.csv
│   │       │   ├── pythia-2.8b-entropy.csv
│   │       │   ├── pythia-2.8b-entropy.md
│   │       │   ├── pythia-2.8b-finance.csv
│   │       │   ├── pythia-2.8b-legal.csv
│   │       │   └── pythia-2.8b-medical.csv
│   │       ├── pythia-410m
│   │       │   ├── pythia-410m-accessibility.csv
│   │       │   ├── pythia-410m-control.csv
│   │       │   ├── pythia-410m-elicitation-entropy-binding.md
│   │       │   ├── pythia-410m-entropy.csv
│   │       │   ├── pythia-410m-entropy.md
│   │       │   ├── pythia-410m-finance.csv
│   │       │   ├── pythia-410m-legal.csv
│   │       │   └── pythia-410m-medical.csv
│   │       └── pythia-6.9b
│   │           ├── pythia-6.9b-accessibility.csv
│   │           ├── pythia-6.9b-control.csv
│   │           ├── pythia-6.9b-elicitation-entropy-binding.md
│   │           ├── pythia-6.9b-entropy.csv
│   │           ├── pythia-6.9b-entropy.md
│   │           ├── pythia-6.9b-finance.csv
│   │           ├── pythia-6.9b-legal.csv
│   │           └── pythia-6.9b-medical.csv
│   ├── frequency
│   │   ├── compound_accuracy_table.csv
│   │   ├── frequency_table.csv
│   │   ├── gpt2
│   │   │   ├── gpt2-large_alt_text_competition.csv
│   │   │   ├── gpt2-large_closed_captions_competition.csv
│   │   │   ├── gpt2-large_color_contrast_competition.csv
│   │   │   ├── gpt2-large_focus_indicator_competition.csv
│   │   │   ├── gpt2-large_keyboard_navigation_competition.csv
│   │   │   ├── gpt2-large_screen_reader_competition.csv
│   │   │   ├── gpt2-large_semantic_html_competition.csv
│   │   │   ├── gpt2-large_skip_link_competition.csv
│   │   │   ├── gpt2-medium_alt_text_competition.csv
│   │   │   ├── gpt2-medium_closed_captions_competition.csv
│   │   │   ├── gpt2-medium_color_contrast_competition.csv
│   │   │   ├── gpt2-medium_focus_indicator_competition.csv
│   │   │   ├── gpt2-medium_keyboard_navigation_competition.csv
│   │   │   ├── gpt2-medium_screen_reader_competition.csv
│   │   │   ├── gpt2-medium_semantic_html_competition.csv
│   │   │   ├── gpt2-medium_skip_link_competition.csv
│   │   │   ├── gpt2-xl_alt_text_competition.csv
│   │   │   ├── gpt2-xl_closed_captions_competition.csv
│   │   │   ├── gpt2-xl_color_contrast_competition.csv
│   │   │   ├── gpt2-xl_focus_indicator_competition.csv
│   │   │   ├── gpt2-xl_keyboard_navigation_competition.csv
│   │   │   ├── gpt2-xl_screen_reader_competition.csv
│   │   │   ├── gpt2-xl_semantic_html_competition.csv
│   │   │   ├── gpt2-xl_skip_link_competition.csv
│   │   │   ├── gpt2_alt_text_competition.csv
│   │   │   ├── gpt2_closed_captions_competition.csv
│   │   │   ├── gpt2_color_contrast_competition.csv
│   │   │   ├── gpt2_focus_indicator_competition.csv
│   │   │   ├── gpt2_keyboard_navigation_competition.csv
│   │   │   ├── gpt2_screen_reader_competition.csv
│   │   │   ├── gpt2_semantic_html_competition.csv
│   │   │   └── gpt2_skip_link_competition.csv
│   │   ├── gpt2_frequency_trajectory.csv
│   │   ├── olmo
│   │   │   ├── OLMo-2-0425-1B-results (1).csv
│   │   │   ├── OLMo-2-0425-1B-results.csv
│   │   │   ├── OLMo-2-0425-1B_spearman_merged.csv
│   │   │   ├── OLMo-2-0425-1B_spearman_result.md
│   │   │   ├── OLMo-2-1124-13B-results.csv
│   │   │   ├── OLMo-2-1124-13B_spearman_merged.csv
│   │   │   ├── OLMo-2-1124-13B_spearman_result.md
│   │   │   ├── OLMo-2-1124-7B-results.csv
│   │   │   ├── OLMo-2-1124-7B_spearman_merged.csv
│   │   │   ├── OLMo-2-1124-7B_spearman_result.md
│   │   │   └── olmo_spearman_partial.csv
│   │   ├── pythia
│   │   │   ├── pythia-12B_alt_text_competition.csv
│   │   │   ├── pythia-12B_closed_captions_competition.csv
│   │   │   ├── pythia-12B_color_contrast_competition.csv
│   │   │   ├── pythia-12B_focus_indicator_competition.csv
│   │   │   ├── pythia-12B_keyboard_navigation_competition.csv
│   │   │   ├── pythia-12B_screen_reader_competition.csv
│   │   │   ├── pythia-12B_semantic_html_competition.csv
│   │   │   ├── pythia-12B_skip_link_competition.csv
│   │   │   ├── pythia-160m_alt_text_competition.csv
│   │   │   ├── pythia-160m_closed_captions_competition.csv
│   │   │   ├── pythia-160m_color_contrast_competition.csv
│   │   │   ├── pythia-160m_focus_indicator_competition.csv
│   │   │   ├── pythia-160m_keyboard_navigation_competition.csv
│   │   │   ├── pythia-160m_screen_reader_competition.csv
│   │   │   ├── pythia-160m_semantic_html_competition.csv
│   │   │   ├── pythia-160m_skip_link_competition.csv
│   │   │   ├── pythia-1b_alt_text_competition.csv
│   │   │   ├── pythia-1b_closed_captions_competition.csv
│   │   │   ├── pythia-1b_color_contrast_competition.csv
│   │   │   ├── pythia-1b_focus_indicator_competition.csv
│   │   │   ├── pythia-1b_keyboard_navigation_competition.csv
│   │   │   ├── pythia-1b_screen_reader_competition.csv
│   │   │   ├── pythia-1b_semantic_html_competition.csv
│   │   │   ├── pythia-1b_skip_link_competition.csv
│   │   │   ├── pythia-2.8b_alt_text_competition.csv
│   │   │   ├── pythia-2.8b_closed_captions_competition.csv
│   │   │   ├── pythia-2.8b_color_contrast_competition.csv
│   │   │   ├── pythia-2.8b_focus_indicator_competition.csv
│   │   │   ├── pythia-2.8b_keyboard_navigation_competition.csv
│   │   │   ├── pythia-2.8b_screen_reader_competition.csv
│   │   │   ├── pythia-2.8b_semantic_html_competition.csv
│   │   │   ├── pythia-2.8b_skip_link_competition.csv
│   │   │   ├── pythia-410m_alt_text_competition.csv
│   │   │   ├── pythia-410m_closed_captions_competition.csv
│   │   │   ├── pythia-410m_color_contrast_competition.csv
│   │   │   ├── pythia-410m_focus_indicator_competition.csv
│   │   │   ├── pythia-410m_keyboard_navigation_competition.csv
│   │   │   ├── pythia-410m_screen_reader_competition.csv
│   │   │   ├── pythia-410m_semantic_html_competition.csv
│   │   │   ├── pythia-410m_skip_link_competition.csv
│   │   │   ├── pythia-6.9B_alt_text_competition.csv
│   │   │   ├── pythia-6.9B_closed_captions_competition.csv
│   │   │   ├── pythia-6.9B_color_contrast_competition.csv
│   │   │   ├── pythia-6.9B_focus_indicator_competition.csv
│   │   │   ├── pythia-6.9B_keyboard_navigation_competition.csv
│   │   │   ├── pythia-6.9B_screen_reader_competition.csv
│   │   │   ├── pythia-6.9B_semantic_html_competition.csv
│   │   │   └── pythia-6.9B_skip_link_competition.csv
│   │   ├── pythia_frequency_trajectory.csv
│   │   ├── scorecard_base_rate.csv
│   │   ├── spearman_accuracy.csv
│   │   ├── spearman_kendall.csv
│   │   ├── spearman_partial.csv
│   │   ├── spearman_pmi_robustness.csv
│   │   ├── spearman_rowlevel_bootstrap.csv
│   │   ├── spearman_secondary_sensitivity.csv
│   │   └── spearman_summary.csv
│   ├── logits
│   │   ├── REGEN_DIVERGENCE.md
│   │   ├── gpt2
│   │   │   ├── gpt2-large_alt_text_because_ranks.csv
│   │   │   ├── gpt2-large_alt_text_because_steps.csv
│   │   │   ├── gpt2-large_because_generations.csv
│   │   │   ├── gpt2-large_screen_reader_because_ranks.csv
│   │   │   ├── gpt2-large_screen_reader_because_steps.csv
│   │   │   ├── gpt2-large_skip_link_because_ranks.csv
│   │   │   ├── gpt2-large_skip_link_because_steps.csv
│   │   │   ├── gpt2-medium_alt_text_because_ranks.csv
│   │   │   ├── gpt2-medium_alt_text_because_steps.csv
│   │   │   ├── gpt2-medium_because_generations.csv
│   │   │   ├── gpt2-medium_screen_reader_because_ranks.csv
│   │   │   ├── gpt2-medium_screen_reader_because_steps.csv
│   │   │   ├── gpt2-medium_skip_link_because_ranks.csv
│   │   │   ├── gpt2-medium_skip_link_because_steps.csv
│   │   │   ├── gpt2-xl_alt_text_because_ranks.csv
│   │   │   ├── gpt2-xl_alt_text_because_steps.csv
│   │   │   ├── gpt2-xl_because_generations.csv
│   │   │   ├── gpt2-xl_screen_reader_because_ranks.csv
│   │   │   ├── gpt2-xl_screen_reader_because_steps.csv
│   │   │   ├── gpt2-xl_skip_link_because_ranks.csv
│   │   │   └── gpt2-xl_skip_link_because_steps.csv
│   │   └── pythia
│   │       ├── pythia-12b_alt_text_because_ranks.csv
│   │       ├── pythia-12b_alt_text_because_steps.csv
│   │       ├── pythia-12b_because_generations.csv
│   │       ├── pythia-12b_screen_reader_because_ranks.csv
│   │       ├── pythia-12b_screen_reader_because_steps.csv
│   │       ├── pythia-12b_skip_link_because_ranks.csv
│   │       ├── pythia-12b_skip_link_because_steps.csv
│   │       ├── pythia-160m_alt_text_because_ranks.csv
│   │       ├── pythia-160m_alt_text_because_steps.csv
│   │       ├── pythia-160m_because_generations.csv
│   │       ├── pythia-160m_screen_reader_because_ranks.csv
│   │       ├── pythia-160m_screen_reader_because_steps.csv
│   │       ├── pythia-160m_skip_link_because_ranks.csv
│   │       ├── pythia-160m_skip_link_because_steps.csv
│   │       ├── pythia-1b_alt_text_because_ranks.csv
│   │       ├── pythia-1b_alt_text_because_steps.csv
│   │       ├── pythia-1b_because_generations.csv
│   │       ├── pythia-1b_screen_reader_because_ranks.csv
│   │       ├── pythia-1b_screen_reader_because_steps.csv
│   │       ├── pythia-1b_skip_link_because_ranks.csv
│   │       ├── pythia-1b_skip_link_because_steps.csv
│   │       ├── pythia-2.8b_alt_text_because_ranks.csv
│   │       ├── pythia-2.8b_alt_text_because_steps.csv
│   │       ├── pythia-2.8b_because_generations.csv
│   │       ├── pythia-2.8b_screen_reader_because_ranks.csv
│   │       ├── pythia-2.8b_screen_reader_because_steps.csv
│   │       ├── pythia-2.8b_skip_link_because_ranks.csv
│   │       ├── pythia-2.8b_skip_link_because_steps.csv
│   │       ├── pythia-410m_alt_text_because_ranks.csv
│   │       ├── pythia-410m_alt_text_because_steps.csv
│   │       ├── pythia-410m_because_generations.csv
│   │       ├── pythia-410m_screen_reader_because_ranks.csv
│   │       ├── pythia-410m_screen_reader_because_steps.csv
│   │       ├── pythia-410m_skip_link_because_ranks.csv
│   │       ├── pythia-410m_skip_link_because_steps.csv
│   │       ├── pythia-6.9b_alt_text_because_ranks.csv
│   │       ├── pythia-6.9b_alt_text_because_steps.csv
│   │       ├── pythia-6.9b_because_generations.csv
│   │       ├── pythia-6.9b_screen_reader_because_ranks.csv
│   │       ├── pythia-6.9b_screen_reader_because_steps.csv
│   │       ├── pythia-6.9b_skip_link_because_ranks.csv
│   │       └── pythia-6.9b_skip_link_because_steps.csv
│   ├── olmo
│   │   ├── OLMo-2-0425-1B_spearman_merged.csv
│   │   ├── OLMo-2-0425-1B_spearman_result.md
│   │   ├── OLMo-2-1124-13B-results.csv
│   │   └── OLMo-2-1124-7B-results.csv
│   └── peak_regress_lens.csv
└── src
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-311.pyc
    │   ├── __init__.cpython-313.pyc
    │   ├── accuracy_coding.cpython-311.pyc
    │   ├── analysis.cpython-311.pyc
    │   ├── binding.cpython-311.pyc
    │   ├── closeout_followups.cpython-311.pyc
    │   ├── d6_multihead_ablation.cpython-311.pyc
    │   ├── d8_frequency_prior.cpython-313.pyc
    │   ├── dual_spearman.cpython-311.pyc
    │   ├── elicitation.cpython-311.pyc
    │   ├── entropy.cpython-311.pyc
    │   ├── frequency.cpython-311.pyc
    │   ├── frequency.cpython-313.pyc
    │   ├── gap_analysis.cpython-311.pyc
    │   ├── head_characterization.cpython-311.pyc
    │   ├── logit_export.cpython-311.pyc
    │   ├── manifest.cpython-311.pyc
    │   ├── models.cpython-311.pyc
    │   ├── olmo_config.cpython-311.pyc
    │   ├── qk_ov.cpython-311.pyc
    │   ├── tangent_byte_compare.cpython-311.pyc
    │   ├── tl217_olmo2_adapter.cpython-311.pyc
    │   └── tl2_olmo2_adapter.cpython-311.pyc
    ├── accuracy_coding.py
    ├── analysis.py
    ├── binding.py
    ├── closeout_followups.py
    ├── d6_multihead_ablation.py
    ├── d7_token_ban.py
    ├── d8_frequency_prior.py
    ├── decompose.py
    ├── dual_spearman.py
    ├── elicitation.py
    ├── entropy.py
    ├── frequency.py
    ├── gap_analysis.py
    ├── head_characterization.py
    ├── heads.py
    ├── logit_export.py
    ├── logit_lens.py
    ├── manifest.py
    ├── models.py
    ├── olmo_config.py
    ├── perplexity.py
    ├── probe.py
    ├── qk_ov.py
    ├── tangent_byte_compare.py
    ├── tl217_olmo2_adapter.py
    └── viz.py

90 directories, 691 files