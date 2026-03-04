from pathlib import Path

# Base project directory (current folder)
BASE_DIR = Path(__file__).parent

# Folders to create
folders = [
    "data_raw",
    "data_processed",
    "src",
    "src/config",
    "src/cleaners",
    "src/pipelines",
    "src/utils",
]

# Files to create
files = [
    "run.py",
    "requirements.txt",
    ".gitignore",
    "README.md",
    "src/config/activity_mapping.py",
    "src/config/project_mapping.py",
    "src/config/settings.py",
    "src/cleaners/header_cleaner.py",
    "src/cleaners/date_cleaner.py",
    "src/cleaners/duration_cleaner.py",
    "src/cleaners/percent_cleaner.py",
    "src/cleaners/boolean_cleaner.py",
    "src/cleaners/text_cleaner.py",
    "src/pipelines/clean_activities.py",
    "src/pipelines/clean_projects.py",
    "src/utils/io.py",
    "src/utils/logger.py",
]


def create_structure():
    # Create folders
    for folder in folders:
        path = BASE_DIR / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {path}")

    # Create files
    for file in files:
        path = BASE_DIR / file
        path.touch(exist_ok=True)
        print(f"Created file: {path}")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    create_structure()
