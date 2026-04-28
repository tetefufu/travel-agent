# Hotel Price Research — Instructions

When asked to do hotel price research for a destination, follow this process exactly.

---

## Folder Structure

Create a subfolder in the project root named after the destination (lowercase, e.g. `bora bora/`).

```
<destination>/
├── hotels-price-distribution.csv   # All popular hotels × weekday/weekend rates
├── hotel-seasonal-pricing.csv      # 2–3 specific hotels × 12 months
└── scraping-plan.md                # Sources, accessibility notes, Python scraper
```

---

## File 1: hotels-price-distribution.csv

**Purpose:** Price distribution snapshot across hotel tiers. One row per hotel.

**Columns:**
```
Hotel, Stars, Category, Weekday_USD, Weekend_USD, Weekend_Premium_Pct,
Weekday_AED, Weekend_AED, Pool, TripAdvisor_Rating, Source, Notes
```

**What to include:**
- 8–12 hotels covering all tiers: Ultra-luxury · Luxury · Upper-mid · Mid · Budget
- Weekday = Monday–Thursday check-in; Weekend = Friday–Saturday check-in
- Weekend premium is typically 20–40%; calculate as `(Weekend - Weekday) / Weekday`
- AED conversion: multiply USD × 3.67 (verify current rate if significantly changed)
- Pool column: Excellent / Good / Limited / Basic / None
- Source: list booking platform(s) used (e.g. `booking.com / fourseasons.com`)

**Data sources (in order of preference):**
1. Official hotel website (most accurate rack rate)
2. Booking.com individual hotel page
3. Hotels.com / Expedia
4. budgetyourtrip.com for baseline validation

---

## File 2: hotel-seasonal-pricing.csv

**Purpose:** Monthly price variation to identify cheapest/peak months. One row per hotel per month (36 rows for 3 hotels).

**Columns:**
```
Hotel, Month, Month_Num, Avg_Nightly_USD, Avg_Nightly_AED, Season, Notes
```

**What to include:**
- Choose 3 hotels that anchor different tiers: one ultra-luxury, one mid-luxury, one mid-range
- 12 months for each hotel (January → December for the current or next calendar year)
- Season labels: Low · Shoulder · Shoulder-Peak · Peak · Holiday Premium
- Notes: key drivers of price change that month (dry season start, school holidays, local festivals, etc.)

**Seasonal pattern research:**
- Look up the destination's dry/wet season calendar
- Identify school holiday periods (European summer Jul–Aug is peak for most tropical destinations)
- Note local festivals or events that spike demand
- Check December–January for holiday premium

**Data sources:**
1. budgetyourtrip.com/hotels/[country]/[city] — public seasonal averages, static HTML, easiest to scrape
2. farandawayadventures.com — detailed per-resort seasonal breakdowns for many tropical destinations
3. Booking.com monthly calendar view per hotel (requires Playwright)

---

## File 3: scraping-plan.md

**Purpose:** Document all sources used and provide Python scripts to refresh the CSVs programmatically.

**What to include:**
1. Source ranking table: source name · difficulty · tech required · best for · rate limit notes
2. Booking.com direct URLs for the 3 seasonal hotels
3. Python script using `httpx` + `beautifulsoup4` for static sources
4. Python script using `playwright` for Booking.com (JS-heavy)
5. Refresh instructions: how often to re-run, how to merge back into CSVs
6. Anti-bot/legal note

**Source difficulty tiers:**
- EASY: budgetyourtrip.com, static travel blogs — plain httpx + BeautifulSoup, no auth
- MODERATE: TripAdvisor, Booking.com individual pages — Playwright + 5–10s random delays
- HARD: Booking.com at scale — residential proxies required (Bright Data, Apify)
- REQUIRES APPROVAL: Amadeus API, Skyscanner Partners API

---

## General Rules

- Always show prices in both USD and AED (rate: ~3.67 AED/USD)
- Always cover all tiers — luxury travellers need context on where they sit relative to alternatives
- Seasonal CSV must show a clear price curve — flag the cheapest month and the peak month explicitly in Notes
- Scraping scripts must include polite delays (5–10s random) and a realistic User-Agent header
- Note data vintage in the CSV filename or a comment row if prices are more than 3 months old
