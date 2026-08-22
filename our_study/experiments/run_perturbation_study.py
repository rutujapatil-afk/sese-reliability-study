"""
Experiment 2: Semantic-graph robustness under controlled perturbations.

This experiment does NOT modify original_work/.

We:
1. construct a baseline semantic graph using the original SeSE components;
2. apply controlled edge-weight noise and edge dropout;
3. measure graph change and structural-entropy change;
4. repeat perturbations across multiple random seeds;
5. save machine-readable results for later analysis.

The original SeSE implementation is treated as read-only.
"""

from __future__ import annotations

import csv
import itertools
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

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

# Our independent perturbation utilities.
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from semantic_perturbation import (  # noqa: E402
    add_edge_weight_noise,
    randomly_dropout_edges,
    relative_frobenius_change,
)


# ---------------------------------------------------------------------------
# Experimental configuration
# ---------------------------------------------------------------------------

NOISE_LEVELS = [0.00, 0.05, 0.10, 0.20]
DROPOUT_LEVELS = [0.00, 0.05, 0.10, 0.20]
SEEDS = [42, 123, 2026]

OUTPUT_DIR = PROJECT_ROOT / "results" / "semantic_perturbation"
OUTPUT_FILE = OUTPUT_DIR / "perturbation_results.csv"


# ---------------------------------------------------------------------------
# Controlled example
# ---------------------------------------------------------------------------

QUESTION = "Who discovered penicillin?"

RESPONSES = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Penicillin was discovered by Alexander Fleming.",
    "Fleming discovered penicillin in 1928.",
    "Alexander Fleming is credited with discovering penicillin.",
    "Penicillin was discovered by Marie Curie.",
    "Marie Curie discovered penicillin in the early twentieth century.",
]


# ---------------------------------------------------------------------------
# Baseline graph construction
# ---------------------------------------------------------------------------

def construct_baseline_graph(
    responses: list[str],
    question: str,
) -> tuple[np.ndarray, list[str]]:
    """
    Construct the semantic adjacency matrix using the SeSE components.

    Nothing in original_work/ is modified.
    """

    print("  Enhancing responses...")
    enhanced = enhancing_answers(responses, question)

    print("  Computing sentence similarities...")
    cosine_similarity = (
        compute_sentence_transformer_similirities(enhanced)
    )

    print("  Computing NLI similarities...")
    entailment_similarity = compute_entailment_scores(enhanced)

    # Same weighted combination used by our threshold experiment.
    w_entail = 0.65

    similarity = np.clip(
        w_entail * entailment_similarity
        + (1.0 - w_entail) * cosine_similarity,
        0.0,
        1.0,
    )

    distance = 1.0 - similarity
    np.fill_diagonal(distance, 0.0)

    from sklearn.cluster import AgglomerativeClustering

    threshold = 0.30

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
            distance_threshold=1.0 - threshold,
            metric="precomputed",
            linkage="average",
        )

        cluster_ids = clusterer.fit_predict(
            distance
        ).tolist()

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

    print(
        f"  Computing entailment for "
        f"{len(pairs)} intra-cluster edges..."
    )

    if pairs:
        edge_scores = compute_entailment_scores(enhanced)

        for i, j in pairs:
            adjacency[i, j] = edge_scores[i, j]
            adjacency[j, i] = edge_scores[j, i]

    adjacency = np.asarray(
        make_connected(adjacency, enhanced),
        dtype=np.float32,
    )

    return adjacency, enhanced


# ---------------------------------------------------------------------------
# Graph statistics
# ---------------------------------------------------------------------------

def graph_statistics(
    matrix: np.ndarray,
) -> dict[str, float]:
    """Return basic statistics for a semantic graph."""

    matrix = np.asarray(matrix, dtype=float)

    n = matrix.shape[0]

    upper = np.triu_indices(n, k=1)
    weights = matrix[upper]

    positive = weights > 0

    return {
        "n_nodes": int(n),
        "n_edges": int(np.sum(positive)),
        "total_edge_weight": float(np.sum(weights)),
        "mean_edge_weight": (
            float(np.mean(weights[positive]))
            if np.any(positive)
            else 0.0
        ),
        "edge_density": (
            float(np.sum(positive) / len(weights))
            if len(weights) > 0
            else 0.0
        ),
    }


# ---------------------------------------------------------------------------
# Result writer
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "perturbation",
    "level",
    "seed",
    "relative_graph_change",
    "baseline_entropy",
    "perturbed_entropy",
    "absolute_entropy_change",
    "relative_entropy_change",
    "n_nodes",
    "n_edges",
    "edge_density",
    "mean_edge_weight",
    "total_edge_weight",
]


