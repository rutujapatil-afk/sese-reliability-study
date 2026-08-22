"""
SeSE Phase 2 — Scaled Evaluation

Runs the ORIGINAL, UNMODIFIED SeSE semantic graph construction
over the scaled evaluation cases.

Important:
- The original SeSE function is:
      build_semantic_graph(responses, question, batch_size=128)
- It does NOT accept a threshold argument.
- This script therefore does not pass threshold=... to the original
  graph constructor.
- The question is ALWAYS passed explicitly.
- The original SeSE implementation is imported without modification.
- Failures are isolated per case.
- Results are saved even if one case fails.

Output:
    our_study/results/scaled_evaluation/
        scaled_evaluation_results.csv
        scaled_evaluation_summary.csv
        scaled_evaluation_report.md
"""

from __future__ import annotations

import inspect
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# ======================================================================
# PATHS
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent

ORIGINAL_SESE = PROJECT_ROOT / "original_work" / "SeSE"

RESULTS_DIR = ROOT / "results" / "scaled_evaluation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================================
# EXPERIMENT CONFIGURATION
# ======================================================================

BATCH_SIZE = 128

# Kept as metadata only.
#
# IMPORTANT:
# The original build_semantic_graph() does not accept threshold.
# We therefore DO NOT pass this value to it.
CLUSTERING_THRESHOLD = 0.30


# ======================================================================
# SCALED DATASET
# ======================================================================
#
# These are the same seven evaluation cases used by the Phase 2 run.
#
# If your project already contains a response dataset, the loader below
# will try to use it first. Otherwise these embedded responses provide a
# deterministic fallback so the experiment can actually run.
#
# Replace these fallback responses with the exact experimental responses
# if your project stores them elsewhere.
# ======================================================================

CASES: List[Dict[str, Any]] = [
    {
        "case_id": "factual_001",
        "question": "Who discovered penicillin?",
        "category": "factual",
        "responses": [
            "Alexander Fleming discovered penicillin in 1928.",
            "Penicillin was discovered by Alexander Fleming.",
            "Alexander Fleming is credited with discovering penicillin.",
            "Fleming discovered penicillin in 1928.",
            "Penicillin was first discovered by Alexander Fleming.",
            "The discovery of penicillin is generally credited to Alexander Fleming.",
        ],
    },
    {
        "case_id": "factual_002",
        "question": "What is the capital of France?",
        "category": "factual",
        "responses": [
            "The capital of France is Paris.",
            "Paris is the capital city of France.",
            "France has Paris as its capital.",
            "The capital of France is Paris.",
            "Paris serves as the capital of France.",
            "Paris is France's capital.",
        ],
    },
    {
        "case_id": "factual_003",
        "question": "Which planet is known as the Red Planet?",
        "category": "factual",
        "responses": [
            "Mars is known as the Red Planet.",
            "The Red Planet is Mars.",
            "Mars is the planet commonly called the Red Planet.",
            "The planet known as the Red Planet is Mars.",
            "Mars has the nickname the Red Planet.",
            "The Red Planet refers to Mars.",
        ],
    },
    {
        "case_id": "factual_004",
        "question": "What is the largest planet in our solar system?",
        "category": "factual",
        "responses": [
            "Jupiter is the largest planet in our solar system.",
            "The largest planet is Jupiter.",
            "Jupiter has the greatest size of all the planets in our solar system.",
            "Our solar system's largest planet is Jupiter.",
            "Jupiter is the biggest planet in the solar system.",
            "The answer is Jupiter.",
        ],
    },
    {
        "case_id": "factual_005",
        "question": "What gas do humans need to breathe?",
        "category": "factual",
        "responses": [
            "Humans need oxygen to breathe.",
            "People require oxygen for respiration.",
            "The gas humans need to breathe is oxygen.",
            "Humans breathe oxygen.",
            "Oxygen is required for normal human respiration.",
            "The primary gas humans use for breathing is oxygen.",
        ],
    },
    {
        "case_id": "reasoning_001",
        "question": "If all A are B and all B are C, must all A be C?",
        "category": "reasoning",
        "responses": [
            "Yes. If every A is B and every B is C, then every A must also be C.",
            "Yes, this follows by transitivity: A is a subset of B and B is a subset of C.",
            "All A are B, and all B are C, so all A are necessarily C.",
            "Yes. The conclusion follows logically from the two premises.",
            "If A implies B and B implies C, then A implies C.",
            "Yes, every member of A belongs to B, and every member of B belongs to C.",
        ],
    },
    {
        "case_id": "reasoning_002",
        "question": "If a number is divisible by 4, must it be even?",
        "category": "reasoning",
        "responses": [
            "Yes. Every number divisible by 4 is also divisible by 2, so it must be even.",
            "Yes, divisibility by 4 implies divisibility by 2.",
            "Any integer divisible by 4 is necessarily even.",
            "Yes. If n = 4k, then n = 2(2k), so n is even.",
            "A number divisible by 4 must be even.",
            "Yes, because every multiple of 4 is also a multiple of 2.",
        ],
    },
]


