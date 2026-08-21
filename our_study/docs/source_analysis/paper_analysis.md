# SeSE Paper Analysis

## Source

**Title:** SeSE: Black-Box Uncertainty Quantification for Large Language Models Based on Structural Information Theory

**Authors:** Xingtao Zhao, Hao Peng, Dingli Su, Xianghua Zeng, Chunyang Liu, Jinzhi Liao, Philip S. Yu

**Venue:** Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence (UAI 2026)

**Reference:** PMLR Volume 337, pages 8209–8237

---

# 1. Research Problem

## 1.1 Problem

Large language models can produce plausible but incorrect responses.

Uncertainty quantification attempts to estimate when an LLM is likely to be unreliable so that uncertain outputs can potentially be rejected or verified.

## 1.2 Limitation Identified by SeSE

The authors argue that existing semantic uncertainty methods primarily represent semantic uncertainty using distributions or pairwise relationships and do not sufficiently capture the latent hierarchical structure of the semantic space.

They also identify limited granularity for uncertainty estimation in long-form outputs containing multiple interwoven claims.

## 1.3 Proposed Solution

SeSE introduces Semantic Structural Entropy, which represents the semantic space as a graph and constructs an optimal hierarchical abstraction using structural entropy minimization.

---

# 2. Core Idea

## 2.1 Semantic Space

For short-form generation, multiple responses to the same query are represented as nodes in a semantic graph.

## 2.2 Directed Semantic Relationships

Relationships between responses are estimated using Natural Language Inference.

The resulting graph is directed and weighted.

## 2.3 Hierarchical Structure

Instead of treating semantic clusters as a flat distribution, SeSE constructs a hierarchical encoding tree.

## 2.4 Structural Entropy

The structural entropy of the optimized encoding tree is used as the uncertainty score.

Higher SeSE corresponds to greater estimated uncertainty.

---

# 3. Short-Form Pipeline

The short-form methodology consists of three major stages:

1. Response sampling
2. Semantic graph construction
3. Hierarchical abstraction

## 3.1 Response Sampling

For a query x:

- Generate a greedy response.
- Generate multiple stochastic responses.
- Use the sampled responses to characterize the model's semantic response space.

### Parameters

- Number of stochastic samples: N
- Sampling temperature
- Model
- Dataset/task

_To be filled with exact experimental settings._

---

## 3.2 Semantic Graph Construction

Each sampled response is represented as a graph node.

A Natural Language Inference model estimates directed semantic relationships between responses.

The graph is weighted according to the inferred semantic relationship.

### Key Question

Why is a directed graph preferable to a simple similarity graph?

_To be answered from the paper._

---

## 3.3 Hierarchical Abstraction

SeSE constructs an encoding tree over the semantic graph.

The objective is to minimize structural entropy.

The resulting optimized tree represents a hierarchical organization of the semantic space.

### Tree Height

K controls the depth of the hierarchical abstraction.

The effect of K must be analyzed carefully because it is a methodological hyperparameter.

---

# 4. Long-Form Pipeline

Long-form generation contains multiple potentially independent claims.

SeSE extends the framework to estimate uncertainty at the claim level.

## 4.1 Claim Decomposition

A long-form response is decomposed into atomic claims.

## 4.2 Claim-Response Graph

A bipartite graph is constructed containing:

- sampled responses
- extracted claims

Semantic entailment relationships connect responses and claims.

## 4.3 Claim-Level Uncertainty

The uncertainty of a claim is calculated using the structural entropy associated with its position in the optimized encoding tree.

This produces fine-grained uncertainty estimates for individual claims.

---

# 5. Theoretical Positioning

The authors state that SeSE generalizes Semantic Entropy.

When the encoding tree is restricted to a single layer (K = 1), SeSE recovers semantic entropy.

This is important because SeSE can be interpreted as extending a flat semantic uncertainty representation into a hierarchical representation.

---

# 6. Evaluation

## 6.1 Datasets

_To be extracted exactly from the paper._

## 6.2 Models

_To be extracted exactly from the paper._

## 6.3 Baselines

_To be extracted exactly from the paper._

## 6.4 Metrics

The main uncertainty evaluation metrics include:

- AUROC
- AURAC

### AUROC

Measures the ability of an uncertainty estimator to distinguish correct from incorrect outputs.

### AURAC

Measures the relationship between uncertainty-based rejection and remaining accuracy.

---

# 7. Main Experimental Claim

The paper reports that SeSE outperforms the evaluated uncertainty baselines across 24 model–dataset combinations.

This claim must be separated from the broader question of whether SeSE is reliable under conditions not covered or not deeply analyzed by the original experiments.

---

# 8. Ablation / Sensitivity Questions

The paper investigates methodological parameters including:

- number of sampled responses;
- encoding tree height;
- model;
- dataset.

These experiments are important because they may reveal whether SeSE's performance depends on particular configuration choices.

---

# 9. What SeSE Establishes

_To be completed after detailed paper analysis._

---

# 10. What SeSE Does Not Establish

This section must be evidence-based.

Potential questions include:

- Calibration of SeSE as an actual probability of correctness.
- Robustness to different error mechanisms.
- Generalization to tasks outside the evaluated benchmark distribution.
- Stability under changes in generation settings.
- Relationship between uncertainty and response complexity.
- Whether uncertainty failures have identifiable structural causes.

These are hypotheses/questions, not established limitations.

---

# 11. Candidate Research Gaps

A candidate gap becomes part of our research only if detailed analysis confirms that the original work does not already answer it adequately.

Potential directions:

### A. Reliability Across Error Types

Does SeSE behave differently for different kinds of incorrect answers?

### B. Calibration

Does a SeSE score correspond consistently to an empirical probability of correctness?

### C. Robustness

How stable is SeSE under changes in sampling, prompt formulation, and generation settings?

### D. Complexity

Does the relationship between SeSE and correctness change with response length or reasoning complexity?

### E. Failure Analysis

What semantic structures cause SeSE to assign low uncertainty to incorrect answers?

### F. Cross-Task Generalization

Does a configuration that works well on one task transfer to other tasks?

---

# 12. Research Design Principle

Our study must not assume that SeSE is flawed.

The study will test competing possibilities:

1. SeSE is robust across conditions.
2. SeSE has systematic weaknesses.
3. SeSE's weaknesses are concentrated in specific conditions.
4. Some weaknesses can be explained by the construction of the semantic graph.
5. An improved methodology may or may not address those weaknesses.

---

# 13. Preliminary Standalone Contribution

The final contribution should be independently understandable without requiring knowledge of the SeSE repository.

The project should contain:

- an independently defined research question;
- explicit hypotheses;
- a reproducible experimental protocol;
- baseline comparisons;
- systematic evaluation;
- failure analysis;
- statistical analysis;
- documented conclusions;
- limitations;
- and, only if justified by evidence, a proposed methodological improvement.

---

# 14. Open Questions

1. What exactly determines SeSE's uncertainty score?
2. How sensitive is the score to sampling?
3. How sensitive is it to the NLI model?
4. How sensitive is it to graph sparsification?
5. How sensitive is it to encoding-tree depth?
6. Does uncertainty remain reliable across different error types?
7. Is the score calibrated?
8. What are the most important failure modes?
9. Can those failure modes be predicted from measurable properties of the semantic graph?
10. Can an improvement be designed from those observations?