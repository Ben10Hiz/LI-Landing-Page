#!/usr/bin/env python3
"""Build race profiles from JSON sources in scripts/elections/profiles/src/.

Each src/<race-id>.json is a profile (shape in data/elections/2026/profiles/
README.md) with {key} citations, plus "sources": {key: [title, publisher,
date, url]}. "office": "@us_house" pulls in src/_shared_us_house_office.json.

    python3 scripts/elections/profiles/build_from_src.py [race-id ...]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import build_profile  # noqa: E402

SRC = Path(__file__).resolve().parent / "src"
SHARED = {"@us_house": "_shared_us_house_office.json"}


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
