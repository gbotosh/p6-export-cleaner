from __future__ import annotations

from pathlib import Path
import pandas as pd


def read_excel(file_path: str) -> pd.DataFrame:
    """
    Read an Excel file into a DataFrame.
    - Reads the first sheet by default.
    - Keeps empty cells as NaN.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    # dtype=str keeps everything as text initially (best for cleaning),
    # we will convert types later (dates/numbers/bools).
    df = pd.read_excel(path, sheet_name=0, dtype=str, engine="openpyxl")

    return df


def save_parquet(df: pd.DataFrame, out_path: str) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"Saved: {path}")


def save_csv(df: pd.DataFrame, out_path: str) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Saved: {path}")


from pathlib import Path
import pandas as pd


def save_xlsx_text_id(df: pd.DataFrame, out_path: str, text_cols: list[str]) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="cleaned")

        ws = writer.book["cleaned"]
        headers = [cell.value for cell in ws[1]]

        # Force text columns
        for col in text_cols:
            if col in headers:
                idx = headers.index(col) + 1
                for r in range(2, ws.max_row + 1):
                    ws.cell(r, idx).number_format = "@"

        # Automatically format datetime columns
        datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns

        for col in datetime_cols:
            if col in headers:
                idx = headers.index(col) + 1
                for r in range(2, ws.max_row + 1):
                    ws.cell(r, idx).number_format = "DD/MM/YYYY"

    print(f"Saved: {out_path}")
