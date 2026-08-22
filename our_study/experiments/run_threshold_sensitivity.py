"""
Experiment 1: Clustering-threshold sensitivity.

IMPORTANT:
This experiment does NOT modify original_work/.

It reproduces the relevant SeSE semantic-graph construction using
the locally downloaded NLI and sentence-embedding models.

The OpenAI enhancement step from the original implementation is
intentionally omitted for this controlled threshold experiment.

Results are saved to:
    our_study/results/threshold_sensitivity_results.csv
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from transformers import AutoModelForSequenceClassification, AutoTokenizer


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

NLI_MODEL_NAME = "microsoft/deberta-v2-xlarge-mnli"

SENTENCE_EMB_MODEL_NAME = (
    "tomaarsen/static-similarity-mrl-multilingual-v1"
)

THRESHOLDS = [0.20, 0.25, 0.30, 0.35, 0.40]

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
OUTPUT_PATH = RESULTS_DIR / "threshold_sensitivity_results.csv"


# ---------------------------------------------------------------------
# Model state
# ---------------------------------------------------------------------

# IMPORTANT:
# Models are intentionally NOT loaded at module import time.
#
# Windows uses multiprocessing "spawn". Loading a large model during
# module import can cause recursive initialization / bootstrapping
# errors in child processes.

entailment_model = None
entailment_tokenizer = None
sentence_embedding_model = None


def load_models() -> None:
    """Load the local models once, from the main process only."""

    global entailment_model
    global entailment_tokenizer
    global sentence_embedding_model

    if (
        entailment_model is not None
        and entailment_tokenizer is not None
        and sentence_embedding_model is not None
    ):
        return

    print("Loading NLI model...", flush=True)

    entailment_model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            NLI_MODEL_NAME,
            local_files_only=True,
        )
        .to(DEVICE)
        .eval()
    )

    entailment_tokenizer = AutoTokenizer.from_pretrained(
        NLI_MODEL_NAME,
        use_fast=False,
        local_files_only=True,
    )

    print("NLI model loaded.", flush=True)

    print("Loading sentence-embedding model...", flush=True)

    sentence_embedding_model = SentenceTransformer(
        SENTENCE_EMB_MODEL_NAME,
        device=str(DEVICE),
    )

    print("Sentence-embedding model loaded.", flush=True)
    print(flush=True)


# ---------------------------------------------------------------------
# NLI
# ---------------------------------------------------------------------

def run_textual_entailment(
    pairs: list[tuple[str, str]],
    batch_size: int = 16,
) -> list[list[float]]:
    """
    Return probabilities in the order:

        [entailment, neutral, contradiction]
    """

    load_models()

    results = []

    for start in range(0, len(pairs), batch_size):

        batch = pairs[start:start + batch_size]

        inputs = entailment_tokenizer(
            [p[0] for p in batch],
            [p[1] for p in batch],
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            logits = entailment_model(**inputs).logits

        probs = torch.softmax(
            logits,
            dim=1,
        ).cpu().tolist()

        # DeBERTa MNLI label order:
        # contradiction, neutral, entailment
        for p in probs:
            results.append(
                [
                    p[2],
                    p[1],
                    p[0],
                ]
            )

    return results


_entailment_cache: dict[
    tuple[str, ...],
    np.ndarray,
] = {}


def compute_entailment_scores(
    strings_list: list[str],
) -> np.ndarray:
    """
    Compute symmetric pairwise entailment matrix.

    Results are cached so repeated threshold calculations do not
    repeatedly run the NLI model.
    """

    key = tuple(strings_list)

    cached = _entailment_cache.get(key)

    if cached is not None:
        return cached.copy()

    n = len(strings_list)

    scores = np.zeros(
        (n, n),
        dtype=np.float32,
    )

    pairs = list(
        itertools.combinations(
            range(n),
            2,
        )
    )

    if not pairs:
        return scores

    sent_pairs = [
        (
            strings_list[i],
            strings_list[j],
        )
        for i, j in pairs
    ]

    probabilities = run_textual_entailment(
        sent_pairs
    )

    for (i, j), prob in zip(
        pairs,
        probabilities,
    ):
        scores[i, j] = prob[0]
        scores[j, i] = prob[0]

    _entailment_cache[key] = scores.copy()

    return scores


# ---------------------------------------------------------------------
# Sentence embeddings
# ---------------------------------------------------------------------

def compute_sentence_transformer_similirities(
    strings_list: list[str],
) -> np.ndarray:
    """Compute cosine similarity matrix."""

    load_models()

    embeddings = sentence_embedding_model.encode(
        strings_list,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings @ embeddings.T


# ---------------------------------------------------------------------
# Connectivity
# ---------------------------------------------------------------------

def is_connected(
    adjacency_matrix: np.ndarray,
) -> tuple[bool, list[list[int]]]:

    n = adjacency_matrix.shape[0]

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):

        ra = find(a)
        rb = find(b)

        if ra != rb:
            parent[rb] = ra

    for i, j in np.argwhere(
        adjacency_matrix > 0
    ):
        union(
            int(i),
            int(j),
        )

    components = {}

    for i in range(n):

        root = find(i)

        components.setdefault(
            root,
            [],
        ).append(i)

    component_list = list(
        components.values()
    )

    return (
        len(component_list) == 1,
        component_list,
    )


def make_connected(
    adjacency_matrix: np.ndarray,
    responses: list[str],
) -> np.ndarray:
    """
    Connect disconnected components using representative
    entailment edges.

    This mirrors the relevant behavior of the original SeSE code.
    """

    connected, components = is_connected(
        adjacency_matrix
    )

    if connected:
        return adjacency_matrix

    representatives = []

    for component in components:

        representatives.append(
            component[0]
        )

    representative_pairs = list(
        itertools.combinations(
            representatives,
            2,
        )
    )

    if not representative_pairs:
        return adjacency_matrix

    entail_pairs = [
        (
            responses[i],
            responses[j],
        )
        for i, j in representative_pairs
    ]

    weights = run_textual_entailment(
        entail_pairs
    )

    edges = sorted(
        zip(
            representative_pairs,
            weights,
        ),
        key=lambda x: x[1][0],
        reverse=True,
    )

    parent = list(
        range(
            adjacency_matrix.shape[0]
        )
    )

    def find(x):

        while parent[x] != x:

            parent[x] = parent[
                parent[x]
            ]

            x = parent[x]

        return x

    def union(a, b):

        ra = find(a)
        rb = find(b)

        if ra == rb:
            return False

        parent[rb] = ra

        return True

    for (u, v), weight in edges:

        if union(u, v):

            adjacency_matrix[
                u,
                v,
            ] = weight[0]

            adjacency_matrix[
                v,
                u,
            ] = weight[0]

    return adjacency_matrix


# ---------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------

def build_graph_with_threshold(
    responses: list[str],
    question: str,
    similarity_threshold: float,
) -> tuple[
    np.ndarray,
    list[int],
    list[str],
]:
    """
    Build the semantic graph while varying only the
    clustering similarity threshold.

    The supplied responses are used directly.
    """

    # No OpenAI enhancement here.
    enhanced = list(responses)

    print(
        "  Computing sentence similarities..."
    )

    cos_sim = (
        compute_sentence_transformer_similirities(
            enhanced
        )
    )

    print(
        "  Computing NLI similarities..."
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

    non_diag = distance[
        ~np.eye(
            len(distance),
            dtype=bool,
        )
    ]

    if np.all(
        non_diag == 0.0
    ):

        cluster_ids = [
            0
        ] * len(enhanced)

    elif np.all(
        non_diag == 1.0
    ):

        cluster_ids = list(
            range(
                len(enhanced)
            )
        )

    else:

        clusterer = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=(
                1.0
                - similarity_threshold
            ),
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
            "  Using entailment scores for "
            f"{len(pairs)} intra-cluster edges..."
        )

        # Already cached from above.
        edge_scores = (
            compute_entailment_scores(
                enhanced
            )
        )

        for i, j in pairs:

            adjacency[
                i,
                j,
            ] = edge_scores[i, j]

            adjacency[
                j,
                i,
            ] = edge_scores[j, i]

    adjacency = make_connected(
        adjacency,
        enhanced,
    )

    return (
        adjacency.astype(
            np.float32
        ),
        cluster_ids,
        enhanced,
    )


# ---------------------------------------------------------------------
# Structural entropy
# ---------------------------------------------------------------------

def compute_structural_entropy(
    adjacency: np.ndarray,
) -> float:
    """
    Compute structural entropy using the SeSE structural entropy
    definition used by the original implementation.
    """

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    original_sese = (
        project_root.parent
        / "original_work"
        / "SeSE"
    )

    original_sese_str = str(
        original_sese
    )

    if original_sese_str not in sys.path:
        sys.path.insert(
            0,
            original_sese_str,
        )

    from sentence_structural_entropy.src.uncertainty_measures.structural_entropy import (
        compute_se,
    )

    return float(
        compute_se(adjacency)
    )


# ---------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------

def summarize_graph(
    adjacency: np.ndarray,
    cluster_ids: list[int],
) -> dict:

    edge_mask = np.triu(
        np.ones_like(
            adjacency,
            dtype=bool,
        ),
        k=1,
    )

    edge_values = adjacency[
        edge_mask
    ]

    positive_edges = (
        edge_values > 0
    )

    n_nodes = adjacency.shape[0]

    possible_edges = (
        n_nodes * (n_nodes - 1) // 2
    )

    n_edges = int(
        np.sum(positive_edges)
    )

    density = (
        n_edges / possible_edges
        if possible_edges > 0
        else 0.0
    )

    return {
        "n_nodes": n_nodes,

        "n_clusters": len(
            set(cluster_ids)
        ),

        "n_edges": n_edges,

        "edge_density": float(
            density
        ),

        "mean_edge_weight": (
            float(
                edge_values[
                    positive_edges
                ].mean()
            )
            if np.any(
                positive_edges
            )
            else 0.0
        ),

        "total_edge_weight": float(
            edge_values.sum()
        ),
    }


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

def main():

    # Windows-safe model initialization.
    load_models()

    question = (
        "Who discovered penicillin?"
    )

    responses = [
        "Alexander Fleming discovered penicillin in 1928.",
        "Penicillin was discovered by Alexander Fleming.",
        "Fleming discovered penicillin in 1928.",
        "Alexander Fleming is credited with discovering penicillin.",
        "Penicillin was discovered by Marie Curie.",
        "Marie Curie discovered penicillin in the early twentieth century.",
    ]

    print()
    print(
        "SeSE threshold sensitivity experiment"
    )
    print("=" * 50)
    print(
        "Original work: UNMODIFIED"
    )
    print()

    records = []

    for threshold in THRESHOLDS:

        print(
            f"Threshold: {threshold:.2f}"
        )

        adjacency, cluster_ids, enhanced = (
            build_graph_with_threshold(
                responses,
                question,
                threshold,
            )
        )

        structural_entropy = (
            compute_structural_entropy(
                adjacency
            )
        )

        summary = summarize_graph(
            adjacency,
            cluster_ids,
        )

        print(
            f"  clusters: "
            f"{summary['n_clusters']}"
        )

        print(
            f"  edges: "
            f"{summary['n_edges']}"
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

        # -------------------------------------------------------------
        # SAVE RECORD
        # -------------------------------------------------------------

        records.append(
            {
                "threshold": float(
                    threshold
                ),
                "question": question,
                "n_nodes": summary[
                    "n_nodes"
                ],
                "n_clusters": summary[
                    "n_clusters"
                ],
                "n_edges": summary[
                    "n_edges"
                ],
                "edge_density": summary[
                    "edge_density"
                ],
                "mean_edge_weight": summary[
                    "mean_edge_weight"
                ],
                "total_edge_weight": summary[
                    "total_edge_weight"
                ],
                "structural_entropy": float(
                    structural_entropy
                ),
                "cluster_ids": ",".join(
                    str(x)
                    for x in cluster_ids
                ),
            }
        )

        print()

    # -----------------------------------------------------------------
    # Save threshold-sensitivity results
    # -----------------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df = pd.DataFrame(
        records
    )

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("=" * 50)
    print("RESULTS SAVED")
    print("=" * 50)
    print(
        OUTPUT_PATH
    )
    print()
    print(
        f"Rows saved: {len(results_df)}"
    )
    print()
    print(
        results_df[
            [
                "threshold",
                "n_clusters",
                "n_edges",
                "edge_density",
                "mean_edge_weight",
                "total_edge_weight",
                "structural_entropy",
            ]
        ].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()