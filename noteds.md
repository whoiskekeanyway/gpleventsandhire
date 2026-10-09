 <div class="why-choose-image">
                    <div class="image-placeholder">
                        <img src="https://res.cloudinary.com/dp24kap9x/image/upload/v1759646923/IMG_3271_ibyci0.jpg"
                            alt="">
                   <i class="fas fa-image"></i>
                        <p>Professional event setup showcasing GPL Events & Hire's attention to detail</p>
                        </div>





Accessories
Audio Guestbook Sets
Arches
Backdrops
Drinks Boards
Easels
Flower Stands
Furniture
Lawn Games
Plinths
Selfie Mirrors
Signs
Table Décor
Welcome Board & Stands

https://www.cherrihire.co.za/

https://backdropanddecorhub.co.za/
https://trendifygames.co.za/
https://thecandlemerchant.co.za/

Full Website Audit — GPL Events & Hire
🎨 Fonts & Colours (from base.css)
The core problem: you have two competing font systems.

base.css imports Faustina + Manrope and sets them as --ff-secondary and --ff-primary.
style.css imports Inter + Rubik and uses those in component-level styles.

So you're loading 4 font families but only consistently using 2. This wastes bandwidth and creates inconsistency.

My recommendation — drop Inter + Rubik entirely and lean into Faustina + Manrope:

Use	Font	Why
All headings (h1–h6, .event-type, .package-category h3)	Faustina (serif)	Elegant, editorial — perfect for a luxury event brand
All body text, descriptions, lists, nav	Manrope (sans-serif)	Clean, modern, highly readable at small sizes
Remove this line from style.css:1:


@import url('...Inter...Rubik...');
Colour application — you have beautiful variables going unused. You defined event-type-specific colours that are never applied:


--clr-wedding-rose: #f8bbd9;
--clr-corporate-steel: #607d8b;
--clr-party-purple: #9c27b0;
--clr-secondary-blush: #fce4ec;
--clr-secondary-cream: #fff8e1;
How to use them beautifully:

Section alternation — swap between white → --clr-secondary-blush → --clr-secondary-cream across page sections instead of the generic #f8f9ff
Card accent stripe — add a 4px left border on .service-card using category-specific colours:
Wedding cards → --clr-wedding-rose
Birthday cards → --clr-party-purple
Corporate cards → --clr-corporate-steel
Price badge — instead of always red, use the event-type colour per category
Section headers — use .title with a thin underline using --clr-accent-red for brand emphasis
⚠️ Technical (CSS/JS) Bugs
These are real bugs, not suggestions:

1. Broken CSS variables (base.css)
Three variables used but never defined:


--clr-secondary-orange  /* used in scrollbar */
--clr-primary           /* used in scrollbar + button hover */
--clr-accent            /* used in :focus outline */
Every :focus state and the scrollbar is currently broken because of this.

2. Single-colour gradients (style.css)
These lines do nothing — same colour both ends:


background: linear-gradient(135deg, var(--clr-accent-red), var(--clr-accent-red));
/* appears on .cta-primary, .step-number, .benefit-item i, .cta-quote */
Use var(--clr-accent-red) directly, or make the gradient meaningful: linear-gradient(135deg, var(--clr-primary-red), var(--clr-accent-red)).

3. Animation double-fire (style.css + script.js)
style.css:828 applies animation: fadeInUp statically on all .service-card elements.
script.js:86 then sets opacity: 0 on the same elements via IntersectionObserver.
These fight each other — cards flash invisible then animate twice. Remove the CSS fadeInUp animation and let the JS IntersectionObserver handle it exclusively.

4. Mobile padding override conflict (style.css:794)


@media (max-width: 480px) {
    .service-card { padding: 2rem 1.5rem; }
}
Cards now use .service-card-body for padding — this rule adds padding directly to the outer card instead, breaking the layout on small screens.

5. Duplicate .why-choose padding (style.css:261)


.why-choose {
    padding: 3rem 0;  /* immediately overridden */
    padding: 1rem;    /* this wins */
}
6. Global icon override (style.css:836)


.fas { color: var(--clr-secondary-cream) !important; }
This makes every Font Awesome icon cream-coloured globally, including nav icons, contact icons, and footer icons. Very hard to override anywhere. Scope this to specific contexts.

7. Form submits with alert() (script.js:62)
alert() is a terrible UX pattern — it blocks the page, looks like a browser warning, and can't be styled. Replace with an inline success message div.

🔍 SEO
Missing fundamentals:

No sitemap.xml — Google can't efficiently crawl your 11 pages
No robots.txt — search engines don't know your crawl rules
Schema markup only on index.html — the location pages (midrand.html, sandton.html, etc.) should each have their own LocalBusiness JSON-LD with that location's addressLocality
Page title issues:
Location pages likely have generic titles. Each should follow the pattern:


Event Planner in [Location] | GPL Events & Hire
Internal linking gaps:

Location pages don't link to each other — you're missing "hub and spoke" SEO
event-packages.html should link back to relevant location pages
Add breadcrumb navigation to all sub-pages
Image SEO:

The hero background is a CSS url() — Google cannot index CSS background images
All Cloudinary images should use Cloudinary's f_auto,q_auto transformations for automatic format/quality optimisation:

/image/upload/f_auto,q_auto/v1759646924/...
Missing <meta name="description"> audit — verify each location page has a unique description (not copied from index).

🖥️ UI/UX
1. No visual hierarchy between package tiers
Basic/Standard/Premium/Luxury cards look identical. Add a visual tier indicator — a subtle badge or a different .service-card-img gradient per tier level (e.g. darker/richer gradient = higher tier).

2. Price badge contrast
The red price badge on a white card works, but "Custom Pricing" and "Request a quote" don't feel premium — they look like missing data. Style these differently, e.g. a navy outline badge instead of a filled red one.

3. No sticky CTA on mobile
On mobile, users scroll through packages without seeing a contact option. A sticky bottom bar with "WhatsApp us" on mobile would significantly improve conversion.

4. The hero USP text is italic red on a dark overlay
font-style: italic; color: var(--clr-accent-red) on a black overlay can read poorly on some screens. Test contrast — red on dark backgrounds often fails WCAG AA.

5. Location pages feel thin
Each has 3 cards + a bullet list. No testimonials, no images, no map embed. These pages will struggle to rank and will feel like low-effort pages to visitors.

6. No "active" state on navigation
Current page has no visual indicator in the navbar. Add aria-current="page" + CSS styling.

7. WhatsApp button UX
The pre-filled WhatsApp messages are great. Consider also adding the WhatsApp icon (fa-whatsapp) to the button for instant recognition.

📦 Non-Technical
No photography on packages — the placeholder gradient cards feel incomplete. Even 3–5 hero-quality photos of real setups used across the package categories would dramatically increase perceived value and trust.

No pricing transparency page — clients want to know if they can afford you before they WhatsApp. A "from R2,500" summary table or FAQ section would reduce the friction before enquiry.

Testimonials not dated — add a month/year to each testimonial to show they're recent. Undated testimonials look old or fabricated.

No Google Maps embed — for a local service business, a map showing your service area on the contact section significantly improves local SEO and trust signals.

No social proof counter — a small line like "200+ events styled in Gauteng" near the hero CTA would boost conversion.

bespoke-gifting.html is disconnected — it has 15 gifting cards but no clear bridge to the events business. A "Add gifting to your event package" cross-sell section would tie it together and increase average order value.