#!/usr/bin/env python3
"""Build the Indiana 2026 general-election candidate list.

Source: Indiana Election Division "2026 General Election Candidate List"
(abbreviated), linked from https://www.in.gov/sos/elections/candidate-information/
A copy of the spreadsheet used is kept in data/elections/2026/indiana/source/.

    python3 scripts/elections/build_indiana_2026.py [path/to/list.xlsx] [--wiki-dir DIR]

Incumbents for U.S. House come from data/elections/2026/congress.json (run
build_congress_2026.py first); incumbents for the Indiana Senate and House
come from the Wikipedia articles "2026 Indiana Senate election" and
"2026 Indiana House of Representatives election".

Writes data/elections/2026/indiana/candidates.csv, candidates.json and
offices.csv (one row per race).
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from datetime import date
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_congress_2026 import fetch_wikitext  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "elections" / "2026" / "indiana"
DEFAULT_SOURCE = OUT / "source" / "Candidate_List_Abbreviated_20260922.xlsx"
SOURCE_URL = (
    "https://www.in.gov/sos/elections/files/"
    "Candidate_List_Abbreviated_20260922_011251PM.xlsx"
)

COUNTIES = [
    "Adams", "Allen", "Bartholomew", "Benton", "Blackford", "Boone", "Brown",
    "Carroll", "Cass", "Clark", "Clay", "Clinton", "Crawford", "Daviess",
    "Dearborn", "Decatur", "DeKalb", "Delaware", "Dubois", "Elkhart",
    "Fayette", "Floyd", "Fountain", "Franklin", "Fulton", "Gibson", "Grant",
    "Greene", "Hamilton", "Hancock", "Harrison", "Hendricks", "Henry",
    "Howard", "Huntington", "Jackson", "Jasper", "Jay", "Jefferson",
    "Jennings", "Johnson", "Knox", "Kosciusko", "LaGrange", "Lake",
    "LaPorte", "Lawrence", "Madison", "Marion", "Marshall", "Martin",
    "Miami", "Monroe", "Montgomery", "Morgan", "Newton", "Noble", "Ohio",
    "Orange", "Owen", "Parke", "Perry", "Pike", "Porter", "Posey", "Pulaski",
    "Putnam", "Randolph", "Ripley", "Rush", "St. Joseph", "Scott", "Shelby",
    "Spencer", "Starke", "Steuben", "Sullivan", "Switzerland", "Tippecanoe",
    "Tipton", "Union", "Vanderburgh", "Vermillion", "Vigo", "Wabash",
    "Warren", "Warrick", "Washington", "Wayne", "Wells", "White", "Whitley",
]
_COUNTY_ALT = "|".join(re.escape(c) for c in sorted(COUNTIES, key=len, reverse=True))
COUNTY_PATTERNS = [
    re.compile(rf"\b({_COUNTY_ALT}) County\b", re.I),
    re.compile(rf"^Judge of the ({_COUNTY_ALT}) (?:Circuit|Superior|Small Claims)", re.I),
    re.compile(rf"\(({_COUNTY_ALT})\)", re.I),
    re.compile(rf", ({_COUNTY_ALT})$", re.I),
]
MULTI_COUNTY = re.compile(rf"\b({_COUNTY_ALT}) & ({_COUNTY_ALT}) Counties\b", re.I)

LEVELS = {
    "US REPRESENTATIVE": "federal",
    "SECRETARY OF STATE": "statewide",
    "STATE COMPTROLLER (AUDITOR OF STATE)": "statewide",
    "TREASURER OF STATE": "statewide",
    "STATE SENATOR": "state legislative",
    "STATE REPRESENTATIVE": "state legislative",
    "JUDGE, CIRCUIT COURT": "judicial",
    "JUDGE, SUPERIOR COURT": "judicial",
    "JUDGE, SMALL CLAIMS COURT": "judicial",
    "JUDGE, CITY COURT": "judicial",
    "PROSECUTING ATTORNEY": "county",
    "CLERK OF THE CIRCUIT COURT": "county",
    "COUNTY AUDITOR": "county",
    "COUNTY RECORDER": "county",
    "COUNTY TREASURER": "county",
    "COUNTY SHERIFF": "county",
    "COUNTY CORONER": "county",
    "COUNTY SURVEYOR": "county",
    "COUNTY ASSESSOR": "county",
    "COUNTY COMMISSIONER": "county",
    "COUNTY COUNCIL MEMBER": "county",
    "TOWNSHIP ASSESSOR": "township",
    "TOWNSHIP TRUSTEE": "township",
    "TOWNSHIP BOARD MEMBER": "township",
    "CONSTABLE OF SMALL CLAIMS COURT": "township",
    "MAYOR": "municipal",
    "CITY CLERK OR CLERK/TREASURER": "municipal",
    "CITY-COUNTY OR CITY COMMON COUNCIL MEMBER": "municipal",
    "TOWN CLERK-TREASURER": "municipal",
    "TOWN COUNCIL MEMBER": "municipal",
    "SCHOOL BOARD MEMBER": "school",
    "OTHER": "special district",
}
LEVEL_ORDER = list(OrderedDict.fromkeys(LEVELS.values()))
ORDINALS = {
    "First": 1, "Second": 2, "Third": 3, "Fourth": 4, "Fifth": 5,
    "Sixth": 6, "Seventh": 7, "Eighth": 8, "Ninth": 9,
}


def _canonical(name):
    return next(c for c in COUNTIES if c.lower() == name.lower())


def county_of(title):
    m = MULTI_COUNTY.search(title)
    if m:
        return f"{_canonical(m.group(1))}; {_canonical(m.group(2))}"
    for pat in COUNTY_PATTERNS:
        m = pat.search(title)
        if m:
            return _canonical(m.group(1))
    return ""


def district_of(title):
    m = re.search(r"\b(\w+) District\b", title)
    if m and m.group(1) in ORDINALS:
        return str(ORDINALS[m.group(1)])
    m = re.search(r"District\s+0*(\d+)", title)
    if m:
        return m.group(1)
    if re.search(r"\bAt Large\b", title, re.I):
        return "At-large"
    return ""


# The state list gives a seat count only when the office title says "(N seats)".
# Multi-seat races confirmed from local election coverage (see each school
# corporation's profile in data/elections/2026/profiles/ for the source).
SEAT_OVERRIDES = {
    "Fort Wayne Community School Board, At Large": 2,   # Journal Gazette
    "Elkhart Goshen School Board, At Large": 2,         # WSBT
    "Vanderburgh School Board, District 2": 2,          # WNIN
    "Marion Decatur Township School Board, At Large": 3,       # Chalkbeat / WFYI
    "Marion Pike Township School Board, At Large": 3,          # Chalkbeat / WFYI
    "Marion Wayne Township Public School Board, At Large": 4,  # Chalkbeat
    "Marion Perry Township Public School Board, At Large": 3,  # Chalkbeat / WFYI
    "Marion Warren Township School Board, At Large": 3,        # Chalkbeat / WFYI
    "Hamilton Noblesville School Board, At Large": 2,          # Noblesville Schools
    "Northwest Allen County School Board, District 4": 2,      # Journal Gazette (two at-large seats)
    "Kokomo School Board, At Large": 3,                        # Howard County candidate list
    "Richmond Community School Board, At Large": 2,            # Western Wayne News
    "Hammond School Board, At Large": 3,                       # Lake County sample ballot
    "Michigan City Area School Board, Civil City (LaPorte, Porter)": 3,  # LaPorte County records
    "LaPorte Community School Board, At Large": 4,             # LaPorte County records
    "Floyd County School Board, At Large": 2,                  # News and Tribune
    "Hendricks Avon School Board, Washington Township": 2,     # Hendricks County ballot
    "Hendricks Plainfield School Board, Guilford Township": 2, # Hendricks County ballot
    "Munster School Board, At Large": 2,                       # Lake County sample ballot
    "Warrick County School Board": 4,                          # VOTE411 / Ballot Brief
    "Hobart School Board, At Large": 4,                        # Lake County sample ballot
    "West Lafayette Community School Board": 3,                # Journal & Courier / district
    "Clay Community School Board, At Large (Clay, Parke)": 3,  # Brazil Times / county ballot
    "Delaware Yorktown Community School Board, Mt Pleasant Twp": 3,  # Delaware County ballot
    "South Harrison School Board District 4, Harrison Township": 2,  # Harrison County ballot
    "Whitley County Consolidated School Board, District Columbia City": 2,  # Whitley County election schedule
    "Grant Marion Community School Board, District 1": 3,  # Chronicle-Tribune
    "North Spencer School Board, Clay, Huff, Hammond Townships, Seat 1, 2": 2,  # office title names Seats 1 and 2; both terms end 2026
    "Crawfordsville School Board, At Large": 3,  # Journal Review
    "Franklin County Community School Board, At Large": 3,  # Franklin County sample ballot
}


# Candidates on the Sept. 22 state list who were later removed from the
# ballot, confirmed from county election records.
REMOVED = {
    ("North Harrison School Board, At Large", "Ray Von Allmen"),  # removed Sept. 1 after a challenge (Harrison County)
}


def seats_of(title):
    if title in SEAT_OVERRIDES:
        return SEAT_OVERRIDES[title]
    m = re.search(r"\((\d+) seats?\)", title, re.I)
    return int(m.group(1)) if m else 1


def category_label(category):
    label = category.title()
    for a, b in ((" Of ", " of "), (" Or ", " or "), (" The ", " the "), ("Us ", "U.S. ")):
        label = label.replace(a, b)
    return label


def normalize_party(raw):
    raw = (raw or "").strip()
    write_in = raw.lower().startswith("write-in")
    if write_in:
        raw = re.sub(r"^Write-In\s*\((.*)\)$", r"\1", raw, flags=re.I).strip()
    if raw in ("", "(  )", "( )", "()"):
        raw = "Nonpartisan"
    if raw == "Non Partisan":
        raw = "Nonpartisan"
    return raw, write_in


def read_rows(path):
    ws = openpyxl.load_workbook(path, read_only=True).active
    category = None
    for row in ws.iter_rows(values_only=True):
        a, b, c, d = (tuple(row) + (None,) * 4)[:4]
        if isinstance(a, str) and a.startswith("OFFICE CATEGORY"):
            category = (b or "").strip()
            continue
        if not a or not c or a == "BALLOT NAME":
            continue
        yield category, str(a).strip(), str(b or "").strip(), " ".join(str(c).split()), d


def filed(d):
    if hasattr(d, "date"):
        return d.date().isoformat()
    m = re.match(r"(\d+)/(\d+)/(\d{4})", str(d or ""))
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def load_house_incumbents():
    """Map IN congressional district -> incumbent name, from congress.json."""
    path = ROOT / "data" / "elections" / "2026" / "congress.json"
    if not path.exists():
        return {}
    races = json.loads(path.read_text())["races"]
    out = {}
    for r in races:
        if r["chamber"] == "U.S. House" and r["state_code"] == "IN":
            for c in r["candidates"]:
                if c.get("incumbent"):
                    out[r["district"]] = c["name"]
    return out


def load_legislature_incumbents(wiki_dir=None):
    """Map ("State Senator"|"State Representative", district) -> incumbent."""
    pages = {
        "State Senator": ("2026_Indiana_Senate_election", "in-senate.wiki"),
        "State Representative": ("2026_Indiana_House_of_Representatives_election", "in-houseleg.wiki"),
    }
    out = {}
    for office, (title, fname) in pages.items():
        try:
            text = (Path(wiki_dir) / fname).read_text() if wiki_dir else fetch_wikitext(title)
        except Exception as err:  # incumbency is a nice-to-have
            print(f"warning: no incumbents for {office}: {err}")
            continue
        parts = re.split(r"\n={2,3}\s*District (\d+)\s*={2,3}\s*\n", text)
        for i in range(1, len(parts), 2):
            body = parts[i + 1]
            m = (re.search(r"before_election\s*=\s*\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", body)
                 or re.search(r"represented by (?:Democrat|Republican|Independent)\s+\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", body))
            if m:
                out[(office, parts[i])] = m.group(1).strip()
    return out


NICKNAMES = {"randy": "randall", "rich": "richard", "becky": "rebecca", "bill": "william"}


def _tokens(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"\b([A-Za-z])\.\s*(?=[A-Za-z]\.)", r"\1", name)  # "J. D." -> "JD."
    toks = re.sub(r"[.,()]", " ", name.lower()).split()
    return [t for t in toks if t not in ("jr", "sr", "ii", "iii")]


def _same_first(a, b):
    a, b = NICKNAMES.get(a, a), NICKNAMES.get(b, b)
    short, long_ = sorted((a, b), key=len)
    return a == b or (len(short) >= 2 and long_.startswith(short))


def same_person(ballot_name, other):
    """Ballot names add middle names, initials or nicknames, e.g.
    "Cynthia (Cinde) Wirth", "Gregory E. Steuerwald", "John (J.D.) Prescott"."""
    a, b = _tokens(ballot_name), _tokens(other)
    if not a or not b or a[-1] != b[-1]:
        return False
    return any(_same_first(t, b[0]) for t in a[:-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", default=str(DEFAULT_SOURCE))
    ap.add_argument("--wiki-dir", help="Directory with in-senate.wiki / in-houseleg.wiki")
    args = ap.parse_args()
    source = Path(args.source)
    house_inc = load_house_incumbents()
    leg_inc = load_legislature_incumbents(args.wiki_dir)
    candidates = []
    seen = set()
    for category, name, party_raw, office, filed_date in read_rows(source):
        party, write_in = normalize_party(party_raw)
        level = LEVELS.get(category, "other")
        district = district_of(office)
        seat_holder = ""
        if category == "US REPRESENTATIVE":
            seat_holder = house_inc.get(district, "")
        elif category in ("STATE SENATOR", "STATE REPRESENTATIVE"):
            seat_holder = leg_inc.get((category.title(), district), "")
        incumbent = "yes" if seat_holder and same_person(name, seat_holder) else ""
        if (office, name) in REMOVED:
            continue
        if (office, name, party) in seen:  # the state list repeats a few rows
            continue
        seen.add((office, name, party))
        candidates.append(OrderedDict(
            level=level,
            office_category=category_label(category),
            office=office,
            county=county_of(office),
            district=district,
            seats=seats_of(office),
            candidate=name,
            party=party,
            write_in="yes" if write_in else "",
            incumbent=incumbent,
            seat_incumbent=seat_holder,
            filed_date=filed(filed_date),
        ))

    candidates.sort(key=lambda r: (
        LEVEL_ORDER.index(r["level"]) if r["level"] in LEVEL_ORDER else 99,
        r["office_category"], r["county"],
        int(r["district"]) if r["district"].isdigit() else 999,
        r["office"], r["write_in"], r["candidate"],
    ))

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "candidates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(candidates[0].keys()))
        w.writeheader()
        w.writerows(candidates)

    offices = OrderedDict()
    for c in candidates:
        key = c["office"]
        o = offices.setdefault(key, OrderedDict(
            level=c["level"], office_category=c["office_category"],
            office=c["office"], county=c["county"], district=c["district"],
            seats=c["seats"], candidates=0, write_ins=0, parties=set(),
        ))
        o["candidates"] += 1
        o["write_ins"] += 1 if c["write_in"] else 0
        o["parties"].add(c["party"])
    with (OUT / "offices.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["level", "office_category", "office", "county", "district",
                    "seats", "candidates", "write_ins", "contested", "parties"])
        for o in offices.values():
            on_ballot = o["candidates"] - o["write_ins"]
            w.writerow([o["level"], o["office_category"], o["office"], o["county"],
                        o["district"], o["seats"], o["candidates"], o["write_ins"],
                        "yes" if on_ballot > o["seats"] else "",
                        "; ".join(sorted(o["parties"]))])

    (OUT / "candidates.json").write_text(json.dumps({
        "election": {"name": "2026 Indiana General Election", "date": "2026-11-03"},
        "source": SOURCE_URL,
        "source_as_of": "2026-09-22",
        "generated": date.today().isoformat(),
        "candidates": candidates,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    no_county = sum(1 for c in candidates if not c["county"] and c["level"] in ("county", "township", "judicial"))
    print(f"{len(candidates)} candidates in {len(offices)} races; "
          f"{no_county} county/township/judicial rows without a county")


if __name__ == "__main__":
    main()
