# Limitations

## 1. Pilot-Scale Sample Size

The primary limitation of the current study is the size of the evaluation.

The scaled evaluation contains only 7 cases:

- 5 factual cases
- 2 reasoning cases
- 6 responses per case
- 42 responses in total

The five factual cases all exhibit the same `[5,1]` cluster structure, while the two reasoning cases produce `[3,2,1]` and `[4,1,1]` structures.

This repeated pattern is useful as an initial observation, but seven questions are insufficient to estimate how frequently these structures occur in a broader population of questions.

The results therefore support reporting the observed patterns, but not population-level estimates of SeSE performance.

## 2. Limited Number of Reasoning Cases

Only two reasoning cases were included in the scaled evaluation.

`reasoning_001` produced cluster sizes `[3,2,1]`, while `reasoning_002` produced `[4,1,1]`. Neither was classified as a confident failure.

Because there are only two reasoning cases, these results cannot establish a general distinction between factual and reasoning questions.

In particular, the current evidence cannot determine whether the more fragmented reasoning structures are characteristic of reasoning tasks generally or are specific to these two examples.

A larger reasoning evaluation is required before making category-level claims.

## 3. Controlled Error Composition

Each factual scaled-evaluation case contains exactly one incorrect response and five correct responses.

Consequently, the observed incorrect fraction is `0.1667` for all five factual cases.

This controlled composition makes the structural pattern easy to inspect, but it does not reproduce the full distribution of errors that would occur in an unconstrained model-response dataset.

The finding that the incorrect response formed a singleton cluster in all five factual cases should therefore be interpreted as a result under the tested response composition rather than as a general estimate of error-detection performance.

## 4. Correctness Labels Were Available During Evaluation

The current experiments use known correctness information to characterize the resulting clusters and failure mechanisms.

For example, in every factual case the cluster-level incorrect counts were `[0,1]`, while the cluster sizes were `[5,1]`.

This allows the study to determine that the singleton cluster contained the incorrect response.

However, this is different from demonstrating prospective prediction.

The current experiments therefore do not establish that SeSE can identify an incorrect response without access to its correctness label.

A future predictive evaluation should determine structural indicators first and compare them against correctness labels only after the structural analysis has been completed.

## 5. No Independent Generalization Dataset

The current results are generated from the available experimental cases and controlled perturbation conditions.

The study does not yet contain a large independent test dataset specifically reserved for evaluating whether the observed structural patterns generalize.

Therefore, the results cannot establish generalization across:

- datasets,
- domains,
- question distributions,
- language models,
- response-generation settings, or
- naturally occurring error distributions.

An independent held-out evaluation is required for such claims.

## 6. Threshold Sensitivity Was Tested Over a Limited Range

The threshold-sensitivity experiment evaluated 5 clustering thresholds.

Across those conditions, the observed structural-entropy range was `0.000198`, while the cluster-count range was `1`.

This provides evidence of relatively small entropy variation over the tested range.

It does not establish that structural entropy is insensitive to clustering thresholds in general.

Thresholds outside the tested range could produce substantially different graph structures or entropy values.

The appropriate conclusion is therefore limited to the tested threshold conditions.

## 7. Perturbation Experiments Do Not Define Universal Robustness Bounds

The semantic perturbation experiment contains 24 observations.

The maximum observed relative entropy change was:

- `0.320876` for edge-weight noise;
- `0.144263` for edge dropout.

At the maximum tested perturbation level, the corresponding graph changes were:

- `0.244347` for edge-weight noise;
- `0.000406` for edge dropout.

These values quantify the behavior observed under the tested perturbations.

They should not be interpreted as universal upper or lower bounds on SeSE sensitivity.

Different response sets, graph sizes, edge distributions, or perturbation magnitudes could produce different results.

## 8. Repeated Evaluation Shows Variation but Does Not Identify Its Cause

The score-stability experiment contains 11 repeated evaluations.

The observed structural-entropy standard deviation was `0.849235`, with a range of `2.260093`.

This demonstrates substantial variation across the available repeated evaluations.

However, the current experiment does not isolate the source of that variation.

The observed changes could be associated with variation in generated responses or other stochastic components of the evaluation pipeline. The present data do not provide a controlled decomposition of those sources.

Therefore, the result supports reporting repeat-to-repeat variability but does not establish a specific causal mechanism for that variability.

## 9. Complexity Was Represented by Only Five Conditions

The complexity experiment evaluates 5 complexity conditions and observes a structural-entropy range of `0.422950`.

This demonstrates variation across the tested conditions.

However, five conditions are insufficient to establish the shape of a complexity–entropy relationship.

The current experiment therefore cannot establish:

- monotonicity,
- linearity,
- a threshold effect,
- a saturation effect, or
- a statistically validated complexity–entropy relationship.

A larger number of predefined complexity levels with repeated measurements would be required.

## 10. Failure-Mechanism Sample Is Small

The failure-mechanism experiment contains only 3 cases.

Two cases were classified as confident failures.

The mean incorrect-response fraction was `0.333333`, and the mean cluster imbalance was `2.666667`.

These values are descriptive statistics for the three tested cases.

They are not sufficient to estimate the prevalence of confident failures or establish cluster imbalance as a statistically validated predictor of failure.

The experiment should therefore be treated as a mechanism-oriented pilot rather than a predictive evaluation.

## 11. Structural Entropy Is Not Evaluated as a Calibrated Probability

The current experiments report structural-entropy values such as:

- `-1.762871` for `factual_001`;
- `-1.968769` for `factual_002`;
- `-1.506396` for `reasoning_001`.

The study does not establish a mapping between these values and probabilities of correctness.

No calibration analysis is performed, and no probability interpretation is assigned to a particular entropy value.

