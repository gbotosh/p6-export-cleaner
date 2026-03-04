import argparse
from pathlib import Path

from src.pipelines.clean_activities import clean_activities
from src.pipelines.clean_projects import clean_projects


def main() -> None:
    parser = argparse.ArgumentParser(description="P6 Export Cleaning Tool")

    parser.add_argument(
        "--type",
        required=True,
        choices=["activities", "projects"],
        help="Type of export to clean",
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the Excel file",
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if args.type == "activities":
        clean_activities(str(file_path))
    else:
        clean_projects(str(file_path))


if __name__ == "__main__":
    main()
