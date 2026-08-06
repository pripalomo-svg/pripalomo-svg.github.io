const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const RENDER = path.join(__dirname, 'render', 'draw-historia.html');
const FRAMES_DIR = path.join(__dirname, 'frames');
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
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--force-color-profile=srgb','--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
  await page.goto('file://' + RENDER, { waitUntil: 'networkidle0' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await new Promise(r => setTimeout(r, 400));

  const total = await page.evaluate(() => window.__totalDuration);
  const totalFrames = Math.round((total / 1000) * FPS);
  const frameDelay = 1000 / FPS;
  console.log(`total ${total}ms -> ${totalFrames} frames`);

  for (let i = 0; i < totalFrames; i++) {
    const t = Math.round(i * frameDelay);
    await page.evaluate((t) => window.__render(t), t);
    await page.screenshot({ path: path.join(FRAMES_DIR, `frame_${String(i).padStart(5,'0')}.png`), type: 'png' });
    if (i % 96 === 0) console.log(`frame ${i}/${totalFrames}`);
  }
  await browser.close();
  console.log(`done: ${totalFrames} frames`);
}
main().catch(e => { console.error(e); process.exit(1); });