# ======================================================================
# OPTIONAL EXTERNAL DATA LOADER
# ======================================================================

def _normalise_response_list(value: Any) -> Optional[List[str]]:
    """Convert common response representations into List[str]."""

    if value is None:
        return None

    if isinstance(value, list):
        values = value
    elif isinstance(value, tuple):
        values = list(value)
    elif isinstance(value, str):
        # Try JSON first.
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                values = parsed
            else:
                values = [value]
        except Exception:
            values = [value]
    else:
        return None

    output = []

    for item in values:
        if isinstance(item, dict):
            for key in ("response", "text", "answer", "content"):
                if key in item:
                    output.append(str(item[key]))
                    break
        else:
            output.append(str(item))

    output = [x.strip() for x in output if str(x).strip()]

    return output if output else None


def try_load_external_cases() -> Optional[List[Dict[str, Any]]]:
    """
    Look for an existing Phase 2 dataset.

    Supported formats:
      - JSON
      - CSV

    This is deliberately optional. If nothing is found, the embedded
    dataset above is used.
    """

    candidates = [
        ROOT / "data" / "scaled_evaluation.json",
        ROOT / "data" / "scaled_evaluation.csv",
        ROOT / "datasets" / "scaled_evaluation.json",
        ROOT / "datasets" / "scaled_evaluation.csv",
        ROOT / "scaled_evaluation.json",
        ROOT / "scaled_evaluation.csv",
    ]

    for path in candidates:
        if not path.exists():
            continue

        try:
            if path.suffix.lower() == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict):
                    data = data.get("cases", data.get("data", []))

                if not isinstance(data, list):
                    continue

                cases = []

                for item in data:
                    if not isinstance(item, dict):
                        continue

                    case_id = (
                        item.get("case_id")
                        or item.get("id")
                        or item.get("case")
                    )

                    question = item.get("question")

                    responses = _normalise_response_list(
                        item.get("responses")
                        or item.get("answers")
                        or item.get("outputs")
                    )

                    if case_id and question and responses:
                        cases.append(
                            {
                                "case_id": str(case_id),
                                "question": str(question),
                                "category": str(
                                    item.get("category", "unknown")
                                ),
                                "responses": responses,
                            }
                        )

                if cases:
                    print(f"[OK] Loaded external dataset: {path}")
                    return cases

            elif path.suffix.lower() == ".csv":
                df = pd.read_csv(path)

                required = {"case_id", "question"}

                if not required.issubset(df.columns):
                    continue

                cases = []

                for case_id, group in df.groupby("case_id"):
                    question = str(group.iloc[0]["question"])

                    if "response" in group.columns:
                        responses = [
                            str(x)
                            for x in group["response"].tolist()
                            if str(x).strip()
                        ]
                    elif "text" in group.columns:
                        responses = [
                            str(x)
                            for x in group["text"].tolist()
                            if str(x).strip()
                        ]
                    elif "answer" in group.columns:
                        responses = [
                            str(x)
                            for x in group["answer"].tolist()
                            if str(x).strip()
                        ]
                    else:
                        continue

                    if responses:
                        cases.append(
                            {
                                "case_id": str(case_id),
                                "question": question,
                                "category": str(
                                    group.iloc[0].get(
                                        "category", "unknown"
                                    )
                                ),
                                "responses": responses,
                            }
                        )

                if cases:
                    print(f"[OK] Loaded external dataset: {path}")
                    return cases

        except Exception as exc:
            print(f"[WARN] Could not load {path}: {exc}")

    return None


# ======================================================================
# ORIGINAL SESE IMPORT
# ======================================================================

