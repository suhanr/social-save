#!/usr/bin/env python3
"""Generate the Social Save static site (pages, sitemap, robots, feed, manifest).

Usage (from the repo root):  python3 tools/build.py

Copy lives in:
  tools/content.json        about, contact, privacy, terms
  tools/content_landings.py keyword landing pages and the two downloader pages
  tools/content_posts.py    Journal posts
  tools/content_faq.py      FAQ page and the stock-media page
Home page copy and all templates are in this file. Styles: assets/css/main.css.
Every link is relative, so the pages work from any base path.
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_faq import FAQ_GROUPS, STOCK  # noqa: E402
from content_landings import EXISTING, LANDINGS, _EXTRA  # noqa: E402
from content_posts import DATE as POST_DATE, POSTS  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "tools", "content.json"), encoding="utf-8"))
BRAND = DATA["brand"]

# ---------------------------------------------------------------- site settings
SITE = "https://socialsave.site/"
SITE_NAME = "Social Save"
BUILD_DATE = "2026-10-10"
# TODO: replace with the real Play Store listing (placeholder carried over from the original site).
PLAY_URL = "https://play.google.com/store/apps/details?id=YOUR_APP_PACKAGE"
CONTACT_EMAIL = ""  # set to show a mailto contact on the Contact page and in the schema
SOCIAL_PROFILES = []  # real profile URLs (Facebook page, YouTube channel, ...) for Organization.sameAs
VERIFICATION = {  # paste the tokens from Search Console / Bing Webmaster Tools
    "google-site-verification": "",
    "msvalidate.01": "",
}
OG_W, OG_H = 1200, 630

# ---------------------------------------------------------------- icons
LUCIDE = {
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
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
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "film": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18"/><path d="M3 7.5h4"/><path d="M3 12h18"/><path d="M3 16.5h4"/><path d="M17 3v18"/><path d="M17 7.5h4"/><path d="M17 16.5h4"/>',
    "life-buoy": '<circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
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


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------- page registry
TOOL_ORDER = [
    "social-media-downloader",
    "instagram-video-downloader",
    "instagram-reels-downloader",
    "facebook-video-downloader",
    "tiktok-video-downloader",
    "youtube-downloader",
    "youtube-shorts-downloader",
    "photo-downloader",
    "free-stock-media",
]
SHORT = {
    "social-media-downloader": "Social Media Video Downloader",
    "instagram-video-downloader": "Instagram Video Downloader",
    "instagram-reels-downloader": "Instagram Reels Downloader",
    "facebook-video-downloader": "Facebook Video Downloader",
    "tiktok-video-downloader": "TikTok Video Downloader",
    "youtube-downloader": "YouTube Video Downloader",
    "youtube-shorts-downloader": "YouTube Shorts Downloader",
    "photo-downloader": "Photo Downloader",
    "free-stock-media": "Free Stock Media Downloader",
}
TOOL_ICON = {
    "social-media-downloader": ("download", None),
    "instagram-video-downloader": (None, "instagram"),
    "instagram-reels-downloader": (None, "instagram"),
    "facebook-video-downloader": (None, "facebook"),
    "tiktok-video-downloader": (None, "tiktok"),
    "youtube-downloader": (None, "youtube"),
    "youtube-shorts-downloader": (None, "youtube"),
    "photo-downloader": ("image", None),
    "free-stock-media": ("film", None),
}
FOOTER_GUIDES = [
    ("How to copy a video link", "how-to-copy-a-video-link-on-any-platform"),
    ("How to save Instagram Reels", "how-to-save-instagram-reels"),
    ("How to save TikTok videos", "how-to-save-tiktok-videos"),
    ("Is downloading videos legal?", "is-it-legal-to-download-social-media-videos"),
    ("Best free stock sites", "best-free-stock-photo-and-video-sites"),
]
PATH = {"home": "", "blog": "blog/", "about": "about/", "contact": "contact/", "faq": "faq/", "privacy-policy": "privacy-policy/", "terms": "terms/"}
for s in TOOL_ORDER:
    PATH[s] = s + "/"
for p in POSTS:
    PATH[p["slug"]] = f"blog/{p['slug']}/"
POST = {p["slug"]: p for p in POSTS}
LANDING = {l["slug"]: l for l in LANDINGS}
LANDING.update({k: dict(v, slug=k, platform="YouTube" if k == "youtube-downloader" else None) for k, v in EXISTING.items()})
LANDING["free-stock-media"] = dict(STOCK, slug="free-stock-media", platform=None)
LANDING["free-stock-media"]["sections"] = list(STOCK["sections"]) + _EXTRA["free-stock-media"]


def url(slug):
    return SITE + PATH[slug]


def L(text, root):
    """Resolve [[slug|anchor]] into relative links (fails the build on unknown slugs)."""

    def rep(m):
        slug = m.group(1)
        if slug not in PATH:
            raise SystemExit(f"Unknown internal link target: {slug}")
        return f'<a href="{root}{PATH[slug]}">{m.group(2)}</a>'

    return re.sub(r"\[\[([a-z0-9-]+)\|([^\]]+)\]\]", rep, text)


def plain(text):
    return strip_tags(re.sub(r"\[\[[a-z0-9-]+\|([^\]]+)\]\]", r"\1", text))


def slugify(text):
    s = re.sub(r"<[^>]+>", "", html.unescape(text))
    s = re.sub(r"^\d+\.\s*", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def with_brand(title):
    """Append the brand when the title stays within ~60 characters."""
    suffix = " | Social Save"
    return title + suffix if len(title) + len(suffix) <= 60 else title


def human_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


# ---------------------------------------------------------------- navigation
NAV = [
    ("Social Media", "social-media-downloader/", "social"),
    ("Stock Media", "free-stock-media/", "stock"),
    ("Journal", "blog/", "journal"),
    ("About", "about/", "about"),
]


def play_badge(root, cls=""):
    return (
        f'<a class="play-badge {cls}" href="{PLAY_URL}" rel="noopener">'
        f'<img src="{root}assets/img/google-play-badge.png" alt="Get it on Google Play" width="124" height="48"></a>'
    )


def header(root, section):
    items, mobile = "", ""
    for label, href, key in NAV:
        cur = ' aria-current="page"' if section == key else ""
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
    def li(label, slug):
        return f'<li><a href="{root}{PATH[slug]}">{label}</a></li>'

    tools = "".join(li(SHORT[s], s) for s in TOOL_ORDER)
    guides = "".join(li(label, s) for label, s in FOOTER_GUIDES) + f'<li><a href="{root}blog/">All guides</a></li>'
    company = "".join(li(l, s) for l, s in [("Journal", "blog"), ("About", "about"), ("FAQ", "faq"), ("Contact", "contact"), ("Privacy", "privacy-policy"), ("Terms", "terms")])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{root or './'}"><img src="{root}assets/img/logo.svg" alt="" width="38" height="38"><span class="brand-name">Social Save</span></a>
        <p>A simple place to save videos, Reels and Shorts, photos and free stock media from the web.</p>
      </div>
      <div class="footer-col"><h2>Tools</h2><ul>{tools}</ul></div>
      <div class="footer-col"><h2>Guides</h2><ul>{guides}</ul></div>
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


# ---------------------------------------------------------------- structured data
def ld_script(graph):
    data = {"@context": "https://schema.org", "@graph": graph}
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{text}</script>\n'


def org_node():
    node = {
        "@type": "Organization",
        "@id": SITE + "#organization",
        "name": SITE_NAME,
        "url": SITE,
        "logo": {"@type": "ImageObject", "@id": SITE + "#logo", "url": SITE + "assets/img/icon-512.png", "width": 512, "height": 512},
        "description": "Social Save is a simple media downloading platform for supported social media videos, Reels, Shorts, photos and free stock media.",
    }
    if SOCIAL_PROFILES:
        node["sameAs"] = SOCIAL_PROFILES
    if CONTACT_EMAIL:
        node["contactPoint"] = {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "availableLanguage": "English"}
    return node


def website_node():
    return {
        "@type": "WebSite",
        "@id": SITE + "#website",
        "url": SITE,
        "name": SITE_NAME,
        "description": "Free social media video, Reel, Shorts and photo downloader.",
        "publisher": {"@id": SITE + "#organization"},
        "inLanguage": "en",
    }


def breadcrumb_node(pageurl, trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE}]
    for i, (name, slug) in enumerate(trail, start=2):
        entry = {"@type": "ListItem", "position": i, "name": name}
        entry["item"] = pageurl if slug is None else url(slug)
        items.append(entry)
    return {"@type": "BreadcrumbList", "@id": pageurl + "#breadcrumb", "itemListElement": items}


def faq_node(pageurl, faqs):
    return {
        "@type": "FAQPage",
        "@id": pageurl + "#faq",
        "isPartOf": {"@id": pageurl + "#webpage"},
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs],
    }


# ---------------------------------------------------------------- page shell
def page(slug, body, *, title, desc, section=None, kind="WebPage", trail=None, extra_nodes=None, og_type="website",
         published=None, modified=BUILD_DATE, noindex=False, abs_root=False, head_extra="", article_section=None, og_title=None):
    path = PATH.get(slug, "")
    root = "/" if abs_root else ("../" * path.count("/") if path else "")
    canonical = SITE + path
    og_img = f"{SITE}assets/og/{slug}.jpg"
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    t, d = esc(title), esc(desc)
    ot = esc(og_title or title)

    graph = [org_node(), website_node()]
    webpage = {
        "@type": kind,
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": desc,
        "isPartOf": {"@id": SITE + "#website"},
        "inLanguage": "en",
        "datePublished": published or BUILD_DATE,
        "dateModified": modified,
        "primaryImageOfPage": {"@type": "ImageObject", "url": og_img, "width": OG_W, "height": OG_H},
    }
    if trail:
        webpage["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    if slug == "home":
        webpage["about"] = {"@id": SITE + "#organization"}
    graph.append(webpage)
    if trail:
        graph.append(breadcrumb_node(canonical, trail))
    graph += extra_nodes or []
    ld = "" if noindex else ld_script(graph)

    canon_tags = "" if noindex else (
        f'<link rel="canonical" href="{canonical}">\n'
        f'<link rel="alternate" hreflang="en" href="{canonical}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{canonical}">\n'
    )
    og_url = "" if noindex else f'<meta property="og:url" content="{canonical}">\n'
    verify = "".join(f'<meta name="{k}" content="{esc(v)}">\n' for k, v in VERIFICATION.items() if v)
    article_meta = ""
    if og_type == "article":
        article_meta = (
            f'<meta property="article:published_time" content="{published}T08:00:00+00:00">\n'
            f'<meta property="article:modified_time" content="{modified}T08:00:00+00:00">\n'
            f'<meta property="article:section" content="{esc(article_section or "Guides")}">\n'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
{canon_tags}<link rel="alternate" type="application/rss+xml" title="Social Save Journal" href="{SITE}feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Social Save">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{ot}">
<meta property="og:description" content="{d}">
{og_url}<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="{OG_W}">
<meta property="og:image:height" content="{OG_H}">
<meta property="og:image:alt" content="{ot}">
{article_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ot}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og_img}">
{verify}<meta name="theme-color" content="#f8fafc">
<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="icon" href="{root}favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="{root}assets/img/logo.svg">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/worksans-latin.woff2" as="font" type="font/woff2" crossorigin>
{head_extra}<link rel="stylesheet" href="{root}assets/css/main.css">
{ld}</head>
<body>
{header(root, section)}
<main id="main">
{body}
</main>
{footer(root)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks
def link_form(root, *, action=None, live=False, only=None, other=None, input_id="link",
              placeholder="Paste a link from Instagram, Facebook, TikTok or YouTube", button="Save"):
    attrs = " novalidate"
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
    """trail items: str (current page) or (label, slug) links."""
    items = f'<li><a href="{root or "./"}">Home</a></li>'
    for i, t in enumerate(trail):
        if i == len(trail) - 1:
            label = t if isinstance(t, str) else t[0]
            items += f'<li aria-current="page">{label}</li>'
        else:
            label, slug = t
            items += f'<li><a href="{root}{PATH[slug]}">{label}</a></li>'
    return f'<ol class="crumbs" aria-label="Breadcrumb">{items}</ol>'


def responsible_callout():
    return (
        '<div class="callout reveal">' + icon("alert") + """
  <div>
    <h3>Use media responsibly</h3>
    <p>Social Save provides technical tools for downloading supported online media. Users are responsible for ensuring that their use of downloaded content complies with the copyright, licensing terms, platform rules and applicable laws.</p>
  </div>
