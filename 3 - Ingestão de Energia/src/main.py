from __future__ import annotations

import argparse
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from config import RunConfig
from extract import extract_data
from transform import transform_data
from validate import validate_schema, validate_quality
from load import load_data


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="Pipeline simples de ingestão de energia")
    parser.add_argument("--input", required=True, help="Caminho para o arquivo de entrada")
    parser.add_argument("--output-dir", required=True, help="Diretório onde a saída será gravada")
    args = parser.parse_args()
    return RunConfig(input_path=Path(args.input), output_dir=Path(args.output_dir))


def main() -> None:
    config = parse_args()
    df_raw = extract_data(config.input_path)
    df = transform_data(df_raw)
    validate_schema(df)
    alerts = validate_quality(df)
    load_data(df, config.output_dir, alerts)

    print("Execução concluída com sucesso.")
    if alerts:
        print("Alertas de qualidade:")
        for alert in alerts:
            print(f"- {alert}")


if __name__ == "__main__":
    main()
