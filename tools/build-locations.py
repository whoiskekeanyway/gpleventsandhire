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
SITE = "https://gpleventsandhire.co.za/"
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
    ye = (' &nbsp;·&nbsp; <a href="../year-end-functions.html">Year-end functions →</a>'
          if "corporate" in area["focus"] else "")
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
    work = ""
    if area.get("work"):
        w = area["work"]
        figs = "".join(
            f'\n                    <figure><img src="{esc(src)}" width="900" height="675" loading="lazy" alt="{esc(alt)}"></figure>'
            for src, alt in w["photos"])
        work = f'''

            <section class="loc-work" aria-labelledby="loc-work-title">
                <h2 class="title" id="loc-work-title">{esc(w['title'])}</h2>
                <p class="subtitle">{esc(w['text'])}</p>
                <div class="loc-work-grid">{figs}
                </div>
                <p class="loc-more"><a href="../event-packages.html#corporate">See our corporate packages →</a></p>
            </section>'''
    return f'''<div class="loc-page">

            <section class="loc-intro" aria-labelledby="loc-intro-title">
                <h2 class="title" id="loc-intro-title">Events in {name}</h2>{paras}
                <ul class="loc-facts">{facts_html}
                </ul>
            </section>

{work}

            <section class="loc-packages" aria-labelledby="loc-pkg-title">
                <h2 class="title" id="loc-pkg-title">Popular packages in {name}</h2>
                <p class="subtitle">Three tiers for every occasion — pick a starting point and we'll tailor it to your theme.</p>
                <div class="loc-cards">{cards}
                </div>
                <p class="loc-more"><a href="../event-packages.html">See all event packages →</a>{ye}</p>
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
    page = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, page)
    page = re.sub(r'(<meta (?:property="og:url"|name="twitter:url") content=")[^"]*', lambda m: m.group(1) + url, page)

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
    # All styles come from the bundle (tools/build-css.py)
    assert "css/site.css" in page and page.rstrip().endswith("</html>"), path
    open(path, "w", encoding="utf-8").write(page)
    print("built", "locations/" + area["slug"] + ".html")


SA_TITLE = "Areas We Serve in Gauteng | GPL Events & Hire"
SA_DESC = ("Event styling, décor hire and bespoke gifts across Midrand, Waterfall, Carlswald, Kyalami, Fourways, "
           "Sandton, Centurion and Johannesburg.")
SA_FAQS = [
    ["Which areas do you serve?", "We're based in Midrand and serve " + ", ".join(a["name"] for a in AREAS[:-1]) +
     " and " + AREAS[-1]["name"] + ". For other parts of Gauteng, send us your venue address and we'll confirm."],
    ["How much is event delivery and collection?", "For event packages, delivery and collection is usually around R1,600 for most Gauteng venues. We confirm the exact amount for your venue in your quote."],
    ["Where is gift delivery free?", "Gift delivery is free in " + FREE_GIFT_AREAS + ", and a R150 flat rate anywhere else in Gauteng."],
    ["Can I collect hire items myself?", "Yes — hire items can be collected from us in Midrand by appointment."],
]


HERO_URL = "https://res.cloudinary.com/dp24kap9x/image/upload/f_auto,q_auto:eco,w_{w}/v1756563796/3162cc56-0c4b-452c-9c8d-5651b155405e_o5l4ko_eu5lsz.webp"
HERO_IMG = ('<img class="hero-photo" src="' + HERO_URL.format(w=900) + '"\n            srcset="' +
            ", ".join(f"{HERO_URL.format(w=w)} {w}w" for w in (640, 900, 1400, 1600)) +
            '"\n            sizes="(max-width: 768px) 340px, 100vw" width="1600" height="1066" fetchpriority="high" alt="">')


def service_areas_main():
    cards = ""
    for a in AREAS:
        badge = ("Free gift delivery" if a["giftDelivery"] == "free" else "R150 gift delivery")
        cards += f'''
                    <a class="sa-card" href="locations/{a['slug']}.html">
                        <span class="sa-name">{esc(a['name'])}</span>
                        <span class="sa-desc">{esc(a['heroSub'])}</span>
                        <span class="sa-badge{' is-free' if a['giftDelivery'] == 'free' else ''}"><i class="fas fa-gift" aria-hidden="true"></i> {badge}</span>
                        <span class="sa-link">Events in {esc(a['name'])} →</span>
                    </a>'''
    faqs = "".join(f'''
                <details class="faq-item">
                    <summary class="faq-question">{esc(q)}</summary>
                    <p class="faq-answer">{esc(a)}</p>
                </details>''' for q, a in SA_FAQS)
    ask = wa("Hi GPL Events, I'm planning an event at this venue/area: ")
    return f'''<main id="main">
    <!-- SA:START -->

    <section class="hero-options">
        {HERO_IMG}
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="hero-title">Areas We Serve</h1>
            <p class="hero-subtitle">From our base in Midrand we style events, deliver décor hire and send bespoke gifts across Gauteng.</p>
            <div class="hero-cta">
                <a class="cta-primary" href="{ask}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Check my area</a>
                <a class="cta-secondary" href="event-packages.html">View packages</a>
            </div>
        </div>
    </section>

    <nav aria-label="Breadcrumb" class="breadcrumb-nav">
        <div class="container">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item breadcrumb-current" aria-current="page">Areas We Serve</li>
            </ol>
        </div>
    </nav>

    <div class="loc-page">
            <section class="loc-intro" aria-labelledby="sa-title">
                <h2 class="title" id="sa-title">Event styling across Gauteng</h2>
                <p>We're based in Midrand, so we're closest to Midrand, Waterfall, Carlswald and Kyalami — and we also travel
                    to Fourways, Sandton, Centurion and greater Johannesburg. Choose your area to see popular packages, hire items
                    and delivery details.</p>
                <ul class="loc-facts">
                    <li><i class="fas fa-location-dot" aria-hidden="true"></i><span>Based in Midrand, Gauteng</span></li>
                    <li><i class="fas fa-wand-magic-sparkles" aria-hidden="true"></i><span>Setup included in every event package</span></li>
                    <li><i class="fas fa-truck" aria-hidden="true"></i><span>Event delivery &amp; collection usually around R1,600</span></li>
                    <li><i class="fas fa-gift" aria-hidden="true"></i><span>Free gift delivery in 5 areas · R150 elsewhere in Gauteng</span></li>
                </ul>
            </section>

            <section class="sa-areas" aria-label="Service areas">
                <div class="sa-grid">{cards}
                </div>
            </section>

            <section class="loc-gifting">
                <i class="fas fa-map-location-dot" aria-hidden="true"></i>
                <div>
                    <h2>Don't see your area?</h2>
                    <p>Send us your venue address on WhatsApp and we'll confirm whether we can accommodate your event.</p>
                </div>
                <a class="loc-btn loc-btn-wa" href="{ask}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Ask us</a>
            </section>

            <section class="faq-section loc-faq">
                <div class="container">
                    <div class="section-header">
                        <h2 class="title">Service Area FAQs</h2>
                        <p class="subtitle">Delivery, collection and coverage</p>
                    </div>
                    <div class="faq-list">{faqs}
                    </div>
                </div>
            </section>
    </div>

    <!-- SA:END -->
    </main>'''


def build_service_areas():
    path = os.path.join(ROOT, "service-areas.html")
    url = SITE + "service-areas.html"
    if os.path.exists(path):
        page = open(path, encoding="utf-8").read()
    else:
        # First run: start from contact.html's shell (head, nav, footer)
        page = open(os.path.join(ROOT, "contact.html"), encoding="utf-8").read()
        page = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
        page = re.sub(r"<a href='#contactus' aria-current=\"page\"\s+title=\"Contact us for a quote\">Contact</a>",
                      "<a href='contact.html' title=\"Contact us for a quote\">Contact</a>", page)
        page = page.replace('    <link rel="stylesheet" href="css/hero-option.css">\n',
                            '    <link rel="stylesheet" href="css/hero-option.css">\n    <link rel="stylesheet" href="css/locations.css">\n', 1)
    page = re.sub(r"<title>.*?</title>", "<title>" + SA_TITLE + "</title>", page, count=1)
    for attr in ('name="title"', 'property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*', lambda m: m.group(1) + esc(SA_TITLE), page)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r'\s+content=")[^"]*', lambda m: m.group(1) + esc(SA_DESC), page, flags=re.S)
    page = re.sub(r'(<meta name="keywords"\s+content=")[^"]*', lambda m: m.group(1) + esc(
        "event planner Gauteng, décor hire Midrand, event décor Sandton, party hire Fourways, event styling Centurion, service areas"), page, flags=re.S)
    page = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, page)
    page = re.sub(r'(<meta (?:property="og:url"|name="twitter:url") content=")[^"]*', lambda m: m.group(1) + url, page)
    page = re.sub(r'<main id="main">.*?</main>', lambda m: service_areas_main(), page, count=1, flags=re.S)
    page = set_schema(page, {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": "GPL Events & Hire",
        "description": "Event styling packages, décor hire and bespoke gifting from Midrand, serving greater Gauteng.",
        "url": SITE, "telephone": "+27649318467", "email": "gpleventsandhire@gmail.com",
        "address": {"@type": "PostalAddress", "addressLocality": "Midrand", "addressRegion": "Gauteng",
                    "postalCode": "1685", "addressCountry": "ZA"},
        "areaServed": [{"@type": "City", "name": a["name"]} for a in AREAS],
        "sameAs": ["https://share.google/hgqL3xBRj575rXru5"],
    })
    page = set_schema(page, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                            {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": url}],
    })
    page = set_schema(page, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in SA_FAQS],
    })
    assert page.rstrip().endswith("</html>")
    open(path, "w", encoding="utf-8").write(page)
    print("built service-areas.html")


for a in AREAS:
    assert len(a["title"]) <= 60, (a["slug"], len(a["title"]))
    assert len(a["description"]) <= 155, (a["slug"], len(a["description"]))
    build(a)
assert len(SA_TITLE) <= 60 and len(SA_DESC) <= 155
build_service_areas()
