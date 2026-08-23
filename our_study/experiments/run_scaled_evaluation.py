"""
SeSE Phase 2 — Scaled Evaluation

Runs the original, unmodified SeSE semantic-graph construction over
a controlled seven-case evaluation set.

Important:
- Does NOT modify original_work/SeSE.
- Calls the actual original API:
      build_semantic_graph(responses, question, batch_size=128)
- The original function returns an adjacency matrix.
- Cluster IDs are recovered independently using the same hybrid
  similarity/clustering procedure used by the original implementation.
- Threshold is therefore an experiment-side analysis parameter and is
  NOT passed into build_semantic_graph().
"""

from __future__ import annotations

from pathlib import Path
import inspect
import itertools
import json
import logging
import sys

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent

ORIGINAL_SESE = PROJECT_ROOT / "original_work" / "SeSE"

RESULTS = ROOT / "results" / "scaled_evaluation"
RESULTS.mkdir(parents=True, exist_ok=True)

RESULTS_CSV = RESULTS / "scaled_evaluation_results.csv"
SUMMARY_CSV = RESULTS / "scaled_evaluation_summary.csv"
RAW_JSON = RESULTS / "scaled_evaluation_raw.json"
REPORT_MD = RESULTS / "scaled_evaluation_report.md"


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

CLUSTERING_THRESHOLD = 0.30
BATCH_SIZE = 128


# ---------------------------------------------------------------------
# Evaluation cases
# ---------------------------------------------------------------------

CASES = [
    {
        "case_id": "factual_001",
        "question": "Who discovered penicillin?",
        "category": "factual",
        "responses": [
            "Alexander Fleming discovered penicillin.",
            "Penicillin was discovered by Alexander Fleming.",
            "Alexander Fleming is credited with discovering penicillin.",
            "Fleming discovered penicillin in 1928.",
            "The discovery of penicillin is attributed to Alexander Fleming.",
            "Marie Curie discovered penicillin.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "factual",
        ],
    },
    {
        "case_id": "factual_002",
        "question": "What is the capital of France?",
        "category": "factual",
        "responses": [
            "The capital of France is Paris.",
            "Paris is the capital city of France.",
            "France has its capital in Paris.",
            "The French capital is Paris.",
            "Paris serves as the capital of France.",
            "The capital of France is Berlin.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "factual",
        ],
    },
    {
        "case_id": "factual_003",
        "question": "Which planet is known as the Red Planet?",
        "category": "factual",
        "responses": [
            "Mars is known as the Red Planet.",
            "The Red Planet is Mars.",
            "Mars has the nickname the Red Planet.",
            "The planet called the Red Planet is Mars.",
            "Mars is commonly known as the Red Planet.",
            "Jupiter is known as the Red Planet.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "factual",
        ],
    },
    {
        "case_id": "factual_004",
        "question": "What is the largest planet in our solar system?",
        "category": "factual",
        "responses": [
            "Jupiter is the largest planet in our solar system.",
            "The largest planet is Jupiter.",
            "Jupiter has the greatest size of all planets in our solar system.",
            "Our solar system's largest planet is Jupiter.",
            "Jupiter is larger than every other planet in the solar system.",
            "Saturn is the largest planet in our solar system.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "factual",
        ],
    },
    {
        "case_id": "factual_005",
        "question": "What gas do humans need to breathe?",
        "category": "factual",
        "responses": [
            "Humans need oxygen to breathe.",
            "Oxygen is the gas humans require for respiration.",
            "People need oxygen for breathing.",
            "The gas humans breathe to support respiration is oxygen.",
            "Humans require oxygen to survive.",
            "Humans need carbon dioxide to breathe.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "factual",
        ],
    },
    {
        "case_id": "reasoning_001",
        "question": "If all A are B and all B are C, must all A be C?",
        "category": "reasoning",
        "responses": [
            "Yes. If all A are B and all B are C, then all A are C.",
            "Yes, the conclusion follows by transitivity.",
            "Every A belongs to B, and every B belongs to C, so every A belongs to C.",
            "Yes. This is a valid transitive implication.",
            "The answer is yes because A is a subset of B and B is a subset of C.",
            "No. A objects can be B without being C.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "reasoning",
        ],
    },
    {
        "case_id": "reasoning_002",
        "question": "If a number is divisible by 4, must it be even?",
        "category": "reasoning",
        "responses": [
            "Yes. Every number divisible by 4 is even.",
            "Yes, divisibility by 4 implies divisibility by 2.",
            "A number divisible by 4 must be even.",
            "Yes. Four is an even number, so every multiple of four is even.",
            "Divisibility by 4 guarantees that the number is even.",
            "No. Some numbers divisible by 4 are odd.",
        ],
        "correctness": [1, 1, 1, 1, 1, 0],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "reasoning",
        ],
    },
]


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)


