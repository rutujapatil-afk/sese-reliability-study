# Discussion

## 1. Main Finding: Factual Errors Produced a Consistent Singleton-Cluster Pattern

The clearest result in the scaled evaluation is the difference between the five factual cases and the two reasoning cases.

All five factual cases contained six responses, with five responses representing the correct answer and one response representing an incorrect answer. In every factual case, the five correct responses formed one cluster of size five while the incorrect response formed a singleton cluster of size one. The resulting cluster structure was therefore identical across all five factual cases: `[5, 1]`.

This pattern was observed for:

- `factual_001` — "Who discovered penicillin?"
- `factual_002` — "What is the capital of France?"
- `factual_003` — "Which planet is known as the Red Planet?"
- `factual_004` — "What is the largest planet in our solar system?"
- `factual_005` — "What gas do humans need to breathe?"

The numerical graph structure was also identical across these five cases: six nodes, eleven edges, and an edge density of `0.7333`. The incorrect-response fraction was `0.1667` in every case, corresponding to one incorrect response out of six.

Most importantly, all five factual cases were classified as `confident_failure = True`.

The reasoning cases did not show this same pattern. `reasoning_001` produced three clusters of sizes `[3, 2, 1]`, while `reasoning_002` produced `[4, 1, 1]`. Both were classified as `confident_failure = False`.

Thus, within this seven-case evaluation, the singleton-cluster pattern was present in all five factual cases and absent from both reasoning cases. This is a direct empirical difference between the two tested categories.

## 2. Factual Cases Were Structurally More Uniform Than Reasoning Cases

The factual cases were not only similar in their cluster structure; they also produced the same number of nodes and edges.

Each factual case produced:

- `n_nodes = 6`
- `n_edges = 11`
- `edge_density = 0.7333`
- `n_clusters = 2`
- `largest_cluster = 5`
- `smallest_cluster = 1`
- `cluster_imbalance = 5`

The reasoning cases were structurally different.

`reasoning_001` produced six nodes and six edges, with an edge density of `0.4000` and three clusters of sizes `[3, 2, 1]`.

`reasoning_002` produced six nodes and eight edges, with an edge density of `0.5333` and three clusters of sizes `[4, 1, 1]`.

Therefore, the factual and reasoning groups differed simultaneously in cluster count, cluster-size distribution, and graph density. The factual cases consistently formed a dense majority cluster plus one isolated minority response, whereas the reasoning cases produced more fragmented response structures.

The present data therefore support a specific observation: the tested factual response sets were structurally more concentrated than the tested reasoning response sets.

They do not establish that factual questions are always more structurally concentrated than reasoning questions. Only five factual and two reasoning cases were evaluated.

## 3. The Incorrect Responses Were Isolated in Every Factual Case

The failure pattern is particularly direct because the incorrect response count was exactly one in each factual case.

For `factual_001` through `factual_005`, the cluster-level incorrect-response counts were `[0, 1]`, while the cluster sizes were `[5, 1]`. The corresponding cluster incorrect fractions were `[0.0, 1.0]`.

This means that the dominant cluster contained five responses and zero incorrect responses, while the singleton cluster contained one response and that response was incorrect.

The same relationship occurred five times.

This is stronger than simply observing that the overall incorrect fraction was `0.1667`. The overall fraction alone says that one of six responses was incorrect. The cluster-level values show where that incorrect response was located in the semantic structure: entirely inside the minority singleton cluster.

This is the specific structural pattern that supports further investigation of cluster-level features as potential indicators of response failure.

However, because the correctness labels were known during these controlled experiments, this result should not be interpreted as an independently validated prediction of correctness. A future evaluation must apply the structural criterion without using the known labels and then test its predictions against unseen correctness labels.

## 4. The Reasoning Cases Showed a Different Failure Structure

The two reasoning cases provide a useful direct contrast.

For `reasoning_001`, the cluster sizes were `[3, 2, 1]`. The cluster incorrect counts were `[0, 0, 1]`, meaning that the incorrect response was again located in a singleton cluster. However, the case was not classified as a confident failure.

For `reasoning_002`, the cluster sizes were `[4, 1, 1]`, and the cluster incorrect counts were `[0, 0, 1]`. Again, the incorrect response occupied a singleton cluster, but the case was not classified as a confident failure.

This is important because it prevents an overly strong interpretation of the factual result.

A singleton incorrect-response cluster by itself was not sufficient to produce a confident-failure classification in the two reasoning cases. The factual cases had a `[5,1]` structure, whereas the reasoning cases had `[3,2,1]` and `[4,1,1]` structures.

