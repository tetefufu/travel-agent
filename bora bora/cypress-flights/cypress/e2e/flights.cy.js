const flightUrls = require("../../flight-urls.json");
const AED_RATE = 3.67;
const TODAY = new Date().toISOString().split("T")[0];

// Parse flight result text blocks into structured data.
// Each result block looks like:
//   "Emirates\n7:15 AM – 4:20 PM\n23 hr 5 min\n2 stops\nAED 3,450"
function parseResults(bodyText) {
  const results = [];
  // Find all AED prices in the page text
  const priceMatches = [...bodyText.matchAll(/AED[\s ]*([\d,]+)/g)];
  // Find airline names before price blocks (rough heuristic)
  const flightBlocks = bodyText.split(/\n{2,}/);

  for (const block of flightBlocks) {
    const priceMatch = block.match(/AED[\s ]*([\d,]+)/);
    if (!priceMatch) continue;

    const priceAed = parseInt(priceMatch[1].replace(/,/g, ""), 10);
    const priceUsd = Math.round(priceAed / AED_RATE);
    const stopsMatch = block.match(/(\d+)\s+stop/i);
    const stops = stopsMatch ? parseInt(stopsMatch[1], 10) : (block.toLowerCase().includes("nonstop") ? 0 : null);
    const durationMatch = block.match(/(\d+)\s+hr(?:\s+(\d+)\s+min)?/);
    const durationHours = durationMatch
      ? parseFloat(durationMatch[1]) + (durationMatch[2] ? parseInt(durationMatch[2], 10) / 60 : 0)
      : null;

    // Extract airline(s): lines that don't contain digits or common labels
    const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
    const airlines = lines
      .filter((l) => /^[A-Z][a-z]/.test(l) && !/^\d|AM|PM|hr|min|stop|AED|Best|Cheapest/.test(l))
      .slice(0, 2)
      .join(" / ") || "Unknown";

    // Extract layover airports (3-letter caps codes in parentheses or standalone)
    const layovers = [...block.matchAll(/\b([A-Z]{3})\b/g)]
      .map((m) => m[1])
      .filter((c) => !["AED", "AM", "PM"].includes(c) && c !== "DXB" && c !== "PPT")
      .filter((v, i, a) => a.indexOf(v) === i)
      .join(" → ") || "—";

    results.push({ priceAed, priceUsd, stops, durationHours, airlines, layovers });
  }

  // Sort: fewer stops first, then price
  results.sort((a, b) => (a.stops ?? 99) - (b.stops ?? 99) || a.priceAed - b.priceAed);
  return results;
}

describe("DXB→PPT Flight Prices", () => {
  before(() => {
    cy.task("initCSV");
  });

  // Run all 36 queries in one test to avoid per-test browser launch overhead
  it("collects prices for all months and cabins", () => {
    // Process sequentially via recursive chaining
    function processNext(index) {
      if (index >= flightUrls.length) return;
      const flight = flightUrls[index];

      cy.log(`[${index + 1}/${flightUrls.length}] ${flight.month} ${flight.year} / ${flight.cabin}`);

      cy.visit(flight.url, { failOnStatusCode: false });

      // Wait up to 25s for prices to appear
      cy.get("body").should(($body) => {
        expect($body.text()).to.match(/AED[\s ]*[\d,]{3}/);
      }, { timeout: 25000 }).then(() => {
        cy.get("body").invoke("text").then((bodyText) => {
          const parsed = parseResults(bodyText);

          const mostDirect = parsed[0] || null;
          // Via California = cheapest result that has LAX in its layovers
          const viaLax = parsed.find((r) => r.layovers.includes("LAX")) || null;

          const makeRow = (routeType, r) => ({
            route_type: routeType,
            cabin: flight.cabin,
            month: flight.month,
            month_num: flight.month_num,
            sample_date: flight.sample_date,
            airlines: r ? r.airlines : "N/A",
            stops: r ? r.stops ?? "?" : "N/A",
            layovers: r ? r.layovers : "N/A",
            duration_hours: r ? (r.durationHours ? r.durationHours.toFixed(1) : "?") : "N/A",
            price_aed: r ? r.priceAed : "N/A",
            price_usd: r ? r.priceUsd : "N/A",
            notes: r ? "+PPT→BOB domestic ~550 AED (Air Tahiti)" : `No ${routeType} result`,
            scraped_date: TODAY,
          });

          const rows = [
            makeRow("Most Direct", mostDirect),
            makeRow("Via California", viaLax),
          ];

          cy.task("appendRows", { rows });
          cy.log(`  Most Direct: ${mostDirect ? mostDirect.priceAed + " AED" : "N/A"} | Via LAX: ${viaLax ? viaLax.priceAed + " AED" : "N/A"}`);
        });
      });

      // Wait between queries to be polite
      cy.wait(2000).then(() => processNext(index + 1));
    }

    processNext(0);
  });
});
