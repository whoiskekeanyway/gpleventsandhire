"""Build the package cards, FAQs and schema on event-packages.html and
bespoke-gifting.html from tools/packages-data.json.

    python3 tools/build-packages.py

Only the parts between the <!-- PKG:START --> / <!-- PKG:END --> and
<!-- FAQ:START --> / <!-- FAQ:END --> markers are rewritten, plus the
FAQPage and OfferCatalog JSON-LD in <head>. Everything else on the page
(hero, nav, footer) is left alone.
"""
import html
import json
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "tools", "packages-data.json"), encoding="utf-8"))
SITE = "https://www.gpleventsandhire.co.za/"
WA = "https://wa.me/27649318467?text="


def esc(text):
    return html.escape(text, quote=True)


def wa_link(message):
    return WA + urllib.parse.quote(message, safe="")


def price_label(price):
    return price if not price.startswith("R") else "from " + price


def card(cat, t, kind):
    popular = t["tier"] == "Signature"
    if t.get("photo"):
        media = f'<img src="{esc(t["photo"])}" width="1200" height="900" loading="lazy" alt="{esc(t["name"])} by GPL Events &amp; Hire">'
    else:
        media = ('<div class="pkg-placeholder" aria-hidden="true">'
                 '<i class="fas fa-camera"></i><span>Photo coming soon</span></div>')
    if kind == "events":
        msg = f"Hi GPL Events, I'm interested in the {t['name']} package ({price_label(t['price'])}). My event date is: "
        cta = "Request this package"
    else:
        msg = f"Hi GPL Events, I'd like to order the {t['name']} ({price_label(t['price'])})."
        cta = "Order on WhatsApp"
    price_html = (f'<span class="pkg-from">From</span> {esc(t["price"])}'
                  if t["price"].startswith("R") else esc(t["price"]))
    guests = (f'\n                            <p class="pkg-guests"><i class="fas fa-users" aria-hidden="true"></i> {esc(t["guests"])}</p>'
              if t.get("guests") else "")
    plus = f'\n                            <p class="pkg-plus">{esc(t["plus"])}</p>' if t.get("plus") else ""
    items = "".join(f'\n                                <li>{esc(i)}</li>' for i in t["includes"])
    badge = '\n                            <span class="pkg-badge">Most popular</span>' if popular else ""
    data = f' data-guests-max="{t["guestsMax"]}"' if t.get("guestsMax") else ""
    return f'''
                    <article class="pkg-card{' is-popular' if popular else ''}" data-tier="{t['tier']}"{data}>
                        <div class="pkg-media">
                            {media}
                            <span class="pkg-tier">{t['tier']}</span>{badge}
                        </div>
                        <div class="pkg-body">
                            <h4 class="pkg-name">{esc(t['name'])}</h4>
                            <p class="pkg-price">{price_html}</p>{guests}
                            <p class="pkg-desc">{esc(t['desc'])}</p>{plus}
                            <ul class="pkg-list">{items}
                            </ul>
                            <a class="pkg-cta" href="{wa_link(msg)}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> {cta}</a>
                        </div>
                    </article>'''


def facts(rows):
    lis = "".join(f'\n                <li><i class="fas {icon}" aria-hidden="true"></i><span>{esc(text)}</span></li>' for icon, text in rows)
    return f'\n            <ul class="pkg-facts">{lis}\n            </ul>'


def tabs(categories, label):
    btns = "".join(
        f'\n                <a class="pkg-tab" href="#{c["id"]}" data-tab="{c["id"]}">{esc(c["tab"])}</a>' for c in categories)
    return f'\n            <nav class="pkg-tabs" aria-label="{label}">{btns}\n            </nav>'


def categories(cats, kind, note):
    out = ""
    for c in cats:
        cards = "".join(card(c, t, kind) for t in c["tiers"])
        out += f'''
            <section class="pkg-category" id="{c['id']}" aria-labelledby="{c['id']}-title">
                <div class="pkg-cat-head">
                    <h3 id="{c['id']}-title">{esc(c['title'])}</h3>
                    <p>{esc(c['intro'])}</p>
                </div>
                <div class="pkg-cards">{cards}
                </div>
                <p class="pkg-swipe-hint" aria-hidden="true">Swipe to compare →</p>
            </section>'''
    return out + f'\n            <p class="pkg-note">{note}</p>'


def steps(rows, title):
    lis = "".join(
        f'\n                    <li><span class="pkg-step-num">{i}</span><strong>{esc(a)}</strong><span>{esc(b)}</span></li>'
        for i, (a, b) in enumerate(rows, 1))
    return f'''
            <section class="pkg-steps" aria-labelledby="steps-title">
                <h3 id="steps-title">{title}</h3>
                <ol>{lis}
                </ol>
            </section>'''


