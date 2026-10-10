# Social Save

Static website for https://socialsave.site/: a light-theme, mobile-first site built with plain HTML, CSS and a little JavaScript. No framework and no build step is needed to run it.

- Tool pages: `social-media-downloader/`, `instagram-video-downloader/`, `instagram-reels-downloader/`, `facebook-video-downloader/`, `tiktok-video-downloader/`, `youtube-downloader/`, `youtube-shorts-downloader/`, `photo-downloader/`, `free-stock-media/`
- Journal: `blog/` with 9 guides
- Other pages: `faq/`, `about/`, `contact/`, `privacy-policy/`, `terms/`, `404.html`

## Run locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080. All links are relative, so the pages also work from a sub-path.

## Structure

- `assets/css/main.css` – design tokens and all styles
- `assets/js/main.js` – mobile menu, link validation, scroll reveal, table-of-contents highlight
- `assets/fonts/`, `assets/img/`, `assets/og/` – fonts, images, social share images
- `tools/` – generator (`build.py`), page copy (`content*.py`, `content.json`), audit (`check.py`), share-image script (`make-og.js`)
- `docs/` – SEO checklist, keyword map and off-page playbook
- `CNAME` – custom domain for GitHub Pages (keep this file)

## Edit the pages

Header, footer, schema and meta tags are generated so they stay consistent. Edit the copy in `tools/`, then:

```bash
python3 tools/build.py   # writes pages, sitemap.xml, robots.txt, feed.xml, manifest
python3 tools/check.py   # SEO and integrity audit (titles, canonicals, schema, links, sitemap)
```

After adding a page, regenerate the share images: `node tools/make-og.js` (needs `playwright`).

## SEO

Technical and on-page SEO are in the code. Read `docs/seo-checklist.md` for what is done and what only the site owner can do (HTTPS redirect, Search Console, Play Store URL, contact email), `docs/keyword-map.md` for the page-to-keyword plan, and `docs/off-page-seo.md` for the link-building and brand plan.

## Before production

- `PLAY_URL` in `tools/build.py` is still the placeholder `…id=YOUR_APP_PACKAGE`.
- The downloader pages validate the pasted link and detect the platform, but there is no download backend. Detected links show a notice pointing to the Android app.
- Set `CONTACT_EMAIL` and `SOCIAL_PROFILES` in `tools/build.py` once you have them.
