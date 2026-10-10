"""Build the 7 location pages (locations/*.html) from tools/locations-data.json.

    python3 tools/build-locations.py

Rewrites each page's <head> title/description, hero text, breadcrumb, the
content between <!-- LOC:START --> and <!-- LOC:END -->, and the
LocalBusiness / FAQPage / BreadcrumbList JSON-LD. Package prices and guest
ranges are read from tools/packages-data.json so they never drift.
"""
import html
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS = json.load(open(os.path.join(ROOT, "tools", "locations-data.json"), encoding="utf-8"))["areas"]
PACKAGES = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "tools", "packages-data.json"), encoding="utf-8"))["events"]["categories"]}
SITE = "https://www.gpleventsandhire.co.za/"
WA = "https://wa.me/27649318467?text="
FREE_GIFT_AREAS = "Midrand, Waterfall, Carlswald, Kyalami and Fourways"


def esc(text):
    return html.escape(text, quote=True)


def wa(message):
    return WA + urllib.parse.quote(message, safe="")


def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n" + "\n".join("    " + line for line in text.split("\n")) + "\n    "


def set_schema(page, obj):
    kind = obj["@type"]
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', page, re.S):
        if json.loads(m.group(2)).get("@type") == kind:
            return page[:m.start(2)] + dump(obj) + page[m.end(2):]
    return page.replace("</head>", '    <script type="application/ld+json">' + dump(obj) + "</script>\n</head>", 1)


def gift_fact(area):
    if area["giftDelivery"] == "free":
        return f"Free gift delivery in {area['name']}"
    return f"Gift delivery to {area['name']}: R150 flat rate"


def package_card(area, cat_id):
    c = PACKAGES[cat_id]
    first = c["tiers"][0]["price"]
    top = c["tiers"][-1]["guestsMax"]
    msg = f"Hi GPL Events, I'm planning a {c['tab'].lower()} event in {area['name']}. My date is: "
    return f'''
                    <article class="loc-card">
                        <h3>{esc(c['title'])}</h3>
                        <p class="loc-price"><span>From</span> {esc(first)}</p>
                        <p class="loc-meta">Essential, Signature &amp; Luxe · up to {top} guests · setup included</p>
                        <p>{esc(c['intro'])}</p>
                        <div class="loc-card-actions">
                            <a class="loc-btn loc-btn-outline" href="../event-packages.html#{cat_id}">Compare packages</a>
                            <a class="loc-btn loc-btn-wa" href="{wa(msg)}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Enquire</a>
                        </div>
                    </article>'''


def region(area):
    name = esc(area["name"])
    paras = "".join(f"\n                <p>{esc(p)}</p>" for p in area["intro"])
    facts = [
        ("fa-location-dot", area["baseFact"]),
        ("fa-wand-magic-sparkles", "Setup included in every event package"),
        ("fa-truck", "Event delivery & collection usually around R1,600"),
        ("fa-gift", gift_fact(area)),
    ]
    facts_html = "".join(f'\n                    <li><i class="fas {i}" aria-hidden="true"></i><span>{esc(t)}</span></li>' for i, t in facts)
    cards = "".join(package_card(area, cid) for cid in area["focus"])
    hire = "".join(f'\n                    <li><a href="../{esc(u)}">{esc(label)}</a></li>' for label, u in area["hire"])
    faqs = "".join(f'''
                <details class="faq-item">
                    <summary class="faq-question">{esc(q)}</summary>
                    <p class="faq-answer">{esc(a)}</p>
                </details>''' for q, a in area["faqs"])
    others = "".join(
        f'\n                    <li><a href="{o["slug"]}.html">{esc(o["name"])}</a></li>' for o in AREAS if o["slug"] != area["slug"])
    if area["giftDelivery"] == "free":
        gift_line = f"Gift hampers and fresh bouquets are delivered <strong>free in {name}</strong> — order before 12:00 for same-day bouquets."
    else:
        gift_line = (f"Gift hampers and fresh bouquets are delivered to {name} for a <strong>R150 flat rate</strong> "
                     f"(free in {FREE_GIFT_AREAS}).")
    return f'''<div class="loc-page">

            <section class="loc-intro" aria-labelledby="loc-intro-title">
                <h2 class="title" id="loc-intro-title">Events in {name}</h2>{paras}
                <ul class="loc-facts">{facts_html}
                </ul>
            </section>

            <section class="loc-packages" aria-labelledby="loc-pkg-title">
                <h2 class="title" id="loc-pkg-title">Popular packages in {name}</h2>
                <p class="subtitle">Three tiers for every occasion — pick a starting point and we'll tailor it to your theme.</p>
                <div class="loc-cards">{cards}
                </div>
                <p class="loc-more"><a href="../event-packages.html">See all event packages →</a></p>
            </section>

            <section class="loc-hire" aria-labelledby="loc-hire-title">
                <h2 class="title" id="loc-hire-title">Popular hire items in {name}</h2>
                <p class="subtitle">Prefer to style it yourself? Hire individual pieces — delivery and collection quoted separately.</p>
                <ul class="loc-chips">{hire}
                </ul>
                <p class="loc-more"><a href="../hire.html">Search all hire items →</a></p>
            </section>

            <section class="loc-gifting">
                <i class="fas fa-gift" aria-hidden="true"></i>
                <div>
                    <h2>Bespoke gifts in {name}</h2>
                    <p>{gift_line}</p>
                </div>
                <a class="loc-btn loc-btn-outline" href="../bespoke-gifting.html">Browse gifts</a>
            </section>

            <section class="faq-section loc-faq">
                <div class="container">
                    <div class="section-header">
                        <h2 class="title">{name} Event FAQs</h2>
                        <p class="subtitle">Common questions about events and décor hire in {name}</p>
                    </div>
                    <div class="faq-list">{faqs}
                    </div>
                </div>
            </section>

            <section class="loc-nearby" aria-labelledby="loc-nearby-title">
                <h2 id="loc-nearby-title">We also serve</h2>
                <ul class="loc-chips">{others}
                </ul>
            </section>

        </div>'''


