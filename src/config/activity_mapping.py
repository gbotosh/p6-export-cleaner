# Keys = standardized (snake_case) version of P6 headers
# Values = cleaned schema names

ACTIVITY_MAPPING = {
    # IDs / WBS
    "project_id": "project_id",
    "project_name": "project_name",
    "activity_id": "activity_id",
    "activity_name": "activity_name",
    "wbs": "wbs_code",
    "wbs_path": "wbs_path",
    "wbs_name": "wbs_name",
    "wbs_category": "wbs_category",
    # Dates
    "start": "start",
    "finish": "finish",
    "actual_start": "actual_start",
    "actual_finish": "actual_finish",
    "bl_project_start": "baseline_project_start",
    "bl_project_finish": "baseline_project_finish",
    "bl1_start": "bl1_start",
    "bl1_finish": "bl1_finish",
    "bl2_start": "bl2_start",
    "bl2_finish": "bl2_finish",
    "bl3_start": "bl3_start",
    "bl3_finish": "bl3_finish",
    "primary_constraint_date": "primary_constraint_date",
    # Durations / float (days)
    "original_duration": "original_duration_days",
    "remaining_duration": "remaining_duration_days",
    "at_completion_duration": "at_completion_duration_days",
    "total_float": "total_float_days",
    "free_float": "free_float_days",
    # Progress
    "percent_complete_type": "percent_complete_type",
    "activity_complete": "activity_percent_complete",  # handles "Activity % Complete" -> activity_complete
    "duration_complete": "duration_percent_complete",  # "Duration % Complete"
    "physical_complete": "physical_percent_complete",  # "Physical % Complete"
    "units_complete": "units_percent_complete",  # "Units % Complete"
    "schedule_complete": "schedule_percent_complete",  # "Schedule % Complete"
    "performance_complete": "performance_percent_complete",  # "Performance % Complete"
    "performance_complete_l": "performance_percent_complete_l",  # "Performance % Complete - L"
    # Flags / constraint type
    "critical": "critical_flag",
    "longest_path": "longest_path_flag",
    "primary_constraint": "primary_constraint_type",
    # Logic / resources
    "predecessors": "predecessors_raw",
    "predecessor_details": "predecessor_details_raw",
    "successors": "successors_raw",
    "successor_details": "successor_details_raw",
    "resource_ids": "resource_ids_raw",
}
