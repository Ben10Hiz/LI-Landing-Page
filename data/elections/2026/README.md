# 2026 General Election candidates (Election Day: November 3, 2026)

Candidate lists for the Legal Insights elections / virtual ballot app.

| File | What it is | Rows |
|---|---|---|
| `candidates-2026.xlsx` | Everything below in one workbook (one tab per list, filters on) | — |
| `us-senate.csv` | Every 2026 U.S. Senate race: 33 regular + FL and OH specials | 123 candidates / 35 races |
| `us-house.csv` | All 435 U.S. House districts | 1,158 candidates / 435 races |
| `congress.json` | Senate + House as nested JSON (race → candidates) | 470 races |
| `indiana/candidates.csv` | Every Indiana candidate on the 2026 general ballot, U.S. House to township board | 7,394 candidates |
| `indiana/candidates.json` | Same as above, JSON | 7,394 |
| `indiana/offices.csv` | One row per Indiana race (seats, # candidates, contested?) | 4,074 races |
| `indiana/source/` | The official spreadsheet these were built from | — |
| `app/` | Compact JSON for the Legal Insights Elections page (copy to the React app's `public/elections/2026/`) | 50 states, 92 counties, 448 towns/school districts |

## Sources

- **Indiana** — Indiana Election Division, *2026 General Election Candidate
  List* (abbreviated), dated **Sept 22, 2026**, from
  <https://www.in.gov/sos/elections/candidate-information/>. This is the
  official certified list and includes declared write-in candidates
  (`write_in = yes`). Incumbent flags for U.S. House come from `congress.json`;
  for the Indiana Senate and House they come from Wikipedia's
  *2026 Indiana Senate election* / *2026 Indiana House of Representatives
  election* articles (`seat_incumbent` = who holds the seat now).
- **U.S. House & Senate (all states)** — the race tables in Wikipedia's
  *2026 United States House of Representatives elections* and *2026 United
  States Senate elections* articles (pulled Oct 10, 2026), which cite each
  state's official filings. Wikipedia is a secondary source: verify against
  the state election office before publishing a state's ballot, the way the
  Indiana list was. Write-in candidates are generally not included.

## Columns

**`us-house.csv` / `us-senate.csv`**: `chamber, state, state_code, district,
candidate, party, incumbent, note, seat_incumbents, seat_status, wikipedia`
— `incumbent = yes` marks the sitting member; `seat_status` is e.g.
"Incumbent renominated", "Incumbent retiring", "Incumbent lost renomination".
Senate `district` is `Class II` (regular) or `Special`.

**`indiana/candidates.csv`**: `level, office_category, office, county,
district, seats, candidate, party, write_in, incumbent, seat_incumbent,
filed_date` — `level` is one of federal, statewide, state legislative,
judicial, county, township, municipal, school, special district. `office` is
the exact ballot title. `seats` > 1 means "vote for N". `county` is filled
for county/township/judicial offices (school and town races often span or
omit counties). `candidate` is the name exactly as it will appear on the
ballot.

## Rebuilding

```bash
pip install openpyxl
python3 scripts/elections/build_congress_2026.py   # refetch Wikipedia → us-*.csv, congress.json
python3 scripts/elections/build_indiana_2026.py    # Indiana list (+ incumbents) → indiana/*
python3 scripts/elections/build_workbook_2026.py   # → candidates-2026.xlsx
python3 scripts/elections/build_app_bundle_2026.py # → app/ (Elections page data)
```

In `app/`, candidate names filed in ALL CAPS are shown in title case and
office numbers are unpadded ("District 096" → "District 96"); the CSVs keep the
names and titles exactly as filed.

To use a newer Indiana list, download it from the Candidate Information page
and pass its path: `build_indiana_2026.py path/to/list.xlsx`.

## Known gaps

- Indiana does not publish which precincts/addresses vote in each race in this
  list; mapping a voter's address to their ballot needs district boundaries
  (congressional, legislative, county commissioner/council, township, school
  corporation, town).
- Judicial retention questions (Indiana Supreme Court, Court of Appeals) and
  local public questions are not in the candidate list.
- Party, bio, and finance data beyond what is listed here are not included yet.
