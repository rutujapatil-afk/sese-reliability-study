Our Study — Research Pathway

Project principle

Original work must remain unmodified.

All new analysis, experiments, code, results, figures, and documentation belong under our_study/.

The original SeSE implementation is treated as a fixed reference/baseline.

Research pathway

                         OUR_STUDY
                            |
             +--------------+--------------+
             |                             |
             v                             v
   Threshold sensitivity          Perturbation robustness
             |                             |
           DONE                          DONE
             |                             |
             +--------------+--------------+
                            |
                            v
                 Repeated-sampling
                      stability
                            |
                            v
                  Error / correctness
                     stratification
                            |
                            v
                 Failure-mechanism
                      analysis
                            |
                            v
                       Calibration
                            |
                            v
                  Final statistical
                       analysis
                            |
                            v
                       Paper +
                       figures

1. Threshold sensitivity — completed

Experiment: our_study/experiments/run_threshold_sensitivity.py

Controlled thresholds: 0.20, 0.25, 0.30, 0.35, 0.40.

Observed on the controlled six-response example:

Threshold

Clusters

Edges

Structural entropy

0.20

2

8

-1.426130

0.25

2

8

-1.426130

0.30

3

8

-1.426328

0.35

3

8

-1.426328

0.40

3

8

-1.426328

This establishes that graph construction can change discretely as the clustering threshold changes.

2. Perturbation robustness — completed initial experiment

Relevant files:

our_study/src/semantic_perturbation.py

our_study/experiments/run_perturbation_study.py

our_study/experiments/config.yaml

our_study/results/semantic_perturbation/perturbation_results.csv

Perturbations:

edge-weight noise: 0.00, 0.05, 0.10, 0.20

edge dropout: 0.00, 0.05, 0.10, 0.20

seeds: 42, 123, 2026

Initial finding:

Increasing edge-weight noise generally produced larger graph changes and larger structural-entropy changes.

Edge dropout showed strong seed dependence: some perturbations produced almost no change, while others produced substantial graph and entropy changes.

Required refinement before publication claims

Record the realized perturbation, not only the requested level:

requested noise/dropout level

actual edges removed

actual dropout rate

realized graph change

entropy change

random seed

3. Next: repeated-sampling stability

Research question

Does the SeSE uncertainty score for the same question remain stable when independent stochastic responses are sampled repeatedly?

Why this matters

Sample-count sensitivity and score stability are different questions. A method may have good aggregate benchmark performance while individual uncertainty scores vary substantially across independent samples.

Planned analysis

For each question:

Generate multiple independent response sets.

Construct the SeSE semantic graph for each set.

Calculate the resulting uncertainty score.

Compare scores across repeated samples.

Quantify within-question variability.

Relate variability to graph properties.

Candidate statistics: mean score, standard deviation, coefficient of variation where appropriate, pairwise score correlation, rank stability, and graph similarity across repetitions.

4. Error / correctness stratification

Separate examples according to correctness and, where supported by the data, error mechanism.

Candidate categories:

factual

reasoning

arithmetic

fabrication

contradiction

incompleteness

The exact categories must be justified by the available data rather than assumed.

Primary question:

Does SeSE reliability differ systematically across types of incorrect answers?

5. Failure-mechanism analysis

Focus specifically on cases where SeSE is confidently wrong.

Compare semantic-graph structure between correctly confident, correctly uncertain, incorrectly uncertain, and confidently wrong cases.

Candidate structural variables:

graph density

edge-weight distribution

number of clusters

cluster imbalance

hierarchy depth

entropy distribution

graph perturbation sensitivity

Goal: move from reporting that SeSE fails to identifying structural conditions associated with failure.

6. Calibration

After stability and failure analysis, test whether SeSE numerical uncertainty corresponds to empirical error probability.

Possible analyses:

reliability diagrams

calibration error

uncertainty bins versus observed error rate

ranking quality

selective prediction / risk-coverage analysis

Calibration should be treated separately from benchmark discrimination.

7. Final statistical analysis

Once experiments are complete:

aggregate results across seeds;

report uncertainty intervals;

quantify effect sizes;

avoid relying on a single controlled example;

distinguish exploratory findings from confirmatory claims;

document all preprocessing and experimental parameters;

preserve reproducibility.

8. Paper and figures

The final paper should build around the strongest supported claim rather than forcing a predetermined conclusion.

Potential narrative:

We investigate the reliability of semantic-structure-based uncertainty estimation by testing sensitivity, stochastic stability, error-specific behavior, and structural failure mechanisms.

Planned figure families:

threshold sensitivity;

perturbation-response curves;

repeated-sampling score distributions;

reliability/calibration plots;

graph-structure comparisons for failure cases;

risk-coverage or selective prediction analysis.

Research-standard guardrails

Before calling a result publication-grade:

Original SeSE code is unchanged.

Experiment is independently reproducible.

Seeds are recorded.

Requested and realized perturbations are distinguished.

Sample sizes are reported.

Statistical uncertainty is reported where appropriate.

Claims are supported by measured evidence.

Exploratory results are labeled as exploratory.

Controlled toy examples are not presented as general evidence.

Failure cases are analyzed rather than hidden.

All generated artifacts remain inside our_study/.

Current status

Completed

Threshold sensitivity experiment.

Initial semantic-graph perturbation robustness experiment.

Next

Repeated-sampling stability.

Then

Error/correctness stratification.

Failure-mechanism analysis.

Calibration.

Final statistical analysis.

Paper and figures.

Non-negotiable project constraint

Do not modify original_work/.

Any adaptation of SeSE for experimental purposes must be implemented as an independent wrapper, reproduction, or analysis inside our_study/.