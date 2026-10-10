# GPL Events & Hire — Improvement Roadmap

Generated from full site audit. Items are grouped by area and ordered by impact.
Quick wins have already been applied — this list covers the remaining improvements.

Related: location-page work is tracked separately in `locationpagestask.md`; hidden items in `hiddenitems.md`.

---

## Full Site Audit — 2026-10-09

Audit of all 98 pages: SEO, technical SEO, typos/content, design, fonts, accessibility, CSS/JS.
The site already converts — these are polish + fixes, no redesign. Ordered by impact within each group.
Items marked **Owner input** need a business decision before changing.

### 🔴 Fix first (broken things) — ✅ all fixed 2026-10-09

> Year: restored the original `.year` snippet (same as AirMarine `scripts/style.js`) at the top of
> `scripts/backtotop.js`, which every page loads. `scrollToForm()` now falls back to `/contact.html`.

- [x] **Two item pages are cut off mid-footer** — `hire/items/marry-me-marquee-set.html` and
  `hire/items/md-marquee-set.html` end at line 186 (no `</footer>`, `</body>`, scripts). Menu,
  option buttons and WhatsApp bar don't work. Rebuild the footer + scripts from a sibling item page.
- [x] **Wrong canonical on `event-packages.html:22`** — points to `/packages.html` (doesn't exist).
  Google may not index the packages page. Change to `/event-packages.html`.
- [x] **`event-packages.html` mobile menu doesn't work** — only loads `script.js` (line 548); missing
  `navbar.js`, `backtotop.js`, `scripts.js`. Also "Get Quote" (`:151`) calls `scrollToForm()` but the
  page has no form → JS error. Point it to `contact.html` or WhatsApp instead.
- [x] **Footer copyright year is blank on every page** — `<span class="year"> </span>` is empty and no
  script fills it. Renders as "© | GPL…". Add a one-line `getFullYear()` script or hard-code 2026.
- [x] **JS errors on every page** — `scripts/script.js:88` queries `.header` (doesn't exist) on every
  scroll; `scripts/scripts.js:84` reads `.testimonial-track` (only on index) with no null check.
  Add null guards. Remove leftover `console.log` (`script.js:83,207,216`).
- [x] **Footer "Services" links → `#ourservices`** on 86 pages — that anchor only exists on index.
  Change to `/index.html#ourservices` (or link to `event-packages.html`).
- [x] **Broken link** `hire/items/charger-side-plate-combo.html:229` → `about.html` (doesn't exist).
  That page's footer has drifted — replace with the standard footer.
- [x] **`event-packages.html:183`** "View Our Package Options" button has `href=""`.

### 🟠 SEO & Technical SEO

- [x] **sitemap.xml cleanup** *(Mostly done 2026-10-09 — removed hire-intent.html + hire-full.html, added the 2 gold-rim glass pages. Still to do: `<lastmod>` dates.)* *(Finished 2026-10-09 — `<lastmod>` on all 83 URLs; removed 4 empty `<url>` blocks left by earlier deletions.)*
  - Remove `hire-intent.html` (line 35 — file doesn't exist, 404 in sitemap)
  - Add missing `hire/items/gold-rim-champagne-glass.html` and `gold-rim-wine-glass.html`
  - Add `<lastmod>` dates
- [x] **Redirect the 3 merged hub pages** *(Done 2026-10-09 — forced `301!` in `_redirects`, removed from sitemap; files kept for re-enabling.)* — create a Netlify `_redirects` file:
  `/hire/accessories.html → /hire/table-decor.html 301`, `/hire/easels.html → /hire/welcome-board-stands.html 301`,
  `/hire/plinths.html → /hire/flower-stands.html 301`. Remove them from sitemap. (They currently
  show old/conflicting prices and are still indexed.)
- [x] **Decide on `hire-full.html`** *(Done 2026-10-09 — deleted; 301 → `hire.html` in new `_redirects`; removed from sitemap.)* — **Owner input.** It duplicates `hire.html` with an older price
  list that conflicts with item pages (Correx R350–R650 vs R900; marquee numbers R150–R300 vs R350).
  Recommend 301 → `hire.html`, or update prices.
- [x] **Compress huge images** *(Done 2026-10-09 — resized to ≤1600px + recompressed; assets 66 MB → 14 MB. `Asset 1@4x.png` → `asset-1.webp`. Originals are in git history. Still to decide: delete unused `image.png` + `IMG_7048.jpeg` (9 MB).)* (biggest page-speed win) — re-export ≤300 KB WebP or move to Cloudinary `f_auto,q_auto`:
  `assets/combo.jpg` **18 MB** (also used as og:image!), `Asset 1@4x.png` **13 MB**, `correx.jpg` 7.5 MB,
  `wineglass.jpg` 4.4 MB, `step-arch-backdrop.jpeg` 2.8 MB, `rosebank.jpeg` 1.9 MB, `welcome-board.jpeg` 1.6 MB,
  `Untitled-2-01/02.webp` 1.4/1.2 MB, `correx2.jpg` 1.3 MB. Delete unused `image.png` and `IMG_7048.jpeg`.
- [x] **Don't lazy-load the main item image** *(Done 2026-10-09 — 31 pages now `fetchpriority="high"`.)* — 31 item pages have `loading="lazy"` on `.img-primary`
  (above the fold). Remove it / add `fetchpriority="high"` → faster LCP.
- [x] **Add Google Analytics to all pages** *(Done 2026-10-09 — G-NE46SRYXMX on all 98 pages; `generate_lead` events for WhatsApp/phone/email taps + form submits in `scripts/script.js`. In GA4: Admin → Events → mark `generate_lead` as a key event.)* — GA only on `index.html` + `bespoke-gifting.html` (2 of 98).
  You can't see which hire/location pages drive enquiries. Add GA4 + click events on `wa.me`, `tel:`, form submit.
- [x] **Shorten titles >60 chars** *(Done 2026-10-09 — 38 titles rewritten, all ≤60.)* (42 pages — worst: `hire/table-decor` 98, `hire-full`/`flower-stands`/
  `welcome-board-stands` 93, `event-packages` 88, `crockery` 85, `bespoke-gifting` 84, `kids` 83, `index` 78).
- [x] **Shorten meta descriptions >155 chars** *(Done 2026-10-09 — 59 rewritten, all ≤155; og/twitter descriptions synced.)* (60 pages, mostly item pages — up to 287 chars).
- [x] **Fix Product schema on item pages** *(Done 2026-10-09 — prices fixed/added (arch-backdrop R550, square-white R1,100, cutlery R30, underplates R35/R20, white carpet R400); clear-acrylic-plinth offer removed until priced; `image` added on the 31 pages that have a photo + 2 gold-rim pages got Product schema. Remaining 36 item pages get `image` when photos are added. `priceValidUntil` skipped — optional.)*
  - Missing price: `cutlery-set`, `golden-pattern-underplate`, `natural-mat-underplate`, `clear-acrylic-plinth`; `white-carpet` has no offer at all
  - Schema price ≠ visible price: `arch-backdrop` (800 vs R550), `square-white-backdrop` (500 vs R1,100)
  - Add `image` (missing on 65) and `priceValidUntil` (missing on all)
- [x] **Homepage canonical slash** — `index.html:17,23` use no trailing slash; sitemap + twitter:url use `/`. Make all `https://www.gpleventsandhire.co.za/`. *(Done 2026-10-09)*
- [ ] **Social share image** *(Owner confirmed 2026-10-09: the `dhvalxorx` Cloudinary account is theirs — image is fine. Still worth giving item pages their own product photo.)* — 82 pages use a Cloudinary image from a different account
  (`dhvalxorx/.../Giftspeoplelove/Asset_1_nbjykf.png`). **Owner input:** confirm it's the GPL brand image.
  Item pages should use their own product photo.
- [x] **Align FAQ schema with visible FAQ text** *(Done 2026-10-09 — FAQPage schema rebuilt from the visible FAQs on 17 pages (41 differences); visible FAQ sections added to gold-balloon-flower-arch + white-carpet, which had schema only.)* (31 mismatched questions; some schema-only questions on
  bespoke-gifting, contact, event-packages, hire-full, and 4 item pages).
- [x] **LocalBusiness schema on location pages** *(Done 2026-10-10 — Midrand address + areaServed.)* — each claims its suburb as `addressLocality`, implying
  branches. Use the real Midrand address + `areaServed` for the suburb. (Links to locationpagestask.md Phase 2.)
- [x] **Render-blocking resources** *(Done 2026-10-09 — Google Fonts already moved to `<link>` + preconnect; Font Awesome now loads non-blocking (`media="print"` swap + `<noscript>` fallback); `defer` on all 393 local script tags.)*
  - Move Google Fonts from `@import` in `base.css:1` to `<link>` + preconnect in each page `<head>` (preconnect is only on index today)
  - Load Font Awesome non-blocking, or only the icons used
  - Add `defer` to scripts
- [x] **Add `width`/`height` to `<img>` tags** (483 missing) — prevents layout shift (CLS). *(Done 2026-10-09 — 483 tags, real intrinsic sizes. Also: navbar logo was an 8493px PNG on every page → Cloudinary `w_1000` (116 KB → 8 KB); footer logo → `w_1600` (110 KB → 12 KB); hero photo 1.9 MB → `w_1920` (480 KB) desktop / `w_900` (130 KB) mobile. **Broken:** homepage gallery "Corporate Event" image (`md-duran-…_vdcbiv.jpg`) returns 404 from Cloudinary — owner to re-upload/replace.)*
- [x] **Low:** add apple-touch-icon; twitter tags use `property=` instead of `name=`; footer logo alt *(Done 2026-10-09 — apple-touch-icon on all pages, twitter tags use `name=`, footer logo alt fixed. Phone display format left as-is.)*
  empty on bespoke-gifting:629, event-packages:460, hire-full:450; standardise phone display to `064 931 8467`.

### 🟡 Typos & Content

- [x] **Typos** *(Done 2026-10-09)*
  - `giant-jenga.html:182` (+FAQ schema) "adult and kids" → "adults and kids"
  - `table-decor.html:364` "centrepieces … creates" → "create"
  - `index.html:660` "became reality" → "became a reality"
  - `index.html:193–195` missing punctuation in "…your vision refined, memorable"
- [x] **"Whatsapp Us" → "WhatsApp Us"** *(Done 2026-10-09)* on the floating button (93 pages).
- [x] **Brand name in footer** *(Done 2026-10-09 — copyright line was hidden by `display:none` in footer.css; now visible as "© 2026 GPL Events & Hire | All rights reserved | Made with love by pixelsinframe.com". Lowercase "copyright" heading removed; designer link now goes to pixelsinframe.com; mobile WhatsApp bar no longer covers it.)* — "GPL Events and Hire" (82 pages) / "GPL events and Hire" (12) → "GPL Events & Hire".
  Footer heading "copyright" → "Copyright".
- [x] **UK spelling** *(Done 2026-10-09 — standardised on "Mom-to-Be")* — `bespoke-gifting.html`: personalized ×7, Personalization ×2, customized ×2,
  customization, "Party favors" → -ise/-isation/favours. `index.html`: "Specializing" (JSON-LD :62),
  "centerpiece(s)" alt text (:542, :570). Mom vs Mum mixed on bespoke-gifting (356–402) — pick one.
- [x] **Décor accent** *(Done 2026-10-09)* — `index.html:220, 288, 565` "decor" → "décor" (288 also "Hire Midrand" → "Hire in Midrand").
- [x] **Delivery contradiction** *(Done 2026-10-09 — owner confirmed: delivery for hire items is quoted separately. Updated all 15 category FAQs (+schema), LED selfie mirror, magic mirror, Correx. Event packages still say delivery/setup included — that is correct for packages. Owner also confirmed setup is NOT included for hire items — fixed arches, audio guestbook, kids, LED mirror, magic mirror.)* — **Owner input.** All category pages + hire-full say "Delivery, setup and
  collection are included"; ~54 item pages say "quoted separately"; `correx-welcome-board.html:187` vs `:191`
  contradict on the same page. Confirm the real policy, then make it one sentence everywhere.
- [x] **Package price contradiction** *(Done 2026-10-09 — owner confirmed birthday packages start from R2,500; all 7 location pages updated.)* — **Owner input.** Location pages say birthday packages "From R1,200–R1,300"
  (e.g. `sandton.html:199`); `event-packages.html:229` and `index.html:829` say packages start at R2,500.
- [x] **Card vs item page price mismatches** *(Resolved — the mismatched hub pages were redirected; remaining cards match.)* (mostly on the to-be-redirected hubs)
  - Candle Holders: `accessories.html:201` says R200–R350, the item page says R100
  - Wooden A-Frame Easel: `easels.html:175` vs its item page
  - Gold Metal Easel: `easels.html:190` vs its item page
  - White Carpet: unit "/ per day" on the item page only
- [ ] **Wrong-item / contradictory copy** *(Partly done 2026-10-09 — fixed: charger→dinner plate copy + WhatsApp texts, crockery combo pre-fill, event-packages tagline, lawn-games "all three", kids 10/20 FAQ contents, marquee popular sets, Pretoria → Midrand/Centurion, branded-cup alt text. Owner answers applied 2026-10-09: plates/glasses per item; kids ages 2–12; guests rinse glasses; selfie mirror not in stock → its 3 pages noindexed + removed from sitemap (see hiddenitems.md). Throne chairs (pair only) and shot glasses hidden by owner — noindexed + removed from sitemap. Also hidden 2026-10-09: sweetheart table, ghost chairs, cocktail table, cornhole, ring toss, white champagne board (furniture + lawn-games copy and ItemLists now list visible items only). Kids sets renamed to "Kids Table & 10 Chairs (Hire Only)" and "20 Kids Chairs (Hire Only)" — new URLs with 301s from the old `*-kids-party-setup` URLs; category FAQs now state setup is not included. **Still open:** caption for the branded-cup photo on index.html (currently "Table Décor").)*
  - `charger-plates.html` — H1 says Dinner Plate, hero and WhatsApp say Charger Plates
  - `crockery.html:275` — WhatsApp pre-fill names the wrong combo
  - "Sets of 10" vs per-item pricing on plates/glasses
  - `event-packages.html:178` / `hire-full.html:169` — taglines swapped
  - `lawn-games.html:253,257` "all three games" → four listed
  - Kids pages — ages 2–10 vs 3–12; 20-kids page chairs-only vs "tables and chairs"; 10-kids "tables" when there's one table
  - `throne-chair.html:181` pair-only vs `furniture.html:358` singles available
  - Glass washing — `champagne-flutes.html:185` vs `crockery.html:359`
  - Selfie mirror printing — included (`selfie-mirrors.html:205`) vs "confirm" (`led-selfie-mirror-station.html:181`)
  - `marquee-letters.html:354` names sets that differ from `popular-marquee-sets.html`
  - `index.html:289` mentions Pretoria (not a service area elsewhere)
  - `index.html:565` caption "Table Decor" on a ceremony photo
- [x] **Hero copy names hidden items** *(Done 2026-10-09 — drinks-boards now describes the champagne wall; crockery lists visible items.)* — `drinks-boards.html:151`, `welcome-board-stands.html:319`,
  `crockery.html:160` (shot glasses has no card). Reword or un-hide.
- [x] **Orphan item pages** *(Resolved 2026-10-09 — both hidden/noindexed.)* — `shot-glasses.html`, `white-champagne-board.html` have no category card linking
  to them (latter says "for Hire" but "yours to keep"). Add a card or remove from sitemap.
- [x] **WhatsApp pre-fill greeting** *(Done 2026-10-10 — all 760 pre-filled links open with "Hi GPL Events,"; 241 blank links now carry a default message; option-button messages in scripts.js updated.)* — standardise to one format ("Hi GPL Events, I'm interested in…").
- [ ] **Testimonials** — all dated Jan–Apr 2025 (18+ months old) and out of order. **Owner input:**
  add newer Google reviews, or drop month labels.

### 🔵 Design, Fonts & Accessibility

- [x] **Body font isn't what was intended** *(Done 2026-10-09 — body/p/li now Manrope; headings stay Faustina; fonts loaded via `<link>` + preconnect on all pages instead of `@import`.)* — `base.css:182–188` overrides `p`/`li` to Faustina, so all body copy
  is serif; `body` has no `font-family` at all, so buttons/links outside `p` fall back to Times.
  Fix: `body { font-family: var(--ff-primary); }` and remove the Faustina override on `p, li`.
  Drop the unused Manrope 200 weight. Replace hardcoded `sans-serif` (`buttons.css:107`).
- [x] **WhatsApp button contrast** *(Done 2026-10-09 — new vars `--clr-whatsapp: #0e7a5f` (5.3:1) / `--clr-whatsapp-dark: #075e54`.)* — white on #25d366 is 1.98:1 (fails). Use darker green #128c7e / #075e54
  on item enquiry buttons (`collections.css:269,420`), sticky bar (`style.css:1065`), footer link (`footer.css:118`).
  This is the main conversion button — make it pop.
- [x] **Other contrast fails** *(Done 2026-10-09 — nav links → `--clr-secondary-red` (light pink on mobile navy menu); quote button white on red; contact links + hero USP → #ffcdd2 on dark; USP on white → dark red. Also added explicit white page background + `color-scheme: light` — dark-mode browsers were painting unstyled sections black.)*
  - Red contact links on navy (`style.css:688`, 2.36:1)
  - Hero USP red on dark overlay (`style.css:67`)
  - Nav links #ef5350 on blush (`navbar.css:50`, 2.9:1)
  - Navy on red quote button (`navbar.css:148`)
  - Fix: use a darker red (#b71c1c) on light backgrounds, white on red
- [x] **Option buttons go blank on hover** *(Done 2026-10-09 — global `button:hover` wrapped in `:where()`.)* — `base.css:271` `button:hover { background: navy }` beats
  `.option-btn` → navy text on navy. Scope the global rule.
- [x] **Form labels + focus styles** *(Done 2026-10-09 — visible labels, autocomplete hints, Netlify honeypot, clear focus outline, "Message us instead" WhatsApp link; Last name + guests now optional.)* — forms (`index.html:759–800`, `contact.html`) use placeholders only;
  focus ring nearly invisible (`style.css:790–792`, `base.css:256`). Add visible labels + clear focus outline.
  Add a Netlify honeypot field (`netlify-honeypot`) to cut spam.
- [x] **Footer/nav drift** *(Done 2026-10-09 — footer redesigned and identical on all 98 pages; source in `tools/footer.html`.)* — standardise footer on `contact.html` (different Services list), `giant-tic-tac-toe.html`,
  `charger-side-plate-combo.html`; add missing WhatsApp float to `charger-side-plate-combo`, `gold-rim-champagne-glass`,
  `gold-rim-wine-glass`; fix different nav markup on `giant-tic-tac-toe`, `gold-balloon-flower-arch`.
- [x] **Accessibility basics** *(Done 2026-10-09 — skip link + `<main>` on all pages, back-to-top is a `<button>`, decorative icons `aria-hidden`, star ratings labelled, testimonial dots focusable, delivery modal focus handling, marquee respects reduced motion.)*
  - Add a skip link and a `<main>` landmark
  - Back-to-top is an `<img>`, so make it a `<button>`
  - Remove `aria-label` on decorative `<i>` icons and `aria-hidden` wrapping focusable dots (`index.html:686`)
  - Delivery modal needs focus management
  - Testimonial marquee should respect `prefers-reduced-motion`
- [x] **Tiny tap targets / text** *(Done 2026-10-09 — option buttons 36px, delivery link 0.82rem, service tags 0.68rem, testimonial dots 24px tap area.)* — `.option-btn` ~18px tall @0.65rem, `.delivery-info-trigger` 0.72rem,
  `.service-tag` 0.52rem (~8px), testimonial dots 8px. Aim for ≥44px tap height, ≥12px text.
- [x] **CSS tidy-up (low)** *(Done 2026-10-10 — 23 unused rules removed (old buttons, nav phone, old package/footer classes); `.ti-widget` kept for Trustindex.)*
  - Load `base.css` before `style.css`
  - `contact.html` is missing `testimonial.css`
  - Replace the hardcoded #1a237e (11×) / WhatsApp greens with vars
  - Define or remove `--card-img`
  - Delete dead selectors and unused vars
  - Merge the duplicate `.cta-primary-btn` and `.hire-item-img` rules
  - Fix the 768px breakpoint overlap (`footer.css:154`) and the 1024/768 order in `testimonial.css:59–80`
  - Remove the dead `handleFormSubmit` / `scrollToContact` JS

### 💡 Conversion ideas (optional, after fixes)

- [ ] Make WhatsApp the primary CTA everywhere (darker green, pre-filled with page/item name).
- [x] Rename "Get an Instant Quote" *(Done 2026-10-09 — now "Get a Free Quote".)* (`index.html:197`) — it only scrolls to a form. Consider a 3-field quick-quote
  (date, area, WhatsApp number) on package + location pages.
- [ ] Trust signals near CTAs: Google rating + review count, real event photos on cards.
- [x] "Request these items" multi-select on hire pages that builds one WhatsApp message. *(Done 2026-10-09 — `scripts/enquiry-list.js`: "Add to list" on every visible card + item page, list kept across pages (localStorage), floating bar → one WhatsApp message with items, sizes, prices + date/venue prompts; GA4 `add_to_enquiry` event.)*
- [x] Replace the auto-scrolling testimonial marquee with static review cards. *(Done 2026-10-09 — homepage Portfolio redesigned (photo grid + lightbox, swipe carousel on mobile, real captions, CTA; broken Cloudinary photo removed) and Reviews redesigned (cards, mobile carousel, Google summary + links). **Google reviews:** `<div id="google-reviews">` in index.html is the slot for the Trustindex widget — paste its `<script>` there; fallback cards hide automatically once it renders.)*

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

- [x] **Thicken location pages** *(Done 2026-10-10 — see locationpagestask.md.)*
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

- [x] **Standardise the "Hire Items" link format across all pages** *(Done 2026-10-09 — all internal page links now use `.html`, matching canonicals; nav link titles fixed.)*
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

### Status — ✅ built 2026-10-09

> `hire-items.json` is generated by `python3 tools/build-hire-items.py` from the **visible** cards on each visible category page. **Re-run it whenever an item is added, hidden, renamed or re-priced.** Search logic: `scripts/hire-search.js` (name matches first, then same-category items; accent/plural tolerant; `hire.html?q=arch` deep links; GA4 `search` event).

- [x] Build `hire-items.json` with all visible items
- [x] Add search input + results panel to `hire.html`
- [x] Write search JS (filter by name — individual item pages now exist, so `itemUrl` can link directly)
- [x] Style search input to match site (navy border, Manrope font)

---

## Event Packages + Bespoke Gifting Rebuild — 2026-10-09

> **Real event photos added 2026-10-10 (Equinix JNO office opening, Johannesburg):** corporate package cards, homepage portfolio (3 new tiles, JNO marquee featured), Johannesburg location page "Recent work" gallery, and "Seen at a real event" photos on the champagne wall, marquee letters and stanchion pages. Photos JNO2, JNO3 and JNO4 are unused — keep for later.

Both pages rebuilt with **Essential · Signature · Luxe** tiers (Signature = "Most popular"), category tabs,
mobile swipe-to-compare cards, "From R…" pricing, booking/ordering steps, enquiry-list buttons and updated FAQs.
**All package content lives in `tools/packages-data.json`** — edit it, then run `python3 tools/build-packages.py`.

Owner policies applied: event setup included, delivery & collection charged (usually ~R1,600 most Gauteng venues);
70% deposit secures the date, balance a week before; refundable/transferable with enough notice; security deposit
may apply (often waived). Gifting: full payment upfront by EFT; free delivery Midrand, Waterfall, Carlswald, Kyalami,
Fourways; R150 flat rate elsewhere in Gauteng; 3–5 / 7–10 business days; fresh bouquets same day before 12:00;
corporate: no minimum, branding available, bulk discounts.

### Owner to fine-tune
- [ ] **Review package inclusions** — drafted from the hire stock; adjust wording/items in `tools/packages-data.json`
- [ ] **Review prices** — events: Birthday R3,500 / R6,500 / R12,000; Baby shower R6,500 / R9,500 / R14,500;
  Wedding R12,000 / R22,000 / R38,000; Corporate R5,000 / R10,000 / R20,000. Gifting (owner-set starting prices,
  upper tiers drafted): Him/Her/Mom-to-Be R2,500 / R3,500 / R5,000; Birthday R1,800 / R2,800 / R4,000;
  Flowers R700 / R1,200 / R2,000; Corporate R1,500 / R2,500 / custom quote.
- [x] **Guest guides** — owner set 2026-10-09: Essential up to 20, Signature 20–50, Luxe 50–80 (birthday, baby shower); wedding + corporate up to 50 / 50–100 / 100–150; table counts in inclusions scaled to match
- [x] Homepage FAQs, contact FAQ and the 7 location pages updated to the new prices/terms

### Photos needed (30 — 3 done: corporate tiers use the Equinix JNO opening photos, 2026-10-10) — placeholders show "Photo coming soon" until added
Size: **1200 × 900 px (4:3)**, WebP or JPG, real setups/gifts. To add one: save it at the path below, set
`"photo": "assets/packages/<file>"` on that tier in `tools/packages-data.json`, run `python3 tools/build-packages.py`.

| Category | Tier | Package | File |
|---|---|---|---|
| Birthday | Essential | Essential Birthday | `assets/packages/birthday-essential.webp` |
| Birthday | Signature | Signature Birthday | `assets/packages/birthday-signature.webp` |
| Birthday | Luxe | Luxe Birthday | `assets/packages/birthday-luxe.webp` |
| Baby Shower | Essential | Essential Baby Shower | `assets/packages/baby-shower-essential.webp` |
| Baby Shower | Signature | Signature Baby Shower | `assets/packages/baby-shower-signature.webp` |
| Baby Shower | Luxe | Luxe Baby Shower | `assets/packages/baby-shower-luxe.webp` |
| Wedding | Essential | Essential Wedding | `assets/packages/wedding-essential.webp` |
| Wedding | Signature | Signature Wedding | `assets/packages/wedding-signature.webp` |
| Wedding | Luxe | Luxe Wedding | `assets/packages/wedding-luxe.webp` |
| Corporate | Essential | Essential Corporate | ✅ done — Equinix JNO photo (Cloudinary) |
| Corporate | Signature | Signature Corporate | ✅ done — Equinix JNO photo (Cloudinary) |
| Corporate | Luxe | Luxe Corporate | ✅ done — Equinix JNO photo (Cloudinary) |
| For Him | Essential | Classic Gentleman's Hamper | `assets/packages/him-essential.webp` |
| For Him | Signature | Executive Gift Set | `assets/packages/him-signature.webp` |
| For Him | Luxe | Sports & Wellness Hamper | `assets/packages/him-luxe.webp` |
| For Her | Essential | Classic Pamper Hamper | `assets/packages/her-essential.webp` |
| For Her | Signature | Gourmet & Luxury Gift Box | `assets/packages/her-signature.webp` |
| For Her | Luxe | Luxury All-In-One Gift | `assets/packages/her-luxe.webp` |
| Mom-to-Be | Essential | Expecting Mom Comfort Bundle | `assets/packages/mom-to-be-essential.webp` |
| Mom-to-Be | Signature | Mom-to-Be Celebration Pack | `assets/packages/mom-to-be-signature.webp` |
| Mom-to-Be | Luxe | Complete Mom-to-Be Experience | `assets/packages/mom-to-be-luxe.webp` |
| Birthday | Essential | Birthday Celebration Hamper | `assets/packages/birthday-gifts-essential.webp` |
| Birthday | Signature | Birthday Experience Box | `assets/packages/birthday-gifts-signature.webp` |
| Birthday | Luxe | Milestone Birthday Edition | `assets/packages/birthday-gifts-luxe.webp` |
| Flowers | Essential | Essential Bouquet | `assets/packages/flowers-essential.webp` |
| Flowers | Signature | Signature Bouquet | `assets/packages/flowers-signature.webp` |
| Flowers | Luxe | Luxe Flower Box | `assets/packages/flowers-luxe.webp` |
| Corporate | Essential | Thank You & Appreciation Gift | `assets/packages/corporate-gifts-essential.webp` |
| Corporate | Signature | Congratulations & Milestone Gift | `assets/packages/corporate-gifts-signature.webp` |
| Corporate | Luxe | Custom Corporate Gift Solution | `assets/packages/corporate-gifts-luxe.webp` |

---

## Top Hire Item Pages Upgrade — 2026-10-10

10 key item pages now have What's included, How it works (where useful), Perfect for, Pair it with,
service-area links and 4–6 FAQs (schema synced): marquee letters A–Z, marquee numbers, popular marquee sets,
champagne wall, round circle arch, balloon arch, gold balloon/flower arch, A1 Correx welcome board,
welcome board flower box, step arch backdrop (+ the retro audio guestbook, done by hand).
Content in `tools/item-extras.json` → `python3 tools/build-item-extras.py` — add more items by adding entries.

- [ ] Owner: review the drafted "Perfect for" / "Pair it with" lists and new FAQs
- [x] Next candidates: kids sets, crockery items, plinths/stands, carpets & stanchions *(Done 2026-10-10 — 24 more pages; 34 item pages upgraded in total.)*

---

## Year-End Functions + Our Work pages — 2026-10-10

- `year-end-functions.html` — corporate packages (live prices), Equinix gallery, year-end add-ons, staff/client gifting,
  booking timeline, 7 FAQs, Service + FAQ schema. Linked from footer, corporate packages, corporate gifts, and the
  Sandton / Johannesburg / Centurion / Waterfall location pages.
- `our-work.html` — Equinix JNO case study (what we styled, items used, 7-photo masonry gallery + lightbox) and
  "More recent setups". Linked from the footer and the homepage portfolio.
- Both built by `python3 tools/build-pages.py`. **To add a new case study:** add an entry to `WORK` in that file
  (client, title, place, summary, what we styled, items, Cloudinary photo ids) and re-run.
- [ ] After the festive season (January): swap the year-end page's urgency line or point it at next year
- [ ] Owner: send photos from each new event → new case study on Our Work

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
