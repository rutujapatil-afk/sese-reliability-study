from pathlib import Path
import ast

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
    / "scaled_evaluation"
    / "scaled_evaluation_results.csv"
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
    / "figure_5_case_level_cluster_error_structure.png"
)


# ---------------------------------------------------------------------
# Load existing scaled-evaluation results
# ---------------------------------------------------------------------

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Scaled evaluation CSV not found:\n{INPUT_CSV}"
    )

df = pd.read_csv(INPUT_CSV)


required_columns = {
    "case_id",
    "category",
    "cluster_sizes",
    "cluster_incorrect_counts",
    "incorrect_responses",
    "incorrect_fraction",
    "confident_failure",
}

missing = required_columns - set(df.columns)

if missing:
    raise ValueError(
        f"CSV is missing required columns: {sorted(missing)}\n"
        f"Available columns: {list(df.columns)}"
    )


# ---------------------------------------------------------------------
# Parse list-valued CSV fields
# ---------------------------------------------------------------------

def parse_list(value):
    """
    Convert a CSV string such as '[5, 1]' into a Python list.
    """
    if isinstance(value, list):
        return value

    return ast.literal_eval(str(value))


df["cluster_sizes_parsed"] = (
    df["cluster_sizes"]
    .apply(parse_list)
)

df["cluster_incorrect_counts_parsed"] = (
    df["cluster_incorrect_counts"]
    .apply(parse_list)
)


# ---------------------------------------------------------------------
# Validate expected scaled-evaluation structure
# ---------------------------------------------------------------------

if len(df) != 7:
    print(
        f"[WARNING] Expected 7 scaled-evaluation cases; "
        f"found {len(df)}."
    )


# ---------------------------------------------------------------------
# Print exact data being visualized
# ---------------------------------------------------------------------

print("=" * 70)
print("FIGURE 5 — CASE-LEVEL CLUSTER / ERROR STRUCTURE")
print("=" * 70)

print(f"Input CSV: {INPUT_CSV}")
print()

for _, row in df.iterrows():

    sizes = row["cluster_sizes_parsed"]
    incorrect = row["cluster_incorrect_counts_parsed"]

    print(
        f"{row['case_id']}: "
        f"category={row['category']}, "
        f"clusters={sizes}, "
        f"incorrect={row['incorrect_responses']}, "
        f"incorrect_fraction={row['incorrect_fraction']:.6f}, "
        f"confident_failure={row['confident_failure']}"
    )

print()


# ---------------------------------------------------------------------
# Create figure
# ---------------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(9.0, 6.2)
)


# ---------------------------------------------------------------------
# Plot each case as a horizontal cluster composition
#
# Each cluster is represented by a block.
#
# Normal responses = filled block.
# Incorrect responses = hatched block.
#
# Width corresponds directly to the number of responses in that cluster.
# ---------------------------------------------------------------------

for case_index, (_, row) in enumerate(df.iterrows()):

    cluster_sizes = row["cluster_sizes_parsed"]
    incorrect_counts = row["cluster_incorrect_counts_parsed"]

    x_position = 0.0

    total_responses = sum(cluster_sizes)

    for cluster_index, (
        cluster_size,
        incorrect_count,
    ) in enumerate(
        zip(
            cluster_sizes,
            incorrect_counts,
        )
    ):

        # Draw cluster block.
        ax.barh(
            case_index,
            cluster_size,
            left=x_position,
            height=0.58,
            edgecolor="black",
            linewidth=1.0,
            color="white",
        )

        # If the cluster contains an incorrect response,
        # overlay the incorrect portion.
        if incorrect_count > 0:

            ax.barh(
                case_index,
                incorrect_count,
                left=(
                    x_position
                    + cluster_size
                    - incorrect_count
                ),
                height=0.58,
                edgecolor="black",
                linewidth=1.0,
                color="white",
                hatch="///",
            )

        # Cluster label.
        ax.text(
            x_position + cluster_size / 2,
            case_index,
            str(cluster_size),
            ha="center",
            va="center",
            fontsize=10,
        )

        x_position += cluster_size


# ---------------------------------------------------------------------
# Y-axis labels
# ---------------------------------------------------------------------

labels = []

for _, row in df.iterrows():

    category = str(row["category"]).capitalize()

    labels.append(
        f"{row['case_id']} ({category})"
    )

ax.set_yticks(
    range(len(df))
)

ax.set_yticklabels(
    labels,
    fontsize=9,
)


# ---------------------------------------------------------------------
# Axis labels
# ---------------------------------------------------------------------

ax.set_xlabel(
    "Number of responses in semantic cluster(s)",
    fontsize=11,
)

ax.set_ylabel(
    "Scaled evaluation case",
    fontsize=11,
)


# ---------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------

ax.set_title(
    "Case-level cluster and error structure",
    fontsize=12,
)


# ---------------------------------------------------------------------
# X-axis
# ---------------------------------------------------------------------

ax.set_xlim(
    0,
    max(
        df["cluster_sizes_parsed"]
        .apply(sum)
    ) + 0.5,
)

ax.set_xticks(
    range(
        0,
        int(
            max(
                df["cluster_sizes_parsed"]
                .apply(sum)
            )
        ) + 1,
    )
)


# ---------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------

ax.grid(
    True,
    axis="x",
    linestyle="--",
    linewidth=0.6,
    alpha=0.35,
)

ax.set_axisbelow(True)


# ---------------------------------------------------------------------
# Clean styling
# ---------------------------------------------------------------------

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(
    axis="both",
    labelsize=9,
)


# ---------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------

from matplotlib.patches import Patch

legend_handles = [
    Patch(
        facecolor="white",
        edgecolor="black",
        label="Correct response(s)",
    ),
    Patch(
        facecolor="white",
        edgecolor="black",
        hatch="///",
        label="Incorrect response",
    ),
]

ax.legend(
    handles=legend_handles,
    frameon=False,
    fontsize=9,
    loc="upper right",
)


# ---------------------------------------------------------------------
# Add cluster-structure annotations
# ---------------------------------------------------------------------

for case_index, (_, row) in enumerate(df.iterrows()):

    sizes = row["cluster_sizes_parsed"]

    structure = "[" + ",".join(
        str(int(x))
        for x in sizes
    ) + "]"

    ax.text(
        max(
            df["cluster_sizes_parsed"]
            .apply(sum)
        ) + 0.15,
        case_index,
        structure,
        va="center",
        fontsize=9,
    )


# Give annotation space on right.
ax.set_xlim(
    0,
    max(
        df["cluster_sizes_parsed"]
        .apply(sum)
    ) + 1.4,
)


# ---------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------

fig.tight_layout()


# ---------------------------------------------------------------------
# Save high-resolution manuscript figure
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
print("Figure 5 generation complete.")
print("=" * 70)