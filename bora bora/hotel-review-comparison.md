# Bora Bora Hotel Review Comparison

Conrad Bora Bora Nui vs. The St. Regis Bora Bora Resort vs. The Westin Bora Bora Resort & Spa vs. Four Seasons Resort Bora Bora — scored on real guest sentiment (TripAdvisor + Google reviews), not star rating or marketing copy. Produced via the `hotel-review-score` skill (`.claude/skills/hotel-review-score/SKILL.md`), extended for this pass to cover the full 1-5 star range (not just 1-3) so complaints buried inside otherwise-glowing reviews get caught too.

## Comparison table

| Hotel | Score /10 | Pos:Neg (12mo) | Top negative themes | Data confidence | Verdict |
|---|---|---|---|---|---|
| **The St. Regis Bora Bora Resort** | 8/10 | ~55:7 | Butler service inconsistency, high F&B prices vs. quality (both recur even in 5★ reviews); isolated pest/lock-wear report from one reliable reviewer | High (62 reviews, full 12-month window) | Still the strongest pick — negatives are minor and mostly single-report, but butler/pricing gripes are structural enough to set expectations on |
| **Four Seasons Resort Bora Bora** | 7.5/10 | ~25:24* | Evening dining limited to 2 restaurants — flagged independently across 4★, 5★, and the earlier 1-3★ pass; service inconsistency; one mold/wear report | High (49 reviews, full 12-month window) | Excellent stay, but the dining-variety gripe is the one theme that survives even among happy reviewers — the clearest "structural" signal in this dataset |
| **The Westin Bora Bora Resort & Spa** | 6.5/10 | ~71:29 | Bike fleet in poor repair, slow/inconsistent breakfast service, weak on-site snorkeling, check-in delays off-peak — recurring across independent reviewers, even 5★ ones | High (100 reviews, full 12-month window) | Beautiful, newer property, but the broadest spread of small operational rough edges of the four — none touch pool or vegetarian food |
| **Conrad Bora Bora Nui** | 6/10 | ~41:14 | Construction/renovation disruption — one explicit "avoid, entire resort under construction" 1★ review, echoed more mildly even in 4-5★ reviews; French restaurant service complaint | High (55 reviews, full 12-month window) | Same caution as before, confirmed structural rather than a one-off — check current renovation status before booking |

\* Four Seasons' near-even ratio looks alarming at face value but is misleading: most of its "Neg" reviews are 5-star stays with one buried gripe the guest still didn't consider score-worthy — lower severity than a dedicated 1-3★ complaint, per the skill's weighting rule (a complaint that recurs across both 1-3★ *and* 4-5★ reviews counts as a stronger/structural signal; a one-off buried gripe does not).

**None of the four surfaced a pool-quality or vegetarian-food complaint** — the two dealbreakers per `preferences.md` (doesn't swim in the sea, vegetarian diet) stay clear across all four hotels, even with the full 1-5 star read.

## Scraper vs. browser automation

Recommendation was to keep using browser automation (Claude-in-Chrome) rather than build a scraper script — borne out in practice: it got clean, complete TripAdvisor data for all four hotels with zero CAPTCHAs or hard blocks. The only snag was an account-level session rate limit partway through (unrelated to scraping/bot-detection), resolved by resuming the affected forks once the limit reset. Full reasoning in the plan this was built from: `.claude/plans/do-another-review-this-dazzling-heron.md` (or wherever it's archived).

## Raw data

289 individual reviews saved as JSONL (one review per line) in `bora bora/reviews-raw/`:

| File | Reviews | Coverage |
|---|---|---|
| `conrad-bora-bora-nui-tripadvisor.jsonl` | 55 | Full 12-month window |
| `st-regis-bora-bora-tripadvisor.jsonl` | 62 | Full 12-month window |
| `westin-bora-bora-tripadvisor.jsonl` | 100 | Full 12-month window |
| `four-seasons-bora-bora-tripadvisor.jsonl` | 49 | Full 12-month window |
| `conrad-bora-bora-nui-google.jsonl` | 6 | Partial, truncated — Google's embedded review widget wouldn't sort/expand/paginate |
| `st-regis-bora-bora-google.jsonl` | 8 | Partial, truncated — same limitation |
| `westin-bora-bora-google.jsonl` | 7 | Partial, truncated — same limitation |
| `four-seasons-bora-bora-google.jsonl` | 2 | Blocked — Google exposes no individual reviews for this property, aggregate rating only |

Schema per line: `hotel, source, star_rating, date, reviewer_name, reviewer_contributions, review_text, review_title, fetched_date`.

## Known gaps / caveats

- **Google Reviews are corroborative only, not primary**, for all four hotels — the same structural widget limitation (sort dropdown wouldn't commit, "more" text wouldn't expand, no pagination past the first several cards) hit every hotel, so TripAdvisor carries the real analytical weight here.
- **Four Seasons Google** is fully blocked — no individual reviews are exposed by Google for this property at all, only an aggregate 5★-1★ distribution.
- **St. Regis raw file mixes date semantics**: entries 1-41 use "date of stay," entries 42-62 use "date posted" — flagged in case the file is parsed directly for date-based analysis.
