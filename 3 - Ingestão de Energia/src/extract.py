from __future__ import annotations

from pathlib import Path
import json
import xml.etree.ElementTree as ET

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _read_json(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if isinstance(payload, dict):
        # aceita {"data": [...]} ou estrutura similar
        for value in payload.values():
            if isinstance(value, list):
                return pd.DataFrame(value)
    return pd.DataFrame(payload)


def _read_xml(path: Path) -> pd.DataFrame:
    tree = ET.parse(path)
    root = tree.getroot()
    records = []
    for item in root.findall(".//record"):
        records.append({child.tag: child.text for child in item})
    if not records:
        # fallback: tenta usar qualquer nó filho homogêneo
        for parent in root:
            if list(parent):
                records.append({child.tag: child.text for child in parent})
    return pd.DataFrame(records)


def extract_data(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _read_csv(path)
    if suffix == ".json":
        return _read_json(path)
    if suffix == ".xml":
        return _read_xml(path)

    raise ValueError(f"Formato não suportado: {suffix}")
