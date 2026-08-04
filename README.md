# De Badgast — website

One-pager voor **De Badgast**, het badkamerrenovatiebedrijf van Gerard Bartels in Roosendaal. Gebouwd op basis van het ontwerp uit Claude Design (handoff-bundel "De Badgast hero sectie", bestand *De Badgast One-pager*).

## Bestanden

| Bestand | Wat |
|---------|-----|
| `index.html` | De one-pager: hero, over Gerard, de formule, diensten, werkwijze, projecten, recensies, offerteformulier. |
| `recensies.html` | Losse pagina met alle recensies (gelinkt vanaf de one-pager). |
| `assets/site.css` | Gedeelde stylesheet voor beide pagina's. |
| `assets/site.js` | Gedeeld gedrag: sticky header met glas-effect, fade-in bij scrollen, projectencarrousel, offerteformulier. |
| `projecten/*.html` | Eén pagina per project, met alle foto's van dat project. Gegenereerd — niet met de hand aanpassen. |
| `tools/genereer-projecten.py` | Genereert de projectkaarten op de homepage en de projectpagina's. |
| `assets/` | Logo, embleem en foto's. Projectfoto's staan per project in `assets/projecten/<slug>/`. |
| `design.md` | Ouder merk-fundament uit de eerste (strandpaviljoen-)versie van dit project; niet meer leidend voor het huidige ontwerp. |

Geen build-stap nodig: het is een statische site (HTML + CSS + JS), met alleen Google Fonts (Manrope) als externe afhankelijkheid. Iconen (Lucide) zijn als SVG in de pagina's opgenomen.

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

Open daarna `http://localhost:8000`.

## Live zetten

De site wordt automatisch naar **GitHub Pages** gepubliceerd bij elke push naar de standaardbranch (workflow: `.github/workflows/pages.yml`). URL: `https://loubartels.github.io/debadgast/`. Een eigen domein koppel je via Settings → Pages → Custom domain.

## Offerteformulier

Het formulier verstuurt via [FormSubmit](https://formsubmit.co) naar `info@debadgast.nl` (geen account nodig). **Bij de allereerste inzending stuurt FormSubmit één activatiemail naar dat adres — klik daarin op de bevestigingsknop, daarna komen aanvragen gewoon per mail binnen.** Ander e-mailadres? Pas het adres aan in `assets/site.js` bij het blok "Offerteformulier".

## Projecten en foto's

Elk project heeft een eigen pagina met een fotogalerij; vanaf de homepage klik je erop door.

Foto's toevoegen aan een bestaand project:

1. Zet de foto's in `assets/projecten/<slug>/`. Ze verschijnen op alfabetische volgorde, dus nummer ze (`01-…`, `02-…`); de eerste foto wordt de omslagfoto op de homepage.
2. Draai `python3 tools/genereer-projecten.py`.

Een nieuw project toevoegen: maak de map `assets/projecten/<nieuwe-slug>/` met de foto's, voeg het project toe aan de lijst `PROJECTEN` bovenin `tools/genereer-projecten.py` en draai het script. De gegenereerde HTML wordt gecommit, dus de site zelf blijft zonder build-stap werken.

## Nog regelen

- [ ] **FormSubmit activeren.** Doe één testinzending op de live site en klik op de link in de activatiemail aan info@debadgast.nl.
- [ ] **Echte projectfoto's toevoegen.** Elk project heeft nu één gecomprimeerde foto uit de design-tool. Zie *Projecten en foto's* hierboven.
- [ ] **Projectgegevens controleren.** Plaats, jaartal, duur en omschrijvingen in `tools/genereer-projecten.py` komen uit het oorspronkelijke ontwerp en zijn nog niet door Gerard bevestigd.
