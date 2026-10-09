# GPL Events & Hire — Improvement Roadmap

Generated from full site audit. Items are grouped by area and ordered by impact.
Quick wins have already been applied — this list covers the remaining improvements.

Related: location-page work is tracked separately in `locationpagestask.md`; hidden items in `hiddenitems.md`.

---

## UI / UX

- [x] **Add a sticky WhatsApp CTA on mobile**
  A fixed bottom bar on small screens showing "Chat with us on WhatsApp" with the green icon.
  Significant conversion win — visitors scroll through packages without a persistent contact option.

- [x] **Visual tier hierarchy on package cards**
  Basic / Standard / Premium / Luxury cards look identical. Add a subtle visual cue per tier:
  e.g. a thin coloured top stripe (cream → rose → navy → gold) or a tier badge ("Most Popular").

- [x] **Style "Custom Pricing" / "Request a quote" price badges differently**
  These look like missing data against the red filled badge. Use a navy outline badge instead:
  `border: 1px solid var(--clr-primary-navy); color: var(--clr-primary-navy); background: transparent;`

- [x] **Add `aria-current="page"` to active nav link + CSS style**
  Users and screen readers have no indication of which page they're on.
  Add `aria-current="page"` to the relevant `<li>` or `<a>` in each page's navbar, and style it:
  `font-weight: 700; border-bottom: 2px solid var(--clr-accent-red);`

- [x] **Replace hero animation with CSS-only approach**
  `script.js` uses `setTimeout` + inline styles for the hero fade-in, which can flash on slow connections.
  Use a CSS `@keyframes heroEnter` with `animation-fill-mode: both` instead.

- [x] **Improve testimonial section**
  - Add month/year to each testimonial (undated testimonials look old or unverified)
  - Add a Google Reviews badge or link — "Read all our reviews on Google"
  - Consider a carousel for mobile so cards don't stack to a very long scroll

- [ ] **Add event photos to package cards**
  The gradient placeholder is in place — swap it for real photos when available.
  Each card has `.service-card-img` — just add `style="background-image: url('...')"`.

---

## SEO

- [x] **Add `robots.txt`**
  Create at the project root. Minimum content:
  ```
  User-agent: *
  Allow: /
  Sitemap: https://www.gpleventsandhire.co.za/sitemap.xml
  ```

- [x] **Submit sitemap to Google Search Console**
  Go to search.google.com/search-console → Sitemaps → enter `sitemap.xml` URL.
  `sitemap.xml` has been created — it just needs to be submitted.

- [x] **Add breadcrumb navigation to sub-pages**
  Simple text breadcrumbs (`Home > Event Packages`) improve both UX and SEO.
  Add BreadcrumbList schema alongside each page's existing LocalBusiness schema.

- [ ] **Add `hreflang` if you ever add other language versions**
  Not urgent now, but keep in mind for future growth. *(No action needed until other languages are added.)*

- [ ] **Thicken location pages**
  Each location page currently has only 3 cards + a bullet list. Google ranks thin pages poorly.
  Suggested additions per location page:
  - 1–2 local testimonials (client from that area)
  - A "Venues we work with in [Location]" bullet section
  - An FAQ specific to events in that area

- [x] **Add hero background as an `<img>` element (not CSS)**
  Google cannot index CSS background images. The hero image is currently in `style.css`.
  Consider adding a visually hidden `<img>` with descriptive alt text, or use a `<picture>` element
  with the overlay on top via CSS.

- [x] **Audit and differentiate meta descriptions per page**
  Several pages may share similar descriptions. Each should be unique (max 155 characters)
  and include the city name + 1–2 service keywords.

---

## Technical

- [x] **Consolidate font stacks**
  `base.css` imports Faustina + Manrope. `style.css` still references `'Playfair Display'` and
  `'Inter'` as string literals in a few component-level rules (contact form, area card h3, step h3).
  Replace all hardcoded font-family strings with `var(--ff-secondary)` / `var(--ff-primary)`.
  Files to check: `css/style.css` (grep for `Playfair` and `'Inter'`).

- [x] **Add `font-display: swap` to Google Fonts import**
  In `css/base.css`, append `&display=swap` to the fonts URL (it may already be there — verify).
  This prevents invisible text while fonts load. *(Was already present — confirmed.)*

- [x] **Add `loading="lazy"` to below-the-fold `<img>` tags**
  Currently only the hero and logo images are above the fold. All gallery images and footer logos
  should have `loading="lazy"` to defer loading.

- [x] **Remove unused `@keyframes fadeInUp` from style.css**
  The animation was removed from the ruleset but the `@keyframes` block itself is still in the file.
  Delete it (search for `@keyframes fadeInUp`).

