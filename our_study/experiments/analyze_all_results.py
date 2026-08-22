"""
Cross-experiment analysis for the SeSE robustness study.

Combines:
1. Threshold sensitivity
2. Semantic perturbation
3. Score stability
4. Complexity dependence
5. Failure mechanisms

Produces:
- combined_results.csv
- experiment_summary.csv
- key_findings.md

This script is deliberately defensive about column names because
individual experiment scripts may use slightly different schemas.
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUTPUT = RESULTS / "cross_experiment_analysis"

OUTPUT.mkdir(parents=True, exist_ok=True)


# ================================================================
# GENERAL HELPERS
# ================================================================

def load_csv(path):
    """Load a CSV if it exists."""
    if path is None or not path.exists():
        if path is not None:
            print(f"[SKIP] {path}")
        return None

    try:
        df = pd.read_csv(path)
        print(f"[OK]   {path.name}: {len(df)} rows")
        print(f"       columns: {list(df.columns)}")
        return df
    except Exception as exc:
        print(f"[ERROR] {path}: {exc}")
        return None


def find_result_csv(filename, preferred_paths=None):
    """
    Find a result CSV.

    First checks preferred paths, then recursively searches results/.
    """
    preferred_paths = preferred_paths or []

    for path in preferred_paths:
        if path.exists():
            return path

    matches = list(RESULTS.rglob(filename))

    if not matches:
        return None

    # Prefer the shortest path / most direct result.
    matches.sort(key=lambda p: (len(p.parts), str(p).lower()))

    return matches[0]


def first_existing_column(df, candidates):
    """Return the first candidate column present in df."""
    for column in candidates:
        if column in df.columns:
            return column
    return None


def flatten_columns(df):
    """Flatten pandas MultiIndex columns."""
    df = df.copy()

    flattened = []

    for column in df.columns:
        if isinstance(column, tuple):
            parts = [
                str(part)
                for part in column
                if str(part) not in ("", "None")
            ]
            flattened.append("_".join(parts))
        else:
            flattened.append(str(column))

    df.columns = flattened
    return df


def coerce_bool_series(series):
    """
    Convert common boolean representations to actual booleans.
    """
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)

    normalized = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

    return normalized.isin(
        {
            "true",
            "1",
            "yes",
            "y",
            "t",
        }
    )


# ================================================================
# NORMALIZATION
# ================================================================

def normalize_complexity_schema(df):
    """
    Normalize complexity grouping column to 'complexity'.
    """
    if df is None:
        return None

    df = df.copy()

    column = first_existing_column(
        df,
        [
            "complexity",
            "complexity_level",
            "level",
            "condition",
            "category",
        ],
    )

    if column is None:
        print(
            "[WARN] Complexity result has no recognizable "
            "complexity column."
        )
        return df

    if column != "complexity":
        df["complexity"] = df[column]

    return df


def normalize_failure_schema(df):
    """
    Normalize failure grouping column to 'case'.
    """
    if df is None:
        return None

    df = df.copy()

    column = first_existing_column(
        df,
        [
            "case",
            "case_id",
            "name",
            "example",
            "condition",
            "scenario",
            "test_case",
        ],
    )

    if column is None:
        print(
            "[WARN] Failure result has no recognizable case column."
        )
        return df

    if column != "case":
        df["case"] = df[column]

    return df


def normalize_stability_schema(df):
    """
    Normalize common score-stability column names.
    """
    if df is None:
        return None

    df = df.copy()

    # Possible example/query identifier.
    identifier = first_existing_column(
        df,
        [
            "case",
            "case_id",
            "example",
            "query",
            "question",
            "sample",
            "id",
        ],
    )

    if identifier is not None and identifier != "case":
        df["case"] = df[identifier]

    return df


# ================================================================
# PERTURBATION
# ================================================================

def analyze_perturbation(df):
    if df is None:
        return None

    required = [
        "perturbation",
        "level",
    ]

    if not all(column in df.columns for column in required):
        print(
            "[WARN] Perturbation analysis skipped: "
            f"missing one of {required}"
        )
        return None

    numeric = [
        "relative_graph_change",
        "absolute_entropy_change",
        "relative_entropy_change",
    ]

    available = [
        column
        for column in numeric
        if column in df.columns
    ]

    if not available:
        print(
            "[WARN] Perturbation analysis skipped: "
            "no compatible numeric columns."
        )
        return None

    aggregations = {}

    for column in available:
        aggregations[f"mean_{column}"] = (column, "mean")
        aggregations[f"std_{column}"] = (column, "std")

    summary = (
        df.groupby(["perturbation", "level"])
        .agg(**aggregations)
        .reset_index()
    )

    summary["experiment"] = "semantic_perturbation"

    return summary


# ================================================================
# COMPLEXITY
# ================================================================

def analyze_complexity(df):
    if df is None:
        return None

    df = normalize_complexity_schema(df)

    if "complexity" not in df.columns:
        return None

    numeric = [
        "structural_entropy",
        "density",
        "mean_edge_weight",
        "total_edge_weight",
        "n_edges",
        "n_nodes",
    ]

    available = [
        column
        for column in numeric
        if column in df.columns
    ]

    if not available:
        print(
            "[WARN] Complexity analysis skipped: "
            "no compatible numeric columns."
        )
        return None

    summary = (
        df.groupby("complexity")[available]
        .agg(["mean", "std"])
        .reset_index()
    )

    summary = flatten_columns(summary)

    summary["experiment"] = "complexity"

    return summary


# ================================================================
# FAILURE MECHANISM
# ================================================================

def analyze_failure(df):
    if df is None:
        return None

    df = normalize_failure_schema(df)

    if "case" not in df.columns:
        return None

    numeric = [
        "structural_entropy",
        "density",
        "mean_edge_weight",
        "cluster_imbalance",
        "incorrect_fraction",
        "n_edges",
        "n_nodes",
    ]

    available = [
        column
        for column in numeric
        if column in df.columns
    ]

    if not available:
        print(
            "[WARN] Failure analysis skipped: "
            "no compatible numeric columns."
        )
        return None

    summary = (
        df.groupby("case")[available]
        .mean()
        .reset_index()
    )

    # ------------------------------------------------------------
    # Confident failure
    # ------------------------------------------------------------

    if "confident_failure" in df.columns:
        confident = (
            df.assign(
                confident_failure_bool=
                coerce_bool_series(
                    df["confident_failure"]
                )
            )
            .groupby("case")["confident_failure_bool"]
            .max()
            .reset_index()
        )

        summary = summary.merge(
            confident,
            on="case",
            how="left",
        )

        summary = summary.rename(
            columns={
                "confident_failure_bool":
                "confident_failure"
            }
        )

    summary["experiment"] = "failure_mechanism"

    return summary


# ================================================================
# SCORE STABILITY
# ================================================================

def analyze_stability(df):
    if df is None:
        return None

    df = normalize_stability_schema(df)

    numeric_candidates = [
        "score",
        "uncertainty_score",
        "se_score",
        "structural_entropy",
        "mean_score",
        "std_score",
        "score_std",
        "score_range",
        "coefficient_of_variation",
    ]

    available = [
        column
        for column in numeric_candidates
        if column in df.columns
    ]

    if not available:
        print(
            "[WARN] Stability analysis skipped: "
            "no recognizable score columns."
        )
        return None

    # If we have a case identifier, summarize per case.
    if "case" in df.columns:
        summary = (
            df.groupby("case")[available]
            .agg(["mean", "std"])
            .reset_index()
        )

        summary = flatten_columns(summary)

    else:
        summary = (
            df[available]
            .agg(["mean", "std"])
            .reset_index()
        )

        summary = flatten_columns(summary)

    summary["experiment"] = "score_stability"

    return summary


# ================================================================
# THRESHOLD SENSITIVITY
# ================================================================

def analyze_threshold(df):
    if df is None:
        return None

    threshold_column = first_existing_column(
        df,
        [
            "threshold",
            "clustering_threshold",
            "similarity_threshold",
            "level",
        ],
    )

    if threshold_column is None:
        print(
            "[WARN] Threshold analysis skipped: "
            "no threshold column found."
        )
        return None

    numeric = [
        "structural_entropy",
        "entropy",
        "mean_edge_weight",
        "total_edge_weight",
        "n_edges",
        "n_clusters",
        "clusters",
    ]

    available = [
        column
        for column in numeric
        if column in df.columns
    ]

    if not available:
        print(
            "[WARN] Threshold analysis skipped: "
            "no compatible metrics."
        )
        return None

    summary = (
        df.groupby(threshold_column)[available]
        .agg(["mean", "std"])
        .reset_index()
    )

    summary = flatten_columns(summary)

    if threshold_column != "threshold":
        summary = summary.rename(
            columns={
                threshold_column: "threshold"
            }
        )

    summary["experiment"] = "threshold_sensitivity"

    return summary


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 70)
    print("SeSE CROSS-EXPERIMENT ANALYSIS")
    print("=" * 70)

    # ------------------------------------------------------------
    # Locate result files
    # ------------------------------------------------------------

    perturbation_path = find_result_csv(
        "perturbation_results.csv",
        [
            RESULTS
            / "semantic_perturbation"
            / "perturbation_results.csv"
        ],
    )

    complexity_path = find_result_csv(
        "complexity_results.csv",
        [
            RESULTS
            / "complexity_study"
            / "complexity_results.csv"
        ],
    )

    failure_path = find_result_csv(
        "failure_mechanism_results.csv",
        [
            RESULTS
            / "failure_mechanism"
            / "failure_mechanism_results.csv"
        ],
    )

    threshold_path = find_result_csv(
        "threshold_sensitivity_results.csv",
        [
            RESULTS
            / "threshold_sensitivity_results.csv",
            RESULTS
            / "threshold_sensitivity"
            / "threshold_sensitivity_results.csv",
        ],
    )

    stability_path = find_result_csv(
        "score_stability_results.csv",
        [
            RESULTS
            / "score_stability"
            / "score_stability_results.csv"
        ],
    )

    # ------------------------------------------------------------
    # Load
    # ------------------------------------------------------------

    perturbation = load_csv(perturbation_path)
    complexity = load_csv(complexity_path)
    failure = load_csv(failure_path)
    threshold = load_csv(threshold_path)
    stability = load_csv(stability_path)

    # ------------------------------------------------------------
    # Analyze
    # ------------------------------------------------------------

    summaries = []

    result = analyze_perturbation(perturbation)
    if result is not None:
        summaries.append(result)

    result = analyze_complexity(complexity)
    if result is not None:
        summaries.append(result)

    result = analyze_failure(failure)
    if result is not None:
        summaries.append(result)

    result = analyze_stability(stability)
    if result is not None:
        summaries.append(result)

    result = analyze_threshold(threshold)
    if result is not None:
        summaries.append(result)

    # ------------------------------------------------------------
    # Combined results
    # ------------------------------------------------------------

    if summaries:

        combined = pd.concat(
            summaries,
            ignore_index=True,
            sort=False,
        )

        combined_path = OUTPUT / "combined_results.csv"

        combined.to_csv(
            combined_path,
            index=False,
        )

        print(f"\nSaved: {combined_path}")

    else:
        print(
            "\n[WARN] No compatible experiment summaries "
            "were generated."
        )

    # ============================================================
    # KEY FINDINGS
    # ============================================================

    findings = []

    # ------------------------------------------------------------
    # Perturbation findings
    # ------------------------------------------------------------

    if perturbation is not None:

        if (
            "perturbation" in perturbation.columns
            and "level" in perturbation.columns
            and "relative_entropy_change"
            in perturbation.columns
        ):

            noise = perturbation[
                perturbation["perturbation"]
                == "edge_weight_noise"
            ]

            for level, group in noise.groupby("level"):

                if float(level) == 0:
                    continue

                change = group[
                    "relative_entropy_change"
                ].mean()

                findings.append(
                    f"- Edge-weight noise level "
                    f"{float(level):.2f} produced a mean "
                    f"relative entropy change of "
                    f"{change:.4f}."
                )

            dropout = perturbation[
                perturbation["perturbation"]
                == "edge_dropout"
            ]

            if not dropout.empty:

                for level, group in dropout.groupby("level"):

                    if float(level) == 0:
                        continue

                    if (
                        "relative_entropy_change"
                        in group.columns
                    ):

                        change = group[
                            "relative_entropy_change"
                        ].mean()

                        findings.append(
                            f"- Edge dropout level "
                            f"{float(level):.2f} produced a mean "
                            f"relative entropy change of "
                            f"{change:.4f}."
                        )

    # ------------------------------------------------------------
    # Complexity findings
    # ------------------------------------------------------------

    if complexity is not None:

        complexity = normalize_complexity_schema(
            complexity
        )

        if (
            "complexity" in complexity.columns
            and "structural_entropy"
            in complexity.columns
        ):

            means = (
                complexity
                .groupby("complexity")[
                    "structural_entropy"
                ]
                .mean()
            )

            if not means.empty:

                findings.append(
                    "- Structural entropy varied across "
                    "semantic/reasoning complexity levels."
                )

                for level, value in means.items():

                    findings.append(
                        f"  - {level}: mean structural "
                        f"entropy {value:.6f}"
                    )

    # ------------------------------------------------------------
    # Failure findings
    # ------------------------------------------------------------

    if failure is not None:

        failure = normalize_failure_schema(
            failure
        )

        if (
            "confident_failure"
            in failure.columns
        ):

            confident_mask = coerce_bool_series(
                failure["confident_failure"]
            )

            confident = failure[
                confident_mask
            ]

            if not confident.empty:

                if "case" in confident.columns:

                    cases = ", ".join(
                        confident["case"]
                        .astype(str)
                        .tolist()
                    )

                    findings.append(
                        "- Confident failures were observed "
                        f"in: {cases}."
                    )

        if "incorrect_fraction" in failure.columns:

            findings.append(
                "- Failure-mechanism analysis measured "
                "incorrect fraction alongside graph density, "
                "cluster imbalance, edge weights, and "
                "structural entropy."
            )

    # ------------------------------------------------------------
    # Threshold findings
    # ------------------------------------------------------------

    if threshold is not None:

        findings.append(
            "- Threshold sensitivity results are available "
            "for comparison with the perturbation and "
            "complexity studies."
        )

    else:

        findings.append(
            "- Threshold sensitivity CSV was not found in "
            "the results directory."
        )

    # ------------------------------------------------------------
    # Stability findings
    # ------------------------------------------------------------

    if stability is not None:

        findings.append(
            "- Score-stability results are available for "
            "assessing whether uncertainty scores vary "
            "across repeated sampling."
        )

    # ------------------------------------------------------------
    # Write findings
    # ------------------------------------------------------------

    findings_path = OUTPUT / "key_findings.md"

    with open(
        findings_path,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "# SeSE Cross-Experiment Findings\n\n"
        )

        f.write(
            "This document summarizes the current "
            "experimental evidence generated by our "
            "independent robustness study.\n\n"
        )

        f.write(
            "## Findings\n\n"
        )

        if findings:

            f.write(
                "\n".join(findings)
            )

            f.write("\n")

        else:

            f.write(
                "No compatible result files were available "
                "for cross-experiment analysis.\n"
            )

    print(f"Saved: {findings_path}")

    # ============================================================
    # EXPERIMENT INVENTORY
    # ============================================================

    inventory = []

    files = {
        "threshold_sensitivity": threshold,
        "semantic_perturbation": perturbation,
        "score_stability": stability,
        "complexity": complexity,
        "failure_mechanism": failure,
    }

    for name, df in files.items():

        inventory.append(
            {
                "experiment": name,
                "available": df is not None,
                "rows": (
                    0
                    if df is None
                    else len(df)
                ),
            }
        )

    inventory_df = pd.DataFrame(
        inventory
    )

    summary_path = (
        OUTPUT / "experiment_summary.csv"
    )

    inventory_df.to_csv(
        summary_path,
        index=False,
    )

    print(
        f"Saved: {summary_path}"
    )

    # ============================================================
    # FINAL STATUS
    # ============================================================

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(
        f"Output directory: {OUTPUT}"
    )

    print("\nExperiment availability:")

    for name, df in files.items():

        status = (
            "AVAILABLE"
            if df is not None
            else "MISSING"
        )

        rows = (
            0
            if df is None
            else len(df)
        )

        print(
            f"  {name:<25} {status:<10} "
            f"{rows} rows"
        )


if __name__ == "__main__":
    main()