# ---------------------------------------------------------------------
# Import original SeSE
# ---------------------------------------------------------------------

def load_original_sese():
    """
    Load the original build_semantic_graph function.

    The discovered original API is:

        build_semantic_graph(
            responses: List[str],
            question: str,
            batch_size: int = 128
        ) -> List[List[float]]
    """

    original_path = str(ORIGINAL_SESE)

    if not ORIGINAL_SESE.exists():
        raise FileNotFoundError(
            f"Original SeSE directory not found:\n{ORIGINAL_SESE}"
        )

    if original_path not in sys.path:
        sys.path.insert(0, original_path)

    try:
        from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (
            build_semantic_graph,
            get_semantic_clusters,
        )
    except Exception as exc:
        raise RuntimeError(
            "Could not import the original SeSE implementation.\n"
            f"Expected location:\n{ORIGINAL_SESE}"
        ) from exc

    print("Original SeSE graph construction loaded.")
    print(
        "build_semantic_graph signature:",
        inspect.signature(build_semantic_graph),
    )

    return build_semantic_graph, get_semantic_clusters


# ---------------------------------------------------------------------
# Correct original API call
# ---------------------------------------------------------------------

def call_original_build_semantic_graph(
    build_semantic_graph,
    responses,
    question,
):
    """
    Call the original API exactly as defined by the installed version.

    IMPORTANT:
    The original function requires:
        responses
        question

    It does NOT accept:
        threshold

    Therefore we never pass threshold here.
    """

    signature = inspect.signature(build_semantic_graph)
    parameters = signature.parameters

    print(
        "    Original function parameters:",
        list(parameters.keys()),
    )

    # Exact API discovered in original SeSE:
    #
    # build_semantic_graph(
    #     responses,
    #     question,
    #     batch_size=128
    # )

    if "responses" in parameters and "question" in parameters:
        kwargs = {
            "responses": responses,
            "question": question,
        }

        if "batch_size" in parameters:
            kwargs["batch_size"] = BATCH_SIZE

        return build_semantic_graph(**kwargs)

    # Defensive positional fallback for another compatible version.
    required = [
        p
        for p in parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]

    if len(required) >= 2:
        return build_semantic_graph(
            responses,
            question,
        )

    raise RuntimeError(
        "Unsupported build_semantic_graph signature: "
        f"{signature}"
    )


# ---------------------------------------------------------------------
# Matrix conversion
# ---------------------------------------------------------------------

def adjacency_matrix_from_result(result, n):
    """
    Convert the original SeSE return value into an NxN numpy matrix.

    The original implementation returns adj.tolist().
    """

    matrix = np.asarray(result, dtype=float)

    if matrix.ndim != 2:
        raise ValueError(
            "Original SeSE build_semantic_graph() did not return a "
            f"2-D adjacency matrix. Shape={matrix.shape}"
        )

    if matrix.shape != (n, n):
        raise ValueError(
            "Unexpected adjacency matrix shape: "
            f"{matrix.shape}; expected {(n, n)}"
        )

    matrix = np.nan_to_num(
        matrix,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    matrix = np.maximum(matrix, 0.0)

    # Ensure numerical symmetry.
    matrix = (matrix + matrix.T) / 2.0

    np.fill_diagonal(matrix, 0.0)

    return matrix


# ---------------------------------------------------------------------
# Graph metrics
# ---------------------------------------------------------------------

def graph_metrics(adj):
    """
    Calculate quantitative graph statistics from the original
    SeSE adjacency matrix.
    """

    n = int(adj.shape[0])

    if n <= 1:
        possible_edges = 0
    else:
        possible_edges = n * (n - 1) // 2

    upper = adj[np.triu_indices(n, k=1)]

    # SeSE uses positive weighted edges.
    positive_edges = upper[upper > 0]

    n_edges = int(len(positive_edges))

    if possible_edges:
        density = n_edges / possible_edges
    else:
        density = 0.0

    if len(positive_edges):
        mean_weight = float(np.mean(positive_edges))
        total_weight = float(np.sum(positive_edges))
    else:
        mean_weight = 0.0
        total_weight = 0.0

    return {
        "n_nodes": n,
        "n_edges": n_edges,
        "edge_density": density,
        "mean_edge_weight": mean_weight,
        "total_edge_weight": total_weight,
    }


# ---------------------------------------------------------------------
# Structural entropy
# ---------------------------------------------------------------------

def compute_structural_entropy(adj):
    """
    Compute structural entropy with the original SeSE implementation.

    This keeps the metric definition identical to the original work
    rather than substituting a generic Shannon entropy formula.
    """

    original_path = str(ORIGINAL_SESE)
    if original_path not in sys.path:
        sys.path.insert(0, original_path)

    try:
        from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
            compute_se,
        )
    except Exception as exc:
        raise RuntimeError(
            "Could not import the original SeSE structural-entropy "
            "implementation."
        ) from exc

    return float(compute_se(adj))


