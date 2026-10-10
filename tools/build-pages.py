"""Build standalone landing pages: year-end-functions.html and our-work.html.

    python3 tools/build-pages.py

Pages are created from contact.html's shell (head, nav, footer) on first run;
after that only the title/meta, <main> content and JSON-LD are rewritten.
Prices come from tools/packages-data.json. Case studies live in WORK below —
add a new dict to WORK for each event you want to show.
"""
import html
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gpleventsandhire.co.za/"
WA = "https://wa.me/27649318467?text="
CL = "https://res.cloudinary.com/dp24kap9x/image/upload/"
PACKAGES = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "tools", "packages-data.json"), encoding="utf-8"))["events"]["categories"]}
GIFTS = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "tools", "packages-data.json"), encoding="utf-8"))["gifting"]["categories"]}


def esc(text):
    return html.escape(text, quote=True)


def wa(message):
    return WA + urllib.parse.quote(message, safe="")


def img(pid, transform):
    return CL + transform + "/" + pid + ".jpg"


EQUINIX = {
    "id": "equinix-jno",
    "client": "Equinix",
    "title": "Equinix JNO office opening",
    "place": "Johannesburg",
    "date": "2026",
    "summary": ("For the grand opening of Equinix's JNO office in Johannesburg, we styled the arrival, ribbon-cutting "
                "and welcome-drinks areas in the brand's colours — a polished first impression for staff, partners and guests."),
    "styled": [
        "A “Welcome to JNO” arch-top welcome board on a white plinth, finished with florals",
        "A VIP ribbon-cutting entrance with gold stanchions",
        "Light-up JNO marquee letters with a green, gold and yellow balloon garland",
        "A branded champagne wall beside the badge drop station",
        "Branded black-and-white balloon columns",
    ],
    "items": [
        ["Champagne wall", "hire/items/champagne-wall.html"],
        ["Marquee letters", "hire/items/marquee-letters-az.html"],
        ["Gold stanchion rope sets", "hire/items/stanchion-rope-set.html"],
        ["Welcome boards", "hire/welcome-board-stands.html"],
        ["Corporate packages", "event-packages.html#corporate"],
    ],
    # [cloudinary id, width, height, alt, caption]
    "photos": [
        ["v1791606018/JNO5_ppe7f3", 3, 2, "Light-up JNO marquee letters with a green, gold and yellow balloon garland", "JNO marquee letters & balloon garland"],
        ["v1791606060/JNO7_wldcfj", 2, 3, "Welcome to JNO arch-top welcome board with florals", "Branded welcome board"],
        ["v1791606018/JNO1_fwougk", 3, 2, "Equinix JNO 2026 grand opening ribbon between gold stanchions", "Ribbon-cutting entrance"],
        ["v1791606019/JNO6_zeqpbi", 4, 5, "Branded champagne wall beside the badge drop station", "Branded champagne wall"],
        ["v1791606018/JNO2_awykmc", 5, 3, "Champagne glasses lined up under the Equinix JNO sign", "Welcome drinks"],
        ["v1791606018/JNO3_bkwtzo", 2, 3, "Champagne being poured into glasses on the champagne wall", "Champagne service"],
        ["v1791606019/JNO4_izox7k", 1, 2, "Branded Equinix JNO balloon column in black and white", "Branded balloon column"],
    ],
}
WORK = [EQUINIX]

# Older portfolio photos (also on the homepage)
OTHER = [
    ["assets/Untitled-2-01-800.webp", 800, 538, "Pink and red balloon backdrop with heart balloons for a campus carnival", "Balloon backdrop", "Campus carnival"],
    ["assets/Untitled-2-02-800.webp", 800, 538, "Blue, white and silver balloon arch framing a custom welcome sign at a corporate event", "Balloon arch & signage", "Corporate event"],
    [img("v1779356961/Untitled-2_cggq8l", "f_auto,q_auto,w_900"), 900, 605, "Festive dinner table styled with red candles, a greenery centrepiece and gold-rim plates", "Table styling", "Festive dinner"],
    ["assets/correx-800.jpg", 800, 800, "Custom printed welcome board for an 18th birthday celebration", "Custom welcome board", "18th birthday"],
    ["assets/correx2-800.jpg", 800, 800, "Greenery welcome board for an educators’ luncheon", "Welcome board", "Educators’ luncheon"],
    ["assets/welcome-board-800.jpeg", 800, 800, "Floral welcome flower box at an event entrance", "Welcome flower box", "Event entrance"],
]


