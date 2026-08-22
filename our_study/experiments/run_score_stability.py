"""
Experiment 2: SeSE score stability under repeated sampling.

IMPORTANT:
- original_work/ is never modified.
- All experiment logic lives inside our_study/.
- The experiment asks whether the same question produces stable
  uncertainty scores when the response sample changes.
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
# Configuration
# ---------------------------------------------------------------------

N_REPEATS = 5
SAMPLE_SIZE = 6
SEED = 2026

QUESTION = "Who discovered penicillin?"

RESPONSES = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Penicillin was discovered by Alexander Fleming.",
    "Fleming discovered penicillin in 1928.",
    "Alexander Fleming is credited with discovering penicillin.",
    "Penicillin was discovered by Marie Curie.",
    "Marie Curie discovered penicillin in the early twentieth century.",
    "Alexander Fleming is widely credited with the discovery of penicillin.",
    "The discovery of penicillin is attributed to Alexander Fleming.",
    "Marie Curie discovered penicillin during the early 1900s.",
    "Fleming found penicillin in 1928.",
]


# ---------------------------------------------------------------------
# Imports from original SeSE
# ---------------------------------------------------------------------

print("Loading SeSE components...")

from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (
    compute_entailment_scores,
    compute_sentence_transformer_similirities,
    enhancing_answers,
    make_connected,
)

from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
    compute_se,
)

print("SeSE components loaded.")


# ---------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------

def build_graph(
    responses: list[str],
    question: str,
    similarity_threshold: float = 0.30,
) -> np.ndarray:
    """
    Reproduce the semantic graph construction used by the
    threshold-sensitivity experiment.

    This function does NOT modify original SeSE.
    """

    enhanced = enhancing_answers(
        responses,
        question,
    )

    print("  Computing sentence similarities...")
    cos_sim = compute_sentence_transformer_similirities(
        enhanced
    )

    print("  Computing NLI similarities...")
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
        if cluster_ids[i] == cluster_ids[j]
    ]

    if pairs:
        print(
            f"  Using entailment scores for "
            f"{len(pairs)} intra-cluster edges..."
        )

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


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

def main() -> None:

    print()
    print("SeSE score stability experiment")
    print("=" * 50)
    print("Original work: UNMODIFIED")
    print()

    rng = np.random.default_rng(SEED)

    scores = []

    output_dir = (
        PROJECT_ROOT
        / "results"
        / "score_stability"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir
        / "score_stability_results.csv"
    )

    for repeat in range(N_REPEATS):

        print(
            f"Repeat {repeat + 1}/{N_REPEATS}"
        )

        # Sample responses without replacement.
        indices = rng.choice(
            len(RESPONSES),
            size=min(
                SAMPLE_SIZE,
                len(RESPONSES),
            ),
            replace=False,
        )

        sampled_responses = [
            RESPONSES[i]
            for i in indices
        ]

        adjacency = build_graph(
            sampled_responses,
            QUESTION,
        )

        entropy = float(
            compute_se(adjacency)
        )

        scores.append(entropy)

        print(
            f"  structural entropy: "
            f"{entropy:.8f}"
        )
        print()

    # -----------------------------------------------------------------
    # Stability statistics
    # -----------------------------------------------------------------

    scores_array = np.asarray(
        scores,
        dtype=float,
    )

    mean_score = float(
        np.mean(scores_array)
    )

    std_score = float(
        np.std(
            scores_array,
            ddof=1,
        )
        if len(scores_array) > 1
        else 0.0
    )

    min_score = float(
        np.min(scores_array)
    )

    max_score = float(
        np.max(scores_array)
    )

    score_range = max_score - min_score

    coefficient_of_variation = (
        abs(std_score / mean_score)
        if mean_score != 0
        else 0.0
    )

    # -----------------------------------------------------------------
    # Save results
    # -----------------------------------------------------------------

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "repeat",
                "structural_entropy",
            ]
        )

        for i, score in enumerate(
            scores_array,
            start=1,
        ):
            writer.writerow(
                [
                    i,
                    score,
                ]
            )

        writer.writerow([])
        writer.writerow(
            [
                "mean",
                mean_score,
            ]
        )

        writer.writerow(
            [
                "std",
                std_score,
            ]
        )

        writer.writerow(
            [
                "min",
                min_score,
            ]
        )

        writer.writerow(
            [
                "max",
                max_score,
            ]
        )

        writer.writerow(
            [
                "range",
                score_range,
            ]
        )

        writer.writerow(
            [
                "coefficient_of_variation",
                coefficient_of_variation,
            ]
        )

    # -----------------------------------------------------------------
    # Report
    # -----------------------------------------------------------------

    print("=" * 50)
    print("STABILITY SUMMARY")
    print("=" * 50)

    print(
        f"Mean score:              "
        f"{mean_score:.8f}"
    )

    print(
        f"Standard deviation:      "
        f"{std_score:.8f}"
    )

    print(
        f"Minimum score:           "
        f"{min_score:.8f}"
    )

    print(
        f"Maximum score:           "
        f"{max_score:.8f}"
    )

    print(
        f"Score range:             "
        f"{score_range:.8f}"
    )

    print(
        f"Coefficient variation:   "
        f"{coefficient_of_variation:.8f}"
    )

    print()
    print(
        f"Results saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    main()