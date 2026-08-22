# SeSE Phase 2 — Scaled Evaluation

This report summarizes the scaled evaluation using the original, unmodified SeSE semantic graph-construction function.

## Configuration

- Cases attempted: 7
- Successful cases: 7
- Failed cases: 0
- Responses per case: nominally 6
- Recorded clustering threshold: 0.30
- Original SeSE implementation: UNMODIFIED
- Graph API: build_semantic_graph(responses, question, batch_size=128)

## Important implementation note

The original SeSE graph constructor does not expose `threshold` as a function argument. The scaled evaluation therefore passes the question explicitly and does not inject a threshold argument into the original function.

## Successful cases

| case_id       | category   |   n_responses |   n_nodes |   n_clusters |   n_edges |   edge_density |   mean_edge_weight |   total_edge_weight |   structural_entropy |
|:--------------|:-----------|--------------:|----------:|-------------:|----------:|---------------:|-------------------:|--------------------:|---------------------:|
| factual_001   | factual    |             6 |         6 |            1 |        15 |       1.000000 |           0.701967 |           10.529501 |            -1.746987 |
| factual_002   | factual    |             6 |         6 |            1 |        15 |       1.000000 |           0.997929 |           14.968942 |            -1.791759 |
| factual_003   | factual    |             6 |         6 |            1 |        15 |       1.000000 |           0.991779 |           14.876680 |            -1.791741 |
| factual_004   | factual    |             6 |         6 |            1 |        15 |       1.000000 |           0.839492 |           12.592382 |            -1.783497 |
| factual_005   | factual    |             6 |         6 |            1 |        15 |       1.000000 |           0.892984 |           13.394761 |            -1.789280 |
| reasoning_001 | reasoning  |             6 |         6 |            1 |         8 |       0.533333 |           0.765696 |            6.125569 |            -1.711617 |
| reasoning_002 | reasoning  |             6 |         6 |            1 |        15 |       1.000000 |           0.472623 |            7.089350 |            -1.710608 |

## Failed cases

No cases failed.

## Aggregate results

| metric                  |     value |
|:------------------------|----------:|
| total_cases             |  7.000000 |
| successful_cases        |  7.000000 |
| failed_cases            |  0.000000 |
| mean_structural_entropy | -1.760784 |
| std_structural_entropy  |  0.037352 |
| min_structural_entropy  | -1.791759 |
| max_structural_entropy  | -1.710608 |
| mean_n_clusters         |  1.000000 |
| std_n_clusters          |  0.000000 |
| min_n_clusters          |  1.000000 |
| max_n_clusters          |  1.000000 |
| mean_n_edges            | 14.000000 |
| std_n_edges             |  2.645751 |
| min_n_edges             |  8.000000 |
| max_n_edges             | 15.000000 |
| mean_edge_density       |  0.933333 |
| std_edge_density        |  0.176383 |
| min_edge_density        |  0.533333 |
| max_edge_density        |  1.000000 |
| mean_mean_edge_weight   |  0.808924 |
| std_mean_edge_weight    |  0.184195 |
| min_mean_edge_weight    |  0.472623 |
| max_mean_edge_weight    |  0.997929 |
| mean_total_edge_weight  | 11.368169 |
| std_total_edge_weight   |  3.591135 |
| min_total_edge_weight   |  6.125569 |
| max_total_edge_weight   | 14.968942 |
