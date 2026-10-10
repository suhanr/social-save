#!/usr/bin/env node
// Renders 1200x630 social share images (assets/og/<slug>.jpg) from tools/og-manifest.json.
// Run `python3 tools/build.py` first (it writes the manifest), then:
//   node tools/make-og.js
// Needs the `playwright` package and a Chromium build (set CHROMIUM_PATH if needed).
const fs = require("fs");
const os = require("os");
const path = require("path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

const root = path.resolve(__dirname, "..");
const entries = JSON.parse(fs.readFileSync(path.join(root, "tools", "og-manifest.json"), "utf8"));
const font = (f) => "file://" + path.join(root, "assets", "fonts", f);
const img = (f) => "file://" + path.join(root, "assets", "img", f);

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function html({ title, tag }) {
  const size = title.length > 70 ? 54 : title.length > 46 ? 62 : 74;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Outfit;src:url(${font("outfit-latin.woff2")}) format("woff2");font-weight:400 800}
@font-face{font-family:"Work Sans";src:url(${font("worksans-latin.woff2")}) format("woff2");font-weight:400 700}
*{box-sizing:border-box;margin:0}
body{width:1200px;height:630px;overflow:hidden;font-family:"Work Sans",sans-serif;color:#0f172a;position:relative;
background:radial-gradient(60% 70% at 0% 0%,rgba(37,99,235,.18),transparent 70%),radial-gradient(50% 60% at 100% 100%,rgba(225,29,72,.10),transparent 70%),#f8fafc}
.brand{position:absolute;left:72px;top:60px;display:flex;align-items:center;gap:16px;font:700 34px Outfit}
.brand img{width:56px;height:56px;border-radius:16px}
.tag{position:absolute;left:72px;top:176px;font:600 22px "Work Sans";letter-spacing:.08em;text-transform:uppercase;color:#1d4ed8;background:#dbeafe;border:1px solid #bfdbfe;border-radius:999px;padding:8px 18px}
h1{position:absolute;left:72px;top:236px;width:700px;font:700 ${size}px/1.06 Outfit;letter-spacing:-.035em}
.url{position:absolute;left:72px;bottom:56px;font:500 26px "Work Sans";color:#475569}
.phone{position:absolute;right:-70px;bottom:-60px;width:560px;filter:drop-shadow(0 30px 40px rgba(15,23,42,.25))}
</style></head><body>
<div class="brand"><img src="${img("logo.svg")}">Social Save</div>
<div class="tag">${esc(tag)}</div>
<h1>${esc(title)}</h1>
<img class="phone" src="${img("app-mockup-768.webp")}">
<div class="url">socialsave.site</div>
</body></html>`;
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ["--no-sandbox"] });
  const page = await (await browser.newContext({ viewport: { width: 1200, height: 630 } })).newPage();
  const out = path.join(root, "assets", "og");
  fs.mkdirSync(out, { recursive: true });
  for (const e of entries) {
    const tmp = path.join(os.tmpdir(), "social-save-og.html");
    fs.writeFileSync(tmp, html(e));
    await page.goto("file://" + tmp, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(out, e.slug + ".jpg"), type: "jpeg", quality: 82 });
  }
  await browser.close();
  fs.rmSync(path.join(os.tmpdir(), "social-save-og.html"), { force: true });
  console.log(`wrote ${entries.length} images to assets/og/`);
})();
