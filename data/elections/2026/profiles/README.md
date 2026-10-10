# Race profiles

Researched, sourced profiles shown on the Legal Insights Elections page
("About this office" on the race card, and the candidate pop-ups). One JSON
file per race, named after the race id the app uses
(`in-` + slug of the official office title, e.g. `in-secretary-of-state.json`).

## Editorial standard

- **Nonpartisan.** Describe policy, plans and public statements. No ideology
  labels, no adjectives that take sides, no predictions, no endorsements.
- **Attributed.** Every factual line ends with a citation like `[3]`
  pointing to `sources`. Criticisms and allegations say who made them.
- **Quoted only from the page.** Direct quotes are used only when read in the
  cited source; everything else is a paraphrase and reads like one.
- **Equal treatment.** Every candidate gets the same sections. When coverage
  is thin, say so under `gaps` rather than filling space.
- **Dated.** `reviewed` is the research date; statements carry their dates
  where known.

## Shape

```jsonc
{
  "race_id": "in-secretary-of-state",
  "reviewed": "2026-10-10",
  "office": {
    "title": "Indiana Secretary of State",
    "summary": "… [1]",
    "facts": [{ "label": "Term", "value": "4 years [2]" }],
    "duties": ["… [1]"],
    "recent_changes": ["… [4]"]
  },
  "incumbent": { "name": "…", "party": "…", "summary": "…", "record": ["2023-…: … [5]"] },
  "race_context": ["… [6]"],
  "candidates": [
    {
      "ballot_name": "Beau Bayh",          // exactly as on the official list
      "seat": "District 2",                // school board profiles only
      "summary": "…",
      "website": "https://…",
      "background": ["… [7]"],
      "path_to_ballot": ["… [8]"],
      "positions": [{ "topic": "Election administration", "items": ["… [9]"] }],
      "on_incumbent": ["… [10]"],
      "plans": ["… [11]"],
      "endorsements_finance": ["… [12]"],
      "gaps": ["No published position on …"]
    }
  ],
  "sources": [{ "id": 1, "title": "…", "publisher": "…", "date": "2026-…", "url": "https://…" }]
}
```

**School boards.** One profile per school corporation covers every seat it
has on the ballot: `in-school-board-{place}` (e.g.
`in-school-board-marion-indianapolis`), with `incumbent: null`, the district
and seat holders described in `race_context`, and a `seat` on each
candidate. School board races without their own profile point to the office
explainer `in-office-school-board` (no candidates). The app bundle sets each
race's `profile_id` accordingly.
