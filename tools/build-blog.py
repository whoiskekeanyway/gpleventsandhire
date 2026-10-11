"""Build the blog from Markdown posts in tools/blog/*.md.

    python3 tools/build-blog.py

Writes blog/<slug>.html for every post, blog/index.html (newest first) and the
blog entries in sitemap.xml (between <!-- BLOG:START --> and <!-- BLOG:END -->).
The page shell (head, header, footer, scripts) is copied from
locations/sandton.html, which already uses ../ paths one folder deep.

Post format — front matter, then Markdown:

    ---
    title: Headline shown on the page (h1)
    seoTitle: Optional shorter <title> (max 60 characters)
    description: Meta description (max 155 characters)
    date: 2026-10-11
    updated: optional, same format
    category: Baby Showers
    image: assets/photo.webp   (or a full https:// URL)
    imageWidth: 1000
    imageHeight: 672
    imageAlt: What the photo shows
    imageSrcset: optional smaller copies, e.g. assets/a-800.webp 800w, assets/a-1000.webp 1000w
    excerpt: One or two sentences for the blog index card
    waText: Optional WhatsApp message for the call-to-action
    ---

Markdown supported: ## and ### headings, paragraphs, - and 1. lists, | tables |,
**bold**, *italic*, [links](page.html) (site links are written from the site
root, e.g. event-packages.html#baby-shower) and ![alt](image) images.
A "## Frequently asked questions" section of ### questions becomes an
accordion plus FAQPage structured data.
Styles: css/blog.css (bundled into css/site.css by tools/build-css.py).
"""
import datetime
import glob
import html
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gpleventsandhire.co.za/"
WA = "https://wa.me/27649318467?text="
LOGO = "https://res.cloudinary.com/dp24kap9x/image/upload/f_auto,q_auto,w_1000/v1759653499/variation-01_nfpohg.png"
FAQ_HEADING = "frequently asked questions"


def esc(text):
    return html.escape(text, quote=True)


def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n" + "\n".join("    " + line for line in text.split("\n")) + "\n    "


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


# ----- Markdown -----

def site_url(url):
    """Site links in posts are written from the root; posts live one folder down."""
    if re.match(r"^(https?:|mailto:|tel:|#)", url):
        return url
    return "../" + url.lstrip("/")


def inline(text):
    out = esc(text)
    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                 lambda m: f'<img src="{site_url(html.unescape(m.group(2)))}" alt="{m.group(1)}" loading="lazy">', out)
    def link(m):
        url = html.unescape(m.group(2))
        ext = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""
        return f'<a href="{esc(site_url(url))}"{ext}>{m.group(1)}</a>'
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", out)
    return out


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def markdown(body):
    """Returns (html, faqs, headings)."""
    blocks = re.split(r"\n\s*\n", body.strip())
    out, faqs, headings = [], [], []
    in_faq, question = False, None

    def close_question():
        nonlocal question
        if question:
            q, answer = question
            out.append(f'''
            <details class="faq-item">
                <summary class="faq-question">{inline(q)}</summary>
                <p class="faq-answer">{inline(" ".join(answer))}</p>
            </details>''')
            faqs.append((q, " ".join(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a).replace("**", "") for a in answer)))
            question = None

    for block in blocks:
        lines = block.strip().split("\n")
        first = lines[0]
        if first.startswith("## "):
            close_question()
            if in_faq:
                out.append("\n            </div>")
            title = first[3:].strip()
            in_faq = title.lower() == FAQ_HEADING
            headings.append(title)
            out.append(f'\n            <h2 id="{slugify(title)}">{inline(title)}</h2>')
            if in_faq:
                out.append('\n            <div class="faq-list">')
            for extra in lines[1:]:
                out.append(f"\n            <p>{inline(extra)}</p>")
        elif first.startswith("### "):
            close_question()
            title = first[4:].strip()
            if in_faq:
                question = (title, [" ".join(lines[1:])] if lines[1:] else [])
            else:
                out.append(f"\n            <h3>{inline(title)}</h3>")
                if lines[1:]:
                    out.append(f"\n            <p>{inline(' '.join(lines[1:]))}</p>")
        elif question is not None:
            question[1].append(" ".join(lines))
        elif first.startswith("|"):
            rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines if not re.match(r"^\|\s*-", ln)]
            head = "".join(f"<th scope=\"col\">{inline(c)}</th>" for c in rows[0])
            body_rows = "".join("\n                    <tr>" + "".join(
                (f'<th scope="row">{inline(c)}</th>' if i == 0 else f"<td>{inline(c)}</td>") for i, c in enumerate(r)) + "</tr>"
                for r in rows[1:])
            out.append(f'''
            <div class="post-table" role="region" aria-label="{esc(rows[0][0])} table" tabindex="0">
                <table>
                    <thead><tr>{head}</tr></thead>
                    <tbody>{body_rows}
                    </tbody>
                </table>
            </div>''')
        elif re.match(r"^(- |\d+\. )", first):
            tag = "ol" if re.match(r"^\d+\. ", first) else "ul"
            items, cur = [], None
            for ln in lines:
                m = re.match(r"^(?:- |\d+\. )(.*)", ln)
                if m:
                    if cur is not None:
                        items.append(cur)
                    cur = m.group(1)
                else:
                    cur += " " + ln.strip()
            items.append(cur)
            lis = "".join(f"\n                <li>{inline(i)}</li>" for i in items)
            out.append(f"\n            <{tag}>{lis}\n            </{tag}>")
        else:
            out.append(f"\n            <p>{inline(' '.join(l.strip() for l in lines))}</p>")
    close_question()
    if in_faq:
        out.append("\n            </div>")
    return "".join(out), faqs, headings


