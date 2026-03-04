from __future__ import annotations

import re
import pandas as pd
import warnings


_ORDINAL_SUFFIX = re.compile(r"(\d+)(st|nd|rd|th)\b", flags=re.IGNORECASE)


def _clean_date_text(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return pd.NA
    if not isinstance(x, str):
        x = str(x)

    t = x.strip()
    if t == "":
        return pd.NA

    # Remove trailing markers found in P6 exports
    # e.g. "05-12-19 A", "29-01-21*"
    t = t.replace(" A", "").replace("A", "") if t.endswith(" A") else t
    t = t[:-1] if t.endswith("*") else t
    t = t.strip()

    # Normalize ordinal dates: "5th Jan 1987" -> "5 Jan 1987"
    t = _ORDINAL_SUFFIX.sub(r"\1", t)

    return t

    # def parse_date_series(series: pd.Series, dayfirst: bool = True) -> pd.Series:
    """
   # Clean and parse dates. Returns datetime64[ns] with NaT for blanks/unparseable.
    """
    # cleaned = series.apply(_clean_date_text)
    # Parse
    # with warnings.catch_warnings():
    # warnings.simplefilter("ignore", UserWarning)
    # dt = pd.to_datetime(cleaned, errors="coerce", dayfirst=True)
    # return dt


def parse_date_series(series: pd.Series, dayfirst: bool = True) -> pd.Series:
    cleaned = series.apply(_clean_date_text)

    # If a value already looks like ISO datetime (YYYY-MM-DD ...),
    # pandas warns when dayfirst=True is set. So we parse flexibly
    # without forcing dayfirst on those rows.
    iso_like = cleaned.astype("string").str.match(r"^\d{4}-\d{2}-\d{2}")

    out = pd.Series(pd.NaT, index=cleaned.index, dtype="datetime64[ns]")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)

        # Parse ISO-like without dayfirst
        if iso_like.any():
            out.loc[iso_like] = pd.to_datetime(
                cleaned.loc[iso_like], errors="coerce", dayfirst=False
            )

        # Parse the rest with dayfirst preference
        if (~iso_like).any():
            out.loc[~iso_like] = pd.to_datetime(
                cleaned.loc[~iso_like], errors="coerce", dayfirst=dayfirst
            )

    return out