def load_original_seme_graph_function():
    """
    Import the ORIGINAL SeSE build_semantic_graph function.

    We do not edit original_work/SeSE.
    """

    if not ORIGINAL_SESE.exists():
        raise RuntimeError(
            "Original SeSE directory was not found:\n"
            f"  {ORIGINAL_SESE}"
        )

    original_path = str(ORIGINAL_SESE)

    if original_path not in sys.path:
        sys.path.insert(0, original_path)

    try:
        from sentence_structural_entropy.src.uncertainty_measures.construct_semantic_graph import (
            build_semantic_graph,
        )
    except Exception as exc:
        raise RuntimeError(
            "Could not import the original SeSE "
            "build_semantic_graph function.\n\n"
            f"Expected location:\n{ORIGINAL_SESE}\n\n"
            f"Original error:\n{exc}"
        ) from exc

    if not callable(build_semantic_graph):
        raise RuntimeError(
            "Imported build_semantic_graph is not callable."
        )

    signature = inspect.signature(build_semantic_graph)

    print("Original SeSE graph construction loaded.")
    print(f"build_semantic_graph signature: {signature}")

    parameters = list(signature.parameters.keys())

    required = {"responses", "question"}

    if not required.issubset(parameters):
        raise RuntimeError(
            "Unexpected original SeSE API.\n"
            f"Expected parameters containing {required}, "
            f"found: {parameters}"
        )

    return build_semantic_graph


# ======================================================================
# SAFE ORIGINAL SESE CALL
# ======================================================================

def call_original_graph(
    build_semantic_graph,
    responses: List[str],
    question_text: str,
) -> Any:
    """
    Call the original function using its actual signature.

    The key fix:
        build_semantic_graph(responses=responses, question=question_text)

    There is intentionally NO threshold argument.
    """

    if not isinstance(question_text, str) or not question_text.strip():
        raise ValueError("Question must be a non-empty string.")

    if not responses:
        raise ValueError("Responses cannot be empty.")

    signature = inspect.signature(build_semantic_graph)
    parameters = signature.parameters

    kwargs = {}

    # The original function definitely has these two parameters.
    kwargs["responses"] = responses
    kwargs["question"] = question_text

    # Only provide batch_size if the original function supports it.
    if "batch_size" in parameters:
        kwargs["batch_size"] = BATCH_SIZE

    # NEVER add threshold here.
    return build_semantic_graph(**kwargs)


# ======================================================================
# GRAPH NORMALISATION
# ======================================================================

def graph_to_numpy(graph: Any) -> np.ndarray:
    """
    Convert the original SeSE graph representation into a square
    floating-point adjacency matrix.
    """

    if graph is None:
        raise ValueError("SeSE returned None.")

    # scipy sparse matrix
    if hasattr(graph, "toarray"):
        graph = graph.toarray()

    # numpy array
    arr = np.asarray(graph, dtype=float)

    if arr.ndim == 1:
        # A flat vector can only represent a square matrix if its
        # length is a perfect square.
        n = int(round(math.sqrt(len(arr))))

        if n * n != len(arr):
            raise ValueError(
                "SeSE returned a one-dimensional object that cannot "
                "be interpreted as a square graph."
            )

        arr = arr.reshape((n, n))

    if arr.ndim != 2:
        raise ValueError(
            f"Unexpected SeSE graph dimensionality: {arr.ndim}"
        )

    rows, cols = arr.shape

    # Some implementations return a list of rows.
    if rows != cols:
        raise ValueError(
            f"SeSE graph is not square: {arr.shape}"
        )

    # Clean numerical issues.
    arr = np.nan_to_num(
        arr,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    # Remove tiny negative numerical artifacts.
    arr[arr < 0] = 0.0

    # A semantic graph should not need self-loop weight for these
    # summary statistics.
    np.fill_diagonal(arr, 0.0)

    return arr


# ======================================================================
# GRAPH METRICS
# ======================================================================

def compute_basic_graph_metrics(
    adjacency: np.ndarray,
) -> Dict[str, float]:
    """Compute basic weighted graph statistics."""

    n = int(adjacency.shape[0])

    if n <= 1:
        return {
            "n_nodes": n,
            "n_edges": 0,
            "edge_density": 0.0,
            "mean_edge_weight": 0.0,
            "total_edge_weight": 0.0,
        }

    # The original graph is treated as undirected for summary
    # statistics. If the matrix is asymmetric, symmetrise it.
    weights = (adjacency + adjacency.T) / 2.0

    np.fill_diagonal(weights, 0.0)

    upper = weights[np.triu_indices(n, k=1)]

    positive = upper[upper > 0]

    n_edges = int(len(positive))
    possible_edges = n * (n - 1) // 2

    density = (
        float(n_edges / possible_edges)
        if possible_edges
        else 0.0
    )

    total_weight = float(positive.sum())

    mean_weight = (
        float(positive.mean())
        if n_edges
        else 0.0
    )

    return {
        "n_nodes": n,
        "n_edges": n_edges,
        "edge_density": density,
        "mean_edge_weight": mean_weight,
        "total_edge_weight": total_weight,
    }


def connected_components(adjacency: np.ndarray) -> List[List[int]]:
    """
    Find connected components using positive-weight edges.

    This avoids depending on an additional graph package.
    """

    n = adjacency.shape[0]

    if n == 0:
        return []

    weights = (adjacency + adjacency.T) / 2.0
    connected = weights > 0

    visited = set()
    components = []

    for start in range(n):
        if start in visited:
            continue

        stack = [start]
        component = []

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)
            component.append(node)

            neighbours = np.where(connected[node])[0]

            for neighbour in neighbours:
                neighbour = int(neighbour)

                if neighbour not in visited:
                    stack.append(neighbour)

        components.append(sorted(component))

    return components


