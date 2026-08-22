"""
Experiment 1: Clustering-threshold sensitivity.

We reproduce the relevant SeSE semantic-graph construction logic
without modifying original_work/.

The experiment varies only the clustering similarity threshold.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SESE = PROJECT_ROOT.parent / "original_work" / "SeSE"

sys.path.insert(0, str(ORIGINAL_SESE))

from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (  # noqa: E501
    compute_entailment_scores,
    compute_sentence_transformer_similirities,
    enhancing_answers,
    make_connected,
)
from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
    compute_se,
)


THRESHOLDS = [0.20, 0.25, 0.30, 0.35, 0.40]


def build_graph_with_threshold(
    responses: list[str],
    question: str,
    similarity_threshold: float,
) -> tuple[np.ndarray, list[int], list[str]]:
    """
    Reproduce SeSE graph construction while exposing the
    clustering similarity threshold.
    """

    enhanced = enhancing_answers(responses, question)

    cos_sim = compute_sentence_transformer_similirities(enhanced)
    entail_sim = compute_entailment_scores(enhanced)

    w_entail = 0.65

    similarity = np.clip(
        w_entail * entail_sim
        + (1.0 - w_entail) * cos_sim,
        0.0,
        1.0,
    )

    distance = 1.0 - similarity
    np.fill_diagonal(distance, 0.0)

    from sklearn.cluster import AgglomerativeClustering

    non_diag = distance[
        ~np.eye(len(distance), dtype=bool)
    ]

    if np.all(non_diag == 0.0):
        cluster_ids = [0] * len(enhanced)

    elif np.all(non_diag == 1.0):
        cluster_ids = list(range(len(enhanced)))

    else:
        clusterer = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1.0 - similarity_threshold,
            metric="precomputed",
            linkage="average",
        )

        cluster_ids = clusterer.fit_predict(distance).tolist()

    n = len(enhanced)

    adjacency = np.zeros(
        (n, n),
        dtype=np.float32,
    )

    pairs = [
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if cluster_ids[i] == cluster_ids[j]
    ]

    if pairs:
        edge_scores = compute_entailment_scores(
            enhanced
        )

        for i, j in pairs:
            adjacency[i, j] = edge_scores[i, j]
            adjacency[j, i] = edge_scores[j, i]

    adjacency = np.asarray(
        make_connected(adjacency, enhanced),
        dtype=np.float32,
    )

    return adjacency, cluster_ids, enhanced


def summarize_graph(
    adjacency: np.ndarray,
    cluster_ids: list[int],
) -> dict:
    """Return interpretable graph statistics."""

    n = adjacency.shape[0]

    edge_mask = np.triu(
        np.ones_like(adjacency, dtype=bool),
        k=1,
    )

    positive_edges = adjacency[edge_mask] > 0

    return {
        "n_nodes": n,
        "n_clusters": len(set(cluster_ids)),
        "n_edges": int(np.sum(positive_edges)),
        "mean_edge_weight": float(
            adjacency[edge_mask][positive_edges].mean()
        )
        if np.any(positive_edges)
        else 0.0,
        "total_edge_weight": float(
            adjacency[edge_mask].sum()
        ),
    }


def main():
    # Small controlled example for pipeline validation.
    #
    # We intentionally use multiple semantically related responses
    # so that clustering has something meaningful to separate.
    question = "Who discovered penicillin?"

    responses = [
        "Alexander Fleming discovered penicillin in 1928.",
        "Penicillin was discovered by Alexander Fleming.",
        "Fleming discovered penicillin in 1928.",
        "Alexander Fleming is credited with discovering penicillin.",
        "Penicillin was discovered by Marie Curie.",
        "Marie Curie discovered penicillin in the early twentieth century.",
    ]

    print("SeSE threshold sensitivity experiment")
    print("=" * 45)
    print()

    for threshold in THRESHOLDS:
        print(f"Threshold: {threshold:.2f}")

        adjacency, cluster_ids, enhanced = (
            build_graph_with_threshold(
                responses,
                question,
                threshold,
            )
        )

        structural_entropy = compute_se(adjacency)

        summary = summarize_graph(
            adjacency,
            cluster_ids,
        )

        print(
            f"  clusters: {summary['n_clusters']}"
        )

        print(
            f"  edges: {summary['n_edges']}"
        )

        print(
            f"  mean edge weight: "
            f"{summary['mean_edge_weight']:.4f}"
        )

        print(
            f"  total edge weight: "
            f"{summary['total_edge_weight']:.4f}"
        )

        print(
            f"  structural entropy: "
            f"{structural_entropy:.6f}"
        )

        print(
            f"  cluster IDs: "
            f"{cluster_ids}"
        )

        print()


if __name__ == "__main__":
    main()