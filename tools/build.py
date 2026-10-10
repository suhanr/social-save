#!/usr/bin/env python3
"""Generate the Social Save static pages.

Usage (from the repo root):  python3 tools/build.py

Copy lives in tools/content.json (about, contact, privacy, terms) and in this
file (home and tool pages). Styles are in assets/css/main.css, behaviour in
assets/js/main.js. Every link is relative, so the site works from any base path
(for example GitHub Pages at /social-save/).
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "tools", "content.json"), encoding="utf-8"))
BRAND = DATA["brand"]

# TODO: replace with the real Play Store listing (this placeholder comes from the original site).
PLAY_URL = "https://play.google.com/store/apps/details?id=YOUR_APP_PACKAGE"
SITE = "https://socialsave.site/"

# ---------------------------------------------------------------- icons
LUCIDE = {
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up-right": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "sparkles": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17v4"/><path d="M17 19h4"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "film": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "life-buoy": '<circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
}
BRAND_CLASS = {"instagram": "ig", "facebook": "fb", "tiktok": "tt", "youtube": "yt"}


def icon(name, cls=""):
    c = f"icon {cls}".strip()
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{LUCIDE[name]}</svg>'


def brand(name, label=None):
    cls = f"icon icon-fill {BRAND_CLASS[name]}"
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 24 24" {aria}><path d="{BRAND[name]}"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- layout
NAV = [
    ("Social Media", "social-media-downloader/", {"social-media-downloader", "youtube-downloader"}),
    ("Stock Media", "free-stock-media/", {"free-stock-media"}),
    ("Journal", "blog/", {"blog"}),
    ("About", "about/", {"about"}),
]

DESC = {
    "home": DATA["meta"]["home"]["description"],
    "social-media-downloader": "Paste a link from Instagram, Facebook, TikTok or YouTube and save supported videos, Reels, Shorts and photos with Social Save.",
    "youtube-downloader": "Save supported YouTube videos and Shorts with Social Save. Copy the link, paste it and choose the available download option.",
    "free-stock-media": "Discover and download supported free stock photos and stock videos for creative and personal projects with Social Save.",
    "blog": "The Social Save journal.",
    "about": "Social Save is a simple media downloading platform for supported social media videos, Reels, Shorts, photos and free stock media.",
    "contact": "Contact Social Save for technical support, feedback and suggestions, or to report a problem with a downloader tool or the Android app.",
    "privacy-policy": DATA["meta"]["privacy-policy"]["description"],
    "terms": DATA["meta"]["terms"]["description"],
}
TITLES = {
    "home": DATA["meta"]["home"]["title"],
    "social-media-downloader": "Social Media Downloader – Social Save",
    "youtube-downloader": "YouTube Downloader – Social Save",
    "free-stock-media": "Free Stock Media – Social Save",
    "blog": "Journal – Social Save",
    "about": DATA["meta"]["about"]["title"],
    "contact": DATA["meta"]["contact"]["title"],
    "privacy-policy": DATA["meta"]["privacy-policy"]["title"],
    "terms": DATA["meta"]["terms"]["title"],
}

LD_JSON = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Social Save",
    "url": SITE,
    "description": "Social Save is a social media downloader for saving videos, Reels, Shorts and photos.",
    "applicationCategory": "MultimediaApplication",
    "operatingSystem": "Android",
}


def play_badge(root, cls=""):
    return (
        f'<a class="play-badge {cls}" href="{PLAY_URL}" rel="noopener">'
        f'<img src="{root}assets/img/google-play-badge.png" alt="Get it on Google Play" width="162" height="48"></a>'
    )


def header(root, slug):
    items, mobile = "", ""
    for label, href, slugs in NAV:
        cur = ' aria-current="page"' if slug in slugs else ""
        items += f'<li><a href="{root}{href}"{cur}>{label}</a></li>'
        mobile += f'<li><a href="{root}{href}"{cur}>{label}{icon("arrow-right")}</a></li>'
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{root or './'}" aria-label="Social Save home">
      <img src="{root}assets/img/logo.svg" alt="" width="38" height="38">
      <span class="brand-name">Social Save</span>
    </a>
    <nav class="nav" aria-label="Main navigation"><ul>{items}</ul></nav>
    <div class="header-cta">{play_badge(root)}</div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-panel" aria-label="Open menu">
      <svg class="icon icon-open" viewBox="0 0 24 24" aria-hidden="true">{LUCIDE["menu"]}</svg>
      <svg class="icon icon-close" viewBox="0 0 24 24" aria-hidden="true">{LUCIDE["x"]}</svg>
    </button>
  </div>
  <div class="mobile-panel" id="mobile-panel">
    <nav aria-label="Mobile navigation"><ul>{mobile}</ul></nav>
    <div class="panel-cta">{play_badge(root)}</div>
  </div>
</header>"""


