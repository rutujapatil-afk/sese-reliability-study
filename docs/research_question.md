# Research Question

## Working Title

**When Does an LLM Know That It Doesn't Know? A Systematic Study of Structural Uncertainty Across Models, Tasks, and Error Types**

## Primary Research Question

> How reliably does structural uncertainty predict the correctness of LLM outputs, and under what model, task, and error conditions does this reliability break down?

## Secondary Research Objective

If systematic evaluation identifies important failure modes in structural uncertainty estimation, investigate whether those failure modes can be addressed through an improved uncertainty-estimation approach.

## Motivation

Large language models can produce fluent and convincing answers that are incorrect. This makes uncertainty estimation important for determining when an LLM's output should be trusted.

SeSE proposes a black-box approach to uncertainty quantification based on structural information in model outputs. Rather than assuming that the method performs equally well in all settings, this study aims to systematically investigate its reliability.

The study will examine whether structural uncertainty consistently corresponds to answer correctness across different:

- model families and model scales;
- task types;
- answer lengths;
- levels of task difficulty; and
- types of model errors.

The objective is not simply to maximize a performance metric, but to understand **when structural uncertainty is informative, when it is unreliable, and why**.

## Initial Study Dimensions

### 1. Model

Investigate whether uncertainty reliability changes across model families and model scales.

### 2. Task

Investigate differences across tasks such as:

- factual question answering;
- mathematical reasoning;
- logical reasoning;
- coding;
- open-ended generation.

The final task set will be determined after reviewing the original SeSE experiments and available datasets.

### 3. Error Type

Where possible, distinguish between different types of incorrect outputs, including:

- factual hallucination;
- reasoning error;
- arithmetic error;
- fabricated information;
- incomplete answer; and
- contradiction or inconsistency.

### 4. Generation Characteristics

Investigate whether uncertainty reliability changes with characteristics such as:

- response length;
- reasoning depth;
- answer complexity; and
- generation uncertainty.

## Core Hypothesis

**H1:** Structural uncertainty is correlated with the probability that an LLM output is incorrect, but the strength and reliability of this relationship varies systematically across models, tasks, and error types.

## Secondary Hypotheses

These will be finalized after reviewing the original SeSE methodology and experiments.

Potential hypotheses include:

- Structural uncertainty may be more effective at detecting factual hallucinations than reasoning errors.
- Structural uncertainty may become less reliable as generated responses become longer or more complex.
- The relationship between uncertainty and correctness may vary with model scale.
- Different uncertainty-estimation methods may identify different classes of model failures.

These are provisional hypotheses and will not be treated as findings until experimentally tested.

## Scope

The initial phase of this project will focus on systematic analysis and reproduction of relevant SeSE experiments.

Only after establishing a reliable baseline will we consider developing a new methodology or modification.

## Research Principle

The project will distinguish clearly between:

1. **Prior work** — results and methodology reported by the original SeSE authors.
2. **Hypotheses** — questions proposed by this study before experimentation.
3. **Our findings** — conclusions supported by experiments conducted in this project.

No original contribution will be presented as part of the SeSE authors' work, and no prior result will be represented as an independent finding of this study.