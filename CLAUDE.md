# Travel Agent — Claude Instructions

## File References

| File | Role | When to use |
|------|------|-------------|
| [`preferences.md`](preferences.md) | Traveler profile, budget, food restrictions, travel style | Apply automatically — never ask about anything already defined here |
| [`output.md`](output.md) | HTML format spec, section structure, style rules | Every output must be a self-contained HTML file per these rules — never markdown |
| [`notes.md`](notes.md) | Research checklist + special destination rules | Use as the research brief — cover every section listed |

## Country Folders

Some destinations have a folder (e.g., `sri lanka/`) containing saved Instagram/social screenshots. When a folder exists:
- Extract all text from every image in the folder
- Consolidate into: **tips · places to eat · places to visit · hotels/spas**
- Fold the intel into the relevant HTML sections — not a separate section

## Special Destination Rules (from notes.md)

- **Dominica, UK, Kenya:** 0 hotel cost (visiting family) — include flights only
- **Trinidad:** Target Carnival in February — include band/concert costs
- **Bora Bora:** Plan as 4-night leg combined with 6-night California
- **Florida:** Pair with Ultra Music Festival (March) — include VIP ticket cost

## Workflow

1. Read `preferences.md`, `output.md`, `notes.md`
2. If a country folder exists, extract all image content first
3. Produce one self-contained HTML file per `output.md` spec
4. Never produce markdown output
