/* Pages CMS homepage content loader.
   The original HTML remains the no-JavaScript fallback and keeps the existing design. */
(async function () {
  try {
    const response = await fetch('/cms/homepage.json', { cache: 'no-cache' });
    if (!response.ok) return;
    const data = await response.json();

    const setText = (selector, value) => {
      const node = document.querySelector(selector);
      if (node && typeof value === 'string' && value.trim()) {
        node.textContent = value;
      }
    };

    if (typeof data.seo_title === 'string' && data.seo_title.trim()) {
      document.title = data.seo_title;
      document.querySelector('meta[property="og:title"]')
        ?.setAttribute('content', data.seo_title);
    }
    if (typeof data.seo_description === 'string' && data.seo_description.trim()) {
      document.querySelector('meta[name="description"]')
        ?.setAttribute('content', data.seo_description);
      document.querySelector('meta[property="og:description"]')
        ?.setAttribute('content', data.seo_description);
    }

    setText('.hero .eyebrow', data.hero_eyebrow);
    setText('.hero .hero-desc', data.hero_description);
    setText('.about-copy .eyebrow', data.about_eyebrow);

    const aboutParagraphs = document.querySelectorAll('.about-copy p');
    if (aboutParagraphs[0] && typeof data.about_paragraph_1 === 'string' && data.about_paragraph_1.trim()) {
      aboutParagraphs[0].textContent = data.about_paragraph_1;
    }
    if (aboutParagraphs[1] && typeof data.about_paragraph_2 === 'string' && data.about_paragraph_2.trim()) {
      aboutParagraphs[1].textContent = data.about_paragraph_2;
    }
  } catch (error) {
    console.warn('Pages CMS content could not be loaded; showing the static homepage.', error);
  }
})();
