from pathlib import Path

import numpy as np
import pandas as pd


# Zufallszahlen reproduzierbar machen
rng = np.random.default_rng(seed=42)

NUMBER_OF_RECORDS = 1000


# -------------------------
# Grunddaten erzeugen
# -------------------------

person_ids = np.arange(
    100001,
    100001 + NUMBER_OF_RECORDS
)

ages = rng.integers(
    low=18,
    high=66,
    size=NUMBER_OF_RECORDS
)

salaries = rng.normal(
    loc=82000,
    scale=18000,
    size=NUMBER_OF_RECORDS
)

salaries = np.round(
    np.clip(salaries, 30000, 180000),
    2
)

employers = rng.choice(
    [
        "AlpenTech AG",
        "Helvetia Services AG",
        "Bodensee Logistics AG",
        "Rhein Consulting GmbH",
        "Säntis Industries AG",
    ],
    size=NUMBER_OF_RECORDS,
)

start_date = pd.Timestamp("2015-01-01")

entry_dates = (
    start_date
    + pd.to_timedelta(
        rng.integers(
            0,
            365 * 11,
            size=NUMBER_OF_RECORDS,
        ),
        unit="D",
    )
)

contribution_rates = rng.uniform(
    0.06,
    0.12,
    NUMBER_OF_RECORDS,
)

contributions = np.round(
    salaries * contribution_rates,
    2,
)


# -------------------------
# DataFrame erstellen
# -------------------------

df = pd.DataFrame(
    {
        "person_id": person_ids,
        "age": ages,
        "annual_salary_chf": salaries,
        "entry_date": entry_dates.strftime("%Y-%m-%d"),
        "employer": employers,
        "annual_contribution_chf": contributions,
    }
)


# -------------------------
# Absichtlich Fehler einbauen
# -------------------------

# Fehlende Gehälter
df.loc[[3, 87, 412], "annual_salary_chf"] = np.nan

# Unrealistisches Alter
df.loc[25, "age"] = 142
df.loc[300, "age"] = -4

# Negatives Gehalt
df.loc[600, "annual_salary_chf"] = -5000

# Fehlender Arbeitgeber
df.loc[710, "employer"] = None

# Beitrag von 0 CHF
df.loc[820, "annual_contribution_chf"] = 0

# Ungültige Datumswerte
df.loc[910, "entry_date"] = "2025-02-31"
df.loc[950, "entry_date"] = "invalid_date"

# Dubletten hinzufügen
duplicates = df.iloc[[20, 120, 450]].copy()

df = pd.concat(
    [df, duplicates],
    ignore_index=True,
)


# -------------------------
# Datei speichern
# -------------------------

output_path = Path("data/raw/pension_records.csv")

df.to_csv(
    output_path,
    index=False,
)

print(f"Datensatz gespeichert: {output_path}")
print(f"Anzahl Datensätze: {len(df)}")

print("\nErste fünf Datensätze:")
print(df.head())