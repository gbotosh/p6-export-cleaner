from __future__ import annotations

import pandas as pd


def trim_all_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim leading/trailing spaces for all string cells.
    Leaves NaN as NaN.
    """
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    return df
