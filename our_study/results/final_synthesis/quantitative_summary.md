# SeSE Quantitative Synthesis

This report summarizes the current evidence from the independent SeSE robustness experiments. It does not modify or reinterpret the original implementation.

## Experiments Included

- Threshold sensitivity
- Semantic perturbation
- Score stability
- Semantic/reasoning complexity
- Failure mechanisms
- Phase 2 scaled evaluation

## Quantitative Results

### threshold_sensitivity: entropy_range

**Value:** 0.000198

Small range indicates limited entropy sensitivity across tested clustering thresholds.

### threshold_sensitivity: thresholds_tested

**Value:** 5.000000

Five clustering thresholds were evaluated.

### threshold_sensitivity: cluster_count_range

**Value:** 1.000000

Cluster count changed within the tested threshold range.

### semantic_perturbation: noise_max_relative_entropy_change

**Value:** 0.320876

Maximum observed relative entropy change under edge-weight noise.

### semantic_perturbation: dropout_max_relative_entropy_change

**Value:** 0.144263

Maximum observed relative entropy change under edge dropout.

### semantic_perturbation: noise_graph_change_at_max_level

**Value:** 0.244347

Graph change observed at the highest tested edge-weight noise level.

### semantic_perturbation: dropout_graph_change_at_max_level

**Value:** 0.000406

Graph change observed at the highest tested edge-dropout level.

### score_stability: repeat_count

**Value:** 11.000000

Repeated evaluations available in the stability dataset.

### score_stability: entropy_std

**Value:** 0.849235

Standard deviation of structural entropy across repeats.

### score_stability: entropy_range

**Value:** 2.260093

Observed structural-entropy range across repeats.

### complexity: complexity_entropy_range

**Value:** 0.422950

Structural entropy variation across tested semantic/reasoning complexity conditions.

### complexity: complexity_levels

**Value:** 5.000000

Number of distinct complexity conditions tested.

### scaled_evaluation: cases_evaluated

**Value:** 7.000000

Number of scaled-evaluation cases represented in the results table.

### scaled_evaluation: unique_cases

**Value:** 7.000000

Number of distinct evaluation cases in the scaled dataset.

### scaled_evaluation: total_responses

**Value:** 42.000000

Total number of responses represented across evaluated cases.

### scaled_evaluation: mean_incorrect_fraction

**Value:** 0.166667

Mean incorrect-response fraction across scaled-evaluation cases.

### scaled_evaluation: confident_failure_count

**Value:** 5.000000

Number of scaled-evaluation cases classified as confident failures.

### scaled_evaluation: entropy_mean

**Value:** -1.812261

Mean structural entropy across scaled-evaluation cases.

### scaled_evaluation: entropy_range

**Value:** 0.462373

Observed structural-entropy range across scaled-evaluation cases.

### scaled_evaluation: cluster_count_range

**Value:** 1.000000

Observed range in cluster counts across scaled-evaluation cases.

### failure_mechanism: confident_failure_count

**Value:** 2.000000

Number of tested cases classified as confident failures.

### failure_mechanism: mean_incorrect_fraction

**Value:** 0.333333

Mean incorrect-response fraction across tested cases.

### failure_mechanism: mean_cluster_imbalance

**Value:** 2.666667

Mean cluster imbalance across tested cases.

