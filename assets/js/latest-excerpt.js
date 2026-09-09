// The first overview card is the source of truth for the latest excerpt.
(async () => {
  const link = document.querySelector('.reading-latest');
  if (!link) return;
  try {
    const response = await fetch('/zamysleni/', { cache: 'no-cache' });
    if (!response.ok) return;
    const overview = new DOMParser().parseFromString(await response.text(), 'text/html');
    const card = overview.querySelector('.reading-list .reading-card');
    const href = card?.querySelector('a')?.getAttribute('href');
    const title = card?.querySelector('h3')?.textContent.trim();
    if (!href || !title || !href.startsWith('/zamysleni/')) return;
    link.setAttribute('href', href);
    link.textContent = `${title} →`;
  } catch {
    // Keep the functional static link if the overview cannot be loaded.
  }
})();
