#!/usr/bin/env python3
"""SEO and integrity audit for the generated site. Standard library only.

Usage (from the repo root, after `python3 tools/build.py`):  python3 tools/check.py
Exit code 1 if any error is found. Warnings do not fail the run.
"""
import itertools
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://socialsave.site/"
errors, warnings = [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.props = {}
        self.links = []          # <link> tags (attrs dicts)
        self.hrefs = []          # <a href>
        self.ids = set()
        self.h = []              # (level, text)
        self._h = None
        self.imgs = []
        self.ld = []
        self._ld = None
        self.details = 0
        self.text = []
        self._skip = 0
        self._main = 0
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self._main += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            if a.get("name"):
                self.meta[a["name"]] = a.get("content", "")
            if a.get("property"):
                self.props[a["property"]] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        elif tag in ("h1", "h2", "h3", "h4"):
            self._h = [int(tag[1]), ""]
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "details":
            if a.get("class") != "toc-mobile":
                self.details += 1
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                self._ld = ""
            self.scripts.append(a)
            self._skip += 1
        elif tag == "style":
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self._main -= 1
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4") and self._h:
            self.h.append((self._h[0], self._h[1].strip()))
            self._h = None
        elif tag == "script":
            if self._ld is not None:
                self.ld.append(self._ld)
                self._ld = None
            self._skip -= 1
        elif tag == "style":
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h is not None:
            self._h[1] += data
        if self._ld is not None:
            self._ld += data
        elif not self._skip and self._main:
            self.text.append(data)


def parse(path):
    p = Page()
    p.feed(open(path, encoding="utf-8").read())
    return p


def page_files():
    out = {}
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "tools", "docs", "assets")]
        for f in files:
            if f in ("index.html", "404.html"):
                rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
                out[rel] = os.path.join(dirpath, f)
    return out


def url_of(rel):
    if rel == "404.html":
        return None
    d = os.path.dirname(rel)
    return SITE + (d + "/" if d else "")


def words(p):
    return re.findall(r"[a-z0-9']+", " ".join(p.text).lower())


def shingles(ws, n=6):
    return {" ".join(ws[i:i + n]) for i in range(max(0, len(ws) - n + 1))}