def read_post(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    assert m, f"{path}: missing front matter"
    meta = {}
    for line in m.group(1).split("\n"):
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["body"] = m.group(2)
    for key in ("title", "description", "date", "category", "image", "imageAlt", "excerpt"):
        assert meta.get(key), f"{path}: '{key}' is required"
    assert len(meta.get("seoTitle") or meta["title"]) <= 60, f"{path}: title over 60 characters — add a shorter seoTitle"
    assert len(meta["description"]) <= 155, f"{path}: description over 155 characters"
    datetime.date.fromisoformat(meta["date"])
    return meta


def image_url(meta, width=None):
    src = meta["image"]
    if src.startswith("http"):
        if width and "/upload/" in src:
            src = re.sub(r"/upload/(?:[^/]*,)?(?=v\d)", f"/upload/f_auto,q_auto,w_{width}/", src, count=1)
        return src
    return SITE + src.lstrip("/")


# ----- Page shell -----

SHELL = open(os.path.join(ROOT, "locations", "sandton.html"), encoding="utf-8").read()


def page(title, description, url, og_image, schema, main, og_type="article"):
    top = SHELL[:SHELL.index('<main id="main">')]
    bottom = SHELL[SHELL.index("</main>"):]
    top = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", top, count=1)
    top = re.sub(r'(<meta name="title" content=")[^"]*', lambda m: m.group(1) + esc(title), top)
    top = re.sub(r'(<meta name="description"\s+content=")[^"]*', lambda m: m.group(1) + esc(description), top, flags=re.S)
    top = re.sub(r'\s*<meta name="keywords"\s+content="[^"]*"\s*/?>', "", top, flags=re.S)
    top = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, top)
    top = re.sub(r'(<meta (?:property="og:url"|name="twitter:url") content=")[^"]*', lambda m: m.group(1) + url, top)
    top = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', lambda m: m.group(1) + esc(title), top)
    top = re.sub(r'(<meta (?:property="og:description"|name="twitter:description")\s+content=")[^"]*',
                 lambda m: m.group(1) + esc(description), top, flags=re.S)
    top = re.sub(r'(<meta (?:property="og:image"|name="twitter:image")\s+content=")[^"]*', lambda m: m.group(1) + og_image, top, flags=re.S)
    top = re.sub(r'(<meta property="og:type" content=")[^"]*', lambda m: m.group(1) + og_type, top)
    top = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", top, flags=re.S)
    top = top.replace(' aria-current="page"', "")
    scripts = "".join(f'\n    <script type="application/ld+json">{dump(obj)}</script>' for obj in schema)
    top = top.replace("</head>", scripts.lstrip("\n") + "\n</head>", 1) if scripts else top
    return top + main + bottom


