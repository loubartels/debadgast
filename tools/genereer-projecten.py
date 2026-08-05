#!/usr/bin/env python3
"""Genereert de projectkaarten op index.html en de projectpagina's.

Een project toevoegen of uitbreiden:

  1. Zet de foto's in assets/projecten/<slug>/ — ze verschijnen op alfabetische
     volgorde, dus nummer ze (01-…, 02-…). De eerste foto wordt de omslagfoto.
  2. Voeg het project toe aan PROJECTEN hieronder (of pas het aan).
  3. Draai:  python3 tools/genereer-projecten.py

De gegenereerde HTML wordt gecommit, dus de site zelf heeft geen build-stap.
"""

import html
import re
from pathlib import Path

WORTEL = Path(__file__).resolve().parent.parent
FOTO_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

# De foto's komen uit Gerards Drive-map "Lou fotomateriaal website"; per project
# is dat zijn eigen "web"-selectie. Het jaartal komt uit de opnamedatum van de
# foto's. "plaats" en "duur" zijn bewust leeg: die staan nergens vast. Vul ze
# hier in zodra Gerard ze doorgeeft, dan verschijnen ze vanzelf op de site.
PROJECTEN = [
    {
        "slug": "musters",
        "titel": "Badkamer met vrijstaand bad en natuurstenen waskommen",
        "label": "Warm en natuurlijk",
        "soort": "Badkamer",
        "plaats": "",
        "jaar": "2014",
        "duur": "",
        "kenmerken": ["Vrijstaand bad", "Natuurstenen waskommen", "Inloopdouche"],
        "omslag_positie": None,
        "lead": "Een badkamer in warme tinten: betonlook tegels, een houten "
                "wastafelblad met twee natuurstenen waskommen en een vrijstaand "
                "bad tegen een accentwand.",
        "werk": [
            "Oude badkamer gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld",
            "Inloopdouche met douchegoot aangelegd",
            "Wastafelblad met waskommen en vrijstaand bad geplaatst",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "delleman",
        "titel": "Toiletruimte met mozaïekaccent",
        "label": "Klein en verfijnd",
        "soort": "Toilet",
        "plaats": "",
        "jaar": "2014",
        "duur": "",
        "kenmerken": ["Zwevend toilet", "Mozaïekaccent", "Tegels tot plafond"],
        "omslag_positie": None,
        "lead": "Een compacte toiletruimte, van vloer tot plafond betegeld, met "
                "een mozaïekstrook op de leidingkoker als accent.",
        "werk": [
            "Oude toiletruimte gestript",
            "Leidingwerk vernieuwd",
            "Tegelwerk tot het plafond, met mozaïekstrook",
            "Zwevend toilet en fonteintje gemonteerd",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "valkenburg",
        "titel": "Badkamer en toilet met inloopdouche",
        "label": "Licht en praktisch",
        "soort": "Badkamer en toilet",
        "plaats": "",
        "jaar": "2013",
        "duur": "",
        "kenmerken": ["Inloopdouche", "Douchegoot", "Nis in de wand"],
        "omslag_positie": None,
        "lead": "Badkamer en toilet in één traject: een inloopdouche met "
                "douchegoot, een nis in de wand en een wastafelmeubel met veel "
                "bergruimte.",
        "werk": [
            "Badkamer en toilet gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld, met nis in de wand",
            "Inloopdouche met douchegoot aangelegd",
            "Wastafelmeubel en zwevend toilet geplaatst",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "badk1",
        "titel": "Badkamer met inloopdouche, toilet en bidet",
        "label": "Ruim en strak",
        "soort": "Badkamer",
        "plaats": "",
        "jaar": "2013",
        "duur": "",
        "kenmerken": ["Inloopdouche", "Dubbele wastafel", "Toilet en bidet"],
        "omslag_positie": None,
        "lead": "Een ruime badkamer met een inloopdouche onder het schuine dak, "
                "een lange dubbele wastafel en een eigen wand voor toilet en "
                "bidet.",
        "werk": [
            "Oude badkamer gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld",
            "Inloopdouche met douchegoot aangelegd",
            "Dubbele wastafel, toilet en bidet geplaatst",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "kessels",
        "titel": "Badkamer met hoekbad en inloopdouche",
        "label": "Donker en warm",
        "soort": "Badkamer",
        "plaats": "",
        "jaar": "2012",
        "duur": "",
        "kenmerken": ["Hoekbad", "Inloopdouche", "Verlichte nissen"],
        "omslag_positie": None,
        "lead": "Antracietkleurige stroken tegels tegen wit, met een hoekbad, een "
                "inloopdouche achter glas en verlichte nissen in de wand.",
        "werk": [
            "Oude badkamer gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld, met nissen in de wand",
            "Inloopdouche en hoekbad geplaatst",
            "Wastafelmeubel met dubbele wastafel gemonteerd",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "quik",
        "titel": "Toiletruimte met zwevend toilet",
        "label": "Compact en strak",
        "soort": "Toilet",
        "plaats": "",
        "jaar": "2012",
        "duur": "",
        "kenmerken": ["Zwevend toilet", "Fonteintje", "Accentwand"],
        "omslag_positie": None,
        "lead": "Een kleine toiletruimte, helemaal opnieuw opgebouwd: een donkere "
                "accentwand achter het zwevende toilet en een strak fonteintje.",
        "werk": [
            "Oude toiletruimte gestript",
            "Leidingwerk vernieuwd",
            "Tegelwerk met donkere accentwand",
            "Zwevend toilet en fonteintje gemonteerd",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "agtmaal",
        "titel": "Zolderbadkamer met hoekbad",
        "label": "Onder het schuine dak",
        "soort": "Badkamer",
        "plaats": "",
        "jaar": "2011",
        "duur": "",
        "kenmerken": ["Hoekbad", "Inloopdouche", "Verlichte spiegel"],
        "omslag_positie": None,
        "lead": "Een badkamer onder het schuine dak, met een hoekbad op een "
                "verhoging, een houtlook vloer en een verlichte spiegel boven het "
                "wastafelblad.",
        "werk": [
            "Oude zolderbadkamer gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld",
            "Hoekbad op verhoging en inloopdouche geplaatst",
            "Wastafelblad met verlichte spiegel gemonteerd",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "babos",
        "titel": "Badkamer met ligbad en twee zuilwastafels",
        "label": "Wit en antraciet",
        "soort": "Badkamer",
        "plaats": "",
        "jaar": "2011",
        "duur": "",
        "kenmerken": ["Ligbad", "Twee zuilwastafels", "Accentwand"],
        "omslag_positie": None,
        "lead": "Wit tegelwerk met een antracieten accentwand, een ligbad onder "
                "het raam en twee vrijstaande zuilwastafels.",
        "werk": [
            "Oude badkamer gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld",
            "Ligbad en twee zuilwastafels geplaatst",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "rombouts",
        "titel": "Badkamer met dubbele wastafel en mozaïekbanen",
        "label": "Warm en klassiek",
        "soort": "Badkamer en toilet",
        "plaats": "",
        "jaar": "2011",
        "duur": "",
        "kenmerken": ["Dubbele wastafel", "Mozaïekbanen", "Inloopdouche"],
        "omslag_positie": None,
        "lead": "Bruine tegels met mozaïekbanen als accent, een inloopdouche "
                "achter glas en twee wastafels naast elkaar.",
        "werk": [
            "Badkamer en toilet gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld, met mozaïekbanen als accent",
            "Inloopdouche, dubbele wastafel en zwevend toilet geplaatst",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
    {
        "slug": "laan",
        "titel": "Badkamer met natuurstenen wastafelblad",
        "label": "Strak en tijdloos",
        "soort": "Badkamer en toilet",
        "plaats": "",
        "jaar": "2008",
        "duur": "",
        "kenmerken": ["Natuurstenen wastafelblad", "Inloopdouche", "Zwevend toilet"],
        "omslag_positie": None,
        "lead": "Strak wit tegelwerk met een donkere natuurstenen vloer en een op "
                "maat gemaakt wastafelblad van natuursteen.",
        "werk": [
            "Badkamer en toilet gesloopt en afgevoerd",
            "Leidingwerk en elektra vernieuwd",
            "Wanden en vloer betegeld",
            "Inloopdouche en zwevend toilet geplaatst",
            "Natuurstenen wastafelblad op maat gemonteerd",
            "Afgewerkt tot en met de laatste kitrand",
        ],
    },
]


def foto_s(slug):
    """Alle foto's uit assets/projecten/<slug>/, op bestandsnaam gesorteerd."""
    map_ = WORTEL / "assets" / "projecten" / slug
    if not map_.is_dir():
        return []
    return sorted(
        (p for p in map_.iterdir() if p.suffix.lower() in FOTO_TYPES),
        key=lambda p: p.name.lower(),
    )


def pad(bestand):
    return "assets/projecten/" + bestand.parent.name + "/" + bestand.name


def e(tekst):
    return html.escape(str(tekst), quote=True)


def waar(project):
    """'Plaats · jaar', of alleen het jaar zolang de plaats nog niet bekend is."""
    delen = [d for d in (project.get("plaats"), project.get("jaar")) if d]
    return " · ".join(str(d) for d in delen)


def in_plaats(project):
    """' in Roosendaal' voor titels, of niets als de plaats onbekend is."""
    return f' in {project["plaats"]}' if project.get("plaats") else ""


def duurchip(project, inspring):
    d = project.get("duur")
    return f'\n{inspring}<span class="chip chip--accent">{e(d)}</span>' if d else ""


def kaart(project, fotos):
    """De klikbare kaart in de carrousel op de homepage."""
    omslag = pad(fotos[0]) if fotos else ""
    pos = project["omslag_positie"]
    stijl = f' style="object-position:{pos}"' if pos else ""
    aantal = len(fotos)
    teller = f"{aantal} foto's" if aantal != 1 else "1 foto"
    kenmerken = "".join(
        f'\n            <span class="chip">{e(k)}</span>' for k in project["kenmerken"]
    )
    return f'''      <a class="project" href="projecten/{project["slug"]}.html" data-fu>
        <img src="{omslag}" alt="{e(project["titel"])}{e(in_plaats(project))}, gerenoveerd door De Badgast" loading="lazy" decoding="async"{stijl}>
        <div class="project-shade"></div>
        <div class="project-caption">
          <div class="project-label">{e(project["label"])}</div>
          <h3>{e(project["titel"])}</h3>
          <div class="project-chips">{kenmerken}{duurchip(project, " " * 12)}
            <span class="chip-meta">{e(waar(project))}</span>
          </div>
          <div class="project-open">Bekijk dit project<svg class="ic" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg><span class="project-teller">{teller}</span></div>
        </div>
      </a>
'''


KOP = '''<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titel}{plaats} — De Badgast</title>
  <meta name="description" content="{lead}">
  <link rel="icon" href="../assets/embleem.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/site.css?v=5">
</head>
<body>

<header class="site-header">
  <a href="../index.html" style="display:block;line-height:0"><img class="logo" src="../assets/logo-badgast.png" alt="De Badgast, badkamerrenovaties"></a>
  <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="hoofdmenu" aria-label="Menu openen">
    <svg class="ic ic-menu" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
    <svg class="ic ic-close" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
  </button>
  <nav class="site-nav" id="hoofdmenu">
    <a href="../index.html#formule">De formule</a>
    <a href="../index.html#diensten">Diensten</a>
    <a href="../index.html#werkwijze">Werkwijze</a>
    <a href="../index.html#projecten">Projecten</a>
    <a href="../recensies.html">Recensies</a>
    <a class="tel-pill" href="tel:+31615956178">+31 6 15956178</a>
  </nav>
</header>
'''

VOET = '''
<footer class="site-footer site-footer--tight">
  <div class="footer-notch" aria-hidden="true"></div>
  <img class="footer-emblem" src="../assets/embleem.png" alt="" aria-hidden="true">
  <div class="footer-cols">
    <div class="footer-col-merk">
      <img src="../assets/logo-badgast.png" alt="De Badgast">
      <p>Totaalrenovatie van badkamers en toiletten door Gerard Bartels.</p>
    </div>
    <div class="footer-col-contact">
      <div class="footer-title">Contactgegevens</div>
      <div class="footer-contact">
        <div><span class="ic-wrap"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg></span><span>Roosendaal<br>en omgeving</span></div>
        <div><span class="ic-wrap"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span><a href="tel:+31615956178">06 - 15 95 61 78</a></div>
        <div><span class="ic-wrap"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg></span><a href="mailto:info@debadgast.nl">info@debadgast.nl</a></div>
        <div><span class="ic-wrap"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg></span><a href="https://debadgast.nl">www.debadgast.nl</a></div>
      </div>
    </div>
    <div class="footer-col-gebied">
      <div class="footer-kicker">Werkgebied</div>
      <p>Roosendaal en omgeving, tot ongeveer 20 km.</p>
    </div>
    <div class="footer-col-gegevens">
      <div class="footer-kicker">Gegevens</div>
      <p>KvK 20133632<br>Algemene voorwaarden op aanvraag</p>
    </div>
  </div>
  <div class="footer-bottom">© 2007–2026 De Badgast</div>
</footer>

<div class="lightbox" id="lightbox" hidden>
  <button type="button" class="lightbox-knop lightbox-sluit" aria-label="Sluiten"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>
  <button type="button" class="lightbox-knop lightbox-vorige" aria-label="Vorige foto"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg></button>
  <button type="button" class="lightbox-knop lightbox-volgende" aria-label="Volgende foto"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg></button>
  <figure class="lightbox-inhoud">
    <img class="lightbox-foto" alt="">
    <figcaption class="lightbox-teller"></figcaption>
  </figure>
</div>

<script src="../assets/site.js?v=5"></script>
</body>
</html>
'''


def projectpagina(project, fotos, vorige, volgende):
    kenmerken = "".join(
        f'\n      <span class="chip">{e(k)}</span>' for k in project["kenmerken"]
    )
    werk = "".join(
        f'\n        <li>{e(w)}</li>' for w in project["werk"]
    )

    if fotos:
        items = "".join(
            f'''      <button type="button" class="galerij-item" data-foto="{i}" aria-label="Foto {i + 1} van {len(fotos)} vergroten">
        <img src="../{pad(f)}" alt="{e(project["titel"])}{e(in_plaats(project))} — foto {i + 1}" loading="lazy" decoding="async">
      </button>
'''
            for i, f in enumerate(fotos)
        )
        galerij = f'''    <div class="galerij" id="galerij">
{items}    </div>
'''
        aantal = len(fotos)
        telregel = f"{aantal} foto's van dit project" if aantal != 1 else "1 foto van dit project"
    else:
        galerij = '''    <p class="galerij-leeg">De foto's van dit project komen binnenkort online.</p>
'''
        telregel = "Foto's volgen"

    nav = ""
    if vorige or volgende:
        links = ""
        if vorige:
            links += f'''      <a class="proj-nav-link proj-nav-link--vorige" href="{vorige["slug"]}.html">
        <svg class="ic" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
        <span><span class="proj-nav-label">Vorige project</span><span class="proj-nav-titel">{e(vorige["titel"])}</span></span>
      </a>
'''
        if volgende:
            links += f'''      <a class="proj-nav-link proj-nav-link--volgende" href="{volgende["slug"]}.html">
        <span><span class="proj-nav-label">Volgende project</span><span class="proj-nav-titel">{e(volgende["titel"])}</span></span>
        <svg class="ic" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
      </a>
'''
        nav = f'''
<nav class="proj-nav" aria-label="Andere projecten">
{links}</nav>
'''

    return KOP.format(
        titel=e(project["titel"]), plaats=e(in_plaats(project)), lead=e(project["lead"])
    ) + f'''
<section class="proj-intro">
  <div class="proj-intro-deco" aria-hidden="true"></div>
  <a class="rec-terug" href="../index.html#projecten" data-fu><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>Terug naar alle projecten</a>
  <div class="proj-soort" data-fu>{e(project["soort"])}</div>
  <h1 data-fu>{e(project["titel"])}</h1>
  <p class="proj-lead" data-fu>{e(project["lead"])}</p>
  <div class="proj-chips" data-fu>{kenmerken}{duurchip(project, " " * 6)}
      <span class="chip-meta">{e(waar(project))}</span>
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
{nav}
<section class="cta-blok">
  <div class="cta-blok-inner" data-fu>
    <div class="cta-blok-deco" aria-hidden="true"></div>
    <div class="cta-blok-tekst">
      <h2>Geïnteresseerd geraakt?</h2>
      <p>Ik kom vrijblijvend langs, meet op en denk met je mee. Geen verkooppraatje, wel een eerlijk verhaal over wat er kan.</p>
      <p class="cta-blok-nb">De planning loopt zo'n 6 maanden vooruit, dus plan op tijd.</p>
    </div>
    <div class="cta-blok-knoppen">
      <a class="btn-primary" href="../index.html#offerte">Vraag offerte aan</a>
      <a class="btn-outline" href="tel:+31615956178"><svg class="ic" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>06 - 15 95 61 78</a>
    </div>
  </div>
</section>
''' + VOET


def main():
    uitvoer = WORTEL / "projecten"
    uitvoer.mkdir(exist_ok=True)

    kaarten = []
    for i, project in enumerate(PROJECTEN):
        fotos = foto_s(project["slug"])
        kaarten.append(kaart(project, fotos))
        pagina = projectpagina(
            project,
            fotos,
            PROJECTEN[i - 1] if i > 0 else None,
            PROJECTEN[i + 1] if i + 1 < len(PROJECTEN) else None,
        )
        (uitvoer / f"{project['slug']}.html").write_text(pagina, encoding="utf-8")
        print(f"  projecten/{project['slug']}.html — {len(fotos)} foto's")

    index = WORTEL / "index.html"
    bron = index.read_text(encoding="utf-8")
    nieuw, aantal = re.subn(
        r"(<!-- projecten:start -->\n).*?(\s*<!-- projecten:end -->)",
        lambda m: m.group(1) + "".join(kaarten) + m.group(2),
        bron,
        flags=re.DOTALL,
    )
    if aantal != 1:
        raise SystemExit("Markers <!-- projecten:start/end --> niet gevonden in index.html")
    index.write_text(nieuw, encoding="utf-8")
    print(f"  index.html — {len(PROJECTEN)} projectkaarten bijgewerkt")


if __name__ == "__main__":
    main()
