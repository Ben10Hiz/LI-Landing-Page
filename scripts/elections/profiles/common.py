"""Shared helpers for race profile scripts (see data/elections/2026/profiles/README.md)."""
import json
import re
from pathlib import Path

from render import render_markdown

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "elections" / "2026" / "profiles"


def _number(obj, sources, order):
    if isinstance(obj, str):
        def sub(m):
            key = m.group(1)
            if key not in sources:
                raise KeyError(f"unknown source {key}")
            if key not in order:
                order.append(key)
            return f"[{order.index(key) + 1}]"
        out = re.sub(r"\{([a-z0-9_]+)\}", sub, obj)
        return re.sub(r"\]\s*\[", ", ", re.sub(r"\s+(\[\d)", r" \1", out)).replace(" .", ".")
    if isinstance(obj, list):
        return [_number(x, sources, order) for x in obj]
    if isinstance(obj, dict):
        return {k: _number(v, sources, order) for k, v in obj.items()}
    return obj


def build_profile(profile, sources):
    """Number {key} citations, attach the source list, write .json and .md."""
    order = []
    out = _number(profile, sources, order)
    out["sources"] = [
        {"id": i + 1, "title": sources[k][0], "publisher": sources[k][1],
         "date": sources[k][2], "url": sources[k][3]}
        for i, k in enumerate(order)
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{out['race_id']}.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / f"{out['race_id']}.md").write_text(render_markdown(out), encoding="utf-8")
    unused = sorted(set(sources) - set(order))
    print(f"{out['race_id']}: {len(out['candidates'])} candidates, "
          f"{len(order)} sources; unused: {unused}")
    return out
