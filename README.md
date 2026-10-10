# Social Save

Static website for Social Save: a light-theme, mobile-first UI built with plain HTML, CSS and a little JavaScript. No framework and no build step is needed to run it.

Pages: home, `social-media-downloader/`, `youtube-downloader/`, `free-stock-media/`, `blog/`, `about/`, `contact/`, `privacy-policy/`, `terms/`.

## Run locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080. All links are relative, so the site also works from a sub-path such as GitHub Pages at `/social-save/`.

## Structure

- `assets/css/main.css` – design tokens (colors, type, radii, shadows) and all styles
- `assets/js/main.js` – mobile menu, link validation, scroll reveal, table-of-contents highlight
- `assets/fonts/` – self-hosted Outfit and Work Sans (latin)
- `assets/img/` – logo, app mockup, Google Play badge
- `tools/build.py` + `tools/content.json` – generator for the HTML pages

## Edit the pages

Header, footer and page copy are generated so they stay identical on every page. Edit `tools/build.py` (home and tool pages) or `tools/content.json` (about, contact, privacy, terms), then run:

```bash
python3 tools/build.py
```

## Before production

- `PLAY_URL` in `tools/build.py` is still the placeholder `https://play.google.com/store/apps/details?id=YOUR_APP_PACKAGE`. Replace it with the real Play Store listing and rebuild.
- The downloader pages validate the pasted link and detect the platform, but this site has no download backend. Detected links show a notice pointing to the Android app. Connect a backend before promising online downloads.
- The Contact page lists no email address or form. Add a contact channel.
- `canonical` and `og:image` still point to https://socialsave.site/. Update them for the final domain.
