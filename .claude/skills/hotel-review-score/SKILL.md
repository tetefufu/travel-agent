---
name: hotel-review-score
description: Use when comparing or ranking a shortlist of hotels by real guest sentiment instead of star rating or marketing copy — triggered by "score these hotels," "compare hotel reviews," or /hotel-review-score
---

# Hotel Review Score

## Overview
Scores a shortlist of hotels 1-10 using recent 1-3 star TripAdvisor and Google reviews, weighted by judgment (not a fixed formula) against the traveler's actual preferences.

## Input
- Destination + hotel list. If `hotels-price-distribution.csv` exists for that destination, pull the hotel list from there instead of retyping it.

## Workflow
1. **Fetch** — per hotel, open TripAdvisor and Google review pages, filtered to 1-3 star reviews from the last 12 months. Cap ~15-20 reviews per source. Source blocked/rate-limited → note it, continue with whatever source is available, don't retry-loop.
2. **Judge** — weigh reviews using:
   - **Recency** — newer within the 12-month window counts more.
   - **Reviewer reliability** — visible history + substantive review counts more; one-off single-line accounts count less.
   - **Relevance** — read from `preferences.md` automatically. Complaints irrelevant to this traveler (e.g. kids' clubs) get discounted; complaints on things that matter to them (pool, food restrictions, noise, service, room quality) keep full weight.
3. **Score** — 1-10 per hotel + one-line "why." Never output an opaque number with no reasoning.
4. **Output** — one markdown table, best to worst:

   `Hotel | Score /10 | Pos:Neg ratio | Top negative themes | Data confidence | Verdict`

## Edge cases
- Too few reviews in window → score anyway, flag "low confidence."
- A source fully blocked for a hotel → mark that source "unavailable." If no source has data → exclude the hotel, don't guess.

## Non-goals
No scraping infrastructure, no database, no scheduled re-runs — single-invocation research, judgment-based weighting (not a fixed equation).