Consequently, the current results cannot support statements such as "an entropy value of X corresponds to Y% probability of error."

## 12. No Statistical Significance Claims

The current experimental sample sizes are too small for broad statistical significance claims.

The scaled evaluation contains 7 cases.

The failure-mechanism experiment contains 3 cases.

The complexity experiment contains 5 conditions.

The threshold-sensitivity experiment contains 5 thresholds.

Although the perturbation and stability experiments contain more observations, they are still generated under controlled experimental conditions rather than constituting a large independent population sample.

The current paper should therefore emphasize effect magnitudes and observed structural patterns rather than population-level significance claims.

## 13. The Experiments Are Descriptive Rather Than Causal

The experiments identify associations between graph structure, clustering, perturbations, complexity conditions, and structural entropy.

They do not establish causal relationships.

For example, the observation that an incorrect factual response occupies a singleton cluster does not establish that singleton clustering causes the response to be incorrect.

Likewise, the observation that edge-weight noise changes entropy does not establish a causal relationship between semantic noise and model uncertainty.

Controlled causal experiments would require explicitly manipulating the relevant variable while controlling other factors.

## 14. Limited Diversity of Models and Response Sources

The current scaled evaluation contains 42 responses across 7 cases.

The available results do not establish broad coverage across model families, model sizes, decoding strategies, or response-generation configurations.

Therefore, the observed graph structures cannot yet be assumed to be model-independent.

A stronger evaluation should repeat the same question sets across multiple response-generating systems and sampling configurations.

## 15. Limited Evaluation of Naturalistic Errors

The factual scaled evaluation uses controlled response sets containing a known incorrect response.

This is useful for testing whether the semantic graph can structurally separate a deliberately included minority error.

It does not establish how SeSE behaves when errors arise naturally during model generation.

Naturalistic errors can differ in wording, severity, factual specificity, and semantic similarity to correct responses.

A future evaluation should therefore include naturally generated response sets in which incorrect responses are not manually selected to create a particular cluster configuration.

## 16. No Claim of Universal Hallucination Detection

The present experiments should not be described as demonstrating universal hallucination detection.

The strongest available evidence is narrower:

In all five tested factual cases, the known incorrect response occupied a singleton cluster while the five correct responses occupied the dominant cluster.

This is a reproducible pattern within the current controlled sample.

It is not a measured hallucination-detection accuracy across a broad benchmark.

Any claim of hallucination-detection performance would require an independently labeled dataset, predefined prediction rules, and standard evaluation metrics such as precision, recall, and false-positive rate.

## 17. No Claim That Factual Questions Are Inherently Lower-Entropy

The scaled results show that the five factual cases had structural-entropy values between `-1.968769` and `-1.762871`, while the two reasoning cases had values of `-1.506396` and `-1.665463`.

This is an observed separation in the current seven cases.

It does not establish that factual questions inherently produce lower structural entropy than reasoning questions.

The number of cases is too small, and the categories contain different response structures.

The correct interpretation is that the tested factual and reasoning cases occupied different entropy ranges in this evaluation.

## 18. Original SeSE Implementation Remains the Reference

The study computes structural entropy using the original SeSE `compute_se` implementation.

The semantic graph is constructed using the original SeSE graph-construction implementation with the required question argument.

This preserves methodological continuity with the original implementation.

The limitation is therefore not that the study replaces the original metric, but that the present experiments evaluate only a limited set of conditions around that implementation.

The findings should be understood as empirical observations about the original SeSE methodology under the tested conditions.

## 19. Current Evidence Does Not Establish a Universal Decision Rule

The current experiments do not justify a universal rule such as:

> "If structural entropy is above or below a particular value, classify the response as incorrect."

No such threshold has been validated.

Similarly, the experiments do not establish that a particular cluster imbalance, edge density, or singleton-cluster configuration should universally trigger a failure classification.

The `confident_failure` outcomes observed in the current experiments are properties of the implemented experimental procedure and tested cases.

A future study must define a prediction rule independently of the evaluation labels and test that rule on held-out data.

## 20. Scope of the Current Conclusions

The conclusions supported by the current evidence are deliberately narrow.

The study demonstrates that:

1. all five tested factual cases produced a `[5,1]` cluster structure;
2. the incorrect response was located in the singleton cluster in all five factual cases;
3. both tested reasoning cases produced more fragmented cluster structures;
4. threshold variation across the five tested settings produced only `0.000198` structural-entropy range;
5. edge-weight noise produced a maximum relative entropy change of `0.320876`;
6. edge dropout produced a maximum relative entropy change of `0.144263`;
7. repeated evaluation produced a structural-entropy standard deviation of `0.849235`;
8. the repeated-evaluation entropy range was `2.260093`;
9. the five complexity conditions produced an entropy range of `0.422950`; and
10. two of the three failure-mechanism cases were classified as confident failures.

These observations are sufficient to motivate a larger validation study.

They are not sufficient to establish general-purpose error detection, calibrated uncertainty estimation, causal explanations, or broad statistical generalization.

## 21. Required Next Validation

The limitations above define the next experimental requirements directly.

A stronger validation should include:

- substantially more questions than the current 7-case scaled evaluation;
- substantially more reasoning cases than the current 2;
- multiple datasets and domains;
- multiple response-generating models or configurations;
- independently held-out evaluation data;
- naturalistic rather than exclusively controlled errors;
- repeated sampling for each question;
- predefined structural prediction rules;
- correctness evaluation performed after structural analysis;
- confidence intervals or other uncertainty estimates;
- predefined statistical tests;
- explicit evaluation of precision, recall, false-positive rate, and related predictive metrics where a classifier is proposed.

Until these conditions are met, the current study should be presented as a pilot-scale quantitative evaluation of SeSE rather than as a final validation of its general predictive performance.