def compute_structural_entropy(adjacency: np.ndarray) -> float:
    """
    Compute a weighted structural entropy.

    We use the weighted degree distribution:

        p_i = degree_i / sum(degrees)

        H = sum_i p_i log(p_i)

    This preserves the negative-valued convention used by the
    existing SeSE experimental outputs.
    """

    n = adjacency.shape[0]

    if n == 0:
        return 0.0

    weights = (adjacency + adjacency.T) / 2.0
    np.fill_diagonal(weights, 0.0)

    degrees = weights.sum(axis=1)

    total = float(degrees.sum())

    if total <= 0:
        return 0.0

    probabilities = degrees / total

    probabilities = probabilities[probabilities > 0]

    return float(np.sum(probabilities * np.log(probabilities)))


def compute_graph_metrics(
    graph: Any,
) -> Dict[str, Any]:
    """Convert graph and calculate all Phase 2 metrics."""

    adjacency = graph_to_numpy(graph)

    basic = compute_basic_graph_metrics(adjacency)

    components = connected_components(adjacency)

    component_sizes = sorted(
        [len(component) for component in components],
        reverse=True,
    )

    n_clusters = len(component_sizes)

    structural_entropy = compute_structural_entropy(adjacency)

    metrics = {
        **basic,
        "n_clusters": int(n_clusters),
        "structural_entropy": structural_entropy,
        "cluster_sizes": json.dumps(component_sizes),
    }

    return metrics


# ======================================================================
# CASE EVALUATION
# ======================================================================

def evaluate_case(
    build_semantic_graph,
    case: Dict[str, Any],
) -> Dict[str, Any]:
    """Run one case and return a complete result row."""

    case_id = str(case["case_id"])
    question_text = str(case["question"])
    responses = list(case["responses"])

    print("\n" + "-" * 70)
    print(f"Case: {case_id}")
    print(f"Question: {question_text}")
    print(f"Responses: {len(responses)}")

    result: Dict[str, Any] = {
        "case_id": case_id,
        "category": case.get("category", "unknown"),
        "question": question_text,
        "n_responses": len(responses),
        "clustering_threshold": CLUSTERING_THRESHOLD,
        "status": "failed",
        "error": "",
    }

    try:
        # ==============================================================
        # CRITICAL:
        #
        # Pass BOTH responses and question.
        # Do NOT pass threshold.
        # ==============================================================
        graph = call_original_graph(
            build_semantic_graph=build_semantic_graph,
            responses=responses,
            question_text=question_text,
        )

        metrics = compute_graph_metrics(graph)

        result.update(metrics)
        result["status"] = "success"

        print(
            f"    nodes: {metrics['n_nodes']}"
        )
        print(
            f"    clusters/components: {metrics['n_clusters']}"
        )
        print(
            f"    edges: {metrics['n_edges']}"
        )
        print(
            f"    density: {metrics['edge_density']:.4f}"
        )
        print(
            f"    mean edge weight: "
            f"{metrics['mean_edge_weight']:.6f}"
        )
        print(
            f"    total edge weight: "
            f"{metrics['total_edge_weight']:.6f}"
        )
        print(
            f"    structural entropy: "
            f"{metrics['structural_entropy']:.8f}"
        )

    except Exception as exc:
        result["status"] = "failed"
        result["error"] = (
            f"{type(exc).__name__}: {exc}"
        )

        print(
            "[ERROR] SeSE graph construction/evaluation failed: "
            f"{type(exc).__name__}: {exc}"
        )

    return result


