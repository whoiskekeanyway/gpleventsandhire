# Hidden Items & Categories

Everything hidden with `style="display:none"` — ready to re-enable when needed.

---

## Hub Tiles (`hire.html`)

| Category | Line (approx) | Notes |
|---|---|---|
| Accessories | ~178 | Merged into Table Décor & Accessories |
| Easels | ~238 | Merged into Welcome Boards & Easels |
| Selfie Mirrors | ~308 | Coming soon |
| Signs | ~318 | Coming soon — category + 3 item pages also noindexed (see table below) |
| Plinths | ~298 | Merged into Stands & Plinths (flower-stands.html) |

---

## Hire Category Items

### `hire/arches.html`

| Item | Line (approx) | Price (when re-enabled) |
|---|---|---|
| Hexagonal Arch | ~227 | R550 – R950 |

### `hire/drinks-boards.html`

| Item | Line (approx) | Price (when re-enabled) |
|---|---|---|
| Acrylic Drinks Board | ~175 | R350 – R600 |
| Mirror Drinks Board | ~188 | R450 – R750 |
| Printed Foam Board Drinks Menu | ~201 | R250 – R450 |

### `hire/furniture.html`

| Item | Line (approx) |
|---|---|
| Throne Chair (pair) | ~266 |
| Sweetheart Table | ~279 |
| Ghost Chairs (set of 4) | ~292 |
| Cocktail Table | ~305 |
| Stanchion Rope Set (Black) | ~335 |
| Stanchion Rope Set (Silver) | ~350 |

### `hire/backdrops.html`

| Item | Line (approx) |
|---|---|
| Draped Fabric Backdrop | ~201 |
| Shimmer Sequin Backdrop | ~229 |
| Flower Backdrop | ~271 |

### `hire/flower-stands.html`

| Item | Line (approx) | Price (when re-enabled) |
|---|---|---|
| Mirror Plinth | ~275 | R400 – R700 |
| Round Cake Stand | ~289 | R150 – R280 |
| Tiered Cupcake Stand (3-tier) | ~301 | R200 – R350 |
| Acrylic Cake Stand | ~313 | R180 – R300 |

### `hire/welcome-board-stands.html`

| Item | Line (approx) |
|---|---|
| Acrylic Welcome Board | ~201 |
| Mirror Welcome Board | ~229 |
| Chrome Display Easel | ~288 |

### `hire/lawn-games.html`

| Item | Line (approx) | Notes |
|---|---|---|
| Cornhole Board Set | ~201 | Temporarily hidden |
| Ring Toss Game | ~214 | Temporarily hidden |

---

## Hidden from Google (noindex + removed from sitemap)

Pages that still exist but are kept out of search until the item is in stock.

| Page | Reason | To re-enable |
|---|---|---|
| `hire/selfie-mirrors.html` | No selfie mirror in stock yet (2026-10-09) | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide hub tile in `hire.html` |
| `hire/items/led-selfie-mirror-station.html` | Same | Change robots meta to `index, follow`, add back to `sitemap.xml` |
| `hire/items/magic-mirror-photo-booth.html` | Same | Change robots meta to `index, follow`, add back to `sitemap.xml` |
| `hire/items/throne-chair.html` | Hidden by owner 2026-10-09 (hired as a pair only) | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `furniture.html`, add back to furniture ItemList schema + hero copy |
| `hire/items/shot-glasses.html` | Hidden by owner 2026-10-09 (no per-item price; no card on crockery page) | Set per-item price, change robots meta to `index, follow`, add back to `sitemap.xml`, add a card to `crockery.html` |
| `hire/signs.html` | Hidden by owner 2026-10-09 (Signs category not offered yet — hub tile hidden) | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide tile in `hire.html` |
| `hire/items/custom-neon-led-sign.html` | Hidden by owner 2026-10-09 (Signs not offered yet) | Change robots meta to `index, follow`, add back to `sitemap.xml` |
| `hire/items/directional-signs-set.html` | Hidden by owner 2026-10-09 (Signs not offered yet) | Change robots meta to `index, follow`, add back to `sitemap.xml` |
| `hire/items/acrylic-table-number-signs.html` | Hidden by owner 2026-10-09 (Signs not offered yet) | Change robots meta to `index, follow`, add back to `sitemap.xml` |
| `hire/items/modern-digital-guestbook-station.html` | Hidden by owner 2026-10-09 (Not in stock — Audio Guestbook category is live with the retro phone only) | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/audio-guestbook-sets.html` |
| `hire/items/sweetheart-table.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/furniture.html`, add back to furniture hero copy |
| `hire/items/ghost-chairs.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/furniture.html`, add back to furniture hero copy |
| `hire/items/cocktail-table.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/furniture.html`, add back to furniture hero copy |
| `hire/items/cornhole-board-set.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/lawn-games.html`, add back to lawn-games hero copy |
| `hire/items/ring-toss-game.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `hire/lawn-games.html`, add back to lawn-games hero copy |
| `hire/items/white-champagne-board.html` | Hidden by owner 2026-10-09 | Change robots meta to `index, follow`, add back to `sitemap.xml`, un-hide card in `— (no card exists; add one to `hire/drinks-boards.html`)` |

---

## Notes

- `hire/easels.html` still exists but its hub tile is hidden — the page content was merged into `welcome-board-stands.html`
- `hire/accessories.html` still exists but its hub tile is hidden — items were merged into `table-decor.html`
- `hire/plinths.html` still exists but its hub tile is hidden — items were merged into `flower-stands.html` (now "Stands & Plinths")
- To re-enable any item or tile: remove `style="display:none"` from the relevant `<div>` tag
- `accessories.html`, `easels.html`, `plinths.html` are also 301-redirected in `_redirects` (added 2026-10-09). To re-enable one, delete its lines from `_redirects` and add it back to `sitemap.xml`
- Category-page Google product lists (ItemList schema) are rebuilt from **visible** cards only — after un-hiding a card, re-add it to that page's ItemList too.
- After hiding or un-hiding anything, re-run `python3 tools/build-hire-items.py` so the hire search (hire.html) stays in sync.
