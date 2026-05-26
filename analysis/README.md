# Election Analysis Workspace

This folder contains analysis code and notes built on top of the official MEDSL
2022 general election files.

## Workflow

Keep the source ZIP files in `individual_states/` unchanged. Put reusable code in
`analysis/src/`, repeatable command-line scripts in `analysis/scripts/`, and
exploratory notebooks in `analysis/notebooks/`. Generated files should go under
`analysis/outputs/`, which is ignored by Git.

Florida is the first prototype state, but the code is written so the same pattern
can be reused for other state files later.

## Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r analysis/requirements.txt
```

## First Checks

Profile Florida:

```bash
python analysis/scripts/profile_state.py fl
```

Profile another state by postal abbreviation:

```bash
python analysis/scripts/profile_state.py ga
```

## Analysis Notes

- Do not sum every row in a state file unless that is truly the question. Offices,
  ballot questions, registration rows, undervotes, and overvotes are stacked in
  the same file.
- For Florida, blank `office` rows contain registration metadata such as
  `REGISTERED VOTERS`, `REGISTERED REPUBLICANS`, `REGISTERED DEMOCRATS`, and
  `REGISTERED OTHER`.
- For `US HOUSE`, always group by `district` as well as `office`.
- Treat `UNDERVOTES`, `OVERVOTES`, and `WRITE-IN` deliberately instead of letting
  them slip into candidate or party summaries by accident.

