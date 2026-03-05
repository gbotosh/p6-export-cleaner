from __future__ import annotations

import re
import pandas as pd
from dateutil import parser

# 5th -> 5, 21st -> 21, etc.
_ORDINAL_SUFFIX = re.compile(r"(\d+)(st|nd|rd|th)\b", flags=re.IGNORECASE)

# ISO-like date/datetime starts with YYYY-MM-DD (or YYYY/MM/DD sometimes)
_ISO_LIKE = re.compile(r"^\d{4}[-/]\d{2}[-/]\d{2}")

# Insert spaces where people sometimes have "5thJan2025" or "5Jan2025"
# digit<->letter boundaries
_DIGIT_LETTER_BOUNDARY = re.compile(r"(?<=\d)(?=[A-Za-z])|(?<=[A-Za-z])(?=\d)")

_COMMAS = re.compile(r",")


def _clean_date_text(x) -> str | pd._libs.missing.NAType:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return pd.NA

    # If Excel already gave us a datetime, keep it
    if isinstance(x, pd.Timestamp):
        return x.isoformat(sep=" ")

    s = str(x).strip()
    if s == "":
        return pd.NA

    # Normalize non-breaking spaces
    s = s.replace("\u00a0", " ").strip()

    # Remove trailing markers (only if at end)
    # e.g. "05-12-2019 A" , "29-01-2021*"
    if s.endswith(" A"):
        s = s[:-2].strip()
    if s.endswith("*"):
        s = s[:-1].strip()

    # Remove commas: "Jan 5, 2025" -> "Jan 5 2025"
    s = _COMMAS.sub("", s).strip()

    # Convert ordinals: "5th Jan 2025" -> "5 Jan 2025"
    s = _ORDINAL_SUFFIX.sub(r"\1", s).strip()

    # Handle stuck-together forms like "5Jan2025" / "5thJan2025"
    s = _DIGIT_LETTER_BOUNDARY.sub(" ", s)

    # Collapse multiple spaces
    s = re.sub(r"\s+", " ", s).strip()

    return s


def _parse_one_date(value: str, dayfirst: bool) -> pd.Timestamp | pd.NaT:
    """
    Robust parse using dateutil with fuzzy matching.
    """
    try:
        dt = parser.parse(value, dayfirst=dayfirst, fuzzy=True)
        return pd.Timestamp(dt)
    except Exception:
        return pd.NaT


def parse_date_series(series: pd.Series, dayfirst: bool = True) -> pd.Series:
    """
    Clean and parse date columns into pandas datetime64[ns].

    Strategy:
    1) Clean text (remove A/*, ordinals, commas, weird spacing)
    2) Parse ISO-like values with pandas quickly
    3) Parse everything else with dateutil.parser.parse(fuzzy=True)
    """
    cleaned = series.apply(_clean_date_text)

    # Prepare output
    out = pd.Series(pd.NaT, index=cleaned.index, dtype="datetime64[ns]")

    cleaned_str = cleaned.astype("string")

    # ISO-like parse (fast and unambiguous)
    iso_mask = cleaned_str.str.match(_ISO_LIKE)

    if iso_mask.any():
        out.loc[iso_mask] = pd.to_datetime(
            cleaned.loc[iso_mask],
            errors="coerce",
            dayfirst=False,
        )

    # Everything else: robust dateutil parse
    other_mask = ~iso_mask
    if other_mask.any():
        out.loc[other_mask] = cleaned.loc[other_mask].apply(
            lambda v: (
                _parse_one_date(v, dayfirst=dayfirst) if isinstance(v, str) else pd.NaT
            )
        )

    return out