def footer(root):
    def li(label, href):
        return f'<li><a href="{root}{href}">{label}</a></li>'

    tools = "".join(
        li(l, h)
        for l, h in [
            ("Social Media Video Downloader", "social-media-downloader/"),
            ("Instagram Reel Video Downloader", "social-media-downloader/"),
            ("Facebook Video and Reel Downloader", "social-media-downloader/"),
            ("TikTok Video Downloader", "social-media-downloader/"),
            ("YouTube Video and Shorts Downloader", "youtube-downloader/"),
        ]
    )
    stock = "".join(
        li(l, h)
        for l, h in [
            ("Free Stock Media Downloader", "free-stock-media/"),
            ("Free Stock Photos Downloader", "free-stock-media/#photos"),
            ("Free Stock Videos Downloader", "free-stock-media/#videos"),
        ]
    )
    company = "".join(li(l, h) for l, h in [("Journal", "blog/"), ("About", "about/"), ("Contact", "contact/"), ("Privacy", "privacy-policy/"), ("Terms", "terms/")])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{root or './'}"><img src="{root}assets/img/logo.svg" alt="" width="38" height="38"><span class="brand-name">Social Save</span></a>
        <p>A simple place to save videos, Reels and Shorts, photos and free stock media from the web.</p>
      </div>
      <div class="footer-col"><h2>Tools</h2><ul>{tools}</ul></div>
      <div class="footer-col"><h2>Stock Media</h2><ul>{stock}</ul></div>
      <div class="footer-col"><h2>Company</h2><ul>{company}</ul></div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Social Save. All rights reserved.</span>
      <ul>
        <li><a href="{root}privacy-policy/">Privacy Policy</a></li>
        <li><a href="{root}terms/">Terms of Use</a></li>
        <li><a href="{root}contact/">Contact</a></li>
      </ul>
    </div>
  </div>
</footer>"""


def page(slug, path, body, extra_head=""):
    root = "../" * (path.count("/")) if path else ""
    canonical = SITE + path
    og_img = DATA["og_image"]
    t, d = esc(TITLES[slug]), esc(DESC[slug])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#f8fafc">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Social Save">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{root}assets/img/logo.svg">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/worksans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/main.css">
{extra_head}</head>
<body>
{header(root, slug)}
<main id="main">
{body}
</main>
{footer(root)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks
def link_form(root, *, action=None, live=False, only=None, other=None, input_id="link", placeholder="Paste a link from Instagram, Facebook, TikTok or YouTube", button="Save"):
    attrs = ' novalidate'
    if live:
        attrs += f' data-live data-badge="{PLAY_URL}" data-badge-img="{root}assets/img/google-play-badge.png"'
    if only:
        attrs += f' data-only="{only}"'
    if other:
        attrs += f' data-other="{other}"'
    act = f' action="{action}" method="get"' if action else ""
    return f"""<form class="link-form"{act}{attrs}>
  <label class="sr-only" for="{input_id}">Paste a public media link</label>
  <div class="link-field">
    {icon("link")}
    <input id="{input_id}" name="u" type="text" inputmode="url" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="{placeholder}">
    <button type="button" class="paste-btn">{icon("clipboard")}Paste</button>
    <button type="submit" class="btn btn-primary">{icon("download")}{button}</button>
  </div>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def android_band(root, id_="android"):
    return f"""<section class="section-sm" id="{id_}">
  <div class="container">
    <div class="band reveal">
      <div class="band-copy">
        <span class="eyebrow">Android App</span>
        <h2>Social Save. <span>On your phone.</span></h2>
        <p>Get the Social Save Android app and access your favorite downloader tools wherever you go.</p>
        {play_badge(root)}
      </div>
      <div class="band-icon"><img src="{root}assets/img/logo.svg" alt="" width="148" height="148" loading="lazy"></div>
    </div>
  </div>
</section>"""


