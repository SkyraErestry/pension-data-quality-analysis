from pathlib import Path

import pandas as pd


# -------------------------
# Datei einlesen
# -------------------------

input_path = Path("data/raw/pension_records.csv")

df = pd.read_csv(input_path)


# -------------------------
# Grundlegende Informationen
# -------------------------

print("=== ERSTE 5 ZEILEN ===")
print(df.head())

print("\n=== DIMENSIONEN ===")
print(f"Zeilen: {df.shape[0]}")
print(f"Spalten: {df.shape[1]}")

print("\n=== SPALTENNAMEN ===")
print(df.columns.tolist())

print("\n=== DATENTYPEN ===")
print(df.dtypes)

print("\n=== FEHLENDE WERTE ===")
print(df.isna().sum())

print("\n=== DOPPELTE ZEILEN ===")
print(f"Anzahl Dubletten: {df.duplicated().sum()}")

print("\n=== STATISTISCHE ÜBERSICHT ===")
print(df.describe())

print("\n=== DATA QUALITY CHECKS ===")

# -------------------------
# Ungültiges Alter
# -------------------------

invalid_age = df[
    (df["age"] < 18) |
    (df["age"] > 100)
]

print(f"Ungültige Alterswerte: {len(invalid_age)}")


# -------------------------
# Ungültiges Gehalt
# -------------------------

invalid_salary = df[
    df["annual_salary_chf"] <= 0
]

print(f"Ungültige Gehälter: {len(invalid_salary)}")


# -------------------------
# Ungültiger Beitrag
# -------------------------

invalid_contribution = df[
    df["annual_contribution_chf"] <= 0
]

print(
    f"Ungültige Beiträge: "
    f"{len(invalid_contribution)}"
)


# -------------------------
# Fehlende Arbeitgeber
# -------------------------

missing_employer = df[
    df["employer"].isna()
]

print(
    f"Fehlende Arbeitgeber: "
    f"{len(missing_employer)}"
)


# -------------------------
# Doppelte Person-IDs
# -------------------------

duplicate_person_ids = df[
    df["person_id"].duplicated(
        keep=False
    )
]

print(
    f"Datensätze mit doppelter Person-ID: "
    f"{len(duplicate_person_ids)}"
)

print("\n=== DATUMSPRÜFUNG ===")

# Versuche, die Spalte in echte Datumswerte umzuwandeln.
# Ungültige Werte werden dabei zu NaT.
parsed_entry_dates = pd.to_datetime(
    df["entry_date"],
    errors="coerce"
)

invalid_dates = df[
    parsed_entry_dates.isna()
]

print(
    f"Ungültige Eintrittsdaten: "
    f"{len(invalid_dates)}"
)

print("\nBetroffene Datensätze:")
print(
    invalid_dates[
        [
            "person_id",
            "entry_date"
        ]
    ]
)

# -------------------------
# Data Quality Report
# -------------------------

missing_salaries = df["annual_salary_chf"].isna().sum()
missing_employers = df["employer"].isna().sum()
duplicate_rows = df.duplicated().sum()
invalid_ages_count = len(invalid_age)
invalid_salaries_count = len(invalid_salary)
invalid_contributions_count = len(invalid_contribution)
invalid_dates_count = len(invalid_dates)

total_issues = (
    missing_salaries
    + missing_employers
    + duplicate_rows
    + invalid_ages_count
    + invalid_salaries_count
    + invalid_contributions_count
    + invalid_dates_count
)

print("\n=== DATA QUALITY REPORT ===")

print(f"Rows:                     {len(df)}")
print(f"Duplicate rows:           {duplicate_rows}")
print(f"Missing salaries:         {missing_salaries}")
print(f"Missing employers:        {missing_employers}")
print(f"Invalid ages:             {invalid_ages_count}")
print(f"Invalid salaries:         {invalid_salaries_count}")
print(f"Invalid contributions:    {invalid_contributions_count}")
print(f"Invalid dates:            {invalid_dates_count}")

print("-" * 40)
print(f"Total detected issues:    {total_issues}")

report = pd.DataFrame(
    {
        "check": [
            "duplicate_rows",
            "missing_salaries",
            "missing_employers",
            "invalid_ages",
            "invalid_salaries",
            "invalid_contributions",
            "invalid_dates",
        ],
        "issues_found": [
            duplicate_rows,
            missing_salaries,
            missing_employers,
            invalid_ages_count,
            invalid_salaries_count,
            invalid_contributions_count,
            invalid_dates_count,
        ],
    }
)

report_path = Path(
    "reports/data_quality_report.csv"
)

report.to_csv(
    report_path,
    index=False,
)

print(
    f"\nReport gespeichert: "
    f"{report_path}"
)