def events_block():
    d = DATA["events"]
    addons = "".join(f'\n                    <li><a href="{esc(url)}">{esc(name)}</a></li>' for name, url in d["addons"])
    cat_opts = "".join(f'\n                            <option value="{c["id"]}">{esc(c["tab"])}</option>' for c in d["categories"])
    return f'''<div class="pkg-page" id="packages">
            <div class="section-header">
                <p class="eyebrow">Event packages</p>
                <h2 class="title">Choose Your Package</h2>
                <p class="subtitle">Three tiers for every occasion — pick a starting point and we'll tailor it to your theme.</p>
            </div>{facts(d["facts"])}{tabs(d["categories"], "Package categories")}
{categories(d["categories"], "events", "Prices are starting points — your final quote depends on your theme, guest count and venue. Delivery &amp; collection are charged separately.")}
{steps(d["steps"], "How booking works")}

            <section class="pkg-addons" aria-labelledby="addons-title">
                <h3 id="addons-title">Popular add-ons</h3>
                <p>Make any package your own with extras from our hire collection.</p>
                <ul>{addons}
                </ul>
            </section>

            <section class="pkg-chooser" id="help-choose" aria-labelledby="chooser-title">
                <h3 id="chooser-title">Not sure which package?</h3>
                <p>Answer two quick questions and we'll point you to the best fit.</p>
                <form class="pkg-chooser-form" novalidate>
                    <div class="form-group">
                        <label for="chooser-event">What are you celebrating?</label>
                        <select id="chooser-event" name="event">{cat_opts}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="chooser-guests">How many guests?</label>
                        <select id="chooser-guests" name="guests">
                            <option value="20">Up to 20</option>
                            <option value="50">21–50</option>
                            <option value="80">51–80</option>
                            <option value="100">81–100</option>
                            <option value="150">101–150</option>
                            <option value="200">More than 150</option>
                        </select>
                    </div>
                    <button type="submit" class="pkg-chooser-btn">Show my package</button>
                </form>
                <div class="pkg-chooser-result" aria-live="polite" hidden></div>
            </section>

            <div class="pkg-crosssell">
                <a class="pkg-cross-card" href="hire.html">
                    <i class="fas fa-couch" aria-hidden="true"></i>
                    <strong>Need individual décor items?</strong>
                    <span>Build your own setup from our hire collection →</span>
                </a>
                <a class="pkg-cross-card" href="bespoke-gifting.html">
                    <i class="fas fa-gift" aria-hidden="true"></i>
                    <strong>Add bespoke gifting</strong>
                    <span>Favours, hampers and flowers for your guests →</span>
                </a>
            </div>
        </div>'''


def gifting_block():
    d = DATA["gifting"]
    return f'''<div class="pkg-page" id="packages">
            <div class="section-header">
                <p class="eyebrow">Gift packages</p>
                <h2 class="title">Choose Your Gift</h2>
                <p class="subtitle">Curated hampers and fresh bouquets in three tiers — every gift can be personalised.</p>
            </div>{facts(d["facts"])}{tabs(d["categories"], "Gift categories")}
{categories(d["categories"], "gifting", "Prices are starting points — every hamper can be customised to your budget. Delivery is free in Midrand, Waterfall, Carlswald, Kyalami &amp; Fourways and R150 elsewhere in Gauteng.")}
{steps(d["steps"], "How ordering works")}

            <section class="pkg-custom" aria-labelledby="custom-title">
                <div>
                    <h3 id="custom-title">Build your own hamper</h3>
                    <p>Have something specific in mind? Tell us who it's for, your budget and their favourite things — we'll curate it for you.</p>
                </div>
                <a class="pkg-cta" href="{wa_link("Hi GPL Events, I'd like a custom gift hamper. It's for: ... My budget is: ...")}" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Start a custom order</a>
            </section>

            <section class="pkg-corporate" id="corporate-gifting" aria-labelledby="corp-title">
                <div class="pkg-corp-info">
                    <p class="eyebrow">Corporate gifting</p>
                    <h3 id="corp-title">Gifts for clients &amp; teams</h3>
                    <ul>
                        <li><i class="fas fa-check" aria-hidden="true"></i> No minimum order</li>
                        <li><i class="fas fa-check" aria-hidden="true"></i> Logo branding on packaging, ribbon &amp; cards</li>
                        <li><i class="fas fa-check" aria-hidden="true"></i> Bulk-order discounts</li>
                        <li><i class="fas fa-check" aria-hidden="true"></i> Delivery across Gauteng</li>
                    </ul>
                </div>
                <form class="pkg-form" name="corporate-gifting" method="POST" data-netlify="true" netlify-honeypot="bot-field">
                    <input type="hidden" name="form-name" value="corporate-gifting">
                    <p class="form-honeypot" aria-hidden="true"><label>Leave this empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="corp-company">Company <span class="req" aria-hidden="true">*</span></label>
                            <input id="corp-company" name="company" autocomplete="organization" required>
                        </div>
                        <div class="form-group">
                            <label for="corp-name">Your name <span class="req" aria-hidden="true">*</span></label>
                            <input id="corp-name" name="name" autocomplete="name" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="corp-email">Email <span class="req" aria-hidden="true">*</span></label>
                            <input id="corp-email" type="email" name="email" autocomplete="email" required>
                        </div>
                        <div class="form-group">
                            <label for="corp-phone">Phone / WhatsApp</label>
                            <input id="corp-phone" type="tel" name="phone" autocomplete="tel" inputmode="tel">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="corp-qty">How many gifts?</label>
                            <input id="corp-qty" type="number" name="quantity" min="1" inputmode="numeric">
                        </div>
                        <div class="form-group">
                            <label for="corp-budget">Budget per gift</label>
                            <input id="corp-budget" name="budget" placeholder="e.g. R500">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="corp-date">Needed by</label>
                        <input id="corp-date" type="date" name="neededBy">
                    </div>
                    <div class="form-group">
                        <label for="corp-message">Branding or other details</label>
                        <textarea id="corp-message" name="message" rows="3"></textarea>
                    </div>
                    <button type="submit" class="form-submit"><i class="fas fa-paper-plane" aria-hidden="true"></i> Request a corporate quote</button>
                </form>
            </section>

            <div class="pkg-crosssell">
                <a class="pkg-cross-card" href="event-packages.html">
                    <i class="fas fa-champagne-glasses" aria-hidden="true"></i>
                    <strong>Planning an event too?</strong>
                    <span>See our styled event packages →</span>
                </a>
                <a class="pkg-cross-card" href="hire.html">
                    <i class="fas fa-couch" aria-hidden="true"></i>
                    <strong>Décor hire</strong>
                    <span>Arches, backdrops, marquee letters and more →</span>
                </a>
            </div>
        </div>'''


