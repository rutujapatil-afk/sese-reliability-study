# SeSE Claim Audit — Evidence Review

## Source Hierarchy

Primary source:

- Published UAI 2026 paper in Proceedings of Machine Learning Research.
- Official SeSE repository.

The published paper is treated as the authoritative version for claims about the final work.

---

# 1. Core Methodological Claims

## Claim 1 — SeSE is a black-box uncertainty quantification framework

### Evidence

The paper presents SeSE as a black-box UQ framework applicable to both open- and closed-source LLMs.

### Assessment

SUPPORTED.

### Important qualification

Black-box access does not mean the method is independent of all external modeling choices. The semantic graph construction and uncertainty computation introduce their own modeling components.

### Research implication

We should investigate whether those components affect reliability.

---

## Claim 2 — SeSE uses latent semantic structural information

### Evidence

The paper's central methodological claim is that existing semantic UQ approaches overlook latent semantic structural information.

SeSE constructs a hierarchical abstraction of the semantic space using structural entropy minimization.

### Assessment

SUPPORTED AS A METHOD DESCRIPTION.

### Important distinction

The existence of structural information in the representation is not itself evidence that every structural feature improves uncertainty estimation.

That requires empirical evaluation.

---

## Claim 3 — SeSE generalizes Semantic Entropy

### Evidence

The paper provides a theoretical result showing that SeSE recovers Semantic Entropy when the encoding tree is restricted to a single layer.

### Assessment

SUPPORTED AS A THEORETICAL CLAIM.

### Research implication

This should not be treated as a research gap.

The interesting question is instead what practical benefits arise from the additional hierarchy.

---

# 2. Empirical Performance

## Claim 4 — SeSE outperforms evaluated baselines

### Evidence

The published paper reports superior empirical performance over baselines across 24 model–dataset combinations.

The repository describes the released experiments as reproducing the paper's main results.

### Assessment

SUPPORTED WITHIN THE REPORTED EXPERIMENTAL SETUP.

### Important qualification

"Outperforms the evaluated baselines" does not mean "universally superior under all conditions."

### Research implication

Our study should investigate boundary conditions rather than merely repeat aggregate benchmark comparisons.

---

## Claim 5 — SeSE works across multiple models

### Evidence

The paper evaluates multiple model–dataset combinations.

### Assessment

SUPPORTED WITHIN THE TESTED MODELS.

### Research implication

A simple "does model choice matter?" study is not sufficiently novel.

Model variation should instead be used as a control or generalization dimension.

---

## Claim 6 — SeSE works across multiple datasets/tasks

### Evidence

The paper reports experiments across 24 model–dataset combinations.

The repository identifies short-form QA settings including BioASQ, TriviaQA, and SQuAD.

### Assessment

SUPPORTED WITHIN THE TESTED BENCHMARKS.

### Research implication

Simply adding datasets is not a sufficiently strong primary contribution.

---

# 3. Short-Form Methodology

## Claim 7 — SeSE can estimate uncertainty from semantic structure in short-form generation

### Evidence

The short-form pipeline:

1. samples answers;
2. constructs semantic structure;
3. performs uncertainty quantification;
4. evaluates uncertainty metrics.

### Assessment

SUPPORTED.

### Research implication

The short-form pipeline should become one of our reproducible baselines.

---

# 4. Long-Form Methodology

## Claim 8 — SeSE provides claim-level uncertainty for long-form outputs

### Evidence

The paper extends SeSE to long-form generation using claim-response bipartite graphs.

The repository contains a dedicated long-form structural entropy module implementing this experimental setup.

### Assessment

SUPPORTED WITHIN THE REPORTED EXPERIMENTS.

### Research implication

"Can SeSE do long-form uncertainty?" is not our research question.

A stronger question is whether its claim-level uncertainty behaves reliably across different kinds of claims and failures.

---

# 5. Hyperparameter Claims

## Claim 9 — Sample count matters

### Evidence

The paper includes sensitivity/ablation analysis involving the number of sampled responses.

### Assessment

ALREADY STUDIED.

### Research implication

Do not use sample count alone as our research gap.

Potentially useful later for studying score stability.

---

## Claim 10 — Encoding-tree height matters

### Evidence

The paper evaluates the effect of encoding-tree height.

### Assessment

ALREADY STUDIED.

### Research implication

Do not use tree height alone as our research gap.

---

# 6. Reliability Evaluation

## Claim 11 — SeSE can distinguish correct and incorrect outputs

### Evidence

