from __future__ import annotations

from src.utils.io import read_excel
from src.cleaners.header_cleaner import standardize_headers, apply_mapping
from src.config.project_mapping import PROJECT_MAPPING
from src.cleaners.id_cleaner import force_id_text
from src.utils.io import save_parquet, save_csv
from src.utils.io import save_parquet, save_csv, save_xlsx_text_id


def clean_projects(file_path: str) -> None:
    df = read_excel(file_path)

    df = standardize_headers(df)
    df = apply_mapping(df, PROJECT_MAPPING)

    print("===================================")
    print("[projects] headers standardized + mapped")
    print(f"Rows: {len(df):,}")
    print(f"Cols: {len(df.columns):,}")
    print("Columns after mapping:")
    for c in df.columns:
        print(f" - {c}")

    if "project_id" in df.columns:
        df["project_id"] = force_id_text(df["project_id"])

    if "project_id" in df.columns:
        df["project_id"] = force_id_text(df["project_id"])

    from pathlib import Path

    input_path = Path(file_path)
    base_name = input_path.stem

    out_csv = f"data_processed/{base_name}_cleaned.csv"
    out_parquet = f"data_processed/{base_name}_cleaned.parquet"

    out_xlsx = f"data_processed/{base_name}_cleaned.xlsx"

    save_parquet(df, out_parquet)
    save_csv(df, out_csv)

    # Save Excel with project_id forced to Text
    save_xlsx_text_id(df, out_xlsx, text_cols=["project_id"])

    print("✅ [projects] done")