</div>"""
    )


def read_minutes(blocks):
    words = 0
    for b in blocks:
        for part in b[1:]:
            if isinstance(part, str):
                words += len(plain(part).split())
            elif isinstance(part, list):
                for x in part:
                    words += len(plain(" ".join(x) if isinstance(x, list) else x).split())
    return max(1, round(words / 200)), words


def render_blocks(blocks, root):
    out, last_h2 = [], "Table"
    for b in blocks:
        t = b[0]
        if t == "h2":
            last_h2 = b[1]
            out.append(f'<h2 id="{slugify(b[1])}">{L(b[1], root)}</h2>')
        elif t == "p":
            out.append(f"<p>{L(b[1], root)}</p>")
        elif t in ("ul", "ol"):
            out.append(f"<{t}>" + "".join(f"<li>{L(i, root)}</li>" for i in b[1]) + f"</{t}>")
        elif t == "table":
            head = "".join(f"<th scope=\"col\">{h}</th>" for h in b[1])
            rows = "".join("<tr>" + "".join(f"<td>{L(c, root)}</td>" for c in r) + "</tr>" for r in b[2])
            out.append(
                f'<div class="table-wrap" role="region" aria-label="{esc(plain(last_h2))}" tabindex="0">'
                f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>"
            )
        elif t == "note":
            out.append(f'<div class="note">{L(b[1], root)}</div>')
    return "\n".join(out)


def faq_section(root, faqs, heading="Frequently asked questions"):
    items = "".join(
        f'<details><summary>{esc(q)}</summary><div class="faq-a"><p>{L(a, root)}</p></div></details>' for q, a in faqs
    )
    return f"""<section class="section-sm" id="faq">
  <div class="container">
    <div class="section-head reveal" style="margin-bottom:24px"><h2>{heading}</h2></div>
    <div class="faq-list reveal">{items}</div>
  </div>