- [x] **Form: wire up to a real backend or form service**
  The contact form currently only logs to console. Options:
  - [Formspree](https://formspree.io) — free tier, no backend needed, 1 line change
  - EmailJS — send directly from the browser
  - A simple serverless function (Netlify/Vercel Functions)
  *(Netlify confirmed — `data-netlify="true"` is set on both forms.)*

- [x] **Add a `<meta name="theme-color">` to pages that are missing it**
  Some location pages may be missing this tag. Verify all pages have:
  `<meta name="theme-color" content="#1a237e">` *(All 11 pages already had it — confirmed.)*

- [x] **Add `rel="noopener noreferrer"` to all external links**
  All `target="_blank"` links should have this for security.
  Run: `grep -rn 'target="_blank"' *.html | grep -v 'noopener'` *(No violations found — confirmed.)*

---

## Content / Non-Technical

- [x] **Add a social proof counter to the homepage hero**
  A single line near the hero CTA: "200+ events styled across Gauteng" — increases trust before
  the visitor scrolls. Update the number periodically.

- [x] **Add a Google Maps embed to the contact section**
  A map showing your Midrand base and service radius is a strong local SEO trust signal.
  Embed via Google Maps iframe (free, no API key needed for basic embed).
  *(Added to contact.html below the enquiry form.)*

- [x] **Cross-sell gifting from event packages**
  `bespoke-gifting.html` is disconnected from the main event flow.
  Add a "Complete your event with bespoke gifting →" section at the bottom of
  `event-packages.html` and vice versa.

- [x] **Add a simple FAQ section to each major page**
  Common questions (min 4–5 per page) improve SEO and reduce "how much does it cost?" enquiries.
  Example questions:
  - "Do you deliver and set up?"
  - "How far in advance do I need to book?"
  - "Can I hire individual items without a full package?"
  - "Do you service [specific area]?"

- [ ] **Add photography to the website**
  The biggest gap. Even 5–8 high-quality event photos (real work, not stock) would:
  - Fill the package card placeholders
  - Build immediate trust
  - Improve Google Business Profile visibility

- [x] **Add date to testimonials**
  "April 2025" or "early 2025" is enough — undated reviews feel fabricated.

- [x] **Add a WhatsApp Business link to the footer**
  The footer has navigation and Google Business but no direct WhatsApp link.
  Clients who scroll to the bottom should have an easy way to contact you.

---

## Hire Collections — Added 2026-06-20

New files: `hire-intent.html` (hub), `css/collections.css`, and 14 pages under `/category/`.

> **Update 2026-10-09:** The hub has since been renamed to `hire.html` and the category pages moved to `/hire/*.html`.
> Three more categories were added: `crockery.html`, `kids.html`, `marquee-letters.html` (17 in total).

### Bugs to Fix

- [x] **Broken cross-sell link in `hire.html`**
  `href="packages.html"` on line ~399 — file does not exist. Correct path is `event-packages.html`.
  Fix: `href="packages.html"` → `href="event-packages.html"`.

- [ ] **Standardise the "Hire Items" link format across all pages**
  The hub is now `hire.html` (superseding `hire-intent.html`), so links already reach the right page.
  But two formats are mixed: extensionless (`href='hire'`, `'../hire'`, `'../../hire'` — ~88 links)
  and `hire.html` (~101 links). Pick one style site-wide (match `canonical` URLs) and apply it.

- [x] **Deduplicate CSS between `style.css` and `hero-option.css`**
  Both files define `.cta-primary`, `.cta-secondary`, `.hero-overlay`, `.hero-content`,
  `.hero-cta`, `.linking-container`, `.hero-subtitle`, `.hero-usp`. Last loaded wins.
  Fixed: `index.html` loads only `style.css` (not hero-option.css), so shared rules stay in
  `style.css`. Removed all duplicates from `hero-option.css` — it now owns only `.hero-options`
  and sub-page spacing overrides. Side-effect: fixes `.cta-primary` flat gradient bug on sub-pages.

### Content to Fill In (Client Action Required)

- [ ] **Verify and update all hire item prices**
  All prices in category pages are estimated. Client must confirm:
  accessories (3 items), audio-guestbook-sets (2), arches (3), backdrops (3),
  drinks-boards (3), easels (3), flower-stands (3), furniture (4), lawn-games (3),
  plinths (3), selfie-mirrors (2), signs (3), table-decor (3), welcome-board-stands (4).

- [ ] **Verify and update all hire item names**
  Names are representative placeholders. Client should confirm stock and adjust accordingly.

- [ ] **Add real photos to category pages**
  All `.hire-item-img` and `.collection-card-img` are placeholder gradient divs.
  When photos are ready — host on Cloudinary with `f_auto,q_auto` transformation,
  add `<img loading="lazy">` inside each image div with descriptive `alt` text.
  Also replace FA icon tiles in `hire.html` collection cards with category photos.

### SEO — Post-Launch Actions

- [ ] **Submit updated sitemap to Google Search Console**
  `sitemap.xml` now has 96 URLs (main pages, locations, 17 category pages, item pages).
  Go to Search Console → Sitemaps → submit `https://www.gpleventsandhire.co.za/sitemap.xml`.

- [x] **Add FAQ sections to all 14 category pages**
  4 questions per page — 3 shared (individual hire, delivery, advance booking) + 1 category-specific.
  FAQPage JSON-LD schema added to `<head>` of each page for Google rich results. HTML uses same
  `<details>/<summary>` accordion pattern as `hire.html`.

---

## Individual Item Pages — 2026-06-22

Each hire item gets its own page at `/hire/items/{{item-slug}}.html` for dedicated SEO per item.

### Template
- **File:** `hire/items/item-template.html`
- Copy → rename → replace all `{{placeholders}}` to create a real item page
- All CSS/script paths already set for the `/hire/items/` depth (`../../`)
- Schema: BreadcrumbList (4 levels) + Product schema + FAQPage

### Checklist per item page
- [ ] Unique slug (e.g. `white-square-plinth`)
- [ ] Title, meta description, canonical URL filled in
- [ ] H1 and hero subtitle written
- [ ] WhatsApp pre-fill text URL-encoded correctly
- [ ] Breadcrumb: correct category name + category slug
- [ ] Description paragraph (2–3 sentences, mention Midrand + Gauteng)
- [ ] Size option buttons added/removed as needed
- [ ] Correct price in JSON-LD `price` field
- [ ] Image uncommented once photo is available
- [ ] Item-specific FAQ question written

### Items to build (visible items only — hidden items can wait)

✅ **All 23 built** (checked 2026-10-09). 67 item pages now exist in `/hire/items/`.
Where the actual file name differs from the planned slug, it's shown in the Slug column.

Pages created in `/hire/items/`:

| Item | Slug | Category slug |
|---|---|---|
| Throne Chair | throne-chair | furniture |
| Sweetheart Table | sweetheart-table | furniture |
| Ghost Chair | ghost-chairs | furniture |
| Cocktail Table | cocktail-table | furniture |
| Stanchion Rope Set (Gold) | stanchion-rope-set | furniture |
| Carpet (Bright Red) | red-carpet | furniture |
| Tall Floral Stand (pair) | tall-floral-stand | flower-stands |
| Round Pedestal Stand | round-pedestal-stand | flower-stands |
| Cylinder Stand | cylinder-stand | flower-stands |
| White Square Plinth | white-square-plinth | flower-stands |
| Clear Acrylic Plinth | clear-acrylic-plinth | flower-stands |
| 3pc Clear Acrylic Plinth Set | 3pc-acrylic-plinth-set | flower-stands |
| A1 Correx Welcome Board | correx-welcome-board | welcome-board-stands |
| Wooden A-Frame Easel | wooden-aframe-easel | welcome-board-stands |
| Welcome Board (Flower Box) | welcome-board-flower-box | welcome-board-stands |
| Decorative Gold Metal Easel | gold-metal-easel | welcome-board-stands |
| Round Circle Arch | round-circle-arch | arches |
| Balloon Arch | balloon-arch | arches |
| Square Arch | square-arch | arches |
| White Champagne Board | white-champagne-board | drinks-boards |
| Candle Holders (set of 6) | candle-holders | table-decor |
| Rose Gold Candle Sticks | rose-gold-candle-sticks | table-decor |
| Black Candle Sticks | black-candle-sticks | table-decor |

---

## Search Functionality — 2026-06-22

Client-side JSON search on `hire.html` (the hire hub) — no backend, no dependencies.

### Approach
1. **`hire-items.json`** (project root) — array of every visible hire item:
   ```json
   [
     {"name": "Throne Chair", "category": "Furniture", "categoryUrl": "hire/furniture.html", "itemUrl": "hire/items/throne-chair.html", "price": "R800"},
     ...
   ]
   ```
2. **Search input** added above the collections grid on `hire.html`
3. **JS** fetches the JSON, filters on keyup, renders matching result cards in a results panel above the grid — clears when input is empty

### Status
- [ ] Build `hire-items.json` with all visible items
- [ ] Add search input + results panel to `hire.html`
- [ ] Write search JS (filter by name — individual item pages now exist, so `itemUrl` can link directly)
- [ ] Style search input to match site (navy border, Manrope font)

---

## Future Category Pages — From Competitor Research (2026-06-20)

Ideas sourced from Backdrop & Decor Hub and Cherri Hire. Not yet built — log here for future sprints.

| Category | Source | Notes |
|---|---|---|
| ~~**Glassware**~~ | Backdrop Hub (11 products) | ✅ Built — wine, champagne & shot glasses live under `hire/crockery.html` |
| ~~**Crockery & Tableware**~~ | Cherri Hire | ✅ Built — `hire/crockery.html` |
| **Chair Covers & Ties** | Cherri Hire | Pairs well with existing furniture hire if catalogue grows |
| ~~**Kiddies / Children's Party**~~ | Cherri Hire | ✅ Built — `hire/kids.html` |
| **Bar & Beverage Equipment** | Cherri Hire | Juice dispensers, bar carts — depends on client offering |
