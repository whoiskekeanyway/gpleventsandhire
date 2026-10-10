# Location Pages Task List

> **Rebuilt 2026-10-10.** Content for all 7 pages lives in `tools/locations-data.json` → `python3 tools/build-locations.py`. Still open: real photos, local testimonials, venue names, and an optional service-areas hub page (+ a Kyalami page — it's a free gift-delivery zone with no page yet).

**Goal:** Make the seven location pages useful for local search visitors and guide them to a relevant enquiry.

Work through one unchecked task at a time. Check an item only after verifying it on all affected pages. Items marked **Owner input** need confirmed business details or assets before implementation.

Pages: `locations/midrand.html`, `locations/johannesburg.html`, `locations/sandton.html`, `locations/centurion.html`, `locations/waterfall.html`, `locations/carlswald.html`, `locations/fourways.html`.

## Phase 1: Fix the Journey

- [x] Fix or replace the footer service links pointing to `#ourservices`; ensure each link reaches a real service section or page.
- [x] Put a clear enquiry action beside each service offer, using the correct enquiry route and location-specific message.
- [x] Check all navigation, footer, package, hire, and contact links on each location page; remove dead or misleading destinations.

## Phase 2: Confirm the Offer

- [x] **Owner input:** Confirm prices, inclusions, minimum spend, delivery/setup fees, and availability for each advertised service. *(Done 2026-10-10 — prices pulled live from `tools/packages-data.json`; delivery/setup terms from owner policies.)*
- [x] Make location-page prices and offer descriptions consistent with the homepage and event-package pages; clearly distinguish packages from individual hire. *(Done — package cards use the same data as event-packages.html; hire shown separately.)*
- [x] **Owner input:** Confirm the areas actually served and any location-specific delivery or setup limits; publish only verified claims. *(Done — 7 areas; beyond Centurion/other areas = "send us the address".)*
- [x] **Owner input:** Confirm the business's actual premises/base. Keep LocalBusiness address and service-area schema accurate; do not imply a physical branch in every target location. *(Done — LocalBusiness now uses the Midrand address on every page, with the suburb in `areaServed`.)*
- [x] **Owner input:** Confirm answers to location-relevant questions about delivery, setup, lead time, venue coordination, and booking before publishing FAQs. *(Done — 5 FAQs per page from owner policies.)*

## Phase 3: Add Genuine Local Value

- [x] Replace generic location claims with confirmed neighbourhood coverage, venue knowledge, or service details specific to each area. *(Done without venue names — real geography, area-specific event types and gift-delivery terms. Add venues later in `tools/locations-data.json`.)*
- [ ] **Owner input:** Add genuine event photos from completed work, with permission and accurate location captions where known.
- [ ] **Owner input:** Add customer testimonials or project examples only when the customer, location, and permission are confirmed.
- [x] Add concise location-specific FAQs using the confirmed policies; avoid copying the same generic answers across every page. *(Done — each page has its own FAQs; ~2 of ~20 sentences shared between pages.)*
- [ ] Review whether a central service-areas page would help visitors compare locations, and link it to all seven pages if created.

## Phase 4: Verify

- [x] Check that each page has a distinct title, meta description, heading, and useful location-specific body content. *(Done)*
- [x] Verify every local link, stylesheet, script, image, canonical URL, structured-data URL, and sitemap entry uses the `/locations/` path correctly. *(Done — tools/check-site.py passes.)*
- [x] Test each page on mobile and desktop; confirm the primary enquiry action is visible and works. *(Done)*
- [ ] Recheck prices, business details, schema, and local claims against the owner's confirmed information before publishing.
