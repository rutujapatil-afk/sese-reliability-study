# Research Gap Analysis — Critical Review

## Purpose

This document evaluates potential research directions against the existing SeSE work.

A candidate direction is not considered a genuine research gap merely because it was not explicitly investigated in the original paper.

A candidate must satisfy three conditions:

1. The original work does not already adequately answer the question.
2. The question is scientifically meaningful.
3. The question can support an independent, reproducible study.

The original SeSE implementation is treated as reference work.

---

# 1. What SeSE Already Establishes

The original work already investigates several important dimensions, including:

- short-form uncertainty estimation;
- long-form uncertainty estimation;
- semantic graph construction;
- hierarchical structural entropy;
- multiple model–dataset combinations;
- comparison with uncertainty-estimation baselines;
- number of sampled responses;
- encoding-tree height;
- AUROC;
- AURAC.

These dimensions should therefore primarily serve as:

- reproduction targets;
- baseline conditions;
- controls;
- or context for our study.

They should not automatically be presented as novel contributions.

---

# 2. Candidate Directions That Should NOT Be Our Main Contribution

## 2.1 More Datasets

### Assessment

Weak as a standalone contribution.

### Reason

SeSE already evaluates across a substantial collection of model–dataset combinations.

### Use in Our Study

Potentially useful for independent validation, but not sufficient as the main research question.

### Decision

REJECT AS PRIMARY QUESTION

---

## 2.2 Model Size / Model Comparison

### Assessment

Insufficient by itself.

### Reason

The original work already evaluates multiple models and examines model-related variation.

### Use in Our Study

Use as an experimental control or generalization dimension.

### Decision

REJECT AS PRIMARY QUESTION

---

## 2.3 Number of Samples

### Assessment

Already studied.

### Use in Our Study

Reproduce as a baseline and potentially investigate stability beyond the original experimental design.

### Decision

REJECT AS PRIMARY QUESTION

---

## 2.4 Encoding Tree Height

### Assessment

Already studied as an ablation.

### Use in Our Study

Baseline / control variable.

### Decision

REJECT AS PRIMARY QUESTION

---

## 2.5 Hallucination Detection in General

### Assessment

Too close to the central motivation and evaluation of SeSE.

### Decision

REJECT AS PRIMARY QUESTION

---

# 3. Stronger Candidate Research Directions

## 3.1 Error-Specific Reliability

### Research Question

Does the reliability of structural uncertainty estimation differ systematically across different mechanisms of LLM error?

### Potential Error Categories

- factual errors;
- reasoning errors;
- arithmetic errors;
- fabricated information;
- contradictions;
- incomplete answers.

### Why This May Be Important

Aggregate AUROC/AURAC can indicate overall discrimination while hiding differences between error mechanisms.

An estimator could perform strongly overall while failing systematically on a particular class of errors.

### What We Need to Verify

We must determine whether the original SeSE experiments already perform sufficiently detailed error-type analysis.

### Status

PROMISING — REQUIRES CLAIM AUDIT

---

# 4. Structural Failure Modes

## Research Question

When SeSE assigns low uncertainty to an incorrect output, what properties of the underlying semantic structure are associated with that failure?

### Motivation

SeSE derives uncertainty from semantic graph structure and hierarchical abstraction.

Therefore, analyzing false-confidence cases at the graph level may reveal information that aggregate performance metrics do not capture.

### Potential Analysis Variables

- graph density;
- number of semantic clusters;
- cluster imbalance;
- edge-weight distribution;
- hierarchy depth;
- entropy distribution;
- disagreement between sampled responses;
- relationship between graph structure and correctness.

### Potential Contribution

A taxonomy or mechanistic explanation of structural uncertainty failures.

### Status

STRONG CANDIDATE — REQUIRES CLAIM AUDIT

---

# 5. Stability of Structural Uncertainty

## Research Question

How stable is the SeSE uncertainty estimate when the same query is evaluated under different stochastic generation conditions?

### Potential Variables

- random seed;
- sampling temperature;
- number of samples;
- decoding configuration;
- prompt formulation.

### Key Distinction

Two separate properties should be measured:

1. UQ discrimination performance.
2. UQ score stability.

