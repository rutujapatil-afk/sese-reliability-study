# Tables

## Table 1. Experimental inventory

<table>
<thead>
<tr>
<th>Experiment</th>
<th>Observations / conditions</th>
<th>Purpose</th>
</tr>
</thead>
<tbody>
<tr>
<td>Scaled evaluation</td>
<td>7 cases; 42 responses</td>
<td>Evaluate semantic graph structure and failure behavior across factual and reasoning cases</td>
</tr>
<tr>
<td>Threshold sensitivity</td>
<td>5 thresholds</td>
<td>Assess sensitivity to clustering-threshold selection</td>
</tr>
<tr>
<td>Semantic perturbation</td>
<td>24 observations</td>
<td>Assess sensitivity to controlled graph perturbations</td>
</tr>
<tr>
<td>Score stability</td>
<td>11 repeats</td>
<td>Assess variation across repeated evaluations</td>
</tr>
<tr>
<td>Complexity</td>
<td>5 complexity conditions</td>
<td>Examine entropy variation across semantic/reasoning complexity</td>
</tr>
<tr>
<td>Failure mechanisms</td>
<td>3 cases</td>
<td>Examine structural characteristics associated with incorrect responses</td>
</tr>
</tbody>
</table>

## Table 2. Scaled evaluation results

<table>
<thead>
<tr>
<th>Case</th>
<th>Category</th>
<th>Responses</th>
<th>Nodes</th>
<th>Edges</th>
<th>Edge density</th>
<th>Structural entropy</th>
<th>Clusters</th>
<th>Cluster sizes</th>
<th>Incorrect fraction</th>
<th>Confident failure</th>
</tr>
</thead>
<tbody>
<tr>
<td>factual_001</td>
<td>Factual</td>
<td>6</td>
<td>6</td>
<td>11</td>
<td>0.7333</td>
<td>-1.762871</td>
<td>2</td>
<td>5, 1</td>
<td>0.1667</td>
<td>Yes</td>
</tr>
<tr>
<td>factual_002</td>
<td>Factual</td>
<td>6</td>
<td>6</td>
<td>11</td>
<td>0.7333</td>
<td>-1.968769</td>
<td>2</td>
<td>5, 1</td>
<td>0.1667</td>
<td>Yes</td>
</tr>
<tr>
<td>factual_003</td>
<td>Factual</td>
<td>6</td>
<td>6</td>
<td>11</td>
<td>0.7333</td>
<td>-1.959936</td>
<td>2</td>
<td>5, 1</td>
<td>0.1667</td>
<td>Yes</td>
</tr>
<tr>
<td>factual_004</td>
<td>Factual</td>
<td>6</td>
<td>6</td>
<td>11</td>
<td>0.7333</td>
<td>-1.897995</td>
<td>2</td>
<td>5, 1</td>
<td>0.1667</td>
<td>Yes</td>
</tr>
<tr>
<td>factual_005</td>
<td>Factual</td>
<td>6</td>
<td>6</td>
<td>11</td>
<td>0.7333</td>
<td>-1.924397</td>
<td>2</td>
<td>5, 1</td>
<td>0.1667</td>
<td>Yes</td>
</tr>
<tr>
<td>reasoning_001</td>
<td>Reasoning</td>
<td>6</td>
<td>6</td>
<td>6</td>
<td>0.4000</td>
<td>-1.506396</td>
<td>3</td>
<td>3, 2, 1</td>
<td>0.1667</td>
<td>No</td>
</tr>
<tr>
<td>reasoning_002</td>
<td>Reasoning</td>
<td>6</td>
<td>6</td>
<td>8</td>
<td>0.5333</td>
<td>-1.665463</td>
<td>3</td>
<td>4, 1, 1</td>
<td>0.1667</td>
<td>No</td>
</tr>
</tbody>
</table>

<p><strong>Note:</strong> Structural entropy values are reported exactly as produced by the original SeSE structural-entropy implementation. They should not be replaced with a generic Shannon entropy formula.</p>

## Table 3. Threshold sensitivity

<table>
<thead>
<tr>
<th>Metric</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold conditions tested</td>
<td>5</td>
</tr>
<tr>
<td>Structural-entropy range</td>
<td>0.000198</td>
</tr>
<tr>
<td>Cluster-count range</td>
<td>1</td>
</tr>
</tbody>
</table>

## Table 4. Semantic perturbation

