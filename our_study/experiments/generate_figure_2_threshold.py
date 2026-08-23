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
    / "threshold_sensitivity_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "our_study"
    / "results"
    / "figures"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PNG = OUTPUT_DIR / "figure_2_threshold_sensitivity.png"
OUTPUT_PDF = OUTPUT_DIR / "figure_2_threshold_sensitivity.pdf"


# ---------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Threshold-sensitivity CSV not found:\n{INPUT_CSV}"
    )

df = pd.read_csv(INPUT_CSV)

required_columns = {
    "threshold",
    "structural_entropy",
}

missing = required_columns - set(df.columns)

if missing:
    raise ValueError(
        f"CSV is missing required columns: {sorted(missing)}\n"
        f"Available columns: {list(df.columns)}"
    )


# ---------------------------------------------------------------------
# Prepare data
# ---------------------------------------------------------------------

plot_df = df[["threshold", "structural_entropy"]].copy()

plot_df["threshold"] = pd.to_numeric(
    plot_df["threshold"],
    errors="coerce",
)

plot_df["structural_entropy"] = pd.to_numeric(
    plot_df["structural_entropy"],
    errors="coerce",
)

plot_df = (
    plot_df
    .dropna()
    .sort_values("threshold")
    .drop_duplicates(subset=["threshold"])
    .reset_index(drop=True)
)

if len(plot_df) < 2:
    raise ValueError(
        "At least two valid threshold/structural_entropy observations "
        "are required."
    )


# ---------------------------------------------------------------------
# Quantitative verification
# ---------------------------------------------------------------------

entropy_range = (
    plot_df["structural_entropy"].max()
    - plot_df["structural_entropy"].min()
)

print("=" * 70)
print("FIGURE 2 — THRESHOLD SENSITIVITY")
print("=" * 70)

print(f"Input CSV: {INPUT_CSV}")
print(f"Observations: {len(plot_df)}")
print(f"Entropy range: {entropy_range:.6f}")
print()
print(plot_df.to_string(index=False))
print()


# ---------------------------------------------------------------------
# Create figure
# ---------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(7.2, 4.6))

ax.plot(
    plot_df["threshold"],
    plot_df["structural_entropy"],
    marker="o",
    linewidth=2.0,
    markersize=6,
)

ax.set_xlabel(
    "Clustering threshold",
    fontsize=11,
)

ax.set_ylabel(
    "Structural entropy",
    fontsize=11,
)

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

fig.tight_layout()


# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------

fig.savefig(
    OUTPUT_PNG,
    dpi=600,
    bbox_inches="tight",
)

fig.savefig(
    OUTPUT_PDF,
    bbox_inches="tight",
)

plt.close(fig)


# ---------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------

print(f"[OK] PNG saved: {OUTPUT_PNG}")
print(f"[OK] PDF saved: {OUTPUT_PDF}")
print()
print("Figure 2 generation complete.")
print("=" * 70)