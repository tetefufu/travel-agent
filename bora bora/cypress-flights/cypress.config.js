const { defineConfig } = require("cypress");
const fs = require("fs");
const path = require("path");

const CSV_PATH = path.join(__dirname, "..", "flights-price-research.csv");
const HEADERS = "Route_Type,Cabin,Month,Month_Num,Sample_Date,Airlines,Stops,Layover_Cities,Duration_Hours,Price_AED,Price_USD,Notes,Scraped_Date";

module.exports = defineConfig({
  e2e: {
    specPattern: "cypress/e2e/**/*.cy.js",
    defaultCommandTimeout: 30000,
    pageLoadTimeout: 60000,
    chromeWebSecurity: false,
    setupNodeEvents(on) {
      on("task", {
        initCSV() {
          fs.writeFileSync(CSV_PATH, HEADERS + "\n");
          return null;
        },
        appendRows({ rows }) {
          const lines = rows.map((r) =>
            [
              r.route_type, r.cabin, r.month, r.month_num, r.sample_date,
              `"${r.airlines}"`, r.stops, `"${r.layovers}"`, r.duration_hours,
              r.price_aed, r.price_usd, `"${r.notes}"`, r.scraped_date,
            ].join(",")
          );
          fs.appendFileSync(CSV_PATH, lines.join("\n") + "\n");
          console.log(`  Appended ${rows.length} rows`);
          return null;
        },
      });
    },
  },
});
