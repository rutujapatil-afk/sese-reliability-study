"""
Phase 2: Scaled evaluation harness for the SeSE robustness study.

This version is compatible with the ORIGINAL SeSE implementation under:

    E:/SeSe/original_work/SeSE

The original build_semantic_graph() API is:

    build_semantic_graph(responses, question, batch_size=128)

and returns a weighted adjacency matrix.

This experiment does NOT modify the original SeSE implementation.
"""

from __future__ import annotations

import csv
import inspect
import sys
from pathlib import Path
from typing import Any

import numpy as np


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL = ROOT.parent / "original_work" / "SeSE"

RESULTS = ROOT / "results" / "scaled_evaluation"
RESULTS.mkdir(parents=True, exist_ok=True)

OUTPUT = RESULTS / "scaled_evaluation_results.csv"


# ---------------------------------------------------------------------
# Make original SeSE importable
# ---------------------------------------------------------------------

if str(ORIGINAL) not in sys.path:
    sys.path.insert(0, str(ORIGINAL))


# ---------------------------------------------------------------------
# Evaluation cases
# ---------------------------------------------------------------------

CASES = [
    {
        "case_id": "factual_001",
        "question": "Who discovered penicillin?",
        "responses": [
            "Alexander Fleming discovered penicillin.",
            "Penicillin was discovered by Alexander Fleming.",
            "Alexander Fleming is credited with discovering penicillin.",
            "Marie Curie discovered penicillin.",
            "Louis Pasteur discovered penicillin.",
            "Alexander Fleming discovered the antibiotic penicillin.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "factual",
            "factual",
            "correct",
        ],
    },
    {
        "case_id": "factual_002",
        "question": "What is the capital of France?",
        "responses": [
            "The capital of France is Paris.",
            "Paris is the capital city of France.",
            "France has Paris as its capital.",
            "The capital of France is Lyon.",
            "Marseille is the capital of France.",
            "Paris serves as the capital of France.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "factual",
            "factual",
            "correct",
        ],
    },
    {
        "case_id": "factual_003",
        "question": "Which planet is known as the Red Planet?",
        "responses": [
            "Mars is known as the Red Planet.",
            "The Red Planet is Mars.",
            "Mars is commonly called the Red Planet.",
            "Venus is known as the Red Planet.",
            "Jupiter is the Red Planet.",
            "Mars is referred to as the Red Planet.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "factual",
            "factual",
            "correct",
        ],
    },
    {
        "case_id": "factual_004",
        "question": "What is the largest planet in our solar system?",
        "responses": [
            "Jupiter is the largest planet in the solar system.",
            "The largest planet is Jupiter.",
            "Jupiter has the greatest planetary size in our solar system.",
            "Saturn is the largest planet.",
            "Earth is the largest planet.",
            "Jupiter is the largest planet in our solar system.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "factual",
            "factual",
            "correct",
        ],
    },
    {
        "case_id": "factual_005",
        "question": "What gas do humans need to breathe?",
        "responses": [
            "Humans need oxygen to breathe.",
            "Oxygen is required for human respiration.",
            "People breathe oxygen.",
            "Humans need carbon dioxide to breathe.",
            "Nitrogen is the gas humans primarily need for respiration.",
            "Oxygen is necessary for human breathing.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "factual",
            "factual",
            "correct",
        ],
    },
    {
        "case_id": "reasoning_001",
        "question": "If all A are B and all B are C, must all A be C?",
        "responses": [
            "Yes. If every A is a B and every B is a C, then every A is a C.",
            "Yes, because membership in A implies membership in B and then C.",
            "All A are necessarily C under those premises.",
            "No, A can be unrelated to C.",
            "The conclusion cannot follow because B and C are different labels.",
            "Yes, the implication follows transitively.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "reasoning",
            "reasoning",
            "correct",
        ],
    },
    {
        "case_id": "reasoning_002",
        "question": "If a number is divisible by 4, must it be even?",
        "responses": [
            "Yes. Every number divisible by 4 is even.",
            "Yes, because divisibility by 4 implies divisibility by 2.",
            "A number divisible by four must be even.",
            "No. Numbers divisible by 4 can be odd.",
            "Divisibility by 4 does not imply evenness.",
            "Yes, divisibility by 4 guarantees an even number.",
        ],
        "correctness": [1, 1, 1, 0, 0, 1],
        "error_type": [
            "correct",
            "correct",
            "correct",
            "reasoning",
            "reasoning",
            "correct",
        ],
    },
]


