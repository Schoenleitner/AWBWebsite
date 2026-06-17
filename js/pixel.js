/* Meta Pixel — feuert nur nach Cookie-Zustimmung */
function activateMetaPixel() {
  if (window._metaPixelLoaded) return;
  window._metaPixelLoaded = true;

  !function(f,b,e,v,n,t,s){
    if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)
  }(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

  fbq('init', '2453756818385630');
  fbq('track', 'PageView');
}

// Wenn bereits zugestimmt wurde (z.B. bei erneutem Seitenaufruf), sofort aktivieren
if (localStorage.getItem('awb_cookie_consent') === 'accepted') {
  activateMetaPixel();
}
