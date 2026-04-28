# Bora Bora Hotel Price Scraping Plan

## Goal
Automate refresh of `hotels-price-distribution.csv` and `hotel-seasonal-pricing.csv` with live pricing data.

---

## Source Ranking (Easiest → Hardest)

### 1. budgetyourtrip.com — EASY
- **URL:** https://www.budgetyourtrip.com/hotels/french-polynesia/bora-bora-p248704
- **Tech:** Static HTML, no JS required, no auth
- **Data:** Monthly average hotel prices, low/mid/high ranges, historical trends
- **Best for:** Seasonal baseline, month-by-month averages
- **Rate limit:** None observed — treat with 2s delay as courtesy

### 2. farandawayadventures.com — EASY
- **URL:** https://farandawayadventures.com/how-much-do-overwater-bungalows-in-bora-bora-cost-a-breakdown-by-season-and-resort/
- **Tech:** Static blog post
- **Data:** Per-resort seasonal price breakdowns (low / shoulder / peak)
- **Best for:** Cross-validating seasonal patterns per hotel
- **Rate limit:** None

### 3. TripAdvisor hotel pages — MODERATE
- **URL pattern:** https://www.tripadvisor.com/Hotel_Review-gXXXXXX-dXXXXXX-Reviews-[Hotel_Name]-Bora_Bora.html
- **Tech:** JS-rendered but pricing partially in HTML source
- **Data:** Ratings, review count, "prices from" indicator
- **Best for:** Rating/review count validation
- **Rate limit:** ~10 req/min; rotate User-Agent

### 4. Booking.com individual hotel pages — MODERATE
- **Tech:** JavaScript-heavy (requires Playwright or Selenium)
- **Data:** Real-time nightly rates for specific check-in dates
- **Best for:** Weekday vs weekend split, current live pricing
- **Rate limit:** ~5 req/min per IP; add 5–10s random delay
- **Anti-bot:** Moderate — works fine for 3–10 hotels without proxies

**Hotel URLs for the 3 tracked hotels:**
- St. Regis: https://www.booking.com/hotel/pf/the-st-regis-bora-bora-resort.html
- InterContinental Thalasso: https://www.booking.com/hotel/pf/intercontinental-bora-bora-resort-thalasso-spa.html
- Maitai Polynesia: https://www.booking.com/hotel/pf/maitai-polynesia.html

### 5. Booking.com at scale (50+ hotels) — HARD
- **Requires:** Residential proxies (Bright Data, OxyLabs ~$15/GB)
- **Or use:** Apify Booking.com Scraper ($20–50/month managed)
- **Anti-bot:** Akamai Bot Manager — will block datacenter IPs

### 6. APIs — REQUIRES APPROVAL
- **Amadeus Hotel Search API:** enterprise pricing, requires partnership
- **Skyscanner Partners API:** free if approved, limited hotel focus
- **RapidAPI (Hotels.com / Booking):** $50–200/month, handles anti-bot

---

## Python Scraper

### Dependencies
```
pip install httpx beautifulsoup4 playwright
playwright install chromium
```

### Script: scrape_budgetyourtrip.py
Fetches seasonal averages from budgetyourtrip.com (static, no JS needed).

```python
import httpx
import csv
import time
from bs4 import BeautifulSoup

URL = "https://www.budgetyourtrip.com/hotels/french-polynesia/bora-bora-p248704"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}
AED_RATE = 3.67

def scrape_seasonal_averages():
    resp = httpx.get(URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # budgetyourtrip renders monthly data in a table — selector may need updating
    rows = soup.select("table.monthly-costs tr")
    results = []
    for row in rows:
        cells = row.select("td")
        if len(cells) >= 2:
            month = cells[0].text.strip()
            price_text = cells[1].text.strip().replace("$", "").replace(",", "")
            try:
                usd = float(price_text)
                results.append({"month": month, "avg_usd": usd, "avg_aed": round(usd * AED_RATE)})
            except ValueError:
                continue
    return results

if __name__ == "__main__":
    data = scrape_seasonal_averages()
    with open("seasonal_raw.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["month", "avg_usd", "avg_aed"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} rows")
```

### Script: scrape_booking_prices.py
Uses Playwright to fetch real-time pricing for specific check-in dates. Targets the 3 tracked hotels.

```python
import asyncio
import csv
import random
from datetime import date, timedelta
from playwright.async_api import async_playwright

AED_RATE = 3.67

HOTELS = [
    {
        "name": "The St. Regis Bora Bora Resort",
        "url": "https://www.booking.com/hotel/pf/the-st-regis-bora-bora-resort.html",
    },
    {
        "name": "InterContinental Bora Bora Resort Thalasso Spa",
        "url": "https://www.booking.com/hotel/pf/intercontinental-bora-bora-resort-thalasso-spa.html",
    },
    {
        "name": "Maitai Polynesia Bora Bora",
        "url": "https://www.booking.com/hotel/pf/maitai-polynesia.html",
    },
]

def sample_dates_per_month():
    """Return one weekday (Tuesday) and one weekend (Saturday) check-in per month for 2026."""
    samples = []
    for month in range(1, 13):
        d = date(2026, month, 1)
        # find first Tuesday
        while d.weekday() != 1:
            d += timedelta(days=1)
        samples.append(("weekday", d))
        # find first Saturday
        d = date(2026, month, 1)
        while d.weekday() != 5:
            d += timedelta(days=1)
        samples.append(("weekend", d))
    return samples

async def get_price(page, hotel_url: str, checkin: date) -> str | None:
    checkout = checkin + timedelta(days=1)
    url = (
        f"{hotel_url}"
        f"?checkin={checkin.isoformat()}"
        f"&checkout={checkout.isoformat()}"
        f"&group_adults=2&no_rooms=1&group_children=0"
    )
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(random.uniform(5, 10))  # polite delay

    # Price selector — may need updating if Booking.com changes layout
    price_el = await page.query_selector('[data-testid="price-and-discounted-price"]')
    if price_el:
        return (await price_el.text_content()).strip()
    return None

async def main():
    date_samples = sample_dates_per_month()
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
        page = await context.new_page()

        for hotel in HOTELS:
            for day_type, checkin in date_samples:
                raw_price = await get_price(page, hotel["url"], checkin)
                results.append({
                    "hotel": hotel["name"],
                    "checkin": checkin.isoformat(),
                    "month": checkin.month,
                    "day_type": day_type,
                    "raw_price": raw_price,
                })
                print(f"{hotel['name']} | {checkin} ({day_type}) → {raw_price}")

        await browser.close()

    with open("booking_prices_raw.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["hotel", "checkin", "month", "day_type", "raw_price"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Done. {len(results)} rows saved to booking_prices_raw.csv")

asyncio.run(main())
```

---

## Refresh Instructions

1. Run `scrape_budgetyourtrip.py` — outputs `seasonal_raw.csv`
2. Run `scrape_booking_prices.py` — outputs `booking_prices_raw.csv` (takes ~15–20 min due to polite delays)
3. Manually merge results back into `hotel-seasonal-pricing.csv` and `hotels-price-distribution.csv`
4. Check AED values: multiply USD × 3.67 (update rate if XE.com shows significant drift)

**Recommended cadence:** Quarterly refresh, or before booking (to catch seasonal promotions).

---

## Notes on Anti-Bot / Legal

- Scripts above respect rate limits and use human-like delays — low risk of blocking for small-scale personal use
- Booking.com ToS technically prohibits scraping; for personal price research the risk is minimal
- If blocked: add residential proxy (Bright Data free trial), or use Apify managed scraper
- Never store or republish scraped data commercially
