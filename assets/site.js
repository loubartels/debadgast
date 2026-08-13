// De Badgast — gedeeld gedrag voor alle pagina's

(function () {
  'use strict';

  // Sticky header krijgt een glas-effect zodra er gescrold is
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-glass', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Hamburgermenu op smalle schermen
  var navToggle = document.querySelector('.nav-toggle');
  if (header && navToggle) {
    var setMenu = function (open) {
      header.classList.toggle('menu-open', open);
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      navToggle.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
    };
    navToggle.addEventListener('click', function () {
      setMenu(!header.classList.contains('menu-open'));
    });
    document.querySelectorAll('.site-nav a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
  }

  // Secties faden omhoog zodra ze in beeld komen
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        entry.target.style.animation = 'fu .7s ' + (i * 0.08) + 's both';
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    document.querySelectorAll('[data-fu]').forEach(function (el) {
      el.style.opacity = '0';
      io.observe(el);
    });
  }

  // Projectencarrousel: pijlknoppen scrollen één kaart per klik
  var rail = document.getElementById('projectRail');
  if (rail) {
    var scrollRail = function (dir) {
      var card = rail.querySelector('.project');
      var step = (card ? card.offsetWidth : rail.clientWidth * 0.8) + 28;
      rail.scrollBy({ left: dir * step, behavior: 'smooth' });
    };
    var prev = document.querySelector('[data-rail-prev]');
    var next = document.querySelector('[data-rail-next]');
    if (prev) prev.addEventListener('click', function () { scrollRail(-1); });
    if (next) next.addEventListener('click', function () { scrollRail(1); });
  }

  // Fotogalerij op de projectpagina's: klik opent de foto groot
  var galerij = document.getElementById('galerij');
  var lightbox = document.getElementById('lightbox');
  if (galerij && lightbox) {
    var items = Array.prototype.slice.call(galerij.querySelectorAll('.galerij-item'));
    var foto = lightbox.querySelector('.lightbox-foto');
    var teller = lightbox.querySelector('.lightbox-teller');
    var huidige = 0;
    var laatstGeopend = null;

    lightbox.classList.toggle('lightbox--enkel', items.length < 2);

    var toon = function (i) {
      huidige = (i + items.length) % items.length;
      var bron = items[huidige].querySelector('img');
      foto.src = bron.src;
      foto.alt = bron.alt;
      teller.textContent = (huidige + 1) + ' / ' + items.length;
    };
    var open = function (i) {
      laatstGeopend = items[i];
      toon(i);
      lightbox.hidden = false;
      document.body.classList.add('lightbox-open');
      lightbox.querySelector('.lightbox-sluit').focus();
    };
    var sluit = function () {
      lightbox.hidden = true;
      document.body.classList.remove('lightbox-open');
      if (laatstGeopend) laatstGeopend.focus();
    };

    items.forEach(function (item, i) {
      item.addEventListener('click', function () { open(i); });
    });
    lightbox.querySelector('.lightbox-sluit').addEventListener('click', sluit);
    lightbox.querySelector('.lightbox-vorige').addEventListener('click', function () { toon(huidige - 1); });
    lightbox.querySelector('.lightbox-volgende').addEventListener('click', function () { toon(huidige + 1); });
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target === lightbox.querySelector('.lightbox-inhoud')) sluit();
    });
    document.addEventListener('keydown', function (e) {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') sluit();
      else if (e.key === 'ArrowLeft') toon(huidige - 1);
      else if (e.key === 'ArrowRight') toon(huidige + 1);
    });
  }

  // Formulieren: versturen via FormSubmit naar info@debadgast.nl en tonen
  // daarna de bevestiging. De eerste inzending vraagt eenmalig om activatie
  // via een mail aan dat adres — zie README.md.
  //
  // Recensies worden hier niet gepubliceerd. Ze komen als mail binnen en
  // Gerard zet ze daarna zelf in de bewerkomgeving. Die tussenstap is met
  // opzet handwerk: er is geen openbaar eindpunt dat iets op de site kan
  // zetten, dus een bot kan hier hooguit een mail veroorzaken.
  function koppelFormulier(opties) {
    var wrap = document.querySelector(opties.wrap);
    if (!wrap) return;
    var form = wrap.querySelector('form');
    var resetBtn = wrap.querySelector(opties.reset);
    if (!form) return;

    var bezig = false;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (bezig) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var btn = form.querySelector('button[type=submit]');
      var err = form.querySelector('.form-error');
      if (err) err.style.display = 'none';
      bezig = true;
      btn.disabled = true;
      btn.textContent = 'Versturen…';

      var data = new FormData(form);
      data.append('_subject', opties.onderwerp);
      data.append('_template', 'table');
      data.append('_captcha', 'false');

      fetch('https://formsubmit.co/ajax/info@debadgast.nl', {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: data
      }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      }).then(function () {
        wrap.classList.add('is-sent');
        form.reset();
      }).catch(function () {
        if (err) err.style.display = 'block';
      }).finally(function () {
        bezig = false;
        btn.disabled = false;
        btn.textContent = opties.knop;
      });
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        wrap.classList.remove('is-sent');
      });
    }
  }

  koppelFormulier({
    wrap: '.offerte-formwrap',
    reset: '.offerte-success button',
    onderwerp: 'Nieuwe offerteaanvraag via debadgast.nl',
    knop: 'Verstuur aanvraag'
  });

  koppelFormulier({
    wrap: '.rec-formwrap',
    reset: '.rec-success button',
    onderwerp: 'Nieuwe recensie via debadgast.nl — nog niet geplaatst',
    knop: 'Recensie versturen'
  });
})();
