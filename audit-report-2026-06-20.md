# GPL Events & Hire — Site Audit Report
**Date:** 2026-06-20

---

## What Was Built This Session

| File                                 | Status                                          |
| ------------------------------------ | ----------------------------------------------- |
| `hire-intent.html`                   | ✅ Created — Collections hub (14 category tiles) |
| `css/collections.css`                | ✅ Created — Styles for hub grid + item cards    |
| `category/accessories.html`          | ✅ Created                                       |
| `category/audio-guestbook-sets.html` | ✅ Created                                       |
| `category/arches.html`               | ✅ Created                                       |
| `category/backdrops.html`            | ✅ Created                                       |
| `category/drinks-boards.html`        | ✅ Created                                       |
| `category/easels.html`               | ✅ Created                                       |
| `category/flower-stands.html`        | ✅ Created                                       |
| `category/furniture.html`            | ✅ Created                                       |
| `category/lawn-games.html`           | ✅ Created                                       |
| `category/plinths.html`              | ✅ Created                                       |
| `category/selfie-mirrors.html`       | ✅ Created                                       |
| `category/signs.html`                | ✅ Created                                       |
| `category/table-decor.html`          | ✅ Created                                       |
| `category/welcome-board-stands.html` | ✅ Created                                       |
| `sitemap.xml`                        | ✅ Updated — 15 new pages added                  |

**Every page includes:**
- Unique `<title>`, `<meta name="description">`, `<link rel="canonical">`
- Open Graph + Twitter card tags
- Breadcrumb JSON-LD schema
- ItemList JSON-LD schema (category pages) / CollectionPage schema (hub)
- 3-level breadcrumb navigation (Home → Hire Collections → Category)
- H1 keyword-targeted to "[Category] Hire in Midrand"
- WhatsApp enquiry links per item with pre-filled messages

---

## Bugs Fixed During Build

### 1. `.cta-secondary` invisible on white cards *(Fixed — `css/collections.css`)*
The hero-level `.cta-secondary` styles (`color: white; border: 2px solid white`) would have made the Enquire button invisible on white `.hire-item-card` backgrounds. Added a specific override:
```css
.hire-item-card a.cta-secondary {
    color: var(--clr-primary-navy);
    border-color: var(--clr-primary-navy);
}
```

### 2. Sitemap missing new pages *(Fixed — `sitemap.xml`)*
`sitemap.xml` had no entries for `hire-intent.html` or any category pages. Added all 15 URLs with `priority: 0.8–0.9` and `changefreq: weekly`.

---

## Bugs Found — Not Yet Fixed

### 3. Broken cross-sell link in `hire.html`
**File:** `hire.html` line 399
**Problem:** `href="packages.html"` — this file does not exist. The correct file is `event-packages.html`.
**Fix:** Change `href="packages.html"` to `href="event-packages.html"`.

### 4. Hero CSS ownership *(Reviewed)*
**Files:** `css/style.css` and `css/hero-option.css`
**Finding:** The shared hero and CTA styles are defined in `style.css`; `hero-option.css` contains the `.hero-options` layout and page-specific spacing. The reported duplicate definitions were not present in the current files.
**Change:** Scoped CTA spacing to `.hero-options` so it no longer applies globally. Keep shared hero styles in `style.css` and sub-page overrides in `hero-option.css`.

### 5. Nav "Hire Items" link not yet updated to `hire-intent.html`
**All pages:** `<a href='hire'>` in nav
**Problem:** Users clicking "Hire Items" land on old `hire.html` not the new collections hub.
**Fix (when ready):** Update `href='hire'` to `href='hire-intent.html'` across all pages, or create a redirect from `/hire` → `/hire-intent.html`.
**Status:** Intentionally deferred — update after confirming new pages look correct.

---

## Content Gaps — Needs Client Input

### 6. All item images are placeholder gradients
Every `.hire-item-img` and `.collection-card-img` is a styled placeholder div with no real photo. When photos are available:
- For collection cards: add `<img>` inside `.collection-card-img`
- For item cards: add `<img>` inside `.hire-item-img`
- All images should use Cloudinary with `f_auto,q_auto` transformation
- All `<img>` tags need descriptive `alt` text
- Use `loading="lazy"` on all below-fold images

### 7. Prices in category pages are estimated
All item prices were approximated based on common market rates. Client must verify and update the following prices in each category page:
- `category/accessories.html` — 3 items
- `category/audio-guestbook-sets.html` — 2 items
- `category/arches.html` — 3 items
- `category/backdrops.html` — 3 items
- `category/drinks-boards.html` — 3 items
- `category/easels.html` — 3 items
- `category/flower-stands.html` — 3 items
- `category/furniture.html` — 4 items
- `category/lawn-games.html` — 3 items
- `category/plinths.html` — 3 items
- `category/selfie-mirrors.html` — 2 items
- `category/signs.html` — 3 items
- `category/table-decor.html` — 3 items
- `category/welcome-board-stands.html` — 4 items

### 8. Item names in category pages are estimated
Item names were based on common hire inventory. Client should verify each item name matches their actual stock and add or remove items per category.

---

## SEO Status

| Check                                    | Status                                      |
| ---------------------------------------- | ------------------------------------------- |
| Unique title per page                    | ✅ All new pages                             |
| Unique meta description per page         | ✅ All new pages                             |
| Canonical URL per page                   | ✅ All new pages                             |
| BreadcrumbList JSON-LD                   | ✅ All new pages                             |
| ItemList/CollectionPage schema           | ✅ All new pages                             |
| robots.txt                               | ✅ Exists, correct                           |
| sitemap.xml updated                      | ✅ Done this session                         |
| Submit updated sitemap to Search Console | ⚠️ Needed — must be done manually            |
| H1 keyword targeting                     | ✅ "[Category] Hire in Midrand" on all pages |
| Local area mentioned in copy             | ✅ Midrand + Gauteng in hero + subtitles     |
| Open Graph tags                          | ✅ All new pages                             |
| FAQ sections on category pages           | ❌ Not yet — see task.md                     |
| Real photos (indexable `<img>`)          | ❌ Placeholder only — needs photos           |

---

## Remaining Known Issues (Carried from Previous Audit)

These were in `noteds.md` and remain unresolved:

| Issue                                                                                                                                  | Priority | Notes                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------- |
| Location pages are thin (3 cards + bullet list)                                                                                        | High     | Weakens local SEO significantly                                     |
| No photography on the site                                                                                                             | High     | Biggest conversion gap                                              |
| Hero image in CSS (not indexable `<img>`)                                                                                              | Medium   | A `.hero-bg-img` workaround class exists but may not be implemented |
| `IntersectionObserver` in `script.js` runs on all `.service-card` elements — will it conflict with the new `.hire-item-card` elements? | Low      | Category pages don't use `.service-card` so likely fine, but verify |

---

## Next Steps (Priority Order)

1. **Verify prices and item names** in all 14 category pages (client)
2. **Fix broken link** in `hire.html`: `packages.html` → `event-packages.html`
3. **Add photos** to category pages as Cloudinary images (client provides)
4. **Update nav link** from `hire` to `hire-intent.html` once pages confirmed correct
5. **Submit sitemap** to Google Search Console (manual step)
6. **Add FAQ sections** to category pages (3–4 questions each)
7. **Hero CSS ownership reviewed** — shared styles remain in `style.css`; sub-page overrides stay in `hero-option.css`
8. **Thicken location pages** with testimonials, venue lists, and FAQs