</section>"""


def tool_card(slug, root):
    ic, br = TOOL_ICON[slug]
    glyph = brand(br) if br else icon(ic)
    return f'<a class="tool" href="{root}{PATH[slug]}"><span class="tool-ic">{glyph}</span><span class="tool-name">{SHORT[slug]}</span>{icon("arrow-right", "go")}</a>'


def post_card(slug, root, *, tag="h3"):
    p = POST[slug]
    mins, _ = read_minutes(p["blocks"])
    return (
        f'<article class="post-card reveal"><span class="pill">{esc(p["category"])}</span>'
        f'<{tag}><a href="{root}{PATH[slug]}">{esc(p["title"])}</a></{tag}>'
        f'<p>{esc(p["desc"])}</p>'
        f'<div class="post-meta"><time datetime="{POST_DATE}">{human_date(POST_DATE)}</time><span>{mins} min read</span></div></article>'
    )


def related(root, tools, guides):
    t = "".join(tool_card(s, root) for s in tools)
    g = "".join(
        f'<a class="rel-link" href="{root}{PATH[s]}"><span>{esc(POST[s]["title"])}</span>{icon("arrow-right", "go")}</a>' for s in guides
    )
    return f"""<aside class="side-stack" aria-label="Related">
  <section class="side-card"><h2>Related tools</h2><div class="tool-grid one">{t}</div></section>
  <section class="side-card"><h2>Guides</h2><div class="rel-list">{g}</div></section>
