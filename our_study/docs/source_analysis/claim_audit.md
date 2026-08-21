# SeSE Claim Audit

## Purpose

This document audits the original SeSE paper's claims against the evidence provided by its experiments.

The objective is to distinguish:

1. What SeSE establishes.
2. What SeSE provides evidence for but only under limited conditions.
3. What remains unanswered.
4. Which unanswered questions could constitute a legitimate research gap.

No research gap will be claimed merely because the original paper does not mention a topic.

---

# 1. Core Methodological Claims

## Claim 1 — Structural information provides useful uncertainty estimates

### Claim

SeSE uses structural information in semantic graphs to estimate LLM uncertainty.

### Evidence

_To be extracted from the paper._

### Experiment

_To be identified._

### Strength of Evidence

TBD

### What Remains Unanswered?

TBD

---

## Claim 2 — Hierarchical abstraction improves semantic uncertainty estimation

### Claim

Hierarchical structural entropy provides useful information beyond a flat semantic representation.

### Evidence

_To be extracted._

### Experiment

_To be identified._

### Strength of Evidence

TBD

### What Remains Unanswered?

TBD

---

## Claim 3 — SeSE generalizes Semantic Entropy

### Claim

SeSE recovers Semantic Entropy under the appropriate restriction of the encoding tree.

### Evidence

_To be extracted._

### Type of Evidence

THEORETICAL / EMPIRICAL

### What Remains Unanswered?

TBD

---

# 2. Empirical Performance Claims

## Claim 4 — SeSE improves uncertainty estimation performance

### Claim

SeSE outperforms the evaluated baselines on the reported benchmark settings.

### Evidence

_To be extracted._

### Datasets

TBD

### Models

TBD

### Metrics

TBD

### Strength of Evidence

TBD

### Generalization Limits

TBD

---

## Claim 5 — SeSE works across different models

### Evidence

_To be extracted._

### Models Tested

TBD

### Experimental Design

TBD

### What Remains Unanswered?

TBD

---

## Claim 6 — SeSE works across different datasets/tasks

### Evidence

_To be extracted._

### Tasks Tested

TBD

### Experimental Design

TBD

### What Remains Unanswered?

TBD

---

# 3. Hyperparameter / Sensitivity Claims

## Claim 7 — Sample count affects performance

### Evidence

_To be extracted._

### Variables Tested

TBD

### Findings

TBD

### What Remains Unanswered?

TBD

---

## Claim 8 — Encoding-tree height affects performance

### Evidence

_To be extracted._

### Variables Tested

TBD

### Findings

TBD

### What Remains Unanswered?

TBD

---

# 4. Long-Form Claims

## Claim 9 — SeSE can estimate uncertainty at claim level

### Evidence

_To be extracted._

### Experimental Setup

TBD

### Findings

TBD

### What Remains Unanswered?

TBD

---

# 5. Reliability Claims

## Claim 10 — SeSE uncertainty is useful for distinguishing correct and incorrect outputs

### Evidence

_To be extracted._

### Metrics

TBD

### Experimental Setup

TBD

### Strength of Evidence

TBD

### Important Limitation

Aggregate discrimination metrics do not necessarily characterize performance across individual error mechanisms.

### Research Question Raised

Does SeSE behave differently across distinct types of incorrect outputs?

### Status

OPEN — TO BE VERIFIED AGAINST ORIGINAL PAPER

---

# 6. Failure Analysis

## Claim 11 — SeSE failure modes are understood

### Evidence

_To be extracted._

### Does the paper systematically analyze false-confidence cases?

TBD

### Does the paper examine semantic graph structure in failed cases?

TBD

### Does the paper provide a taxonomy of failure mechanisms?

TBD

### Status

OPEN — TO BE VERIFIED

---

# 7. Stability

## Claim 12 — SeSE uncertainty estimates are stable

### Evidence

_To be extracted._

### Randomness Tested?

TBD

### Sampling Conditions Tested?

TBD

### Prompt Variations Tested?

TBD

### Score-Level Stability Tested?

TBD

### Status

OPEN — TO BE VERIFIED

---

# 8. Complexity

## Claim 13 — SeSE remains reliable as semantic complexity increases

### Evidence

_To be extracted._

### Response Length Tested?

TBD

### Number of Claims Tested?

TBD

### Reasoning Complexity Tested?

TBD

### Graph Complexity Tested?

TBD

### Status

OPEN — TO BE VERIFIED

---

# 9. Calibration

## Claim 14 — SeSE produces calibrated probabilities

### Assessment

This claim should NOT be assumed.

The paper describes SeSE as a relative uncertainty score rather than an exact probability of correctness.

### Question

Does the paper evaluate calibration or decision usefulness beyond ranking/rejection metrics?

### Evidence

TBD

### Status

OPEN — TO BE VERIFIED

---

# 10. Critical Evidence Table

| Question | Evidence in SeSE | Strength | Remaining Gap |
|---|---|---|---|
| Does SeSE discriminate correct/incorrect outputs? | TBD | TBD | TBD |
| Does it work across models? | TBD | TBD | TBD |
| Does it work across datasets? | TBD | TBD | TBD |
| Does sample count matter? | TBD | TBD | TBD |
| Does tree height matter? | TBD | TBD | TBD |
| Does it work for long-form generation? | TBD | TBD | TBD |
| Does it work across error types? | TBD | TBD | TBD |
| Are failure mechanisms understood? | TBD | TBD | TBD |
| Is score stability understood? | TBD | TBD | TBD |
| Is complexity sensitivity understood? | TBD | TBD | TBD |
| Is calibration/decision usefulness established? | TBD | TBD | TBD |

---

# 11. Candidate Gaps After Evidence Review

A candidate gap will only survive if the evidence supports it.

## Candidate A — Error-Specific Reliability

Status: TBD

## Candidate B — Structural Failure Mechanisms

Status: TBD

## Candidate C — Stability

Status: TBD

## Candidate D — Complexity

Status: TBD

## Candidate E — Decision Usefulness / Calibration

Status: TBD

---

# 12. Final Research Question

NOT YET LOCKED.

The final research question will be selected only after the claim audit is complete.