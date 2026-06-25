const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

async function main() {
  const outDir = path.resolve(__dirname, "flywheel-store-screens");
  fs.mkdirSync(outDir, { recursive: true });

  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
  const browser = await chromium.launch({
    headless: true,
    executablePath: fs.existsSync(chromePath) ? chromePath : undefined,
  });
  const page = await browser.newPage({
    viewport: { width: 1680, height: 1080 },
    deviceScaleFactor: 1,
  });

  await page.goto(`file://${path.resolve(__dirname, "flywheel-store-screens.html").replace(/\\/g, "/")}`);
  await page.evaluate(() => document.fonts.ready);

  const shots = await page.$$eval(".shot", nodes =>
    nodes.map(node => ({ id: node.id, file: node.dataset.file }))
  );

  for (const shot of shots) {
    const locator = page.locator(`#${shot.id}`);
    await locator.screenshot({
      path: path.join(outDir, `${shot.file}.png`),
      animations: "disabled",
    });
  }

  await browser.close();
  console.log(`Exported ${shots.length} images to ${outDir}`);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
