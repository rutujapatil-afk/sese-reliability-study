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
    / "semantic_perturbation"
    / "perturbation_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "our_study"
    / "results"
    / "figures"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PNG = OUTPUT_DIR / "figure_3_semantic_perturbation.png"


# ---------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Perturbation results CSV not found:\n{INPUT_CSV}"
    )

df = pd.read_csv(INPUT_CSV)

required_columns = {
    "perturbation",
    "level",
    "seed",
    "relative_graph_change",
    "relative_entropy_change",
}

missing = required_columns - set(df.columns)

if missing:
    raise ValueError(
        f"CSV is missing required columns: {sorted(missing)}\n"
        f"Available columns: {list(df.columns)}"
    )


# ---------------------------------------------------------------------
# Clean numeric columns
# ---------------------------------------------------------------------

for column in [
    "level",
    "seed",
    "relative_graph_change",
    "relative_entropy_change",
]:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )

df = df.dropna(
    subset=[
        "perturbation",
        "level",
        "relative_graph_change",
        "relative_entropy_change",
    ]
).copy()


# ---------------------------------------------------------------------
# Normalize perturbation labels
# ---------------------------------------------------------------------

def normalize_perturbation(value):
    value = str(value).strip().lower()

    if "noise" in value:
        return "Edge-weight noise"

    if "dropout" in value:
        return "Edge dropout"

    return str(value)


df["perturbation_label"] = df["perturbation"].apply(
    normalize_perturbation
)


# ---------------------------------------------------------------------
# Aggregate repeated seeds
#
# The figure uses the mean across seeds at each perturbation level.
# No new experimental data are generated.
# ---------------------------------------------------------------------

summary = (
    df.groupby(
        ["perturbation_label", "level"],
        as_index=False,
    )
    .agg(
        mean_relative_entropy_change=(
            "relative_entropy_change",
            "mean",
        ),
        std_relative_entropy_change=(
            "relative_entropy_change",
            "std",
        ),
        mean_relative_graph_change=(
            "relative_graph_change",
            "mean",
        ),
        std_relative_graph_change=(
            "relative_graph_change",
            "std",
        ),
        n_observations=(
            "relative_entropy_change",
            "count",
        ),
    )
    .sort_values(
        ["perturbation_label", "level"]
    )
)


# ---------------------------------------------------------------------
# Quantitative verification
# ---------------------------------------------------------------------

noise_entropy_max = df.loc[
    df["perturbation_label"] == "Edge-weight noise",
    "relative_entropy_change",
].max()

dropout_entropy_max = df.loc[
    df["perturbation_label"] == "Edge dropout",
    "relative_entropy_change",
].max()

noise_graph_max = df.loc[
    df["perturbation_label"] == "Edge-weight noise",
    "relative_graph_change",
].max()

dropout_graph_max = df.loc[
    df["perturbation_label"] == "Edge dropout",
    "relative_graph_change",
].max()


print("=" * 70)
print("FIGURE 3 — SEMANTIC-GRAPH PERTURBATION")
print("=" * 70)

print(f"Input CSV: {INPUT_CSV}")
print(f"Rows used: {len(df)}")
print()

print("Aggregated plotting data:")
print(summary.to_string(index=False))
print()

print(
    f"Noise maximum relative entropy change: "
    f"{noise_entropy_max:.6f}"
)

print(
    f"Dropout maximum relative entropy change: "
    f"{dropout_entropy_max:.6f}"
)

print(
    f"Noise maximum relative graph change: "
    f"{noise_graph_max:.6f}"
)

print(
    f"Dropout maximum relative graph change: "
    f"{dropout_graph_max:.6f}"
)

if pd.notna(noise_entropy_max) and pd.notna(dropout_entropy_max):
    print(
        f"Noise/dropout entropy ratio: "
        f"{noise_entropy_max / dropout_entropy_max:.4f}"
    )

print()


# ---------------------------------------------------------------------
# Create publication figure
# ---------------------------------------------------------------------

fig, axes = plt.subplots(
    2,
    1,
    figsize=(7.2, 7.4),
    sharex=True,
)


# ---------------------------------------------------------------------
# Panel A — Relative entropy change
# ---------------------------------------------------------------------

ax = axes[0]

for perturbation in [
    "Edge-weight noise",
    "Edge dropout",
]:

    subset = summary[
        summary["perturbation_label"] == perturbation
    ].sort_values("level")

    if subset.empty:
        continue

    ax.plot(
        subset["level"],
        subset["mean_relative_entropy_change"],
        marker="o",
        linewidth=2.0,
        markersize=6,
        label=perturbation,
    )

    # Show standard deviation only where repeated observations exist.
    if (subset["n_observations"] > 1).any():

        std_values = (
            subset["std_relative_entropy_change"]
            .fillna(0)
        )

        ax.errorbar(
            subset["level"],
            subset["mean_relative_entropy_change"],
            yerr=std_values,
            fmt="none",
            capsize=3,
            alpha=0.7,
        )

ax.set_ylabel(
    "Relative entropy change",
    fontsize=11,
)

ax.set_title(
    "(A) Structural-entropy response",
    fontsize=11,
    loc="left",
)

ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.35,
)

ax.legend(
    frameon=False,
    fontsize=9,
)


# ---------------------------------------------------------------------
# Panel B — Relative graph change
# ---------------------------------------------------------------------

ax = axes[1]

for perturbation in [
    "Edge-weight noise",
    "Edge dropout",
]:

    subset = summary[
        summary["perturbation_label"] == perturbation
    ].sort_values("level")

    if subset.empty:
        continue

    ax.plot(
        subset["level"],
        subset["mean_relative_graph_change"],
        marker="o",
        linewidth=2.0,
        markersize=6,
        label=perturbation,
    )

    if (subset["n_observations"] > 1).any():

        std_values = (
            subset["std_relative_graph_change"]
            .fillna(0)
        )

        ax.errorbar(
            subset["level"],
            subset["mean_relative_graph_change"],
            yerr=std_values,
            fmt="none",
            capsize=3,
            alpha=0.7,
        )

ax.set_xlabel(
    "Perturbation level",
    fontsize=11,
)

ax.set_ylabel(
    "Relative graph change",
    fontsize=11,
)

ax.set_title(
    "(B) Structural-graph response",
    fontsize=11,
    loc="left",
)

ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.35,
)

ax.legend(
    frameon=False,
    fontsize=9,
)


# ---------------------------------------------------------------------
# Clean manuscript styling
# ---------------------------------------------------------------------

for ax in axes:

    ax.tick_params(
        axis="both",
        labelsize=10,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


fig.tight_layout(
    h_pad=2.0
)


# ---------------------------------------------------------------------
# Save PNG
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

print(f"[OK] PNG saved:")
print(OUTPUT_PNG)
print()
print("Figure 3 generation complete.")
print("=" * 70)