def crumbs(root, *trail):
    items = f'<li><a href="{root or "./"}">Home</a></li>'
    for i, t in enumerate(trail):
        items += f'<li aria-current="page">{t}</li>' if i == len(trail) - 1 else f'<li>{t}</li>'
    return f'<ol class="crumbs" aria-label="Breadcrumb">{items}</ol>'


def responsible_callout():
    return """<div class="callout reveal">
  """ + icon("alert") + """
  <div>
    <h3>Use media responsibly</h3>
    <p>Social Save provides technical tools for downloading supported online media. Users are responsible for ensuring that their use of downloaded content complies with the copyright, licensing terms, platform rules and applicable laws.</p>
  </div>
</div>"""


# ---------------------------------------------------------------- pages
def home():
    root = ""
    platforms = "".join(
        f'<li>{brand(k)}{label}</li>' for k, label in [("instagram", "Instagram"), ("facebook", "Facebook"), ("tiktok", "TikTok"), ("youtube", "YouTube")]
    ) + f'<li>{icon("image", "ph")}Photos</li>'
    tool_cards = "".join(
        f'<a class="tool reveal" href="{href}"><span class="tool-ic">{ic}</span><span class="tool-name">{name}</span>{icon("arrow-right", "go")}</a>'
        for name, href, ic in [
            ("Social Media Video Downloader", "social-media-downloader/", icon("download")),
            ("Instagram Reel Video Downloader", "social-media-downloader/", brand("instagram")),
            ("Facebook Video and Reel Downloader", "social-media-downloader/", brand("facebook")),
            ("TikTok Video Downloader", "social-media-downloader/", brand("tiktok")),
            ("YouTube Video and Shorts Downloader", "youtube-downloader/", brand("youtube")),
            ("Free Stock Media Downloader", "free-stock-media/", icon("image", "ph")),
        ]
    )
    body = f"""<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <a class="chip" href="#android"><b>New</b> Social Save for Android is live {icon("arrow-right")}</a>
      <h1>Save. <span class="accent">Anything.</span> Anywhere.</h1>
      <p class="lead">Save videos, Reels, Shorts and photos with Social Save. A simple way to keep the media you need, wherever you are.</p>
      {link_form(root, action="social-media-downloader/", input_id="hero-link")}
      <ul class="trust">
        <li>{icon("check-circle")}Free</li>
        <li>{icon("check-circle")}No sign-up</li>
        <li>{icon("check-circle")}No watermark</li>
      </ul>
      <div class="hero-actions">
        {play_badge(root)}
        <a class="btn btn-ghost" href="social-media-downloader/">Use Social Save Online {icon("arrow-right")}</a>
      </div>
    </div>
    <div class="hero-visual">
      <div class="visual-card">
        <img src="assets/img/app-mockup.webp" alt="Social Save Android app screens" width="1536" height="1024" fetchpriority="high">
      </div>
      <div class="float float-saved">
        <span class="float-ic">{icon("check-circle")}</span>
        <div><strong>Saved to gallery</strong><span>HD · no watermark</span></div>
      </div>
      <div class="float float-app">
        <span class="float-ic"><img src="assets/img/logo.svg" alt="" width="36" height="36"></span>
        <div><strong>Social Save</strong><span>Android App</span></div>
      </div>
    </div>
  </div>
</section>

<section class="strip" aria-label="Works with">
  <div class="container">
    <div class="strip-inner reveal">
      <span class="strip-label">Works with</span>
      <div class="strip-icons">{brand("facebook", "Facebook")}{brand("instagram", "Instagram")}{brand("tiktok", "TikTok")}{brand("youtube", "YouTube")}</div>
      <ul class="strip-tags"><li>Android App</li><li>Video Downloader</li><li>Reel Downloader</li><li>Photo Downloader</li></ul>
    </div>
  </div>
</section>

<section class="section" id="how">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2>Copy. Paste. Download.</h2>
      <p>There are no complicated settings to learn. You paste a link, process it and download the available media.</p>
    </div>
    <ol class="steps">
      <li class="step reveal"><span class="step-no" aria-hidden="true">1</span><span class="step-ic">{icon("copy")}</span><h3>Copy a link</h3><p>Copy a supported URL from Instagram, Facebook, TikTok or YouTube.</p></li>
      <li class="step reveal"><span class="step-no" aria-hidden="true">2</span><span class="step-ic">{icon("link")}</span><h3>Paste it into Social Save</h3><p>Paste the link into Social Save and process it.</p></li>
      <li class="step reveal"><span class="step-no" aria-hidden="true">3</span><span class="step-ic">{icon("download")}</span><h3>Choose a download</h3><p>Choose the available download option.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="tools" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Tools</span>
      <h2>Social media downloader tools</h2>
      <p>Social Save provides a collection of social media downloading tools designed around common media formats and platforms.</p>
    </div>
    <div class="tool-grid">{tool_cards}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our approach</span>
      <h2>Simple, fast and useful.</h2>
      <p>Social Save is built around three simple principles.</p>
    </div>
    <div class="bento">
      <article class="card card-lg span-4 reveal">
        <span class="card-ic ic-blue">{icon("image")}</span>
        <h3>More than a video downloader</h3>
        <p>Our free stock media tools are designed to help users discover and download supported stock photos and stock videos for creative and personal projects.</p>
        <div class="actions"><a class="btn btn-primary btn-sm" href="free-stock-media/">Free Stock Media Downloader {icon("arrow-right")}</a></div>
      </article>
      <article class="card span-2 reveal"><span class="card-ic ic-rose">{icon("sparkles")}</span><h3>Simple</h3><p>The tools should be easy to understand and use.</p></article>
      <article class="card span-3 reveal"><span class="card-ic ic-green">{icon("zap")}</span><h3>Fast</h3><p>The path from URL to available download should be as straightforward as possible.</p></article>
      <article class="card span-3 reveal"><span class="card-ic ic-blue">{icon("check-circle")}</span><h3>Useful</h3><p>Every feature should solve a real media-saving problem.</p></article>
    </div>
  </div>
</section>

{android_band(root)}
"""
    ld = f'<script type="application/ld+json">{json.dumps(LD_JSON)}</script>\n'
    return page("home", "", body, ld)


