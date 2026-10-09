// Size option buttons — updates price and WhatsApp link on selection
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.option-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var container = this.closest('.hire-item-card') || this.closest('.hire-item-detail-info');
            if (!container) return;
            container.querySelectorAll('.option-btn').forEach(function (b) { b.classList.remove('active'); });
            this.classList.add('active');
            var priceEl = container.querySelector('.hire-item-price');
            if (priceEl && this.dataset.price) priceEl.textContent = this.dataset.price;
            var waLink = container.querySelector('.cta-secondary');
            if (waLink && this.dataset.size) {
                var nameEl = container.querySelector('.hire-item-name') || container.querySelector('h2');
                if (!nameEl) return;
                var name = nameEl.textContent.trim();
                var msg = "Hi, I'm interested in the " + name + " (" + this.dataset.size + "). Please confirm availability and pricing.";
                waLink.href = 'https://wa.me/27649318467?text=' + encodeURIComponent(msg);
            }
        });
    });
});

// Delivery info modal — hire category pages + individual item pages
document.addEventListener('DOMContentLoaded', function () {
    var hasCards  = document.querySelector('.hire-item-body');
    var hasDetail = document.querySelector('.hire-item-detail-info');
    if (!hasCards && !hasDetail) return;

    document.body.insertAdjacentHTML('beforeend',
        '<div class="delivery-modal-overlay" id="deliveryModal" role="dialog" aria-modal="true">' +
            '<div class="delivery-modal">' +
                '<button class="delivery-modal-close" aria-label="Close">&times;</button>' +
                '<h3>Delivery &amp; Collection</h3>' +
                '<p>Delivery and collection are quoted separately based on your location. ' +
                'You\'re also welcome to collect your order from our warehouse free of charge — ' +
                'by appointment only. Simply select your preferred option when requesting your quote.</p>' +
            '</div>' +
        '</div>'
    );

    var overlay = document.getElementById('deliveryModal');

    document.querySelectorAll('.hire-item-body').forEach(function (body) {
        var btn = document.createElement('button');
        btn.className = 'delivery-info-trigger';
        btn.textContent = 'Delivery & collection info';
        body.appendChild(btn);
    });

    document.querySelectorAll('.hire-item-detail-info').forEach(function (info) {
        var backLink = info.querySelector('.hire-item-detail-back');
        var btn = document.createElement('button');
        btn.className = 'delivery-info-trigger';
        btn.textContent = 'Delivery & collection info';
        if (backLink) {
            info.insertBefore(btn, backLink);
        } else {
            info.appendChild(btn);
        }
    });

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('delivery-info-trigger')) {
            overlay.classList.add('active');
        }
    });

    overlay.querySelector('.delivery-modal-close').addEventListener('click', function () {
        overlay.classList.remove('active');
    });

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) overlay.classList.remove('active');
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') overlay.classList.remove('active');
    });
});

document.addEventListener("DOMContentLoaded", function () {
  const track = document.querySelector(".testimonial-track");
  const container = document.querySelector(".testimonial-container");
  const images = Array.from(track.children);

  // Duplicate images for seamless scroll
  images.forEach((img) => {
    const clone = img.cloneNode(true);
    track.appendChild(clone);
  });

  let scrollAmount = 0;
  const speed = 1; // pixels per frame, adjust for speed

  function animate() {
    scrollAmount += speed;
    if (scrollAmount >= track.scrollWidth / 2) {
      scrollAmount = 0;
    }
    track.style.transform = `translateX(-${scrollAmount}px)`;
    requestAnimationFrame(animate);
  }

  animate();
});
