from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_CSV = (
    PROJECT_ROOT
    / "our_study"
    / "results"
    / "score_stability"
    / "score_stability_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "our_study"
    / "results"
    / "figures"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PNG = (
    OUTPUT_DIR
    / "figure_4_repeated_score_stability.png"
)


# ---------------------------------------------------------------------
# Load existing results
# ---------------------------------------------------------------------

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Score-stability CSV not found:\n{INPUT_CSV}"
    )

df = pd.read_csv(INPUT_CSV)

required_columns = {
    "repeat",
    "structural_entropy",
}

missing = required_columns - set(df.columns)

if missing:
    raise ValueError(
        f"CSV is missing required columns: {sorted(missing)}\n"
        f"Available columns: {list(df.columns)}"
    )


# ---------------------------------------------------------------------
# Clean data
# ---------------------------------------------------------------------

df["repeat"] = pd.to_numeric(
    df["repeat"],
    errors="coerce",
)

df["structural_entropy"] = pd.to_numeric(
    df["structural_entropy"],
    errors="coerce",
)

df = (
    df[
        [
            "repeat",
            "structural_entropy",
        ]
    ]
    .dropna()
    .sort_values("repeat")
    .reset_index(drop=True)
)


if len(df) < 2:
    raise ValueError(
        "At least two valid repeated evaluations are required "
        "to generate Figure 4."
    )


# ---------------------------------------------------------------------
# Calculate descriptive statistics from existing observations
# ---------------------------------------------------------------------

entropy_mean = df["structural_entropy"].mean()
entropy_std = df["structural_entropy"].std()
entropy_min = df["structural_entropy"].min()
entropy_max = df["structural_entropy"].max()
entropy_range = entropy_max - entropy_min


print("=" * 70)
print("FIGURE 4 — REPEATED-SCORE STABILITY")
print("=" * 70)

print(f"Input CSV: {INPUT_CSV}")
print(f"Observations: {len(df)}")
print()

print("Recorded observations:")
print(df.to_string(index=False))
print()

print(f"Mean structural entropy: {entropy_mean:.6f}")
print(f"Standard deviation:      {entropy_std:.6f}")
print(f"Minimum:                 {entropy_min:.6f}")
print(f"Maximum:                 {entropy_max:.6f}")
print(f"Observed range:          {entropy_range:.6f}")
print()


# ---------------------------------------------------------------------
# Create publication figure
# ---------------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(7.2, 4.8)
)


# Individual recorded scores
ax.plot(
    df["repeat"],
    df["structural_entropy"],
    marker="o",
    linewidth=1.8,
    markersize=6,
)


# Mean reference line
ax.axhline(
    entropy_mean,
    linestyle="--",
    linewidth=1.0,
    alpha=0.7,
    label=f"Mean = {entropy_mean:.3f}",
)


# ---------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------

ax.set_xlabel(
    "Evaluation repeat",
    fontsize=11,
)

ax.set_ylabel(
    "Structural entropy",
    fontsize=11,
)

ax.set_title(
    "Repeated structural-entropy evaluations",
    fontsize=11,
)


# ---------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------

ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.35,
)

ax.tick_params(
    axis="both",
    labelsize=10,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(
    frameon=False,
    fontsize=9,
)


# ---------------------------------------------------------------------
# Integer repeat ticks
# ---------------------------------------------------------------------

ax.set_xticks(
    df["repeat"].astype(int)
)

fig.tight_layout()


# ---------------------------------------------------------------------
# Save high-resolution PNG
# ---------------------------------------------------------------------

fig.savefig(
    OUTPUT_PNG,
    dpi=600,
    bbox_inches="tight",
)

plt.close(fig)


# ---------------------------------------------------------------------
# Final output
# ---------------------------------------------------------------------

print("[OK] PNG saved:")
print(OUTPUT_PNG)
print()
print("Figure 4 generation complete.")
print("=" * 70)