"""FAQ page and the free-stock-media page copy."""

FAQ_GROUPS = [
    ("About Social Save", [
        ("What is Social Save?", "Social Save is a simple media downloading platform that brings tools for saving supported videos, Reels, Shorts, photos and free stock media together in one place. It is available on the web and as an Android app."),
        ("Is Social Save free?", "Yes. Social Save is free to use, with no sign-up and no watermark added by Social Save."),
        ("Which platforms does Social Save work with?", "Instagram, Facebook, TikTok and YouTube, including Reels and Shorts, plus supported photos. Platform support can change over time."),
        ("Can I save videos in my browser on this website?", "This website checks your link and identifies the platform, but online downloads are not switched on yet. The Social Save Android app brings the tools to your phone."),
    ]),
    ("Using the tools", [
        ("How do I use Social Save?", "Copy a supported URL, paste it into Social Save and choose the available download option. See [[how-to-copy-a-video-link-on-any-platform|how to copy a video link]] for each platform."),
        ("Why is my link not working?", "Check that the post is public and still available, that you copied the whole link and that it comes from a supported platform. Private accounts, deleted posts and age-restricted content cannot be saved, and creators can switch off downloads. Availability can vary depending on the source platform, media type and other technical factors."),
        ("What quality will I get?", "It depends on what the creator uploaded and on which versions the platform makes available. A downloader cannot add detail that was not in the original."),
        ("Which file format will I get?", "Most videos are MP4 and most photos are JPG or WebP. See [[mp4-vs-webm-vs-mov-video-formats|MP4 vs WebM vs MOV]] for how to choose."),
        ("Where do downloaded files go?", "That depends on your device and browser. Most phones use the Downloads folder or the gallery. See [[where-do-downloaded-videos-go-on-android|where downloaded videos go on Android]]."),
    ]),
    ("Privacy, rights and legal", [
        ("Can Social Save download from private accounts?", "No. Social Save works with publicly accessible links only."),
        ("Is it legal to download social media videos?", "It depends on the content, the platform's terms and the laws where you live. Read [[is-it-legal-to-download-social-media-videos|our plain-language guide]]. It is general information, not legal advice."),
        ("What happens to the links I paste?", "Our [[privacy-policy|Privacy Policy]] explains what information may be collected, including URLs and media requests, and how it is used."),
        ("How do I report a problem or a copyright concern?", "Use the [[contact|Contact]] page. Include the page or tool you were using and enough detail for us to understand and review the issue."),
    ]),
]

STOCK = {
    "h1": "Free Stock Photos & Videos Downloader",
    "title": "Free Stock Photos & Videos Downloader | Social Save",
    "desc": "Discover and download supported free stock photos and stock videos for creative and personal projects, and learn how to read a stock licence.",
    "lead": "Our free stock media tools are designed to help users discover and download supported stock photos and stock videos for creative and personal projects.",
    "sections": [
        ("h2", "Why use stock media"),
        ("p", "Content you find on social media usually belongs to its creator. Stock libraries are different: their files are offered under licences that say what you may do with them, which makes them a safer choice for blogs, presentations, videos and design work."),
        ("h2", "Read the licence every time"),
        ("ul", [
            "Check whether commercial use is allowed.",
            "Check whether attribution is required.",
            "Check what you may edit or combine.",
            "Do not assume a free licence covers the people, logos or artwork in a picture.",
        ]),
        ("p", "Our guide to [[best-free-stock-photo-and-video-sites|free stock photo and video sites]] lists well-known libraries and what to look for in each licence."),
        ("h2", "Photos and videos"),
        ("p", "Photos are small and easy to reuse. Video clips are larger, so check the resolution and format first; [[mp4-vs-webm-vs-mov-video-formats|MP4 vs WebM vs MOV]] explains the common choices."),
        ("p", "Social Save is continuously evolving with new tools, better experiences and additional media resources."),
    ],
    "faq": [
        ("What does free stock media mean?", "Free stock media is photography and video offered under a licence that allows reuse, often including commercial use, without paying per file. Terms differ between sites, so read the licence for each download."),
        ("Do I need to credit the creator?", "Sometimes. Some licences require attribution and others do not. Check the licence on the page you download from."),
        ("Can I use stock media in a commercial project?", "Many licences allow it, but not all, and some limit how you may use pictures of people or brands. Read the licence before you publish."),
        ("What is the difference between social media content and stock media?", "Social media content generally belongs to its creator, so reuse needs permission. Stock media is published to be reused under a stated licence."),
        ("Can Social Save download from stock sites?", "The stock media tools are designed to help you discover and download supported stock photos and stock videos. Availability can vary depending on the source and media type."),
    ],
    "tools": ["photo-downloader", "social-media-downloader", "youtube-downloader"],
    "guides": ["best-free-stock-photo-and-video-sites", "mp4-vs-webm-vs-mov-video-formats", "is-it-legal-to-download-social-media-videos"],
}
