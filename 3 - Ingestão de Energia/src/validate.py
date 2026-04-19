from __future__ import annotations

import pandas as pd

from config import EXPECTED_COLUMNS


def validate_schema(df: pd.DataFrame) -> None:
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")


def validate_quality(df: pd.DataFrame) -> list[str]:
    alerts: list[str] = []

    if df["reference_date"].isna().any():
        raise ValueError("Há datas inválidas na coluna reference_date.")

    if df["value_mwmed"].isna().any():
        raise ValueError("Há valores numéricos inválidos em value_mwmed.")

    if (df["value_mwmed"] < 0).any():
        raise ValueError("Foram encontrados valores negativos em value_mwmed.")

    duplicated_keys = df["natural_key"].duplicated().sum()
    if duplicated_keys > 0:
        raise ValueError(f"Foram encontradas {duplicated_keys} chaves naturais duplicadas.")

    zero_count = int((df["value_mwmed"] == 0).sum())
    if zero_count > 0:
        alerts.append(f"{zero_count} registro(s) com value_mwmed igual a zero.")

    null_subsystems = int((df["subsystem"].astype(str).str.len() == 0).sum())
    if null_subsystems > 0:
        raise ValueError("Há registros com subsystem vazio.")

    return alerts
