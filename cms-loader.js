/* Decap CMS content loader.
   Static HTML remains the SEO/no-JavaScript fallback. The build step also writes SEO
   metadata and generated CMS pages before deployment. */
(async function () {
  const setText = (selector, value) => {
    const node = document.querySelector(selector);
    if (node && typeof value === 'string' && value.trim()) node.textContent = value;
  };
  const setMeta = (selector, value) => {
    const node = document.querySelector(selector);
    if (node && typeof value === 'string' && value.trim()) node.setAttribute('content', value);
  };
  const readJson = async (path) => {
    const response = await fetch(path, { cache: 'no-cache' });
    if (!response.ok) throw new Error('Unable to load ' + path);
    return response.json();
  };

  if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
  try {
    const data = await readJson('/cms/homepage.json');
    if (data.seo_title) {
      document.title = data.seo_title;
      setMeta('meta[property="og:title"]', data.seo_title);
      setMeta('meta[name="twitter:title"]', data.seo_title);
    }
    if (data.seo_description) {
      setMeta('meta[name="description"]', data.seo_description);
      setMeta('meta[property="og:description"]', data.seo_description);
      setMeta('meta[name="twitter:description"]', data.seo_description);
    }
    setText('.hero .eyebrow', data.hero_eyebrow);
    setText('.hero .hero-desc', data.hero_description);
    setText('.about-copy .eyebrow', data.about_eyebrow);
    const aboutParagraphs = document.querySelectorAll('.about-copy p');
    if (aboutParagraphs[0] && data.about_paragraph_1) aboutParagraphs[0].textContent = data.about_paragraph_1;
    if (aboutParagraphs[1] && data.about_paragraph_2) aboutParagraphs[1].textContent = data.about_paragraph_2;
    if (data.profile_image) {
      const portrait = [...document.querySelectorAll('img')].find(img => /Afzal, digital marketing professional/i.test(img.alt || ''));
      if (portrait) portrait.src = data.profile_image;
    }
  } catch (error) {
    console.warn('Homepage CMS content could not be loaded; showing the static HTML fallback.', error);
  }
  }

  try {
    const settings = await readJson('/cms/global-settings.json');
    const root = document.documentElement;
    const design = settings.design || {};
    const cssVars = {
      background: '--ink',
      panel: '--ink2',
      text: '--paper',
      muted: '--muted',
      accent: '--orange',
      border: '--line',
      heading_font: '--serif',
      body_font: '--sans',
      content_width: '--max'
    };
    Object.entries(cssVars).forEach(([key, variable]) => {
      if (typeof design[key] === 'string' && design[key].trim()) root.style.setProperty(variable, design[key]);
    });
    const aliases = { background: '--bg', panel: '--panel', text: '--text', muted: '--muted', accent: '--orange', border: '--line', heading_font: '--serif', body_font: '--sans', content_width: '--max' };
    Object.entries(aliases).forEach(([key, variable]) => {
      if (typeof design[key] === 'string' && design[key].trim()) root.style.setProperty(variable, design[key]);
    });
    if (design.corner_radius) root.style.setProperty('--cms-radius', design.corner_radius);

    if (settings.brand) {
      setText('.brand-copy strong', settings.brand.name);
      setText('.brand-copy small', settings.brand.subtitle);
      setText('.brand small', settings.brand.subtitle);
      const monogram = document.querySelector('.brand .monogram');
      if (monogram && settings.brand.logo) {
        const logo = document.createElement('img');
        logo.src = settings.brand.logo;
        logo.alt = settings.brand.name || 'Brand';
        logo.style.cssText = 'width:100%;height:100%;object-fit:cover;border-radius:50%;display:block';
        monogram.replaceChildren(logo);
      } else if (monogram) { monogram.textContent = settings.brand.monogram || 'MA'; }
    }
    if (Array.isArray(settings.navigation) && settings.navigation.length) {
      const nav = document.querySelector('#navlinks') || document.querySelector('header nav');
      if (nav) {
        nav.replaceChildren();
        settings.navigation.forEach(item => {
          if (!item || !item.label || !item.url) return;
          const link = document.createElement('a');
          link.href = (window.location.pathname !== '/' && item.url.startsWith('#')) ? '/' + item.url : item.url;
          link.textContent = item.label;
          if (item.highlight) link.className = 'navcta';
          nav.appendChild(link);
          link.addEventListener('click', () => {
            nav.classList.remove('open');
            const menu = document.getElementById('menu');
            if (menu) { menu.setAttribute('aria-expanded', 'false'); menu.textContent = 'Menu +'; }
          });
        });
      }
    }
    if (settings.footer) {
      const copyright = document.querySelector('.footer-inner > span:first-child');
      if (copyright && settings.footer.copyright) copyright.textContent = settings.footer.copyright;
      const footerLinks = document.querySelector('.footer-inner > span:last-child');
      if (footerLinks && Array.isArray(settings.footer.links)) {
        footerLinks.replaceChildren();
        settings.footer.links.forEach((item, index) => {
          if (!item || !item.label || !item.url) return;
          if (index) footerLinks.append(' · ');
          const link = document.createElement('a');
          link.href = (window.location.pathname !== '/' && item.url.startsWith('#')) ? '/' + item.url : item.url;
          link.textContent = item.label;
          footerLinks.appendChild(link);
        });
      }
    }
    const contact = settings.contact || {};
    if (contact.whatsapp_url) {
      const wa = document.querySelector('.hero-whatsapp');
      if (wa) wa.href = contact.whatsapp_url;
    }
    if (contact.linkedin_url) {
      document.querySelectorAll('a[href*="linkedin.com"]').forEach(a => a.href = contact.linkedin_url);
    }
    if (contact.instagram_url) {
      document.querySelectorAll('a[href*="instagram.com"]').forEach(a => a.href = contact.instagram_url);
    }
    if (contact.email) {
      document.querySelectorAll('a[href^="mailto:"]').forEach(a => a.href = 'mailto:' + contact.email);
    }
    if (contact.phone) {
      document.querySelectorAll('a[href^="tel:"]').forEach(a => a.href = 'tel:' + contact.phone.replace(/[^+0-9]/g, ''));
    }
  } catch (error) {
    // Global settings are optional until the corresponding CMS entry is published.
    console.info('Global CMS settings are not available; using the portfolio defaults.');
  }
})();
