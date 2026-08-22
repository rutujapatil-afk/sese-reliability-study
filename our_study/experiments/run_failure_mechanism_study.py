"""
Experiment 4: SeSE failure-mechanism analysis.

Goal
----
Compare structural properties of semantic graphs for:
    1. correct answers
    2. incorrect answers
    3. confident failures

IMPORTANT
---------
This experiment is independent of original_work/.
Nothing inside original_work/ is modified.
"""

from __future__ import annotations

import csv
import itertools
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SESE = PROJECT_ROOT.parent / "original_work" / "SeSE"

sys.path.insert(0, str(ORIGINAL_SESE))


# ---------------------------------------------------------------------
# Import original SeSE functions WITHOUT modifying original_work
# ---------------------------------------------------------------------

from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (  # noqa: E501
    compute_entailment_scores,
    compute_sentence_transformer_similirities,
    enhancing_answers,
    make_connected,
)

from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
    compute_se,
)


# ---------------------------------------------------------------------
# Experimental data
# ---------------------------------------------------------------------

# Each case represents one question with multiple sampled answers.
#
# correctness is assigned at the RESPONSE level.
#
# This allows us to ask:
#
#   "What does the semantic graph look like when the answer set
#    contains a confident but incorrect semantic cluster?"
#
# The examples are intentionally controlled and small for validation.
# The next stage can replace these with benchmark samples.

CASES = [
    {
        "case_id": "penicillin",
        "question": "Who discovered penicillin?",
        "responses": [
            "Alexander Fleming discovered penicillin in 1928.",
            "Penicillin was discovered by Alexander Fleming.",
            "Fleming discovered penicillin in 1928.",
            "Alexander Fleming is credited with discovering penicillin.",
            "Penicillin was discovered by Marie Curie.",
            "Marie Curie discovered penicillin in the early twentieth century.",
        ],
        "correct": [True, True, True, True, False, False],
    },
    {
        "case_id": "capital_france",
        "question": "What is the capital of France?",
        "responses": [
            "Paris is the capital of France.",
            "The capital of France is Paris.",
            "France has Paris as its capital.",
            "Paris serves as the capital city of France.",
            "The capital of France is Lyon.",
            "Lyon is the capital of France.",
        ],
        "correct": [True, True, True, True, False, False],
    },
    {
        "case_id": "planet",
        "question": "Which planet is known as the Red Planet?",
        "responses": [
            "Mars is known as the Red Planet.",
            "The Red Planet is Mars.",
            "Mars is called the Red Planet because of its reddish appearance.",
            "The planet known as the Red Planet is Mars.",
            "Jupiter is known as the Red Planet.",
            "Jupiter is called the Red Planet.",
        ],
        "correct": [True, True, True, True, False, False],
    },
]


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

CLUSTERING_THRESHOLD = 0.30

# A "confident failure" is operationalized as:
#
#   incorrect response belonging to a cluster containing
#   at least one other incorrect response.
#
# This is deliberately structural rather than score-dependent.
#
# We also record the cluster-level fraction of incorrect responses.

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "failure_mechanism"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------

def build_graph(
    responses: list[str],
    question: str,
    threshold: float,
):
    """
    Reproduce the relevant SeSE graph construction independently.

    original_work/ is imported but never edited.
    """

    enhanced = enhancing_answers(
        responses,
        question,
    )

    cos_sim = compute_sentence_transformer_similirities(
        enhanced
    )

    entail_sim = compute_entailment_scores(
        enhanced
    )

    w_entail = 0.65

    similarity = np.clip(
        w_entail * entail_sim
        + (1.0 - w_entail) * cos_sim,
        0.0,
        1.0,
    )

    distance = 1.0 - similarity

    np.fill_diagonal(
        distance,
        0.0,
    )

    from sklearn.cluster import AgglomerativeClustering

    non_diag = distance[
        ~np.eye(
            len(distance),
            dtype=bool,
        )
    ]

    if np.all(non_diag == 0.0):

        cluster_ids = [
            0
        ] * len(enhanced)

    elif np.all(non_diag == 1.0):

        cluster_ids = list(
            range(len(enhanced))
        )

    else:

        clusterer = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1.0 - threshold,
            metric="precomputed",
            linkage="average",
        )

        cluster_ids = (
            clusterer
            .fit_predict(distance)
            .tolist()
        )

    n = len(enhanced)

    adjacency = np.zeros(
        (n, n),
        dtype=np.float32,
    )

    pairs = [
        (i, j)
        for i, j in itertools.combinations(
            range(n),
            2,
        )
        if cluster_ids[i]
        == cluster_ids[j]
    ]

    if pairs:

        print(
            f"    Computing entailment "
            f"for {len(pairs)} intra-cluster edges..."
        )

        edge_scores = compute_entailment_scores(
            enhanced
        )

        for i, j in pairs:

            adjacency[i, j] = (
                edge_scores[i, j]
            )

            adjacency[j, i] = (
                edge_scores[j, i]
            )

    adjacency = np.asarray(
        make_connected(
            adjacency,
            enhanced,
        ),
        dtype=np.float32,
    )

    return (
        adjacency,
        cluster_ids,
        enhanced,
    )