Therefore, the present results indicate that the relationship between minority-cluster structure and the `confident_failure` classification depends on the complete graph and clustering configuration rather than on singleton membership alone.

## 5. Structural Entropy Varied Across the Seven Scaled Cases

The structural-entropy values in the scaled evaluation were:

| Case | Structural entropy |
|---|---:|
| factual_001 | -1.762871 |
| factual_002 | -1.968769 |
| factual_003 | -1.959936 |
| factual_004 | -1.897995 |
| factual_005 | -1.924397 |
| reasoning_001 | -1.506396 |
| reasoning_002 | -1.665463 |

The five factual values ranged from `-1.968769` to `-1.762871`, while the two reasoning values were `-1.506396` and `-1.665463`.

The reasoning cases therefore had less-negative entropy values than every factual case in this particular seven-case sample.

This is an observed separation in the present dataset, but it should not be interpreted as evidence that structural entropy universally distinguishes factual from reasoning questions. The sample contains only seven cases and was not designed to estimate a category-level effect size.

The appropriate conclusion is narrower: in the present scaled evaluation, the two reasoning cases occupied a different structural-entropy range from the five factual cases.

## 6. Threshold Sensitivity Was Low for Structural Entropy

The threshold-sensitivity experiment evaluated five clustering thresholds.

Across those five thresholds, the observed structural-entropy range was only `0.000198`. The cluster count changed by a range of `1`.

This means that the structural-entropy value changed very little across the tested threshold settings, even though the clustering structure was not completely unchanged.

The direct implication is that the entropy statistic was comparatively stable within this specific threshold range.

This result is important because the scaled evaluation used a clustering threshold of `0.3`. The threshold-sensitivity experiment therefore provides supporting evidence that the entropy measurement is not highly unstable around the tested clustering configuration.

However, the result only covers five tested thresholds. It does not justify claiming threshold invariance outside that range.

## 7. Edge-Weight Noise Had a Larger Effect on Entropy Than Edge Dropout

The perturbation experiment produced a clear quantitative difference between the two tested perturbation mechanisms.

Under edge-weight noise, the maximum observed relative entropy change was `0.320876`.

Under edge dropout, the maximum observed relative entropy change was `0.144263`.

The maximum relative entropy change under edge-weight noise was therefore more than twice the maximum observed under edge dropout in the tested conditions.

The graph-change measurements also differed substantially. At the maximum tested perturbation level, edge-weight noise produced a graph change of `0.244347`, whereas edge dropout produced a graph change of only `0.000406`.

Thus, the two perturbation experiments should not be treated as equivalent stress tests. The observed entropy response was substantially larger for the tested edge-weight noise condition.

This establishes sensitivity under the tested perturbations, but it does not establish that edge-weight noise is inherently more important than edge dropout in all SeSE graphs. The perturbation magnitudes and graph structures determine the observed response.

## 8. Repeated Evaluation Revealed Substantial Score Variation

The score-stability experiment contained 11 repeated evaluations.

The structural-entropy standard deviation was `0.849235`, and the observed range was `2.260093`.

Compared with the threshold-sensitivity result of `0.000198`, this is a substantially larger source of observed entropy variation.

The direct comparison is therefore important:

- threshold variation in the tested experiment produced an entropy range of `0.000198`;
- repeated evaluation produced an entropy range of `2.260093`.

The difference shows that the observed entropy variation associated with repeated evaluation was much larger than the variation observed across the tested clustering thresholds.

This suggests that repeat-to-repeat variation deserves more attention than threshold variation when interpreting individual entropy values under the present experimental conditions.

The result does not identify the cause of the repeat variation. It could arise from changes in generated responses, graph construction inputs, or other stochastic components of the evaluation. Additional controlled repetitions would be required to isolate those sources.

## 9. Complexity Conditions Produced Measurable Entropy Differences

The complexity experiment evaluated five conditions and produced a structural-entropy range of `0.422950`.

This value is substantially larger than the `0.000198` entropy range observed in the threshold-sensitivity experiment.

The direct comparison shows that the tested complexity conditions produced more variation in structural entropy than the tested clustering-threshold changes.

However, the experiment does not establish a monotonic relationship between complexity and entropy. The current result only demonstrates that changing the tested complexity condition was associated with a measurable change in structural entropy.

To establish a complexity relationship, future experiments would need more levels, repeated measurements at each level, and a predefined quantitative definition of complexity.

## 10. Failure-Mechanism Results Are Consistent With the Scaled Factual Pattern

The failure-mechanism experiment evaluated three cases and identified two confident failures.

Across those three cases, the mean incorrect-response fraction was `0.333333`, and the mean cluster imbalance was `2.666667`.

