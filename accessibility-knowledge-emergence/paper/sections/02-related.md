## Related Work

**Emergence in language models.** Wei et al. (2022) established that language models exhibit emergent abilities --- capabilities that appear
sharply at specific parameter scales rather than improving gradually. We treat accessibility concept acquisition as a domain-specific case study
of emergence, using the Pythia suite's controlled architecture to isolate scale as the variable of interest. 

**Knowledge representation in transformers.** Geva et al. (2021) demonstrated that feed-forward layers in transformers function as
key-value memories, storing factual associations that attention heads retrieve and route. Subsequent work by Yao et al. (2024) mapped
knowledge circuits in GPT-2 Medium using factual recall tasks, noting explicitly that their findings "may not be universally applicable to all
knowledge domains." We examine whether domain-specific, low-frequency knowledge follows the same patterns.

**Attention as an interpretability tool.** Clark et al. (2019) showed that attention patterns in BERT encode linguistically meaningful
relationships, establishing attention visualization as a valid method
for probing internal representations. We apply the same approach to
compound accessibility terms, asking whether models bind multi-token
concepts as units.

**Mechanistic interpretability.** Olsson et al. (2022) characterized
induction circuits and previous-token heads in transformer models,
providing the framework used here to interpret early-layer binding
patterns. The distinction between positional binding mechanisms and
representational binding --- central to the control analysis --- draws
directly on their circuit taxonomy.

**AI and digital accessibility.** A growing body of work applies AI to
accessibility tasks --- generating alt text, detecting contrast
failures, automating WCAG audits. We take the inverse approach: rather
than using AI as an accessibility tool, we examine what AI systems
actually know about accessibility and when that knowledge emerges.
