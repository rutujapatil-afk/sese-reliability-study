# SeSE Phase 2 — Scaled Evaluation

This report records evaluation results obtained by calling the original, unmodified SeSE semantic graph construction function.

## Experimental configuration

- Cases: 7
- Responses: 42
- Batch size: 128
- Original SeSE implementation: UNMODIFIED
- Threshold override: none

## Evaluation status

- Successful cases: 7
- Failed cases: 0

## Successful case results

| case_id       | category   |   n_responses |   n_nodes |   n_edges |   edge_density |   mean_edge_weight |   total_edge_weight |   n_connected_components |   original_structural_entropy |
|:--------------|:-----------|--------------:|----------:|----------:|---------------:|-------------------:|--------------------:|-------------------------:|------------------------------:|
| factual_001   | factual    |             6 |         6 |         8 |       0.533333 |           0.668395 |             5.34716 |                        1 |                           nan |
| factual_002   | factual    |             6 |         6 |        15 |       1        |           0.997415 |            14.9612  |                        1 |                           nan |
| factual_003   | factual    |             6 |         6 |        15 |       1        |           0.718707 |            10.7806  |                        1 |                           nan |
| factual_004   | factual    |             6 |         6 |        15 |       1        |           0.804778 |            12.0717  |                        1 |                           nan |
| factual_005   | factual    |             6 |         6 |        15 |       1        |           0.599283 |             8.98925 |                        1 |                           nan |
| reasoning_001 | reasoning  |             6 |         6 |        11 |       0.733333 |           0.557199 |             6.12919 |                        1 |                           nan |
| reasoning_002 | reasoning  |             6 |         6 |         6 |       0.4      |           0.64156  |             3.84936 |                        1 |                           nan |

## Category summary

| category   |   n_responses_mean |   n_responses_std |   n_nodes_mean |   n_nodes_std |   n_edges_mean |   n_edges_std |   edge_density_mean |   edge_density_std |   mean_edge_weight_mean |   mean_edge_weight_std |   total_edge_weight_mean |   total_edge_weight_std |   n_connected_components_mean |   n_connected_components_std |   weight_entropy_diagnostic_mean |   weight_entropy_diagnostic_std |   original_structural_entropy_mean |   original_structural_entropy_std |
|:-----------|-------------------:|------------------:|---------------:|--------------:|---------------:|--------------:|--------------------:|-------------------:|------------------------:|-----------------------:|-------------------------:|------------------------:|------------------------------:|-----------------------------:|---------------------------------:|--------------------------------:|-----------------------------------:|----------------------------------:|
| factual    |                  6 |                 0 |              6 |             0 |           13.6 |       3.1305  |            0.906667 |           0.2087   |                0.757716 |              0.153518  |                 10.43    |                 3.57984 |                             1 |                            0 |                          4.47461 |                        0.522548 |                                nan |                               nan |
| reasoning  |                  6 |                 0 |              6 |             0 |            8.5 |       3.53553 |            0.566667 |           0.235702 |                0.599379 |              0.0596519 |                  4.98927 |                 1.61208 |                             1 |                            0 |                          3.58866 |                        0.722411 |                                nan |                               nan |

## Reproducibility note

The scaled evaluator does not reimplement the SeSE semantic graph algorithm. It imports `build_semantic_graph` from `original_work/SeSE` and invokes it with the original API: `responses`, `question`, and optional `batch_size`.
