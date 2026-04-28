"""
Scrapes real DXB→PPT flight prices from Google Flights via fast-flights.
No API key required.

Routes:
  Most Direct  — single DXB→PPT query (fetch_mode=local, uses Playwright)
  Via California — DXB→LAX + LAX→PPT summed (fetch_mode=common, fast)

Output: flights-price-research.csv  (72 rows: 2 routes × 3 cabins × 12 months)
Note: prices are DXB→PPT (Papeete). Add ~550 AED for PPT→BOB Air Tahiti domestic.

Usage:
  pip install fast-flights playwright
  playwright install chromium
  python "scrape_flights.py"
"""

import csv
import re
import time
import random
from datetime import date, timedelta
from pathlib import Path

from fast_flights import FlightData, Passengers, get_flights

AED_RATE = 3.67

CABINS = [
    ("economy",         "Economy"),
    ("premium-economy", "Premium Economy"),
    ("business",        "Business"),
]

FIELDNAMES = [
    "Route_Type", "Cabin", "Month", "Month_Num", "Sample_Date",
    "Airlines", "Stops", "Duration_Hours", "Price_AED", "Notes", "Scraped_Date",
]


def second_tuesday(year: int, month: int) -> date:
    d = date(year, month, 1)
    while d.weekday() != 1:
        d += timedelta(days=1)
    return d + timedelta(weeks=1)


def sample_dates() -> list[date]:
    today = date.today()
    year, month = today.year, today.month + 1
    if month > 12:
        month, year = 1, year + 1
    dates = []
    for _ in range(12):
        dates.append(second_tuesday(year, month))
        month += 1
        if month > 12:
            month, year = 1, year + 1
    return dates


def parse_duration(duration_str: str) -> float | None:
    """'42 hr 50 min' → 42.83"""
    m = re.match(r"(\d+)\s*hr(?:\s*(\d+)\s*min)?", duration_str or "")
    if not m:
        return None
    return float(m.group(1)) + (int(m.group(2)) / 60 if m.group(2) else 0)


def parse_price(price_val) -> int | None:
    """'AED 3,115' or 3115 or 'AED3115' → 3115"""
    s = str(price_val).replace(",", "").replace("AED", "").strip()
    try:
        return int(s) if s else None
    except ValueError:
        return None


def best_flight(results):
    """Pick cheapest valid flight from a result set."""
    valid = [f for f in results.flights if parse_price(f.price) and parse_price(f.price) > 0 and f.name]
    if not valid:
        return None
    return min(valid, key=lambda f: parse_price(f.price))


def query(frm: str, to: str, dt: date, seat: str, mode: str):
    return get_flights(
        flight_data=[FlightData(date=dt.strftime("%Y-%m-%d"), from_airport=frm, to_airport=to)],
        trip="one-way",
        seat=seat,
        passengers=Passengers(adults=1),
        fetch_mode=mode,
    )


def collect_row(route_type: str, cabin_label: str, sample_date: date, flight, notes: str) -> dict:
    today = date.today().isoformat()
    if flight:
        price = parse_price(flight.price)
        dur = parse_duration(flight.duration)
        return {
            "Route_Type":     route_type,
            "Cabin":          cabin_label,
            "Month":          sample_date.strftime("%B"),
            "Month_Num":      sample_date.month,
            "Sample_Date":    sample_date.isoformat(),
            "Airlines":       flight.name or "Unknown",
            "Stops":          flight.stops if flight.stops != "Unknown" else "?",
            "Duration_Hours": f"{dur:.1f}" if dur else "?",
            "Price_AED":      price,
            "Notes":          notes,
            "Scraped_Date":   today,
        }
    return {
        "Route_Type":     route_type,
        "Cabin":          cabin_label,
        "Month":          sample_date.strftime("%B"),
        "Month_Num":      sample_date.month,
        "Sample_Date":    sample_date.isoformat(),
        "Airlines":       "N/A",
        "Stops":          "N/A",
        "Duration_Hours": "N/A",
        "Price_AED":      "N/A",
        "Notes":          notes,
        "Scraped_Date":   today,
    }


def save(rows: list, path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main():
    output = Path(__file__).parent / "flights-price-research.csv"
    dates = sample_dates()
    all_rows: list[dict] = []

    print(f"Collecting DXB→PPT prices: {len(dates)} months × {len(CABINS)} cabins")
    print(f"Most Direct uses Playwright (slow ~20s/query); Via California is fast.\n")

    for sample_date in dates:
        for seat_key, cabin_label in CABINS:
            tag = f"{sample_date.strftime('%b %Y')} / {cabin_label}"
            print(f"  {tag}...", end=" ", flush=True)

            # — Most Direct: single DXB→PPT via local Playwright —
            direct_row = None
            try:
                r = query("DXB", "PPT", sample_date, seat_key, "local")
                f = best_flight(r)
                direct_row = collect_row(
                    "Most Direct", cabin_label, sample_date, f,
                    "+PPT→BOB domestic ~550 AED (Air Tahiti, not included)"
                )
            except Exception as e:
                direct_row = collect_row("Most Direct", cabin_label, sample_date, None, f"Error: {e}")

            time.sleep(random.uniform(1.5, 2.5))

            # — Via California: DXB→LAX + LAX→PPT (common mode, fast) —
            via_row = None
            try:
                r1 = query("DXB", "LAX", sample_date, seat_key, "common")
                r2 = query("LAX", "PPT", sample_date, seat_key, "common")
                f1 = best_flight(r1)
                f2 = best_flight(r2)

                if f1 and f2:
                    p1 = parse_price(f1.price)
                    p2 = parse_price(f2.price)
                    combined_price = p1 + p2
                    d1 = parse_duration(f1.duration)
                    d2 = parse_duration(f2.duration)
                    dur = f"{(d1 + d2):.1f}" if d1 and d2 else "?"
                    via_row = {
                        "Route_Type":     "Via California",
                        "Cabin":          cabin_label,
                        "Month":          sample_date.strftime("%B"),
                        "Month_Num":      sample_date.month,
                        "Sample_Date":    sample_date.isoformat(),
                        "Airlines":       f"{f1.name} + {f2.name}",
                        "Stops":          f"{f1.stops}+{f2.stops}",
                        "Duration_Hours": dur,
                        "Price_AED":      combined_price,
                        "Notes":          f"DXB→LAX {p1} AED ({f1.name}) + LAX→PPT {p2} AED ({f2.name}). Two tickets. +PPT→BOB ~550 AED.",
                        "Scraped_Date":   date.today().isoformat(),
                    }
                else:
                    via_row = collect_row("Via California", cabin_label, sample_date, None, "No results on one or both legs")
            except Exception as e:
                via_row = collect_row("Via California", cabin_label, sample_date, None, f"Error: {e}")

            all_rows.extend([direct_row, via_row])

            d_price = direct_row.get("Price_AED", "N/A")
            v_price = via_row.get("Price_AED", "N/A")
            print(f"Direct: {d_price} AED | Via LAX: {v_price} AED")

            save(all_rows, output)
            time.sleep(random.uniform(1.0, 2.0))

    na = sum(1 for r in all_rows if r["Price_AED"] == "N/A")
    print(f"\n{'─'*60}")
    print(f"Done. {len(all_rows)} rows → {output}")
    if na:
        print(f"N/A rows: {na} — check Notes column")


if __name__ == "__main__":
    main()
