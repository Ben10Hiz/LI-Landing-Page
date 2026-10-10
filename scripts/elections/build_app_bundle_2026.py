#!/usr/bin/env python3
"""Package the 2026 candidate data as small static JSON files for the
Legal Insights Elections page (served from the app's public/ folder).

    python3 scripts/elections/build_app_bundle_2026.py [OUT_DIR]

Default OUT_DIR is data/elections/2026/app/. Copy that folder to the React
app as public/elections/2026/. Layout:

    congress/{ST}.json         U.S. Senate + House races for each state
    indiana/index.json         IN federal, statewide and legislative races,
                               plus the county / place pickers
    indiana/counties/{slug}.json  county, judicial, township (and some town)
                               races for one county
    indiana/places/{id}.json   city/town or school-board races for one place
    profiles/{race-id}.json    researched race profiles, copied from
                               data/elections/2026/profiles/
"""
import csv
import json
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "elections" / "2026"
ELECTION = {"id": "2026-general", "name": "2026 General Election",
            "date": "2026-11-03", "type": "general"}
PROFILES = DATA / "profiles"
IN_SOURCE = ("Indiana Election Division, 2026 General Election Candidate List "
             "(Sept 22, 2026)")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n",
                    encoding="utf-8")


# ─── Congress (all states) ───────────────────────────────────────────────────

def congress_race(r):
    is_senate = r["chamber"] == "U.S. Senate"
    district = r["district"]
    rid = slug(f'{r["state_code"]}-{"sen" if is_senate else "house"}-{district}')
    if is_senate:
        label = f'{r["state"]} (special election)' if district == "Special" else r["state"]
    else:
        label = "At-large" if district == "At-large" else f"District {district}"
    return {
        "id": rid,
        "level": "federal",
        "office": "U.S. Senator" if is_senate else "U.S. Representative",
        "district": label,
        "seats": 1,
        "description": r["status"],
        "candidates": [
            {
                "id": f"{rid}-{i}",
                "name": c["name"],
                "party": c["party"],
                "incumbent": bool(c.get("incumbent")),
                "note": c.get("note") or "",
                "wikipedia": c.get("wikipedia") or "",
            }
            for i, c in enumerate(r["candidates"])
        ],
    }


def build_congress(out):
    races = json.loads((DATA / "congress.json").read_text())["races"]
    by_state = defaultdict(lambda: {"senate": [], "house": OrderedDict()})
    names = {}
    for r in races:
        st = by_state[r["state_code"]]
        names[r["state_code"]] = r["state"]
        if r["chamber"] == "U.S. Senate":
            st["senate"].append(congress_race(r))
        else:
            st["house"][r["district"]] = congress_race(r)
    for code, st in by_state.items():
        write(out / "congress" / f"{code}.json", {
            "state": code, "state_name": names[code], "election": ELECTION,
            "source": "Wikipedia 2026 U.S. House / Senate election race tables",
            "senate": st["senate"], "house": st["house"],
        })
    return len(by_state)


# ─── Indiana ─────────────────────────────────────────────────────────────────

LEVEL_TO_TAB = {
    "federal": "federal", "statewide": "state", "state legislative": "state",
    "judicial": "local", "county": "local", "township": "local",
    "municipal": "local", "school": "local", "special district": "local",
}
ORDINAL_WORDS = {"1": "1st", "2": "2nd", "3": "3rd"}

PLACE_PATTERNS = [
    re.compile(r"^Mayor of (.+)$"),
    re.compile(r"^MSD of (.+?) District"),
    re.compile(r"^School Board Member, (.+)$"),
    re.compile(r"^(.+?) (?:Community |Consolidated |Metropolitan |United |Unified |Township |Public |)School"),
    re.compile(r"^(.+?) (?:Town|City)\b"),
    re.compile(r"^(.+?) Clerk-Treasurer"),
    re.compile(r"^(.+?) City Judge"),
]
TOWNSHIP_PATTERNS = [
    re.compile(r"^(.+?) Township (?:Trustee|Board|Assessor)"),
    re.compile(r"^Constable of Small Claims Court, (.+?) Township"),
    re.compile(r"Small Claims Court, (.+?) Twp"),
]


def display_name(name):
    """Ballot names are printed as filed; soften the ones filed in ALL CAPS."""
    if name.upper() != name or not re.search(r"[A-Z]{3}", name):
        return name
    out = name.title()
    out = re.sub(r"\b(Mc|Mac)([a-z])", lambda m: m.group(1) + m.group(2).upper(), out)
    return re.sub(r"\b(Ii|Iii|Iv)\b", lambda m: m.group(1).upper(), out)


def display_office(office):
    return re.sub(r"District 0+(\d)", r"District \1", office)


def place_of(office):
    for pat in PLACE_PATTERNS:
        m = pat.match(office)
        if m:
            return m.group(1).strip(" ,")
    return office


def township_of(office):
    for pat in TOWNSHIP_PATTERNS:
        m = pat.search(office)
        if m:
            return m.group(1).strip()
    return ""


def same_person(a, b):
    a = re.sub(r"[.,()]", " ", a.lower()).split()
    b = re.sub(r"[.,()]", " ", b.lower()).split()
    return bool(a and b) and a[-1] == b[-1] and b[0] in a[:-1]