def build(area):
    path = os.path.join(ROOT, "locations", area["slug"] + ".html")
    page = open(path, encoding="utf-8").read()
    url = SITE + "locations/" + area["slug"] + ".html"

    # ----- head
    page = re.sub(r"<title>.*?</title>", "<title>" + esc(area["title"]).replace("&amp;", "&") + "</title>", page, count=1)
    for attr in ('name="title"', 'property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*', lambda m: m.group(1) + esc(area["title"]), page)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r'\s+content=")[^"]*', lambda m: m.group(1) + esc(area["description"]), page, flags=re.S)
    page = re.sub(r'(<meta name="keywords"\s+content=")[^"]*', lambda m: m.group(1) + esc(area["keywords"]), page, flags=re.S)

    # ----- hero
    hero_msg = f"Hi GPL Events, I'm planning an event in {area['name']}. Please share pricing and availability."
    hero = f'''<div class="hero-content">
            <h1 class="hero-title">{esc(area['h1'])}</h1>
            <p class="hero-subtitle">{esc(area['heroSub'])}</p>
            <div class="hero-cta">
                <a class="cta-primary" href="{wa(hero_msg)}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp enquiry</a>
                <a class="cta-secondary" href="../event-packages.html">View packages</a>
            </div>
            <p class="hero-usp"><span>{esc(area['usp'])}</span></p>
        </div>
    </section>'''
    start = page.index('<div class="hero-content">', page.index('<section class="hero-options">'))
    end = page.index("</section>", start) + len("</section>")
    page = page[:start] + hero + page[end:]

    # ----- breadcrumb
    page = re.sub(r'(<li class="breadcrumb-item breadcrumb-current" aria-current="page">)[^<]*(</li>)',
                  lambda m: m.group(1) + esc(area["h1"]) + m.group(2), page, count=1)

    # ----- main content
    block = "<!-- LOC:START -->\n        " + region(area) + "\n        <!-- LOC:END -->"
    if "<!-- LOC:START -->" in page:
        page = re.sub(r"<!-- LOC:START -->.*?<!-- LOC:END -->", lambda m: block, page, flags=re.S)
    else:
        crumb = page.index('<nav aria-label="Breadcrumb"')
        after = page.index("</nav>", crumb) + len("</nav>")
        main_end = page.index("\n    </main>")
        page = page[:after] + "\n\n    " + block + "\n" + page[main_end:]

    # ----- schema
    page = set_schema(page, {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "GPL Events & Hire",
        "description": f"Event styling packages, décor hire and bespoke gifting serving {area['name']} from our base in Midrand, Gauteng.",
        "url": SITE,
        "telephone": "+27649318467",
        "email": "gpleventsandhire@gmail.com",
        "logo": "https://res.cloudinary.com/dp24kap9x/image/upload/f_auto,q_auto,w_1000/v1759653499/variation-01_nfpohg.png",
        "address": {"@type": "PostalAddress", "addressLocality": "Midrand", "addressRegion": "Gauteng",
                    "postalCode": "1685", "addressCountry": "ZA"},
        "areaServed": [{"@type": "City", "name": area["name"]}] +
                      [{"@type": "City", "name": o["name"]} for o in AREAS if o["slug"] != area["slug"]],
        "sameAs": ["https://share.google/hgqL3xBRj575rXru5"],
    })
    page = set_schema(page, {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": area["h1"], "item": url},
        ],
    })
    page = set_schema(page, {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in area["faqs"]],
    })

    # ----- stylesheet
    if "css/locations.css" not in page:
        page = page.replace('    <link rel="stylesheet" href="../css/hero-option.css">\n',
                            '    <link rel="stylesheet" href="../css/hero-option.css">\n    <link rel="stylesheet" href="../css/locations.css">\n', 1)
    assert "css/locations.css" in page and page.rstrip().endswith("</html>"), path
    open(path, "w", encoding="utf-8").write(page)
    print("built", "locations/" + area["slug"] + ".html")


for a in AREAS:
    assert len(a["title"]) <= 60, (a["slug"], len(a["title"]))
    assert len(a["description"]) <= 155, (a["slug"], len(a["description"]))
    build(a)
