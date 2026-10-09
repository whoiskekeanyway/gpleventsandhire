// Smooth scrolling functions
function scrollToContact() {
  document.getElementById("contact").scrollIntoView({
    behavior: "smooth",
  });
}

function scrollToForm() {
  const form = document.getElementById("contact-form");
  if (form) {
    form.scrollIntoView({ behavior: "smooth" });
  } else {
    window.location.href = "/contact.html";
  }
}

// Form submission handler
function showFormMessage(form, message, type) {
  let msg = form.querySelector(".form-inline-msg");
  if (!msg) {
    msg = document.createElement("div");
    msg.className = "form-inline-msg";
    form.appendChild(msg);
  }
  msg.textContent = message;
  msg.style.cssText = [
    "padding: 0.9rem 1.2rem",
    "border-radius: 10px",
    "font-size: 0.95rem",
    "font-weight: 500",
    "margin-top: 1rem",
    "text-align: center",
    type === "success"
      ? "background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7;"
      : "background: #fdecea; color: #c62828; border: 1px solid #ef9a9a;",
  ].join(";");
  msg.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);

  if (
    !data.firstName ||
    !data.lastName ||
    !data.email ||
    !data.phone ||
    !data.eventType ||
    !data.eventDate ||
    !data.guestCount ||
    !data.location
  ) {
    showFormMessage(form, "Please fill in all required fields.", "error");
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(data.email)) {
    showFormMessage(form, "Please enter a valid email address.", "error");
    return;
  }

  const phoneRegex = /^[\+]?[0-9\s\-\(\)]+$/;
  if (!phoneRegex.test(data.phone)) {
    showFormMessage(form, "Please enter a valid phone number.", "error");
    return;
  }

  const selectedDate = new Date(data.eventDate);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  if (selectedDate < today) {
    showFormMessage(form, "Please select a future date for your event.", "error");
    return;
  }

  showFormMessage(
    form,
    "Thank you! We'll be in touch within 24 hours with your personalised quote.",
    "success"
  );
  form.reset();
}

// Header scroll effect
function handleScroll() {
  const header = document.querySelector(".header");
  if (!header) return;
  if (window.scrollY > 100) {
    header.style.background = "rgba(255, 255, 255, 0.98)";
    header.style.boxShadow = "0 2px 30px rgba(0, 0, 0, 0.15)";
  } else {
    header.style.background = "rgba(255, 255, 255, 0.95)";
    header.style.boxShadow = "0 2px 20px rgba(0, 0, 0, 0.1)";
  }
}

// Intersection Observer for animations
function setupAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe elements for animation
  const animatedElements = document.querySelectorAll(
    ".service-card, .step, .testimonial-card, .area-card, .benefit-item"
  );
  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "all 0.6s ease-out";
    observer.observe(el);
  });
}

// Phone number formatting
function formatPhoneNumber(input) {
  let value = input.value.replace(/\D/g, "");

  if (value.startsWith("27")) {
    value = "+" + value;
  } else if (value.startsWith("0")) {
    value = "+27" + value.substring(1);
  } else if (!value.startsWith("+")) {
    value = "+27" + value;
  }

  input.value = value;
}

// Testimonial carousel dot indicators
function setupTestimonialCarousel() {
  const grid = document.querySelector(".testimonials-grid");
  const dots = document.querySelectorAll(".dot");
  if (!grid || !dots.length) return;

  function updateDots() {
    const cards = grid.querySelectorAll(".testimonial-card");
    if (!cards.length) return;
    const cardWidth = cards[0].offsetWidth;
    const gap = 16; // matches 1rem gap
    const active = Math.min(
      Math.round(grid.scrollLeft / (cardWidth + gap)),
      dots.length - 1
    );
    dots.forEach((dot, i) => dot.classList.toggle("dot--active", i === active));
  }

  // Update dots while scrolling
  grid.addEventListener("scroll", updateDots, { passive: true });

  // Click a dot to scroll to that card
  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      const cards = grid.querySelectorAll(".testimonial-card");
      const cardWidth = cards[0]?.offsetWidth || 0;
      const gap = 16;
      grid.scrollTo({ left: i * (cardWidth + gap), behavior: "smooth" });
    });
  });
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Setup scroll listener
  window.addEventListener("scroll", handleScroll);

  // Setup animations
  setupAnimations();

  // Setup testimonial carousel
  setupTestimonialCarousel();

  // Setup phone formatting
  const phoneInput = document.querySelector('input[name="phone"]');
  if (phoneInput) {
    phoneInput.addEventListener("blur", function () {
      formatPhoneNumber(this);
    });
  }

  // Setup date input minimum date
  const dateInput = document.querySelector('input[name="eventDate"]');
  if (dateInput) {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    dateInput.min = tomorrow.toISOString().split("T")[0];
  }
});


