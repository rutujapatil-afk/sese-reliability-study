# SeSE Code Analysis

## Purpose

This document reconstructs the actual computational pipeline implemented by the original SeSE repository.

The objective is to understand the implementation independently of the paper's high-level description.

The original repository is reference material and will not be modified.

---

# 1. Short-Form Entry Points

Directory:

`../original_work/SeSE/sentence_structural_entropy/`

Main files:

- `sample_answers.py`
- `uncertainty_quantification.py`
- `analyze_results.py`

Supporting implementation:

- `src/`

---

# 2. High-Level Computational Pipeline

The short-form implementation can be represented as:

Query
↓
Generated responses
↓
Response selection
↓
Semantic relationship inference
↓
Semantic graph
↓
Structural entropy
↓
Uncertainty score
↓
Correctness comparison / evaluation

---

# 3. Response Sampling

Implementation:

`sample_answers.py`

Questions to answer:

1. Which model generates the responses?
2. How many responses are generated?
3. What decoding strategy is used?
4. What temperature is used?
5. Is the first/most-likely response treated differently?
6. Are random seeds controlled?
7. Are token log-likelihoods retained?
8. What information is stored for each response?

Findings:

_To be completed._

---

# 4. Uncertainty Quantification

Implementation:

`uncertainty_quantification.py`

The implementation loads generated responses and computes multiple uncertainty measures.

Relevant measures include:

- length-normalized entropy;
- semantic entropy;
- structural entropy.

---

# 5. Response Selection

The implementation supports selecting either:

- all available generations; or
- a configured number of generations.

Questions:

1. Does changing the number of generations change the graph itself?
2. Does it change only the entropy calculation?
3. How does the implementation handle the most-likely response?
4. Is the same subset used for all uncertainty measures?

Findings:

_To be completed._

---

# 6. Semantic Relationship Construction

The implementation supports different entailment/semantic approaches.

Relevant components include:

- DeBERTa-based entailment;
- GPT-4o-based entailment;
- AMSC semantic clustering;
- semantic graph construction.

Questions:

1. What exactly constitutes an edge?
2. Is the graph directed?
3. How are edge weights calculated?
4. What threshold is used?
5. Does the question itself affect edge construction?
6. How sensitive is the final score to the semantic relationship model?

Findings:

_To be completed._

---

# 7. Semantic Graph

Implementation:

`src/uncertainty_measures/construct_semantic_graph.py`

Questions:

1. What are the graph nodes?
2. What are the graph edges?
3. What does edge weight represent?
4. Is the graph sparse or dense?
5. Is the graph symmetric?
6. Are self-edges used?
7. Are disconnected nodes possible?
8. Is graph normalization performed?

Findings:

_To be completed._

---

# 8. Structural Entropy

Implementation:

`src/uncertainty_measures/structural_entropy.py`

Questions:

1. What mathematical quantity is computed?
2. What probability distribution is used?
3. How is the encoding tree constructed?
4. Is the tree optimized?
5. What determines the tree depth?
6. What information from the original semantic graph is retained?
7. What information is discarded when producing the final scalar score?

Findings:

_To be completed._

---

# 9. Final Uncertainty Score

The structural entropy calculation produces a scalar uncertainty value.

Questions:

1. Is the value normalized?
2. Is it comparable across queries?
3. Is it comparable across datasets?
4. Is it comparable across models?
5. Is it a probability?
6. Is it only meaningful for ranking examples?
7. Does the implementation transform the raw score before evaluation?

Findings:

_To be completed._

---

# 10. Ground-Truth Correctness

The implementation retains correctness information for the most-likely answer.

Questions:

1. How is correctness determined?
2. Is correctness binary?
3. Is partial correctness possible?
4. How are unanswerable questions handled?
5. Does the correctness label correspond to the same response whose uncertainty is measured?

Findings:

_To be completed._

---

# 11. Evaluation

Implementation:

`analyze_results.py`

Questions:

1. Which metrics are computed?
2. How is AUROC calculated?
3. How is AURAC calculated?
4. Are uncertainty scores inverted before evaluation?
5. Are confidence intervals reported?
6. Are statistical significance tests performed?
7. Are per-example failures analyzed?

Findings:

_To be completed._

---

# 12. Information Flow

Important information flow to investigate:

Generated responses
→ semantic relationships
→ graph
→ structural entropy
→ scalar uncertainty

Potentially discarded information:

- individual semantic relationships;
- graph topology;
- cluster structure;
- response-level disagreement;
- hierarchy information;
- local graph properties.

Whether this information is actually discarded, and at what stage, must be verified from the implementation.

---

# 13. Potential Research Significance

If the implementation compresses a rich semantic graph into a single scalar uncertainty value, an important research question may be:

> Can information contained in the intermediate semantic structure explain or predict cases where the final uncertainty score fails?

This is only a hypothesis at this stage.

It must not be treated as a finding until the implementation has been fully analyzed.

---

# 14. Implementation Questions Requiring Verification

1. What exactly is `build_semantic_graph()` doing?
2. What exactly is `compute_se()` doing?
3. What exactly does the NLI model output?
4. How are NLI outputs converted into graph weights?
5. How does graph structure affect structural entropy?
6. What happens to graph information after entropy calculation?
7. Which parameters can change the graph?
8. Which parameters can change the final score?
9. Which sources of randomness remain uncontrolled?
10. Which intermediate values can we save for later analysis?

---

# 15. Research Direction

Do not modify the original implementation.

The purpose of this analysis is to determine which intermediate representations can be independently analyzed in our study.

Any future implementation should be written under:

`our_study/src/`

and should be clearly distinguished from the original implementation.