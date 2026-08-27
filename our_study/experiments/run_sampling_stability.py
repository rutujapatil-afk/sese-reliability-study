"""
Experiment 2: Sampling / score stability.

This experiment studies how stable the SeSE structural-entropy score is
when the semantic graph is subjected to controlled stochastic variation.

IMPORTANT:
- original_work/ is never modified.
- All experiment code lives under our_study/.
- Seeds are explicit and reproducible.
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

from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (
    compute_entailment_scores,
    compute_sentence_transformer_similirities,
    enhancing_answers,
    make_connected,
)
from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
    compute_se,
)


# ---------------------------------------------------------------------------
# Experiment configuration
# ---------------------------------------------------------------------------

SEEDS = [42, 123, 2026]

QUESTION = "Who discovered penicillin?"

RESPONSES = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Penicillin was discovered by Alexander Fleming.",
    "Fleming discovered penicillin in 1928.",
    "Alexander Fleming is credited with discovering penicillin.",
    "Penicillin was discovered by Marie Curie.",
    "Marie Curie discovered penicillin in the early twentieth century.",
]

# Small controlled perturbation used only to study score stability.
NOISE_LEVEL = 0.05

OUTPUT_DIR = PROJECT_ROOT / "results" / "sampling_stability"
OUTPUT_FILE = OUTPUT_DIR / "sampling_stability_results.csv"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_baseline_graph(
    responses: list[str],
    question: str,
) -> np.ndarray:
    """
    Reproduce the semantic graph construction used by our study.

    This function does not modify original SeSE code.
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

    similarity_threshold = 0.30

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
        for i, j in itertools.combinations(
            range(n),
            2,
        )
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
        make_connected(
            adjacency,
            enhanced,
        ),
        dtype=np.float32,
    )

    return adjacency


# ---------------------------------------------------------------------------
# Controlled stochastic variation
# ---------------------------------------------------------------------------

def perturb_graph(
    adjacency: np.ndarray,
    seed: int,
) -> np.ndarray:
    """
    Apply reproducible bounded Gaussian noise to graph edge weights.

    The diagonal is preserved.
    Values remain in [0, 1].
    """

    rng = np.random.default_rng(seed)

    perturbed = adjacency.astype(
        np.float64,
        copy=True,
    )

    noise = rng.normal(
        loc=0.0,
        scale=NOISE_LEVEL,
        size=perturbed.shape,
    )

    perturbed += noise

    np.fill_diagonal(
        perturbed,
        np.diag(adjacency),
    )

    perturbed = np.clip(
        perturbed,
        0.0,
        1.0,
    )

    return perturbed


# ---------------------------------------------------------------------------
# Graph statistics
# ---------------------------------------------------------------------------

def graph_statistics(
    adjacency: np.ndarray,
) -> dict[str, float]:
    """Calculate basic graph statistics."""

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

    possible_edges = n * (n - 1) / 2

    return {
        "n_nodes": n,
        "n_edges": int(np.sum(positive)),
        "edge_density": (
            float(np.sum(positive) / possible_edges)
            if possible_edges > 0
            else 0.0
        ),
        "mean_edge_weight": (
            float(weights[positive].mean())
            if np.any(positive)
            else 0.0
        ),
        "total_edge_weight": float(
            weights.sum()
        ),
    }


def relative_graph_change(
    original: np.ndarray,
    perturbed: np.ndarray,
) -> float:
    """Calculate relative Frobenius graph change."""

    denominator = np.linalg.norm(
        original,
        ord="fro",
    )

    if denominator == 0:
        return float(
            np.linalg.norm(
                perturbed,
                ord="fro",
            )
        )

    return float(
        np.linalg.norm(
            perturbed - original,
            ord="fro",
        )
        / denominator
    )


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main() -> None:
    print(
        "SeSE repeated-sampling stability experiment"
    )
    print("=" * 55)
    print()
    print("Original work: UNMODIFIED")
    print()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Building baseline semantic graph...")

    baseline_graph = build_baseline_graph(
        RESPONSES,
        QUESTION,
    )

    baseline_entropy = float(
        compute_se(
            baseline_graph
        )
    )

    baseline_stats = graph_statistics(
        baseline_graph
    )

    print(
        f"Baseline structural entropy: "
        f"{baseline_entropy:.6f}"
    )

    print(
        f"Baseline edges: "
        f"{baseline_stats['n_edges']}"
    )

    print()

    rows = []

    for seed in SEEDS:

        print(
            f"Seed {seed}: computing perturbed score..."
        )

        perturbed_graph = perturb_graph(
            baseline_graph,
            seed,
        )

        perturbed_entropy = float(
            compute_se(
                perturbed_graph
            )
        )

        stats = graph_statistics(
            perturbed_graph
        )

        graph_change = relative_graph_change(
            baseline_graph,
            perturbed_graph,
        )

        absolute_entropy_change = (
            perturbed_entropy
            - baseline_entropy
        )

        relative_entropy_change = (
            absolute_entropy_change
            / abs(baseline_entropy)
            if baseline_entropy != 0
            else 0.0
        )

        rows.append(
            {
                "question": QUESTION,
                "seed": seed,
                "noise_level": NOISE_LEVEL,
                "baseline_entropy": baseline_entropy,
                "perturbed_entropy": perturbed_entropy,
                "absolute_entropy_change": absolute_entropy_change,
                "relative_entropy_change": relative_entropy_change,
                "relative_graph_change": graph_change,
                **stats,
            }
        )

        print(
            f"  entropy: "
            f"{perturbed_entropy:.6f}"
        )

        print(
            f"  graph change: "
            f"{graph_change:.6f}"
        )

        print()

    fieldnames = list(
        rows[0].keys()
    )

    with OUTPUT_FILE.open(
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

    entropy_values = np.array(
        [
            row["perturbed_entropy"]
            for row in rows
        ],
        dtype=float,
    )

    graph_changes = np.array(
        [
            row["relative_graph_change"]
            for row in rows
        ],
        dtype=float,
    )

    print("=" * 55)
    print("Stability summary")
    print("=" * 55)

    print(
        f"Mean entropy: "
        f"{entropy_values.mean():.6f}"
    )

    print(
        f"Entropy standard deviation: "
        f"{entropy_values.std(ddof=1):.6f}"
    )

    print(
        f"Entropy range: "
        f"{entropy_values.min():.6f} "
        f"to "
        f"{entropy_values.max():.6f}"
    )

    print(
        f"Mean relative graph change: "
        f"{graph_changes.mean():.6f}"
    )

    print()
    print(
        f"Results saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()