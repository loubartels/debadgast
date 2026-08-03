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

  // Offerteformulier: verstuurt via FormSubmit naar info@debadgast.nl
  // en toont daarna de bevestiging. Eerste inzending vraagt eenmalig om
  // activatie via een mail aan dat adres — zie README.md.
  var formwrap = document.querySelector('.offerte-formwrap');
  if (formwrap) {
    var form = formwrap.querySelector('form');
    var resetBtn = formwrap.querySelector('.offerte-success button');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var btn = form.querySelector('button[type=submit]');
        var err = form.querySelector('.form-error');
        if (err) err.style.display = 'none';
        btn.disabled = true;
        btn.textContent = 'Versturen…';
        var data = new FormData(form);
        data.append('_subject', 'Nieuwe offerteaanvraag via debadgast.nl');
        data.append('_template', 'table');
        fetch('https://formsubmit.co/ajax/info@debadgast.nl', {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: data
        }).then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        }).then(function () {
          formwrap.classList.add('is-sent');
          form.reset();
        }).catch(function () {
          if (err) err.style.display = 'block';
        }).finally(function () {
          btn.disabled = false;
          btn.textContent = 'Verstuur aanvraag';
        });
      });
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        formwrap.classList.remove('is-sent');
      });
    }
  }
})();
