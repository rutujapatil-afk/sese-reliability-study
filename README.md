# SeSE: Structural Analysis of Uncertainty in Large Language Model Responses

## Overview

This project presents an empirical evaluation of **SeSE (Structural Entropy-based Semantic Uncertainty)** for black-box uncertainty quantification in large language models (LLMs).

Rather than treating uncertainty solely as a property of individual response probabilities, this study investigates whether the **semantic organization of multiple model responses** provides a useful structural signal of uncertainty.

The evaluation follows the original SeSE methodology introduced by Zhao et al. [1]. The original structural-entropy implementation is used directly rather than replacing it with a generic Shannon-entropy formulation.

The central research question is:

> **How robust, stable, and diagnostically informative is structural entropy when the semantic response graph is subjected to controlled changes in clustering, graph structure, repeated evaluation, problem complexity, and response correctness?**

The project combines controlled experiments with a seven-case scaled evaluation to characterize where the structural signal is stable and where it is sensitive.

---

## Research Objectives

The study evaluates SeSE along five complementary dimensions:

1. **Threshold robustness** — Does structural entropy change substantially when the semantic clustering threshold is varied?
2. **Semantic-graph perturbation sensitivity** — How does structural entropy respond to edge-weight noise and edge dropout?
3. **Repeated-score stability** — How much variation is observed across repeated evaluations?
4. **Complexity sensitivity** — Does the structural signal vary across heterogeneous response conditions?
5. **Case-level failure structure** — How are incorrect responses positioned within semantic response clusters, particularly across factual and reasoning cases?

Together, these analyses distinguish **robustness of the metric** from **sensitivity to particular sources of structural variation**.

---

## Methodological Framework

For each question, multiple LLM responses are collected.

Each response constitutes a node in a semantic response graph. Semantic processing organizes responses into clusters, while pairwise natural-language-inference relationships provide the semantic relationships used to construct eligible graph edges and their weights.

The resulting weighted graph is evaluated using the original SeSE structural-entropy implementation [1].

```text
Question
   │
   ▼
Multiple LLM Responses
   │
   ▼
Semantic Processing
   │
   ▼
Semantic Clustering
   │
   ▼
Pairwise Semantic Relationships
   │
   ▼
Weighted Semantic Response Graph
   │
   ▼
Original SeSE Structural Entropy
   │
   ▼
Structural Evaluation
   │
   ├── Threshold Sensitivity
   ├── Graph Perturbation
   ├── Repeated Evaluation
   ├── Complexity Analysis
   └── Case-Level Failure Analysis
```

### Correctness-label separation

Correctness labels are used for **retrospective evaluation and failure analysis**.

They are **not used as inputs to construct the uncertainty graph**.

This distinction prevents correctness information from entering the structural uncertainty calculation.

---

# Experimental Program

## 1. Threshold Sensitivity

The clustering threshold is varied across five tested conditions.

The final evaluation produced an observed structural-entropy range of:

```text
0.000198
```

The corresponding trajectory was comparatively flat across the tested threshold range.

This supports threshold robustness **within the tested experimental regime**. It does not establish that clustering itself is invariant or that the result generalizes to arbitrary thresholds.

### Output

```text
our_study/results/threshold_sensitivity_results.csv
```

### Figure

```text
our_study/results/figures/figure_2_threshold_sensitivity.png
```

---

## 2. Semantic-Graph Perturbation

The semantic response graph is subjected to controlled perturbations using:

- edge-weight noise
- edge dropout

The experiment measures both relative structural-entropy change and relative graph change.

At the strongest tested condition:

```text
Maximum relative entropy change — noise:   0.320876
Maximum relative entropy change — dropout: 0.144263

Maximum relative graph change — noise:     0.244347
Maximum relative graph change — dropout:   0.000406
```

The maximum relative entropy response under edge-weight noise was approximately:

```text
2.23 ×
```

the corresponding response under edge dropout.

The result demonstrates measurable sensitivity to semantic edge-weight structure while showing that different graph perturbations do not produce equivalent effects.

### Output

```text
our_study/results/semantic_perturbation/perturbation_results.csv
```

### Figure

```text
our_study/results/figures/figure_3_semantic_perturbation.png
```

---

## 3. Repeated-Score Stability

The repeated-evaluation experiment produced:

```text
11 observations
```

with:

```text
Structural-entropy standard deviation: 0.849235
Observed range:                       2.260093
```

This provides an important qualification to the threshold-sensitivity result: the score can be comparatively stable to the tested clustering threshold while exhibiting substantially larger variation across repeated evaluations.

The threshold and repeated-evaluation experiments manipulate different sources of variation and are therefore interpreted as a **descriptive contrast**, not as a causal decomposition of variance.

### Output

```text
our_study/results/score_stability/score_stability_results.csv
```

### Figure

```text
our_study/results/figures/figure_4_score_stability.png
```

---

## 4. Complexity Analysis

Five complexity conditions are evaluated:

```text
simple_factual
explanatory
multi_claim
reasoning_heavy
contradictory_fabricated
```

Structural entropy varied across these conditions over a range of:

```text
0.422950
```