def profile_incumbent(rid):
    """Officeholder named in a race profile, if any (statewide offices are
    not flagged in the state's candidate list)."""
    path = PROFILES / f"{rid}.json"
    if not path.exists():
        return ""
    return (json.loads(path.read_text(encoding="utf-8")).get("incumbent") or {}).get("name", "")


def in_race(office_row, cands):
    o = office_row
    rid = "in-" + slug(o["office"])
    level = o["level"]
    desc = {
        "federal": "Indiana's member of the U.S. House. 2-year term.",
        "statewide": "Statewide executive office. 4-year term.",
    }.get(level, "")
    if level == "state legislative":
        desc = ("Indiana Senate. 4-year term." if "Senator" in o["office"]
                else "Indiana House of Representatives. 2-year term.")
    if int(o["seats"]) > 1:
        desc = (desc + " " if desc else "") + f'Vote for up to {o["seats"]}.'
    holder = profile_incumbent(rid)
    if any(c["write_in"] for c in cands):
        desc = (desc + " " if desc else "") + "Write-in candidates must be written in by name."
    return {
        "id": rid,
        "has_profile": (PROFILES / f"{rid}.json").exists(),
        "level": LEVEL_TO_TAB[level],
        "category": o["office_category"],
        "office": display_office(o["office"]),
        "district": o["district"],
        "county": o["county"],
        "seats": int(o["seats"]),
        "description": desc,
        "candidates": [
            {
                "id": f"{rid}-{i}",
                "name": display_name(c["candidate"]),
                "party": c["party"],
                "incumbent": c["incumbent"] == "yes"
                or bool(holder and same_person(c["candidate"], holder)),
                "write_in": c["write_in"] == "yes",
                "seat_incumbent": holder or c["seat_incumbent"],  # a researched profile is newer than the seat-holder list
                "is_federal": level == "federal",
                "chamber": {"U.S. Representative": "house",
                            "State Senator": "upper",
                            "State Representative": "lower"}.get(c["office_category"], ""),
            }
            for i, c in enumerate(sorted(cands, key=lambda c: (c["write_in"] == "yes", c["candidate"])))
        ],
    }


def build_indiana(out):
    with (DATA / "indiana" / "offices.csv").open(encoding="utf-8") as f:
        offices = list(csv.DictReader(f))
    with (DATA / "indiana" / "candidates.csv").open(encoding="utf-8") as f:
        by_office = defaultdict(list)
        for c in csv.DictReader(f):
            by_office[c["office"]].append(c)

    top = {"federal": {}, "statewide": [], "senate": {}, "house": {}}
    counties = defaultdict(lambda: {"races": [], "townships": set()})
    places = OrderedDict()

    for o in offices:
        race = in_race(o, by_office[o["office"]])
        lvl, cat = o["level"], o["office_category"]
        if lvl == "federal":
            top["federal"][o["district"]] = race
        elif lvl == "statewide":
            top["statewide"].append(race)
        elif cat == "State Senator":
            top["senate"][o["district"]] = race
        elif cat == "State Representative":
            top["house"][o["district"]] = race
        elif lvl in ("municipal", "school") and not (lvl == "municipal" and o["county"]):
            name = place_of(o["office"])
            kind = "school" if lvl == "school" else "town"
            pid = f"{kind}-{slug(name)}"
            race["place"] = name
            places.setdefault(pid, {"id": pid, "name": name, "type": kind, "races": []})
            places[pid]["races"].append(race)
        else:
            for county in (o["county"].split("; ") if o["county"] else []):
                twp = township_of(o["office"]) if lvl in ("township", "judicial") else ""
                if twp:
                    race = {**race, "township": twp}
                    counties[county]["townships"].add(twp)
                counties[county]["races"].append(race)

    county_index = []
    for name in sorted(counties):
        c = counties[name]
        cslug = slug(name)
        write(out / "indiana" / "counties" / f"{cslug}.json", {
            "county": name, "townships": sorted(c["townships"]), "races": c["races"],
        })
        county_index.append({"name": name, "slug": cslug, "townships": sorted(c["townships"])})

    for pid, p in places.items():
        write(out / "indiana" / "places" / f"{pid}.json", p)
    write(out / "indiana" / "index.json", {
        "state": "IN", "election": ELECTION, "source": IN_SOURCE,
        "generated": date.today().isoformat(),
        "federal": top["federal"], "statewide": top["statewide"],
        "senate": top["senate"], "house": top["house"],
        "senate_districts_on_ballot": sorted(top["senate"], key=int),
        "counties": county_index,
        "places": sorted(
            ({"id": p["id"], "name": p["name"], "type": p["type"]} for p in places.values()),
            key=lambda p: (p["type"], p["name"]),
        ),
    })
    return len(county_index), len(places)


def copy_profiles(out):
    n = 0
    for path in sorted(PROFILES.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))  # validates JSON
        write(out / "profiles" / path.name, profile)
        n += 1
    return n


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA / "app"
    n_states = build_congress(out)
    n_counties, n_places = build_indiana(out)
    n_profiles = copy_profiles(out)
    total = sum(f.stat().st_size for f in out.rglob("*.json"))
    print(f"{n_states} congress files, {n_counties} IN counties, {n_places} IN places; "
          f"{n_profiles} race profiles; {total / 1024:.0f} KB total -> {out}")


if __name__ == "__main__":
    main()
