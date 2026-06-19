In research, prompts are not just questions; they are **instrumentation tools**. Because LLMs are sensitive to formatting, researchers use specific templates to ensure they are measuring the model's actual knowledge rather than its reaction to a specific word choice.

Here are the primary prompt templates and structural frameworks used in current AI research:

---

### 1. The "Shot-Based" Templates

These are the industry standard for benchmarking. They test how a model learns or retrieves information within its "context window."

* **Zero-Shot (Direct Instruction):** * **Goal:** Measuring baseline "out-of-the-box" knowledge.
* **Template:** `[Task Description] + [Input Data]`
* *Example:* "Translate the following English text to French: 'The cat is on the mat.'"


* **Few-Shot (In-Context Learning):** * **Goal:** Guiding the model toward a specific pattern or output format.
* **Template:** `[Example 1] + [Example 2] + [Target Task]`
* *Example:* * "Input: Great movie! -> Sentiment: Positive"
* "Input: It was okay. -> Sentiment: Neutral"
* "Input: Hated it. -> Sentiment: [Model Output]"





### 2. Reasoning-Focused Templates

Used when testing "emergence" of logical capabilities or solving complex math/code problems.

* **Zero-Shot Chain-of-Thought (CoT):** * **Template:** `[Problem] + "Let's think step by step."`
* **Significance:** Adding this specific phrase was a breakthrough in 2022 (Kojima et al.) because it triggers the model to output intermediate reasoning steps before the final answer.


* **Few-Shot Chain-of-Thought:**
* **Template:** Providing 3-5 examples where the "Answer" section contains a full explanation of the logic.


* **Least-to-Most Prompting:**
* **Template:** `[Decompose the problem into sub-problems] + [Solve each one sequentially].`
* **Significance:** Used for tasks that are too large for a single "reasoning hop."



### 3. Evaluation & Guardrail Templates

Researchers use these when they are using an LLM to grade another LLM (LLM-as-a-Judge).

* **The "Rubric-Based" Template:**
* **Structure:**
1. **System Persona:** "You are an expert evaluator."
2. **The Response:** `[Model A's output]`
3. **The Rubric:** "Score on a scale of 1-5 for accuracy, helpfulness, and tone."
4. **Justification Request:** "Explain your score before providing the final number."




* **Constitutional / AI Feedback (RLAIF):**
* **Template:** `[Draft Response] + "Critique this response against the following principles: [Principle X]. Now rewrite it."`



### 4. Semantic & Mechanistic Probes (The "Cloze" Task)

Since you are working with **TransformerLens**, you likely use this template often. It is used to isolate exactly where a concept is "retrieved" in the layers.

* **Cloze Template:**
* **Structure:** `[Prefix] + [Hidden Token]`
* *Example:* "The capital of France is [MASK]."
* **Research Use:** Researchers measure the log-probability of the correct token compared to incorrect ones across different model sizes (exactly what you did in Experiment 3).



### 5. Structured Output Templates

For code or data extraction research, where the model's fluency can interfere with the data.

* **JSON/Markdown Enforcer:**
* **Template:** `[Instructions] + "Return the response strictly in the following JSON format: { 'concept': '', 'definition': '', 'confidence': 0-1 }"`



---

### Key Research Best Practices

When drafting your paper, you should explicitly state which of these you used. For example:

> *"We utilized a **zero-shot completion template** for Experiment 1 and a **log-probability cloze task** for Experiment 3 to ensure result comparability across the Pythia suite."*

**Would you like me to rewrite your "Methodology" section to use this more formal academic terminology?**