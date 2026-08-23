"""
Generate the quantitative synthesis of the SeSE robustness study.

Reads all completed experiment outputs and produces:
    results/final_synthesis/
        quantitative_summary.csv
        quantitative_summary.md
        research_claims.md

This script summarizes the evidence without modifying the original SeSE work.
"""

from pathlib import Path
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUTPUT = RESULTS / "final_synthesis"
OUTPUT.mkdir(parents=True, exist_ok=True)


def load(path):
    if not path.exists():
        print(f"[MISSING] {path}")
        return None

    df = pd.read_csv(path)
    print(f"[OK] {path.name}: {len(df)} rows")
    return df


def safe_float(value):
    if pd.isna(value):
        return None
    return float(value)


def main():
    print("=" * 70)
    print("SeSE FINAL QUANTITATIVE SYNTHESIS")
    print("=" * 70)

    threshold = load(
        RESULTS / "threshold_sensitivity_results.csv"
    )

    perturbation = load(
        RESULTS
        / "semantic_perturbation"
        / "perturbation_results.csv"
    )

    stability = load(
        RESULTS
        / "score_stability"
        / "score_stability_results.csv"
    )

    complexity = load(
        RESULTS
        / "complexity_study"
        / "complexity_results.csv"
    )

    failure = load(
        RESULTS
        / "failure_mechanism"
        / "failure_mechanism_results.csv"
    )

    # Phase 2 scaled evaluation. Support the current directory layout first,
    # while also accepting a flat results/scaled_evaluation_results.csv file.
    scaled_candidates = [
        RESULTS / "scaled_evaluation" / "scaled_evaluation_results.csv",
        RESULTS / "scaled_evaluation_results.csv",
    ]
    scaled = None
    for candidate in scaled_candidates:
        if candidate.exists():
            scaled = load(candidate)
            break

    rows = []

    # ------------------------------------------------------------
    # 1. Threshold sensitivity
    # ------------------------------------------------------------

    if threshold is not None:
        entropy = threshold["structural_entropy"]

        rows.append(
            {
                "experiment": "threshold_sensitivity",
                "metric": "entropy_range",
                "value": float(entropy.max() - entropy.min()),
                "interpretation":
                    "Small range indicates limited entropy sensitivity "
                    "across tested clustering thresholds.",
            }
        )

        rows.append(
            {
                "experiment": "threshold_sensitivity",
                "metric": "thresholds_tested",
                "value": int(len(threshold)),
                "interpretation":
                    "Five clustering thresholds were evaluated.",
            }
        )

        rows.append(
            {
                "experiment": "threshold_sensitivity",
                "metric": "cluster_count_range",
                "value": int(
                    threshold["n_clusters"].max()
                    - threshold["n_clusters"].min()
                ),
                "interpretation":
                    "Cluster count changed within the tested threshold range.",
            }
        )

    # ------------------------------------------------------------
    # 2. Semantic perturbation
    # ------------------------------------------------------------

    if perturbation is not None:

        noise = perturbation[
            perturbation["perturbation"] == "edge_weight_noise"
        ]

        dropout = perturbation[
            perturbation["perturbation"] == "edge_dropout"
        ]

        if not noise.empty:
            nonzero_noise = noise[noise["level"] > 0]

            rows.append(
                {
                    "experiment": "semantic_perturbation",
                    "metric": "noise_max_relative_entropy_change",
                    "value": float(
                        nonzero_noise["relative_entropy_change"].abs().max()
                    ),
                    "interpretation":
                        "Maximum observed relative entropy change under "
                        "edge-weight noise.",
                }
            )

        if not dropout.empty:
            nonzero_dropout = dropout[dropout["level"] > 0]

            rows.append(
                {
                    "experiment": "semantic_perturbation",
                    "metric": "dropout_max_relative_entropy_change",
                    "value": float(
                        nonzero_dropout["relative_entropy_change"].abs().max()
                    ),
                    "interpretation":
                        "Maximum observed relative entropy change under "
                        "edge dropout.",
                }
            )

        if not noise.empty:
            rows.append(
                {
                    "experiment": "semantic_perturbation",
                    "metric": "noise_graph_change_at_max_level",
                    "value": float(
                        noise.loc[
                            noise["level"].idxmax(),
                            "relative_graph_change",
                        ]
                    ),
                    "interpretation":
                        "Graph change observed at the highest tested "
                        "edge-weight noise level.",
                }
            )

        if not dropout.empty:
            rows.append(
                {
                    "experiment": "semantic_perturbation",
                    "metric": "dropout_graph_change_at_max_level",
                    "value": float(
                        dropout.loc[
                            dropout["level"].idxmax(),
                            "relative_graph_change",
                        ]
                    ),
                    "interpretation":
                        "Graph change observed at the highest tested "
                        "edge-dropout level.",
                }
            )

    # ------------------------------------------------------------
    # 3. Score stability
    # ------------------------------------------------------------

    if stability is not None:

        entropy = stability["structural_entropy"]

        rows.append(
            {
                "experiment": "score_stability",
                "metric": "repeat_count",
                "value": int(len(stability)),
                "interpretation":
                    "Repeated evaluations available in the stability dataset.",
            }
        )

        rows.append(
            {
                "experiment": "score_stability",
                "metric": "entropy_std",
                "value": float(entropy.std()),
                "interpretation":
                    "Standard deviation of structural entropy across repeats.",
            }
        )

        rows.append(
            {
                "experiment": "score_stability",
                "metric": "entropy_range",
                "value": float(entropy.max() - entropy.min()),
                "interpretation":
                    "Observed structural-entropy range across repeats.",
            }
        )

    # ------------------------------------------------------------
    # 4. Complexity
    # ------------------------------------------------------------

    if complexity is not None:

        level_column = next(
            c
            for c in ["complexity_level", "complexity", "level"]
            if c in complexity.columns
        )

        entropy = complexity["structural_entropy"]

        rows.append(
            {
                "experiment": "complexity",
                "metric": "complexity_entropy_range",
                "value": float(entropy.max() - entropy.min()),
                "interpretation":
                    "Structural entropy variation across tested "
                    "semantic/reasoning complexity conditions.",
            }
        )

        rows.append(
            {
                "experiment": "complexity",
                "metric": "complexity_levels",
                "value": int(complexity[level_column].nunique()),
                "interpretation":
                    "Number of distinct complexity conditions tested.",
            }
        )

    # ------------------------------------------------------------
    # 5. Scaled evaluation
    # ------------------------------------------------------------

    if scaled is not None:
        # The scaled runner records one row per evaluated case.
        # Prefer explicit success flags when available.
        successful = scaled
        if "status" in scaled.columns:
            successful = scaled[
                scaled["status"].astype(str).str.lower().isin(
                    ["success", "successful", "ok", "completed"]
                )
            ]
        elif "success" in scaled.columns:
            successful = scaled[
                scaled["success"].astype(str).str.lower().isin(
                    ["true", "1", "yes"]
                )
            ]

        rows.append(
            {
                "experiment": "scaled_evaluation",
                "metric": "cases_evaluated",
                "value": int(len(successful)),
                "interpretation":
                    "Number of scaled-evaluation cases represented in the "
                    "results table.",
            }
        )

        if "case_id" in scaled.columns:
            rows.append(
                {
                    "experiment": "scaled_evaluation",
                    "metric": "unique_cases",
                    "value": int(successful["case_id"].nunique()),
                    "interpretation":
                        "Number of distinct evaluation cases in the scaled dataset.",
                }
            )

        if "n_nodes" in successful.columns:
            rows.append(
                {
                    "experiment": "scaled_evaluation",
                    "metric": "total_responses",
                    "value": int(successful["n_nodes"].sum()),
                    "interpretation":
                        "Total number of responses represented across evaluated cases.",
                }
            )

        if "incorrect_fraction" in successful.columns:
            rows.append(
                {
                    "experiment": "scaled_evaluation",
                    "metric": "mean_incorrect_fraction",
                    "value": float(successful["incorrect_fraction"].mean()),
                    "interpretation":
                        "Mean incorrect-response fraction across scaled-evaluation cases.",
                }
            )

        if "confident_failure" in successful.columns:
            confident = successful["confident_failure"].astype(str).str.lower()
            rows.append(
                {
                    "experiment": "scaled_evaluation",
                    "metric": "confident_failure_count",
                    "value": int(
                        confident.isin(["true", "1", "yes"]).sum()
                    ),
                    "interpretation":
                        "Number of scaled-evaluation cases classified as confident failures.",
                }
            )

        if "structural_entropy" in successful.columns:
            entropy = pd.to_numeric(
                successful["structural_entropy"], errors="coerce"
            ).dropna()

            if not entropy.empty:
                rows.append(
                    {
                        "experiment": "scaled_evaluation",
                        "metric": "entropy_mean",
                        "value": float(entropy.mean()),
                        "interpretation":
                            "Mean structural entropy across scaled-evaluation cases.",
                    }
                )
                rows.append(
                    {
                        "experiment": "scaled_evaluation",
                        "metric": "entropy_range",
                        "value": float(entropy.max() - entropy.min()),
                        "interpretation":
                            "Observed structural-entropy range across scaled-evaluation cases.",
                    }
                )

        if "n_clusters" in successful.columns:
            clusters = pd.to_numeric(
                successful["n_clusters"], errors="coerce"
            ).dropna()
            if not clusters.empty:
                rows.append(
                    {
                        "experiment": "scaled_evaluation",
                        "metric": "cluster_count_range",
                        "value": float(clusters.max() - clusters.min()),
                        "interpretation":
                            "Observed range in cluster counts across scaled-evaluation cases.",
                    }
                )

    # ------------------------------------------------------------
    # 6. Failure mechanisms
    # ------------------------------------------------------------

    if failure is not None:

        if "confident_failure" in failure.columns:
            confident = failure["confident_failure"].astype(str).str.lower()

            rows.append(
                {
                    "experiment": "failure_mechanism",
                    "metric": "confident_failure_count",
                    "value": int(
                        confident.isin(["true", "1", "yes"]).sum()
                    ),
                    "interpretation":
                        "Number of tested cases classified as confident failures.",
                }
            )

        if "incorrect_fraction" in failure.columns:
            rows.append(
                {
                    "experiment": "failure_mechanism",
                    "metric": "mean_incorrect_fraction",
                    "value": float(
                        failure["incorrect_fraction"].mean()
                    ),
                    "interpretation":
                        "Mean incorrect-response fraction across tested cases.",
                }
            )

        if "cluster_imbalance" in failure.columns:
            rows.append(
                {
                    "experiment": "failure_mechanism",
                    "metric": "mean_cluster_imbalance",
                    "value": float(
                        failure["cluster_imbalance"].mean()
                    ),
                    "interpretation":
                        "Mean cluster imbalance across tested cases.",
                }
            )

    summary = pd.DataFrame(rows)

    csv_path = OUTPUT / "quantitative_summary.csv"
    summary.to_csv(csv_path, index=False)

    print(f"\nSaved: {csv_path}")

    # ------------------------------------------------------------
    # Human-readable report
    # ------------------------------------------------------------

    md_path = OUTPUT / "quantitative_summary.md"

    with open(md_path, "w", encoding="utf-8") as f:

        f.write("# SeSE Quantitative Synthesis\n\n")

        f.write(
            "This report summarizes the current evidence from the "
            "independent SeSE robustness experiments. It does not "
            "modify or reinterpret the original implementation.\n\n"
        )

        f.write("## Experiments Included\n\n")

        f.write(
            "- Threshold sensitivity\n"
            "- Semantic perturbation\n"
            "- Score stability\n"
            "- Semantic/reasoning complexity\n"
            "- Failure mechanisms\n"
            "- Phase 2 scaled evaluation\n\n"
        )

        f.write("## Quantitative Results\n\n")

        for _, row in summary.iterrows():

            value = row["value"]

            if isinstance(value, float):
                value_text = f"{value:.6f}"
            else:
                value_text = str(value)

            f.write(
                f"### {row['experiment']}: "
                f"{row['metric']}\n\n"
            )

            f.write(f"**Value:** {value_text}\n\n")

            f.write(
                f"{row['interpretation']}\n\n"
            )

    print(f"Saved: {md_path}")

    # ------------------------------------------------------------
    # Research claims
    # ------------------------------------------------------------

    claims_path = OUTPUT / "research_claims.md"

    with open(claims_path, "w", encoding="utf-8") as f:

        f.write("# Candidate Research Claims\n\n")

        f.write(
            "These are deliberately conservative claims generated "
            "from the current experimental evidence. They should be "
            "validated against the underlying result tables before "
            "being used in a paper.\n\n"
        )

        f.write("## Claim 1 — Threshold robustness\n\n")

        if threshold is not None:
            entropy_range = (
                threshold["structural_entropy"].max()
                - threshold["structural_entropy"].min()
            )

            f.write(
                f"Across the tested clustering thresholds, structural "
                f"entropy varied by approximately {entropy_range:.6f}. "
                "The tested threshold range therefore does not show "
                "large entropy instability, although cluster assignments "
                "can change.\n\n"
            )

        f.write("## Claim 2 — Structural perturbation sensitivity\n\n")

        if perturbation is not None:

            noise = perturbation[
                perturbation["perturbation"] == "edge_weight_noise"
            ]

            if not noise.empty:
                max_noise = noise[
                    noise["level"] > 0
                ]["relative_entropy_change"].abs().max()

                f.write(
                    f"Edge-weight perturbations produced measurable "
                    f"changes in structural entropy, reaching an "
                    f"absolute relative change of approximately "
                    f"{max_noise:.4f} at the strongest tested condition. "
                    "This provides evidence that the measured structural entropy can "
                    "respond to perturbations of semantic edge weights "
                    "under the tested conditions.\n\n"
                )

        f.write("## Claim 3 — Complexity dependence\n\n")

        if complexity is not None:

            entropy_range = (
                complexity["structural_entropy"].max()
                - complexity["structural_entropy"].min()
            )

            f.write(
                f"Structural entropy varied across the tested semantic/"
                f"reasoning complexity conditions, with an observed "
                f"range of approximately {entropy_range:.6f}. "
                "This motivates further testing of whether graph "
                "complexity systematically affects uncertainty behavior.\n\n"
            )

        f.write("## Claim 4 — Failure mechanisms\n\n")

        if failure is not None:

            if "confident_failure" in failure.columns:

                confident_count = int(
                    failure["confident_failure"]
                    .astype(str)
                    .str.lower()
                    .isin(["true", "1", "yes"])
                    .sum()
                )

                f.write(
                    f"The failure-mechanism experiment identified "
                    f"{confident_count} confident-failure case(s) "
                    "within the tested examples. These cases provide "
                    "motivation for further examination of structural properties of "
                    "semantic graphs in situations where uncertainty "
                    "is incorrectly high.\n\n"
                )

        f.write("## Claim 5 — Scaled evaluation\n\n")

        if scaled is not None:
            successful = scaled
            if "status" in scaled.columns:
                successful = scaled[
                    scaled["status"].astype(str).str.lower().isin(
                        ["success", "successful", "ok", "completed"]
                    )
                ]
            elif "success" in scaled.columns:
                successful = scaled[
                    scaled["success"].astype(str).str.lower().isin(
                        ["true", "1", "yes"]
                    )
                ]

            case_count = (
                int(successful["case_id"].nunique())
                if "case_id" in successful.columns
                else int(len(successful))
            )
            response_count = (
                int(successful["n_nodes"].sum())
                if "n_nodes" in successful.columns
                else None
            )

            if response_count is not None:
                f.write(
                    f"The Phase 2 scaled evaluation covered {case_count} "
                    f"cases and {response_count} responses. The results "
                    "provide a broader pilot-scale check of structural "
                    "entropy behavior across factual and reasoning cases. "
                    "Because the current run used the SeSE original-response "
                    "fallback when enhancement requests were unavailable, "
                    "this should be interpreted as a scaled evaluation of "
                    "the fallback/original-response path rather than a "
                    "fully enhancement-enabled evaluation.\n\n"
                )
            else:
                f.write(
                    f"The Phase 2 scaled evaluation covered {case_count} "
                    "cases. It provides a broader pilot-scale check of "
                    "structural entropy behavior, subject to the limitations "
                    "of the current dataset and execution path.\n\n"
                )
        else:
            f.write(
                "The Phase 2 scaled evaluation was not available in the "
                "current results directory and therefore is not included "
                "in this synthesis.\n\n"
            )

        f.write("## What We Cannot Yet Claim\n\n")

        f.write(
            "- We cannot claim generalization across datasets from "
            "these experiments alone.\n"
            "- We cannot claim calibrated probabilities of error.\n"
            "- We cannot claim causal mechanisms from the current "
            "observational structural analyses.\n"
            "- We cannot claim broad statistical significance from "
            "the current small experimental sample.\n"
            "- We should not present these results as replacing or "
            "modifying the original SeSE method.\n\n"
        )

        f.write("## Recommended Next Stage\n\n")

        f.write(
            "The next stage should be replication at larger scale: "
            "more questions, multiple datasets, repeated sampling, "
            "and predefined statistical analyses. The purpose is to "
            "determine whether the patterns observed here persist "
            "beyond the current pilot-scale experiments.\n"
        )

    print(f"Saved: {claims_path}")

    print("\n" + "=" * 70)
    print("SYNTHESIS COMPLETE")
    print("=" * 70)
    print(f"Output directory: {OUTPUT}")


if __name__ == "__main__":
    main()