</aside>"""


# ---------------------------------------------------------------- pages
def home():
    root = ""
    tool_cards = "".join(tool_card(s, root).replace('class="tool"', 'class="tool reveal"') for s in TOOL_ORDER)
    guides = "".join(
        post_card(s, root)
        for s in ["how-to-copy-a-video-link-on-any-platform", "how-to-save-instagram-reels", "is-it-legal-to-download-social-media-videos"]
    )
    faqs = [
        ("Is Social Save free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
        ("Which platforms does Social Save work with?", "Instagram, Facebook, TikTok and YouTube, including Reels and Shorts, plus supported photos. Platform support can change over time."),
        ("Can I save videos in my browser on this website?", "This website checks your link and identifies the platform, but online downloads are not switched on yet. The Social Save Android app brings the tools to your phone."),
        ("Why is my link not working?", "Check that the post is public and still available and that you copied the whole link. Private accounts, deleted posts and age-restricted content cannot be saved, and creators can switch off downloads."),
    ]
    body = f"""<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <a class="chip" href="#android"><b>New</b> Social Save for Android is live {icon("arrow-right")}</a>
      <h1><span class="h1-kicker">Free video, Reel &amp; photo downloader</span>Save. <span class="accent">Anything.</span> Anywhere.</h1>
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
        <img src="assets/img/app-mockup-1152.webp" srcset="assets/img/app-mockup-768.webp 768w, assets/img/app-mockup-1152.webp 1152w, assets/img/app-mockup.webp 1536w" sizes="(min-width: 900px) 48vw, 100vw" alt="Social Save Android app screens showing the video downloader" width="1536" height="1024" fetchpriority="high">
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

<section class="section" id="about-social-save">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Social media video downloader</span>
      <h2>Save videos, Reels, Shorts and photos in one place</h2>
      <p>Social Save is a simple and practical media downloading platform built for people who want an easier way to save content from the web. It brings tools for Instagram, Facebook, TikTok and YouTube together, along with free stock media. <a href="about/">Read more about Social Save</a>.</p>
    </div>
  </div>
</section>

<section class="section" id="how" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2>Copy. Paste. Download.</h2>
      <p>There are no complicated settings to learn. You paste a link, process it and download the available media. Not sure where to find the link? See <a href="blog/how-to-copy-a-video-link-on-any-platform/">how to copy a video link on any platform</a>.</p>
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

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Journal</span>
      <h2>Guides to saving videos, Reels and photos</h2>
      <p>Practical, plain-language guides, from copying a link to what the law says.</p>
    </div>
    <div class="post-grid">{guides}</div>
    <p style="margin-top:20px"><a class="btn btn-ghost btn-sm" href="blog/">All guides {icon("arrow-right")}</a></p>
  </div>
</section>

{faq_section(root, faqs)}