# ---------------------------------------------------------------------
# Cluster recovery
# ---------------------------------------------------------------------

def recover_clusters(
    get_semantic_clusters,
    responses,
    question,
):
    """
    Recover the semantic clusters using the original SeSE clustering
    implementation.

    This is deliberately separate from build_semantic_graph() because
    build_semantic_graph() returns only the adjacency matrix.
    """

    # IMPORTANT: the verified original SeSE implementation calls
    # get_semantic_clusters(responses, question) internally.  It does
    # not expose a similarity_threshold argument in that API.  The
    # threshold used by this experiment is therefore recorded as
    # metadata only; it is never injected into the original function.
    cluster_ids, enhanced = get_semantic_clusters(
        responses,
        question,
    )

    if len(cluster_ids) != len(responses):
        raise ValueError(
            "Original SeSE returned an invalid number of cluster IDs: "
            f"{len(cluster_ids)} for {len(responses)} responses."
        )

    return list(cluster_ids), enhanced


# ---------------------------------------------------------------------
# Cluster statistics
# ---------------------------------------------------------------------

def cluster_statistics(cluster_ids, correctness):
    """
    Compute cluster-level correctness information.
    """

    if not cluster_ids:
        return {
            "n_clusters": 0,
            "cluster_sizes": "",
            "cluster_incorrect_counts": "",
            "cluster_incorrect_fraction": "",
            "largest_cluster": 0,
            "smallest_cluster": 0,
            "cluster_imbalance": np.nan,
        }

    cluster_ids = list(cluster_ids)

    unique_clusters = sorted(set(cluster_ids))

    sizes = []
    incorrect_counts = []
    incorrect_fractions = []

    for cluster in unique_clusters:
        indices = [
            i
            for i, c in enumerate(cluster_ids)
            if c == cluster
        ]

        size = len(indices)

        incorrect = sum(
            1 - int(correctness[i])
            for i in indices
        )

        fraction = (
            incorrect / size
            if size
            else 0.0
        )

        sizes.append(size)
        incorrect_counts.append(incorrect)
        incorrect_fractions.append(fraction)

    largest = max(sizes) if sizes else 0
    smallest = min(sizes) if sizes else 0

    imbalance = (
        largest / smallest
        if smallest > 0
        else np.nan
    )

    return {
        "n_clusters": len(unique_clusters),
        "cluster_sizes": json.dumps(sizes),
        "cluster_incorrect_counts": json.dumps(
            incorrect_counts
        ),
        "cluster_incorrect_fraction": json.dumps(
            [round(x, 6) for x in incorrect_fractions]
        ),
        "largest_cluster": largest,
        "smallest_cluster": smallest,
        "cluster_imbalance": imbalance,
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 70)
    print("SeSE PHASE 2 — SCALED EVALUATION")
    print("=" * 70)

    print(f"Cases: {len(CASES)}")
    print(
        f"Responses: "
        f"{sum(len(c['responses']) for c in CASES)}"
    )

    build_semantic_graph, get_semantic_clusters = (
        load_original_sese()
    )

    rows = []
    raw_results = []

    for case in CASES:

        case_id = case["case_id"]
        question = case["question"]
        category = case["category"]
        responses = case["responses"]
        correctness = case["correctness"]
        error_types = case["error_type"]

        print("\n" + "-" * 70)
        print(f"Case: {case_id}")
        print(f"Question: {question}")
        print(f"Responses: {len(responses)}")

        if not (
            len(responses)
            == len(correctness)
            == len(error_types)
        ):
            raise ValueError(
                f"Metadata mismatch in {case_id}"
            )

        try:

            # ---------------------------------------------------------
            # 1. ORIGINAL SeSE GRAPH
            # ---------------------------------------------------------

            print(
                "    Calling original "
                "build_semantic_graph(responses, question)..."
            )

            graph_result = call_original_build_semantic_graph(
                build_semantic_graph,
                responses,
                question,
            )

            adj = adjacency_matrix_from_result(
                graph_result,
                len(responses),
            )

            metrics = graph_metrics(adj)

            entropy = compute_structural_entropy(adj)

            # ---------------------------------------------------------
            # 2. ORIGINAL SeSE CLUSTERS
            # ---------------------------------------------------------

            print(
                "    Recovering semantic clusters..."
            )

            cluster_ids, enhanced = recover_clusters(
                get_semantic_clusters,
                responses,
                question,
            )

            cluster_info = cluster_statistics(
                cluster_ids,
                correctness,
            )

            # ---------------------------------------------------------
            # 3. FAILURE METRICS
            # ---------------------------------------------------------

            incorrect_responses = sum(
                1 - int(x)
                for x in correctness
            )

            incorrect_fraction = (
                incorrect_responses / len(correctness)
            )

            confident_failure = (
                incorrect_fraction > 0
                and cluster_info["n_clusters"] <= 2
                and metrics["mean_edge_weight"] >= 0.50
            )

            # ---------------------------------------------------------
            # 4. RESULT ROW
            # ---------------------------------------------------------

            row = {
                "case_id": case_id,
                "category": category,
                "question": question,
                "n_responses": len(responses),
                "clustering_threshold": CLUSTERING_THRESHOLD,
                "n_nodes": metrics["n_nodes"],
                "n_edges": metrics["n_edges"],
                "edge_density": metrics["edge_density"],
                "mean_edge_weight": metrics[
                    "mean_edge_weight"
                ],
                "total_edge_weight": metrics[
                    "total_edge_weight"
                ],
                "structural_entropy": entropy,
                "n_clusters": cluster_info[
                    "n_clusters"
                ],
                "cluster_imbalance": cluster_info[
                    "cluster_imbalance"
                ],
                "largest_cluster": cluster_info[
                    "largest_cluster"
                ],
                "smallest_cluster": cluster_info[
                    "smallest_cluster"
                ],
                "incorrect_responses": incorrect_responses,
                "incorrect_fraction": incorrect_fraction,
                "confident_failure": confident_failure,
                "cluster_ids": json.dumps(
                    cluster_ids
                ),
                "cluster_sizes": cluster_info[
                    "cluster_sizes"
                ],
                "cluster_incorrect_counts": cluster_info[
                    "cluster_incorrect_counts"
                ],
                "cluster_incorrect_fraction": cluster_info[
                    "cluster_incorrect_fraction"
                ],
                "status": "success",
            }

            rows.append(row)

            raw_results.append(
                {
                    "case_id": case_id,
                    "category": category,
                    "question": question,
                    "responses": responses,
                    "correctness": correctness,
                    "error_type": error_types,
                    "enhanced_responses": enhanced,
                    "cluster_ids": cluster_ids,
                    "adjacency_matrix": adj.tolist(),
                    "metrics": metrics,
                    "structural_entropy": entropy,
                }
            )

            # ---------------------------------------------------------
            # 5. CONSOLE OUTPUT
            # ---------------------------------------------------------

            print(
                f"    clusters: "
                f"{row['n_clusters']}"
            )

            print(
                f"    edges: "
                f"{row['n_edges']}"
            )

            print(
                f"    density: "
                f"{row['edge_density']:.4f}"
            )

            print(
                f"    mean edge weight: "
                f"{row['mean_edge_weight']:.4f}"
            )

            print(
                f"    total edge weight: "
                f"{row['total_edge_weight']:.4f}"
            )

            print(
                f"    structural entropy: "
                f"{row['structural_entropy']:.8f}"
            )

            print(
                f"    incorrect fraction: "
                f"{row['incorrect_fraction']:.4f}"
            )

            print(
                f"    confident failure: "
                f"{row['confident_failure']}"
            )

        except Exception as exc:

            print(
                "[ERROR] Evaluation failed:",
                repr(exc),
            )

            rows.append(
                {
                    "case_id": case_id,
                    "category": category,
                    "question": question,
                    "n_responses": len(responses),
                    "clustering_threshold": (
                        CLUSTERING_THRESHOLD
                    ),
                    "n_nodes": np.nan,
                    "n_edges": np.nan,
                    "edge_density": np.nan,
                    "mean_edge_weight": np.nan,
                    "total_edge_weight": np.nan,
                    "structural_entropy": np.nan,
                    "n_clusters": np.nan,
                    "cluster_imbalance": np.nan,
                    "largest_cluster": np.nan,
                    "smallest_cluster": np.nan,
                    "incorrect_responses": (
                        sum(1 - int(x) for x in correctness)
                    ),
                    "incorrect_fraction": (
                        sum(1 - int(x) for x in correctness)
                        / len(correctness)
                    ),
                    "confident_failure": False,
                    "cluster_ids": "",
                    "cluster_sizes": "",
                    "cluster_incorrect_counts": "",
                    "cluster_incorrect_fraction": "",
                    "status": "error",
                    "error": str(exc),
                }
            )

    # -----------------------------------------------------------------
    # Save dataframe
    # -----------------------------------------------------------------

    if not rows:
        raise RuntimeError(
            "No evaluation results were generated."
        )

    results_df = pd.DataFrame(rows)

    successful = results_df[
        results_df["status"] == "success"
    ].copy()

    results_df.to_csv(
        RESULTS_CSV,
        index=False,
    )

    print("\n" + "=" * 70)
    print("RESULTS SAVED")
    print("=" * 70)

    print(RESULTS_CSV)
    print(
        f"Rows saved: {len(results_df)}"
    )
    print(
        f"Successful: {len(successful)}"
    )
    print(
        f"Failed: "
        f"{len(results_df) - len(successful)}"
    )

    if successful.empty:
        raise RuntimeError(
            "No successful SeSE evaluations were generated."
        )

    # -----------------------------------------------------------------
    # Category summary
    # -----------------------------------------------------------------

    numeric_columns = [
        "n_nodes",
        "n_edges",
        "edge_density",
        "mean_edge_weight",
        "total_edge_weight",
        "structural_entropy",
        "n_clusters",
        "cluster_imbalance",
        "incorrect_fraction",
    ]

    available_numeric = [
        c
        for c in numeric_columns
        if c in successful.columns
    ]

    if available_numeric:

        summary = (
            successful
            .groupby("category")[available_numeric]
            .agg(["mean", "std"])
            .reset_index()
        )

        summary.columns = [
            "_".join(c).strip("_")
            if isinstance(c, tuple)
            else c
            for c in summary.columns
        ]

        summary.to_csv(
            SUMMARY_CSV,
            index=False,
        )

        print(
            f"Saved: {SUMMARY_CSV}"
        )

    # -----------------------------------------------------------------
    # Raw JSON
    # -----------------------------------------------------------------

    with open(
        RAW_JSON,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            raw_results,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved: {RAW_JSON}"
    )

    # -----------------------------------------------------------------
    # Markdown report
    # -----------------------------------------------------------------

    with open(
        REPORT_MD,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "# SeSE Phase 2 — Scaled Evaluation\n\n"
        )

        f.write(
            "This experiment evaluates the original, "
            "unmodified SeSE semantic graph construction "
            "over a controlled seven-case dataset.\n\n"
        )

        f.write(
            "## Configuration\n\n"
        )

        f.write(
            f"- Cases: {len(CASES)}\n"
        )

        f.write(
            "- Responses per case: 6\n"
        )

        f.write(
            f"- Total responses: "
            f"{len(CASES) * 6}\n"
        )

        f.write(
            f"- Analysis clustering threshold: "
            f"{CLUSTERING_THRESHOLD:.2f}\n"
        )

        f.write(
            f"- Batch size: {BATCH_SIZE}\n"
        )

        f.write(
            "- Original SeSE implementation: "
            "UNMODIFIED\n\n"
        )

        f.write(
            "## Important API detail\n\n"
        )

        f.write(
            "The original `build_semantic_graph()` "
            "requires both `responses` and `question` "
            "and returns an adjacency matrix. The "
            "experiment therefore does not pass an "
            "unsupported `threshold` argument.\n\n"
        )

        f.write(
            "## Successful evaluations\n\n"
        )

        f.write(
            f"- Successful cases: {len(successful)}\n"
        )

        f.write(
            f"- Failed cases: "
            f"{len(results_df) - len(successful)}\n\n"
        )

        f.write(
            "## Per-case results\n\n"
        )

        display_columns = [
            "case_id",
            "category",
            "n_nodes",
            "n_clusters",
            "n_edges",
            "edge_density",
            "mean_edge_weight",
            "total_edge_weight",
            "structural_entropy",
            "incorrect_fraction",
            "confident_failure",
            "status",
        ]

        existing = [
            c
            for c in display_columns
            if c in results_df.columns
        ]

        f.write(
            results_df[
                existing
            ].to_markdown(index=False)
        )

        f.write("\n")

    print(
        f"Saved: {REPORT_MD}"
    )

    print("\n" + "=" * 70)
    print("PHASE 2 SCALED EVALUATION COMPLETE")
    print("=" * 70)
    print(
        f"Output directory: {RESULTS}"
    )


if __name__ == "__main__":
    main()