from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE_TEMPLATE = "2022-{state}-local-precinct-general.zip"


def normalize_state_code(state: str) -> str:
    """Return a lowercase two-letter state code."""
    state_code = state.strip().lower()
    if len(state_code) != 2 or not state_code.isalpha():
        raise ValueError("State must be a two-letter postal abbreviation, like 'fl'.")
    return state_code


def state_zip_path(state: str, repo_root: Path | None = None) -> Path:
    """Return the official ZIP path for a state."""
    state_code = normalize_state_code(state)
    root = repo_root or REPO_ROOT
    return root / "individual_states" / STATE_FILE_TEMPLATE.format(state=state_code)


def state_csv_name(zip_path: Path) -> str:
    """Return the CSV filename inside a state ZIP archive."""
    with ZipFile(zip_path) as archive:
        csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]

    if len(csv_names) != 1:
        raise ValueError(f"Expected one CSV in {zip_path}, found {len(csv_names)}.")
    return csv_names[0]


def read_state_csv(state: str, repo_root: Path | None = None) -> pd.DataFrame:
    """Read a state CSV from its official ZIP archive."""
    zip_path = state_zip_path(state, repo_root=repo_root)
    if not zip_path.exists():
        raise FileNotFoundError(f"State file not found: {zip_path}")

    csv_name = state_csv_name(zip_path)
    df = pd.read_csv(zip_path, compression="zip", dtype=str, keep_default_na=False)
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype("int64")
    df.attrs["source_zip"] = str(zip_path)
    df.attrs["source_csv"] = csv_name
    return df
