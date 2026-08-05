#!/usr/bin/env python3
"""Bouwt de hele site uit de databestanden in content/.

    python3 tools/bouw.py

Wat erin gaat:
    content/site.json       contactgegevens en teksten die overal terugkomen
    content/home.json       alle teksten van de homepage
    content/projecten.json  de projecten
    content/recensies.json  de recensies
    assets/projecten/<slug>/  de foto's per project

Wat eruit komt:
    index.html, recensies.html, projecten/<slug>.html

Deze bestanden worden overschreven — pas ze dus niet met de hand aan, maar
wijzig de inhoud in content/. Dat is ook wat de bewerkomgeving doet.
"""

import html
import json
import shutil
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
CONTENT = WORTEL / "content"
FOTO_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
ASSETVERSIE = "6"

# ---------------------------------------------------------------- iconen ----
# Lijntekeningen uit de Lucide-set, als SVG in de pagina opgenomen zodat er
# geen externe scripts nodig zijn.
ICONEN = {
    "hamer": '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
    "vrachtwagen": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "doos": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/><path d="m7.5 4.27 9 5.15"/>',
    "verfroller": '<rect width="16" height="6" x="2" y="2" rx="2"/><path d="M10 16v-2a2 2 0 0 1 2-2h8a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect width="4" height="6" x="8" y="16" rx="1"/>',
    "glans": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
    "bad": '<path d="M10 4 8 6"/><path d="M17 19v2"/><path d="M2 12h20"/><path d="M7 19v2"/><path d="M9 5 7.621 3.621A2.121 2.121 0 0 0 4 5v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/>',
    "deur": '<path d="M18 20V6a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14"/><path d="M2 20h20"/><path d="M14 12v.01"/>',
    "handen": '<path d="M11 12h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 14"/><path d="m7 18 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 13 6 6"/>',
    "pijl-rechts": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "pijl-links": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "pijl-rechtsboven": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "agenda": '<path d="M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h5"/><path d="M17.5 17.5 16 16.3V14"/><circle cx="16" cy="16" r="6"/>',
    "bon": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>',
    "chevron-links": '<path d="m15 18-6-6 6-6"/>',
    "chevron-rechts": '<path d="m9 18 6-6-6-6"/>',
    "citaat": '<path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/><path d="M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/>',
    "vinkje": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "locatie": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "telefoon": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "bericht": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 12a2 2 0 0 0 2-2V8H8"/><path d="M14 12a2 2 0 0 0 2-2V8h-2"/>',
    "menu": '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "kruis": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
}


def svg(naam, maat=18, klasse="ic"):
    return (
        f'<svg class="{klasse}" xmlns="http://www.w3.org/2000/svg" width="{maat}" '
        f'height="{maat}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{ICONEN[naam]}</svg>'
    )


def e(tekst):
    """Ontsmet tekst uit de databestanden voor gebruik in HTML."""
    return html.escape(str(tekst), quote=True)


def laad(naam):
    return json.loads((CONTENT / naam).read_text(encoding="utf-8"))


# ------------------------------------------------------- gedeelde stukken ----

def kop(titel, omschrijving, p=""):
    """<head> plus de header met menu. p is het pad terug naar de wortel."""
    return f'''<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titel)}</title>
  <meta name="description" content="{e(omschrijving)}">
  <link rel="icon" href="{p}assets/embleem.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{p}assets/site.css?v={ASSETVERSIE}">
</head>
<body>
'''


def header(s, p="", home=False):
    logo = f'<img class="logo" src="{p}assets/logo-badgast.png" alt="{e(s["bedrijfsnaam"])}, badkamerrenovaties">'
    if not home:
        logo = f'<a href="{p}index.html" style="display:block;line-height:0">{logo}</a>'
    h = "#" if home else f"{p}index.html#"
    recensies_link = "#recensies" if home else f"{p}recensies.html"
    return f'''
<header class="site-header">
  {logo}
  <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="hoofdmenu" aria-label="Menu openen">
    {svg("menu", 24, "ic ic-menu")}
    {svg("kruis", 24, "ic ic-close")}
  </button>
  <nav class="site-nav" id="hoofdmenu">
    <a href="{h}formule">De formule</a>
    <a href="{h}diensten">Diensten</a>
    <a href="{h}werkwijze">Werkwijze</a>
    <a href="{h}projecten">Projecten</a>
    <a href="{recensies_link}">Recensies</a>
    <a class="tel-pill" href="tel:{s["telefoon_link"]}">{e(s["telefoon_kort"])}</a>
  </nav>
</header>
'''


