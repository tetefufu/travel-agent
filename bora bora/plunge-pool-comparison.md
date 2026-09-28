# Plunge pool availability & price premium — Bora Bora hotels

Research date: 2026-09-27 (Westin and Conrad re-verified same day via direct live queries on marriott.com and hilton.com — see verification note below). Covers all 7 hotels currently tracked (St. Regis, Four Seasons, Westin, Conrad, InterContinental Le Moana, Le Bora Bora by Pearl Resorts, Maitai Polynesia). Excludes Royal Bora Bora and Village Temanuata (no overwater bungalows at all — see `research-decisions.md`) and InterContinental Thalasso Spa (closed for renovation since 2026-06-01 — its plunge-pool "Overwater Pool Villas" exist but the hotel can't currently be booked).

## Summary table

| Hotel | Plunge pool available? | Pool room name | Pool price (AED/night) | Non-pool comparison (same week) | Premium | Confidence |
|---|---|---|---|---|---|---|
| **Four Seasons** | Yes | Beach-View Overwater Suite with Plunge Pool | 7,769 | Beach-View Overwater Bungalow Suite: 6,457 | **+20.3%** | High — both real prices, same week, same suite tier, direct site (`four-seasons-weekly-rates-2027.csv`) |
| **Westin** | Yes — confirmed live on marriott.com | Otemanu Overwater w/Pool: **7,164** AED/night ($1,952) | Otemanu View Overwater (same view tier, non-pool): **6,758** AED/night ($1,841) | **+6.0%** | **High** — both real live prices, same week (Mon 10–Sat 15 May 2027), same Otemanu view tier, direct marriott.com booking engine. Supersedes the old scaled estimate entirely |
| **St. Regis** | Yes | Overwater Royal Villa (1BR) w/ Pool | 18,361 | Overwater Superior: 7,736 | +137% | Medium — both real prices, same week (`st-regis-weekly-rates-2027.csv`), but Royal is a whole different tier (bigger villa, more amenities), not a pure "add a pool" upgrade — treat this premium as tier-jump, not pool-add-on cost |
| **Conrad Bora Bora Nui** | Yes — confirmed live on hilton.com (13 room categories) | King Overwater Pool Villa: **11,570** AED/night ($3,153) | True overwater non-pool ("King Overwater Villa") was **sold out** in both weeks checked (10–15 May and 24–29 May 2027) — closest true apples-to-apples pair is same-tier beach: King Tropical Beach View Villa **10,402** AED/night vs King Tropical Beach View Villa **with Pool** 10,543 AED/night | **+1.4%** (beach-tier proxy; true overwater pool premium unmeasurable this round — base overwater villa unavailable) | **Medium** — pool price and room-name are now live-verified (not a judgment call), but the non-pool overwater baseline is a persistent no-availability across 2 separate weeks, so the premium % uses a beach-tier proxy, not overwater-to-overwater |
| **Le Bora Bora by Pearl Resorts** | Yes — confirmed ("Pool Overwater Villa" — only 4 units, glass-bottom bed, Otemanu view) | Pool Overwater Villa | **Not found** — no public rate on official site | Bungalow, Lagoon View, Overwater (breakfast incl.): 8,014 | Unknown | Gap — needs a live date-specific quote (site is JS-rendered; static fetch shows no price) |
| **InterContinental Le Moana** | **No** — confirmed. Its basic overwater bungalows have no private plunge pool; that feature belongs to the sister property (Thalasso Spa), which is currently closed for renovation | — | — | — | N/A | High |
| **Maitai Polynesia** | **No** — confirmed. Its 10 overwater bungalows have no private pools or glass floors, and the property has no pool at all | — | — | — | N/A | High |

## Verification note (2026-09-27 follow-up)

Went direct to hilton.com and marriott.com (live booking engines, not Google's aggregator) for Conrad and Westin, at the query's request to raise confidence on these two:

- **Westin**: marriott.com's own rate list for Mon 10–Sat 15 May 2027, 2 adults, returned all 11 room categories with real per-night USD prices. This gave a clean same-view-tier comparison (Otemanu View Overwater vs. Otemanu Overwater w/Pool) that didn't exist before — confidence upgraded from Low to High, and the old derived/scaled estimate is now superseded.
- **Conrad**: hilton.com's rate list for the same week returned 13 room categories with real per-night XPF prices (confirming exact names: "King Overwater Pool Villa," "King Tropical Beach View Villa," etc.). This confirmed the room-naming judgment call from the earlier Google Travel pass was directionally correct, and gave a true same-tier (beach) pool-vs-non-pool pair. However, the true overwater non-pool room ("King Overwater Villa") showed **Room Not Available** in both 10–15 May and 24–29 May 2027 — checked two separate weeks with the identical result, so this isn't a one-off; it's either persistently sold out this far out or held back from standard booking. The overwater-specific premium therefore still can't be directly measured — only the beach-tier proxy (+1.4%) is confirmed apples-to-apples.

## Takeaways

- **Westin now has the second-cleanest number** (after Four Seasons): a real +6.0% same-tier premium, replacing what used to be the weakest data point in this file.
- **Four Seasons remains the cleanest**: ~20% more per night for the plunge-pool upgrade, same suite tier.
- **St. Regis's "pool" option isn't a simple upgrade** — it jumps to the Royal Villa tier entirely (bigger villa, more space), so the +137% reflects a category change, not a pool add-on cost.
- **Conrad's pool price is now solid, but its premium % is still a proxy** — the base overwater (non-pool) room won't show as available no matter which week is queried, so a true overwater-to-overwater comparison remains out of reach with current inventory.
- **Le Bora Bora has a genuine plunge-pool room but no discoverable price** — worth a dedicated live check if this hotel makes the shortlist.
- **Two hotels flatly don't have the option**: InterContinental Le Moana and Maitai Polynesia.
