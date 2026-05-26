from __future__ import annotations

import pandas as pd


LOGICAL_ROW_KEY = [
    "county_name",
    "precinct",
    "office",
    "district",
    "candidate",
    "party_simplified",
    "mode",
]


def basic_profile(df: pd.DataFrame) -> dict[str, object]:
    """Return high-level profile values for a state results dataframe."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "unique_counties": df["county_name"].nunique(dropna=False),
        "unique_precincts": df[["county_name", "precinct"]].drop_duplicates().shape[0],
        "unique_offices": df["office"].nunique(dropna=False),
        "modes": df["mode"].value_counts(dropna=False).to_dict(),
        "years": df["year"].value_counts(dropna=False).to_dict(),
        "stages": df["stage"].value_counts(dropna=False).to_dict(),
        "blank_office_rows": int(df["office"].fillna("").eq("").sum()),
    }


def duplicate_logical_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return logical duplicate rows, if any, with duplicate counts."""
    key = [column for column in LOGICAL_ROW_KEY if column in df.columns]
    counts = df.groupby(key, dropna=False).size().reset_index(name="row_count")
    return counts[counts["row_count"] > 1].sort_values("row_count", ascending=False)

