(() => {
  const form = document.getElementById('downloadForm');
  const input = document.getElementById('mediaUrl');
  const message = document.getElementById('formMessage');
  const toast = document.getElementById('toast');
  const toggle = document.getElementById('menuToggle');
  const nav = document.querySelector('.desktop-nav');
  document.getElementById('year').textContent = new Date().getFullYear();

  let toastTimer;
  function showToast(text) {
    toast.textContent = text;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
  }
  function setMessage(text, type = '') {
    message.textContent = text;
    message.className = 'form-message' + (type ? ' ' + type : '');
  }
  const domains = {
    Instagram: ['instagram.com', 'instagr.am'],
    Facebook: ['facebook.com', 'fb.watch', 'm.facebook.com'],
    TikTok: ['tiktok.com', 'vm.tiktok.com'],
    YouTube: ['youtube.com', 'youtu.be']
  };
  document.querySelectorAll('.quick-platforms button').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.quick-platforms button').forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      input.focus();
      const platform = button.dataset.platform;
      input.placeholder = platform === 'Other'
        ? 'Paste a supported public media link…'
        : 'Paste a public ' + platform + ' link here…';
    });
  });
  document.querySelectorAll('[data-fill]').forEach(card => {
    card.addEventListener('click', () => {
      const platform = card.dataset.fill;
      document.querySelectorAll('.quick-platforms button').forEach(b => {
        b.classList.toggle('active', b.dataset.platform === platform);
      });
      input.placeholder = 'Paste a public ' + platform + ' link here…';
      setTimeout(() => input.focus({preventScroll: true}), 250);
    });
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const raw = input.value.trim();
    let url;
    try {
      url = new URL(raw);
      if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Only HTTP(S) links are supported.');
    } catch {
      setMessage('Please enter a valid link beginning with https:// or http://.', 'error');
      input.focus();
      return;
    }
    const hostname = url.hostname.toLowerCase().replace(/^www\./, '');
    const platform = Object.entries(domains).find(([, list]) => list.some(domain => hostname === domain || hostname.endsWith('.' + domain)));
    if (!platform) {
      setMessage('This link may be unsupported. Try a public Instagram, Facebook, TikTok or YouTube post.', 'error');
      return;
    }
    const apiEndpoint = document.querySelector('meta[name="social-save-api"]')?.content?.trim();
    if (!apiEndpoint) {
      setMessage('Link checked: ' + platform[0] + '. The downloader API is not configured yet, so this demo cannot fetch media or produce a download file. Add your authorized backend endpoint to enable processing.', 'success');
      showToast('Link validated. Configure the media API to enable downloads.');
      return;
    }
    const submit = form.querySelector('button[type="submit"]');
    const original = submit.innerHTML;
    submit.disabled = true;
    submit.innerHTML = 'Checking… <span>↻</span>';
    setMessage('Checking the public link with the configured service…');
    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url.href})
      });
      if (!response.ok) throw new Error('Service returned ' + response.status);
      const result = await response.json();
      if (!result || !Array.isArray(result.medias) || result.medias.length === 0) {
        throw new Error(result?.message || 'No downloadable media was returned for this link.');
      }
      message.replaceChildren();
      setMessage('Media found. Choose a format below.', 'success');
      const options = document.createElement('div');
      options.className = 'media-options';
      options.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 12px';
      result.medias.forEach((media, index) => {
        if (!media || typeof media.url !== 'string') return;
        let safeUrl;
        try {
          safeUrl = new URL(media.url);
          if (!['https:', 'http:'].includes(safeUrl.protocol)) return;
        } catch { return; }
        const link = document.createElement('a');
        link.className = 'button button-dark';
        link.href = safeUrl.href;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = [media.quality || media.type || 'Download', media.extension ? '(' + media.extension + ')' : ''].filter(Boolean).join(' ');
        options.appendChild(link);
      });
      if (options.children.length) message.after(options);
      else throw new Error('The API response did not include any safe media URLs.');
    } catch (error) {
      setMessage('Could not process this link. ' + (error?.message || 'Please try again later.'), 'error');
    } finally {
      submit.disabled = false;
      submit.innerHTML = original;
    }
  });
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }));
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
      if (id === '#contact') showToast('Contact page content still needs to be configured.');
      if (id === '#privacy') showToast('Add a project-specific privacy policy before launch.');
      if (id === '#terms') showToast('Add project-specific terms before launch.');
    });
  });
})();