def save_results(rows: list[dict]) -> None:
    """Save experiment results to CSV."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------------

def run_experiment() -> list[dict]:
    print("Constructing baseline semantic graph...")
    print()

    baseline, enhanced = construct_baseline_graph(
        RESPONSES,
        QUESTION,
    )

    baseline_entropy = float(
        compute_se(baseline)
    )

    baseline_stats = graph_statistics(
        baseline
    )

    print()
    print("Baseline graph")
    print("-" * 45)
    print(
        f"Nodes:             "
        f"{baseline_stats['n_nodes']}"
    )
    print(
        f"Edges:             "
        f"{baseline_stats['n_edges']}"
    )
    print(
        f"Edge density:      "
        f"{baseline_stats['edge_density']:.4f}"
    )
    print(
        f"Mean edge weight:   "
        f"{baseline_stats['mean_edge_weight']:.4f}"
    )
    print(
        f"Total edge weight:  "
        f"{baseline_stats['total_edge_weight']:.4f}"
    )
    print(
        f"Structural entropy: "
        f"{baseline_entropy:.6f}"
    )
    print()

    rows: list[dict] = []

    # ---------------------------------------------------------------
    # Edge-weight noise
    # ---------------------------------------------------------------

    print("Experiment A: Edge-weight noise")
    print("=" * 45)

    for level in NOISE_LEVELS:

        for seed in SEEDS:

            if level == 0.0:
                perturbed = baseline.copy()
            else:
                perturbed = add_edge_weight_noise(
                    baseline,
                    noise_level=level,
                    seed=seed,
                )

            change = relative_frobenius_change(
                baseline,
                perturbed,
            )

            entropy = float(
                compute_se(perturbed)
            )

            stats = graph_statistics(
                perturbed
            )

            absolute_entropy_change = (
                entropy - baseline_entropy
            )

            if baseline_entropy != 0:
                relative_entropy_change = (
                    absolute_entropy_change
                    / abs(baseline_entropy)
                )
            else:
                relative_entropy_change = 0.0

            row = {
                "perturbation": "edge_weight_noise",
                "level": level,
                "seed": seed,
                "relative_graph_change": change,
                "baseline_entropy": baseline_entropy,
                "perturbed_entropy": entropy,
                "absolute_entropy_change": absolute_entropy_change,
                "relative_entropy_change": relative_entropy_change,
                **stats,
            }

            rows.append(row)

            print(
                f"noise={level:.2f} "
                f"seed={seed} "
                f"graph_change={change:.4f} "
                f"entropy={entropy:.6f}"
            )

    print()

    # ---------------------------------------------------------------
    # Edge dropout
    # ---------------------------------------------------------------

    print("Experiment B: Edge dropout")
    print("=" * 45)

    for level in DROPOUT_LEVELS:

        for seed in SEEDS:

            if level == 0.0:
                perturbed = baseline.copy()
            else:
                perturbed = randomly_dropout_edges(
                    baseline,
                    dropout_rate=level,
                    seed=seed,
                )

            change = relative_frobenius_change(
                baseline,
                perturbed,
            )

            entropy = float(
                compute_se(perturbed)
            )

            stats = graph_statistics(
                perturbed
            )

            absolute_entropy_change = (
                entropy - baseline_entropy
            )

            if baseline_entropy != 0:
                relative_entropy_change = (
                    absolute_entropy_change
                    / abs(baseline_entropy)
                )
            else:
                relative_entropy_change = 0.0

            row = {
                "perturbation": "edge_dropout",
                "level": level,
                "seed": seed,
                "relative_graph_change": change,
                "baseline_entropy": baseline_entropy,
                "perturbed_entropy": entropy,
                "absolute_entropy_change": absolute_entropy_change,
                "relative_entropy_change": relative_entropy_change,
                **stats,
            }

            rows.append(row)

            print(
                f"dropout={level:.2f} "
                f"seed={seed} "
                f"graph_change={change:.4f} "
                f"entropy={entropy:.6f}"
            )

    save_results(rows)

    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:

    print()
    print(
        "SeSE Semantic-Graph Robustness Study"
    )
    print("=" * 55)
    print("Original work: UNMODIFIED")
    print()

    rows = run_experiment()

    print()
    print("=" * 55)
    print("Experiment complete.")
    print(
        f"Results saved to:\n{OUTPUT_FILE}"
    )
    print(
        f"Total experimental rows: {len(rows)}"
    )


if __name__ == "__main__":
    main()