# ---------------------------------------------------------------- helpers

def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n" + "\n".join("    " + line for line in text.split("\n")) + "\n    "


def set_schema(page, obj):
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', page, re.S):
        if json.loads(m.group(2)).get("@type") == obj["@type"]:
            return page[:m.start(2)] + dump(obj) + page[m.end(2):]
    return page.replace("</head>", '    <script type="application/ld+json">' + dump(obj) + "</script>\n</head>", 1)


def shell(path, extra_css, extra_js):
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    page = open(os.path.join(ROOT, "contact.html"), encoding="utf-8").read()
    page = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
    page = re.sub(r"<a href='#contactus' aria-current=\"page\"\s+title=\"Contact us for a quote\">Contact</a>",
                  "<a href='contact.html' title=\"Contact us for a quote\">Contact</a>", page)
    links = "".join(f'    <link rel="stylesheet" href="css/{c}">\n' for c in extra_css)
    page = page.replace('    <link rel="stylesheet" href="css/hero-option.css">\n',
                        '    <link rel="stylesheet" href="css/hero-option.css">\n' + links, 1)
    scripts = "".join(f'    <script src="./scripts/{j}" defer></script>\n' for j in extra_js)
    page = page.replace('    <script src="./scripts/backtotop.js" defer></script>\n',
                        '    <script src="./scripts/backtotop.js" defer></script>\n' + scripts, 1)
    return page


def set_head(page, url, title, desc, keywords):
    assert len(title) <= 60 and len(desc) <= 155, (title, len(title), len(desc))
    page = re.sub(r"<title>.*?</title>", "<title>" + title + "</title>", page, count=1)
    for attr in ('name="title"', 'property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r' content=")[^"]*', lambda m: m.group(1) + esc(title), page)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'(<meta ' + re.escape(attr) + r'\s+content=")[^"]*', lambda m: m.group(1) + esc(desc), page, flags=re.S)
    page = re.sub(r'(<meta name="keywords"\s+content=")[^"]*', lambda m: m.group(1) + esc(keywords), page, flags=re.S)
    page = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, page)
    page = re.sub(r'(<meta (?:property="og:url"|name="twitter:url") content=")[^"]*', lambda m: m.group(1) + url, page)
    og = img("v1791606018/JNO5_ppe7f3", "f_auto,q_auto,c_fill,g_auto,w_1200,h_630")
    page = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*', lambda m: m.group(1) + og, page)
    return page


HERO_URL = CL + "f_auto,q_auto:eco,w_{w}/v1759646924/IMG_3259_mysmrz.jpg"
HERO_IMG = ('<img class="hero-photo" src="' + HERO_URL.format(w=900) + '"\n            srcset="' +
            ", ".join(f"{HERO_URL.format(w=w)} {w}w" for w in (640, 900, 1400, 1920)) +
            '"\n            sizes="(max-width: 768px) 340px, 100vw" width="1920" height="1440" fetchpriority="high" alt="">')


def hero(h1, sub, primary, secondary):
    return f'''
    <section class="hero-options">
        {HERO_IMG}
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="hero-title">{esc(h1)}</h1>
            <p class="hero-subtitle">{esc(sub)}</p>
            <div class="hero-cta">
                <a class="cta-primary" href="{primary[1]}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> {esc(primary[0])}</a>
                <a class="cta-secondary" href="{secondary[1]}">{esc(secondary[0])}</a>
            </div>
        </div>
    </section>

    <nav aria-label="Breadcrumb" class="breadcrumb-nav">
        <div class="container">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item breadcrumb-current" aria-current="page">{esc(h1)}</li>
            </ol>
        </div>
    </nav>
'''