def breadcrumb(items):
    lis = ""
    for i, (name, href) in enumerate(items):
        if href:
            lis += f'\n                <li class="breadcrumb-item"><a href="{href}">{esc(name)}</a></li>'
        else:
            lis += f'\n                <li class="breadcrumb-item breadcrumb-current" aria-current="page">{esc(name)}</li>'
    return f'''
    <nav aria-label="Breadcrumb" class="breadcrumb-nav">
        <div class="container">
            <ol class="breadcrumb-list">{lis}
            </ol>
        </div>
    </nav>
'''


def breadcrumb_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)]}


def build_post(meta, posts):
    body, faqs, headings = markdown(meta["body"])
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    minutes = max(1, round(words / 200))
    url = f"{SITE}blog/{meta['slug']}.html"
    title = meta.get("seoTitle") or meta["title"]
    wa_text = meta.get("waText") or f"Hi GPL Events, I read your guide \"{meta['title']}\" and I'd like a quote."
    img = meta["image"]
    src = img if img.startswith("http") else "../" + img
    dates = f'<time datetime="{meta["date"]}">{nice_date(meta["date"])}</time>'
    if meta.get("updated"):
        dates += f' · Updated <time datetime="{meta["updated"]}">{nice_date(meta["updated"])}</time>'

    others = [p for p in posts if p["slug"] != meta["slug"]][:3]
    more = ""
    if others:
        cards = "".join(card(p, "") for p in others)
        more = f'''
    <section class="blog-more" aria-labelledby="more-title">
        <div class="container">
            <h2 class="title" id="more-title">More from the blog</h2>
            <div class="blog-grid">{cards}
            </div>
        </div>
    </section>
'''

    main = f'''<main id="main">
{breadcrumb([("Home", "../index.html"), ("Blog", "index.html"), (meta["title"], None)])}
    <article class="post">
        <div class="post-header">
            <p class="eyebrow">{esc(meta["category"])}</p>
            <h1 class="post-title">{esc(meta["title"])}</h1>
            <p class="post-meta">{dates} · {minutes} min read · By GPL Events &amp; Hire</p>
        </div>

        <figure class="post-hero">
            <img src="{esc(src)}"{srcset(meta)} width="{meta.get("imageWidth", "1200")}" height="{meta.get("imageHeight", "800")}"
                fetchpriority="high" alt="{esc(meta["imageAlt"])}">
        </figure>

        <div class="post-body">{body}
        </div>

        <aside class="post-cta" aria-label="Get a quote">
            <h2>Planning something? Let's talk.</h2>
            <p>Send us your date, venue and guest count — we'll reply within 24 hours with ideas and a quote.</p>
            <div class="post-cta-actions">
                <a class="cta-primary cta-whatsapp" href="{WA + urllib.parse.quote(wa_text, safe='')}" target="_blank" rel="noopener noreferrer">
                    <i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp us</a>
                <a class="post-cta-link" href="../contact.html">Or use our contact form →</a>
            </div>
        </aside>
    </article>
{more}
    '''

    schema = [{
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": meta["title"], "description": meta["description"],
        "image": [image_url(meta)], "datePublished": meta["date"],
        "dateModified": meta.get("updated") or meta["date"],
        "mainEntityOfPage": url, "articleSection": meta["category"], "wordCount": words,
        "author": {"@type": "Organization", "name": "GPL Events & Hire", "url": SITE},
        "publisher": {"@type": "Organization", "name": "GPL Events & Hire", "url": SITE,
                      "logo": {"@type": "ImageObject", "url": LOGO}},
    }, breadcrumb_schema([("Home", SITE), ("Blog", SITE + "blog/"), (meta["title"], url)])]
    if faqs:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})

    out = page(title, meta["description"], url, image_url(meta), schema, main)
    assert out.rstrip().endswith("</html>")
    open(os.path.join(ROOT, "blog", meta["slug"] + ".html"), "w", encoding="utf-8").write(out)
    print(f"built blog/{meta['slug']}.html ({minutes} min read, {len(faqs)} FAQs)")


