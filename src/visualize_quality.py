from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# -------------------------
# Report einlesen
# -------------------------

input_path = Path(
    "reports/data_quality_comparison.csv"
)

df = pd.read_csv(input_path)


# -------------------------
# Diagramm erstellen
# -------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["quality_check"],
    df["raw_data"]
)

plt.title(
    "Data Quality Issues in Raw Pension Data"
)

plt.xlabel("Quality Check")
plt.ylabel("Number of Issues")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()


# -------------------------
# Diagramm speichern
# -------------------------

output_path = Path(
    "reports/data_quality_issues.png"
)

plt.savefig(
    output_path,
    dpi=150
)

plt.show()

print(
    f"Diagramm gespeichert: {output_path}"
)