# ---------------------------------------------------------------------
# Structural measurements
# ---------------------------------------------------------------------

def graph_statistics(
    adjacency: np.ndarray,
    cluster_ids: list[int],
    correct: list[bool],
) -> dict:

    n = adjacency.shape[0]

    upper = np.triu(
        np.ones_like(
            adjacency,
            dtype=bool,
        ),
        k=1,
    )

    weights = adjacency[upper]

    positive = weights > 0

    n_edges = int(
        np.sum(positive)
    )

    possible_edges = (
        n * (n - 1) // 2
    )

    density = (
        n_edges / possible_edges
        if possible_edges
        else 0.0
    )

    positive_weights = (
        weights[positive]
    )

    mean_weight = (
        float(
            positive_weights.mean()
        )
        if len(positive_weights)
        else 0.0
    )

    total_weight = float(
        weights.sum()
    )

    # -------------------------------------------------------------
    # Cluster statistics
    # -------------------------------------------------------------

    unique_clusters = sorted(
        set(cluster_ids)
    )

    cluster_sizes = []

    cluster_correct = []

    cluster_incorrect = []

    cluster_incorrect_fraction = []

    for cluster in unique_clusters:

        indices = [
            i
            for i, c in enumerate(
                cluster_ids
            )
            if c == cluster
        ]

        labels = [
            correct[i]
            for i in indices
        ]

        size = len(indices)

        n_correct = sum(labels)

        n_incorrect = (
            size - n_correct
        )

        fraction_incorrect = (
            n_incorrect / size
            if size
            else 0.0
        )

        cluster_sizes.append(size)
        cluster_correct.append(
            n_correct
        )
        cluster_incorrect.append(
            n_incorrect
        )
        cluster_incorrect_fraction.append(
            fraction_incorrect
        )

    # -------------------------------------------------------------
    # Cluster imbalance
    # -------------------------------------------------------------

    if cluster_sizes:

        cluster_imbalance = (
            max(cluster_sizes)
            / min(cluster_sizes)
        )

    else:

        cluster_imbalance = 0.0

    # -------------------------------------------------------------
    # Incorrect concentration
    # -------------------------------------------------------------

    incorrect_indices = [
        i
        for i, value in enumerate(correct)
        if not value
    ]

    confident_failure = False

    if incorrect_indices:

        for cluster in unique_clusters:

            members = [
                i
                for i, c in enumerate(
                    cluster_ids
                )
                if c == cluster
            ]

            incorrect_members = [
                i
                for i in members
                if not correct[i]
            ]

            if len(incorrect_members) >= 2:

                confident_failure = True

                break

    # -------------------------------------------------------------
    # Structural entropy
    # -------------------------------------------------------------

    structural_entropy = float(
        compute_se(adjacency)
    )

    return {
        "n_nodes": n,
        "n_edges": n_edges,
        "edge_density": density,
        "mean_edge_weight": mean_weight,
        "total_edge_weight": total_weight,
        "n_clusters": len(
            unique_clusters
        ),
        "cluster_imbalance": cluster_imbalance,
        "largest_cluster": (
            max(cluster_sizes)
            if cluster_sizes
            else 0
        ),
        "smallest_cluster": (
            min(cluster_sizes)
            if cluster_sizes
            else 0
        ),
        "incorrect_responses": len(
            incorrect_indices
        ),
        "incorrect_fraction": (
            len(incorrect_indices)
            / n
            if n
            else 0.0
        ),
        "confident_failure": int(
            confident_failure
        ),
        "structural_entropy": (
            structural_entropy
        ),
        "cluster_sizes": ";".join(
            map(
                str,
                cluster_sizes,
            )
        ),
        "cluster_incorrect_counts": ";".join(
            map(
                str,
                cluster_incorrect,
            )
        ),
        "cluster_incorrect_fraction": ";".join(
            f"{x:.4f}"
            for x in cluster_incorrect_fraction
        ),
    }


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

