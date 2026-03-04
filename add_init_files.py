from pathlib import Path

BASE_DIR = Path(__file__).parent

init_folders = [
    "src",
    "src/config",
    "src/cleaners",
    "src/pipelines",
    "src/utils",
]

for folder in init_folders:
    init_file = BASE_DIR / folder / "__init__.py"
    init_file.touch(exist_ok=True)
    print(f"Created: {init_file}")

print("\n__init__.py files added!")
