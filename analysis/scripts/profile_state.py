#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS_DIR))

from src.checks import basic_profile, duplicate_logical_rows
from src.load_data import read_state_csv, normalize_state_code
from src.summarize import registration_rows, statewide_candidate_totals


DEFAULT_OFFICES = ["US SENATE", "GOVERNOR", "US HOUSE"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile one MEDSL state results file.")
    parser.add_argument("state", help="Two-letter state abbreviation, for example: fl")
    parser.add_argument(
        "--top",
        type=int,
        default=12,
        help="Number of top offices/counties/candidates to print.",
    )
    return parser.parse_args()


def print_mapping(title: str, values: dict[object, object]) -> None:
    print(f"\n{title}")
    for key, value in values.items():
        print(f"  {key}: {value}")


def main() -> int:
    args = parse_args()
    state = normalize_state_code(args.state)
    df = read_state_csv(state)

    profile = basic_profile(df)
    source_zip = df.attrs.get("source_zip", "unknown")
    source_csv = df.attrs.get("source_csv", "unknown")

    print(f"State: {state.upper()}")
    print(f"Source ZIP: {source_zip}")
    print(f"Source CSV: {source_csv}")
    print(f"Rows: {profile['rows']:,}")
    print(f"Columns: {len(profile['columns'])}")
    print(f"Unique counties: {profile['unique_counties']:,}")
    print(f"Unique county-precincts: {profile['unique_precincts']:,}")
    print(f"Unique offices: {profile['unique_offices']:,}")
    print(f"Blank office rows: {profile['blank_office_rows']:,}")

    print_mapping("Modes", profile["modes"])
    print_mapping("Years", profile["years"])
    print_mapping("Stages", profile["stages"])

    print("\nTop offices by row count")
    print(df["office"].fillna("").value_counts().head(args.top).to_string())

    print("\nTop counties by row count")
    print(df["county_name"].value_counts().head(args.top).to_string())

    duplicate_rows = duplicate_logical_rows(df)
    print(f"\nDuplicate logical rows: {len(duplicate_rows):,}")

    registration = registration_rows(df)
    if not registration.empty:
        print("\nRegistration metadata rows")
        print(registration["candidate"].value_counts().head(args.top).to_string())

    candidate_totals = statewide_candidate_totals(df, DEFAULT_OFFICES)
    print("\nSelected candidate totals")
    print(candidate_totals.head(args.top * 2).to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

