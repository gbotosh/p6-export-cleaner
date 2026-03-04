from __future__ import annotations

import re
from typing import Dict
import pandas as pd


def to_snake_case(text: str) -> str:
    """
    Convert a column name to snake_case:
    - lower
    - replace non-alphanumeric with underscore
    - collapse multiple underscores
    - trim underscores
    """
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def standardize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [to_snake_case(c) for c in df.columns]
    return df


def apply_mapping(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    mapping keys should be snake_case versions of P6 headers.
    Only renames columns that exist.
    """
    df = df.copy()
    rename_dict = {k: v for k, v in mapping.items() if k in df.columns}
    return df.rename(columns=rename_dict)