def tool_page(slug, path, *, h1, lead, only=None, supported, steps, form_title="Paste a link", extra=""):
    root = "../"
    other = f"{root}social-media-downloader/" if only else None
    sup = "".join(f'<li>{icon("check")}{s}</li>' for s in supported)
    st = "".join(f"<li>{s}</li>" for s in steps)
    plats = (
        f'<ul class="platforms" aria-label="Supported platforms"><li>{brand("youtube")}YouTube</li></ul>'
        if only
        else '<ul class="platforms" aria-label="Supported platforms">'
        + "".join(f'<li>{brand(k)}{l}</li>' for k, l in [("instagram", "Instagram"), ("facebook", "Facebook"), ("tiktok", "TikTok"), ("youtube", "YouTube")])
        + f'<li>{icon("image", "ph")}Photos</li></ul>'
    )
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Social Media", h1)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
  <div class="tool-layout">
    <section class="tool-card reveal" aria-labelledby="tool-title">
      <h2 id="tool-title">{form_title}</h2>
      {link_form(root, live=True, only=only, other=other, input_id="tool-link")}
      <div class="form-hint"><span>Works with</span>{plats}</div>
    </section>
    <aside class="side-card reveal" aria-labelledby="side-how">
      <h2 id="side-how">How it works</h2>
      <ol class="mini-steps">{st}</ol>
    </aside>
  </div>
  <div class="tool-layout" style="padding-top:8px">
    <section class="side-card reveal" aria-labelledby="side-sup">
      <h2 id="side-sup">What you can save</h2>
      <p style="color:var(--muted)">Depending on platform support, you can use Social Save to download:</p>
      <ul class="check-list">{sup}</ul>
    </section>
    {responsible_callout()}
  </div>
