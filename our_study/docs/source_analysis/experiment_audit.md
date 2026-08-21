# SeSE Experimental Audit

## Purpose

This document records exactly what the original SeSE experiments test.

The goal is to determine the boundary of the evidence provided by the original work and identify questions that remain genuinely unanswered.

We distinguish:

- variables deliberately manipulated by SeSE;
- variables merely present in the benchmark;
- aggregate evaluation;
- fine-grained analysis;
- and experiments that are absent.

---

# 1. Experimental Scope

## Short-Form Experiments

### Tasks / Datasets

TBD

### Models

TBD

### Number of Samples

TBD

### Sampling Configuration

TBD

### Semantic Graph Construction

TBD

### NLI Model

TBD

### Tree Construction

TBD

### Tree Height

TBD

### Baselines

TBD

### Metrics

TBD

---

# 2. Long-Form Experiments

### Datasets

TBD

### Models

TBD

### Claim Extraction

TBD

### Claim-Response Graph

TBD

### Evaluation

TBD

### Metrics

TBD

---

# 3. Variables Explicitly Manipulated

| Variable | Manipulated? | Range / Conditions | Purpose | Finding |
|---|---|---|---|---|
| Sample count | TBD | TBD | Sensitivity | TBD |
| Tree height | TBD | TBD | Sensitivity | TBD |
| Model | TBD | TBD | Generalization | TBD |
| Dataset | TBD | TBD | Generalization | TBD |
| Generation setting | TBD | TBD | TBD | TBD |
| NLI model | TBD | TBD | TBD | TBD |

---

# 4. Variables Observed but Not Necessarily Manipulated

| Variable | Present in Data? | Explicitly Analyzed? | Notes |
|---|---|---|---|
| Response length | TBD | TBD | |
| Number of claims | TBD | TBD | |
| Reasoning complexity | TBD | TBD | |
| Semantic diversity | TBD | TBD | |
| Graph density | TBD | TBD | |
| Graph structure | TBD | TBD | |
| Error type | TBD | TBD | |
| Sampling variability | TBD | TBD | |

---

# 5. Evaluation Granularity

## Aggregate Performance

What aggregate metrics are reported?

TBD

## Per-Example Analysis

Are individual predictions analyzed?

TBD

## Error-Type Analysis

Are incorrect outputs divided into meaningful error categories?

TBD

## Failure-Case Analysis

Are false-confidence cases systematically analyzed?

TBD

## Structural Analysis

Are properties of the semantic graph linked to prediction failures?

TBD

---

# 6. Stability

## Question

Does the original study evaluate whether the SeSE score for the same query changes under independent stochastic sampling?

TBD

### Distinction

Sample-count sensitivity and score stability are different.

A method can have stable aggregate performance while producing unstable individual uncertainty scores.

---

# 7. Complexity

## Question

Does the original study explicitly test how uncertainty reliability changes with semantic/reasoning complexity?

TBD

### Candidate Measures

- response length;
- number of claims;
- reasoning steps;
- semantic diversity;
- graph complexity;
- task difficulty.

---

# 8. Error Mechanisms

## Question

Does the original study distinguish different causes of incorrect answers?

TBD

### Candidate Categories

- factual;
- reasoning;
- arithmetic;
- fabrication;
- contradiction;
- incompleteness.

---

# 9. Failure Mechanisms

## Question

When SeSE is confidently wrong, does the original study analyze the underlying semantic graph?

TBD

### Possible Structural Variables

- graph density;
- edge-weight distribution;
- number of clusters;
- cluster imbalance;
- hierarchy depth;
- entropy distribution.

---

# 10. Critical Distinction

The following should NOT be treated as equivalent:

### A. Benchmark performance

"SeSE achieves high AUROC."

### B. Reliability characterization

"SeSE performs similarly across error types."

### C. Stability

"The uncertainty score is stable across repeated sampling."

### D. Mechanistic understanding

"We can explain why SeSE becomes confidently wrong."

### E. Calibration

"A numerical uncertainty value corresponds to an empirical probability of error."

The original experiments may establish A without necessarily establishing B–E.

---

# 11. Candidate Gap Assessment

| Candidate | Explicitly Tested? | Tested Thoroughly? | Evidence Strength | Remaining Question |
|---|---|---|---|---|
| Error-specific reliability | TBD | TBD | TBD | TBD |
| Failure mechanisms | TBD | TBD | TBD | TBD |
| Score stability | TBD | TBD | TBD | TBD |
| Complexity dependence | TBD | TBD | TBD | TBD |
| Decision usefulness | TBD | TBD | TBD | TBD |

---

# 12. Final Decision

No research question will be locked until this table has been completed using evidence from the original paper.

The final question must be:

- genuinely unresolved;
- experimentally testable;
- scientifically meaningful;
- feasible;
- independently reproducible;
- and substantial enough to constitute a standalone study.