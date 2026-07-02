## Appendix


### SUGGESTION: Related work framing

This section should be restructured as proper related work rather than an appendix. The reference list in 10-references.md provides the organized source material. The narrative should establish three things:

1. **Frequency bias is well-documented** (Giulianelli, Chen, Kandpal, Razeghi, Mallen). Prior work establishes that models favor high-frequency tokens and that training data frequency predicts factual recall. These studies operate at the behavioral/benchmark level.

2. **Internal knowledge can exceed output behavior** (Patel et al., SPARK). Linear probes show models encode knowledge they don't output. SPARK calls it "statistical pressure toward common training-distribution patterns." These studies document the gap but don't explain the mechanism at the token level.

3. **AI for accessibility is tool-focused** (Fuglerud, López-Gil). The field asks "can AI test for accessibility" not "what does AI know about accessibility and how." Nobody has examined accessibility knowledge mechanistically.

Your paper sits at the intersection: you take the documented frequency effect, show the documented internal-vs-output gap, and connect them mechanistically in a domain nobody else is examining at this level.