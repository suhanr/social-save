# SEO checklist

Status of technical, on-page and off-page SEO for https://socialsave.site/. Nobody can promise a number-one ranking: search results depend on competition, authority (links and brand), content quality and user behaviour. This checklist covers everything that can be done in the codebase, and lists what only the site owner can do.

## Done in the code

### Technical
- [x] One canonical URL per page (`https://socialsave.site/…/`), trailing-slash consistent, `hreflang` en and x-default
- [x] `robots.txt` (allow all, points to the sitemap) and `sitemap.xml` with `lastmod` for all 25 pages
- [x] `404.html` (noindex) with links back to the main tools
- [x] RSS feed `feed.xml`, advertised with `<link rel="alternate">`
- [x] Robots meta with `max-image-preview:large`, `max-snippet:-1`, `max-video-preview:-1`
- [x] Open Graph and Twitter cards with a unique 1200×630 image for every page (`assets/og/`)
- [x] Structured data (JSON-LD `@graph`): Organization, WebSite, WebPage / AboutPage / ContactPage / CollectionPage, BreadcrumbList, FAQPage, BlogPosting, ItemList, SoftwareApplication (home)
- [x] Web app manifest, favicon.ico (16/32/48), SVG favicon, apple-touch-icon, 192 and 512 px icons
- [x] Responsive hero image (`srcset`, `sizes`, preload), explicit image dimensions, self-hosted fonts with `font-display: swap`, no third-party requests
- [x] Semantic HTML: one `h1` per page, ordered headings, landmarks, skip link, descriptive link text, alt text
- [x] Accessibility audit with axe-core: no violations (WCAG 2.1 A/AA)
- [x] All links relative (works on any base path); build fails on a broken internal link target

### On-page
- [x] Unique title (about 60 characters) and meta description (about 155 characters) per page
- [x] Keyword map: each page targets one primary intent (see `keyword-map.md`)
- [x] 6 new landing pages (Instagram video, Instagram Reels, Facebook video, TikTok video, YouTube Shorts, photos), plus richer content on the 3 existing tool pages
- [x] 9 Journal guides, each with its own FAQ and schema, written to answer real questions
- [x] FAQ page (12 questions) with FAQPage schema
- [x] Internal linking: footer link groups on every page, related tools and guides blocks, contextual links in copy, breadcrumbs
- [x] E-E-A-T basics: About, Contact, Privacy Policy, Terms, honest limits stated on every tool page

## Needs the site owner

Do these in order. The first three have the biggest effect.

1. **Turn on HTTPS redirects.** `http://socialsave.site/` currently answers 200 instead of redirecting to HTTPS.
   - GitHub: repository Settings → Pages → tick **Enforce HTTPS**.
   - Cloudflare (the domain is behind it): SSL/TLS → Edge Certificates → **Always Use HTTPS** on. Use SSL/TLS mode **Full** or **Full (strict)**.
2. **Purge the Cloudflare cache.** `https://socialsave.site/robots.txt` still returns the old WordPress/Yoast file from before the move. After deploying this repo, purge the cache for `robots.txt` (Caching → Configuration → Purge). Then open the URL and check it lists `sitemap.xml`.
3. **Verify the site in Google Search Console** (Domain property, using a DNS TXT record, covers http, https and www) and submit `https://socialsave.site/sitemap.xml`. Use URL Inspection → Request indexing for the home page and the main tool pages. Optional: paste the HTML-tag token into `VERIFICATION["google-site-verification"]` in `tools/build.py` and rebuild.
4. **Verify in Bing Webmaster Tools** (you can import the site from Search Console). Bing also feeds other search engines. Optional: set up IndexNow for instant URL submissions.
5. **Set the real Google Play URL.** `PLAY_URL` in `tools/build.py` is still the placeholder `…id=YOUR_APP_PACKAGE`. A working store link is a conversion and trust signal, and lets the app listing link back to the site. When you have it, the home page schema can also carry `installUrl`.
6. **Add a real contact channel.** Set `CONTACT_EMAIL` in `tools/build.py` (it appears on the Contact page and in the Organization schema). Pages with no way to reach the owner are weaker for trust.
7. **Add real social profiles** (only ones you will maintain) to `SOCIAL_PROFILES` in `tools/build.py`. They become `sameAs` links in the schema.
8. **Decide what to do with the old WordPress URLs.** Before the move the domain had hundreds of posts (jobs circulars, rates, captions, etc.). They now return 404 because the new site is a different, static site. Google will drop them over time. If any of them had traffic or backlinks you want to keep, use Cloudflare Redirect Rules or Bulk Redirects to send each old URL to the closest relevant page (or the home page), because GitHub Pages cannot do server-side redirects. If the old content no longer matters, do nothing.
9. **Make the downloader actually work.** The online tool detects the platform but does not download yet. Search engines and visitors reward pages that deliver what they promise, and a working tool is the single strongest on-page signal for these keywords. When the backend exists, add `WebApplication` structured data to the tool pages and update the wording on them.
10. **Follow the off-page plan** in `off-page-seo.md`.

## After launch

- Search Console: check Pages (indexing), Sitemaps, Performance (queries and pages), Core Web Vitals and Enhancements (breadcrumbs, FAQ) weekly for the first month.
- Update `BUILD_DATE` and post dates in the code when you change a page, then run `python3 tools/build.py`, so `lastmod` stays honest.
- Add new guides from the backlog in `keyword-map.md` regularly (one or two a month beats a burst).
- Re-run the OG image script after adding pages: `node tools/make-og.js`.
