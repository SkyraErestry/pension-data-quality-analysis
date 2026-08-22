from pathlib import Path

import pandas as pd


# -------------------------
# Dateien einlesen
# -------------------------

raw_path = Path("data/raw/pension_records.csv")
clean_path = Path("data/processed/pension_records_clean.csv")

df_raw = pd.read_csv(raw_path)
df_clean = pd.read_csv(clean_path)


# -------------------------
# Hilfsfunktion
# -------------------------

def count_quality_issues(df):
    parsed_dates = pd.to_datetime(
        df["entry_date"],
        errors="coerce"
    )

    issues = {
        "duplicate_rows": df.duplicated().sum(),

        "missing_salaries":
            df["annual_salary_chf"].isna().sum(),

        "missing_employers":
            df["employer"].isna().sum(),

        "invalid_ages":
            (
                (df["age"] < 18)
                | (df["age"] > 100)
            ).sum(),

        "invalid_salaries":
            (
                df["annual_salary_chf"] <= 0
            ).sum(),

        "invalid_contributions":
            (
                df["annual_contribution_chf"] <= 0
            ).sum(),

        "invalid_dates":
            parsed_dates.isna().sum(),
    }

    return issues


# -------------------------
# Checks durchführen
# -------------------------

raw_issues = count_quality_issues(df_raw)
clean_issues = count_quality_issues(df_clean)


# -------------------------
# Report erstellen
# -------------------------

comparison = pd.DataFrame(
    {
        "quality_check": raw_issues.keys(),
        "raw_data": raw_issues.values(),
        "clean_data": clean_issues.values(),
    }
)

comparison["issues_removed"] = (
    comparison["raw_data"]
    - comparison["clean_data"]
)

print("\n=== DATA QUALITY COMPARISON ===")
print(comparison.to_string(index=False))


# -------------------------
# Ergebnis speichern
# -------------------------

output_path = Path(
    "reports/data_quality_comparison.csv"
)

comparison.to_csv(
    output_path,
    index=False
)

print(
    f"\nComparison saved: {output_path}"
)