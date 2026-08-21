# SeSE Paper Analysis

## Source

**Paper:** SeSE: Black-Box Uncertainty Quantification for Large Language Models Based on Structural Information Theory

**Authors:** Xingtao Zhao, Hao Peng, Dingli Su, Xianghua Zeng, Chunyang Liu, Jinzhi Liao, Philip S. Yu

**Venue:** UAI 2026

**Primary source:** arXiv:2511.16275

---

# 1. Research Problem

_To be completed from the paper._

## 1.1 Why is the problem important?

_To be completed._

## 1.2 What limitation in existing UQ methods do the authors identify?

_To be completed._

---

# 2. SeSE's Core Idea

_To be completed._

## 2.1 What is Semantic Structural Entropy?

_To be completed._

## 2.2 Why use structural information?

_To be completed._

## 2.3 What does "uncertainty" mean in this framework?

_To be completed._

---

# 3. Short-Form Methodology

## Step 1 — Response Sampling

_To be completed._

### Inputs

_To be completed._

### Outputs

_To be completed._

---

## Step 2 — Semantic Graph Construction

_To be completed._

### NLI Model

_To be completed._

### Edge Construction

_To be completed._

### Edge Weight

_To be completed._

---

## Step 3 — Hierarchical Abstraction

_To be completed._

### Structural Entropy

_To be completed._

### Encoding Tree

_To be completed._

### Optimization

_To be completed._

### Final SeSE Score

_To be completed._

---

# 4. Long-Form Methodology

## Motivation

_To be completed._

## Claim Extraction

_To be completed._

## Claim-Response Bipartite Graph

_To be completed._

## Claim-Level Uncertainty

_To be completed._

---

# 5. Theoretical Claims

## SeSE and Semantic Entropy

_To be completed._

## Generalization Relationship

_To be completed._

---

# 6. Baselines

The paper compares SeSE against multiple uncertainty estimation approaches.

_To be completed with descriptions of each baseline._

---

# 7. Evaluation

## Datasets

_To be completed._

## Models

_To be completed._

## Metrics

_To be completed._

## Experimental Protocol

_To be completed._

---

# 8. Main Results

_To be completed._

## Short-Form Results

_To be completed._

## Long-Form Results

_To be completed._

---

# 9. Ablation Studies

## Number of Samples

_To be completed._

## Encoding Tree Height

_To be completed._

## Other Ablations

_To be completed._

---

# 10. Statistical Analysis

_To be completed._

---

# 11. Authors' Conclusions

_To be completed._

---

# 12. Potential Research Gaps

This section must contain only gaps that are actually supported by the paper or clearly identified through our analysis.

Potential questions to investigate:

- Does uncertainty reliability vary systematically by task?
- Does uncertainty reliability vary by error type?
- How does response length affect uncertainty reliability?
- How does model scale affect uncertainty reliability?
- How stable is the uncertainty score under different sampling settings?
- Does the optimal tree height generalize to unseen tasks?
- Does high uncertainty correspond to a calibrated probability of error?
- Are there systematic cases where the semantic structure appears confident despite an incorrect answer?

These are research questions, not findings.

---

# 13. Questions We Need to Answer Before Designing Our Experiments

1. Which claims made by SeSE are directly supported by experiments?
2. Which are theoretical claims?
3. Which experimental variables have already been thoroughly tested?
4. Which variables have only been tested indirectly?
5. Which potentially important variables have not been studied?
6. What would constitute a meaningful extension rather than a minor reproduction?