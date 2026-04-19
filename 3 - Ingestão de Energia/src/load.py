from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


def load_data(df: pd.DataFrame, output_dir: Path, alerts: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    processed_path = output_dir / "energy_processed.csv"
    quality_path = output_dir / "quality_report.json"
    partitioned_dir = output_dir / "partitioned"

    df.to_csv(processed_path, index=False)

    partitioned_dir.mkdir(exist_ok=True)
    for date_value, group in df.groupby(df["reference_date"].dt.strftime("%Y-%m-%d")):
        group.to_csv(partitioned_dir / f"reference_date={date_value}.csv", index=False)

    payload = {
        "row_count": int(len(df)),
        "min_reference_date": str(df["reference_date"].min().date()),
        "max_reference_date": str(df["reference_date"].max().date()),
        "alerts": alerts,
    }
    quality_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