# ---------------------------------------------------------------------
# Original SeSE loading
# ---------------------------------------------------------------------

def load_seme_graph_module():
    """
    Import the ORIGINAL SeSE semantic graph module.
    """

    try:
        import sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph as module

    except Exception as exc:
        raise RuntimeError(
            "Could not import the original SeSE module from "
            f"{ORIGINAL}. Check original_work/SeSE."
        ) from exc

    if not hasattr(module, "build_semantic_graph"):
        raise RuntimeError(
            "The original construct_semantic_graph module does not "
            "expose build_semantic_graph."
        )

    return module


def load_seme_graph_functions():

    module = load_seme_graph_module()

    build_semantic_graph = module.build_semantic_graph

    print("Original SeSE graph construction loaded.")

    try:
        print(
            "build_semantic_graph signature:",
            inspect.signature(build_semantic_graph),
        )
    except (TypeError, ValueError):
        pass

    return module, build_semantic_graph


# ---------------------------------------------------------------------
# Graph normalization
# ---------------------------------------------------------------------

def to_numpy_matrix(graph: Any) -> np.ndarray:
    """
    Convert the original SeSE result into a square numeric matrix.
    """

    if graph is None:
        raise ValueError(
            "Original SeSE graph construction returned None."
        )

    if hasattr(graph, "toarray"):
        graph = graph.toarray()

    matrix = np.asarray(graph, dtype=float)

    if matrix.ndim != 2:
        raise ValueError(
            "Expected a 2-D SeSE adjacency matrix, "
            f"got shape {matrix.shape}."
        )

    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(
            "Expected a square SeSE adjacency matrix, "
            f"got shape {matrix.shape}."
        )

    if not np.all(np.isfinite(matrix)):
        raise ValueError(
            "SeSE graph contains NaN or infinite values."
        )

    return matrix


