from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


input_path = Path("reports/data_quality_comparison.csv")
df = pd.read_csv(input_path)

label_mapping = {
    "duplicate_rows": "Duplicate rows",
    "missing_salaries": "Missing salaries",
    "missing_employers": "Missing employers",
    "invalid_ages": "Invalid ages",
    "invalid_salaries": "Invalid salaries",
    "invalid_contributions": "Invalid contributions",
    "invalid_dates": "Invalid dates",
}

df["label"] = df["quality_check"].map(label_mapping)

source_path = Path("data/raw/pension_records.csv")

fig = plt.figure(figsize=(10, 6))

bars = plt.barh(
    df["label"],
    df["raw_data"]
)

fig.canvas.manager.set_window_title(
    f"Data Quality Analysis - {source_path.name}"
)

plt.suptitle(
    "Detected Data Quality Issues",
    fontweight="bold",
    fontsize=14
)

plt.title(
    f"Source: {source_path.name}",
    fontsize=8
)

plt.xlabel("Number of issues")
plt.ylabel("Quality issue")

plt.gca().invert_yaxis()

for bar in bars:
    width = bar.get_width()
    plt.text(
        width + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width)}",
        va="center"
    )

plt.tight_layout()

output_path = Path("reports/data_quality_issues.png")
plt.savefig(output_path, dpi=150)
plt.show()

print(f"Figure saved: {output_path}")