The scaled evaluation provides a more detailed example of the same type of structural relationship. In all five factual cases, the incorrect response occupied a singleton cluster while the correct responses occupied the dominant cluster.

The two experiments therefore point in the same direction: incorrect responses can occur in structurally distinct minority clusters.

The evidence is still too small to determine whether cluster imbalance, singleton membership, or another graph statistic is the most useful predictor. The failure-mechanism dataset contains only three cases, and the scaled evaluation contains only seven.

## 11. The Experiments Do Not Support a Single Universal Entropy Interpretation

The results show several distinct sources of structural-entropy variation:

- threshold sensitivity: `0.000198` range;
- semantic perturbation: up to `0.320876` relative change under edge-weight noise;
- score stability: `0.849235` standard deviation and `2.260093` range;
- complexity: `0.422950` range;
- scaled evaluation: distinct entropy values across factual and reasoning cases.

These results demonstrate that the structural-entropy value depends on the response-set structure and the experimental conditions.

Consequently, an entropy value should not be interpreted independently of the response set, graph construction, clustering configuration, and evaluation procedure.

The current experiments do not establish a universal numerical threshold at which a SeSE score should be interpreted as "certain," "uncertain," "correct," or "incorrect."

## 12. Methodological Consistency With Original SeSE

The scaled evaluation uses the original SeSE graph-construction function:

`build_semantic_graph(responses, question, batch_size=128)`

The required `question` argument is explicitly supplied to the original implementation.

Structural entropy is also computed using the original SeSE `compute_se` implementation rather than a replacement entropy formula.

This matters because the objective of the present work is to evaluate the original SeSE methodology rather than introduce a new structural-entropy definition.

The observed results should therefore be interpreted as measurements generated by the original SeSE graph and entropy machinery under the experimental conditions described above.

## 13. What the Current Evidence Actually Establishes

The completed experiments establish five concrete observations.

First, all five tested factual cases produced the same `[5,1]` cluster structure, with the incorrect response isolated in the singleton cluster.

Second, the two tested reasoning cases produced `[3,2,1]` and `[4,1,1]` cluster structures and were not classified as confident failures.

Third, structural entropy changed very little across the five tested clustering thresholds, with a range of `0.000198`.

Fourth, structural entropy showed substantially larger variation under repeated evaluation and controlled graph perturbation, including a `0.849235` standard deviation across 11 stability observations and a maximum relative change of `0.320876` under edge-weight noise.

Fifth, structural entropy varied across the five tested complexity conditions, with a range of `0.422950`.

These are the direct findings supported by the current data.

## 14. What These Results Do Not Establish

The current results do not establish that SeSE can reliably detect hallucinations across arbitrary datasets.

They do not establish calibrated probabilities of correctness or error.

They do not establish that singleton clusters are a universal indicator of incorrect responses.

They do not establish that factual questions necessarily produce lower structural entropy than reasoning questions.

They do not establish a causal relationship between graph structure and model failure.

They do not establish statistical significance or population-level effect sizes.

They do not establish that the observed perturbation responses generalize to other graph sizes, response distributions, models, or perturbation magnitudes.

These limitations follow directly from the size and design of the current experiments.

## 15. Implication for the Next Experimental Stage

The next stage should directly test whether the structural patterns observed here survive larger and independent evaluations.

The most important test is whether the `[majority cluster + minority incorrect cluster]` pattern observed in all five factual cases remains present when the number of questions is increased substantially.

The second test is whether the distinction between the factual and reasoning structures remains after evaluating many more examples of each category.

The third test is whether cluster-level structural features predict correctness when correctness labels are withheld during the structural analysis and evaluated only afterward.

The fourth test is whether the large repeat-to-repeat entropy variation observed in the stability experiment persists under a controlled repeated-sampling protocol.

The fifth test is whether the perturbation response remains consistent across multiple graph sizes and response distributions.

These experiments would convert the current structural observations into quantitative tests of generalization and predictive validity.

## 16. Overall Interpretation

The strongest result from the completed study is not a universal entropy threshold. It is the repeated structural separation observed in the five factual cases.

In every factual case, five correct responses formed the dominant cluster and one incorrect response formed a singleton cluster. In both reasoning cases, the response structures were more fragmented and neither case was classified as a confident failure.

At the same time, the robustness experiments show that entropy itself is affected differently by threshold selection, graph perturbation, repeated evaluation, and complexity.

Taken together, the results support a specific conclusion: **SeSE produces measurable structural differences between the response sets examined in this study, and those differences are particularly clear in the five controlled factual cases.**

The evidence is sufficient to justify a larger validation study. It is not sufficient to claim that these structural patterns constitute a generally validated uncertainty estimator or error detector.