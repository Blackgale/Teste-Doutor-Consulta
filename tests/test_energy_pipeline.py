from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "03_energy_ingestion" / "src"
sys.path.insert(0, str(ROOT))

from extract import extract_data
from transform import transform_data
from validate import validate_schema, validate_quality


def test_pipeline_happy_path():
    data_path = Path(__file__).resolve().parents[1] / "03_energy_ingestion" / "data" / "sample_energy.csv"
    df = extract_data(data_path)
    df = transform_data(df)
    validate_schema(df)
    alerts = validate_quality(df)
    assert len(df) == 9
    assert alerts
