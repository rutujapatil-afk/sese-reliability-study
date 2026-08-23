"""
SeSE FINAL SYNTHESIS AUDIT

Read-only audit of the final quantitative synthesis.

Reads:
    results/final_synthesis/quantitative_summary.csv
    results/final_synthesis/quantitative_summary.md
    results/final_synthesis/research_claims.md

Does NOT modify any experiment or synthesis files.
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "results" / "final_synthesis"

CSV_FILE = SYNTHESIS / "quantitative_summary.csv"
SUMMARY_FILE = SYNTHESIS / "quantitative_summary.md"
CLAIMS_FILE = SYNTHESIS / "research_claims.md"


def print_file(title, path):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    if not path.exists():
        print(f"[MISSING] {path}")
        return False

    print(f"[FILE] {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"[ERROR] Could not read file: {exc}")
        return False

    print("-" * 80)
    print(text)
    print("-" * 80)

    return True


def audit_csv():
    print("\n" + "=" * 80)
    print("QUANTITATIVE SUMMARY TABLE")
    print("=" * 80)

    if not CSV_FILE.exists():
        print(f"[MISSING] {CSV_FILE}")
        return None

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as exc:
        print(f"[ERROR] Could not read CSV: {exc}")
        return None

    print(f"[OK] Rows: {len(df)}")
    print(f"[OK] Columns: {list(df.columns)}")
    print()

    if df.empty:
        print("[WARNING] Quantitative summary is empty.")
        return df

    print(df.to_string(index=False))

    return df


def check_scaled_evaluation(df):
    print("\n" + "=" * 80)
    print("SCALED EVALUATION CHECK")
    print("=" * 80)

    if df is None or df.empty:
        print("[WARNING] No quantitative summary available.")
        return

    scaled = df[df["experiment"].astype(str) == "scaled_evaluation"]

    if scaled.empty:
        print("[ERROR] No scaled_evaluation metrics found.")
        return

    print("[OK] scaled_evaluation metrics found.")
    print()

    print(scaled.to_string(index=False))

    print()

    metrics = set(scaled["metric"].astype(str))

    expected = {
        "cases_evaluated",
        "unique_cases",
        "total_responses",
    }

    missing = expected - metrics

    if missing:
        print(f"[WARNING] Missing expected metrics: {sorted(missing)}")
    else:
        print("[OK] Core scaled-evaluation metrics are present.")


def check_claims():
    print("\n" + "=" * 80)
    print("RESEARCH CLAIMS CHECK")
    print("=" * 80)

    if not CLAIMS_FILE.exists():
        print(f"[MISSING] {CLAIMS_FILE}")
        return

    text = CLAIMS_FILE.read_text(encoding="utf-8")

    expected_sections = [
        "Claim 1",
        "Claim 2",
        "Claim 3",
        "Claim 4",
        "Claim 5",
        "What We Cannot Yet Claim",
        "Recommended Next Stage",
    ]

    for section in expected_sections:
        if section in text:
            print(f"[OK] {section}")
        else:
            print(f"[WARNING] Missing section: {section}")

    if "scaled evaluation" in text.lower():
        print("[OK] Scaled evaluation is mentioned in research claims.")
    else:
        print("[WARNING] Scaled evaluation is not mentioned in research claims.")

    if "fallback" in text.lower():
        print("[OK] Enhancement/API fallback caveat is documented.")
    else:
        print("[WARNING] Enhancement/API fallback caveat was not detected.")


def main():
    print("=" * 80)
    print("SeSE FINAL SYNTHESIS — EVIDENCE AUDIT")
    print("=" * 80)
    print(f"Project root: {ROOT}")
    print(f"Synthesis directory: {SYNTHESIS}")

    required_files = [
        CSV_FILE,
        SUMMARY_FILE,
        CLAIMS_FILE,
    ]

    print("\n" + "=" * 80)
    print("FILE AVAILABILITY")
    print("=" * 80)

    all_present = True

    for path in required_files:
        if path.exists():
            print(f"[OK] {path.name}")
        else:
            print(f"[MISSING] {path.name}")
            all_present = False

    if not all_present:
        print("\n[ERROR] One or more synthesis files are missing.")
        return 1

    df = audit_csv()

    check_scaled_evaluation(df)

    print_file(
        "QUANTITATIVE SYNTHESIS MARKDOWN",
        SUMMARY_FILE,
    )

    print_file(
        "RESEARCH CLAIMS",
        CLAIMS_FILE,
    )

    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)

    print(
        """
No files were modified.

Next step:
Review the quantitative values and candidate claims above.
"""
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())