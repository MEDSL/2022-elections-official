from __future__ import annotations

import pandas as pd


SPECIAL_CANDIDATES = {"UNDERVOTES", "OVERVOTES"}


def election_result_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows that represent contests, excluding registration metadata rows."""
    return df[df["office"].fillna("").ne("")].copy()


def registration_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows that represent registration metadata."""
    return df[df["office"].fillna("").eq("")].copy()


def statewide_candidate_totals(
    df: pd.DataFrame,
    offices: list[str] | None = None,
    include_special_candidates: bool = False,
) -> pd.DataFrame:
    """Summarize statewide candidate totals by office, district, candidate, and party."""
    filtered = election_result_rows(df)

    if offices:
        filtered = filtered[filtered["office"].isin(offices)]

    if not include_special_candidates:
        filtered = filtered[~filtered["candidate"].isin(SPECIAL_CANDIDATES)]

    group_cols = ["office", "district", "candidate", "party_simplified"]
    return (
        filtered.groupby(group_cols, dropna=False, as_index=False)["votes"]
        .sum()
        .sort_values(group_cols[:2] + ["votes"], ascending=[True, True, False])
    )


def county_party_totals(df: pd.DataFrame, offices: list[str] | None = None) -> pd.DataFrame:
    """Summarize county-level party totals for selected offices."""
    filtered = election_result_rows(df)

    if offices:
        filtered = filtered[filtered["office"].isin(offices)]

    group_cols = ["county_name", "office", "district", "party_simplified"]
    return (
        filtered.groupby(group_cols, dropna=False, as_index=False)["votes"]
        .sum()
        .sort_values(["county_name", "office", "district", "votes"], ascending=[True, True, True, False])
    )

