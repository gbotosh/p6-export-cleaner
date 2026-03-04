from __future__ import annotations

from src.utils.io import read_excel
from src.cleaners.header_cleaner import standardize_headers, apply_mapping
from src.cleaners.text_cleaner import trim_all_strings
from src.cleaners.boolean_cleaner import yes_no_to_bool
from src.cleaners.percent_cleaner import normalize_percent
from src.config.activity_mapping import ACTIVITY_MAPPING
from src.cleaners.date_cleaner import parse_date_series
from src.cleaners.duration_cleaner import to_float_days
from src.cleaners.id_cleaner import force_id_text
from src.utils.io import save_parquet, save_csv

DATE_COLS = [
    "actual_start",
    "actual_finish",
    "start",
    "finish",
    "baseline_project_start",
    "baseline_project_finish",
    "bl1_start",
    "bl1_finish",
    "bl2_start",
    "bl2_finish",
    "bl3_start",
    "bl3_finish",
    "primary_constraint_date",
]

NUM_DAY_COLS = [
    "original_duration_days",
    "remaining_duration_days",
    "at_completion_duration_days",
    "total_float_days",
    "free_float_days",
]
PERCENT_COLS = [
    "activity_percent_complete",
    "duration_percent_complete",
    "physical_percent_complete",
    "units_percent_complete",
    "schedule_percent_complete",
    "performance_percent_complete",
    "performance_percent_complete_l",
]


def clean_activities(file_path: str) -> None:
    df = read_excel(file_path)

    # Step 13: headers + mapping
    df = standardize_headers(df)
    df = apply_mapping(df, ACTIVITY_MAPPING)

    # Step 14: trim text
    df = trim_all_strings(df)

    # Step 14: booleans
    if "critical_flag" in df.columns:
        df["critical_flag"] = yes_no_to_bool(df["critical_flag"])
    if "longest_path_flag" in df.columns:
        df["longest_path_flag"] = yes_no_to_bool(df["longest_path_flag"])

    # Step 14: percent columns
    for c in PERCENT_COLS:
        if c in df.columns:
            df[c] = normalize_percent(df[c])

    print("===================================")
    print("[activities] step 14 complete (trim + bool + percent)")
    # print(df.head(3).to_string(index=False))

    # Step 15: dates
    for c in DATE_COLS:
        if c in df.columns:
            df[c] = parse_date_series(df[c], dayfirst=True)

    # Step 15: numeric days
    for c in NUM_DAY_COLS:
        if c in df.columns:
            df[c] = to_float_days(df[c])

    # Step 16: IDs as text (protect against Excel damage)
    if "activity_id" in df.columns:
        df["activity_id"] = force_id_text(df["activity_id"])
    if "project_id" in df.columns:
        df["project_id"] = force_id_text(df["project_id"])

    # Save outputs
    # Step 16: IDs as text
    if "activity_id" in df.columns:
        df["activity_id"] = force_id_text(df["activity_id"])
    if "project_id" in df.columns:
        df["project_id"] = force_id_text(df["project_id"])

    # Build dynamic output name
    from pathlib import Path

    input_path = Path(file_path)
    base_name = input_path.stem  # file name without extension

    out_csv = f"data_processed/{base_name}_cleaned.csv"
    out_parquet = f"data_processed/{base_name}_cleaned.parquet"

    if "activity_id" in df.columns:
        df["activity_id"] = df["activity_id"].astype(str)

    save_parquet(df, out_parquet)
    save_csv(df, out_csv)

    from src.utils.io import save_xlsx_text_id

    out_xlsx = f"data_processed/{base_name}_cleaned.xlsx"
    save_xlsx_text_id(df, out_xlsx, text_cols=["activity_id"])
    print("✅ [activities] done")
