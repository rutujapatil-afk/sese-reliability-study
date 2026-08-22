"""
Experiment 3: Semantic/reasoning complexity sensitivity.

This experiment does NOT modify original_work/.

We construct controlled response sets with increasing semantic
complexity and measure how SeSE structural entropy changes.

Complexity levels:
    1. simple factual
    2. explanatory
    3. multi-claim
    4. reasoning-heavy
    5. contradiction/fabrication
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SESE = PROJECT_ROOT.parent / "original_work" / "SeSE"

sys.path.insert(0, str(ORIGINAL_SESE))

# ---------------------------------------------------------------------
# IMPORTANT:
# Keep ALL original_work imports inside main() so Windows multiprocessing
# does not recursively import the model in child processes.
# ---------------------------------------------------------------------


QUESTION = "Who discovered penicillin?"

RESPONSE_LEVELS = {
    "simple_factual": [
        "Alexander Fleming discovered penicillin.",
        "Penicillin was discovered by Alexander Fleming.",
        "Fleming discovered penicillin in 1928.",
        "Alexander Fleming is credited with discovering penicillin.",
        "Marie Curie discovered penicillin.",
        "Penicillin was discovered by Marie Curie.",
    ],

    "explanatory": [
        "Alexander Fleming discovered penicillin after observing its "
        "antibacterial effect in 1928.",
        "Penicillin is generally credited to Alexander Fleming, who "
        "noticed that a mold inhibited bacterial growth.",
        "Fleming discovered penicillin in 1928 after observing that "
        "mold contamination prevented bacteria from growing.",
        "The discovery of penicillin is associated with Alexander Fleming "
        "and his observation of antibacterial activity from mold.",
        "Marie Curie discovered penicillin after studying antibacterial "
        "mold during the early twentieth century.",
        "Penicillin was discovered by Marie Curie while investigating "
        "the medical effects of microorganisms.",
    ],

    "multi_claim": [
        "Alexander Fleming discovered penicillin in 1928, after noticing "
        "that mold inhibited bacterial growth, and his observation later "
        "contributed to antibiotic medicine.",
        "Fleming discovered penicillin in 1928. The substance came from "
        "a mold and showed antibacterial properties.",
        "Alexander Fleming is credited with discovering penicillin. "
        "He observed bacterial inhibition around a mold colony and "
        "recognized its medical significance.",
        "The discovery occurred in 1928 when Fleming noticed that mold "
        "prevented bacterial growth. The observation became important "
        "for the development of antibiotics.",
        "Marie Curie discovered penicillin in 1928 and demonstrated "
        "that it could treat bacterial infections.",
        "Marie Curie identified penicillin while studying radioactive "
        "materials and subsequently developed it as an antibiotic.",
    ],

    "reasoning_heavy": [
        "If discovery is defined as the first observation of the "
        "antibacterial substance, then Alexander Fleming should receive "
        "credit because his 1928 observation identified mold-related "
        "bacterial inhibition. Later researchers developed the substance "
        "into a practical treatment, but that does not change the "
        "historical attribution of the discovery.",
        "Alexander Fleming is the most appropriate answer because the "
        "question asks who discovered penicillin rather than who later "
        "developed it for widespread medical use. Fleming observed the "
        "antibacterial effect in 1928, whereas subsequent scientists "
        "helped turn the discovery into a usable drug.",
        "The answer should be Alexander Fleming. The key evidence is the "
        "1928 observation that mold inhibited bacterial growth. Although "
        "other researchers played important roles in purification and "
        "development, those contributions are distinct from the original "
        "discovery.",
        "One could mistakenly attribute penicillin to later developers, "
        "but that would confuse discovery with development. Fleming's "
        "observation establishes the conventional attribution of the "
        "discovery.",
        "Marie Curie discovered penicillin because she studied scientific "
        "phenomena and therefore could reasonably have identified the "
        "antibacterial substance before Fleming. This reasoning makes "
        "Curie the most likely discoverer.",
        "Because Marie Curie was a famous scientist, and because penicillin "
        "was an important scientific discovery, it follows that Curie "
        "probably discovered penicillin. Fleming's role may have been "
        "limited to later development.",
    ],

    "contradictory_fabricated": [
        "Alexander Fleming discovered penicillin in 1928, but Marie Curie "
        "also discovered the same antibiotic independently in 1910. "
        "Both scientists therefore deserve equal credit.",
        "Fleming discovered penicillin in 1928, although some evidence "
        "suggests that Marie Curie had already discovered it decades "
        "earlier. The historical record is therefore contradictory.",
        "Marie Curie discovered penicillin before Fleming, but Fleming "
        "also discovered it in 1928. Both claims can be treated as "
        "equally correct.",
        "Penicillin was discovered by Fleming in 1928 and by Marie Curie "
        "in the early twentieth century. The two discoveries were "
        "independent.",
        "Alexander Fleming discovered penicillin, but the discovery "
        "actually occurred during Marie Curie's research into radioactive "
        "materials.",
        "Marie Curie discovered penicillin in the early twentieth century, "
        "and Fleming later rediscovered the same substance.",
    ],
}


def compute_graph(
    responses,
    question,
    threshold,
):
    from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (
        compute_entailment_scores,
        compute_sentence_transformer_similirities,
        enhancing_answers,
        make_connected,
    )

    enhanced = enhancing_answers(responses, question)

    print("    Computing sentence similarities...")
    cos_sim = compute_sentence_transformer_similirities(enhanced)

    print("    Computing NLI similarities...")
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
            distance_threshold=1.0 - threshold,
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
        print(
            f"    Computing entailment for "
            f"{len(pairs)} intra-cluster edges..."
        )

        edge_scores = compute_entailment_scores(enhanced)

        for i, j in pairs:
            adjacency[i, j] = edge_scores[i, j]
            adjacency[j, i] = edge_scores[j, i]

    adjacency = np.asarray(
        make_connected(adjacency, enhanced),
        dtype=np.float32,
    )

    return adjacency, cluster_ids


def graph_summary(adjacency, cluster_ids):
    edge_mask = np.triu(
        np.ones_like(adjacency, dtype=bool),
        k=1,
    )

    values = adjacency[edge_mask]
    positive = values > 0

    n_nodes = adjacency.shape[0]
    possible_edges = n_nodes * (n_nodes - 1) / 2

    n_edges = int(np.sum(positive))

    return {
        "n_nodes": n_nodes,
        "n_clusters": len(set(cluster_ids)),
        "n_edges": n_edges,
        "edge_density": (
            n_edges / possible_edges
            if possible_edges > 0
            else 0.0
        ),
        "mean_edge_weight": (
            float(values[positive].mean())
            if np.any(positive)
            else 0.0
        ),
        "total_edge_weight": float(values.sum()),
    }


def main():
    from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
        compute_se,
    )

    threshold = 0.30

    print()
    print("SEMANTIC / REASONING COMPLEXITY STUDY")
    print("=" * 60)
    print("Original work: UNMODIFIED")
    print(f"Clustering threshold: {threshold:.2f}")
    print()

    results = []

    for level, responses in RESPONSE_LEVELS.items():

        print("-" * 60)
        print(f"Complexity level: {level}")
        print("-" * 60)

        adjacency, cluster_ids = compute_graph(
            responses,
            QUESTION,
            threshold,
        )

        entropy = float(compute_se(adjacency))

        summary = graph_summary(
            adjacency,
            cluster_ids,
        )

        print(
            f"    clusters: {summary['n_clusters']}"
        )

        print(
            f"    edges: {summary['n_edges']}"
        )

        print(
            f"    density: {summary['edge_density']:.4f}"
        )

        print(
            f"    mean edge weight: "
            f"{summary['mean_edge_weight']:.4f}"
        )

        print(
            f"    total edge weight: "
            f"{summary['total_edge_weight']:.4f}"
        )

        print(
            f"    structural entropy: "
            f"{entropy:.8f}"
        )

        results.append(
            {
                "complexity_level": level,
                "structural_entropy": entropy,
                **summary,
            }
        )

        print()

    # -------------------------------------------------------------
    # Save CSV
    # -------------------------------------------------------------

    import csv

    output_dir = PROJECT_ROOT / "results" / "complexity_study"
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / "complexity_results.csv"

    fieldnames = list(results[0].keys())

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print("=" * 60)
    print("RESULTS SAVED")
    print("=" * 60)
    print(output_file)


if __name__ == "__main__":
    main()