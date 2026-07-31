## The Behavioral Gap

A model that correctly defines an accessibility concept when asked directly can fail completely when asked to apply it — and the two abilities scale differently. The difference between declarative accuracy and evaluative accuracy is the declarative-evaluative gap. This section establishes it behaviorally across both model families.

**Setup.** All five investigations in this paper share one environment, declared here once; each later section states its own instrument where it is used. The models are six Pythia scales (160M, 410M, 1B, 2.8B, 6.9B, 12B) and four GPT-2 scales (124M, 355M, 774M, 1.5B), all base models, generating greedily. Corpus frequency is measured with Infini-gram against The Pile — exact for Pythia, a labeled cross-corpus proxy for GPT-2 (Section 4). The behavioral instrument is an elicitation battery: matched declarative and evaluative prompts per concept, plus a small completion battery across four concepts (n = 8 per scale). Responses are coded by deterministic, version-controlled criteria. All 510 responses were coded; every change to the criteria is recorded in the decision log before it takes effect.

Two cuts of the coded data appear in this paper: the gap series, computed on the concepts that appear in both the declarative and evaluative batteries, and the full-battery view, which scores every response as binary correct or incorrect. Both views find the gap at nine of ten model-scale points; at Pythia-12B, declarative accuracy declines to meet evaluative failure and the gap closes. Whether that decline appears in the aggregate depends on which concepts are in the denominator — but per-concept, the regression is unambiguous, and the trajectory claims that follow are made at that resolution.

Writing $a_d(c,s)$ and $a_e(c,s)$ for a concept's declarative and evaluative accuracy at scale $s$, the gap at each scale is the difference of matched-set means:

$$\Delta(s) = \overline{a_d}(s) - \overline{a_e}(s).$$

The completion-paradox claim is a direction, tested as one: completion accuracy exceeds declarative accuracy at all ten suite-by-scale points (sign test, p ≈ .001).

Every threshold in this paper was committed to the repository before its result was computed, and every intervention was gated on first reproducing the observation it targets.

The gap is real in both model-families and behaves differently in each. In GPT-2 it widens with scale, reaching 50 points at 1.5B — declarative knowledge accumulates faster than the ability to deploy it. In Pythia it persists at every scale with one exception, and the exception is the finding. At 12B the gap closes because declarative accuracy decreases to meet evaluative accuracy, not because evaluative accuracy rises. Convergence by decay is not mastery.

One generation pair makes this concrete. Pythia-2.8B asked declaratively: "A skip link is a link that is used to skip a section of a web page." The same model asked evaluatively why a long navigation menu without a skip link is not accessible: "because the skip link is not present." Both sentences are fluent. Only one contains the concept doing work. The evaluative answer is a tautology — the words arranged in the shape of a reason, with the reasoning absent.

The completion battery reveals a second dimension: syntactic form is learned before declarative content. Pythia-160M generates a well-formed alt attribute in 100% of completion prompts but scores 0% on defining alt text. The direction is consistent across both model families at every scale tested (sign test, p ≈ .001). The battery is small and exploratory in origin because the coding criteria were authored after the data were collected. It establishes the existence and direction of the effect, not its magnitude. It was subsequently recovered in blind analysis without access to this hypothesis.

The gap has internal structure that accuracy numbers alone do not show. Models enter distinct failure states depending on how they are asked, and the character of evaluative failure changes as models scale. A single corpus statistic — the bigram frequency of each compound in the training data — predicts which concepts take which path.