</div>
{extra}
{android_band(root)}
"""
    return page(slug, path, body)


def social_media():
    return tool_page(
        "social-media-downloader",
        "social-media-downloader/",
        h1="Social media downloader",
        lead="Social Save provides a collection of social media downloading tools designed around common media formats and platforms.",
        supported=["Social media videos", "Instagram Reels", "Facebook videos and Reels", "TikTok videos", "YouTube videos and Shorts", "Photos and other supported media"],
        steps=["Copy a supported URL from the platform.", "Paste it into Social Save.", "Choose the available download option."],
    )


def youtube():
    return tool_page(
        "youtube-downloader",
        "youtube-downloader/",
        h1="Youtube Downloader",
        lead="Copy a supported YouTube URL, paste it into Social Save, and choose the available download option.",
        only="YouTube",
        supported=["YouTube videos", "YouTube Shorts"],
        steps=["Copy a supported YouTube URL.", "Paste it into Social Save.", "Choose the available download option."],
    )


def stock():
    root = "../"
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Stock Media", "Free stock media")}
    <h1>Free stock media</h1>
    <p class="lead">Our free stock media tools are designed to help users discover and download supported stock photos and stock videos for creative and personal projects.</p>
  </div>
  <div class="support-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
    <article class="card" id="photos"><span class="card-ic ic-blue">{icon("image")}</span><h2>Free Stock Photos Downloader</h2><p>Discover and download supported stock photos for creative and personal projects.</p></article>
    <article class="card" id="videos"><span class="card-ic ic-rose">{icon("film")}</span><h2>Free Stock Videos Downloader</h2><p>Discover and download supported stock videos for creative and personal projects.</p></article>
  </div>
  <div class="tool-layout" style="padding-top:24px">
    <section class="side-card reveal"><h2>More than a video downloader</h2><p style="color:var(--muted)">This makes Social Save useful not only for downloading social media content, but also for finding practical media resources in one place. Social Save is continuously evolving with new tools, better experiences and additional media resources.</p><div><a class="btn btn-ghost btn-sm" href="{root}social-media-downloader/">Social Media Downloader {icon("arrow-right")}</a></div></section>
    {responsible_callout()}
  </div>
</div>
{android_band(root)}
"""
    return page("free-stock-media", "free-stock-media/", body)


def blog():
    root = "../"
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Journal")}
    <h1>Journal</h1>
  </div>
  <div class="empty reveal">
    <span class="card-ic ic-blue">{icon("inbox")}</span>
    <h2>No results</h2>
    <p>There are no articles to show right now.</p>
    <a class="btn btn-primary" href="{root or './'}">Back to home {icon("arrow-right")}</a>
  </div>