{android_band(root)}
"""
    return page(
        "home", body,
        title="Social Save – Free Video, Reel & Photo Downloader",
        desc="Save videos, Reels, Shorts and photos from Instagram, Facebook, TikTok and YouTube with Social Save. Free, no sign-up, no watermark added.",
        extra_nodes=[
            {
                "@type": "SoftwareApplication",
                "@id": SITE + "#app",
                "name": "Social Save",
                "operatingSystem": "Android",
                "applicationCategory": "MultimediaApplication",
                "description": "Social Save is a social media downloader for saving videos, Reels, Shorts and photos.",
                "url": SITE,
                "image": SITE + "assets/img/icon-512.png",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "publisher": {"@id": SITE + "#organization"},
            },
            faq_node(SITE, faqs),
        ],
        head_extra='<link rel="preload" as="image" href="assets/img/app-mockup-1152.webp" imagesrcset="assets/img/app-mockup-768.webp 768w, assets/img/app-mockup-1152.webp 1152w, assets/img/app-mockup.webp 1536w" imagesizes="(min-width: 900px) 48vw, 100vw" fetchpriority="high">\n',
    )


SUPPORTED = {
    "social-media-downloader": ["Social media videos", "Instagram Reels", "Facebook videos and Reels", "TikTok videos", "YouTube videos and Shorts", "Photos and other supported media"],
}


def tool_page(slug):
    root = "../"
    spec = LANDING[slug]
    h1 = spec["h1"]
    only = spec.get("platform")
    other = f"{root}social-media-downloader/" if only else None
    steps = spec.get("steps") or ["Copy a supported URL from the platform.", "Paste it into Social Save.", "Choose the available download option."]
    st = "".join(f"<li><span>{L(s, root)}</span></li>" for s in steps)
    plat_keys = [("instagram", "Instagram"), ("facebook", "Facebook"), ("tiktok", "TikTok"), ("youtube", "YouTube")]
    if only:
        plats = f'<ul class="platforms" aria-label="Supported platforms"><li>{brand(only.lower())}{only}</li></ul>'
    else:
        plats = '<ul class="platforms" aria-label="Supported platforms">' + "".join(f"<li>{brand(k)}{l}</li>" for k, l in plat_keys) + f'<li>{icon("image", "ph")}Photos</li></ul>'
    placeholder = {
        "Instagram": "Paste an Instagram link",
        "Facebook": "Paste a Facebook video link",
        "TikTok": "Paste a TikTok video link",
        "YouTube": "Paste a YouTube link",
    }.get(only, "Paste a link from Instagram, Facebook, TikTok or YouTube")
    section_key = "stock" if slug == "free-stock-media" else "social"
    if slug in ("social-media-downloader", "free-stock-media"):
        bc = crumbs(root, h1)
        trail = [(h1, None)]
    else:
        bc = crumbs(root, ("Social Media", "social-media-downloader"), h1)
        trail = [("Social Media", "social-media-downloader"), (h1, None)]

    blocks = spec["sections"]
    prose = render_blocks(blocks, root)
    supported = ""
    if slug in SUPPORTED:
        items = "".join(f'<li>{icon("check")}{s}</li>' for s in SUPPORTED[slug])
        supported = f'<section class="side-card reveal"><h2>What you can save</h2><p style="color:var(--muted)">Depending on platform support, you can use Social Save to download:</p><ul class="check-list">{items}</ul></section>'

    if slug == "free-stock-media":
        tool_block = f"""<div class="support-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr));padding-bottom:24px">
    <article class="card" id="photos"><span class="card-ic ic-blue">{icon("image")}</span><h2>Free Stock Photos Downloader</h2><p>Discover and download supported stock photos for creative and personal projects.</p></article>
    <article class="card" id="videos"><span class="card-ic ic-rose">{icon("film")}</span><h2>Free Stock Videos Downloader</h2><p>Discover and download supported stock videos for creative and personal projects.</p></article>
  </div>"""
    else:
        tool_block = f"""<div class="tool-layout">
    <section class="tool-card reveal" aria-labelledby="tool-title">
      <h2 id="tool-title">Paste a link</h2>
      {link_form(root, live=True, only=only, other=other, input_id="tool-link", placeholder=placeholder)}
      <div class="form-hint"><span>Works with</span>{plats}</div>
    </section>
    <aside class="side-card reveal" aria-labelledby="side-how">
      <h2 id="side-how">How it works</h2>
      <ol class="mini-steps">{st}</ol>
    </aside>
  </div>"""

    body = f"""<div class="container">
  <div class="page-head">
    {bc}
    <h1>{h1}</h1>
    <p class="lead">{L(spec["lead"], root)}</p>
  </div>
  {tool_block}
  <div class="content-layout">
    <div class="stack">
      {supported}
      <article class="prose reveal">
{prose}
      </article>
    </div>
    {related(root, spec["tools"], spec["guides"])}
  </div>
</div>
{faq_section(root, spec["faq"])}
<div class="container" style="padding-bottom:8px">{responsible_callout()}</div>
{android_band(root)}
"""
    return page(
        slug, body,
        title=spec["title"], desc=spec["desc"], section=section_key, trail=trail,
        extra_nodes=[faq_node(url(slug), spec["faq"])],
    )


def blog_index():
    root = "../"
    cards = "".join(post_card(s, root, tag="h2") for s in PATH if s in POST)
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Journal")}
    <h1>Journal: guides to saving videos, Reels and photos</h1>
    <p class="lead">Practical, plain-language guides on copying links, saving media from Instagram, Facebook, TikTok and YouTube, formats, free stock media and the legal basics.</p>
  </div>
  <div class="post-grid">{cards}</div>
</div>
{android_band(root)}
"""
    items = [{"@type": "ListItem", "position": i, "url": url(s), "name": POST[s]["title"]} for i, s in enumerate([s for s in PATH if s in POST], start=1)]
    return page(
        "blog", body,
        title="Journal – Guides to Saving Videos, Reels & Photos | Social Save",
        desc="Plain-language guides to copying video links, saving Instagram Reels, TikTok and YouTube Shorts, choosing formats, free stock media and the legal basics.",
        section="journal", kind="CollectionPage", trail=[("Journal", None)],
        extra_nodes=[{"@type": "ItemList", "@id": url("blog") + "#list", "itemListElement": items}],
    )


