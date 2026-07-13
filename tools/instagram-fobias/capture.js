const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const RENDER_DIR = path.join(__dirname, 'render');
const FRAMES_DIR = path.join(__dirname, 'frames');
const FPS = 24;
const DURATION_S = 4.5;
const WIDTH = 1080;
const HEIGHT = 1920;

const CHROME_PATH = process.env.CHROME_PATH || '/usr/bin/google-chrome-stable';

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function captureOne(browser, slug) {
  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  const filePath = path.join(RENDER_DIR, `${slug}.html`);
  await page.goto('file://' + filePath, { waitUntil: 'networkidle0' });
  await sleep(200);

  const outDir = path.join(FRAMES_DIR, slug);
  fs.mkdirSync(outDir, { recursive: true });

  const totalFrames = Math.round(FPS * DURATION_S);
  const frameDelayMs = 1000 / FPS;

  const start = Date.now();
  for (let i = 0; i < totalFrames; i++) {
    const target = start + i * frameDelayMs;
    const now = Date.now();
    if (target > now) await sleep(target - now);
    const framePath = path.join(outDir, `frame_${String(i).padStart(4, '0')}.png`);
    await page.screenshot({ path: framePath, type: 'png' });
  }

  await page.close();
  console.log(`captured ${totalFrames} frames for ${slug}`);
}

async function main() {
  const slugsArg = process.argv.slice(2);
  const indexData = JSON.parse(fs.readFileSync(path.join(RENDER_DIR, 'index.json'), 'utf-8'));
  const slugs = slugsArg.length ? slugsArg : indexData.map((f) => f.slug);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      '--force-color-profile=srgb',
      '--hide-scrollbars',
    ],
  });

  for (const slug of slugs) {
    await captureOne(browser, slug);
  }

  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
