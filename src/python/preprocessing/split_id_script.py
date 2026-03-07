"""Preprocessing scripts for medical datathon data."""

import csv
from pathlib import Path

# Paths (data is in data/ relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
COOKED_DIR = PROJECT_ROOT / "data" / "cooked"
IDS_MAPPING_PATH = RAW_DIR / "IDS_mapping.csv"


def split_ids_mapping() -> None:
    """Read IDS_mapping.csv and save as 3 separate mapping CSVs in data/cooked."""
    COOKED_DIR.mkdir(parents=True, exist_ok=True)

    with open(IDS_MAPPING_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Split by empty rows; each section starts with a header
    sections = []
    current_section = []

    for row in rows:
        if not row or all(cell.strip() == "" for cell in row):
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            current_section.append(row)

    if current_section:
        sections.append(current_section)

    # Map section headers to output filenames
    output_mapping = {
        "admission_type_id": "admission_type_id_mapping.csv",
        "discharge_disposition_id": "discharge_disposition_id_mapping.csv",
        "admission_source_id": "admission_source_id_mapping.csv",
    }

    for section in sections:
        if not section:
            continue
        header = section[0]
        first_col = header[0].strip() if header else ""
        filename = output_mapping.get(first_col)
        if filename:
            output_path = COOKED_DIR / filename
            with open(output_path, "w", newline="", encoding="utf-8") as out:
                writer = csv.writer(out)
                writer.writerows(section)
            print(f"Saved {output_path}")


if __name__ == "__main__":
    split_ids_mapping()
