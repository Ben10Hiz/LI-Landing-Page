#!/usr/bin/env python3
"""Build the 2026 U.S. House and U.S. Senate general-election candidate lists.

Source: the race tables on the English Wikipedia articles
"2026 United States House of Representatives elections" and
"2026 United States Senate elections", which cite each state's official
candidate filings. Re-run to refresh:

    python3 scripts/elections/build_congress_2026.py            # fetch + build
    python3 scripts/elections/build_congress_2026.py --wiki-dir DIR  # use saved wikitext

Writes data/elections/2026/us-house.csv, us-senate.csv and congress.json.
"""
import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "elections" / "2026"
UA = "LegalInsightsResearch/0.1 (elections data build)"
PAGES = {
    "house": "2026_United_States_House_of_Representatives_elections",
    "senate": "2026_United_States_Senate_elections",
}

STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska",
    "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "AS": "American Samoa", "DC": "District of Columbia", "GU": "Guam",
    "MP": "Northern Mariana Islands", "PR": "Puerto Rico",
    "VI": "U.S. Virgin Islands",
}
STATE_CODES = {v: k for k, v in STATES.items()}


def fetch_wikitext(title):
    url = (
        "https://en.wikipedia.org/w/api.php?action=parse&prop=wikitext"
        "&format=json&formatversion=2&redirects=1&page="
        + urllib.parse.quote(title)
    )
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)["parse"]["wikitext"]
        except Exception:  # rate limits are common; back off and retry
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Could not fetch {title}")


# ─── Wikitext helpers ────────────────────────────────────────────────────────

REF_RE = re.compile(r"<ref[^>/]*/>|<ref[^>]*>.*?</ref>", re.S)


def strip_refs(text):
    return REF_RE.sub("", text)


def clean(text):
    """Reduce a wikitext fragment to plain text."""
    t = strip_refs(text)
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\{\{\s*(?:small|nowrap|Small|Nowrap)\s*\|([^{}]*)\}\}", r"\1", t)
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", t)
    for _ in range(3):
        t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"^\s*(?:(?:style|data-sort-value|class)=(?:\"[^\"]*\"|\S+)\s*)+\|", "", t)
    t = t.replace("'''", "").replace("''", "").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", t).strip(" |")


def wiki_link(fragment):
    m = re.search(r"\[\[([^|\]]+)", fragment)
    return m.group(1).strip() if m else ""


def parse_sortname(fragment):
    m = re.search(r"\{\{sortname\|([^|}]*)\|([^|}]*)", fragment, re.I)
    return f"{m.group(1).strip()} {m.group(2).strip()}" if m else ""


CANDIDATE_RE = re.compile(r"^\s*\*\s*(.*)$", re.M)


def parse_candidates(cell):
    out = []
    cell = re.sub(r"\s*\*\s*\{\{Party stripe", "\n*{{Party stripe", strip_refs(cell), flags=re.I)
    for line in CANDIDATE_RE.findall(cell):
        if "Party stripe" not in line and "(" not in line:
            continue
        body = re.sub(r"^\{\{Party stripe\|[^}]*\}\}\s*", "", line.strip(), flags=re.I)
        text = clean(body)
        m = re.match(r"^(.*?)\s*\(([^()]*(?:\([^()]*\))?[^()]*)\)\s*(.*)$", text)
        if not m:
            continue
        name, party, note = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if not name:
            continue
        out.append({
            "name": name,
            "party": party,
            "note": note,
            "wikipedia": wiki_link(body),
        })
    return out


def split_rows(table):
    return re.split(r"\n\|-[^\n]*", table)


def tables_in(section):
    return re.findall(r"\{\|.*?\n\|\}", section, re.S)


