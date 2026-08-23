# Candidate Research Claims

These are deliberately conservative claims generated from the current experimental evidence. They should be validated against the underlying result tables before being used in a paper.

## Claim 1 — Threshold robustness

Across the tested clustering thresholds, structural entropy varied by approximately 0.000198. The tested threshold range therefore does not show large entropy instability, although cluster assignments can change.

## Claim 2 — Structural perturbation sensitivity

Edge-weight perturbations produced measurable changes in structural entropy, reaching an absolute relative change of approximately 0.3209 at the strongest tested condition. This provides evidence that the measured structural entropy can respond to perturbations of semantic edge weights under the tested conditions.

## Claim 3 — Complexity dependence

Structural entropy varied across the tested semantic/reasoning complexity conditions, with an observed range of approximately 0.422950. This motivates further testing of whether graph complexity systematically affects uncertainty behavior.

## Claim 4 — Failure mechanisms

The failure-mechanism experiment identified 2 confident-failure case(s) within the tested examples. These cases provide motivation for further examination of structural properties of semantic graphs in situations where uncertainty is incorrectly high.

## Claim 5 — Scaled evaluation

The Phase 2 scaled evaluation covered 7 cases and 42 responses. The results provide a broader pilot-scale check of structural entropy behavior across factual and reasoning cases. Because the current run used the SeSE original-response fallback when enhancement requests were unavailable, this should be interpreted as a scaled evaluation of the fallback/original-response path rather than a fully enhancement-enabled evaluation.

## What We Cannot Yet Claim

- We cannot claim generalization across datasets from these experiments alone.
- We cannot claim calibrated probabilities of error.
- We cannot claim causal mechanisms from the current observational structural analyses.
- We cannot claim broad statistical significance from the current small experimental sample.
- We should not present these results as replacing or modifying the original SeSE method.

## Recommended Next Stage

The next stage should be replication at larger scale: more questions, multiple datasets, repeated sampling, and predefined statistical analyses. The purpose is to determine whether the patterns observed here persist beyond the current pilot-scale experiments.
