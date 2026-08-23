# SeSE Phase 2 — Scaled Evaluation

This experiment evaluates the original, unmodified SeSE semantic graph construction over a controlled seven-case dataset.

## Configuration

- Cases: 7
- Responses per case: 6
- Total responses: 42
- Analysis clustering threshold: 0.30
- Batch size: 128
- Original SeSE implementation: UNMODIFIED

## Important API detail

The original `build_semantic_graph()` requires both `responses` and `question` and returns an adjacency matrix. The experiment therefore does not pass an unsupported `threshold` argument.

## Successful evaluations

- Successful cases: 7
- Failed cases: 0

## Per-case results

| case_id       | category   |   n_nodes |   n_clusters |   n_edges |   edge_density |   mean_edge_weight |   total_edge_weight |   structural_entropy |   incorrect_fraction | confident_failure   | status   |
|:--------------|:-----------|----------:|-------------:|----------:|---------------:|-------------------:|--------------------:|---------------------:|---------------------:|:--------------------|:---------|
| factual_001   | factual    |         6 |            2 |        11 |       0.733333 |           0.578266 |             6.36093 |             -1.76287 |             0.166667 | True                | success  |
| factual_002   | factual    |         6 |            2 |        11 |       0.733333 |           0.906888 |             9.97577 |             -1.96877 |             0.166667 | True                | success  |
| factual_003   | factual    |         6 |            2 |        11 |       0.733333 |           0.871388 |             9.58527 |             -1.95994 |             0.166667 | True                | success  |
| factual_004   | factual    |         6 |            2 |        11 |       0.733333 |           0.745487 |             8.20035 |             -1.89799 |             0.166667 | True                | success  |
| factual_005   | factual    |         6 |            2 |        11 |       0.733333 |           0.796307 |             8.75937 |             -1.9244  |             0.166667 | True                | success  |
| reasoning_001 | reasoning  |         6 |            3 |         6 |       0.4      |           0.570262 |             3.42157 |             -1.5064  |             0.166667 | False               | success  |
| reasoning_002 | reasoning  |         6 |            3 |         8 |       0.533333 |           0.635109 |             5.08088 |             -1.66546 |             0.166667 | False               | success  |