def cta_blok(s, titel, p=""):
    return f'''
<section class="cta-blok">
  <div class="cta-blok-inner" data-fu>
    <div class="cta-blok-deco" aria-hidden="true"></div>
    <div class="cta-blok-tekst">
      <h2>{e(titel)}</h2>
      <p>Ik kom vrijblijvend langs, meet op en denk met je mee. Geen verkooppraatje, wel een eerlijk verhaal over wat er kan.</p>
      <p class="cta-blok-nb">{e(s["planning_notitie"])}</p>
    </div>
    <div class="cta-blok-knoppen">
      <a class="btn-primary" href="{p}index.html#offerte">Vraag offerte aan</a>
      <a class="btn-outline" href="tel:{s["telefoon_link"]}">{svg("telefoon")}{e(s["telefoon_weergave"])}</a>
    </div>
  </div>
</section>
'''


def voet(s, p="", lightbox=False, strak=True):
    klasse = "site-footer site-footer--tight" if strak else "site-footer"
    lb = f'''
<div class="lightbox" id="lightbox" hidden>
  <button type="button" class="lightbox-knop lightbox-sluit" aria-label="Sluiten">{svg("kruis", 24)}</button>
  <button type="button" class="lightbox-knop lightbox-vorige" aria-label="Vorige foto">{svg("chevron-links", 24)}</button>
  <button type="button" class="lightbox-knop lightbox-volgende" aria-label="Volgende foto">{svg("chevron-rechts", 24)}</button>
  <figure class="lightbox-inhoud">
    <img class="lightbox-foto" alt="">
    <figcaption class="lightbox-teller"></figcaption>
  </figure>
</div>
''' if lightbox else ""
    return f'''
<footer class="{klasse}">
  <div class="footer-notch" aria-hidden="true"></div>
  <img class="footer-emblem" src="{p}assets/embleem.png" alt="" aria-hidden="true">
  <div class="footer-cols">
    <div class="footer-col-merk">
      <img src="{p}assets/logo-badgast.png" alt="{e(s["bedrijfsnaam"])}">
      <p>{e(s["footer_omschrijving"])}</p>
    </div>
    <div class="footer-col-contact">
      <div class="footer-title">Contactgegevens</div>
      <div class="footer-contact">
        <div><span class="ic-wrap">{svg("locatie", 17)}</span><span>{s["werkgebied_kort"]}</span></div>
        <div><span class="ic-wrap">{svg("telefoon", 17)}</span><a href="tel:{s["telefoon_link"]}">{e(s["telefoon_weergave"])}</a></div>
        <div><span class="ic-wrap">{svg("mail", 17)}</span><a href="mailto:{e(s["email"])}">{e(s["email"])}</a></div>
        <div><span class="ic-wrap">{svg("globe", 17)}</span><a href="https://debadgast.nl">{e(s["website"])}</a></div>
      </div>
    </div>
    <div class="footer-col-gebied">
      <div class="footer-kicker">Werkgebied</div>
      <p>{e(s["werkgebied"])}</p>
    </div>
    <div class="footer-col-gegevens">
      <div class="footer-kicker">Gegevens</div>
      <p>{s["kvk"]}</p>
    </div>
  </div>
  <div class="footer-bottom">{e(s["copyright"])}</div>
</footer>
{lb}
<script src="{p}assets/site.js?v={ASSETVERSIE}"></script>
</body>
</html>
'''


# ------------------------------------------------------------- projecten ----