This establishes variation across the tested conditions but does not establish that complexity causes higher or lower uncertainty. The sample is too small for such an inference.

### Output

```text
our_study/results/complexity_study/complexity_results.csv
```

---

## 5. Scaled Case-Level Evaluation

A seven-case scaled evaluation provides case-level structural evidence.

The evaluation contains:

```text
5 factual cases
2 reasoning cases
```

Each case contains six responses.

### Factual cases

All five factual cases produced:

```text
Cluster structure:             [5,1]
Incorrect responses:           1
Incorrect-response fraction:   0.166667
Confident failure:             True
```

In every factual case, the single incorrect response occupied the singleton semantic cluster.

### Reasoning cases

The two reasoning cases produced:

```text
Reasoning 001: [3,2,1]
Reasoning 002: [4,1,1]
```

Each contained one incorrect response, but neither was classified as a confident failure.

The case-level analysis therefore shows a specific structural distinction within the tested examples: the factual cases consistently exhibit a dominant five-response cluster plus an isolated response, whereas the reasoning cases exhibit more fragmented semantic organization.

Because the scaled evaluation contains only seven cases, these findings are treated as **case-level empirical evidence rather than broad population-level claims**.

### Output

```text
our_study/results/scaled_evaluation/scaled_evaluation_results.csv
```

### Figure

```text
our_study/results/figures/figure_5_case_level_cluster_error_structure.png
```

---

# Final Quantitative Synthesis

The experiments indicate a **selective robustness profile rather than uniform stability**.

| Analysis | Main observation |
|---|---:|
| Threshold sensitivity | Entropy range = 0.000198 |
| Repeated evaluation | Entropy range = 2.260093 |
| Repeated evaluation | Entropy SD = 0.849235 |
| Graph perturbation — noise | Maximum relative entropy change = 0.320876 |
| Graph perturbation — dropout | Maximum relative entropy change = 0.144263 |
| Complexity conditions | Entropy range = 0.422950 |
| Scaled factual cases | Cluster structure = [5,1] |
| Scaled reasoning cases | Cluster structures = [3,2,1], [4,1,1] |

The central empirical observation is that **different sources of variation affect the structural signal differently**.

Threshold changes within the tested range produced very small entropy variation, whereas repeated evaluation and graph perturbation produced substantially larger changes.

At the case level, incorrect responses were structurally isolated in all five factual examples, while the two reasoning examples exhibited more fragmented cluster configurations.

These findings support a nuanced interpretation of structural uncertainty: SeSE should not be characterized simply as either “robust” or “unstable.” Its observed behavior depends on **which component of the semantic-response structure is being changed**.

---

# Reproducibility

The experimental implementations are located under:

```text
our_study/experiments/
```

The generated quantitative results are stored under:

```text
our_study/results/
```

## Main experiment and analysis scripts

```text
our_study/experiments/
├── run_scaled_evaluation.py
├── run_failure_mechanism_study.py
├── generate_final_synthesis.py
├── audit_final_synthesis.py
├── audit_scaled_results.py
├── generate_figure_2_threshold.py
├── generate_figure_3_perturbation.py
├── generate_figure_4_score_stability.py
└── generate_figure_5_case_structure.py
```

## Main result directories

```text
our_study/results/
├── threshold_sensitivity_results.csv
├── semantic_perturbation/
│   └── perturbation_results.csv
├── score_stability/
│   └── score_stability_results.csv
├── complexity_study/
│   └── complexity_results.csv
├── scaled_evaluation/
│   └── scaled_evaluation_results.csv
├── final_synthesis/
│   ├── quantitative_summary.csv
│   ├── quantitative_summary.md
│   └── research_claims.md
└── figures/
    ├── figure_2_threshold_sensitivity.png
    ├── figure_3_semantic_perturbation.png
    ├── figure_4_score_stability.png
    └── figure_5_case_level_cluster_error_structure.png
```

---

# Final Synthesis Pipeline

The final quantitative synthesis is generated from the individual experiment outputs:

```text
Individual experiment outputs
          │
          ▼
generate_final_synthesis.py
          │
          ├── quantitative_summary.csv
          ├── quantitative_summary.md
          └── research_claims.md
```

Run:

```bat
python our_study\experiments\generate_final_synthesis.py
```

Outputs are written to:

```text
our_study/results/final_synthesis/
```

---

# Quality-Control and Audit

Two audit scripts are included to verify the generated quantitative outputs and scaled-evaluation structure:

```text
our_study/experiments/audit_final_synthesis.py
our_study/experiments/audit_scaled_results.py
```

These are intended to reduce inconsistencies between experiment outputs, synthesis files, and reported manuscript claims.

---

# Main Figures

The final main-text figure sequence is:

### Figure 1 — Experimental Pipeline

The end-to-end methodology from question and response collection through semantic graph construction and structural entropy evaluation.

### Figure 2 — Threshold Sensitivity

Structural entropy across the tested clustering thresholds.

### Figure 3 — Semantic-Graph Perturbation Response

Structural-entropy and graph responses to edge-weight noise and edge dropout.

### Figure 4 — Repeated-Score Stability

Individual structural-entropy observations across repeated evaluations.

