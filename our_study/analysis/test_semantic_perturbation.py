import sys
from pathlib import Path

import numpy as np

# Allow imports from our_study/src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.semantic_perturbation import (
    add_edge_weight_noise,
    randomly_dropout_edges,
    relative_frobenius_change,
)


def main():
    matrix = np.array(
        [
            [1.0, 0.8, 0.2],
            [0.8, 1.0, 0.6],
            [0.2, 0.6, 1.0],
        ]
    )

    noisy = add_edge_weight_noise(
        matrix,
        noise_level=0.05,
        seed=42,
    )

    dropped = randomly_dropout_edges(
        matrix,
        dropout_rate=0.10,
        seed=42,
    )

    print("Original:")
    print(matrix)

    print("\nNoisy:")
    print(noisy)

    print("\nDropped:")
    print(dropped)

    print(
        "\nRelative change - noise:",
        relative_frobenius_change(matrix, noisy),
    )

    print(
        "Relative change - dropout:",
        relative_frobenius_change(matrix, dropped),
    )


if __name__ == "__main__":
    main()