def faq_block(title, rows):
    items = "".join(f'''
                <details class="faq-item">
                    <summary class="faq-question">{esc(q)}</summary>
                    <p class="faq-answer">{esc(a)}</p>
                </details>''' for q, a in rows)
    return f'''
            <section class="faq-section loc-faq">
                <div class="container">
                    <div class="section-header">
                        <h2 class="title">{esc(title)}</h2>
                    </div>
                    <div class="faq-list">{items}
                    </div>
                </div>
            </section>'''


def finish(path, page, main, url, crumb, schemas):
    page = re.sub(r'<main id="main">.*?</main>', lambda m: '<main id="main">\n    <!-- PAGE:START -->' + main + '\n    <!-- PAGE:END -->\n    </main>',
                  page, count=1, flags=re.S)
    page = set_schema(page, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    for s in schemas:
        page = set_schema(page, s)
    assert page.rstrip().endswith("</html>")
    open(path, "w", encoding="utf-8").write(page)
    print("built", os.path.relpath(path, ROOT))


def gallery_figs(photos, event, transform="f_auto,q_auto,w_1200"):
    out = ""
    for pid, rw, rh, alt, cap in photos:
        w = 1200
        h = round(w * rh / rw)
        out += f'''
                <figure class="pf-item">
                    <button type="button" class="pf-open" aria-label="View larger: {esc(cap)}">
                        <img src="{img(pid, "f_auto,q_auto,w_900")}" srcset="{img(pid, "f_auto,q_auto,w_600")} 600w, {img(pid, "f_auto,q_auto,w_900")} 900w, {img(pid, "f_auto,q_auto,w_1200")} 1200w" sizes="(max-width: 640px) 50vw, 33vw" width="{w}" height="{h}" loading="lazy" alt="{esc(alt)}">
                    </button>
                    <figcaption><span class="pf-tag">{esc(cap)}</span><span class="pf-event">{esc(event)}</span></figcaption>
                </figure>'''
    return out


LIGHTBOX = '''
        <dialog class="pf-lightbox" aria-label="Photo">
            <button type="button" class="pf-lb-close" aria-label="Close">&times;</button>
            <button type="button" class="pf-lb-prev" aria-label="Previous photo">&#8249;</button>
            <figure>
                <img src="" alt="">
                <figcaption></figcaption>
            </figure>
            <button type="button" class="pf-lb-next" aria-label="Next photo">&#8250;</button>
        </dialog>'''


# ---------------------------------------------------------------- year-end functions

YE_FAQS = [
    ["How early should I book our year-end function décor?",
     "As early as possible — November and December book up fast. Your date is secured with a 70% deposit, and the balance is due a week before your function."],
    ["How much does year-end function décor cost?",
     "Our corporate packages start from R5,000 (Essential), with Signature from R10,000 and Luxe from R20,000. Delivery and collection are charged separately — usually around R1,600 for most Gauteng venues."],
    ["Can you brand the décor with our company logo or colours?",
     "Yes — every corporate package includes a branded welcome board, we can style balloons in your brand colours, and the Luxe package adds your initials or logo letters in marquee lights."],
    ["Do you set up at hotels, offices and function venues?",
     "Yes — setup is included in every event package. Tell us your venue's access and setup window when you book, and we'll schedule our team around it."],
    ["Can we add year-end gifts for staff or clients?",
     "Yes — our corporate gifts start from R1,500 with no minimum order, logo branding and bulk-order discounts. Gift delivery is free in Midrand, Waterfall, Carlswald, Kyalami and Fourways, and R150 elsewhere in Gauteng."],
    ["Which areas do you cover for year-end functions?",
     "We're based in Midrand and style year-end functions across Johannesburg, Sandton, Midrand, Centurion, Waterfall, Fourways, Kyalami and Carlswald."],
    ["How do we pay?",
     "By EFT — a 70% deposit secures your date and the balance is due a week before your function."],
]


def year_end():
    path = os.path.join(ROOT, "year-end-functions.html")
    url = SITE + "year-end-functions.html"
    page = shell(path, ["collections.css", "locations.css", "testimonial.css"], [])
    page = set_head(page, url,
                    "Year-End Function Décor in Johannesburg | GPL Events & Hire",
                    "Year-end function décor in Johannesburg, Sandton & Midrand — corporate packages from R5,000, branded décor, red carpets and staff gifts. Book early.",
                    "year-end function décor Johannesburg, year end function Sandton, corporate year-end party décor, year-end function Midrand, corporate event styling Gauteng")
    corp = PACKAGES["corporate"]
    msg_book = "Hi GPL Events, I'd like to book décor for our year-end function. Our date is: "
    cards = ""
    for t in corp["tiers"]:
        inc = "".join(f"\n                                <li>{esc(i)}</li>" for i in t["includes"])
        plus = f'\n                            <p class="loc-meta">{esc(t["plus"])}</p>' if t.get("plus") else ""
        cards += f'''
                    <article class="loc-card{' ye-popular' if t['tier'] == 'Signature' else ''}">
                        <p class="ye-tier">{esc(t['tier'])}{' · Most popular' if t['tier'] == 'Signature' else ''}</p>
                        <h3>{esc(t['name'])}</h3>
                        <p class="loc-price"><span>From</span> {esc(t['price'])}</p>
                        <p class="loc-meta">{esc(t['guests'])} · setup included</p>{plus}
                        <ul class="ye-list">{inc}
                        </ul>
                        <div class="loc-card-actions">
                            <a class="loc-btn loc-btn-wa" href="{wa(f"Hi GPL Events, I'm interested in the {t['name']} package ({'from ' + t['price']}) for our year-end function. Our date is: ")}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Request this package</a>
                        </div>
                    </article>'''
    work = "".join(
        f'\n                    <figure><img src="{img(p[0], "f_auto,q_auto,c_fill,g_auto,w_900,h_675")}" width="900" height="675" loading="lazy" alt="{esc(p[3])} at the Equinix office opening"></figure>'
        for p in EQUINIX["photos"][:4])
    addons = [["Red carpet", "hire/items/red-carpet.html"], ["Gold stanchions", "hire/items/stanchion-rope-set.html"],
              ["Marquee letters", "hire/items/marquee-letters-az.html"], ["Marquee numbers (e.g. 2026)", "hire/items/marquee-numbers.html"],
              ["Champagne wall", "hire/items/champagne-wall.html"], ["Photo backdrops", "hire/backdrops.html"],
              ["Branded welcome boards", "hire/items/correx-welcome-board.html"], ["Crockery & glassware", "hire/crockery.html"],
              ["Audio guestbook", "hire/items/retro-telephone-guestbook.html"]]
    chips = "".join(f'\n                    <li><a href="{u}">{esc(n)}</a></li>' for n, u in addons)
    gift_from = GIFTS["corporate-gifts"]["tiers"][0]["price"]
    steps = [["Enquire early", "WhatsApp us your date, venue and guest count — ideally in October or early November."],
             ["Get your quote", "We confirm your package, branding, add-ons and delivery fee."],
             ["Secure your date", "Pay a 70% deposit by EFT; the balance is due a week before."],
             ["We set up", "Our team styles your venue before guests arrive, then collects afterwards."]]
    step_html = "".join(f'\n                    <li><span class="item-step-num">{i}</span><strong>{esc(a)}</strong><span>{esc(b)}</span></li>'
                        for i, (a, b) in enumerate(steps, 1))
    areas = [["Johannesburg", "johannesburg"], ["Sandton", "sandton"], ["Midrand", "midrand"], ["Centurion", "centurion"],
             ["Waterfall", "waterfall"], ["Fourways", "fourways"], ["Kyalami", "kyalami"], ["Carlswald", "carlswald"]]
    area_chips = "".join(f'\n                    <li><a href="locations/{s}.html">{n}</a></li>' for n, s in areas)
    main = hero("Year-End Function Décor & Styling",
                "Branded, polished year-end functions for teams and clients across Johannesburg, Sandton, Midrand and Centurion — with setup included in every package.",
                ("Book your year-end date", wa(msg_book)), ("See packages", "#packages")) + f'''
    <div class="loc-page">

            <p class="ye-urgent"><i class="fas fa-calendar-check" aria-hidden="true"></i> December dates book up fast — a 70% deposit secures yours.</p>

            <section class="loc-intro" aria-labelledby="ye-intro">
                <h2 class="title" id="ye-intro">Year-end functions, styled for your brand</h2>
                <p>Celebrate your team and thank your clients with a function that looks the part. We design and style year-end
                    parties, award evenings and client functions with branded welcome boards, VIP red carpet entrances,
                    light-up marquee letters, champagne walls and table styling — and our team sets it all up on the day.</p>
                <ul class="loc-facts">
                    <li><i class="fas fa-wand-magic-sparkles" aria-hidden="true"></i><span>Setup included in every package</span></li>
                    <li><i class="fas fa-tag" aria-hidden="true"></i><span>Corporate packages from {esc(corp['tiers'][0]['price'])}</span></li>
                    <li><i class="fas fa-calendar-check" aria-hidden="true"></i><span>70% deposit secures your date</span></li>
                    <li><i class="fas fa-truck" aria-hidden="true"></i><span>Delivery &amp; collection usually around R1,600</span></li>
                </ul>
            </section>

            <section class="loc-packages" id="packages" aria-labelledby="ye-pkg">
                <h2 class="title" id="ye-pkg">Year-end function packages</h2>
                <p class="subtitle">Three tiers to suit your team size and budget — every package can be tailored to your brand.</p>
                <div class="loc-cards">{cards}
                </div>
                <p class="loc-more"><a href="event-packages.html#corporate">Compare all corporate packages →</a></p>
            </section>

            <section class="loc-work" aria-labelledby="ye-work">
                <h2 class="title" id="ye-work">Recent corporate work: Equinix office opening</h2>
                <p class="subtitle">Branded welcome board, VIP ribbon-cutting entrance, JNO marquee letters with a balloon garland in the brand colours, and a branded champagne wall.</p>
                <div class="loc-work-grid">{work}
                </div>
                <p class="loc-more"><a href="our-work.html#equinix-jno">See the full Equinix case study →</a></p>
            </section>

            <section class="loc-hire" aria-labelledby="ye-addons">
                <h2 class="title" id="ye-addons">Popular year-end add-ons</h2>
                <p class="subtitle">Add these to any package, or hire them on their own.</p>
                <ul class="loc-chips">{chips}
                </ul>
            </section>

            <section class="loc-gifting">
                <i class="fas fa-gift" aria-hidden="true"></i>
                <div>
                    <h2>Year-end gifts for staff &amp; clients</h2>
                    <p>Corporate gifts from {esc(gift_from)} — no minimum order, logo branding on packaging, ribbon and cards, and bulk-order discounts.</p>
                </div>
                <a class="loc-btn loc-btn-outline" href="bespoke-gifting.html#corporate-gifting">Corporate gifting</a>
            </section>

            <section class="ye-steps" aria-labelledby="ye-steps">
                <h2 class="title" id="ye-steps">How to book your year-end function</h2>
                <ol class="item-steps">{step_html}
                </ol>
            </section>
{faq_block("Year-End Function FAQs", YE_FAQS)}

            <section class="loc-nearby" aria-labelledby="ye-areas">
                <h2 id="ye-areas">Year-end function décor across Gauteng</h2>
                <ul class="loc-chips">{area_chips}
                </ul>
            </section>
    </div>'''
    offers = [{"@type": "Offer", "name": t["name"], "priceCurrency": "ZAR",
               "priceSpecification": {"@type": "PriceSpecification", "minPrice": int(re.sub(r"\D", "", t["price"])), "priceCurrency": "ZAR"}}
              for t in corp["tiers"]]
    finish(path, page, main, url, "Year-End Function Décor & Styling", [
        {"@context": "https://schema.org", "@type": "Service", "name": "Year-end function décor and styling",
         "serviceType": "Corporate event styling", "url": url,
         "provider": {"@type": "LocalBusiness", "name": "GPL Events & Hire", "telephone": "+27649318467",
                      "address": {"@type": "PostalAddress", "addressLocality": "Midrand", "addressRegion": "Gauteng", "postalCode": "1685", "addressCountry": "ZA"}},
         "areaServed": [{"@type": "City", "name": n} for n, _ in areas],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Year-end function packages", "itemListElement": offers}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in YE_FAQS]},
    ])


# ---------------------------------------------------------------- our work

def our_work():
    path = os.path.join(ROOT, "our-work.html")
    url = SITE + "our-work.html"
    page = shell(path, ["collections.css", "locations.css", "testimonial.css"], ["portfolio-reviews.js"])
    page = set_head(page, url, "Our Work — Event Styling Portfolio | GPL Events & Hire",
                    "Real events styled by GPL Events & Hire — from the Equinix office opening in Johannesburg to weddings, birthdays and celebrations across Gauteng.",
                    "event styling portfolio Gauteng, corporate event décor Johannesburg, Equinix office opening décor, event décor examples Midrand")
    studies = ""
    for w in WORK:
        styled = "".join(f"\n                        <li>{esc(s)}</li>" for s in w["styled"])
        items = "".join(f'\n                        <li><a href="{u}">{esc(n)}</a></li>' for n, u in w["items"])
        studies += f'''
            <article class="work-study" id="{w['id']}" aria-labelledby="{w['id']}-title">
                <p class="eyebrow">{esc(w['client'])} · {esc(w['place'])} · {esc(w['date'])}</p>
                <h2 class="title" id="{w['id']}-title">{esc(w['title'])}</h2>
                <p class="work-summary">{esc(w['summary'])}</p>
                <div class="work-cols">
                    <div>
                        <h3>What we styled</h3>
                        <ul class="ye-list">{styled}
                        </ul>
                    </div>
                    <div>
                        <h3>Items &amp; packages used</h3>
                        <ul class="loc-chips work-items">{items}
                        </ul>
                    </div>
                </div>
                <div class="pf-grid work-gallery" aria-label="{esc(w['title'])} photos">{gallery_figs(w['photos'], w['title'])}
                </div>
            </article>'''
    others = ""
    for src, ww, hh, alt, tag, ev in OTHER:
        others += f'''
                <figure class="pf-item">
                    <button type="button" class="pf-open" aria-label="View larger: {esc(tag)} — {esc(ev)}">
                        <img src="{esc(src)}" width="{ww}" height="{hh}" loading="lazy" alt="{esc(alt)}">
                    </button>
                    <figcaption><span class="pf-tag">{esc(tag)}</span><span class="pf-event">{esc(ev)}</span></figcaption>
                </figure>'''
    main = hero("Our Work", "Real events we've styled across Gauteng — from corporate office openings to weddings, birthdays and celebrations.",
                ("Plan your event", wa("Hi GPL Events, I saw your work and I'd like to plan an event. My date is: ")),
                ("View packages", "event-packages.html")) + f'''
    <div class="loc-page work-page">
{studies}

            <section class="work-more" aria-labelledby="work-more-title">
                <h2 class="title" id="work-more-title">More recent setups</h2>
                <div class="pf-grid">{others}
                </div>
            </section>

            <section class="loc-gifting">
                <i class="fas fa-champagne-glasses" aria-hidden="true"></i>
                <div>
                    <h2>Planning something similar?</h2>
                    <p>Send us your date and venue — we'll suggest a package and confirm availability.</p>
                </div>
                <a class="loc-btn loc-btn-wa" href="{wa("Hi GPL Events, I'd like something similar to your recent work. My date is: ")}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> WhatsApp us</a>
            </section>

            <section class="loc-nearby">
                <h2>Explore</h2>
                <ul class="loc-chips">
                    <li><a href="event-packages.html">Event packages</a></li>
                    <li><a href="year-end-functions.html">Year-end functions</a></li>
                    <li><a href="hire.html">Hire items</a></li>
                    <li><a href="service-areas.html">Areas we serve</a></li>
                </ul>
            </section>
    </div>
{LIGHTBOX}'''
    finish(path, page, main, url, "Our Work", [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Our Work — GPL Events & Hire", "url": url,
         "author": {"@type": "LocalBusiness", "name": "GPL Events & Hire"},
         "hasPart": [{"@type": "CreativeWork", "name": w["title"] + " — " + w["place"], "description": w["summary"],
                      "url": url + "#" + w["id"],
                      "image": [img(p[0], "f_auto,q_auto,w_1200") for p in w["photos"][:3]]} for w in WORK]},
    ])


year_end()
our_work()