</div>
"""
    return page("blog", "blog/", body)


# ---- document pages
def slugify(text):
    s = re.sub(r"<[^>]+>", "", html.unescape(text))
    s = re.sub(r"^\d+\.\s*", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def linkify(h, root):
    h = h.replace("our Contact page", f'our <a href="{root}contact/">Contact page</a>')
    h = re.sub(r"(?<![>\w])(Privacy Policy)(?![^<]*</a>)", lambda m: m.group(0), h)
    h = h.replace("and our Privacy Policy", f'and our <a href="{root}privacy-policy/">Privacy Policy</a>')
    return h


def render_blocks(blocks, root, *, ids=True):
    out = []
    for b in blocks:
        t = b["t"]
        if t in ("ul", "ol"):
            out.append(f"<{t}>" + "".join(f"<li>{i}</li>" for i in b["items"]) + f"</{t}>")
        elif t == "h2":
            out.append(f'<h2 id="{slugify(b["html"])}">{b["html"]}</h2>' if ids else f'<h2>{b["html"]}</h2>')
        elif t == "h3":
            out.append(f'<h3>{b["html"]}</h3>')
        else:
            out.append(f'<p>{linkify(b["html"], root)}</p>')
    return "\n".join(out)


def toc(blocks):
    heads = [(slugify(b["html"]), b["html"]) for b in blocks if b["t"] == "h2"]
    li = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return (
        f'<details class="toc-mobile"><summary>On this page</summary><ol>{li}</ol></details>',
        f'<nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>{li}</ol></nav>',
    )


def legal(slug, path, h1):
    root = "../"
    blocks = DATA["blocks"][slug]
    blocks = [b for b in blocks if not (b["t"] == "h1")]
    updated = ""
    if blocks and "Last Updated" in blocks[0].get("html", ""):
        updated = re.sub(r"<[^>]+>", "", blocks[0]["html"])
        blocks = blocks[1:]
    # drop the trailing brand sign-off (we render our own)
    tail = [i for i, b in enumerate(blocks) if b.get("html", "") == "<strong>Social Save</strong>"]
    sign = None
    if tail:
        sign = blocks[tail[-1] + 1]["html"] if tail[-1] + 1 < len(blocks) else ""
        blocks = blocks[: tail[-1]]
    mobile, side = toc(blocks)
    pill = f'<span class="pill">{updated}</span>' if updated else ""
    closing = f'<div class="closing"><strong>Social Save</strong>{sign}</div>' if sign else ""
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, h1)}
    {pill}
    <h1>{h1}</h1>
  </div>
  <div class="doc">
    {side}
    <div>
      {mobile}
      <article class="prose">
{render_blocks(blocks, root)}
{closing}
      </article>
    </div>
  </div>
</div>
"""
    # mobile TOC sits above the article; add spacing
    body = body.replace('<details class="toc-mobile">', '<details class="toc-mobile" style="margin-bottom:16px">')
    return page(slug, path, body)


def about():
    root = "../"
    blocks = [b for b in DATA["blocks"]["about"] if b["t"] != "h1"]
    lead, intro, rest = blocks[0]["html"], blocks[1:3], blocks[3:]
    mobile, side = toc(rest)
    out = []
    i = 0
    while i < len(rest):
        b = rest[i]
        h = b.get("html", "")
        if h == "[Get Social Save on Google Play]":
            out.append(f'<p>{play_badge(root)}</p>')
        elif h.startswith("<strong>Simple</strong>"):
            items = "".join("<li>" + rest[i + k]["html"].replace("<br>", "<span>", 1) + "</span></li>" for k in range(3))
            out.append(f'<ul class="principles">{items}</ul>')
            i += 2
        elif h.startswith("<strong>Social Save</strong><br>"):
            out.append(f'<div class="closing">{h}</div>')
        elif b["t"] == "p" and "Users are responsible" in h:
            out.append(f'<div class="callout" style="margin-top:16px">{icon("alert")}<p>{h}</p></div>')
        else:
            out.append(render_blocks([b], root))
        i += 1
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "About")}
    <h1>About</h1>
    <p class="lead">{lead}</p>
  </div>
  <div class="doc">
    {side}
    <div>
      {mobile}
      <article class="prose">
{render_blocks(intro, root)}
{chr(10).join(out)}
      </article>
    </div>
  </div>
