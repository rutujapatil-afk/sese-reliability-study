# SeSE Repository Map

## Reference Repository

The original SeSE repository is preserved locally at:

`../original_work/SeSE/`

It is treated as reference material and is not modified.

## High-Level Structure

The original project contains two main experimental modules:

1. Long-form structural entropy
2. Sentence/short-form structural entropy

---

## 1. Long-Form Structural Entropy

Location:

`../original_work/SeSE/long_form_structural_entropy/`

### Files

| File | Role |
|---|---|
| `HCSE.py` | Hierarchical Clustering Structural Entropy implementation |
| `main.py` | Main experimental entry point |
| `utils.py` | Utility and evaluation functions |
| `factscore_*.json` | Experimental data/results associated with FActScore |
| `popqa_*.json` | Experimental data/results associated with PopQA |

### README-described pipeline

The long-form module performs uncertainty quantification on paragraph-level LLM outputs.

The README describes the process as involving:

- LLM calls
- adjacency matrix construction
- structural entropy calculation
- evaluation

The primary implementation files are `HCSE.py`, `main.py`, and `utils.py`.

---

## 2. Short-Form Structural Entropy

Location:

`../original_work/SeSE/sentence_structural_entropy/`

### Files

| File | Role |
|---|---|
| `sample_answers.py` | Samples LLM-generated answers |
| `uncertainty_quantification.py` | Performs uncertainty quantification |
| `analyze_results.py` | Analyzes uncertainty metrics |
| `src/` | Supporting data, models, uncertainty measures, and utilities |

### README-described pipeline

The short-form experiments consist of:

1. Sampling answers from an LLM.
2. Running uncertainty quantification.
3. Analyzing the resulting metrics.

The README identifies metrics including AUROC and structural entropy.

---

## 3. Long-Form vs Short-Form

| Dimension | Long-form | Short-form |
|---|---|---|
| Output type | Paragraph-level generation | Standard QA |
| Main structure | Claim-response bipartite graph | Semantic structure |
| Main entropy approach | Hierarchical Clustering Structural Entropy | Structural entropy |
| Main purpose | Hallucination / uncertainty analysis | Semantic uncertainty quantification |
| Primary implementation | `HCSE.py`, `main.py` | `uncertainty_quantification.py` |

This distinction is important for our study because uncertainty reliability may behave differently for short answers and long-form generation.

---

## 4. Experimental Environment

The original README specifies:

- Python 3.11
- PyTorch 2.5.1
- Linux environment used by the authors
- NVIDIA GPU hardware for LLM inference

The original experiments may require external APIs and model access.

We will not assume that reproducing the complete original environment is necessary until we have analyzed the paper and experimental requirements.

---

## 5. Initial Research Questions Raised by the Repository

The repository structure immediately raises several questions for our study:

1. Does structural uncertainty behave differently between short-form and long-form outputs?
2. Does uncertainty reliability depend on the type of task?
3. Does structural uncertainty reliably distinguish correct and incorrect answers?
4. Are some error types easier to detect than others?
5. How does response length affect uncertainty reliability?
6. How does model choice affect uncertainty reliability?
7. Which evaluation metrics best measure uncertainty reliability?
8. Which limitations of the original experimental design remain unexplored?

These questions are preliminary and will be refined after studying the paper.

---

## 6. Important Reproducibility Notes

The original README states that:

- the repository contains code intended to reproduce the paper's experiments;
- datasets are automatically downloaded in most cases;
- BioASQ requires separate manual download;
- some experiments require external API access;
- model access may require separate authorization;
- some experiments incur API costs.

These constraints will be considered when designing our reproduction study.

---

## 7. Next Analysis

Before implementing anything ourselves, we need to understand:

1. The mathematical definition of structural entropy.
2. How the semantic structure is constructed.
3. How uncertainty is calculated.
4. How long-form claim-response graphs are constructed.
5. How the original experiments evaluate uncertainty.
6. What baselines SeSE is compared against.
7. What the authors identify as limitations and future work.

Only after this analysis should we finalize our experimental hypotheses.