def fotos(slug):
    map_ = WORTEL / "assets" / "projecten" / slug
    if not map_.is_dir():
        return []
    return sorted((p for p in map_.iterdir() if p.suffix.lower() in FOTO_TYPES),
                  key=lambda p: p.name.lower())


def fotopad(bestand):
    return f"assets/projecten/{bestand.parent.name}/{bestand.name}"


def waar(pr):
    return " · ".join(str(d) for d in (pr.get("plaats"), pr.get("jaar")) if d)


def in_plaats(pr):
    return f' in {pr["plaats"]}' if pr.get("plaats") else ""


def duurchip(pr, inspring):
    d = pr.get("duur")
    return f'\n{inspring}<span class="chip chip--accent">{e(d)}</span>' if d else ""


def projectkaart(pr, fs):
    omslag = fotopad(fs[0]) if fs else ""
    pos = pr.get("omslag_positie")
    stijl = f' style="object-position:{pos}"' if pos else ""
    teller = f"{len(fs)} foto's" if len(fs) != 1 else "1 foto"
    kenmerken = "".join(f'\n            <span class="chip">{e(k)}</span>'
                        for k in pr["kenmerken"])
    return f'''      <a class="project" href="projecten/{pr["slug"]}.html" data-fu>
        <img src="{omslag}" alt="{e(pr["titel"])}{e(in_plaats(pr))}, gerenoveerd door De Badgast" loading="lazy" decoding="async"{stijl}>
        <div class="project-shade"></div>
        <div class="project-caption">
          <div class="project-label">{e(pr["label"])}</div>
          <h3>{e(pr["titel"])}</h3>
          <div class="project-chips">{kenmerken}{duurchip(pr, " " * 12)}
            <span class="chip-meta">{e(waar(pr))}</span>
          </div>
          <div class="project-open">Bekijk dit project{svg("pijl-rechts", 16)}<span class="project-teller">{teller}</span></div>
        </div>
      </a>
'''


def projectpagina(s, pr, fs, vorige, volgende):
    kenmerken = "".join(f'\n      <span class="chip">{e(k)}</span>' for k in pr["kenmerken"])
    werk = "".join(f'\n        <li>{e(w)}</li>' for w in pr["werk"])

    if fs:
        items = "".join(
            f'''      <button type="button" class="galerij-item" data-foto="{i}" aria-label="Foto {i + 1} van {len(fs)} vergroten">
        <img src="../{fotopad(f)}" alt="{e(pr["titel"])}{e(in_plaats(pr))} — foto {i + 1}" loading="lazy" decoding="async">
      </button>
''' for i, f in enumerate(fs))
        galerij = f'    <div class="galerij" id="galerij">\n{items}    </div>\n'
        telregel = f"{len(fs)} foto's van dit project" if len(fs) != 1 else "1 foto van dit project"
    else:
        galerij = '    <p class="galerij-leeg">De foto\'s van dit project komen binnenkort online.</p>\n'
        telregel = "Foto's volgen"

    nav = ""
    if vorige or volgende:
        links = ""
        if vorige:
            links += f'''      <a class="proj-nav-link proj-nav-link--vorige" href="{vorige["slug"]}.html">
        {svg("pijl-links")}
        <span><span class="proj-nav-label">Vorige project</span><span class="proj-nav-titel">{e(vorige["titel"])}</span></span>
      </a>
'''
        if volgende:
            links += f'''      <a class="proj-nav-link proj-nav-link--volgende" href="{volgende["slug"]}.html">
        <span><span class="proj-nav-label">Volgende project</span><span class="proj-nav-titel">{e(volgende["titel"])}</span></span>
        {svg("pijl-rechts")}
      </a>
'''
        nav = f'\n<nav class="proj-nav" aria-label="Andere projecten">\n{links}</nav>\n'

    return (
        kop(f'{pr["titel"]}{in_plaats(pr)} — De Badgast', pr["lead"], "../")
        + header(s, "../")
        + f'''
<section class="proj-intro">
  <div class="proj-intro-deco" aria-hidden="true"></div>
  <a class="rec-terug" href="../index.html#projecten" data-fu>{svg("pijl-links", 16)}Terug naar alle projecten</a>
  <div class="proj-soort" data-fu>{e(pr["soort"])}</div>
  <h1 data-fu>{e(pr["titel"])}</h1>
  <p class="proj-lead" data-fu>{e(pr["lead"])}</p>
  <div class="proj-chips" data-fu>{kenmerken}{duurchip(pr, " " * 6)}
      <span class="chip-meta">{e(waar(pr))}</span>
  </div>
</section>

<section class="proj-body">
  <div class="proj-body-inner">
    <div class="proj-werk" data-fu>
      <div class="kicker">Wat ik heb gedaan</div>
      <ul>{werk}
      </ul>
    </div>
    <div class="proj-galerij-kop" data-fu>
      <div class="kicker kicker--muted">Foto's</div>
      <p>{telregel}. Klik op een foto om hem groot te bekijken.</p>
    </div>
  </div>
{galerij}</section>
{nav}'''
        + cta_blok(s, "Geïnteresseerd geraakt?", "../")
        + voet(s, "../", lightbox=True)
    )