def srcset(meta, sizes="(max-width: 768px) 100vw, 736px"):
    """Optional 'imageSrcset: assets/a-800.webp 800w, assets/a-1000.webp 1000w' (site-root paths)."""
    if not meta.get("imageSrcset"):
        return ""
    parts = []
    # URLs can contain commas (Cloudinary transforms), so match "url 800w" pairs instead of splitting
    for path, width in re.findall(r"(\S+?),?\s+(\d+w)", meta["imageSrcset"]):
        parts.append(f"{path if path.startswith('http') else '../' + path} {width}")
    assert parts, "imageSrcset: expected 'url 800w, url 1200w'"
    return f' srcset="{esc(", ".join(parts))}" sizes="{sizes}"'


def card(p, prefix):
    img = p["image"]
    src = img if img.startswith("http") else "../" + img
    return f'''
                <article class="blog-card">
                    <a class="blog-card-link" href="{prefix}{p['slug']}.html">
                        <img src="{esc(src)}"{srcset(p, "(max-width: 768px) 100vw, 360px")} width="{p.get('imageWidth', '1200')}" height="{p.get('imageHeight', '800')}" loading="lazy" alt="{esc(p['imageAlt'])}">
                        <span class="blog-card-body">
                            <span class="blog-card-cat">{esc(p['category'])}</span>
                            <span class="blog-card-title">{esc(p['title'])}</span>
                            <span class="blog-card-excerpt">{esc(p['excerpt'])}</span>
                            <span class="blog-card-date">{nice_date(p['date'])}</span>
                        </span>
                    </a>
                </article>'''


def build_index(posts):
    url = SITE + "blog/"
    title = "Blog: Event Ideas, Prices & Guides | GPL Events & Hire"
    description = ("Event planning guides, décor ideas and honest price breakdowns for birthdays, baby showers, "
                   "weddings and corporate events across Gauteng.")
    cards = "".join(card(p, "") for p in posts)
    main = f'''<main id="main">
{breadcrumb([("Home", "../index.html"), ("Blog", None)])}
    <section class="blog-index">
        <div class="container">
            <div class="blog-index-header">
                <p class="eyebrow">The GPL blog</p>
                <h1 class="title">Event Ideas, Prices &amp; Guides</h1>
                <p class="subtitle">Practical advice from our styling team — what things cost, what to hire and how to plan a celebration your guests will remember.</p>
            </div>
            <div class="blog-grid">{cards}
            </div>
        </div>
    </section>

    '''
    schema = [{
        "@context": "https://schema.org", "@type": "Blog", "name": "GPL Events & Hire Blog", "url": url,
        "description": description,
        "publisher": {"@type": "Organization", "name": "GPL Events & Hire", "url": SITE},
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}blog/{p['slug']}.html",
                      "datePublished": p["date"]} for p in posts],
    }, breadcrumb_schema([("Home", SITE), ("Blog", url)])]
    og = image_url(posts[0]) if posts else LOGO
    out = page(title, description, url, og, schema, main, og_type="website")
    open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8").write(out)
    print(f"built blog/index.html ({len(posts)} posts)")


def update_sitemap(posts):
    path = os.path.join(ROOT, "sitemap.xml")
    sitemap = open(path, encoding="utf-8").read()
    newest = max([p.get("updated") or p["date"] for p in posts], default=datetime.date.today().isoformat())
    rows = [f"  <url><loc>{SITE}blog/</loc><lastmod>{newest}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>"]
    rows += [f"  <url><loc>{SITE}blog/{p['slug']}.html</loc><lastmod>{p.get('updated') or p['date']}</lastmod>"
             f"<changefreq>monthly</changefreq><priority>0.7</priority></url>" for p in posts]
    block = "  <!-- BLOG:START -->\n" + "\n".join(rows) + "\n  <!-- BLOG:END -->"
    if "<!-- BLOG:START -->" in sitemap:
        sitemap = re.sub(r"  <!-- BLOG:START -->.*?<!-- BLOG:END -->", lambda m: block, sitemap, flags=re.S)
    else:
        sitemap = sitemap.replace("</urlset>", block + "\n</urlset>")
    open(path, "w", encoding="utf-8").write(sitemap)
    print(f"sitemap.xml: {len(rows)} blog URLs")


os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
POSTS = sorted((read_post(p) for p in glob.glob(os.path.join(ROOT, "tools", "blog", "*.md"))),
               key=lambda p: p["date"], reverse=True)
for post in POSTS:
    build_post(post, POSTS)
build_index(POSTS)
update_sitemap(POSTS)