</div>
"""
    body = body.replace('<details class="toc-mobile">', '<details class="toc-mobile" style="margin-bottom:16px">')
    return page("about", "about/", body)


def contact():
    root = "../"
    blocks = [b for b in DATA["blocks"]["contact"] if b["t"] != "h1"]
    lead = blocks[0]["html"]
    second = blocks[1]["html"]
    # split sections
    sections, cur = [], None
    for b in blocks[2:]:
        if b["t"] == "h2":
            cur = {"h": b["html"], "b": []}
            sections.append(cur)
        else:
            cur["b"].append(b)
    get = next(s for s in sections if s["h"].startswith("Get in Touch"))
    before = next(s for s in sections if s["h"].startswith("Before Contacting"))
    copy = next(s for s in sections if "Copyright" in s["h"])
    last = next(s for s in sections if s["h"] == "Social Save")
    # support cards from h3 groups
    cards, cur = [], None
    intro = []
    for b in get["b"]:
        if b["t"] == "h3":
            cur = {"h": b["html"], "b": []}
            cards.append(cur)
        elif cur is None:
            intro.append(b)
        else:
            cur["b"].append(b)
    ics = {"Technical Support": ("life-buoy", "ic-blue"), "Feedback &amp; Suggestions": ("message", "ic-green"), "Report a Problem": ("flag", "ic-rose")}
    card_html = ""
    for c in cards:
        ic, cl = ics.get(c["h"], ("message", "ic-blue"))
        card_html += f'<article class="card reveal"><span class="card-ic {cl}">{icon(ic)}</span><h3>{c["h"]}</h3>' + "".join(f'<p>{b["html"]}</p>' for b in c["b"]) + "</article>"
    bp = "".join(f'<p>{b["html"]}</p>' for b in before["b"])
    bp = (
        bp.replace("Social Media Downloader tools", f'<a href="{root}social-media-downloader/">Social Media Downloader tools</a>')
        .replace("Free Stock Media resources", f'<a href="{root}free-stock-media/">Free Stock Media resources</a>')
        .replace("Journal", f'<a href="{root}blog/">Journal</a>')
        .replace("About page", f'<a href="{root}about/">About page</a>')
    )
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Contact")}
    <h1>Contact</h1>
    <p class="lead">{lead}</p>
    <p class="lead" style="margin-top:10px">{second}</p>
  </div>
  <section class="reveal" style="padding:24px 0 8px">
    <div class="section-head" style="margin-bottom:24px"><h2>{get["h"]}</h2>{"".join(f"<p>{b['html']}</p>" for b in intro)}</div>
    <div class="support-grid">{card_html}</div>
  </section>
  <div class="tool-layout" style="padding-top:24px">
    <section class="side-card reveal"><h2>{before["h"]}</h2>{bp}</section>
    <div class="callout reveal">{icon("alert")}<div><h3>{copy["h"]}</h3>{"".join(f"<p>{b['html']}</p>" for b in copy["b"])}</div></div>
  </div>
  <div class="closing reveal" style="margin-top:24px"><strong>{last["h"]}</strong>{last["b"][0]["html"]}<p style="margin-top:6px;color:var(--ink)">{last["b"][1]["html"]}</p></div>
</div>
"""
    return page("contact", "contact/", body)


def write(path, content):
    full = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(full, ROOT))


if __name__ == "__main__":
    write("", home())
    write("social-media-downloader", social_media())
    write("youtube-downloader", youtube())
    write("free-stock-media", stock())
    write("blog", blog())
    write("about", about())
    write("contact", contact())
    write("privacy-policy", legal("privacy-policy", "privacy-policy/", "Privacy Policy"))
    write("terms", legal("terms", "terms/", "Terms"))
