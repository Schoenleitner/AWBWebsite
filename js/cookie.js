/* Cookie Consent — Attergauer Wohnbau */
(function () {
  const CONSENT_KEY = 'awb_cookie_consent';
  const banner = document.getElementById('cookie-banner');
  if (!banner) return;

  const consent = localStorage.getItem(CONSENT_KEY);
  if (!consent) {
    setTimeout(() => banner.classList.add('visible'), 800);
  }

  banner.querySelector('.cookie-accept')?.addEventListener('click', () => {
    localStorage.setItem(CONSENT_KEY, 'accepted');
    banner.classList.remove('visible');
    // Meta Pixel will be activated here later
    if (typeof activateMetaPixel === 'function') activateMetaPixel();
  });

  banner.querySelector('.cookie-decline')?.addEventListener('click', () => {
    localStorage.setItem(CONSENT_KEY, 'declined');
    banner.classList.remove('visible');
  });
})();