def main():

    print()
    print(
        "SESE FAILURE-MECHANISM STUDY"
    )
    print(
        "=" * 60
    )
    print(
        "Original work: UNMODIFIED"
    )
    print(
        f"Clustering threshold: "
        f"{CLUSTERING_THRESHOLD:.2f}"
    )
    print()

    rows = []

    for case in CASES:

        print(
            "-" * 60
        )

        print(
            f"Case: {case['case_id']}"
        )

        print(
            f"Question: "
            f"{case['question']}"
        )

        print()

        adjacency, cluster_ids, enhanced = (
            build_graph(
                case["responses"],
                case["question"],
                CLUSTERING_THRESHOLD,
            )
        )

        stats = graph_statistics(
            adjacency,
            cluster_ids,
            case["correct"],
        )

        row = {
            "case_id": case["case_id"],
            "question": case["question"],
            "clustering_threshold": (
                CLUSTERING_THRESHOLD
            ),
            "cluster_ids": ";".join(
                map(
                    str,
                    cluster_ids,
                )
            ),
            **stats,
        }

        rows.append(row)

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
            f"    mean edge weight: "
            f"{stats['mean_edge_weight']:.4f}"
        )

        print(
            f"    cluster imbalance: "
            f"{stats['cluster_imbalance']:.4f}"
        )

        print(
            f"    incorrect fraction: "
            f"{stats['incorrect_fraction']:.4f}"
        )

        print(
            f"    confident failure: "
            f"{bool(stats['confident_failure'])}"
        )

        print(
            f"    structural entropy: "
            f"{stats['structural_entropy']:.8f}"
        )

        print()

    # -----------------------------------------------------------------
    # Save detailed results
    # -----------------------------------------------------------------

    detailed_path = (
        OUTPUT_DIR
        / "failure_mechanism_results.csv"
    )

    fieldnames = list(
        rows[0].keys()
    )

    with detailed_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------

    summary_path = (
        OUTPUT_DIR
        / "failure_mechanism_summary.csv"
    )

    summary_rows = []

    for failure_value, label in [
        (0, "no_confident_failure"),
        (1, "confident_failure"),
    ]:

        subset = [
            r
            for r in rows
            if r["confident_failure"]
            == failure_value
        ]

        if not subset:
            continue

        def avg(key):

            return float(
                np.mean(
                    [
                        r[key]
                        for r in subset
                    ]
                )
            )

        summary_rows.append(
            {
                "group": label,
                "n_cases": len(subset),
                "mean_clusters": avg(
                    "n_clusters"
                ),
                "mean_edges": avg(
                    "n_edges"
                ),
                "mean_density": avg(
                    "edge_density"
                ),
                "mean_edge_weight": avg(
                    "mean_edge_weight"
                ),
                "mean_total_edge_weight": avg(
                    "total_edge_weight"
                ),
                "mean_cluster_imbalance": avg(
                    "cluster_imbalance"
                ),
                "mean_structural_entropy": avg(
                    "structural_entropy"
                ),
            }
        )

    if summary_rows:

        with summary_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=list(
                    summary_rows[0].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                summary_rows
            )

    print(
        "=" * 60
    )

    print(
        "RESULTS SAVED"
    )

    print(
        detailed_path
    )

    print(
        summary_path
    )

    print()


if __name__ == "__main__":

    # Required for Windows multiprocessing.
    import multiprocessing

    multiprocessing.freeze_support()

    main()