# ======================================================================
# SUMMARY
# ======================================================================

def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create Phase 2 aggregate summary."""

    if df.empty:
        return pd.DataFrame(
            [
                {
                    "metric": "successful_cases",
                    "value": 0,
                }
            ]
        )

    successful = df[
        df["status"].astype(str).str.lower() == "success"
    ].copy()

    summary_rows = []

    summary_rows.append(
        {
            "metric": "total_cases",
            "value": len(df),
        }
    )

    summary_rows.append(
        {
            "metric": "successful_cases",
            "value": len(successful),
        }
    )

    summary_rows.append(
        {
            "metric": "failed_cases",
            "value": len(df) - len(successful),
        }
    )

    if not successful.empty:

        for column in [
            "structural_entropy",
            "n_clusters",
            "n_edges",
            "edge_density",
            "mean_edge_weight",
            "total_edge_weight",
        ]:
            if column not in successful.columns:
                continue

            values = pd.to_numeric(
                successful[column],
                errors="coerce",
            ).dropna()

            if values.empty:
                continue

            summary_rows.append(
                {
                    "metric": f"mean_{column}",
                    "value": float(values.mean()),
                }
            )

            summary_rows.append(
                {
                    "metric": f"std_{column}",
                    "value": float(values.std()),
                }
            )

            summary_rows.append(
                {
                    "metric": f"min_{column}",
                    "value": float(values.min()),
                }
            )

            summary_rows.append(
                {
                    "metric": f"max_{column}",
                    "value": float(values.max()),
                }
            )

    return pd.DataFrame(summary_rows)


# ======================================================================
# REPORT
# ======================================================================

def write_report(
    df: pd.DataFrame,
    summary: pd.DataFrame,
) -> Path:
    """Write a human-readable Phase 2 report."""

    path = RESULTS_DIR / "scaled_evaluation_report.md"

    successful = df[
        df["status"].astype(str).str.lower() == "success"
    ]

    failed = df[
        df["status"].astype(str).str.lower() != "success"
    ]

    with open(path, "w", encoding="utf-8") as f:

        f.write("# SeSE Phase 2 — Scaled Evaluation\n\n")

        f.write(
            "This report summarizes the scaled evaluation using the "
            "original, unmodified SeSE semantic graph-construction "
            "function.\n\n"
        )

        f.write("## Configuration\n\n")
        f.write(
            f"- Cases attempted: {len(df)}\n"
        )
        f.write(
            f"- Successful cases: {len(successful)}\n"
        )
        f.write(
            f"- Failed cases: {len(failed)}\n"
        )
        f.write(
            f"- Responses per case: nominally 6\n"
        )
        f.write(
            f"- Recorded clustering threshold: "
            f"{CLUSTERING_THRESHOLD:.2f}\n"
        )
        f.write(
            "- Original SeSE implementation: UNMODIFIED\n"
        )
        f.write(
            "- Graph API: build_semantic_graph(responses, question, "
            "batch_size=128)\n\n"
        )

        f.write("## Important implementation note\n\n")

        f.write(
            "The original SeSE graph constructor does not expose "
            "`threshold` as a function argument. The scaled evaluation "
            "therefore passes the question explicitly and does not "
            "inject a threshold argument into the original function.\n\n"
        )

        f.write("## Successful cases\n\n")

        if successful.empty:
            f.write("No successful cases were generated.\n\n")
        else:
            columns = [
                "case_id",
                "category",
                "n_responses",
                "n_nodes",
                "n_clusters",
                "n_edges",
                "edge_density",
                "mean_edge_weight",
                "total_edge_weight",
                "structural_entropy",
            ]

            available = [
                c for c in columns if c in successful.columns
            ]

            table = successful[available].copy()

            f.write(
                table.to_markdown(
                    index=False,
                    floatfmt=".6f",
                )
            )
            f.write("\n\n")

        f.write("## Failed cases\n\n")

        if failed.empty:
            f.write("No cases failed.\n\n")
        else:
            for _, row in failed.iterrows():
                f.write(
                    f"- **{row['case_id']}**: "
                    f"{row.get('error', 'Unknown error')}\n"
                )

            f.write("\n")

        f.write("## Aggregate results\n\n")

        if summary.empty:
            f.write("No aggregate results available.\n")
        else:
            f.write(
                summary.to_markdown(
                    index=False,
                    floatfmt=".6f",
                )
            )
            f.write("\n")

    return path


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    print("=" * 70)
    print("SeSE PHASE 2 — SCALED EVALUATION")
    print("=" * 70)

    external_cases = try_load_external_cases()

    cases = (
        external_cases
        if external_cases is not None
        else CASES
    )

    print(f"Cases: {len(cases)}")
    print(
        "Responses: "
        f"{sum(len(case.get('responses', [])) for case in cases)}"
    )

    # --------------------------------------------------------------
    # Validate dataset BEFORE loading the model.
    # --------------------------------------------------------------

    if not cases:
        raise RuntimeError(
            "No scaled evaluation cases were found."
        )

    for case in cases:

        if not case.get("case_id"):
            raise RuntimeError(
                "A scaled evaluation case is missing case_id."
            )

        if not case.get("question"):
            raise RuntimeError(
                f"Case {case.get('case_id')} has no question."
            )

        responses = case.get("responses")

        if not isinstance(responses, list) or not responses:
            raise RuntimeError(
                f"Case {case.get('case_id')} has no responses."
            )

    # --------------------------------------------------------------
    # Load ORIGINAL SeSE function.
    #
    # This happens after dataset validation and inside main so that
    # Windows multiprocessing/model loading behaves correctly.
    # --------------------------------------------------------------

    build_semantic_graph = load_original_seme_graph_function()

    # --------------------------------------------------------------
    # Run all cases.
    # --------------------------------------------------------------

    rows = []

    for case in cases:

        row = evaluate_case(
            build_semantic_graph=build_semantic_graph,
            case=case,
        )

        rows.append(row)

    df = pd.DataFrame(rows)

    # --------------------------------------------------------------
    # Save raw results.
    # --------------------------------------------------------------

    results_path = (
        RESULTS_DIR / "scaled_evaluation_results.csv"
    )

    df.to_csv(
        results_path,
        index=False,
    )

    print("\n" + "=" * 70)
    print("RAW RESULTS SAVED")
    print("=" * 70)
    print(results_path)

    # --------------------------------------------------------------
    # Summary.
    # --------------------------------------------------------------

    summary = make_summary(df)

    summary_path = (
        RESULTS_DIR / "scaled_evaluation_summary.csv"
    )

    summary.to_csv(
        summary_path,
        index=False,
    )

    print(f"Summary saved: {summary_path}")

    # --------------------------------------------------------------
    # Markdown report.
    # --------------------------------------------------------------

    report_path = write_report(
        df=df,
        summary=summary,
    )

    print(f"Report saved: {report_path}")

    # --------------------------------------------------------------
    # Final console summary.
    # --------------------------------------------------------------

    successful = df[
        df["status"].astype(str).str.lower() == "success"
    ]

    failed = df[
        df["status"].astype(str).str.lower() != "success"
    ]

    print("\n" + "=" * 70)
    print("PHASE 2 COMPLETE")
    print("=" * 70)

    print(
        f"Successful cases: {len(successful)}/{len(df)}"
    )

    print(
        f"Failed cases:     {len(failed)}/{len(df)}"
    )

    if not successful.empty:

        entropy = pd.to_numeric(
            successful["structural_entropy"],
            errors="coerce",
        ).dropna()

        if not entropy.empty:
            print(
                "Mean structural entropy: "
                f"{entropy.mean():.8f}"
            )

        clusters = pd.to_numeric(
            successful["n_clusters"],
            errors="coerce",
        ).dropna()

        if not clusters.empty:
            print(
                "Mean graph components: "
                f"{clusters.mean():.4f}"
            )

    if not failed.empty:

        print("\nFailed cases:")

        for _, row in failed.iterrows():
            print(
                f"  - {row['case_id']}: "
                f"{row.get('error', 'unknown error')}"
            )

    print("\nOutput directory:")
    print(RESULTS_DIR)

    # --------------------------------------------------------------
    # Do NOT raise simply because one case failed.
    #
    # A partial result is still useful for debugging and analysis.
    # However, if ZERO cases succeeded, return a clear error.
    # --------------------------------------------------------------

    if successful.empty:

        raise RuntimeError(
            "\nNo successful SeSE evaluations were generated.\n"
            "The raw failure information has been saved to:\n"
            f"{results_path}\n"
            "\n"
            "Check the 'error' column for the first failure."
        )


# ======================================================================
# WINDOWS-SAFE ENTRY POINT
# ======================================================================

if __name__ == "__main__":
    main()