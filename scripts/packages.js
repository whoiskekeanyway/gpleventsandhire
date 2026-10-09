// Package pages — category tabs, "help me choose" and mobile card centring
(function () {
  const page = document.querySelector(".pkg-page");
  if (!page) return;

  const tabs = Array.from(page.querySelectorAll(".pkg-tab"));
  const panels = Array.from(page.querySelectorAll(".pkg-category"));
  const isMobile = () => window.matchMedia("(max-width: 680px)").matches;

  // On phones, start each swipe row on the "Most popular" card
  function centrePopular(panel) {
    if (!isMobile()) return;
    const row = panel.querySelector(".pkg-cards");
    const popular = row && row.querySelector(".is-popular");
    if (!row || !popular) return;
    row.scrollLeft = popular.offsetLeft - row.offsetLeft - (row.clientWidth - popular.offsetWidth) / 2;
  }

  function activate(id, updateHash) {
    const panel = panels.find((p) => p.id === id) || panels[0];
    panels.forEach((p) => p.classList.toggle("is-active", p === panel));
    tabs.forEach((t) => t.setAttribute("aria-current", String(t.dataset.tab === panel.id)));
    // Keep the active chip visible in the horizontally scrolling tab row (phones)
    const activeTab = tabs.find((t) => t.dataset.tab === panel.id);
    const row = activeTab && activeTab.parentElement;
    if (row && row.scrollWidth > row.clientWidth) {
      row.scrollLeft = activeTab.offsetLeft - row.offsetLeft - (row.clientWidth - activeTab.offsetWidth) / 2;
    }
    if (updateHash) history.replaceState(null, "", "#" + panel.id);
    centrePopular(panel);
    return panel;
  }

  if (tabs.length && panels.length) {
    page.classList.add("tabs-ready");
    const fromHash = window.location.hash.slice(1);
    activate(panels.some((p) => p.id === fromHash) ? fromHash : panels[0].id, false);

    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        e.preventDefault();
        activate(tab.dataset.tab, true);
      });
    });

    // Links elsewhere on the page that point at a category (e.g. #wedding)
    window.addEventListener("hashchange", () => {
      const id = window.location.hash.slice(1);
      if (panels.some((p) => p.id === id)) activate(id, false);
    });
  }

  // ----- Help me choose -----
  const form = page.querySelector(".pkg-chooser-form");
  const result = page.querySelector(".pkg-chooser-result");
  if (!form || !result) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const category = form.elements.event.value;
    const guests = parseInt(form.elements.guests.value, 10);
    const panel = activate(category, true);
    const cards = Array.from(panel.querySelectorAll(".pkg-card"));
    const pick = cards.find((c) => parseInt(c.dataset.guestsMax, 10) >= guests) || cards[cards.length - 1];

    cards.forEach((c) => c.classList.toggle("is-highlight", c === pick));
    const name = pick.querySelector(".pkg-name").textContent;
    const price = pick.querySelector(".pkg-price").textContent.replace(/\s+/g, " ").trim();
    const guide = pick.querySelector(".pkg-guests");
    const wa = pick.querySelector(".pkg-cta").getAttribute("href");

    result.hidden = false;
    result.innerHTML =
      "<p>We recommend the <strong>" + name + "</strong> — " + price +
      (guide ? " (" + guide.textContent.trim().toLowerCase() + ")" : "") + ".</p>" +
      '<div class="pkg-result-actions">' +
      '<a class="pkg-result-view" href="#' + panel.id + '">See the package</a>' +
      '<a class="pkg-cta" href="' + wa + '" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Request it on WhatsApp</a>' +
      "</div>";

    result.querySelector(".pkg-result-view").addEventListener("click", (ev) => {
      ev.preventDefault();
      pick.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
    });
  });
})();
