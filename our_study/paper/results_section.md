Results

1. Experimental Overview

We evaluated the SeSE structural-uncertainty framework through a set of complementary experiments designed to assess its behavior under controlled semantic variation, perturbation, repeated evaluation, increasing response complexity, and known failure conditions. The experimental suite comprised five robustness studies together with a scaled evaluation.

The scaled evaluation contained 7 questions and 42 responses, with six responses generated for each question. The remaining experiments evaluated threshold sensitivity, semantic perturbation, score stability, semantic/reasoning complexity, and failure mechanisms. All structural-entropy calculations used the original SeSE implementation rather than a replacement entropy definition.

2. Scaled Evaluation

The scaled evaluation included five factual questions and two reasoning questions. Each case contained six responses and was evaluated using the SeSE semantic-graph construction followed by the original structural-entropy calculation.

Across the five factual cases, the response sets exhibited a consistent majority/minority structure. Each factual case contained five correct responses and one incorrect response. The incorrect response formed a singleton semantic cluster, while the five correct responses formed the dominant cluster. Thus, all five factual cases were classified as confident failures under the experiment's predefined failure criterion.

The five factual cases were:

Who discovered penicillin?

What is the capital of France?

Which planet is known as the Red Planet?

What is the largest planet in our solar system?

What gas do humans need to breathe?

For each factual case, the incorrect-response fraction was 1/6 (0.1667), with two semantic clusters of sizes 5 and 1 and a cluster imbalance of 5.0.

The two reasoning cases produced more distributed semantic structures. The transitivity case produced three clusters with sizes 3, 2, and 1, while the divisibility case produced three clusters with sizes 4, 1, and 1. Neither reasoning case was classified as a confident failure.

These results provide pilot-scale evidence that semantic graph structure can distinguish a minority incorrect factual response from a majority of mutually consistent responses. However, the seven-case sample is insufficient to establish general performance across datasets or domains.

3. Threshold Sensitivity

Structural entropy was evaluated across five clustering thresholds. The observed structural-entropy range was approximately 0.000198, indicating limited entropy variation across the tested threshold conditions.

The number of clusters changed within the tested threshold range, demonstrating that graph partitioning itself can be threshold-sensitive even when the resulting structural-entropy values remain relatively stable.

This result suggests that, within the tested range, the structural-entropy metric was comparatively stable to clustering-threshold variation. It does not establish threshold invariance outside the evaluated range.

4. Semantic Perturbation

The perturbation experiment evaluated changes to semantic graph structure through edge-weight noise and edge dropout. The experiment contained 24 perturbation observations.

Edge-weight noise produced measurable changes in structural entropy. The maximum observed relative entropy change was approximately 0.3209 at the strongest tested noise condition, accompanied by a relative graph change of approximately 0.2443.

Edge dropout produced a smaller maximum relative entropy change of approximately 0.1443. At the highest tested dropout level, the reported relative graph change was approximately 0.000406.

Together, these observations indicate that structural entropy responds to modifications of semantic graph edge structure, with the magnitude of the response depending on the perturbation mechanism. The results should be interpreted as sensitivity measurements rather than evidence of a causal relationship.

5. Score Stability

Score stability was evaluated using 11 repeated observations. Structural entropy exhibited a standard deviation of approximately 0.8492 and an observed range of approximately 2.2601 across the available repeats.

The observed variation indicates that repeated evaluation can produce non-trivial changes in structural entropy under the conditions represented in the stability dataset. This is important when interpreting individual entropy scores: a single score should not automatically be treated as invariant or perfectly reproducible.

The stability experiment therefore motivates repeated sampling and uncertainty intervals in future larger-scale evaluations.

6. Semantic and Reasoning Complexity

The complexity experiment evaluated five complexity conditions. Structural entropy varied across these conditions, with an observed entropy range of approximately 0.4230.

The result indicates that response-set complexity is associated with measurable variation in the resulting structural-entropy values in the tested conditions. However, the current experiment does not establish whether complexity has a monotonic relationship with entropy or whether the observed differences generalize to other datasets.

7. Failure Mechanisms

The failure-mechanism study contained three evaluated cases. Two cases were classified as confident failures. Across the tested cases, the mean incorrect-response fraction was 0.3333, while the mean cluster imbalance was 2.6667.

The failure cases provide controlled examples in which graph structure and response correctness can be examined jointly. In particular, the scaled factual evaluation demonstrates a recurring pattern in which an incorrect response occupies a small semantic cluster separated from the dominant correct-response cluster.

These observations motivate further investigation of whether structural features such as minority-cluster size, cluster imbalance, and edge connectivity can serve as useful indicators of response-level failure.

8. Consolidated Findings

Across the experimental suite, four main observations emerge.

First, the scaled factual evaluation showed a consistent semantic separation between the incorrect response and the majority of correct responses. All five factual cases exhibited a singleton incorrect-response cluster.

Second, structural entropy was comparatively stable across the five tested clustering thresholds, with an observed entropy range of approximately 0.000198.

Third, controlled graph perturbations produced measurable changes in structural entropy, demonstrating that the metric responds to changes in semantic edge structure.

Fourth, structural entropy varied across repeated evaluations and complexity conditions, indicating that the metric is sensitive to both evaluation variability and response-set structure.

Taken together, these results provide preliminary empirical support for using semantic graph structure and structural entropy as objects of analysis for response uncertainty and failure behavior. They do not, by themselves, establish calibrated error probabilities, broad generalization, causal mechanisms, or statistical significance across datasets.

9. Scope of the Evidence

The present results should be regarded as a pilot experimental evaluation. The scaled evaluation contains only seven questions, and the robustness experiments use relatively small controlled samples. The findings therefore demonstrate measurable behaviors of the SeSE framework under the tested conditions rather than providing a comprehensive benchmark of uncertainty estimation.

Future validation should expand the number and diversity of questions, include multiple datasets and domains, increase repeated sampling, pre-register statistical analyses where appropriate, and evaluate whether the observed structural indicators remain predictive under independently constructed response sets.

10. Reproducibility

All reported results were generated from the experiment outputs in the SeSE study directory. The final synthesis incorporated results from:

threshold sensitivity;

semantic perturbation;

score stability;

semantic/reasoning complexity;

failure mechanisms; and

scaled evaluation.

The structural-entropy calculation remained tied to the original SeSE implementation throughout the analysis, preserving the original metric definition for the experimental comparisons.