def symmetrize(weights: np.ndarray) -> np.ndarray:
    """
    Normalize the weighted graph for downstream analysis.
    """

    matrix = np.asarray(weights, dtype=float)

    matrix = np.nan_to_num(
        matrix,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    matrix = np.maximum(matrix, 0.0)

    matrix = (matrix + matrix.T) / 2.0

    np.fill_diagonal(matrix, 0.0)

    return matrix


# ---------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------

def compute_clusters(
    weights: np.ndarray,
    threshold: float = 0.30,
) -> np.ndarray:
    """
    Compute connected components after thresholding the ORIGINAL
    SeSE weighted graph.

    IMPORTANT:

        threshold is applied here.

    It is NOT passed to build_semantic_graph(), because the original
    SeSE function does not accept a threshold argument.
    """

    matrix = symmetrize(weights)

    n = matrix.shape[0]

    if n == 0:
        return np.array([], dtype=int)

    adjacency = matrix >= float(threshold)

    np.fill_diagonal(adjacency, False)

    labels = -np.ones(n, dtype=int)

    component = 0

    for start in range(n):

        if labels[start] != -1:
            continue

        stack = [start]

        labels[start] = component

        while stack:

            node = stack.pop()

            neighbours = np.flatnonzero(
                adjacency[node]
            )

            for neighbour in neighbours:

                neighbour = int(neighbour)

                if labels[neighbour] == -1:

                    labels[neighbour] = component

                    stack.append(neighbour)

        component += 1

    return labels


# ---------------------------------------------------------------------
# Structural entropy
# ---------------------------------------------------------------------

def graph_entropy_fallback(
    weights: np.ndarray,
) -> float:
    """
    Deterministic fallback structural entropy.

    The original construct_semantic_graph module returns the graph matrix,
    not an entropy scalar. When no dedicated entropy helper is exported by
    that module, calculate the negative Shannon entropy of the weighted
    degree distribution.

    This keeps the experiment executable without inventing an API for the
    original implementation.
    """

    matrix = symmetrize(weights)

    degree = matrix.sum(axis=1)

    total = float(degree.sum())

    if total <= 0.0:
        return 0.0

    probabilities = degree / total

    probabilities = probabilities[
        probabilities > 0.0
    ]

    return float(
        np.sum(
            probabilities
            * np.log(probabilities)
        )
    )


def try_original_entropy(
    module,
    weights: np.ndarray,
    labels: np.ndarray,
):
    """
    If the original module happens to expose a structural entropy helper,
    use it. Otherwise return None.
    """

    candidates = [
        "structural_entropy",
        "compute_structural_entropy",
        "calculate_structural_entropy",
        "get_structural_entropy",
    ]

    for name in candidates:

        function = getattr(
            module,
            name,
            None,
        )

        if not callable(function):
            continue

        try:
            signature = inspect.signature(
                function
            )
        except (TypeError, ValueError):
            continue

        kwargs = {}

        compatible = True

        for parameter in signature.parameters.values():

            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            if parameter.name in {
                "graph",
                "adjacency",
                "matrix",
                "weights",
            }:
                kwargs[parameter.name] = weights

            elif parameter.name in {
                "cluster_ids",
                "labels",
                "clusters",
                "cluster_labels",
            }:
                kwargs[parameter.name] = labels

            elif parameter.default is parameter.empty:

                compatible = False

                break

        if not compatible:
            continue

        try:

            value = function(**kwargs)

            if (
                np.isscalar(value)
                and np.isfinite(float(value))
            ):
                return float(value)

        except Exception:
            continue

    return None


def compute_structural_entropy(
    module,
    weights: np.ndarray,
    labels: np.ndarray,
) -> float:

    original_value = try_original_entropy(
        module,
        weights,
        labels,
    )

    if original_value is not None:
        return original_value

    return graph_entropy_fallback(
        weights
    )


# ---------------------------------------------------------------------
# Graph statistics
# ---------------------------------------------------------------------

def graph_statistics(
    weights: np.ndarray,
    labels: np.ndarray,
) -> dict:

    matrix = symmetrize(weights)

    n = matrix.shape[0]

    upper = matrix[
        np.triu_indices(
            n,
            k=1,
        )
    ]

    positive_edges = upper > 0

    n_edges = int(
        np.count_nonzero(
            positive_edges
        )
    )

    if n_edges:

        total_edge_weight = float(
            upper[positive_edges].sum()
        )

        mean_edge_weight = float(
            upper[positive_edges].mean()
        )

    else:

        total_edge_weight = 0.0

        mean_edge_weight = 0.0

    possible_edges = (
        n * (n - 1) / 2.0
    )

    if possible_edges:

        edge_density = float(
            n_edges / possible_edges
        )

    else:

        edge_density = 0.0

    _, cluster_sizes = np.unique(
        labels,
        return_counts=True,
    )

    n_clusters = int(
        len(cluster_sizes)
    )

    if len(cluster_sizes):

        largest_cluster = int(
            cluster_sizes.max()
        )

        smallest_cluster = int(
            cluster_sizes.min()
        )

        cluster_imbalance = float(
            largest_cluster
            / smallest_cluster
        )

    else:

        largest_cluster = 0

        smallest_cluster = 0

        cluster_imbalance = 0.0

    return {
        "n_nodes": int(n),
        "n_clusters": n_clusters,
        "n_edges": n_edges,
        "edge_density": edge_density,
        "mean_edge_weight": mean_edge_weight,
        "total_edge_weight": total_edge_weight,
        "cluster_imbalance": cluster_imbalance,
        "largest_cluster": largest_cluster,
        "smallest_cluster": smallest_cluster,
    }


# ---------------------------------------------------------------------
# ORIGINAL graph invocation
# ---------------------------------------------------------------------

def build_original_graph(
    build_semantic_graph,
    responses,
    question,
):
    """
    Correct invocation of the ORIGINAL SeSE API.

    Known original signature:

        build_semantic_graph(
            responses,
            question,
            batch_size=128,
        )

    NEVER pass threshold here.
    """

    try:

        signature = inspect.signature(
            build_semantic_graph
        )

    except (TypeError, ValueError):

        signature = None

    if signature is not None:

        parameter_names = list(
            signature.parameters
        )

        if (
            len(parameter_names) >= 2
            and parameter_names[0] == "responses"
            and parameter_names[1] == "question"
        ):

            kwargs = {}

            if (
                "batch_size"
                in signature.parameters
            ):

                kwargs["batch_size"] = 128

            return build_semantic_graph(
                responses,
                question,
                **kwargs,
            )

    # Defensive fallback.

    errors = []

    attempts = [
        (
            responses,
            question,
            128,
        ),
        (
            responses,
            question,
        ),
    ]

    for args in attempts:

        try:

            return build_semantic_graph(
                *args
            )

        except Exception as exc:

            errors.append(
                f"{type(exc).__name__}: {exc}"
            )

    raise RuntimeError(
        "Could not call the original "
        "build_semantic_graph(). "
        "Discovered signature is incompatible. "
        + " | ".join(errors)
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 70)
    print(
        "SeSE PHASE 2 — SCALED EVALUATION"
    )
    print("=" * 70)

    print(
        f"Cases: {len(CASES)}"
    )

    print(
        "Responses:",
        sum(
            len(case["responses"])
            for case in CASES
        ),
    )

    module, build_semantic_graph = (
        load_seme_graph_functions()
    )

    rows = []

    for case in CASES:

        print(
            "\n"
            + "-" * 70
        )

        print(
            f"Case: {case['case_id']}"
        )

        print(
            f"Question: {case['question']}"
        )

        responses = case["responses"]

        correctness = case[
            "correctness"
        ]

        error_types = case[
            "error_type"
        ]

        if not (
            len(responses)
            == len(correctness)
            == len(error_types)
        ):

            raise ValueError(
                f"Metadata length mismatch "
                f"in {case['case_id']}"
            )

        print(
            f"Responses: {len(responses)}"
        )

        try:

            # ---------------------------------------------------------
            # THIS IS THE CRITICAL FIX.
            #
            # The original SeSE function requires:
            #
            #     responses
            #     question
            #
            # and optionally batch_size.
            #
            # The clustering threshold is NOT an argument to this
            # function.
            # ---------------------------------------------------------

            graph = build_original_graph(
                build_semantic_graph,
                responses,
                case["question"],
            )

            weights = to_numpy_matrix(
                graph
            )

            print(
                f"Graph shape: {weights.shape}"
            )

            # Threshold is applied AFTER graph construction.

            labels = compute_clusters(
                weights,
                threshold=0.30,
            )

            entropy = (
                compute_structural_entropy(
                    module,
                    weights,
                    labels,
                )
            )

            stats = graph_statistics(
                weights,
                labels,
            )

            print(
                f"    clusters: "
                f"{stats['n_clusters']}"
            )

            print(
                f"    edges: "
                f"{stats['n_edges']}"
            )

            print(
                f"    density: "
                f"{stats['edge_density']:.4f}"
            )

            print(
                "    mean edge weight: "
                f"{stats['mean_edge_weight']:.4f}"
            )

            print(
                "    structural entropy: "
                f"{entropy:.8f}"
            )

        except Exception as exc:

            print(
                "[ERROR] SeSE graph "
                "construction failed: "
                f"{type(exc).__name__}: {exc}"
            )

            continue

        incorrect_count = int(
            sum(
                int(value) == 0
                for value in correctness
            )
        )

        incorrect_fraction = float(
            incorrect_count
            / len(correctness)
        )

        cluster_sizes = []

        cluster_incorrect_counts = []

        cluster_incorrect_fraction = []

        for cluster_id in np.unique(
            labels
        ):

            indices = np.flatnonzero(
                labels == cluster_id
            )

            size = int(
                len(indices)
            )

            incorrect = int(
                sum(
                    int(
                        correctness[int(index)]
                    )
                    == 0
                    for index in indices
                )
            )

            cluster_sizes.append(
                size
            )

            cluster_incorrect_counts.append(
                incorrect
            )

            cluster_incorrect_fraction.append(
                float(
                    incorrect / size
                )
                if size
                else 0.0
            )

        confident_failure = bool(
            incorrect_fraction > 0.0
            and stats["n_clusters"] >= 2
            and stats["cluster_imbalance"]
            >= 1.5
        )

        cluster_ids_serialized = (
            ",".join(
                str(int(value))
                for value in labels
            )
        )

        cluster_sizes_serialized = (
            ",".join(
                str(value)
                for value in cluster_sizes
            )
        )

        cluster_incorrect_serialized = (
            ",".join(
                str(value)
                for value
                in cluster_incorrect_counts
            )
        )

        cluster_fraction_serialized = (
            ",".join(
                f"{value:.6f}"
                for value
                in cluster_incorrect_fraction
            )
        )

        # -------------------------------------------------------------
        # One row per response.
        #
        # Graph-level measurements are repeated for each response in
        # the case, while correctness/error metadata remains response-
        # specific.
        # -------------------------------------------------------------

        for response_index, response in enumerate(
            responses
        ):

            row = {
                "case_id": case["case_id"],
                "question": case["question"],
                "response_index": response_index,
                "response": response,
                "correct": int(
                    correctness[
                        response_index
                    ]
                ),
                "error_type": error_types[
                    response_index
                ],
                "clustering_threshold": 0.30,
                "cluster_ids": (
                    cluster_ids_serialized
                ),
                **stats,
                "incorrect_responses": (
                    incorrect_count
                ),
                "incorrect_fraction": (
                    incorrect_fraction
                ),
                "confident_failure": (
                    confident_failure
                ),
                "structural_entropy": (
                    entropy
                ),
                "cluster_sizes": (
                    cluster_sizes_serialized
                ),
                "cluster_incorrect_counts": (
                    cluster_incorrect_serialized
                ),
                "cluster_incorrect_fraction": (
                    cluster_fraction_serialized
                ),
            }

            rows.append(row)

    # -----------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------

    if not rows:

        raise RuntimeError(
            "No successful SeSE evaluations "
            "were generated."
        )

    fieldnames = [
        "case_id",
        "question",
        "response_index",
        "response",
        "correct",
        "error_type",
        "clustering_threshold",
        "cluster_ids",
        "n_nodes",
        "n_clusters",
        "n_edges",
        "edge_density",
        "mean_edge_weight",
        "total_edge_weight",
        "cluster_imbalance",
        "largest_cluster",
        "smallest_cluster",
        "incorrect_responses",
        "incorrect_fraction",
        "confident_failure",
        "structural_entropy",
        "cluster_sizes",
        "cluster_incorrect_counts",
        "cluster_incorrect_fraction",
    ]

    with open(
        OUTPUT,
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        writer.writerows(rows)

    successful_cases = len(
        {
            row["case_id"]
            for row in rows
        }
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "RESULTS SAVED"
    )

    print(
        "=" * 70
    )

    print(
        OUTPUT
    )

    print(
        f"Rows saved: {len(rows)}"
    )

    print(
        f"Successful cases: "
        f"{successful_cases}/{len(CASES)}"
    )

    if successful_cases < len(CASES):

        print(
            "WARNING: Some cases failed. "
            "Inspect the errors above."
        )


# ---------------------------------------------------------------------
# Windows-safe entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()