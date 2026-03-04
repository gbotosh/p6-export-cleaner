from __future__ import annotations

import pandas as pd


def yes_no_to_bool(series: pd.Series) -> pd.Series:
    """
    Convert Yes/No (case-insensitive) to True/False.
    Leaves other values as-is (or NaN).
    """

    def conv(x):
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return x
        if isinstance(x, str):
            t = x.strip().lower()
            if t == "yes":
                return True
            if t == "no":
                return False
        return x

    return series.apply(conv)
