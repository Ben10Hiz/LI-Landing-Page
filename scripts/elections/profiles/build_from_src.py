#!/usr/bin/env python3
"""Build race profiles from JSON sources in scripts/elections/profiles/src/.

Each src/<race-id>.json is a profile (shape in data/elections/2026/profiles/
README.md) with {key} citations, plus "sources": {key: [title, publisher,
date, url]}. "office": "@us_house" / "@in_senate" / "@in_house" / "@in_school_board" pulls in the shared
office section from src/_shared_*_office.json.

    python3 scripts/elections/profiles/build_from_src.py [race-id ...]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import build_profile  # noqa: E402

SRC = Path(__file__).resolve().parent / "src"
SHARED = {
    "@us_house": "_shared_us_house_office.json",
    "@in_senate": "_shared_in_senate_office.json",
    "@in_house": "_shared_in_house_office.json",
    "@in_school_board": "_shared_in_school_board_office.json",
}


def load(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    sources = data.pop("sources")
    if isinstance(data.get("office"), str):
        shared = json.loads((SRC / SHARED[data["office"]]).read_text(encoding="utf-8"))
        data["office"] = shared["office"]
        sources = {**shared["sources"], **sources}
    return data, sources


def main():
    wanted = set(sys.argv[1:])
    for path in sorted(SRC.glob("*.json")):
        if path.name.startswith("_") or (wanted and path.stem not in wanted):
            continue
        profile, sources = load(path)
        build_profile(profile, sources)


if __name__ == "__main__":
    main()