def main():
    files = page_files()
    pages = {rel: parse(path) for rel, path in files.items()}
    indexable = {rel: p for rel, p in pages.items() if rel != "404.html"}
    titles, descs, ids_seen = {}, {}, {}

    for rel, p in pages.items():
        name = rel
        # --- head
        t = p.title.strip()
        d = p.meta.get("description", "")
        if not t:
            err(name, "missing <title>")
        if len(t) > 65:
            warn(name, f"title is {len(t)} chars (aim for about 60 or fewer)")
        if len(t) < 25:
            warn(name, f"title is short ({len(t)} chars)")
        if not d:
            err(name, "missing meta description")
        elif rel != "404.html" and not 70 <= len(d) <= 165:
            warn(name, f"description is {len(d)} chars (aim for 70-160)")
        if rel != "404.html":
            titles.setdefault(t, []).append(name)
            descs.setdefault(d, []).append(name)
        canon = [l for l in p.links if l.get("rel") == "canonical"]
        if rel == "404.html":
            if "noindex" not in p.meta.get("robots", ""):
                err(name, "404 page must be noindex")
        else:
            if len(canon) != 1:
                err(name, f"expected exactly 1 canonical, found {len(canon)}")
            elif canon[0].get("href") != url_of(rel):
                err(name, f"canonical {canon[0].get('href')} != {url_of(rel)}")
            if "noindex" in p.meta.get("robots", ""):
                err(name, "unexpected noindex")
            if p.props.get("og:url") != url_of(rel):
                err(name, "og:url differs from the canonical URL")
            og = p.props.get("og:image", "")
            if not og.startswith(SITE + "assets/og/"):
                err(name, f"og:image should be a local share image, got {og}")
            else:
                local = os.path.join(ROOT, og.replace(SITE, ""))
                if not os.path.exists(local):
                    err(name, f"og:image file missing: {og}")
            for k in ("og:title", "og:description", "og:type", "og:site_name"):
                if not p.props.get(k):
                    err(name, f"missing {k}")
            if p.meta.get("twitter:card") != "summary_large_image":
                err(name, "missing twitter:card")
        # --- headings
        h1s = [h for h in p.h if h[0] == 1]
        if len(h1s) != 1:
            err(name, f"expected exactly 1 h1, found {len(h1s)}")
        prev = 1
        for level, text in p.h:
            if level > prev + 1:
                warn(name, f"heading jump h{prev} -> h{level} at '{text[:40]}'")
            prev = level
        # --- images
        for im in p.imgs:
            if "alt" not in im:
                err(name, f"<img> without alt: {im.get('src')}")
            if not im.get("width") or not im.get("height"):
                warn(name, f"<img> without width/height: {im.get('src')}")
        # --- ids
        # --- links
        base = os.path.dirname(files[rel])
        for href in p.hrefs:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                if href.startswith("http://socialsave.site") or href.startswith("http://www.socialsave.site"):
                    err(name, f"insecure internal link {href}")
                continue
            if href.startswith("#"):
                if href != "#" and href[1:] not in p.ids:
                    err(name, f"broken in-page anchor {href}")
                continue
            target = urlparse(href)
            path = unquote(target.path)
            full = os.path.normpath(os.path.join(ROOT if path.startswith("/") else base, path.lstrip("/") if path.startswith("/") else path))
            if os.path.isdir(full):
                full = os.path.join(full, "index.html")
            if not os.path.exists(full):
                err(name, f"broken link {href}")
            elif target.fragment and full.endswith(".html"):
                other = pages.get(os.path.relpath(full, ROOT))
                if other is not None and target.fragment not in other.ids:
                    err(name, f"broken anchor {href}")
        # --- JSON-LD
        if rel != "404.html":
            if not p.ld:
                err(name, "no JSON-LD found")
            for block in p.ld:
                try:
                    data = json.loads(block)
                except ValueError as e:
                    err(name, f"invalid JSON-LD: {e}")
                    continue
                graph = data.get("@graph", [data])
                types = []
                for node in graph:
                    ntype = node.get("@type")
                    types.append(ntype)
                    nid = node.get("@id")
                    if nid:
                        if nid in ids_seen.get(rel, set()):
                            err(name, f"duplicate @id {nid}")
                        ids_seen.setdefault(rel, set()).add(nid)
                    if ntype == "BreadcrumbList":
                        pos = [i["position"] for i in node["itemListElement"]]
                        if pos != list(range(1, len(pos) + 1)):
                            err(name, "BreadcrumbList positions are not sequential")
                    if ntype == "FAQPage":
                        n = len(node["mainEntity"])
                        if n != p.details:
                            err(name, f"FAQPage has {n} questions but the page shows {p.details}")
                    if ntype == "BlogPosting":
                        for k in ("headline", "datePublished", "dateModified", "author", "publisher", "image", "mainEntityOfPage"):
                            if k not in node:
                                err(name, f"BlogPosting missing {k}")
                        if len(node.get("headline", "")) > 110:
                            err(name, "BlogPosting headline over 110 characters")
                    if ntype == "SoftwareApplication" and "YOUR_APP_PACKAGE" in json.dumps(node):
                        err(name, "placeholder Play URL inside structured data")
                if "Organization" not in types or "WebSite" not in types:
                    err(name, "JSON-LD graph lacks Organization/WebSite")
        # --- misc
        if "YOUR_APP_PACKAGE" in open(files[rel], encoding="utf-8").read() and rel == "index.html":
            warn(name, "Play Store link is still the YOUR_APP_PACKAGE placeholder")

    for t, where in titles.items():
        if len(where) > 1:
            err("sitewide", f"duplicate title '{t}' on {', '.join(where)}")
    for d, where in descs.items():
        if len(where) > 1:
            err("sitewide", f"duplicate meta description on {', '.join(where)}")

    # --- sitemap vs pages
    sm_path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm_path):
        err("sitemap.xml", "missing")
    else:
        locs = set(re.findall(r"<loc>([^<]+)</loc>", open(sm_path, encoding="utf-8").read()))
        expected = {url_of(r) for r in indexable}
        for u in sorted(expected - locs):
            err("sitemap.xml", f"page missing from sitemap: {u}")
        for u in sorted(locs - expected):
            err("sitemap.xml", f"sitemap URL has no page: {u}")
    robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "robots.txt")) else ""
    if "Sitemap: " + SITE + "sitemap.xml" not in robots:
        err("robots.txt", "missing or does not point to the sitemap")
    if re.search(r"(?im)^disallow:\s*/\s*$", robots):
        err("robots.txt", "disallows the whole site")
    for f in ("manifest.webmanifest", "feed.xml", "favicon.ico", "assets/img/icon-192.png", "assets/img/icon-512.png", "CNAME"):
        if not os.path.exists(os.path.join(ROOT, f)):
            err(f, "missing")

    # --- duplicate-content risk between pages (shared 6-word phrases)
    bodies = {rel: shingles(words(p)) for rel, p in indexable.items() if rel.endswith("index.html")}
    legal = {"privacy-policy/index.html", "terms/index.html"}
    for a, b in itertools.combinations(sorted(bodies), 2):
        if not bodies[a] or not bodies[b] or {a, b} == legal:
            continue
        shared = len(bodies[a] & bodies[b])
        ratio = shared / min(len(bodies[a]), len(bodies[b]))
        if ratio > 0.45:
            warn("duplicate-content", f"{a} and {b} share {ratio:.0%} of 6-word phrases (main content only)")

    print(f"Checked {len(pages)} pages.")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
