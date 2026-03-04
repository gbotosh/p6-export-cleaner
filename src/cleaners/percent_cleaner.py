from __future__ import annotations

import pandas as pd


def normalize_percent(series: pd.Series) -> pd.Series:
    """
    Normalize percent values to 0–100 float.
    Handles:
    - "50%" -> 50
    - "0.45" -> 45
    - "45" -> 45
    - 0.45 -> 45
    Leaves blanks/NaN as NaN.
    """

    def conv(x):
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return pd.NA

        if isinstance(x, str):
            t = x.strip()
            if t == "":
                return pd.NA
            if t.endswith("%"):
                t = t[:-1].strip()

            # try parse number
            try:
                val = float(t)
            except ValueError:
                return pd.NA
        else:
            try:
                val = float(x)
            except Exception:
                return pd.NA

        # If 0–1 scale, convert to 0–100
        if 0 <= val <= 1:
            val = val * 100

        return float(val)

    return series.apply(conv)