def status_from(row):
    lines = row.split("\n")
    for i, line in enumerate(lines):
        # The status cell sits directly before the candidate list.
        if re.search(r"plainlist", line, re.I) and i > 0 and not lines[i - 1].startswith("!"):
            prev = clean(re.sub(r"^\|\s*(?:\{\{[^}]*\}\}\s*)?(?:data-sort-value=\S+\s*)?\|?", "", lines[i - 1]))
            if prev and not re.fullmatch(r"[\d.%A-Z ]+", prev):
                return prev
    for line in lines:
        plain = clean(line.split("|", 2)[-1] if line.count("|") >= 2 else line)
        if re.search(r"\b(Incumbent|New (?:member|representative|senator|delegate|commissioner))", plain):
            return plain
    return ""


def incumbent_party(row):
    for line in row.split("\n"):
        m = re.search(r"\|\s*(Democratic|Republican|Independent|Libertarian|Nonpartisan|Democratic–NPL|DFL)\s*$", line)
        if m:
            return m.group(1)
    return ""


# ─── House ───────────────────────────────────────────────────────────────────

# Only the row-header cell ("!{{ushr|IN|1|X}}") opens a district; other
# {{ushr}} mentions are "Redistricted from ..." notes.
USHR_RE = re.compile(r"^!\s*(?:rowspan=\d+\s*\|)?\s*\{\{ushr\|([A-Z]{2})\|([^|}]+)", re.I | re.M)


def build_house(wikitext):
    sections = re.split(r"\n==([^=].*?)==\s*\n", wikitext)
    races = []
    for i in range(1, len(sections), 2):
        state_name = sections[i].strip()
        if state_name not in STATE_CODES:
            continue
        body = sections[i + 1]
        for table in tables_in(body):
            if "ushr" not in table:
                continue
            current = None
            for row in split_rows(table):
                m = USHR_RE.search(row)
                incumbent = parse_sortname(row)
                if m:
                    district = m.group(2).strip()
                    current = {
                        "chamber": "U.S. House",
                        "state": state_name,
                        "state_code": m.group(1).upper(),
                        "district": "At-large" if district.upper() in ("AL", "AT-LARGE") else district,
                        "incumbents": [],
                        "status": status_from(row),
                        "candidates": parse_candidates(row),
                    }
                    races.append(current)
                elif current is None or not incumbent:
                    continue
                if incumbent:
                    current["incumbents"].append({
                        "name": incumbent,
                        "party": incumbent_party(row),
                        "status": status_from(row),
                    })
    return races


# ─── Senate ──────────────────────────────────────────────────────────────────

SENATE_STATE_RE = re.compile(
    r"^!\s*\[\[2026 United States Senate (special )?election in ([^|\]]+)\|", re.M
)


