"""Render a race profile (JSON shape in data/elections/2026/profiles/README.md)
as Markdown for review."""


def _bullets(items):
    return "".join(f"- {t}\n" for t in items or [])


def render_markdown(p):
    o, inc = p["office"], p.get("incumbent")
    out = [f"# {o['title']} — 2026 race profile\n\n",
           f"_Researched {p['reviewed']} · status: {p.get('status', 'final')}._ {p.get('status_note', '')}\n\n",
           "## About the office\n\n", o["summary"] + "\n\n",
           "".join(f"- **{f['label']}:** {f['value']}\n" for f in o.get("facts", [])),
           "\n### What the office does\n\n", _bullets(o.get("duties")),
           "\n### Recent changes to the office\n\n", _bullets(o.get("recent_changes"))]
    if inc:
        out += [f"\n## Current officeholder: {inc['name']} ({inc['party']})\n\n",
                inc.get("summary", "") + "\n\n", _bullets(inc.get("record"))]
    out += ["\n## This race\n\n", _bullets(p.get("race_context"))]
    sections = [("Background", "background"), ("Path to the ballot", "path_to_ballot"),
                ("On the current officeholder", "on_incumbent"),
                ("How they say they'd run the office", "plans"),
                ("Endorsements & fundraising", "endorsements_finance"),
                ("What we couldn't verify", "gaps")]
    for c in p["candidates"]:
        out += [f"\n## {c['ballot_name']}\n\n", c.get("summary", "") + "\n"]
        if c.get("website"):
            out.append(f"\nCampaign website: {c['website']}\n")
        for title, key in sections[:2]:
            if c.get(key):
                out += [f"\n### {title}\n\n", _bullets(c[key])]
        if c.get("positions"):
            out.append("\n### Positions & plans\n")
            for pos in c["positions"]:
                out += [f"\n**{pos['topic']}**\n\n", _bullets(pos["items"])]
        for title, key in sections[2:]:
            if c.get(key):
                out += [f"\n### {title}\n\n", _bullets(c[key])]
    out.append("\n## Sources\n\n")
    out += [f"{s['id']}. [{s['title']}]({s['url']}) — {s['publisher']}{', ' + s['date'] if s['date'] else ''}\n"
            for s in p["sources"]]
    return "".join(out)
