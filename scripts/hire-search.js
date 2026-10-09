// Hire search — filters hire-items.json (built by tools/build-hire-items.py)
(function () {
  const input = document.getElementById("hire-search-input");
  const results = document.getElementById("hire-search-results");
  const status = document.getElementById("hire-search-status");
  if (!input || !results || !status) return;

  const WHATSAPP = "https://wa.me/27649318467?text=";
  let items = null;
  let loading = null;
  let trackTimer = null;

  // Lowercase, strip accents (décor -> decor), "&" -> "and", drop punctuation
  function normalise(str) {
    return str
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  // Treat "glasses"/"glass" and "chairs"/"chair" as the same word
  function stem(word) {
    if (word.length > 4 && word.endsWith("es")) return word.slice(0, -2);
    if (word.length > 3 && word.endsWith("s")) return word.slice(0, -1);
    return word;
  }

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }

  function loadItems() {
    if (!loading) {
      loading = fetch("/hire-items.json")
        .then((res) => res.json())
        .then((data) => {
          items = data.map((item) => ({
            ...item,
            nameWords: normalise(item.name).split(" ").map(stem),
            words: normalise(item.name + " " + item.category).split(" ").map(stem),
          }));
        })
        .catch(() => {
          items = [];
        });
    }
    return loading;
  }

  // Items whose own name matches come first, then other items in a matching
  // category (so "glasses" lists the glasses before the rest of Crockery & Glassware)
  function search(query) {
    const terms = normalise(query).split(" ").filter(Boolean).map(stem);
    if (!terms.length) return [];
    const matchesAll = (words) => terms.every((term) => words.some((word) => word.startsWith(term)));
    const byName = items.filter((item) => matchesAll(item.nameWords));
    const byCategory = items.filter((item) => !byName.includes(item) && matchesAll(item.words));
    return byName.concat(byCategory);
  }

  function render(query) {
    const q = query.trim();
    if (!q) {
      results.hidden = true;
      results.innerHTML = "";
      status.textContent = "";
      return;
    }
    const matches = search(q);
    results.hidden = false;
    if (!matches.length) {
      const wa = WHATSAPP + encodeURIComponent(`Hi GPL Events, I'm looking for "${q}" to hire. Do you have something similar?`);
      status.textContent = `No items found for "${q}".`;
      results.innerHTML =
        `<p class="hire-search-empty">Can't find it? <a href="${wa}" target="_blank" rel="noopener noreferrer">Ask us on WhatsApp</a> — we may have something similar.</p>`;
      return;
    }
    status.textContent = `${matches.length} item${matches.length === 1 ? "" : "s"} found`;
    results.innerHTML = matches
      .map((item) => {
        const href = "/" + (item.itemUrl || item.categoryUrl);
        const img = item.image
          ? `<img src="/${item.image}" alt="" loading="lazy" width="80" height="80">`
          : `<span class="hire-search-noimg" aria-hidden="true"><i class="fas fa-image"></i></span>`;
        return `<a class="hire-search-card" href="${href}">
            ${img}
            <span class="hire-search-info">
              <span class="hire-search-name">${escapeHtml(item.name)}</span>
              <span class="hire-search-cat">${escapeHtml(item.category)}</span>
              ${item.price ? `<span class="hire-search-price">${escapeHtml(item.price)}</span>` : ""}
            </span>
          </a>`;
      })
      .join("");
  }

  function track(query) {
    clearTimeout(trackTimer);
    if (typeof gtag !== "function" || !query.trim()) return;
    trackTimer = setTimeout(() => gtag("event", "search", { search_term: query.trim() }), 1200);
  }

  input.addEventListener("focus", loadItems, { once: true });
  input.addEventListener("input", () => {
    const query = input.value;
    loadItems().then(() => render(query));
    track(query);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      input.value = "";
      render("");
    }
  });

  // Support links like hire.html?q=arch
  const initial = new URLSearchParams(window.location.search).get("q");
  if (initial) {
    input.value = initial;
    loadItems().then(() => render(initial));
  }
})();