def senate_incumbent(row):
    name = parse_sortname(row)
    if name:
        return name
    lines = row.split("\n")
    for i, line in enumerate(lines):
        if "Shading PVI" in line and i + 1 < len(lines):
            m = re.search(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", lines[i + 1])
            return m.group(1).strip() if m else clean(lines[i + 1])
    return ""


def build_senate(wikitext):
    start = wikitext.find("=== Elections leading to the next Congress ===")
    special = wikitext.find("=== Special elections during the preceding Congress ===")
    table_text = wikitext[start:]
    table = tables_in(table_text)[0]
    races = []
    for row in split_rows(table):
        m = SENATE_STATE_RE.search(row)
        if not m:
            continue
        state_name = m.group(2).strip()
        races.append({
            "chamber": "U.S. Senate",
            "state": state_name,
            "state_code": STATE_CODES.get(state_name, ""),
            "district": "Special" if m.group(1) else "Class II",
            "incumbents": [{
                "name": senate_incumbent(row),
                "party": incumbent_party(row),
                "status": status_from(row),
            }],
            "status": status_from(row),
            "candidates": parse_candidates(row),
        })
    # The main table omits incumbents for special elections (FL, OH); take
    # them from the "Special elections during the preceding Congress" table.
    if special != -1:
        sp_tables = tables_in(wikitext[special:start])
        by_state = {r["state"]: r for r in races}
        for row in (split_rows(sp_tables[0]) if sp_tables else []):
            m = re.search(r"^!\s*\[\[2026 United States Senate special election in ([^|\]]+)\|", row, re.M)
            if not m:
                continue
            state_name = m.group(1).strip()
            race = by_state.get(state_name)
            if race is None:
                race = {
                    "chamber": "U.S. Senate",
                    "state": state_name,
                    "state_code": STATE_CODES.get(state_name, ""),
                    "district": "Special",
                    "incumbents": [{"name": ""}],
                    "status": "",
                    "candidates": parse_candidates(row),
                }
                races.append(race)
            if not race["incumbents"][0]["name"]:
                race["incumbents"] = [{
                    "name": senate_incumbent(row),
                    "party": incumbent_party(row),
                    "status": status_from(row),
                }]
                race["status"] = race["status"] or status_from(row)
    return races


# ─── Output ──────────────────────────────────────────────────────────────────

def mark_incumbents(races):
    """Flag the candidate(s) who currently hold the seat.

    Matches exact names first, then same first + last name (handles middle
    initials). When several candidates share a name (e.g. two "Dan Sullivan"s
    in Alaska) only the one linked to a Wikipedia article is flagged.
    """
    for race in races:
        for inc in race["incumbents"]:
            name = inc["name"].lower().split()
            if not name:
                continue
            exact = [c for c in race["candidates"] if c["name"].lower().split() == name]
            loose = [
                c for c in race["candidates"]
                if c["name"].lower().split()[:1] == name[:1]
                and c["name"].lower().split()[-1:] == name[-1:]
            ]
            hits = exact or loose
            if len(hits) > 1:
                hits = [c for c in hits if c["wikipedia"]] or hits[:0]
            for c in hits:
                c["incumbent"] = True
        for c in race["candidates"]:
            c.setdefault("incumbent", False)


def write_csv(path, races):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "chamber", "state", "state_code", "district", "candidate",
            "party", "incumbent", "note", "seat_incumbents", "seat_status",
            "wikipedia",
        ])
        for r in races:
            inc = "; ".join(f'{i["name"]} ({i["party"]})' for i in r["incumbents"])
            for c in r["candidates"] or [{"name": "", "party": "", "note": "No candidates listed", "wikipedia": "", "incumbent": False}]:
                w.writerow([
                    r["chamber"], r["state"], r["state_code"], r["district"],
                    c["name"], c["party"], "yes" if c.get("incumbent") else "",
                    c["note"], inc, r["status"],
                    f'https://en.wikipedia.org/wiki/{c["wikipedia"].replace(" ", "_")}' if c["wikipedia"] else "",
                ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-dir", help="Directory with house.wiki / senate.wiki")
    args = ap.parse_args()
    if args.wiki_dir:
        d = Path(args.wiki_dir)
        house_wt = (d / "house.wiki").read_text()
        senate_wt = (d / "senate.wiki").read_text()
    else:
        house_wt = fetch_wikitext(PAGES["house"])
        senate_wt = fetch_wikitext(PAGES["senate"])

    house = build_house(house_wt)
    senate = build_senate(senate_wt)
    mark_incumbents(house)
    mark_incumbents(senate)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "us-house.csv", house)
    write_csv(OUT / "us-senate.csv", senate)
    (OUT / "congress.json").write_text(json.dumps({
        "election": {"name": "2026 General Election", "date": "2026-11-03"},
        "generated": date.today().isoformat(),
        "sources": [f"https://en.wikipedia.org/wiki/{p}" for p in PAGES.values()],
        "races": senate + house,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    for label, races in (("House", house), ("Senate", senate)):
        n = sum(len(r["candidates"]) for r in races)
        empty = [f'{r["state_code"]}-{r["district"]}' for r in races if not r["candidates"]]
        print(f"{label}: {len(races)} races, {n} candidates, no candidates: {empty}")


if __name__ == "__main__":
    main()