<table>
<thead>
<tr>
<th>Perturbation</th>
<th>Maximum relative entropy change</th>
<th>Graph change at maximum tested level</th>
</tr>
</thead>
<tbody>
<tr>
<td>Edge-weight noise</td>
<td>0.320876</td>
<td>0.244347</td>
</tr>
<tr>
<td>Edge dropout</td>
<td>0.144263</td>
<td>0.000406</td>
</tr>
</tbody>
</table>

## Table 5. Score stability

<table>
<thead>
<tr>
<th>Metric</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>Repeats</td>
<td>11</td>
</tr>
<tr>
<td>Structural-entropy standard deviation</td>
<td>0.849235</td>
</tr>
<tr>
<td>Structural-entropy range</td>
<td>2.260093</td>
</tr>
</tbody>
</table>

## Table 6. Complexity

<table>
<thead>
<tr>
<th>Metric</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>Complexity conditions</td>
<td>5</td>
</tr>
<tr>
<td>Structural-entropy range</td>
<td>0.422950</td>
</tr>
</tbody>
</table>

## Table 7. Failure mechanisms

<table>
<thead>
<tr>
<th>Metric</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>Cases evaluated</td>
<td>3</td>
</tr>
<tr>
<td>Confident failures</td>
<td>2</td>
</tr>
<tr>
<td>Mean incorrect-response fraction</td>
<td>0.333333</td>
</tr>
<tr>
<td>Mean cluster imbalance</td>
<td>2.666667</td>
</tr>
</tbody>
</table>

## Table 8. Consolidated quantitative findings

<table>
<thead>
<tr>
<th>Experimental dimension</th>
<th>Main observation</th>
</tr>
</thead>
<tbody>
<tr>
<td>Scaled factual evaluation</td>
<td>5/5 factual cases had a singleton incorrect-response cluster and were classified as confident failures</td>
</tr>
<tr>
<td>Scaled reasoning evaluation</td>
<td>2/2 reasoning cases produced distributed cluster structures and were not classified as confident failures</td>
</tr>
<tr>
<td>Threshold sensitivity</td>
<td>Structural-entropy range of approximately 0.000198 across five tested thresholds</td>
</tr>
<tr>
<td>Edge-weight perturbation</td>
<td>Maximum relative entropy change of approximately 0.3209</td>
</tr>
<tr>
<td>Edge dropout</td>
<td>Maximum relative entropy change of approximately 0.1443</td>
</tr>
<tr>
<td>Score stability</td>
<td>Entropy standard deviation of approximately 0.8492 across 11 repeats</td>
</tr>
<tr>
<td>Complexity</td>
<td>Entropy range of approximately 0.4230 across five conditions</td>
</tr>
<tr>
<td>Failure mechanisms</td>
<td>2 confident failures among 3 tested cases</td>
</tr>
</tbody>
</table>

## Table 9. Evidence scope and interpretation

<table>
<thead>
<tr>
<th>Finding</th>
<th>Supported interpretation</th>
<th>Not supported by current evidence</th>
</tr>
</thead>
<tbody>
<tr>
<td>Incorrect factual responses formed singleton clusters</td>
<td>Semantic graph structure can separate the tested minority incorrect responses from majority-consistent responses</td>
<td>General hallucination-detection performance</td>
</tr>
<tr>
<td>Low threshold-related entropy variation</td>
<td>Entropy was comparatively stable across the tested thresholds</td>
<td>Threshold invariance across arbitrary ranges</td>
</tr>
<tr>
<td>Perturbations changed entropy</td>
<td>Structural entropy responds to tested graph perturbations</td>
<td>A causal interpretation of the response</td>
</tr>
<tr>
<td>Repeated scores varied</td>
<td>Repeated evaluation can produce non-trivial entropy variation</td>
<td>A universal reproducibility estimate</td>
</tr>
<tr>
<td>Complexity conditions differed</td>
<td>Entropy varies across the tested complexity conditions</td>
<td>A general monotonic complexity–entropy law</td>
</tr>
<tr>
<td>Failure cases showed structural differences</td>
<td>Structural graph properties warrant further investigation as failure indicators</td>
<td>Calibrated error probabilities or statistically validated predictors</td>
</tr>
</tbody>
</table>

## Reporting Note

These tables summarize the current pilot-scale evidence. They should be read together with the Results, Discussion, and Limitations sections. The reported values are descriptive results from the completed experiments and are not intended to establish broad statistical generalization.