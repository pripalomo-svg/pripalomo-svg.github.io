const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const RENDER_DIR = path.join(__dirname, 'render');
const FRAMES_DIR = path.join(__dirname, 'frames', 'minha-historia');
const FPS = 24;
const WIDTH = 1920;
const HEIGHT = 1080;

const CHROME_PATH = process.env.CHROME_PATH || '/usr/bin/google-chrome-stable';

async function main() {
  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
  fs.mkdirSync(FRAMES_DIR, { recursive: true });

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

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(RENDER_DIR, 'minha-historia.html'), { waitUntil: 'networkidle0' });

  const totalDurationMs = await page.evaluate(() => window.__totalDuration);
  const totalFrames = Math.round((totalDurationMs / 1000) * FPS);
  const frameDelayMs = 1000 / FPS;
  console.log(`total duration ${totalDurationMs}ms -> ${totalFrames} frames`);

  for (let i = 0; i < totalFrames; i++) {
    const t = Math.round(i * frameDelayMs);
    await page.evaluate((t) => window.__render(t), t);
    const framePath = path.join(FRAMES_DIR, `frame_${String(i).padStart(5, '0')}.png`);
    await page.screenshot({ path: framePath, type: 'png' });
    if (i % 96 === 0) console.log(`frame ${i}/${totalFrames} (t=${t}ms)`);
  }

  await page.close();
  await browser.close();
  console.log(`done: ${totalFrames} frames`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
