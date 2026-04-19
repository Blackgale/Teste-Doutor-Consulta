from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EXPECTED_COLUMNS = {
    "reference_date": "datetime64[ns]",
    "subsystem": "object",
    "metric_type": "object",
    "value_mwmed": "float64",
    "source": "object",
}

CANONICAL_COLUMN_MAP = {
    "data": "reference_date",
    "date": "reference_date",
    "dt_referencia": "reference_date",
    "subsistema": "subsystem",
    "subsystem": "subsystem",
    "tipo_metrica": "metric_type",
    "metric_type": "metric_type",
    "valor": "value_mwmed",
    "value": "value_mwmed",
    "valor_mwmed": "value_mwmed",
    "fonte": "source",
    "source": "source",
}


@dataclass(frozen=True)
class RunConfig:
    input_path: Path
    output_dir: Path
