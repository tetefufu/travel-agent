# Hotel Review Score Skill — Design

## Purpose

A repo-wide skill that scores and ranks a shortlist of hotels using real guest
sentiment (TripAdvisor + Google reviews) instead of marketing copy or star
rating alone. Triggered by phrases like "score these hotels," "compare hotel
reviews," or `/hotel-review-score`.

Source note: `bora bora/review kill.md` (the original scratch notes this
skill is built from).

## Input

- A destination name and a list of hotel names.
- If a `hotels-price-distribution.csv` already exists for that destination
  (per the `hotels.md` research convention), the skill may pull the hotel
  list from there instead of requiring it to be retyped.

## Workflow

1. **Fetch** — for each hotel, use the browser tool to open its TripAdvisor
   and Google review pages, sorted/filtered to 1–3 star reviews from the
   last 12 months. Cap at ~15–20 reviews per source per hotel so the fetch
   stays bounded.
   - If a source blocks or rate-limits, note it and continue with whatever
     source is still available rather than retrying/looping.
2. **Read & judge** — no fixed formula. Claude reads the pulled reviews and
   weighs them using judgment guided by:
   - **Recency** — more recent reviews within the 12-month window count
     more than older ones.
   - **Reviewer reliability** — a reviewer with visible history/many
     contributions and a substantive review counts more; a one-off,
     single-line, or single-review-ever account counts less.
   - **Relevance to this traveler** — read automatically from
     `preferences.md` (couple, no kids, doesn't swim in the sea so pool
     matters more than beach, vegetarian food, luxury expectations).
     Complaints about kids' clubs/family rooms are discounted; complaints
     about pool condition, vegetarian food, noise, service, room quality
     keep full weight.
3. **Score** — each hotel gets a 1–10 score plus a one-line "why." The
   reasoning must stay inspectable (no opaque single number with no
   explanation).
4. **Output** — one markdown comparison table, sorted best to worst:

   ```
   Hotel | Score /10 | Pos:Neg ratio | Top negative themes | Data confidence | Verdict
   ```

## Edge cases

- Too few reviews in the 12-month window → hotel is flagged "low
  confidence" but still scored and shown, caveated.
- A source is fully blocked for a hotel → hotel marked "reviews
  unavailable" for that source; if no source has data, exclude the hotel
  from the ranking rather than guessing.

## Non-goals

- No persistent scraping infrastructure, no database, no scheduled re-runs.
  This is a single-invocation research skill, run on demand.
- No strict weighting formula — deliberately judgment-based per user
  preference, since sarcasm/mixed reviews don't reduce well to a fixed
  equation.

## Where it lives

`travel-agent/.claude/skills/hotel-review-score/SKILL.md` — repo-wide project
skill (not Bora-Bora-specific), consistent with how `hotels.md` already
documents a repo-wide hotel research process.
