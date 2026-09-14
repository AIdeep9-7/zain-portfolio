const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#site-nav');

const syncHeader = () => {
  header.classList.toggle('scrolled', window.scrollY > 24);
};
syncHeader();
window.addEventListener('scroll', syncHeader, { passive: true });

// Match the reference's light navigation treatment while the cream sections are visible.
const lightSections = document.querySelectorAll('.section-cream, .section-cream-alt');
if ('IntersectionObserver' in window) {
  const lightObserver = new IntersectionObserver((entries) => {
    const showLightHeader = entries.some((entry) => entry.isIntersecting && entry.intersectionRatio > 0.12);
    header.classList.toggle('on-light', showLightHeader);
  }, { rootMargin: '-18% 0px -58% 0px', threshold: [0, 0.12, 0.4] });
  lightSections.forEach((section) => lightObserver.observe(section));
}

menuToggle?.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!open));
  nav.classList.toggle('open', !open);
});

nav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle?.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
  });
});

// Close the mobile menu when the user taps outside it.
document.addEventListener('click', (event) => {
  if (!nav?.classList.contains('open')) return;
  if (!nav.contains(event.target) && !menuToggle.contains(event.target)) {
    nav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
  }
});