The experimental evaluation uses uncertainty-ranking metrics including AUROC and rejection-oriented evaluation.

### Assessment

SUPPORTED WITHIN THE TESTED TASKS.

### Critical limitation

Aggregate discrimination does not necessarily reveal:

- which error mechanisms are detected;
- which errors are missed;
- why false-confidence cases occur;
- whether uncertainty estimates remain stable;
- whether graph structure explains failures.

### Research implication

This is the first major area where a deeper study may be justified.

---

# 7. Error-Type Analysis

## Question

Does the original work systematically characterize SeSE performance across distinct mechanisms of incorrectness?

### Current Assessment

NOT YET ESTABLISHED.

The published abstract and repository documentation establish aggregate UQ evaluation, but they do not by themselves establish a comprehensive error taxonomy analysis.

### Required Next Step

Inspect the full experimental sections and result tables before declaring this a research gap.

### Status

PROMISING — NOT YET LOCKED.

---

# 8. Failure Mechanisms

## Question

When SeSE gives low uncertainty to an incorrect answer, does the original work explain the structural reason for the failure?

### Current Assessment

NOT ESTABLISHED FROM THE HIGH-LEVEL EVIDENCE.

The method constructs semantic graphs and hierarchical abstractions, but aggregate benchmark performance does not by itself constitute a mechanistic failure analysis.

### Required Next Step

Inspect:

- qualitative examples;
- ablations;
- failure cases;
- graph construction analysis;
- discussion sections.

### Status

STRONG CANDIDATE — REQUIRES FULL-PAPER VERIFICATION.

---

# 9. Stability

## Question

Does the original work establish that individual SeSE scores are stable under stochastic changes in generation?

### Current Assessment

NOT ESTABLISHED FROM THE HIGH-LEVEL EVIDENCE.

The method depends on sampled responses, so stochasticity is methodologically relevant.

However, sample-count sensitivity is not equivalent to score-level stability.

### Important distinction

These are different questions:

1. Does changing N change average benchmark performance?
2. Does the uncertainty score for an individual query remain stable across independent sampling runs?

The second is potentially underexplored.

### Status

STRONG CANDIDATE — REQUIRES FULL-PAPER VERIFICATION.

---

# 10. Complexity

## Question

Does SeSE's reliability systematically change with semantic/reasoning complexity?

### Current Assessment

NOT ESTABLISHED FROM THE HIGH-LEVEL EVIDENCE.

The method explicitly models semantic structure, but this does not establish how performance changes as structural complexity increases.

### Potential Variables

- response length;
- number of claims;
- number of reasoning steps;
- semantic diversity;
- graph complexity;
- task difficulty.

### Status

STRONG CANDIDATE — REQUIRES FULL-PAPER VERIFICATION.

---

# 11. Calibration

## Question

Does SeSE output a calibrated probability of correctness?

### Assessment

This should NOT be framed as a failure of SeSE.

The method is described as an uncertainty score rather than a probability estimate.

### Better question

How useful and stable is the SeSE score for decision-making under selective prediction or abstention?

### Status

POTENTIAL SECONDARY QUESTION.

---

# 12. Current Research-Gap Ranking

| Candidate | Novelty Potential | Scientific Depth | Risk of Already Being Studied | Current Status |
|---|---:|---:|---:|---|
| More datasets | Low | Low | High | Reject |
| Model-size comparison | Low | Medium | High | Reject |
| Sample count | Low | Medium | High | Reject |
| Tree height | Low | Medium | High | Reject |
| Hallucination detection | Low | Medium | Very high | Reject |
| Calibration alone | Medium | Medium | Medium | Secondary |
| Error-specific reliability | High | High | Medium | Investigate |
| Failure mechanisms | Very high | Very high | Medium | Investigate |
| Score stability | High | High | Medium | Investigate |
| Complexity dependence | High | High | Medium | Investigate |
| Mechanism-driven improvement | Very high | Very high | Low | Phase 2 |

---

# 13. Current Best Research Direction

The strongest current direction is:

> When and why does structural uncertainty fail to identify incorrect LLM outputs?

This is intentionally not yet the final research question.

It will be decomposed only after the full paper audit.

---

# 14. Required Next Evidence

Before locking the research question, inspect the original paper for:

1. Detailed experimental tables.
2. Ablation experiments.
3. Sensitivity experiments.
4. Qualitative examples.
5. Discussion of limitations.
6. Error/failure analysis.
7. Sampling methodology.
8. Graph construction methodology.
9. NLI model details.
10. Evaluation protocol.

Only after this evidence review should the final research question be selected.