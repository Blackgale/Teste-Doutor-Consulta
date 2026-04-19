from __future__ import annotations

import pandas as pd

from config import CANONICAL_COLUMN_MAP


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(col).strip().lower() for col in cleaned.columns]
    cleaned = cleaned.rename(columns={col: CANONICAL_COLUMN_MAP.get(col, col) for col in cleaned.columns})
    return cleaned


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    transformed = standardize_columns(df)

    transformed["reference_date"] = pd.to_datetime(transformed["reference_date"], errors="coerce")
    transformed["subsystem"] = transformed["subsystem"].astype(str).str.strip().str.upper()
    transformed["metric_type"] = transformed["metric_type"].astype(str).str.strip().str.lower()
    transformed["source"] = transformed["source"].astype(str).str.strip().str.upper()
    transformed["value_mwmed"] = pd.to_numeric(transformed["value_mwmed"], errors="coerce")

    transformed["ingestion_timestamp"] = pd.Timestamp.utcnow()
    transformed["natural_key"] = (
        transformed["reference_date"].dt.strftime("%Y-%m-%d")
        + "|"
        + transformed["subsystem"]
        + "|"
        + transformed["metric_type"]
    )

    return transformed
