"""
Experiment 1: SeSE clustering-threshold sensitivity.

This experiment investigates how the semantic clustering threshold
affects the resulting structural-entropy uncertainty estimate.

The original SeSE implementation is treated as reference material.
This script does not modify original_work/.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

THRESHOLDS = [
    0.20,
    0.25,
    0.30,  # Original SeSE default
    0.35,
    0.40,
]


def main():
    print("SeSE clustering-threshold sensitivity study")
    print()
    print("Thresholds:")
    
    for threshold in THRESHOLDS:
        marker = " <- original default" if threshold == 0.30 else ""
        print(f"  {threshold:.2f}{marker}")


if __name__ == "__main__":
    main()