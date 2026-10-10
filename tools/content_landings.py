"""Copy for the keyword landing pages and the three existing tool pages.

Markup inside strings:
  [[slug|anchor text]]  -> internal link (resolved by build.py)
  basic inline HTML (<strong>, <em>) is allowed.
Section blocks: ("h2", text) ("p", html) ("ul", [html]) ("ol", [html]) ("table", [headers], [[cells]]) ("note", html)
"""

AVAILABILITY = (
    "Social Save works with publicly accessible links. Private accounts, deleted posts and age-restricted content "
    "cannot be saved, creators can switch off downloads for their own posts, and availability can vary depending on "
    "the source platform, media type and other technical factors."
)

RESPONSIBLY = (
    "Copyright still applies to anything you save. Keep a copy for personal reference when that is allowed, ask the "
    "creator before you repost or reuse it, and follow the platform's rules. Our plain-language guide, "
    "[[is-it-legal-to-download-social-media-videos|Is it legal to download social media videos?]], explains the "
    "basics. It is general information, not legal advice."
)

LANDINGS = [
    # ------------------------------------------------------------------ Instagram video
    {
        "slug": "instagram-video-downloader",
        "platform": "Instagram",
        "icon": "instagram",
        "h1": "Instagram Video Downloader",
        "title": "Instagram Video Downloader – Save IG Videos | Social Save",
        "desc": "Copy an Instagram video link, paste it into Social Save and follow the available download option. Steps, limits and answers to common questions.",
        "lead": "Found an Instagram video worth keeping? Social Save is built around one simple workflow: copy the video's link, paste it into Social Save, and choose the available download option.",
        "steps": [
            "Open the video in the Instagram app or on instagram.com.",
            "Tap the Share (paper plane) icon and choose <strong>Copy link</strong>. On a computer, copy the address from the browser bar.",
            "Paste the link into the box above and choose the available download option.",
        ],
        "sections": [
            ("h2", "Which Instagram links work"),
            ("p", "Instagram uses different links for different kinds of posts. A normal feed post has <code>/p/</code> in its link, a Reel has <code>/reel/</code>, and Stories use a separate link that stops working once the story disappears after 24 hours. Social Save recognises links from instagram.com and tells you when a link is not from a supported platform."),
            ("p", "If you want to save a Reel specifically, our [[instagram-reels-downloader|Instagram Reels downloader]] page has steps and tips just for that format. To save the pictures from a post instead, see the [[photo-downloader|photo downloader]]."),
            ("h2", "What can and cannot be saved"),
            ("ul", [
                "<strong>Can usually be saved:</strong> videos and Reels from public accounts, when the creator has not turned downloads off.",
                "<strong>Cannot be saved:</strong> posts from private accounts, deleted posts, and Stories that have already expired.",
                "<strong>Depends on the creator:</strong> Instagram lets creators control whether their Reels can be downloaded, so some public videos will not be available.",
            ]),
            ("h2", "Tips for a smoother result"),
            ("ul", [
                "Copy the full link. Share links often end with extra text after a question mark; that part is harmless.",
                "Open the link in a private browser window first. If you cannot see the video there, Social Save will not be able to see it either.",
                "Saved quality depends on what the creator uploaded, not on the downloader.",
            ]),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Is the Social Save Instagram video downloader free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
            ("Can I download videos from a private Instagram account?", "No. Social Save only works with publicly accessible links. If an account is private, only approved followers can see its posts, and Social Save cannot access them."),
            ("Why is my Instagram link not working?", "Check that the post is public and still exists, that you copied the whole link, and that it really comes from Instagram. " + AVAILABILITY),
            ("Where does a saved video go on my phone?", "It depends on your device and browser. Most phones place downloads in the Downloads folder or the gallery. See our guide to [[where-do-downloaded-videos-go-on-android|where downloaded videos go on Android]]."),
            ("Is it legal to download Instagram videos?", "Copyright applies to Instagram content and Instagram's terms set their own rules. Saving a video for personal reference is different from reposting it. Read [[is-it-legal-to-download-social-media-videos|our plain-language guide]]; it is general information, not legal advice."),
        ],
        "tools": ["instagram-reels-downloader", "photo-downloader", "social-media-downloader"],
        "guides": ["how-to-copy-a-video-link-on-any-platform", "how-to-save-instagram-reels", "is-it-legal-to-download-social-media-videos"],
    },
    # ------------------------------------------------------------------ Instagram Reels
    {
        "slug": "instagram-reels-downloader",
        "platform": "Instagram",
        "icon": "instagram",
        "h1": "Instagram Reels Downloader",
        "title": "Instagram Reels Downloader – Save Reels | Social Save",
        "desc": "How to save an Instagram Reel: copy the Reel link, paste it into Social Save and choose the available option. Includes limits, tips and a Reels FAQ.",
        "lead": "Reels are short vertical videos, and they are easy to lose in a feed. Copy the Reel's link, paste it into Social Save, and choose the available download option.",
        "steps": [
            "Open the Reel and tap the Share (paper plane) icon.",
            "Choose <strong>Copy link</strong>. The link contains <code>/reel/</code>.",
            "Paste it into the box above and choose the available download option.",
        ],
        "sections": [
            ("h2", "Why people save Reels"),
            ("p", "Creators keep Reels as visual references, marketers save examples of formats that work, and everyday users want a recipe, workout or tutorial available without a connection. Instagram's own bookmark saves a Reel inside the app only; it does not put a file on your phone. A link-based downloader is designed for the second case."),
            ("h2", "Reels and music"),
            ("p", "Many Reels use licensed music or audio from other creators. A saved Reel normally keeps that audio, but the right to use it often covers Instagram only. Watching offline is one thing; posting the same clip on another platform can trigger a copyright claim."),
            ("h2", "Why some Reels cannot be saved"),
            ("ul", [
                "The creator has turned off downloads for their Reels.",
                "The account is private or the Reel has been removed.",
                "The link is incomplete, or it is a Story or profile link instead of a Reel link.",
            ]),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("How do I copy a Reel link?", "Open the Reel, tap the paper plane Share icon and choose Copy link. On a computer, copy the address from the browser bar. The link will contain /reel/."),
            ("Will a saved Reel include its music?", "Usually the audio is part of the video. The licence for that music often covers Instagram only, so check before reposting anywhere else."),
            ("Does Social Save add a watermark to Reels?", "No. Social Save does not add its own watermark. Any logo or name that is already part of the original video stays as the creator published it."),
            ("Why can I save one Reel but not another?", "Creators can switch off downloads for their Reels, and private or removed posts are not available. " + AVAILABILITY),
            ("Is there a Reels downloader app?", "Social Save has an Android app that brings the same tools to your phone. Use the Google Play button on this page."),
        ],
        "tools": ["instagram-video-downloader", "photo-downloader", "social-media-downloader"],
        "guides": ["how-to-save-instagram-reels", "how-to-copy-a-video-link-on-any-platform", "is-it-legal-to-download-social-media-videos"],
    },
    # ------------------------------------------------------------------ Facebook
    {
        "slug": "facebook-video-downloader",
        "platform": "Facebook",
        "icon": "facebook",
        "h1": "Facebook Video Downloader",
        "title": "Facebook Video Downloader – Save FB Videos & Reels | Social Save",
        "desc": "Save public Facebook videos and Reels: copy the link, paste it into Social Save and choose the available option. Limits, privacy and troubleshooting.",
        "lead": "Facebook videos can disappear from a timeline as quickly as they arrive. Copy the video's link, paste it into Social Save and choose the available download option.",
        "steps": [
            "Open the video or Reel on Facebook and tap <strong>Share</strong>.",
            "Choose <strong>Copy link</strong>. Short links that start with <code>fb.watch</code> also work.",
            "Paste the link into the box above and choose the available download option.",
        ],
        "sections": [
            ("h2", "Facebook video links explained"),
            ("p", "Facebook shares videos in several forms: regular posts, the Watch tab, Reels and live videos that have ended. Links can look like <code>facebook.com/watch/?v=…</code>, <code>facebook.com/reel/…</code> or the short <code>fb.watch/…</code>. Social Save recognises all of these as Facebook links."),
            ("h2", "Public and private videos"),
            ("p", "Only videos that anyone can open can be saved. A video shared with friends, inside a private group, or with limited audience settings is not available to Social Save, even if you can see it while logged in. If you want a copy of a video you uploaded yourself, Facebook's own tools are the better route. Our guide to [[how-to-save-facebook-videos|saving Facebook videos]] compares the options."),
            ("h2", "Troubleshooting"),
            ("ul", [
                "Open the link in a private browser window. If Facebook asks you to log in, the video is not public.",
                "Copy the link from the Share menu rather than from a screenshot or a message preview.",
                "A live video becomes a normal video after it ends, but only if the owner leaves it public.",
            ]),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Is the Facebook video downloader free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
            ("Can I save a video from a private group?", "No. Social Save only works with publicly accessible links. Videos in private groups or shared with limited audiences cannot be accessed."),
            ("Does it work with fb.watch links?", "Yes. Social Save recognises fb.watch short links as Facebook links."),
            ("Can I download Facebook Reels?", "Reels from public accounts are treated like other public Facebook videos, as long as the creator allows it. " + AVAILABILITY),
            ("Is it legal to download Facebook videos?", "Copyright applies to Facebook videos and Facebook's terms set their own rules. Read [[is-it-legal-to-download-social-media-videos|our plain-language guide]]; it is general information, not legal advice."),
        ],
        "tools": ["social-media-downloader", "instagram-video-downloader", "tiktok-video-downloader"],
        "guides": ["how-to-save-facebook-videos", "how-to-copy-a-video-link-on-any-platform", "is-it-legal-to-download-social-media-videos"],
    },
    # ------------------------------------------------------------------ TikTok
    {
        "slug": "tiktok-video-downloader",
        "platform": "TikTok",
        "icon": "tiktok",
        "h1": "TikTok Video Downloader",
        "title": "TikTok Video Downloader – Save TikToks | Social Save",
        "desc": "Save TikTok videos: copy the video link, paste it into Social Save and choose the available option. Includes watermark facts, limits and FAQs.",
        "lead": "Copy the TikTok video's link, paste it into Social Save, and choose the available download option. No sign-up, and Social Save adds no watermark of its own.",
        "steps": [
            "Open the video in TikTok and tap the <strong>Share</strong> arrow.",
            "Choose <strong>Copy link</strong>. Links look like <code>tiktok.com/@name/video/…</code> or the short <code>vm.tiktok.com/…</code>.",
            "Paste the link into the box above and choose the available download option.",
        ],
        "sections": [
            ("h2", "TikTok and watermarks"),
            ("p", "When you save a video with TikTok's own Save button, TikTok adds its logo and the creator's username to the clip. Social Save does not add a watermark of its own. It does not claim to remove anything that is part of the original video, and it does not change who owns the content."),
            ("h2", "Who decides if a TikTok can be saved"),
            ("p", "TikTok creators can allow or block downloads of their videos. If a creator has turned downloads off, or the account is private, the video will not be available. Videos set to friends-only or private are never accessible."),
            ("h2", "Sounds and reuse"),
            ("p", "TikTok sounds are often licensed for use on TikTok only. A saved clip is fine for personal viewing, but uploading it elsewhere with the same music can lead to a copyright claim."),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Does Social Save add a watermark to TikTok videos?", "No. Social Save does not add its own watermark. Anything already in the original video stays as the creator published it."),
            ("Do vm.tiktok.com short links work?", "Yes. Social Save recognises short links from tiktok.com subdomains as TikTok links."),
            ("Why can't I save a particular TikTok?", "The creator may have turned off downloads, the account may be private, or the video may have been removed. " + AVAILABILITY),
            ("Is the TikTok video downloader free?", "Yes. Social Save is free to use, with no sign-up."),
            ("Can I repost a TikTok I saved?", "Only with the creator's permission. See [[is-it-legal-to-download-social-media-videos|our plain-language guide]]; it is general information, not legal advice."),
        ],
        "tools": ["social-media-downloader", "instagram-reels-downloader", "youtube-shorts-downloader"],
        "guides": ["how-to-save-tiktok-videos", "how-to-copy-a-video-link-on-any-platform", "is-it-legal-to-download-social-media-videos"],
    },
    # ------------------------------------------------------------------ YouTube Shorts
    {
        "slug": "youtube-shorts-downloader",
        "platform": "YouTube",
        "icon": "youtube",
        "h1": "YouTube Shorts Downloader",
        "title": "YouTube Shorts Downloader – Save Shorts | Social Save",
        "desc": "How to save a YouTube Short: copy the Shorts link, paste it into Social Save and choose the available option. Includes YouTube's own offline options.",
        "lead": "Copy the YouTube Short's link, paste it into Social Save, and choose the available download option. Read the notes below about YouTube's terms first.",
        "steps": [
            "Open the Short in the YouTube app and tap <strong>Share</strong>.",
            "Choose <strong>Copy link</strong>. Shorts links contain <code>/shorts/</code>.",
            "Paste the link into the box above and choose the available download option.",
        ],
        "sections": [
            ("h2", "Shorts links"),
            ("p", "A Short opens at an address that looks like <code>youtube.com/shorts/…</code>. Sharing from the app can also give you a short <code>youtu.be/…</code> link. Social Save recognises both forms as YouTube links. For regular long videos, use the [[youtube-downloader|YouTube video downloader]] page."),
            ("h2", "YouTube's own options"),
            ("p", "YouTube's terms generally allow downloading only through features YouTube provides. Two official routes are worth knowing: <strong>Save</strong> adds a Short to a playlist such as Watch later, and <strong>YouTube Premium</strong> includes offline downloads inside the YouTube app. If you are the creator, YouTube Studio lets you download your own uploads."),
            ("h2", "Before you use a downloader"),
            ("p", "Check YouTube's terms and the creator's rights. Saving a Short for private viewing is different from reuploading it. " + AVAILABILITY),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("How do I copy a YouTube Shorts link?", "Open the Short, tap Share and choose Copy link. The link contains /shorts/ or is a short youtu.be link."),
            ("Can I download a Short from my own channel?", "Yes. As the creator you can download your own uploads from YouTube Studio."),
            ("Does YouTube allow downloading Shorts?", "YouTube's terms generally permit downloads only through features YouTube provides, such as offline downloads with YouTube Premium. Read the terms and respect the creator's rights."),
            ("Why won't my Shorts link work?", "Check that the Short is public and still available, and that you copied the full link. " + AVAILABILITY),
            ("Is Social Save free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
        ],
        "tools": ["youtube-downloader", "tiktok-video-downloader", "instagram-reels-downloader"],
        "guides": ["how-to-save-youtube-shorts", "how-to-copy-a-video-link-on-any-platform", "is-it-legal-to-download-social-media-videos"],
    },
    # ------------------------------------------------------------------ Photos
    {
        "slug": "photo-downloader",
        "platform": None,
        "icon": "image",
        "h1": "Photo Downloader",
        "title": "Photo Downloader – Save Photos from Social Media | Social Save",
        "desc": "Save supported photos from public Instagram and Facebook posts: copy the link, paste it into Social Save and choose the available option.",
        "lead": "Social Save is not only for video. Copy the link to a public post with a photo, paste it into Social Save and choose the available download option.",
        "steps": [
            "Open the post that contains the photo and copy its link from the Share menu.",
            "Paste the link into the box above.",
            "Choose the available download option for the photo.",
        ],
        "sections": [
            ("h2", "Photos on social media"),
            ("p", "Photos are shared as single images and as carousels that hold several pictures in one post. Quality depends on what the owner uploaded and on which sizes the platform makes available; a photo that was small to start with cannot be made sharper by a downloader."),
            ("h2", "Common photo formats"),
            ("table", ["Format", "Good for", "Notes"], [
                ["JPG", "Photographs", "Small files, widely supported, slight quality loss."],
                ["PNG", "Graphics, screenshots, text", "Larger files, supports transparency."],
                ["WebP", "Web images", "Smaller than JPG at similar quality, newer."],
            ]),
            ("h2", "People and privacy"),
            ("p", "A photo of a person is also about that person. Keep saved photos for personal use and do not share or publish pictures of other people without their permission. For images you can reuse freely, browse licensed libraries through our [[free-stock-media|free stock media]] page instead."),
            ("h2", "Save responsibly"),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Can I download photos from Instagram and Facebook?", "Photos from public posts can be supported, as long as the owner has not restricted them. " + AVAILABILITY),
            ("What file format will I get?", "That depends on the source. Most social photos are JPG or WebP."),
            ("Can I use a downloaded photo on my website?", "Only with the owner's permission or a licence that allows it. For free-to-use images, see [[best-free-stock-photo-and-video-sites|our guide to free stock sites]]."),
            ("Does Social Save add a watermark to photos?", "No. Social Save does not add its own watermark."),
            ("Why can't I save a carousel?", "Availability can vary depending on the source platform, media type and other technical factors."),
        ],
        "tools": ["instagram-video-downloader", "free-stock-media", "social-media-downloader"],
        "guides": ["best-free-stock-photo-and-video-sites", "mp4-vs-webm-vs-mov-video-formats", "is-it-legal-to-download-social-media-videos"],
    },
]

# --------------------------------------------------------------------------- existing tool pages
EXISTING = {
    "social-media-downloader": {
        "h1": "Social Media Video Downloader",
        "title": "Social Media Video Downloader – Reels, Shorts & Photos",
        "desc": "Paste a public Instagram, Facebook, TikTok or YouTube link and Social Save detects the platform to help you save videos, Reels, Shorts and photos.",
        "lead": "Social Save provides a collection of social media downloading tools designed around common media formats and platforms. Copy a supported URL, paste it into Social Save, and choose the available download option.",
        "sections": [
            ("h2", "Where to find the link"),
            ("p", "Every platform has a Share button that can copy a link. Pick your platform below for a dedicated page with steps and answers."),
            ("table", ["Platform", "How to copy the link", "Dedicated page"], [
                ["Instagram", "Share (paper plane) → Copy link", "[[instagram-video-downloader|Instagram video downloader]], [[instagram-reels-downloader|Reels downloader]]"],
                ["Facebook", "Share → Copy link", "[[facebook-video-downloader|Facebook video downloader]]"],
                ["TikTok", "Share arrow → Copy link", "[[tiktok-video-downloader|TikTok video downloader]]"],
                ["YouTube", "Share → Copy", "[[youtube-downloader|YouTube video downloader]], [[youtube-shorts-downloader|Shorts downloader]]"],
                ["Photos", "Copy the post link", "[[photo-downloader|Photo downloader]]"],
            ]),
            ("h2", "What Social Save is designed for"),
            ("p", "Social Save is a simple, practical media downloading tool for people who want an easier way to save content from the web: content creators, students, marketers, researchers and everyday internet users. There are no complicated settings to learn. You paste a link, process it and download the available media."),
            ("h2", "Limits to know about"),
            ("p", AVAILABILITY),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Which platforms does Social Save support?", "Instagram, Facebook, TikTok and YouTube, including Reels and Shorts, plus supported photos. Platform support can change."),
            ("Can I save videos in my browser on this site?", "This page checks your link and identifies the platform, but online downloads are not switched on yet. The Social Save Android app brings the tools to your phone."),
            ("Is Social Save free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
            ("Do I need to install anything?", "No installation is needed to check a link on this website. The Android app is optional."),
            ("Is it legal to save videos from social media?", "That depends on the content, the platform's terms and the laws where you live. See [[is-it-legal-to-download-social-media-videos|our plain-language guide]]; it is general information, not legal advice."),
        ],
        "tools": ["instagram-reels-downloader", "facebook-video-downloader", "tiktok-video-downloader"],
        "guides": ["how-to-copy-a-video-link-on-any-platform", "how-to-save-instagram-reels", "where-do-downloaded-videos-go-on-android"],
    },
    "youtube-downloader": {
        "h1": "YouTube Video & Shorts Downloader",
        "title": "YouTube Video Downloader – Save Videos & Shorts | Social Save",
        "desc": "Copy a YouTube video or Shorts link, paste it into Social Save and follow the available option. Includes YouTube's own offline options and terms notes.",
        "lead": "Copy a supported YouTube URL, paste it into Social Save, and choose the available download option. Please read the notes on YouTube's terms below.",
        "sections": [
            ("h2", "Links this page understands"),
            ("ul", [
                "Regular videos: <code>youtube.com/watch?v=…</code>",
                "Short links from the Share menu: <code>youtu.be/…</code>",
                "Shorts: <code>youtube.com/shorts/…</code> (see the [[youtube-shorts-downloader|Shorts downloader]])",
            ]),
            ("h2", "YouTube's own options come first"),
            ("p", "YouTube's terms generally allow downloading only through features YouTube provides. <strong>YouTube Premium</strong> offers offline downloads inside the YouTube app, and creators can download their own uploads from YouTube Studio. If one of those covers what you need, use it."),
            ("h2", "When a downloader is appropriate"),
            ("p", "Use a downloader only for content you own, content with a licence that permits it, or where you have the creator's permission. " + AVAILABILITY),
            ("p", RESPONSIBLY),
        ],
        "faq": [
            ("Can Social Save download a YouTube video?", "Social Save checks YouTube links and is designed around copy, paste and choose-a-download. Online downloads are not switched on yet on this website. Respect YouTube's terms and the creator's rights."),
            ("What is the difference between this page and the Shorts page?", "This page covers regular videos and Shorts links; the [[youtube-shorts-downloader|Shorts downloader]] page focuses on Shorts only."),
            ("How do I copy a YouTube link?", "Open the video, tap Share and choose Copy link, or copy the address from your browser."),
            ("Is Social Save free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
            ("Can I download my own YouTube videos?", "Yes. As the creator you can download your uploads from YouTube Studio."),
        ],
        "tools": ["youtube-shorts-downloader", "social-media-downloader", "tiktok-video-downloader"],
        "guides": ["how-to-save-youtube-shorts", "is-it-legal-to-download-social-media-videos", "mp4-vs-webm-vs-mov-video-formats"],
    },
}


# --------------------------------------------------------------------------- extra depth (inserted before "Save responsibly")
_EXTRA = {
    "instagram-video-downloader": [
        ("h2", "Who uses an Instagram video downloader"),
        ("ul", [
            "<strong>Creators</strong> keep public videos as visual references for their own shoots.",
            "<strong>Students and researchers</strong> save educational videos to watch offline, where permitted.",
            "<strong>Marketers</strong> keep examples of formats and trends for campaign reviews.",
            "<strong>Everyday users</strong> save a recipe, a travel tip or a workout to watch without a connection.",
        ]),
        ("h2", "Troubleshooting checklist"),
        ("ol", [
            "Open the link in a private browser window. If you cannot see the video, the account is probably private.",
            "Check that the link points to a video, not to a profile or a hashtag.",
            "Copy the link again from the Share menu in case the first copy was cut off.",
            "Try a different post from the same account. If other posts work, the creator may have restricted that one.",
            "Wait a few minutes and try again. Availability can vary depending on the source platform, media type and other technical factors.",
        ]),
        ("h2", "Photos and carousels"),
        ("p", "Instagram posts can hold several pictures or a mix of photos and video. For pictures, use the [[photo-downloader|photo downloader]]; the workflow is the same, and it also applies to the first image of a carousel link."),
    ],
    "instagram-reels-downloader": [
        ("h2", "Reels compared with other Instagram videos"),
        ("table", ["Type", "Link contains", "Format", "Notes"], [
            ["Reel", "/reel/", "Vertical, short", "Often uses licensed music"],
            ["Feed video", "/p/", "Square, portrait or landscape", "Appears on a profile grid"],
            ["Story", "/stories/", "Vertical, 24 hours", "Stops working after it expires"],
        ]),
        ("h2", "Troubleshooting a Reel link"),
        ("ol", [
            "Check that the link contains <code>/reel/</code>. If it contains <code>/p/</code>, use the [[instagram-video-downloader|Instagram video downloader]] instead.",
            "Make sure the account is public. Private accounts are never accessible.",
            "If the Reel was shared to you in a message, open it first and copy the link from the Share menu.",
            "A very new or just-edited Reel can take a moment to become available. Try again later.",
        ]),
        ("h2", "Ideas for using saved Reels"),
        ("ul", [
            "Keep a private folder of recipes, workouts and tutorials you want to follow offline.",
            "Collect examples of editing styles you like, for your own inspiration.",
            "Save a Reel you created, so you have the original file and not only the app version.",
        ]),
    ],
    "facebook-video-downloader": [
        ("h2", "Types of Facebook video"),
        ("table", ["Type", "Where it lives", "Typical link", "Public?"], [
            ["Page or profile video", "A post on a page or profile", "facebook.com/watch/?v=…", "Depends on audience setting"],
            ["Reel", "Reels tab", "facebook.com/reel/…", "Usually, from public accounts"],
            ["Group video", "Inside a group", "A group post link", "Only if the group is public"],
            ["Ended live video", "A post on a page or profile", "A post link", "If the owner left it public"],
        ]),
        ("h2", "Who saves Facebook videos"),
        ("ul", [
            "<strong>Local organisations</strong> that want a copy of a public announcement for their records.",
            "<strong>Families</strong> keeping a video they were tagged in, after asking the person who posted it.",
            "<strong>Students</strong> keeping lecture-style videos for offline study, where allowed.",
        ]),
        ("h2", "If a Facebook link will not work"),
        ("ol", [
            "Open the link while logged out or in a private window. A login prompt means it is not public.",
            "Check that you copied a video link and not the link to a whole page or album.",
            "For fb.watch links, copy a fresh one from the Share menu.",
            "Ask the owner to change the audience to Public, if you are the intended viewer and they agree.",
        ]),
    ],
    "tiktok-video-downloader": [
        ("h2", "TikTok links explained"),
        ("table", ["Link", "What it is", "Works with Social Save?"], [
            ["tiktok.com/@name/video/…", "A full video link", "Yes, for public videos"],
            ["vm.tiktok.com/… or vt.tiktok.com/…", "A short share link", "Yes"],
            ["tiktok.com/@name", "A profile", "No, open a video first"],
            ["tiktok.com/music/…", "A sound page", "No, open a video first"],
        ]),
        ("h2", "If a TikTok will not save"),
        ("ol", [
            "Open the link in a private browser window. If the video does not play, it is private or removed.",
            "Check that you copied a video link, not a profile or a sound.",
            "Try again later; availability can vary depending on the source platform and other technical factors.",
            "If you are the creator, check your own download settings for that video.",
        ]),
        ("h2", "For creators"),
        ("p", "You decide whether others can download your videos. If you want your work to travel with its credit, leaving downloads on keeps the TikTok watermark attached to saved copies. If you need more control, switch downloads off for videos you would rather keep inside TikTok."),
    ],
    "youtube-shorts-downloader": [
        ("h2", "Shorts compared with regular videos"),
        ("table", ["Feature", "Shorts", "Regular video"], [
            ["Link", "youtube.com/shorts/…", "youtube.com/watch?v=… or youtu.be/…"],
            ["Shape", "Vertical, short", "Usually horizontal, any length"],
            ["Where to start", "This page", "[[youtube-downloader|YouTube video downloader]]"],
        ]),
        ("h2", "Official options compared"),
        ("table", ["Option", "What you get", "Where it works"], [
            ["Save to Watch later", "A bookmark", "Inside YouTube"],
            ["YouTube Premium download", "Offline viewing", "Inside the YouTube app"],
            ["YouTube Studio download", "Your own upload as a file", "Your own channel"],
        ]),
        ("h2", "If a Shorts link will not work"),
        ("ol", [
            "Check that the Short is public and has not been removed.",
            "Copy the link again from the Share menu.",
            "Open it in a private window; if it plays there, the link is fine.",
            "Remember that availability can vary depending on the source and that creators control their content.",
        ]),
    ],
    "photo-downloader": [
        ("h2", "Getting the best quality"),
        ("ul", [
            "Choose the largest version offered; thumbnails are much smaller than the original.",
            "Do not edit and re-save a JPG repeatedly: each save loses a little quality.",
            "Keep the original file and make edits on a copy.",
        ]),
        ("h2", "Common uses"),
        ("ul", [
            "Keeping a photo you were tagged in, after asking the person who posted it.",
            "Saving a product picture or a recipe photo for personal reference.",
            "Collecting images for a mood board, with credit and permission if you plan to publish.",
        ]),
        ("h2", "If a photo will not save"),
        ("ol", [
            "Check that the post is public and still available.",
            "Make sure you pasted the post link, not the image file address from another site.",
            "Try a different post from the same account to see whether the restriction is for one post only.",
        ]),
    ],
    "social-media-downloader": [
        ("h2", "Choosing the right page"),
        ("p", "Each dedicated page checks that your link matches its platform and gives you tips that fit it. If you are not sure which one you need, paste the link above: Social Save detects the platform for you."),
        ("h2", "Troubleshooting"),
        ("ol", [
            "Open the link in a private browser window. If it does not play, it is not public.",
            "Check that the link points to a specific video or photo, not to a profile.",
            "Copy the link again from the platform's Share menu.",
            "Try another post from the same account. If it works, the creator may have restricted the first one.",
        ]),
        ("h2", "Android app"),
        ("p", "Social Save is also available as an Android app, bringing our media tools directly to mobile devices. The Android experience focuses on convenience, speed and a simple workflow."),
    ],
    "youtube-downloader": [
        ("h2", "YouTube link formats"),
        ("table", ["Link", "What it is"], [
            ["youtube.com/watch?v=…", "A regular video"],
            ["youtu.be/…", "The short link from the Share menu"],
            ["youtube.com/shorts/…", "A Short"],
            ["youtube.com/playlist?list=…", "A playlist; open a single video instead"],
        ]),
        ("h2", "Official options compared"),
        ("table", ["Option", "What you get", "Who it is for"], [
            ["YouTube Premium downloads", "Offline viewing inside the app", "Anyone who watches offline a lot"],
            ["YouTube Studio download", "Your own upload as a file", "Creators"],
            ["Link-based tool", "A file, where available and permitted", "Content you own or have permission to keep"],
        ]),
        ("h2", "If your YouTube link will not work"),
        ("ol", [
            "Check that the video is public and not age-restricted or removed.",
            "Make sure the link points to a single video, not a channel or playlist.",
            "Copy it again from the Share menu.",
        ]),
    ],
    "free-stock-media": [
        ("h2", "How to choose good stock media"),
        ("ul", [
            "Search with simple words, then narrow by orientation or colour.",
            "Pick a resolution larger than you need, so you can crop.",
            "Prefer files with a clear licence on the download page.",
            "Avoid images with recognisable people or brands unless the licence clearly covers them.",
        ]),
        ("h2", "If a stock download does not work"),
        ("ol", [
            "Check that you pasted the link to a specific photo or video page.",
            "Try another file from the same source to see if the problem is with one item.",
            "Availability can vary depending on the source and media type.",
        ]),
    ],
}


def _merge_extra():
    for slug, extra in _EXTRA.items():
        spec = next((l for l in LANDINGS if l["slug"] == slug), None) or EXISTING.get(slug)
        if spec is None:
            continue
        sections = spec["sections"]
        idx = next((i for i, b in enumerate(sections) if b[0] == "h2" and b[1].startswith("Save responsibly")), len(sections))
        spec["sections"] = sections[:idx] + extra + sections[idx:]


_merge_extra()