def faq_items(rows):
    return "".join(f'''
                <details class="faq-item">
                    <summary class="faq-question">{esc(q)}</summary>
                    <p class="faq-answer">{esc(a)}</p>
                </details>''' for q, a in rows)


def dump(obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n" + "\n".join("    " + line for line in text.split("\n")) + "\n    "


def set_schema(page, obj, marker_type):
    """Replace the JSON-LD block whose @type is marker_type, or add it before </head>."""
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', page, re.S):
        if json.loads(m.group(2)).get("@type") == marker_type:
            return page[:m.start(2)] + dump(obj) + page[m.end(2):]
    return page.replace("</head>", '    <script type="application/ld+json">' + dump(obj) + "</script>\n</head>", 1)


def offer_catalog(name, url, cats):
    offers = []
    for c in cats:
        for t in c["tiers"]:
            offer = {"@type": "Offer", "name": t["name"], "priceCurrency": "ZAR"}
            if t["price"].startswith("R"):
                offer["priceSpecification"] = {"@type": "PriceSpecification", "minPrice": int(re.sub(r"\D", "", t["price"])), "priceCurrency": "ZAR"}
            offers.append(offer)
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "url": url,
        "provider": {"@type": "LocalBusiness", "name": "GPL Events & Hire"},
        "areaServed": "Gauteng",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": name, "itemListElement": offers},
    }


def build(path, block, faqs, catalog):
    full = os.path.join(ROOT, path)
    page = open(full, encoding="utf-8").read()
    region = "<!-- PKG:START -->\n        " + block + "\n        <!-- PKG:END -->"
    if "<!-- PKG:START -->" in page:
        page = re.sub(r"<!-- PKG:START -->.*?<!-- PKG:END -->", lambda m: region, page, flags=re.S)
    else:
        start = page.index('<div class="packages-container"')
        end = page.index('    <section class="faq-section">')
        page = page[:start] + region + "\n\n" + page[end:]
    faq_region = "<!-- FAQ:START -->" + faq_items(faqs) + "\n                <!-- FAQ:END -->"
    if "<!-- FAQ:START -->" in page:
        page = re.sub(r"<!-- FAQ:START -->.*?<!-- FAQ:END -->", lambda m: faq_region, page, flags=re.S)
    else:
        faq_at = page.index('<section class="faq-section">')
        list_start = page.index('<div class="faq-list">', faq_at) + len('<div class="faq-list">')
        list_end = page.index("\n            </div>", list_start)
        page = page[:list_start] + "\n                " + faq_region + page[list_end:]
    page = set_schema(page, {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }, "FAQPage")
    page = set_schema(page, catalog, "Service")
    assert page.rstrip().endswith("</html>")
    open(full, "w", encoding="utf-8").write(page)
    print("built", path)


build("event-packages.html", events_block(), DATA["events"]["faqs"],
      offer_catalog("Event styling packages", SITE + "event-packages.html", DATA["events"]["categories"]))
build("bespoke-gifting.html", gifting_block(), DATA["gifting"]["faqs"],
      offer_catalog("Bespoke gift hampers and flower bouquets", SITE + "bespoke-gifting.html", DATA["gifting"]["categories"]))
