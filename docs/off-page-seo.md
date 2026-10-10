# Off-page SEO playbook

Off-page SEO means everything that happens outside your own pages that tells search engines your site is trusted: links from other sites, brand mentions, profiles and reviews. It cannot be automated safely from code, so this is a plan for the site owner. It uses only approaches that follow Google's spam policies.

## Rules

- Earn links; do not buy them. Paid links, private blog networks, link exchanges at scale, automated comments and fake reviews can lead to a manual action or a loss of rankings.
- Quality over quantity. A few relevant links from real sites beat hundreds from directories nobody reads.
- Be useful first. Every outreach message should offer something the other person's readers want.
- Use accurate anchors. Mostly your brand name or the plain page title, not an exact-match keyword every time.
- Respect each platform's rules. Several social platforms restrict promoting downloaders; read their policies before you post.

## Foundations (week 1)

1. **Brand consistency.** Use the same name (Social Save), logo (`assets/img/logo.svg`) and one-line description everywhere. Short descriptions you can reuse:
   - 60 characters: *Free video, Reel and photo downloader. No sign-up.*
   - 160 characters: *Social Save is a simple media downloading platform for supported social media videos, Reels, Shorts, photos and free stock media.*
   - 300 characters: *Social Save is a simple and practical media downloading platform built for people who want an easier way to save content from the web. It brings tools for Instagram, Facebook, TikTok and YouTube together with free stock media, plus plain-language guides and an Android app.*
2. **Google Play listing.** Use the real app name, description and screenshots, and link to https://socialsave.site/ from the listing. App store pages are strong brand signals and often rank for the app name.
3. **Profiles you will maintain.** Create only the ones you will use (for example Facebook page, YouTube channel, Instagram, X, LinkedIn, Pinterest, GitHub). Add them to `SOCIAL_PROFILES` in `tools/build.py`.
4. **Google Search Console and Bing Webmaster Tools.** See `seo-checklist.md`.

## Product and tool directories (weeks 2 to 3)

Submit once, with the descriptions above and a real screenshot. Pick relevant ones; skip anything that looks like a link farm.

- Product Hunt, AlternativeTo, SaaSHub, Slant and similar software directories
- Android app directories and "best apps" lists run by editors, not auto-generated ones
- Crunchbase and similar company profiles, if you want a company presence
- Local or regional business and startup directories for your country

## Content that earns links (weeks 2 to 12)

People link to things that help. These pages are built to be linked to:

| Asset | Who might link | How to pitch |
|---|---|---|
| [Is it legal to download social media videos?](https://socialsave.site/blog/is-it-legal-to-download-social-media-videos/) | Creator, student and social-media blogs, digital-literacy resources | Offer it as a plain-language explainer for readers who ask the question |
| [How to copy a video link](https://socialsave.site/blog/how-to-copy-a-video-link-on-any-platform/) | Help centres, community wikis, tutorial writers | Offer it as a reference they can link instead of writing their own steps |
| [Best free stock photo and video sites](https://socialsave.site/blog/best-free-stock-photo-and-video-sites/) | Resource pages for designers, teachers and bloggers | Ask to be included if the page lists free resources |
| [MP4 vs WebM vs MOV](https://socialsave.site/blog/mp4-vs-webm-vs-mov-video-formats/) | Video-editing and photography blogs | Suggest it as a beginner explainer |

Ideas for a bigger linkable asset, only if you can do them well: an original survey with real respondents about how people save and keep online videos; a free checklist or one-page PDF; a short explainer video of your own.

## Outreach tactics

1. **Resource-page links.** Search for pages such as "free stock photo sites" or "video tools for teachers". If your page is genuinely a good addition, email the owner (template below).
2. **Broken-link replacement.** Find relevant pages with dead links to guides on the same topic. Tell the owner about the dead link and suggest your guide as a replacement, only if it fits.
3. **Guest articles.** Offer a useful article, not a promotion, to blogs your audience already reads. One link in the author bio or where it is natural.
4. **Expert quotes.** Platforms that connect journalists with sources (such as Qwoted or Featured) let you answer questions about online video, creator tools or digital rights. Answer only where you have real expertise.
5. **Community answers.** On Reddit, Quora, Stack Exchange or creator forums, answer questions fully, disclose that you work on Social Save, and link only where it adds something. Never post the same link repeatedly.
6. **Creator and student communities.** Share the legal and formats guides in relevant groups and newsletters where self-promotion is allowed.
7. **Reviews.** Ask real users to review the Android app after they have used it. Never offer payment for positive reviews or write them yourself.
8. **Partnerships.** Creator-tool sites, schools and digital-literacy projects can link to your guides if you offer something for their audience, such as a short workshop handout.

## 90-day schedule

| Weeks | Focus | Output |
|---|---|---|
| 1 | Foundations | Search Console and Bing set up, profiles created, Play listing completed |
| 2–3 | Directories | 5 to 10 relevant listings with consistent descriptions |
| 4–6 | Resource pages | 20 targeted outreach emails to resource pages and broken-link pages |
| 7–9 | Guest content | 2 guest articles pitched or published; 2 new Journal guides from the backlog |
| 10–12 | Review and double down | Check which links and pages brought impressions; repeat what worked |

## Outreach templates

Replace the bracketed parts and personalise the first line for each person. Keep emails short, polite and honest.

### Resource page

> Subject: Suggestion for your page "[page title]"
>
> Hi [name],
>
> I found your list of [topic] and liked [specific detail]. I wrote a plain-language guide that your readers might find useful: [title and link]. It covers [one-sentence summary].
>
> If you think it fits, it would be great to see it on the page. Either way, thanks for putting the list together.
>
> [your name], Social Save

### Broken link

> Subject: Broken link on "[page title]"
>
> Hi [name],
>
> While reading [page title] I noticed the link to [dead URL] no longer works. I recently published a guide on the same topic: [title and link]. If it is useful, you could use it as a replacement.
>
> Thanks for keeping the page up to date.
>
> [your name], Social Save

### Guest article

> Subject: Guest article idea: [working title]
>
> Hi [name],
>
> I read [recent article] and enjoyed it. I would like to write a guest article for [site] on [topic], aimed at [audience]. A short outline: [3 bullet points]. I would write it from scratch, with examples, and not as a sales piece.
>
> Would you be interested?
>
> [your name], Social Save

### Reply to a journalist or expert request

> Hi [name], here are my answers to your questions on [topic]. [Short, concrete, quotable answers.] I am [role] at Social Save, which provides media tools for supported social media content. Happy to provide more detail or a photo.

## Tracking sheet

Keep one spreadsheet with these columns: date, target site, page URL, contact, template used, status (sent, replied, link placed, declined), link URL, anchor, notes.

## What to measure

- Referring domains and the quality of the sites linking to you (Search Console → Links)
- Branded searches: people searching "Social Save" or "socialsave.site"
- Impressions, clicks and average position for the keywords in `keyword-map.md`
- Indexed pages and Core Web Vitals in Search Console
- App installs and reviews from the Play Console
