"""
Experiment: Clean SeSE score stability.

Purpose
-------
Measure whether the SeSE score is stable when the SAME fixed responses
are scored repeatedly.

Important:
- original_work/ is NOT modified.
- Responses are fixed.
- Answer enhancement is performed once only.
- The same enhanced responses are reused for every repetition.
- No OpenAI/API call is made inside the repetition loop.
- NLI and sentence embeddings are computed once and reused.
- Only the final graph/entropy calculation is repeated.

This isolates computational/stochastic stability from API enhancement.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORIGINAL_SESE = (
    PROJECT_ROOT.parent
    / "original_work"
    / "SeSE"
)

sys.path.insert(0, str(ORIGINAL_SESE))


# ---------------------------------------------------------------------
# Fixed experiment configuration
# ---------------------------------------------------------------------

N_REPEATS = 10

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "score_stability_clean"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "score_stability_clean_results.csv"
)


QUESTION = "Who discovered penicillin?"

RESPONSES = [
    "Alexander Fleming discovered penicillin in 1928.",
    "Penicillin was discovered by Alexander Fleming.",
    "Fleming discovered penicillin in 1928.",
    "Alexander Fleming is credited with discovering penicillin.",
    "Penicillin was discovered by Marie Curie.",
    "Marie Curie discovered penicillin in the early twentieth century.",
]


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

def main() -> None:

    print("SeSE CLEAN SCORE STABILITY EXPERIMENT")
    print("=" * 55)
    print("Original work: UNMODIFIED")
    print()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------
    # Import original SeSE components.
    #
    # This imports them from original_work but does not modify them.
    # -------------------------------------------------------------

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
    print()

    # -------------------------------------------------------------
    # STEP 1
    # Enhancement happens ONCE.
    #
    # This is deliberately outside the repeat loop.
    # -------------------------------------------------------------

    print("STEP 1/4: Preparing fixed responses...")
    print()

    print("Attempting answer enhancement once...")

    try:
        enhanced = enhancing_answers(
            RESPONSES,
            QUESTION,
        )

        if not enhanced or len(enhanced) != len(RESPONSES):
            raise RuntimeError(
                "Enhancement returned an invalid response set."
            )

        print("Enhancement succeeded.")

    except Exception as exc:
        print(
            "Enhancement unavailable."
        )
        print(
            f"Reason: {type(exc).__name__}: {exc}"
        )
        print(
            "Using the fixed original responses."
        )

        enhanced = list(RESPONSES)

    print()
    print("Fixed responses:")
    for i, response in enumerate(enhanced):
        print(f"  {i}: {response}")

    print()

    # -------------------------------------------------------------
    # STEP 2
    # Compute semantic similarities ONCE.
    # -------------------------------------------------------------

    print("STEP 2/4: Computing sentence similarities...")

    cos_sim = np.asarray(
        compute_sentence_transformer_similirities(
            enhanced
        ),
        dtype=float,
    )

    print("Sentence similarities computed.")
    print()

    # -------------------------------------------------------------
    # STEP 3
    # Compute NLI similarities ONCE.
    #
    # This avoids repeatedly loading/recomputing the expensive model.
    # -------------------------------------------------------------

    print("STEP 3/4: Computing NLI similarities...")

    entail_sim = np.asarray(
        compute_entailment_scores(
            enhanced
        ),
        dtype=float,
    )

    print("NLI similarities computed.")
    print()

    # -------------------------------------------------------------
    # Construct the fixed semantic similarity matrix.
    # -------------------------------------------------------------

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

    # -------------------------------------------------------------
    # Import clustering here.
    # -------------------------------------------------------------

    from sklearn.cluster import AgglomerativeClustering

    similarity_threshold = 0.30

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
            distance_threshold=(
                1.0 - similarity_threshold
            ),
            metric="precomputed",
            linkage="average",
        )

        cluster_ids = (
            clusterer
            .fit_predict(distance)
            .tolist()
        )

    print(
        f"Fixed clustering threshold: "
        f"{similarity_threshold:.2f}"
    )

    print(
        f"Fixed cluster IDs: "
        f"{cluster_ids}"
    )

    print(
        f"Fixed number of clusters: "
        f"{len(set(cluster_ids))}"
    )

    print()

    # -------------------------------------------------------------
    # Fixed intra-cluster graph.
    # -------------------------------------------------------------

    n = len(enhanced)

    adjacency_base = np.zeros(
        (n, n),
        dtype=np.float32,
    )

    for i in range(n):
        for j in range(i + 1, n):

            if cluster_ids[i] == cluster_ids[j]:

                adjacency_base[i, j] = (
                    entail_sim[i, j]
                )

                adjacency_base[j, i] = (
                    entail_sim[j, i]
                )

    # -------------------------------------------------------------
    # STEP 4
    #
    # Repeat only graph construction / connectivity / entropy.
    #
    # No API calls.
    # No model loading.
    # No embedding calculation.
    # No NLI calculation.
    # -------------------------------------------------------------

    print("STEP 4/4: Running stability repetitions...")
    print()

    scores = []

    rows = []

    for repeat in range(1, N_REPEATS + 1):

        print(
            f"Repeat {repeat}/{N_REPEATS}"
        )

        adjacency = np.asarray(
            make_connected(
                adjacency_base.copy(),
                enhanced,
            ),
            dtype=np.float32,
        )

        structural_entropy = float(
            compute_se(adjacency)
        )

        scores.append(
            structural_entropy
        )

        print(
            f"  structural entropy: "
            f"{structural_entropy:.10f}"
        )

        rows.append(
            {
                "repeat": repeat,
                "structural_entropy":
                    structural_entropy,
                "n_nodes":
                    int(n),
                "n_clusters":
                    int(len(set(cluster_ids))),
                "n_edges":
                    int(
                        np.sum(
                            np.triu(
                                adjacency,
                                k=1,
                            ) > 0
                        )
                    ),
                "total_edge_weight":
                    float(
                        np.triu(
                            adjacency,
                            k=1,
                        ).sum()
                    ),
            }
        )

    # -------------------------------------------------------------
    # Summary statistics
    # -------------------------------------------------------------

    scores_np = np.asarray(
        scores,
        dtype=float,
    )

    mean_score = float(
        np.mean(scores_np)
    )

    std_score = float(
        np.std(
            scores_np,
            ddof=1,
        )
    )

    min_score = float(
        np.min(scores_np)
    )

    max_score = float(
        np.max(scores_np)
    )

    score_range = (
        max_score - min_score
    )

    if mean_score != 0:

        coefficient_variation = (
            std_score
            / abs(mean_score)
        )

    else:

        coefficient_variation = float(
            "nan"
        )

    # -------------------------------------------------------------
    # Bootstrap 95% CI for the mean.
    #
    # Fixed RNG makes the analysis reproducible.
    # -------------------------------------------------------------

    rng = np.random.default_rng(
        2026
    )

    bootstrap_means = []

    for _ in range(10_000):

        sample = rng.choice(
            scores_np,
            size=len(scores_np),
            replace=True,
        )

        bootstrap_means.append(
            np.mean(sample)
        )

    bootstrap_means = np.asarray(
        bootstrap_means
    )

    ci_low, ci_high = np.percentile(
        bootstrap_means,
        [2.5, 97.5],
    )

    # -------------------------------------------------------------
    # Print summary.
    # -------------------------------------------------------------

    print()
    print("=" * 55)
    print("CLEAN STABILITY SUMMARY")
    print("=" * 55)

    print(
        f"Mean score:              "
        f"{mean_score:.10f}"
    )

    print(
        f"Standard deviation:      "
        f"{std_score:.10f}"
    )

    print(
        f"Minimum score:           "
        f"{min_score:.10f}"
    )

    print(
        f"Maximum score:           "
        f"{max_score:.10f}"
    )

    print(
        f"Score range:             "
        f"{score_range:.10f}"
    )

    print(
        f"Coefficient variation:   "
        f"{coefficient_variation:.10f}"
    )

    print(
        f"Bootstrap 95% CI:        "
        f"[{ci_low:.10f}, {ci_high:.10f}]"
    )

    print()

    # -------------------------------------------------------------
    # Save repetition-level results.
    # -------------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "repeat",
                "structural_entropy",
                "n_nodes",
                "n_clusters",
                "n_edges",
                "total_edge_weight",
            ],
        )

        writer.writeheader()

        writer.writerows(rows)

    # -------------------------------------------------------------
    # Save summary.
    # -------------------------------------------------------------

    summary_file = (
        OUTPUT_DIR
        / "score_stability_clean_summary.txt"
    )

    with open(
        summary_file,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "SeSE Clean Score Stability Experiment\n"
        )

        f.write(
            "Original work: UNMODIFIED\n\n"
        )

        f.write(
            f"Repeats: {N_REPEATS}\n"
        )

        f.write(
            f"Similarity threshold: "
            f"{similarity_threshold}\n"
        )

        f.write(
            f"Mean score: "
            f"{mean_score:.10f}\n"
        )

        f.write(
            f"Standard deviation: "
            f"{std_score:.10f}\n"
        )

        f.write(
            f"Minimum score: "
            f"{min_score:.10f}\n"
        )

        f.write(
            f"Maximum score: "
            f"{max_score:.10f}\n"
        )

        f.write(
            f"Range: "
            f"{score_range:.10f}\n"
        )

        f.write(
            f"Coefficient variation: "
            f"{coefficient_variation:.10f}\n"
        )

        f.write(
            f"Bootstrap 95% CI: "
            f"[{ci_low:.10f}, "
            f"{ci_high:.10f}]\n"
        )

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        summary_file
    )


if __name__ == "__main__":
    # Windows-safe entry point.
    import multiprocessing

    multiprocessing.freeze_support()

    main()