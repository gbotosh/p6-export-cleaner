from __future__ import annotations

import re
import pandas as pd

# Extract the first number found in a string:
# "10d" -> 10
# "10 days" -> 10
# " 15 d " -> 15
# "5.5days" -> 5.5
# "-2 days" -> -2
_FIRST_NUMBER = re.compile(r"[-+]?\d*\.?\d+")


def to_float_days(series: pd.Series) -> pd.Series:
    """
    Convert duration/float columns to numeric days.

    Works with values like:
    - "10d"
    - "10 days"
    - " 15 d "
    - "5.5days"
    - "-3"
    - 12

    Returns pandas.NA for blanks or unparseable values.
    """

    def conv(x):
        # Keep missing values as NA
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return pd.NA

        # Convert to string and trim spaces
        s = str(x).strip()
        if s == "":
            return pd.NA

        # Normalize odd spaces and remove commas
        s = s.replace("\u00a0", " ")  # non-breaking space
        s = s.replace(",", "")

        # Find the first numeric value
        m = _FIRST_NUMBER.search(s)
        if not m:
            return pd.NA

        try:
            return float(m.group(0))
        except ValueError:
            return pd.NA

    return series.apply(conv)