def post_page(slug):
    root = "../../"
    p = POST[slug]
    mins, words = read_minutes(p["blocks"])
    heads = [(slugify(b[1]), b[1]) for b in p["blocks"] if b[0] == "h2"]
    li = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    toc_m = f'<details class="toc-mobile" style="margin-bottom:16px"><summary>In this guide</summary><ol>{li}</ol></details>'
    toc_d = f'<nav class="toc" aria-label="In this guide"><div class="toc-title">In this guide</div><ol>{li}</ol></nav>'
    others = [s for s in p["guides"] if s != slug]
    faq = p.get("faq") or []
    faq_html = faq_section(root, faq, heading="Frequently asked questions") if faq else ""
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, ("Journal", "blog"), p["title"])}
    <span class="pill">{esc(p["category"])}</span>
    <h1>{esc(p["title"])}</h1>
    <p class="lead">{L(p["lead"], root)}</p>
    <p class="byline">By <a href="{root}about/">Social Save</a> · <time datetime="{POST_DATE}">{human_date(POST_DATE)}</time> · {mins} min read</p>
  </div>
  <div class="doc">
    {toc_d}
    <div>
      {toc_m}
      <article class="prose">
{render_blocks(p["blocks"], root)}
      </article>
    </div>
  </div>
</div>
{faq_html}
<div class="container">
  <section class="section-sm">
    <div class="section-head" style="margin-bottom:20px"><h2>Try the tools</h2></div>
    <div class="tool-grid">{"".join(tool_card(s, root) for s in p["tools"])}</div>
  </section>
  <section class="section-sm">
    <div class="section-head" style="margin-bottom:20px"><h2>Keep reading</h2></div>
    <div class="post-grid">{"".join(post_card(s, root) for s in others)}</div>
  </section>
</div>
{android_band(root)}
"""
    pageurl = url(slug)
    article = {
        "@type": "BlogPosting",
        "@id": pageurl + "#article",
        "mainEntityOfPage": {"@id": pageurl + "#webpage"},
        "headline": p["title"][:110],
        "description": p["desc"],
        "image": [f"{SITE}assets/og/{slug}.jpg"],
        "datePublished": POST_DATE,
        "dateModified": POST_DATE,
        "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE + "about/"},
        "publisher": {"@id": SITE + "#organization"},
        "articleSection": p["category"],
        "wordCount": words + sum(len(plain(q + " " + a).split()) for q, a in faq),
        "inLanguage": "en",
    }
    return page(
        slug, body, title=with_brand(p["seo_title"]), desc=p["desc"], section="journal",
        trail=[("Journal", "blog"), (p["title"], None)], extra_nodes=[article] + ([faq_node(pageurl, faq)] if faq else []), og_type="article",
        published=POST_DATE, article_section=p["category"], og_title=p["title"],
    )


def faq_page():
    root = "../"
    allq = [qa for _, qs in FAQ_GROUPS for qa in qs]
    groups = ""
    for name, qs in FAQ_GROUPS:
        items = "".join(f'<details><summary>{esc(q)}</summary><div class="faq-a"><p>{L(a, root)}</p></div></details>' for q, a in qs)
        groups += f'<h2 class="faq-h" id="{slugify(name)}">{name}</h2><div class="faq-list">{items}</div>'
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "FAQ")}
    <h1>Frequently asked questions</h1>
    <p class="lead">Answers about Social Save, how to use the downloader tools, why a link might not work, and the rights and privacy basics.</p>
  </div>
  <div class="faq-page">{groups}</div>
  <div style="padding-top:28px">{responsible_callout()}</div>
</div>
{android_band(root)}
"""
    return page(
        "faq", body, title="FAQ – Social Save Video & Photo Downloader",
        desc="Answers to common questions about Social Save: free use, supported platforms, why a link does not work, file formats, privacy and copyright.",
        section=None, trail=[("FAQ", None)], extra_nodes=[faq_node(url("faq"), allq)],
    )


# ---- document pages
def toc(blocks):
    heads = [(slugify(b["html"]), b["html"]) for b in blocks if b["t"] == "h2"]
    li = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return (
        f'<details class="toc-mobile" style="margin-bottom:16px"><summary>On this page</summary><ol>{li}</ol></details>',
        f'<nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>{li}</ol></nav>',
    )


def doc_blocks(blocks, root):
    out = []
    for b in blocks:
        t = b["t"]
        if t in ("ul", "ol"):
            out.append(f"<{t}>" + "".join(f"<li>{i}</li>" for i in b["items"]) + f"</{t}>")
        elif t == "h2":
            out.append(f'<h2 id="{slugify(b["html"])}">{b["html"]}</h2>')
        elif t == "h3":
            out.append(f'<h3>{b["html"]}</h3>')
        else:
            h = b["html"].replace("our Contact page", f'our <a href="{root}contact/">Contact page</a>').replace("and our Privacy Policy", f'and our <a href="{root}privacy-policy/">Privacy Policy</a>')
            out.append(f"<p>{h}</p>")
    return "\n".join(out)


