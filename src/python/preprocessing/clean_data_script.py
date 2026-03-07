"""Clean the diabetic dataset and save the processed CSV."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetic_data.csv"
COOKED_DIR = PROJECT_ROOT / "data" / "cooked"
OUTPUT_PATH = COOKED_DIR / "clean_data.csv"

ADMISSION_SOURCE_NULL_VALS = [9, 15, 17, 20, 21]
ADMISSION_TYPE_NULL_VALS = [5, 6, 8]
DISCHARGE_DISPOSITION_NULL_VALS = [18, 25, 26]

MED_COLS = [
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "examide",
    "citoglipton",
    "insulin",
    "glyburide-metformin",
    "glipizide-metformin",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
    "metformin-pioglitazone",
]


def clean_data(input_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Apply the cleaning steps from clean.ipynb to the raw diabetic dataset."""
    data = pd.read_csv(input_path)

    # The notebook inspects the dropped frame, so preserve that intended result.
    data = data.drop(columns=["encounter_id"])

    data["weight"] = data["weight"] != "?"
    data["admission_source_id"] = ~data["admission_source_id"].isin(
        ADMISSION_SOURCE_NULL_VALS
    )
    data["admission_type_id"] = ~data["admission_type_id"].isin(
        ADMISSION_TYPE_NULL_VALS
    )
    data["discharge_disposition_id"] = ~data["discharge_disposition_id"].isin(
        DISCHARGE_DISPOSITION_NULL_VALS
    )

    data["payer_code"] = data["payer_code"].replace("?", "unknown").astype("category")
    data["medical_specialty"] = (
        data["medical_specialty"].replace("?", "unknown").astype("category")
    )
    data[["diag_1", "diag_2", "diag_3"]] = data[["diag_1", "diag_2", "diag_3"]].astype(
        "category"
    )
    data[["max_glu_serum", "A1Cresult"]] = (
        data[["max_glu_serum", "A1Cresult"]].fillna("unknown").astype("category")
    )
    data[MED_COLS] = data[MED_COLS].astype("category")
    data[["change", "diabetesMed"]] = data[["change", "diabetesMed"]].astype(
        "category"
    )
    data["readmitted"] = data["readmitted"] == "<30"

    return data


def save_clean_data(output_path: Path = OUTPUT_PATH) -> Path:
    """Save the cleaned diabetic dataset to data/cooked/clean_data.csv."""
    COOKED_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_data = clean_data()
    cleaned_data.to_csv(output_path, index=False)
    print(f"Saved {output_path}")

    return output_path


if __name__ == "__main__":
    save_clean_data()
