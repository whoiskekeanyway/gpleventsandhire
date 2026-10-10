"""Add "What's included", how-it-works, perfect-for, pair-with, service areas and
extra FAQs to the top hire item pages, from tools/item-extras.json.

    python3 tools/build-item-extras.py

Rewrites only the marked regions (<!-- INC:... -->, <!-- EXTRA:... -->,
<!-- FAQ:... -->), the FAQPage JSON-LD, and optional title/description.
Styles: .item-included / .item-extra in css/collections.css.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS = json.load(open(os.path.join(ROOT, "tools", "item-extras.json"), encoding="utf-8"))["items"]
AREAS = json.load(open(os.path.join(ROOT, "tools", "locations-data.json"), encoding="utf-8"))["areas"]


def esc(text):
    return html.escape(text, quote=True)


def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n" + "\n".join("    " + line for line in text.split("\n")) + "\n    "


def put(page, name, content, insert_at):
    """Replace <!-- NAME:START -->…<!-- NAME:END -->, or insert it at insert_at()."""
    block = f"<!-- {name}:START -->{content}<!-- {name}:END -->"
    pattern = re.compile(rf"<!-- {name}:START -->.*?<!-- {name}:END -->", re.S)
    if pattern.search(page):
        return pattern.sub(lambda m: block, page, count=1)
    i = insert_at(page)
    return page[:i] + block + page[i:]


def included(data):
    items = "".join(f"\n                        <li>{esc(i)}</li>" for i in data["included"])
    return f'''
                <div class="item-included">
                    <p class="item-included-title">What's included</p>
                    <ul>{items}
                    </ul>
                </div>
                '''


def extra(slug, data, product):
    out = '\n    <section class="item-extra" aria-label="More about this item">\n        <div class="item-extra-inner">'
    if data.get("event"):
        e = data["event"]
        out += f'''
            <h2 class="title">Seen at a real event</h2>
            <figure class="item-event">
                <img src="{esc(e['src'])}" width="1200" height="800" loading="lazy" alt="{esc(e['alt'])}">
                <figcaption>{esc(e['caption'])}</figcaption>
            </figure>
'''
    if data.get("steps"):
        steps = "".join(
            f'\n                <li><span class="item-step-num">{i}</span><strong>{esc(a)}</strong><span>{esc(b)}</span></li>'
            for i, (a, b) in enumerate(data["steps"], 1))
        out += f'\n            <h2 class="title">How it works</h2>\n            <ol class="item-steps">{steps}\n            </ol>\n'
    tags = "".join(f"\n                <li>{esc(t)}</li>" for t in data["perfect"])
    pairs = "".join(f'\n                <li><a href="{esc(u)}">{esc(n)}</a></li>' for n, u in data["pair"])
    areas = ",\n                ".join(
        f'<a href="../../locations/{a["slug"]}.html">{esc(a["name"])}</a>' for a in AREAS[:-1])
    last = AREAS[-1]
    out += f'''
            <h2 class="title">Perfect for</h2>
            <ul class="item-tags">{tags}
            </ul>

            <h2 class="title">Pair it with</h2>
            <ul class="item-related">{pairs}
            </ul>

            <p class="item-areas">{esc(product)} hire available in
                {areas} and
                <a href="../../locations/{last['slug']}.html">{esc(last['name'])}</a> —
                <a href="../../service-areas.html">see all areas</a>.</p>
        </div>
    </section>
    '''
    return out


def faq_items(rows):
    return "".join(f'''
                <details class="faq-item">
                    <summary class="faq-question">{esc(q)}</summary>
                    <p class="faq-answer">{esc(a)}</p>
                </details>''' for q, a in rows) + "\n                "


def build(slug, data):
    path = os.path.join(ROOT, "hire", "items", slug + ".html")
    page = open(path, encoding="utf-8").read()
    product = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<div class="hire-item-detail-info">\s*<h2>(.*?)</h2>', page, re.S).group(1))).strip()

    if data.get("title"):
        assert len(data["title"]) <= 60, slug
        page = re.sub(r"<title>.*?</title>", "<title>" + data["title"] + "</title>", page, count=1)
        for attr in ('name="title"', 'property="og:title"', 'name="twitter:title"'):
            page = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*', lambda m: m.group(1) + esc(data["title"]), page)
    if data.get("description"):
        assert len(data["description"]) <= 155, slug
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            page = re.sub(r'(<meta ' + re.escape(attr) + r'\s+content=")[^"]*', lambda m: m.group(1) + esc(data["description"]), page, flags=re.S)

    # What's included — just before the first WhatsApp button in the detail panel
    def before_cta(p):
        info = p.index('<div class="hire-item-detail-info">')
        return p.index('<a class="cta-secondary"', info)
    page = put(page, "INC", included(data), before_cta)

    # Extra section — straight after the detail section
    def after_detail(p):
        start = p.index('<section class="hire-item-detail-section">')
        return p.index("</section>", start) + len("</section>")
    page = put(page, "EXTRA", extra(slug, data, product), after_detail)

    # FAQs
    def faq_list(p):
        faq = p.index('<section class="faq-section">')
        start = p.index('<div class="faq-list">', faq) + len('<div class="faq-list">')
        end = p.index("\n            </div>", start)
        return start, end
    if '<section class="faq-section">' not in page:
        # Page has no FAQ section yet — add one right after the extra content
        section = (f'''
    <section class="faq-section">
        <div class="container">
            <div class="section-header">
                <h2 class="title">{esc(product)} Hire FAQs</h2>
                <p class="subtitle">Common questions about {esc(product.lower())} hire in Midrand</p>
            </div>
            <div class="faq-list">
            </div>
        </div>
    </section>
''')
        end = page.index("<!-- EXTRA:END -->") + len("<!-- EXTRA:END -->")
        page = page[:end] + section + page[end:]
    if "<!-- FAQ:START -->" in page:
        page = re.sub(r"<!-- FAQ:START -->.*?<!-- FAQ:END -->",
                      lambda m: "<!-- FAQ:START -->" + faq_items(data["faqs"]) + "<!-- FAQ:END -->", page, flags=re.S)
    else:
        s, e = faq_list(page)
        page = page[:s] + "\n                <!-- FAQ:START -->" + faq_items(data["faqs"]) + "<!-- FAQ:END -->" + page[e:]

    obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in data["faqs"]]}
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', page, re.S):
        if json.loads(m.group(2)).get("@type") == "FAQPage":
            page = page[:m.start(2)] + dump(obj) + page[m.end(2):]
            break
    else:
        page = page.replace("</head>", '    <script type="application/ld+json">' + dump(obj) + "</script>\n</head>", 1)

    assert page.rstrip().endswith("</html>"), slug
    open(path, "w", encoding="utf-8").write(page)
    print("built hire/items/" + slug + ".html")


for slug, data in ITEMS.items():
    build(slug, data)
