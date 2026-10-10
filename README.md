# Social Save

A responsive media-tools landing page inspired by the public information architecture of Social Save. Includes a custom-built homepage, link input UX, platform entry points, stock-media section, how-it-works flow, Android promotion, FAQ, journal cards, and footer navigation.

## Run locally

No build tools are required for the current static version. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Current functionality

- Responsive layout and mobile navigation
- URL shape validation for Instagram, Facebook, TikTok and YouTube
- Clear user-facing state for valid links when no API is configured
- Optional JSON API integration using a `meta[name="social-save-api"]` tag
- Reduced-motion support and accessible status updates

## Connect a downloader API

The client looks for:

```html
<meta name="social-save-api" content="https://your-api.example.com/process">
```

When configured, it sends `POST { "url": "https://..." }` with JSON and expects a response shaped like:

```json
{
  "medias": [
    {
      "url": "https://cdn.example.com/media.mp4",
      "quality": "HD",
      "type": "video",
      "extension": "mp4"
    }
  ]
}
```

You must implement and secure the server-side endpoint yourself. Apply SSRF protections, validate supported hostnames after redirects, enforce request limits/timeouts, avoid fetching private or restricted content, rate-limit requests, and respect copyright, platform terms, and applicable law. Do not expose third-party secrets in browser code. The UI intentionally does not pretend to download media while the endpoint is absent.

## Before production

- Configure and verify your permitted backend/API provider.
- Replace the Android app CTA with the official Play Store URL if applicable.
- Add final project-specific Contact, Privacy, and Terms pages.
- Review all platform support and content/licensing claims.
- Test actual API responses, security and deployment configuration.

## Files

- `index.html` — page structure and content
- `styles.css` — styles, visuals, responsive breakpoints
- `app.js` — menu, input validation, optional API call