def legal(slug, h1, title, desc):
    root = "../"
    blocks = [b for b in DATA["blocks"][slug] if b["t"] != "h1"]
    updated = ""
    if blocks and "Last Updated" in blocks[0].get("html", ""):
        updated = re.sub(r"<[^>]+>", "", blocks[0]["html"])
        blocks = blocks[1:]
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
{doc_blocks(blocks, root)}
{closing}
      </article>
    </div>
  </div>
</div>
"""
    return page(slug, body, title=title, desc=desc, trail=[(h1, None)], modified=BUILD_DATE)


def about():
    root = "../"
    blocks = [b for b in DATA["blocks"]["about"] if b["t"] != "h1"]
    lead, intro, rest = blocks[0]["html"], blocks[1:3], blocks[3:]
    mobile, side = toc(rest)
    out, i = [], 0
    while i < len(rest):
        b = rest[i]
        h = b.get("html", "")
        if h == "[Get Social Save on Google Play]":
            out.append(f"<p>{play_badge(root)}</p>")
        elif h.startswith("<strong>Simple</strong>"):
            items = "".join("<li>" + rest[i + k]["html"].replace("<br>", "<span>", 1) + "</span></li>" for k in range(3))
            out.append(f'<ul class="principles">{items}</ul>')
            i += 2
        elif h.startswith("<strong>Social Save</strong><br>"):
            out.append(f'<div class="closing">{h}</div>')
        elif b["t"] == "p" and "Users are responsible" in h:
            out.append(f'<div class="callout" style="margin-top:16px">{icon("alert")}<p>{h}</p></div>')
        else:
            out.append(doc_blocks([b], root))
        i += 1
    tools = "".join(tool_card(s, root) for s in ["social-media-downloader", "instagram-reels-downloader", "free-stock-media"])
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "About")}
    <h1>About Social Save</h1>
    <p class="lead">{lead}</p>
  </div>
  <div class="doc">
    {side}
    <div>
      {mobile}
      <article class="prose">
{doc_blocks(intro, root)}
{chr(10).join(out)}
      </article>
    </div>
  </div>
  <section class="section-sm"><div class="section-head" style="margin-bottom:20px"><h2>Explore the tools</h2></div><div class="tool-grid">{tools}</div></section>
</div>
"""
    return page(
        "about", body, title="About Social Save – Social Media Downloader & Media Tools",
        desc="Social Save is a simple media downloading platform for supported social media videos, Reels, Shorts, photos and free stock media.",
        section="about", kind="AboutPage", trail=[("About", None)],
    )


def contact():
    root = "../"
    blocks = [b for b in DATA["blocks"]["contact"] if b["t"] != "h1"]
    lead, second = blocks[0]["html"], blocks[1]["html"]
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
    cards, cur, intro = [], None, []
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
    email = (
        f'<div class="notice notice-info" style="margin-top:16px">{icon("mail")}<div><strong>Email us</strong><br><a href="mailto:{esc(CONTACT_EMAIL)}">{esc(CONTACT_EMAIL)}</a></div></div>'
        if CONTACT_EMAIL else ""
    )
    body = f"""<div class="container">
  <div class="page-head">
    {crumbs(root, "Contact")}
    <h1>Contact Social Save</h1>
    <p class="lead">{lead}</p>
    <p class="lead" style="margin-top:10px">{second}</p>
    {email}
  </div>
  <section class="reveal" style="padding:24px 0 8px">
    <div class="section-head" style="margin-bottom:24px"><h2>{get["h"]}</h2>{"".join(f"<p>{b['html']}</p>" for b in intro)}</div>
    <div class="support-grid">{card_html}</div>
  </section>
  <div class="tool-layout" style="padding-top:24px">
    <section class="side-card reveal"><h2>{before["h"]}</h2>{bp}<p><a href="{root}faq/">Read the FAQ</a></p></section>
    <div class="callout reveal">{icon("alert")}<div><h3>{copy["h"]}</h3>{"".join(f"<p>{b['html']}</p>" for b in copy["b"])}</div></div>
  </div>
  <div class="closing reveal" style="margin-top:24px"><strong>{last["h"]}</strong>{last["b"][0]["html"]}<p style="margin-top:6px;color:var(--ink)">{last["b"][1]["html"]}</p></div>
</div>
"""
    return page(
        "contact", body, title="Contact Social Save – Support, Feedback & Technical Help",
        desc="Contact Social Save for technical support, feedback and suggestions, or to report a problem with a downloader tool or the Android app.",
        kind="ContactPage", trail=[("Contact", None)],
    )


