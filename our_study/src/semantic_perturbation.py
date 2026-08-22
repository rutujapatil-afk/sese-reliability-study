"""
Controlled perturbations for semantic graphs used in the SeSE robustness study.

This module does not modify the original SeSE implementation.
It provides independent transformations that can be applied to a
semantic adjacency/similarity matrix before uncertainty calculation.
"""

from __future__ import annotations

import numpy as np


def validate_similarity_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Validate and return a floating-point copy of a similarity matrix.
    """
    matrix = np.asarray(matrix, dtype=float)

    if matrix.ndim != 2:
        raise ValueError("Similarity matrix must be two-dimensional.")

    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Similarity matrix must be square.")

    if not np.all(np.isfinite(matrix)):
        raise ValueError("Similarity matrix contains non-finite values.")

    return matrix.copy()


def add_edge_weight_noise(
    matrix: np.ndarray,
    noise_level: float,
    seed: int,
) -> np.ndarray:
    """
    Add bounded Gaussian perturbation to existing edge weights.

    Diagonal entries are preserved.
    Values are clipped to [0, 1].

    The original matrix is never modified.
    """
    if not 0.0 <= noise_level:
        raise ValueError("noise_level must be non-negative.")

    matrix = validate_similarity_matrix(matrix)

    rng = np.random.default_rng(seed)

    noise = rng.normal(
        loc=0.0,
        scale=noise_level,
        size=matrix.shape,
    )

    perturbed = matrix + noise

    # Preserve self-similarity.
    np.fill_diagonal(perturbed, np.diag(matrix))

    # Similarity values are bounded.
    perturbed = np.clip(perturbed, 0.0, 1.0)

    return perturbed


def randomly_dropout_edges(
    matrix: np.ndarray,
    dropout_rate: float,
    seed: int,
) -> np.ndarray:
    """
    Randomly remove existing off-diagonal edges.

    An edge is removed by setting its similarity to zero.

    The same seed produces the same perturbation, making experiments
    reproducible.
    """
    if not 0.0 <= dropout_rate <= 1.0:
        raise ValueError("dropout_rate must be between 0 and 1.")

    matrix = validate_similarity_matrix(matrix)

    rng = np.random.default_rng(seed)

    mask = rng.random(matrix.shape) < dropout_rate

    # Never modify the diagonal.
    np.fill_diagonal(mask, False)

    perturbed = matrix.copy()
    perturbed[mask] = 0.0

    return perturbed


def relative_frobenius_change(
    original: np.ndarray,
    perturbed: np.ndarray,
) -> float:
    """
    Measure the relative change between two matrices.

    This allows us to distinguish the magnitude of the perturbation
    from the resulting change in the SeSE uncertainty score.
    """
    original = validate_similarity_matrix(original)
    perturbed = validate_similarity_matrix(perturbed)

    denominator = np.linalg.norm(original, ord="fro")

    if denominator == 0:
        return float(np.linalg.norm(perturbed, ord="fro"))

    return float(
        np.linalg.norm(perturbed - original, ord="fro")
        / denominator
    )