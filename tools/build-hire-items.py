"""Build hire-items.json (used by the search box on hire.html).

Reads every visible category tile on hire.html, then every visible
.hire-item-card on that category page. Hidden tiles/cards
(style="display:none") are skipped, so re-run this after hiding,
un-hiding, adding or re-pricing an item:

    python3 tools/build-hire-items.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split()


def clean(fragment):
    return " ".join(text(fragment))


def main():
    hub = open(os.path.join(ROOT, "hire.html"), encoding="utf-8").read()
    items = []
    tiles = re.finditer(
        r'<a class="collection-card" href="(hire/[\w-]+\.html)"( style="display:none")?>(.*?)</a>',
        hub, re.S)
    for tile in tiles:
        if tile.group(2):
            continue
        cat_url = tile.group(1)
        cat_name = clean(re.search(r'collection-card-title">(.*?)</p>', tile.group(3), re.S).group(1))
        page = open(os.path.join(ROOT, cat_url), encoding="utf-8").read()
        cards = re.finditer(
            r'<div class="hire-item-card"( style="display:none")?>(.*?)<a class="cta-secondary"',
            page, re.S)
        for card in cards:
            if card.group(1):
                continue
            body = card.group(2)
            name_html = re.search(r'class="hire-item-name">(.*?)</p>', body, re.S).group(1)
            link = re.search(r'href="/?(hire/items/[\w-]+\.html)"', name_html)
            price = re.search(r'class="hire-item-price[^"]*">(.*?)</p>', body, re.S)
            img = re.search(r'<img[^>]*src="\.\./([^"]+)"', body)
            items.append({
                "name": clean(name_html),
                "category": cat_name,
                "categoryUrl": cat_url,
                "itemUrl": link.group(1) if link else None,
                "price": clean(price.group(1)) if price else "",
                "image": img.group(1) if img else None,
            })
    out = os.path.join(ROOT, "hire-items.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(items)} items to hire-items.json")


if __name__ == "__main__":
    main()
