// Enquiry list — lets visitors collect several hire items and packages (across
// pages) and send them in one pre-filled WhatsApp message. Loaded on hire.html,
// the hire category and item pages, event-packages.html and bespoke-gifting.html.
(function () {
  const STORAGE_KEY = "gplEnquiryList";
  const WHATSAPP = "https://wa.me/27649318467?text=";
  let memoryList = [];

  function load() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
      return memoryList;
    }
  }

  function save(list) {
    memoryList = list;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    } catch (e) {
      /* private mode / storage blocked — keep the list for this page only */
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }

  // Read name / option / price / link from a card or an item page
  function readItem(container) {
    const nameEl = container.querySelector(".hire-item-name") || container.querySelector(".pkg-name") || container.querySelector("h2");
    const link = container.querySelector(".hire-item-name a");
    const option = container.querySelector(".option-btn.active");
    const price = container.querySelector(".hire-item-price") || container.querySelector(".pkg-price");
    const name = nameEl.textContent.trim();
    const size = option ? option.dataset.size || option.textContent.trim() : "";
    return {
      id: name + (size ? " (" + size + ")" : ""),
      name: name,
      size: size,
      price: price ? price.textContent.replace(/\s+/g, " ").trim() : "",
      url: link ? link.getAttribute("href") : window.location.pathname,
    };
  }

  function has(id) {
    return load().some((item) => item.id === id);
  }

  function toggle(item) {
    let list = load();
    if (list.some((i) => i.id === item.id)) {
      list = list.filter((i) => i.id !== item.id);
    } else {
      list.push(item);
      if (typeof gtag === "function") gtag("event", "add_to_enquiry", { item_name: item.id });
    }
    save(list);
    refresh();
  }

  function remove(id) {
    save(load().filter((i) => i.id !== id));
    refresh();
  }

  function message(list) {
    const lines = list.map((i) => "• " + i.id + (i.price ? " — " + i.price : ""));
    return (
      "Hi GPL Events, I'd like to check availability for:\n" +
      lines.join("\n") +
      "\n\nEvent date: \nVenue / area: \nQuantities (if more than one): "
    );
  }

  // ----- Add buttons on cards / item page -----

  const containers = Array.from(document.querySelectorAll(".hire-item-card .hire-item-body, .hire-item-detail-info, .pkg-card .pkg-body"))
    .filter((el) => !el.closest('[style*="display:none"]'));

  containers.forEach((container) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "enquiry-add";
    const cta = container.querySelector(".cta-secondary") || container.querySelector(".pkg-cta");
    if (cta) cta.insertAdjacentElement("afterend", btn);
    else container.appendChild(btn);
    btn.addEventListener("click", () => toggle(readItem(container)));
    // Size buttons change the item id, so re-sync the label when they're clicked
    container.querySelectorAll(".option-btn").forEach((opt) => opt.addEventListener("click", () => setTimeout(refresh)));
  });

  // ----- Floating bar + panel -----

  const bar = document.createElement("div");
  bar.className = "enquiry-bar";
  bar.hidden = true;
  bar.innerHTML =
    '<div class="enquiry-panel" id="enquiryPanel" hidden>' +
    '<p class="enquiry-panel-title">Your enquiry list</p>' +
    '<ul class="enquiry-items"></ul>' +
    '<p class="enquiry-hint">We\'ll confirm availability, delivery and the final price on WhatsApp.</p>' +
    '<div class="enquiry-actions">' +
    '<a class="enquiry-send" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp" aria-hidden="true"></i> Send on WhatsApp</a>' +
    '<button type="button" class="enquiry-clear">Clear list</button>' +
    "</div></div>" +
    '<button type="button" class="enquiry-toggle" aria-expanded="false" aria-controls="enquiryPanel">' +
    '<span class="enquiry-count"></span><span class="enquiry-toggle-label">View &amp; send</span></button>';
  document.body.appendChild(bar);

  const panel = bar.querySelector(".enquiry-panel");
  const toggleBtn = bar.querySelector(".enquiry-toggle");
  const itemsEl = bar.querySelector(".enquiry-items");
  const sendLink = bar.querySelector(".enquiry-send");

  function setOpen(open) {
    panel.hidden = !open;
    toggleBtn.setAttribute("aria-expanded", String(open));
    bar.querySelector(".enquiry-toggle-label").textContent = open ? "Hide list" : "View & send";
  }

  toggleBtn.addEventListener("click", () => setOpen(panel.hidden));
  bar.querySelector(".enquiry-clear").addEventListener("click", () => {
    save([]);
    setOpen(false);
    refresh();
  });
  itemsEl.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-remove]");
    if (btn) remove(btn.dataset.remove);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden) setOpen(false);
  });

  function refresh() {
    const list = load();
    containers.forEach((container) => {
      const btn = container.querySelector(".enquiry-add");
      const added = has(readItem(container).id);
      btn.classList.toggle("is-added", added);
      btn.setAttribute("aria-pressed", String(added));
      // Short labels on the narrow category cards, fuller wording on item pages
      const short = !container.classList.contains("hire-item-detail-info");
      btn.innerHTML = added
        ? '<i class="fas fa-check" aria-hidden="true"></i> ' + (short ? "Added" : "Added to enquiry")
        : '<i class="fas fa-plus" aria-hidden="true"></i> ' + (short ? "Add to list" : "Add to enquiry list");
    });

    bar.hidden = list.length === 0;
    document.body.classList.toggle("has-enquiry", list.length > 0);
    if (!list.length) setOpen(false);
    bar.querySelector(".enquiry-count").textContent = list.length + (list.length === 1 ? " item" : " items") + " in your enquiry";
    itemsEl.innerHTML = list
      .map(
        (i) =>
          '<li><a href="' + escapeHtml(i.url) + '">' + escapeHtml(i.id) + "</a>" +
          (i.price ? '<span class="enquiry-price">' + escapeHtml(i.price) + "</span>" : "") +
          '<button type="button" class="enquiry-remove" data-remove="' + escapeHtml(i.id) + '" aria-label="Remove ' + escapeHtml(i.id) + '">&times;</button></li>'
      )
      .join("");
    sendLink.href = WHATSAPP + encodeURIComponent(message(list));
  }

  // Keep tabs in sync if the list changes in another tab
  window.addEventListener("storage", (e) => {
    if (e.key === STORAGE_KEY) refresh();
  });

  refresh();
})();
