// Navigation

const menuBtn = document.querySelector(".menu");
const navList = document.querySelector(".nav-list");
const body = document.body;
let scrollPosition = 0; // Store the scroll position

menuBtn.addEventListener("click", () => {
  const isOpening = !menuBtn.classList.contains("active");
  if (isOpening) {
    // Menu is being opened
    scrollPosition = window.pageYOffset; // Store current scroll position
    body.style.top = `-${scrollPosition}px`; // Set body position
    body.classList.add("menu-open");
    menuBtn.setAttribute("aria-expanded", "true");
  } else {
    // Menu is being closed
    body.classList.remove("menu-open");
    body.style.top = "";
    window.scrollTo(0, scrollPosition); // Restore scroll position
    menuBtn.setAttribute("aria-expanded", "false");
  }
  menuBtn.classList.toggle("active");
  navList.classList.toggle("active");
});

// Close menu when clicking a link
const navLinks = document.querySelectorAll(".list-item a");
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    menuBtn.classList.remove("active");
    navList.classList.remove("active");
    body.classList.remove("menu-open");
    body.style.top = "";
    window.scrollTo(0, scrollPosition); // Restore scroll position
    menuBtn.setAttribute("aria-expanded", "false");
  });
});