### Figure 5 — Case-Level Cluster and Error Structure

Semantic cluster organization and incorrect-response placement across the seven scaled cases.

Figures 2–5 are generated from the corresponding experiment outputs.

---

# Manuscript

The manuscript materials are maintained under:

```text
our_study/paper/
```

The manuscript follows a research-paper structure covering:

1. Introduction
2. Related Work
3. Methodology
4. Experimental Design
5. Results
6. Discussion
7. Limitations
8. Conclusion
9. References

The manuscript uses numbered IEEE-style citations.

The original SeSE work is maintained as Reference [1].

---

# Methodological Principles

The project follows these principles:

- The original SeSE structural-entropy implementation is used.
- Correctness labels are not used to construct the uncertainty graph.
- Quantitative results are derived from experiment outputs.
- Perturbation experiments use controlled graph modifications.
- Repeated-evaluation variation is reported descriptively.
- Small-sample findings are not presented as population-level conclusions.
- Threshold robustness is interpreted only over the tested threshold range.
- Complexity results are not treated as causal evidence.
- Case-level structural observations are distinguished from general claims.
- Figures are generated from the corresponding CSV outputs.

---

# Limitations

This study is an empirical evaluation rather than a definitive characterization of SeSE across all LLMs, prompts, datasets, or task distributions.

Important limitations include:

- the scaled evaluation contains only seven cases;
- the complexity experiment contains five tested conditions;
- the repeated-evaluation experiment contains 11 observations;
- threshold robustness is established only over the tested threshold range;
- perturbation results depend on the tested perturbation mechanisms and strengths;
- factual and reasoning cases are not sufficient to establish broad task-general behavior;
- descriptive differences between experiments should not be interpreted as a causal decomposition of variance.

These limitations define the scope of the claims made in the manuscript.

---

# Research Status

| Component | Status |
|---|---|
| Experimental evaluation | Complete |
| Quantitative synthesis | Complete |
| Audit and validation | Complete |
| Main figures | Complete |
| Scaled case analysis | Complete |
| Manuscript | Finalization and submission preparation |

---

# References

[1] X. Zhao, H. Peng, D. Su, X. Zeng, C. Liu, J. Liao, and P. S. Yu, “SeSE: Black-box uncertainty quantification for large language models based on structural information theory,” in *Proc. 42nd Conf. Uncertainty Artif. Intell.*, vol. 337, pp. 8209–8237, 2026.

[2] S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal, “Detecting hallucinations in large language models using semantic entropy,” *Nature*, vol. 630, pp. 625–630, 2024, doi: 10.1038/s41586-024-07421-0.

[3] O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar, “A survey on uncertainty quantification of large language models: Taxonomy, open research challenges, and future directions,” *ACM Computing Surveys*, vol. 58, no. 3, Art. no. 63, 2025, doi: 10.1145/3744238.

[4] L. Huang *et al.*, “A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions,” *ACM Transactions on Information Systems*, vol. 43, no. 2, Art. no. 42, 2025, doi: 10.1145/3703155.

[5] Z. Lin, S. Guan, W. Zhang, H. Zhang, Y. Li, and H. Zhang, “Towards trustworthy LLMs: A review on debiasing and dehallucinating in large language models,” *Artificial Intelligence Review*, vol. 57, Art. no. 243, 2024, doi: 10.1007/s10462-024-10896-y.

[6] R. Vashurin *et al.*, “Benchmarking uncertainty quantification methods for large language models with LM-Polygraph,” *Transactions of the Association for Computational Linguistics*, vol. 13, pp. 220–248, 2025, doi: 10.1162/tacl_a_00737.

[7] P. Manakul, A. Liusie, and M. J. F. Gales, “SelfCheckGPT: Zero-resource black-box hallucination detection for generative large language models,” in *Proc. 2023 Conf. Empirical Methods in Natural Language Processing*, pp. 9004–9017, 2023, doi: 10.18653/v1/2023.emnlp-main.557.

[8] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou, “Self-consistency improves chain of thought reasoning in language models,” in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2023.

[9] G. Ahdritz, T. Qin, N. Vyas, B. Barak, and B. L. Edelman, “Distinguishing the knowable from the unknowable with language models,” in *Proc. 41st Int. Conf. Mach. Learn.*, vol. 235, pp. 503–549, 2024.

[10] S. Ao, S. Rueger, and A. Siddharthan, “CSS: Contrastive semantic similarities for uncertainty quantification of LLMs,” in *Proc. 40th Conf. Uncertainty Artif. Intell.*, vol. 244, pp. 77–87, 2024.

---

# Citation

If you use the structural methodology evaluated in this project, please cite the original SeSE work:

> [1] X. Zhao, H. Peng, D. Su, X. Zeng, C. Liu, J. Liao, and P. S. Yu, “SeSE: Black-box uncertainty quantification for large language models based on structural information theory,” in *Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence*, vol. 337, pp. 8209–8237, 2026.

---

## Project Status

**Experimental evaluation complete. Quantitative synthesis complete. Main figures complete. Scaled case analysis complete. Manuscript prepared for finalization and submission.**