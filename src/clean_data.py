from pathlib import Path

import pandas as pd


# -------------------------
# Dateien
# -------------------------

input_path = Path("data/raw/pension_records.csv")
output_path = Path("data/processed/pension_records_clean.csv")


# -------------------------
# Daten einlesen
# -------------------------

df = pd.read_csv(input_path)

print(f"Ausgangsdatensätze: {len(df)}")


# -------------------------
# 1. Dubletten entfernen
# -------------------------

df = df.drop_duplicates()

print(f"Nach Dublettenbereinigung: {len(df)}")


# -------------------------
# 2. Eintrittsdatum konvertieren
# -------------------------

df["entry_date"] = pd.to_datetime(
    df["entry_date"],
    errors="coerce"
)


# -------------------------
# 3. Ungültige Werte markieren
# -------------------------

df.loc[
    (df["age"] < 18) | (df["age"] > 100),
    "age"
] = pd.NA

df.loc[
    df["annual_salary_chf"] <= 0,
    "annual_salary_chf"
] = pd.NA

df.loc[
    df["annual_contribution_chf"] <= 0,
    "annual_contribution_chf"
] = pd.NA


# -------------------------
# 4. Unvollständige Datensätze entfernen
# -------------------------

required_columns = [
    "person_id",
    "age",
    "annual_salary_chf",
    "entry_date",
    "employer",
    "annual_contribution_chf",
]

df_clean = df.dropna(
    subset=required_columns
)


# -------------------------
# 5. Bereinigte Daten speichern
# -------------------------

df_clean.to_csv(
    output_path,
    index=False
)

print(f"Bereinigte Datensätze: {len(df_clean)}")
print(f"Datei gespeichert: {output_path}")