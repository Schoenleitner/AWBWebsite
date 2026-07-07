/* Attergauer Wohnbau — Main JS */

document.addEventListener('DOMContentLoaded', () => {

  /* --- Hero Slider --- */
  const slides = document.querySelectorAll('.hero-slide');
  if (slides.length > 1) {
    let current = 0;
    setInterval(() => {
      slides[current].classList.remove('active');
      current = (current + 1) % slides.length;
      slides[current].classList.add('active');
    }, 5000);
  }

  /* --- Mobile Nav Toggle --- */
  const toggle = document.querySelector('.navbar-toggle');
  const menu = document.querySelector('.navbar-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', () => menu.classList.toggle('open'));

    // Dropdown on mobile: tap to open
    document.querySelectorAll('.nav-dropdown > a').forEach(link => {
      link.addEventListener('click', e => {
        if (window.innerWidth < 700) {
          e.preventDefault();
          link.parentElement.classList.toggle('open');
        }
      });
    });

    // Menü schließen wenn ein normaler Link geklickt wird (inkl. Hash-Links wie #kontakt)
    menu.querySelectorAll('a:not(.nav-dropdown > a)').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('open');
      });
    });
  }

  /* --- Active nav link --- */
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-menu a').forEach(a => {
    if (a.getAttribute('href') && path.includes(a.getAttribute('href')) && a.getAttribute('href') !== '/') {
      a.classList.add('active');
    }
    if (path === '/' && a.getAttribute('href') === '/') {
      a.classList.add('active');
    }
  });

  /* --- Lightbox --- */
  const lightbox = document.getElementById('lightbox');
  if (lightbox) {
    const lbImg = lightbox.querySelector('.lightbox-img');
    const galleryItems = Array.from(document.querySelectorAll('.gallery-item[data-src]'));
    let currentIdx = 0;

    const openLightbox = (idx) => {
      currentIdx = idx;
      lbImg.src = galleryItems[idx].dataset.src;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
    };
    const closeLightbox = () => {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    };

    galleryItems.forEach((item, idx) => {
      item.addEventListener('click', () => openLightbox(idx));
    });
    lightbox.querySelector('.lightbox-close')?.addEventListener('click', closeLightbox);
    lightbox.querySelector('.lightbox-prev')?.addEventListener('click', () => {
      openLightbox((currentIdx - 1 + galleryItems.length) % galleryItems.length);
    });
    lightbox.querySelector('.lightbox-next')?.addEventListener('click', () => {
      openLightbox((currentIdx + 1) % galleryItems.length);
    });
    lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', e => {
      if (!lightbox.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') openLightbox((currentIdx - 1 + galleryItems.length) % galleryItems.length);
      if (e.key === 'ArrowRight') openLightbox((currentIdx + 1) % galleryItems.length);
    });
  }

  /* --- Tabs (Grundrisse) --- */
  document.querySelectorAll('.tabs-nav .tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      btn.closest('.floorplans-tabs').querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      btn.closest('.floorplans-tabs').querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.getElementById(target)?.classList.add('active');
    });
  });

  /* --- Contact Form --- */
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('.form-submit');
      const successMsg = document.getElementById('form-success');
      const errorMsg = document.getElementById('form-error');

      btn.textContent = 'Wird gesendet…';
      btn.disabled = true;

      const data = {
        hp_website: form.hp_website?.value,
        name: form.name?.value,
        email: form.email?.value,
        phone: form.phone?.value,
        subject: form.subject?.value,
        message: form.message?.value,
        object: form.object?.value,
        privacy: form.privacy?.checked,
        newsletter: form.newsletter?.checked,
        interesse_miete: form.interesse_miete?.checked,
        interesse_mietkauf_belags: form.interesse_mietkauf_belags?.checked,
        interesse_mietkauf_schluessel: form.interesse_mietkauf_schluessel?.checked,
      };

      try {
        if (typeof grecaptcha === 'undefined') {
          if (errorMsg) { errorMsg.style.display = 'block'; }
          btn.textContent = 'Anfrage senden';
          btn.disabled = false;
          return;
        }
        await new Promise(resolve => grecaptcha.ready(resolve));
        data.recaptchaToken = await grecaptcha.execute('6LeVikgtAAAAAFGjShS6lKvxFgSwOyP60HqwJo2n', { action: 'contact' });

        const res = await fetch('/.netlify/functions/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        if (res.ok) {
          form.reset();
          if (successMsg) { successMsg.style.display = 'block'; }
          form.style.display = 'none';
        } else {
          throw new Error('Server error');
        }
      } catch {
        if (errorMsg) { errorMsg.style.display = 'block'; }
        btn.textContent = 'Anfrage senden';
        btn.disabled = false;
      }
    });
  }

});
