"""
src/data_loader.py
------------------
Responsible for reading the raw CSV and renaming columns to
project-standard names. Supports both a local file path and
an in-memory uploaded file (Streamlit UploadedFile).
"""
import pandas as pd
import io


# ── Fuzzy column matching: maps lowercased keywords → standard name ────────
# This handles asterisks, extra spaces, casing differences, and minor
# wording variations across CSV exports without breaking on deployment.
FUZZY_MAP: list[tuple[str, str]] = [
    ("apprehended",    "CBP_Apprehensions"),
    ("cbp custody",    "CBP_In_Custody"),
    ("transferred out","CBP_Transfers_Out"),
    ("in hhs care",    "HHS_In_Care"),
    ("discharged",     "HHS_Discharges"),
]

REQUIRED_STANDARD: list[str] = [
    "Date",
    "CBP_Apprehensions",
    "CBP_Transfers_Out",
    "HHS_In_Care",
    "HHS_Discharges",
]


def load_data(filepath) -> pd.DataFrame:
    """
    Load dataset from a local file path (str or Path).

    Parameters
    ----------
    filepath : str | Path
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with columns renamed to project standard.
    """
    df = pd.read_csv(filepath, encoding="utf-8")
    return _rename_and_validate(df)


def load_data_from_upload(uploaded_file) -> pd.DataFrame:
    """
    Load dataset from a Streamlit UploadedFile object.

    Parameters
    ----------
    uploaded_file : streamlit.runtime.uploaded_file_manager.UploadedFile

    Returns
    -------
    pd.DataFrame
        Raw dataframe with columns renamed to project standard.
    """
    content = uploaded_file.read()
    df = pd.read_csv(io.BytesIO(content), encoding="utf-8")
    return _rename_and_validate(df)


def _fuzzy_rename(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns using fuzzy keyword matching instead of exact strings.
    Handles asterisks, casing, extra whitespace, and minor wording changes.
    """
    rename_map = {}
    for col in df.columns:
        col_lower = col.lower().strip()
        for keyword, standard_name in FUZZY_MAP:
            if keyword in col_lower and standard_name not in rename_map.values():
                rename_map[col] = standard_name
                break  # first match wins — move to next column
    return df.rename(columns=rename_map)


def _rename_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Internal helper: strip whitespace, fuzzy-rename columns,
    validate required fields exist, and warn (not crash) on missing ones.
    """
    # 1. Strip whitespace from all column names
    df.columns = df.columns.str.strip()

    # 2. Normalise Date column casing (some exports use 'date' lowercase)
    date_candidates = [c for c in df.columns if c.lower() == "date"]
    if date_candidates and date_candidates[0] != "Date":
        df = df.rename(columns={date_candidates[0]: "Date"})

    # 3. Fuzzy rename — tolerates asterisks, casing, minor wording drift
    df = _fuzzy_rename(df)

    # 4. Warn on missing columns instead of hard-crashing
    #    This lets the dashboard load partially rather than showing blank page
    missing = [c for c in REQUIRED_STANDARD if c not in df.columns]
    if missing:
        import warnings
        warnings.warn(
            f"[data_loader] Missing expected columns after rename: {missing}\n"
            f"Available columns: {list(df.columns)}\n"
            f"Some charts may not render correctly.",
            UserWarning,
            stacklevel=2,
        )

    return df