def not_found():
    body = f"""<div class="container">
  <div class="page-head"><h1>Page not found</h1><p class="lead">We could not find that page. It may have moved, or the link may be wrong.</p></div>
  <div class="empty">
    <span class="card-ic ic-blue">{icon("inbox")}</span>
    <h2>Try one of these</h2>
    <div class="tool-grid" style="width:100%;max-width:720px;text-align:left">{"".join(tool_card(s, "/") for s in ["social-media-downloader", "instagram-reels-downloader", "youtube-downloader"])}</div>
    <a class="btn btn-primary" href="/">Back to home {icon("arrow-right")}</a>
  </div>
</div>
"""
    return page("404", body, title="Page not found – Social Save", desc="Page not found.", noindex=True, abs_root=True)


# ---------------------------------------------------------------- files
def write(relpath, content):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def sitemap(slugs):
    rows = ""
    for s in slugs:
        lm = POST_DATE if s in POST else BUILD_DATE
        rows += f"  <url>\n    <loc>{url(s)}</loc>\n    <lastmod>{lm}</lastmod>\n  </url>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n'


def rfc822(iso):
    return datetime.datetime.fromisoformat(iso + "T08:00:00").strftime("%a, %d %b %Y %H:%M:%S +0000")


def feed():
    items = ""
    for p in POSTS:
        items += (
            f"    <item>\n      <title>{html.escape(p['title'])}</title>\n      <link>{url(p['slug'])}</link>\n"
            f'      <guid isPermaLink="true">{url(p["slug"])}</guid>\n      <pubDate>{rfc822(POST_DATE)}</pubDate>\n'
            f"      <category>{html.escape(p['category'])}</category>\n      <description>{html.escape(p['desc'])}</description>\n    </item>\n"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n  <channel>\n'
        f"    <title>Social Save Journal</title>\n    <link>{url('blog')}</link>\n"
        "    <description>Guides to saving videos, Reels, Shorts and photos.</description>\n    <language>en</language>\n"
        f'    <atom:link href="{SITE}feed.xml" rel="self" type="application/rss+xml"/>\n    <lastBuildDate>{rfc822(BUILD_DATE)}</lastBuildDate>\n'
        f"{items}  </channel>\n</rss>\n"
    )


def manifest():
    return json.dumps(
        {
            "name": "Social Save",
            "short_name": "Social Save",
            "description": "Free video, Reel and photo downloader.",
            "start_url": "./",
            "scope": "./",
            "display": "standalone",
            "background_color": "#f8fafc",
            "theme_color": "#2563eb",
            "icons": [
                {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
                {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
            ],
        },
        indent=2,
    ) + "\n"


def og_manifest(entries):
    return json.dumps(entries, indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    pages = {"": home()}
    pages[PATH["blog"]] = blog_index()
    for s in TOOL_ORDER:
        pages[PATH[s]] = tool_page(s)
    for p in POSTS:
        pages[PATH[p["slug"]]] = post_page(p["slug"])
    pages[PATH["faq"]] = faq_page()
    pages[PATH["about"]] = about()
    pages[PATH["contact"]] = contact()
    pages[PATH["privacy-policy"]] = legal(
        "privacy-policy", "Privacy Policy", DATA["meta"]["privacy-policy"]["title"], DATA["meta"]["privacy-policy"]["description"])
    pages[PATH["terms"]] = legal("terms", "Terms", DATA["meta"]["terms"]["title"], DATA["meta"]["terms"]["description"])
    for path, content in pages.items():
        write(os.path.join(path, "index.html") if path else "index.html", content)
    write("404.html", not_found())

    slugs = ["home"] + TOOL_ORDER + ["blog"] + [p["slug"] for p in POSTS] + ["faq", "about", "contact", "privacy-policy", "terms"]
    write("sitemap.xml", sitemap(slugs))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    write("feed.xml", feed())
    write("manifest.webmanifest", manifest())

    # input for tools/make-og.js
    og = [{"slug": "home", "title": "Free Video, Reel & Photo Downloader", "tag": "Social Save"}]
    for s in TOOL_ORDER:
        og.append({"slug": s, "title": LANDING[s]["h1"], "tag": "Downloader"})
    for p in POSTS:
        og.append({"slug": p["slug"], "title": p["title"], "tag": p["category"]})
    og += [
        {"slug": "blog", "title": "Journal: guides to saving videos, Reels and photos", "tag": "Journal"},
        {"slug": "faq", "title": "Frequently asked questions", "tag": "FAQ"},
        {"slug": "about", "title": "About Social Save", "tag": "About"},
        {"slug": "contact", "title": "Contact Social Save", "tag": "Contact"},
        {"slug": "privacy-policy", "title": "Privacy Policy", "tag": "Legal"},
        {"slug": "terms", "title": "Terms & Conditions", "tag": "Legal"},
        {"slug": "404", "title": "Page not found", "tag": "Social Save"},
    ]
    write("tools/og-manifest.json", og_manifest(og))
    print(f"built {len(pages) + 1} pages, sitemap with {len(slugs)} URLs")
