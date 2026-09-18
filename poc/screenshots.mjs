// Captures figures for the paper from the BimOpenFlow web editor's 3D page.
// Requires the host (port 5214) and web editor (port 5300) to be running with the
// poc/store analysis store, and the toolkit's Playwright at ../bim-open-toolkit/viz.
//
//   node poc/screenshots.mjs
//
// Writes PNGs to paper/figures/ and prints the pane status text for each capture.
import { chromium } from "../../bim-open-toolkit/viz/node_modules/playwright-core/index.mjs";
import { mkdir } from "node:fs/promises";
import { resolve } from "node:path";

const base = "http://127.0.0.1:5300";
const out = resolve("paper/figures");
await mkdir(out, { recursive: true });

// [analysis id, pane tab, output file name, whether to capture the whole page]
const captures = [
  ["nrc-storey-carbon-chart", "Chart", "figure-2-storey-carbon-chart.png", true],
  ["nrc-storey-carbon-chart", "Table", "figure-3-storey-carbon-table.png", false],
  ["nrc-property-values", "Table", "figure-4-property-values-table.png", false],
  ["nrc-color-operational-carbon", "3D", "gap-3d-pane-duplex-error.png", false],
];

const browser = await chromium.launch({ channel: "msedge", headless: true, args: ["--enable-unsafe-swiftshader"] });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on("pageerror", e => console.log("PAGE ERROR", e.message));
  await page.goto(base + "/3d.html");
  await page.waitForSelector(".bof-panes-viewstatus", { timeout: 120000 });
  for (const [analysis, tab, file, fullPage] of captures) {
    await page.getByRole("combobox").first().selectOption(analysis);
    await page.waitForTimeout(3000);
    await page.getByText(tab, { exact: true }).last().click();
    await page.waitForTimeout(4000);
    const status = (await page.locator(".bof-panes-viewstatus").textContent({ timeout: 2000 }).catch(() => "")) ?? "";
    await page.screenshot({ path: resolve(out, file), fullPage });
    console.log(`${file}: ${status.trim()}`);
  }
} finally {
  await browser.close();
}