A method can have strong average discrimination while producing unstable uncertainty scores.

### Potential Contribution

A systematic characterization of the robustness of structural uncertainty estimation.

### Status

STRONG CANDIDATE — REQUIRES CLAIM AUDIT

---

# 6. Structural Complexity

## Research Question

Does the relationship between structural uncertainty and correctness change as the semantic or reasoning complexity of an output increases?

### Potential Complexity Measures

- response length;
- number of claims;
- number of reasoning steps;
- semantic diversity;
- graph complexity;
- task difficulty.

### Motivation

Because SeSE explicitly models semantic structure, increasing structural complexity may affect both the representation and the resulting uncertainty estimate.

### Status

STRONG CANDIDATE — REQUIRES CLAIM AUDIT

---

# 7. Calibration / Decision Usefulness

## Important Distinction

SeSE explicitly treats its output as a relative uncertainty score rather than an exact probability of correctness.

Therefore, the claim:

> "SeSE is not calibrated"

would not constitute a valid criticism by itself.

A more meaningful question is:

> How stable and decision-useful is SeSE's uncertainty score when used to support selective prediction or abstention decisions?

### Potential Measures

- selective accuracy;
- coverage;
- risk-coverage curves;
- expected calibration error where appropriate;
- threshold stability;
- cross-condition transfer of thresholds.

### Status

POTENTIALLY USEFUL — REQUIRES FURTHER LITERATURE AND CLAIM REVIEW

---

# 8. Mechanism-Driven Methodological Improvement

This is NOT an initial research question.

It is a potential second phase.

## Proposed Logic

1. Reproduce SeSE.
2. Identify a reproducible failure mode.
3. Determine the structural mechanism associated with the failure.
4. Formulate a hypothesis explaining the failure.
5. Design a modification specifically targeting that mechanism.
6. Compare the modification against SeSE and established baselines.
7. Evaluate on held-out conditions.

### Principle

We must not modify SeSE merely to obtain a higher score.

Any methodological change must be motivated by an observed limitation.

### Status

PHASE-2 POSSIBILITY

---

# 9. Strongest Current Research Direction

The strongest current direction is not simply:

> "Does SeSE work?"

Instead:

> **When and why does structural uncertainty fail to identify incorrect LLM outputs?**

This can be operationalized through three linked questions:

### RQ1 — Reliability

How does structural uncertainty reliability vary across distinct types and levels of LLM error?

### RQ2 — Mechanism

What structural properties of the semantic response representation are associated with false-confidence failures?

### RQ3 — Improvement

Can the mechanisms identified in RQ1 and RQ2 motivate a more reliable structural uncertainty estimator?

---

# 10. Why This Could Constitute a Standalone Study

The proposed study would have an independent:

- research question;
- experimental design;
- hypotheses;
- evaluation framework;
- error taxonomy;
- failure analysis;
- statistical analysis;
- interpretation;
- and potentially a new methodological contribution.

SeSE would function as the foundational reference and baseline rather than the identity of the entire project.

---

# 11. Falsifiability

The study must allow outcomes that contradict our expectations.

Possible outcomes include:

### Outcome A

SeSE is highly robust across error types.

### Outcome B

SeSE has systematic weaknesses for particular error types.

### Outcome C

SeSE failures are associated with identifiable graph structures.

### Outcome D

The observed failures cannot be explained by the proposed structural variables.

### Outcome E

A proposed improvement does not outperform SeSE.

All outcomes should be considered valid research findings if supported by appropriate evidence.

---

# 12. Current Decision

No final research question is locked yet.

Before locking the question, we must complete:

1. A claim-by-claim audit of the SeSE paper.
2. A detailed examination of its experimental design.
3. A review of the relevant uncertainty-quantification literature.
4. Identification of what has already been studied by subsequent work.
5. A feasibility analysis of candidate experiments.

Only then should the final research question be selected.

---

# 13. Research Integrity Rule

The project must distinguish between:

- prior work;
- our hypotheses;
- our experimental observations;
- our interpretations;
- and our original contributions.

No limitation will be claimed merely because it was not discussed by the original authors.

Every claimed research gap must be supported by evidence.