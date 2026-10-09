// Homepage portfolio lightbox + reviews carousel dots
(function () {
  // ----- Portfolio lightbox -----
  const items = Array.from(document.querySelectorAll(".pf-item"));
  const box = document.querySelector(".pf-lightbox");

  if (items.length && box && typeof box.showModal === "function") {
    const img = box.querySelector("img");
    const caption = box.querySelector("figcaption");
    let current = 0;

    function show(index) {
      current = (index + items.length) % items.length;
      const src = items[current].querySelector("img");
      const tag = items[current].querySelector(".pf-tag").textContent;
      const event = items[current].querySelector(".pf-event").textContent;
      img.src = src.currentSrc || src.src;
      img.alt = src.alt;
      caption.textContent = tag + " — " + event + "  (" + (current + 1) + " / " + items.length + ")";
    }

    items.forEach((item, i) => {
      item.querySelector(".pf-open").addEventListener("click", () => {
        show(i);
        box.showModal();
      });
    });

    box.querySelector(".pf-lb-close").addEventListener("click", () => box.close());
    box.querySelector(".pf-lb-prev").addEventListener("click", () => show(current - 1));
    box.querySelector(".pf-lb-next").addEventListener("click", () => show(current + 1));

    // Click on the dark backdrop closes it
    box.addEventListener("click", (e) => {
      if (e.target === box) box.close();
    });

    box.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });

    // Return focus to the photo that opened the lightbox
    box.addEventListener("close", () => {
      const opener = items[current] && items[current].querySelector(".pf-open");
      if (opener) opener.focus();
    });
  }

  // ----- Reviews carousel dots (mobile) -----
  const track = document.querySelector(".rv-track");
  const dots = Array.from(document.querySelectorAll(".rv-dot"));
  if (!track || !dots.length) return;
  const cards = Array.from(track.querySelectorAll(".rv-card"));

  function activeIndex() {
    const left = track.scrollLeft;
    let best = 0;
    cards.forEach((card, i) => {
      if (Math.abs(card.offsetLeft - track.offsetLeft - left) < Math.abs(cards[best].offsetLeft - track.offsetLeft - left)) best = i;
    });
    return best;
  }

  track.addEventListener(
    "scroll",
    () => {
      const active = activeIndex();
      dots.forEach((dot, i) => dot.classList.toggle("is-active", i === active));
    },
    { passive: true }
  );

  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      track.scrollTo({ left: cards[i].offsetLeft - track.offsetLeft, behavior: "smooth" });
    });
  });
})();