# -------------------------------------------------------------- homepage ----

def bouw_index(s, h, projecten):
    punten = "".join(f'        <div class="hero-usp"><span class="drop"></span>{e(t)}</div>\n'
                     for t in h["hero"]["punten"])
    cijfers = "".join(f'        <div class="hero-stat"><b>{e(c["getal"])}</b><span>{e(c["label"])}</span></div>\n'
                      for c in h["hero"]["cijfers"])
    zelf = "".join(f'''        <div class="zelf-item">
          <span class="ic-wrap">{svg(i["icoon"], 20)}</span>
          <div><b>{e(i["titel"])}</b><p>{e(i["tekst"])}</p></div>
        </div>
''' for i in h["formule"]["lijst"])
    diensten = "".join(f'''    <div class="dienst-card" data-fu>
      <div class="ic-wrap">{svg(i["icoon"], 32)}</div>
      <h3>{e(i["titel"])}</h3>
      <p>{e(i["tekst"])}</p>
    </div>
''' for i in h["diensten"]["items"])
    stappen = "".join(f'''    <div class="stap" data-fu>
      <div class="stap-top"><span class="stap-num">{n:02d}</span><span class="drop"></span></div>
      <h3>{e(st["titel"])}</h3>
      <p>{e(st["tekst"])}</p>
      <div class="stap-tag">{e(st["tag"])}</div>
    </div>
''' for n, st in enumerate(h["werkwijze"]["stappen"], 1))
    wmeta = "".join(f'    <span>{svg(m["icoon"])}{e(m["tekst"])}</span>\n'
                    for m in h["werkwijze"]["meta"])
    kaarten = "".join(projectkaart(pr, fotos(pr["slug"])) for pr in projecten)

    recensies = laad("recensies.json")
    uitgelicht = [r for r in recensies if r.get("uitgelicht")]
    rec_kaarten = "".join(f'''    <figure class="review" data-fu>
      <span class="review-quote-drop"><span>{svg("citaat", 17)}</span></span>
      <div class="review-stars">★★★★★</div>
      <blockquote>“{e(r.get("kort") or r["tekst"])}”</blockquote>
      <figcaption>
        <span class="review-avatar"><span>{e(initialen(r["naam"]))}</span></span>
        <span class="review-who"><b>{e(r["naam"])}</b><span>{e(r["plaats"])} · {e(r["datum"])}</span></span>
      </figcaption>
    </figure>
''' for r in uitgelicht)

    o = h["offerte"]
    return (
        kop(h["titel"], h["omschrijving"])
        + header(s, home=True)
        + f'''
<section class="hero">
  <img class="hero-img" src="assets/hero-badkamer.jpg" alt="Door De Badgast gerenoveerde badkamer met vrijstaand bad" fetchpriority="high" decoding="async">
  <div class="hero-shade-side"></div>
  <div class="hero-shade-bottom"></div>

  <div class="hero-inner">
    <div class="hero-copy">
      <div class="hero-eyebrow" data-fu>{e(h["hero"]["bovenkop"])}</div>
      <h1 data-fu>{e(h["hero"]["titel"])}<br><span class="accent">{e(h["hero"]["titel_accent"])}</span></h1>
      <p class="hero-lead" data-fu>{e(h["hero"]["tekst"])}</p>
      <div class="hero-ctas" data-fu>
        <a class="btn-primary" href="#offerte">{e(h["hero"]["knop_offerte"])}</a>
        <a class="btn-ghost" href="tel:{s["telefoon_link"]}">{e(h["hero"]["knop_bellen"])}</a>
      </div>
      <div class="hero-usps" data-fu>
{punten}      </div>
    </div>

    <div class="hero-card" data-fu>
      <div class="hero-card-head">
        <span class="hero-card-stars">★★★★★</span>
        <span class="hero-card-label">{e(h["hero"]["kaart_label"])}</span>
      </div>
      <blockquote>“{e(h["hero"]["kaart_citaat"])}”</blockquote>
      <div class="hero-card-name">{e(h["hero"]["kaart_naam"])}</div>
      <div class="hero-stats">
{cijfers}      </div>
    </div>
  </div>
</section>

<section id="over" class="over">
  <div class="over-inner">
    <div class="over-photos" data-fu>
      <div class="over-deco" aria-hidden="true"></div>
      <div class="over-main">
        <div class="over-badge">
          <span class="drop"></span>
          <b>{e(h["over"]["badge"])}</b>
        </div>
        <img src="{e(h["over"]["foto_groot"])}" alt="{e(h["over"]["foto_groot_alt"])}" loading="lazy" decoding="async">
      </div>
      <div class="over-small">
        <img src="{e(h["over"]["foto_klein"])}" alt="{e(h["over"]["foto_klein_alt"])}" loading="lazy" decoding="async">
      </div>
    </div>
    <div class="over-text" data-fu>
      <div class="kicker">{e(h["over"]["kicker"])}</div>
      <h2>{e(h["over"]["titel"])}</h2>
      <p>{e(h["over"]["tekst"])}</p>
    </div>
  </div>
</section>

<section id="formule" class="formule">
  <div class="formule-inner">
    <div class="formule-col" data-fu>
      <div class="kicker">{e(h["formule"]["kicker"])}</div>
      <h2>{h["formule"]["titel"]}</h2>
      <p>{e(h["formule"]["tekst"])}</p>
      <p class="formule-nb">{e(h["formule"]["naschrift"])}</p>
    </div>
    <div class="formule-col formule-col--lijst" data-fu>
      <div class="kicker kicker--muted">{e(h["formule"]["lijst_kicker"])}</div>
      <div class="zelf-lijst">
{zelf}      </div>
    </div>
  </div>
</section>

<section id="diensten" class="diensten">
  <div class="diensten-head" data-fu>
    <div class="kicker">{e(h["diensten"]["kicker"])}</div>
    <h2>{e(h["diensten"]["titel"])}</h2>
  </div>
  <div class="dienst-grid">
{diensten}  </div>
</section>

<section id="werkwijze" class="werkwijze">
  <div class="werkwijze-deco" aria-hidden="true"></div>
  <div class="werkwijze-head">
    <div class="werkwijze-head-copy" data-fu>
      <div class="kicker kicker--light">{e(h["werkwijze"]["kicker"])}</div>
      <h2>{h["werkwijze"]["titel"]}</h2>
      <p>{e(h["werkwijze"]["tekst"])}</p>
    </div>
    <a class="btn-white" href="#offerte" data-fu>{e(h["werkwijze"]["knop"])}{svg("pijl-rechts")}</a>
  </div>

  <div class="stappen">
{stappen}  </div>

  <div class="werkwijze-meta" data-fu>
{wmeta}  </div>
</section>

<section id="projecten" class="projecten">
  <div class="projecten-head" data-fu>
    <div class="kicker kicker--wide">{e(h["projecten"]["kicker"])}</div>
    <h2>{e(h["projecten"]["titel"])} <span>{e(h["projecten"]["titel_grijs"])}</span></h2>
    <p>{e(h["projecten"]["tekst"])}</p>
  </div>

  <div class="rail-wrap">
    <button type="button" class="rail-btn rail-btn--prev" data-rail-prev aria-label="Vorige project">{svg("chevron-links", 20)}</button>
    <button type="button" class="rail-btn rail-btn--next" data-rail-next aria-label="Volgende project">{svg("chevron-rechts", 20)}</button>
    <div class="rail-fade rail-fade--l"></div>
    <div class="rail-fade rail-fade--r"></div>
    <div id="projectRail" class="rail">
{kaarten}    </div>
  </div>

  <div class="projecten-foot" data-fu>
    <span><span class="drop"></span>{e(h["projecten"]["voetregel"])}</span>
  </div>
</section>

<section id="recensies" class="recensies">
  <div class="recensies-deco" aria-hidden="true"></div>
  <div class="recensies-head">
    <div class="recensies-head-copy" data-fu>
      <div class="kicker">{e(h["recensies"]["kicker"])}</div>
      <h2>{h["recensies"]["titel"]}</h2>
      <p>{e(h["recensies"]["tekst"])}</p>
    </div>
    <a class="link-pill" href="recensies.html" data-fu>{e(h["recensies"]["knop"])}{svg("pijl-rechtsboven", 17)}</a>
  </div>
  <div class="review-grid">
{rec_kaarten}  </div>
</section>

<section id="offerte" class="offerte">
  <div class="offerte-inner">
    <div class="offerte-copy" data-fu>
      <h2>{e(o["titel"])}</h2>
      <p>{e(o["tekst"])}</p>
      <div class="offerte-nb"><span>{e(o["notitie"])}</span></div>
      <div class="offerte-bel">
        <div class="offerte-bel-label">{e(o["bel_label"])}</div>
        <a class="offerte-tel" href="tel:{s["telefoon_link"]}">{e(s["telefoon_kort"])}</a>
        <div class="offerte-mail">{e(o["mail_label"])} <a href="mailto:{e(s["email"])}">{e(s["email"])}</a></div>
      </div>
    </div>
    <div class="offerte-formwrap" data-fu>
      <form class="offerte-form">
        <label><span>{e(o["veld_naam"])}</span><input name="naam" required placeholder="{e(o["veld_naam_hint"])}"></label>
        <div class="form-row">
          <label><span>{e(o["veld_telefoon"])}</span><input name="telefoon" type="tel" required placeholder="{e(o["veld_telefoon_hint"])}"></label>
          <label><span>{e(o["veld_email"])}</span><input name="email" type="email" required placeholder="{e(o["veld_email_hint"])}"></label>
        </div>
        <label><span>{e(o["veld_omschrijving"])}</span><textarea name="omschrijving" rows="4" placeholder="{e(o["veld_omschrijving_hint"])}"></textarea></label>
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" style="display:none" aria-hidden="true">
        <button type="submit">{e(o["knop"])}</button>
        <div class="form-error">{e(o["fout"])} <a href="tel:{s["telefoon_link"]}">{e(s["telefoon_weergave"])}</a> / mail <a href="mailto:{e(s["email"])}">{e(s["email"])}</a>.</div>
        <div class="form-privacy">{e(o["privacy"])}</div>
      </form>
      <div class="offerte-success">
        <div class="ic-wrap">{svg("vinkje", 34)}</div>
        <h3>{e(o["succes_titel"])}</h3>
        <p>{e(o["succes_tekst"])}</p>
        <button type="button">{e(o["succes_knop"])}</button>
      </div>
    </div>
  </div>
</section>
'''
        + voet(s, strak=False)
        .replace("</body>", f'''<div class="ctabar">
  <a class="ctabar-primary" href="#offerte">{e(h["mobiele_balk"]["offerte"])}</a>
  <a class="ctabar-bel" href="tel:{s["telefoon_link"]}">{svg("telefoon")}{e(h["mobiele_balk"]["bellen"])}</a>
</div>

</body>''')
    )


