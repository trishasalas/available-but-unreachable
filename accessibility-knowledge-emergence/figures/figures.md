# Figures Titles and Captions

## Figure 1

Filename: `binding-behavior.png`
Location: Introduction
Title: Binding Depth and Behavioral Emergence Follow the Same Shape
Caption: Binding depth and behavioral emergence score rise at the same 2.8B parameter threshold across the Pythia model suite. Binding depth = last strong layer (≥0.5) / total layers. Behavioral emergence score = mean across five concepts (correct=1, partial=0.5, incorrect=0). ARIA scores negative at 1B–6.9B reflecting fluent confabulation rather than absence of response.
Alt Text: Line graph with two lines plotted across four Pythia model sizes (410M, 1B, 2.8B, 6.9B). Navy solid line shows binding depth rising sharply at 2.8B. Light blue dashed line shows behavioral emergence score following the same shape, also rising at 2.8B. Both lines are flat or declining before 2.8B and rise together after. A dashed vertical marker labels the 2.8B emergence threshold. An annotation at 6.9B notes ARIA confabulation depresses the behavioral score.

## Figure 2

Filename: `pythia-perplexity.png`
Location: Results > Experiment 3
Title: Recognition Precedes Generation — Pythia
Caption: Correct definition perplexity falls below wrong definition perplexity at the 1B threshold in Pythia, indicating the model finds the correct definition more expected before it can generate it.
Alt Text: Line graph across five Pythia model sizes (160M to 6.9B). Navy line (correct definition) and light blue line (wrong definition) begin close together at 160M and cross between 410M and 1B. After crossing, the correct definition line stays consistently lower. A shaded region marks the flip zone between 410M and 1B.

## Figure 3

Filename: `gpt2-perplexity.png`
Location: Results > Experiment 3
Title: Recognition Precedes Generation — GPT-2
Caption: GPT-2 shows a less clean crossing than Pythia — the flip zone spans Medium through XL, possibly reflecting differences in how preference emerges across architectures and training regimes.
Alt Text: Line graph across four GPT-2 model sizes (Small 117M to XL 1.5B). Navy line (correct definition) and light blue line (wrong definition) track closely through Medium and Large before diverging at XL. The crossing is ambiguous through the middle range. A wider shaded flip zone spans Medium through XL.

## Figure 4

Filename: `binding-persistence.png`
Location: Results > Experiment 4
Title: Binding Persistence by Model Scale
Caption: Strong binding heads persist to the final network layers only above the 2.8B emergence threshold, suggesting late-layer sustained binding is a mechanistic correlate of behavioral emergence.
Alt Text: Bar chart with five bars for Pythia model sizes 160M through 6.9B. Light blue bars for 160M, 410M, and 1B show last strong binding layer at 11, 9, and 6 respectively. Navy bars for 2.8B and 6.9B jump to layers 29 and 30. A dashed vertical line between 1B and 2.8B marks the emergence threshold.

## Figure 5

Filename: `compound-comparison.png`
Location: Results > Experiment 4
Title: Binding Generalizes Across Accessibility Compounds
Caption: Binding generalizes across all three accessibility compounds at 2.8B, with alt text and skip link activating more heads than screen reader but all three showing strong head counts above threshold.
Alt Text: Grouped bar chart with three concept pairs: screen reader, alt text, and skip link. Each group has two bars — light blue for all heads above 0.1 (101, 200, 208) and navy for strong heads above 0.5 (25, 40, 40). Alt text and skip link show substantially more binding heads than screen reader in both categories.
