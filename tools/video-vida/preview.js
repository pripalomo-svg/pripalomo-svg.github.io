const puppeteer = require('puppeteer-core');
const path = require('path');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: 'new',
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'render', 'vida.html'), { waitUntil: 'networkidle0' });
  const times = [0, 500, 6000, 11500, 19000, 30000, 42000, 55000, 66000, 77000, 86000, 91000];
  for (const t of times) {
    await page.evaluate((t) => window.__render(t), t);
    await page.screenshot({ path: `/tmp/vida_preview_${t}.png` });
  }
  await browser.close();
})();