SKIP = {"en", "&", "de", "van", "der", "een"}


def initialen(naam):
    import re
    woorden = [w.strip(".,") for w in re.split(r"[\s,]+", naam) if w.strip(".,")]
    kern = [w for w in woorden if w.lower() not in SKIP] or woorden
    return (kern[0][0] if len(kern) == 1 else kern[0][0] + kern[-1][0]).upper()


# ------------------------------------------------------ recensiepagina ----

def bouw_recensies(s, recensies):
    kaarten = "".join(f'''    <figure class="rec-kaart" data-fu>
      <div class="review-stars">★★★★★</div>
      <blockquote>“{e(r["tekst"])}”</blockquote>
      <figcaption>
        <span class="review-avatar"><span>{e(initialen(r["naam"]))}</span></span>
        <span class="review-who"><b>{e(r["naam"])}</b><span>{e(r["plaats"])} · {e(r["datum"])}</span></span>
      </figcaption>
    </figure>
''' for r in recensies)

    return (
        kop("Recensies — De Badgast, badkamerrenovaties Roosendaal",
            "Wat klanten schrijven over de badkamer- en toiletrenovaties van Gerard Bartels (De Badgast) in Roosendaal en omgeving. Alleen vijf sterren tot nu toe.")
        + header(s)
        + f'''
<section class="rec-intro">
  <div class="rec-intro-deco" aria-hidden="true"></div>
  <a class="rec-terug" href="index.html" data-fu>{svg("pijl-links", 16)}Terug naar de homepage</a>
  <h1 data-fu>Wat klanten over<br>mijn werk schrijven</h1>
  <p data-fu>Bijna al mijn klanten komen via mond-tot-mondreclame. Hieronder lees je wat mensen zelf over de renovatie van hun badkamer of toilet schreven.</p>
  <div class="rec-intro-feiten" data-fu>
    <div><span class="sterren">★★★★★</span>Alleen vijf sterren tot nu toe</div>
    <div><span class="drop"></span>{len(recensies)} recensies · ±500 badkamers sinds 2007</div>
  </div>
</section>

<section class="rec-lijst">
  <div class="rec-kolommen">
{kaarten}    <figure class="rec-kaart rec-kaart--uitnodiging">
      <div class="rec-uitnodiging-kop">{svg("bericht")}Ruimte voor jouw recensie</div>
      <p>Heb ik bij jou gewerkt en wil je iets achterlaten? Mail me gerust, dan zet ik het erbij.</p>
      <a class="rec-mail-link" href="mailto:{e(s["email"])}">{e(s["email"])}{svg("pijl-rechtsboven", 16)}</a>
    </figure>
  </div>
  <p class="rec-bron" data-fu>Alle {len(recensies)} recensies, integraal overgenomen van debadgast.nl.</p>
</section>
'''
        + cta_blok(s, "Ook op deze lijst komen?")
        + voet(s)
    )


def main():
    s = laad("site.json")
    h = laad("home.json")
    projecten = laad("projecten.json")
    recensies = laad("recensies.json")

    (WORTEL / "index.html").write_text(bouw_index(s, h, projecten), encoding="utf-8")
    print(f"  index.html — {len(projecten)} projecten, "
          f"{sum(1 for r in recensies if r.get('uitgelicht'))} uitgelichte recensies")

    (WORTEL / "recensies.html").write_text(bouw_recensies(s, recensies), encoding="utf-8")
    print(f"  recensies.html — {len(recensies)} recensies")

    uit = WORTEL / "projecten"
    if uit.exists():
        shutil.rmtree(uit)
    uit.mkdir()
    for i, pr in enumerate(projecten):
        fs = fotos(pr["slug"])
        pagina = projectpagina(
            s, pr, fs,
            projecten[i - 1] if i > 0 else None,
            projecten[i + 1] if i + 1 < len(projecten) else None,
        )
        (uit / f"{pr['slug']}.html").write_text(pagina, encoding="utf-8")
        print(f"  projecten/{pr['slug']}.html — {len(fs)} foto's")


if __name__ == "__main__":
    main()
