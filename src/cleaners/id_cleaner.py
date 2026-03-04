from __future__ import annotations

import pandas as pd


def force_id_text(series: pd.Series) -> pd.Series:
    """
    Force ID column to text and fix Excel float artifacts like '2000.0' -> '2000'.
    """

    def conv(x):
        if pd.isna(x):
            return ""

        s = str(x).strip()

        # Remove Excel float artifact
        if s.endswith(".0"):
            s = s[:-2]

        return s

    return series.apply(conv).astype("string")
